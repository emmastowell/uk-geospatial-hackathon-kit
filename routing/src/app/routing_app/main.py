"""FastAPI entry point: Valhalla's HTTP API under /api and the demo map at /.

Every Valhalla action keeps its usual name and JSON body, so Valhalla's API docs and
clients work against ``<app url>/api``. Requests from outside the browser need an OAuth
token for the App (see the quickstart notebook).
"""

import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Protocol

from fastapi import FastAPI, Query, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from routing_app.errors import RoutingError
from routing_app.service import RoutingService
from routing_app.settings import Settings


class Engine(Protocol):
    def call(self, action: str, request: str) -> str: ...


class EngineHost(Protocol):
    """What the API needs from the service that warms the engine up."""

    @property
    def engine(self) -> Engine | None: ...

    def start(self) -> object: ...

    def health(self) -> dict[str, Any]: ...


STATIC_DIR = Path(__file__).parent / "static"
# The actions the engine serves, in the order Valhalla documents them.
PUBLIC_ACTIONS = (
    "route",
    "optimized_route",
    "sources_to_targets",
    "isochrone",
    "locate",
    "trace_route",
    "trace_attributes",
    "expansion",
    "centroid",
    "status",
)
SUPPORTED_ACTIONS = frozenset(PUBLIC_ACTIONS) | {"matrix"}


def parse_request(raw: str | bytes) -> str:
    """Return the request as compact JSON, or raise Valhalla's parse error."""

    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError as error:
        message = f"Failed to parse json request: {error}"
        raise RoutingError(400, 100, message, "Bad Request") from error
    if not isinstance(payload, dict):
        message = "Failed to parse json request: expected an object"
        raise RoutingError(400, 100, message, "Bad Request")
    return json.dumps(payload, separators=(",", ":"))


def create_app(service: EngineHost) -> FastAPI:
    """Build the App around a routing service that is still warming up."""

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        service.start()
        yield

    app = FastAPI(
        title="Valhalla routing",
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )
    app.add_middleware(GZipMiddleware, minimum_size=1024)

    @app.exception_handler(RoutingError)
    async def routing_error(_: Request, error: RoutingError) -> JSONResponse:
        return JSONResponse(error.body(), status_code=error.status_code)

    async def dispatch(action: str, raw: str | bytes) -> Response:
        if action not in SUPPORTED_ACTIONS:
            raise RoutingError(404, 106, f"Try any of: {', '.join(PUBLIC_ACTIONS)}", "Not Found")
        engine = service.engine
        if engine is None:
            message = f"Routing engine is not ready ({service.health()['state']})"
            raise RoutingError(503, 503, message, "Service Unavailable")
        result = await run_in_threadpool(engine.call, action, parse_request(raw))
        return Response(result, media_type="application/json")

    @app.get("/api/health")
    async def health() -> dict[str, Any]:
        return service.health()

    @app.post("/api/{action}")
    async def post_action(action: str, request: Request) -> Response:
        return await dispatch(action, await request.body())

    @app.get("/api/{action}")
    async def get_action(action: str, payload: str = Query("{}", alias="json")) -> Response:
        return await dispatch(action, payload)

    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="map")
    return app


def build_app() -> FastAPI:
    """Uvicorn factory (``--factory``): configure the service from the environment."""

    return create_app(RoutingService.from_settings(Settings.from_env()))
