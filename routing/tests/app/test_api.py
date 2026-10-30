import json
from typing import Any

import pytest
from fastapi.testclient import TestClient

from routing_app.errors import RoutingError
from routing_app.main import create_app


class FakeEngine:
    def __init__(self, response: str = '{"trip": {}}', error: RoutingError | None = None) -> None:
        self.response = response
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def call(self, action: str, request: str) -> str:
        self.calls.append((action, request))
        if self.error:
            raise self.error
        return self.response


class FakeHost:
    def __init__(self, engine: FakeEngine | None) -> None:
        self.engine = engine
        self.started = False

    def start(self) -> None:
        self.started = True

    def health(self) -> dict[str, Any]:
        return {"state": "ready" if self.engine else "downloading"}


def client_for(engine: FakeEngine | None) -> TestClient:
    return TestClient(create_app(FakeHost(engine)))


def test_health_reports_the_service_state() -> None:
    with client_for(None) as client:
        assert client.get("/api/health").json() == {"state": "downloading"}


def test_actions_wait_for_the_engine() -> None:
    with client_for(None) as client:
        response = client.post("/api/route", json={"locations": []})
    assert response.status_code == 503
    assert response.json()["error"] == "Routing engine is not ready (downloading)"


def test_post_passes_the_request_through_and_returns_valhalla_json() -> None:
    engine = FakeEngine('{"trip": {"summary": {"time": 60}}}')
    with client_for(engine) as client:
        response = client.post("/api/sources_to_targets", json={"sources": [], "targets": []})
    assert response.json() == {"trip": {"summary": {"time": 60}}}
    assert engine.calls == [("sources_to_targets", '{"sources":[],"targets":[]}')]


def test_get_takes_the_request_from_the_json_query_parameter() -> None:
    engine = FakeEngine()
    with client_for(engine) as client:
        client.get("/api/isochrone", params={"json": json.dumps({"costing": "pedestrian"})})
    assert engine.calls == [("isochrone", '{"costing":"pedestrian"}')]


@pytest.mark.parametrize(
    ("action", "body", "status", "error_code"),
    [
        ("teleport", "{}", 404, 106),
        ("route", "not json", 400, 100),
        ("route", "[1, 2]", 400, 100),
    ],
)
def test_bad_requests_get_valhalla_error_codes(
    action: str, body: str, status: int, error_code: int
) -> None:
    with client_for(FakeEngine()) as client:
        response = client.post(f"/api/{action}", content=body)
    assert response.status_code == status
    assert response.json()["error_code"] == error_code


def test_engine_errors_keep_valhallas_status_and_code() -> None:
    error = RoutingError(400, 171, "No suitable edges near location", "Bad Request")
    with client_for(FakeEngine(error=error)) as client:
        response = client.post("/api/route", json={"locations": []})
    assert response.status_code == 400
    assert response.json() == error.body()


def test_serves_the_demo_map() -> None:
    with client_for(None) as client:
        page = client.get("/")
    assert page.status_code == 200
    assert "Valhalla routing" in page.text
