"use strict";

const BASEMAP = "https://tiles.openfreemap.org/styles/positron";
// Nearest to furthest: green through amber, so the shortest times read as "close".
const CONTOUR_COLOURS = ["1a9850", "91cf60", "fdae61", "d73027"];
const DEFAULT_CONTOURS = { auto: "10, 20, 30, 45", pedestrian: "5, 10, 15, 20", bicycle: "10, 20, 30, 40" };
const EMPTY = { type: "FeatureCollection", features: [] };

const ui = {
  status: document.getElementById("status"),
  extent: document.getElementById("extent"),
  error: document.getElementById("error"),
  routeHint: document.getElementById("route-hint"),
  isochroneHint: document.getElementById("isochrone-hint"),
  summary: document.getElementById("route-summary"),
  maneuvers: document.getElementById("maneuvers"),
  contours: document.getElementById("contours"),
  legend: document.getElementById("legend"),
  apiBase: document.getElementById("api-base"),
  lastRequest: document.getElementById("last-request"),
  copyRequest: document.getElementById("copy-request"),
};

const state = {
  tab: "route", costing: "auto", ready: false, start: null, end: null, origin: null, shape: [], framed: null,
};

// Great Britain is the default extract; smaller extents replace this once /api/health
// names them, so the first click lands on roads the engine can actually route.
const DEFAULT_VIEW = { center: [-2.6, 54.3], zoom: 5.4 };
const EXTENT_VIEWS = {
  "great-britain": DEFAULT_VIEW,
  "isle-of-wight": { center: [-1.32, 50.67], zoom: 10.5 },
};

const map = new maplibregl.Map({
  container: "map",
  style: BASEMAP,
  ...DEFAULT_VIEW,
  attributionControl: { compact: true },
});
map.addControl(new maplibregl.NavigationControl(), "top-right");
map.addControl(new maplibregl.ScaleControl({ unit: "metric" }), "bottom-right");

map.on("load", () => {
  map.addSource("isochrone", { type: "geojson", data: EMPTY });
  map.addLayer({ id: "isochrone-fill", type: "fill", source: "isochrone",
    paint: { "fill-color": ["get", "fill"], "fill-opacity": 0.22 } });
  map.addLayer({ id: "isochrone-line", type: "line", source: "isochrone",
    paint: { "line-color": ["get", "fill"], "line-width": 1.5 } });
  map.addSource("route", { type: "geojson", data: EMPTY });
  map.addLayer({ id: "route-casing", type: "line", source: "route",
    layout: { "line-cap": "round", "line-join": "round" },
    paint: { "line-color": "#ffffff", "line-width": 9 } });
  map.addLayer({ id: "route-line", type: "line", source: "route",
    layout: { "line-cap": "round", "line-join": "round" },
    paint: { "line-color": "#1d4ed8", "line-width": 5 } });
});

/** Decode a Valhalla polyline6 string into [lon, lat] pairs. */
function decodePolyline(encoded, precision = 6) {
  const factor = 10 ** precision;
  const coordinates = [];
  let index = 0;
  let lat = 0;
  let lon = 0;
  const next = () => {
    let result = 0;
    let shift = 0;
    let byte;
    do {
      byte = encoded.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);
    return result & 1 ? ~(result >> 1) : result >> 1;
  };
  while (index < encoded.length) {
    lat += next();
    lon += next();
    coordinates.push([lon / factor, lat / factor]);
  }
  return coordinates;
}

function showError(message) {
  ui.error.textContent = message;
  ui.error.hidden = !message;
}

async function valhalla(action, body) {
  ui.lastRequest.textContent = `POST ${API}/${action}\n${JSON.stringify(body, null, 2)}`;
  const { response, payload } = await callApi(action, body);
  if (!response.ok) throw new Error(payload.error || `${response.status} ${response.statusText}`);
  return payload;
}

function formatDuration(seconds) {
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes} min`;
  return `${Math.floor(minutes / 60)} h ${minutes % 60} min`;
}

function formatDistance(km) {
  return km < 1 ? `${Math.round(km * 1000)} m` : `${km.toFixed(1)} km`;
}

function marker(colour, onMove) {
  const created = new maplibregl.Marker({ color: colour, draggable: true });
  created.on("dragend", onMove);
  return created;
}

function point(markerInstance) {
  const { lng, lat } = markerInstance.getLngLat();
  return { lat: Number(lat.toFixed(6)), lon: Number(lng.toFixed(6)) };
}

async function planRoute() {
  if (!state.start || !state.end) return;
  showError("");
  try {
    const response = await valhalla("route", {
      locations: [point(state.start), point(state.end)],
      costing: state.costing,
      directions_options: { units: "kilometers", language: "en-GB" },
    });
    const legs = response.trip.legs;
    const shape = legs.flatMap((leg) => decodePolyline(leg.shape));
    state.shape = shape;
    map.getSource("route").setData({ type: "Feature", geometry: { type: "LineString", coordinates: shape }, properties: {} });
    const { length, time } = response.trip.summary;
    ui.summary.innerHTML = `${formatDistance(length)} · ${formatDuration(time)}<small>${(length / 1.609344).toFixed(1)} miles</small>`;
    ui.summary.hidden = false;
    ui.maneuvers.replaceChildren(...legs.flatMap((leg) => leg.maneuvers).map((step) => {
      const item = document.createElement("li");
      const text = document.createElement("span");
      text.textContent = step.instruction;
      const distance = document.createElement("span");
      distance.className = "distance";
      distance.textContent = step.length ? formatDistance(step.length) : "";
      item.append(text, distance);
      item.addEventListener("click", () => map.flyTo({ center: shape[step.begin_shape_index], zoom: 16 }));
      return item;
    }));
  } catch (error) {
    map.getSource("route").setData(EMPTY);
    ui.summary.hidden = true;
    ui.maneuvers.replaceChildren();
    showError(error.message);
  }
}

function parseContours() {
  const minutes = ui.contours.value.split(/[\s,]+/).map(Number).filter((value) => value > 0);
  return [...new Set(minutes)].sort((a, b) => a - b).slice(0, 4);
}

async function planIsochrone() {
  if (!state.origin) return;
  showError("");
  const minutes = parseContours();
  try {
    const response = await valhalla("isochrone", {
      locations: [point(state.origin)],
      costing: state.costing,
      contours: minutes.map((time, index) => ({ time, color: CONTOUR_COLOURS[index] })),
      polygons: true,
      denoise: 0.3,
      generalize: 40,
    });
    response.features.sort((a, b) => b.properties.contour - a.properties.contour);
    map.getSource("isochrone").setData(response);
    ui.legend.replaceChildren(...minutes.map((time, index) => {
      const item = document.createElement("li");
      const swatch = document.createElement("span");
      swatch.className = "swatch";
      swatch.style.background = `#${CONTOUR_COLOURS[index]}`;
      item.append(swatch, `${time} min`);
      return item;
    }));
  } catch (error) {
    map.getSource("isochrone").setData(EMPTY);
    ui.legend.replaceChildren();
    showError(error.message);
  }
}

map.on("click", (event) => {
  if (!state.ready) {
    showError("The routing engine is still loading its tiles.");
    return;
  }
  if (state.tab === "route") {
    if (!state.start) {
      state.start = marker("#15803d", planRoute).setLngLat(event.lngLat).addTo(map);
      return;
    }
    state.end = (state.end || marker("#b91c1c", planRoute)).setLngLat(event.lngLat).addTo(map);
    planRoute();
  } else if (state.tab === "isochrone") {
    state.origin = (state.origin || marker("#1d4ed8", planIsochrone)).setLngLat(event.lngLat).addTo(map);
    planIsochrone();
  }
});

function selectTab(tab) {
  state.tab = tab;
  document.querySelectorAll("[data-tab]").forEach((button) => button.setAttribute("aria-selected", String(button.dataset.tab === tab)));
  document.querySelectorAll("[data-panel]").forEach((panel) => { panel.hidden = panel.dataset.panel !== tab; });
  const routeVisible = tab !== "isochrone" ? "visible" : "none";
  const isochroneVisible = tab !== "route" ? "visible" : "none";
  ["route-casing", "route-line"].forEach((id) => map.getLayer(id) && map.setLayoutProperty(id, "visibility", routeVisible));
  ["isochrone-fill", "isochrone-line"].forEach((id) => map.getLayer(id) && map.setLayoutProperty(id, "visibility", isochroneVisible));
  [state.start, state.end].forEach((item) => item && item.getElement().style.setProperty("display", tab === "isochrone" ? "none" : ""));
  if (state.origin) state.origin.getElement().style.setProperty("display", tab === "route" ? "none" : "");
  showError("");
}

document.querySelectorAll("[data-tab]").forEach((button) => button.addEventListener("click", () => selectTab(button.dataset.tab)));

document.querySelectorAll("[data-costing]").forEach((button) => button.addEventListener("click", () => {
  state.costing = button.dataset.costing;
  document.querySelectorAll("[data-costing]").forEach((other) => other.setAttribute("aria-checked", String(other === button)));
  ui.contours.value = DEFAULT_CONTOURS[state.costing];
  planRoute();
  planIsochrone();
}));

ui.contours.addEventListener("change", planIsochrone);
ui.apiBase.textContent = `${window.location.origin}${API}`;
ui.copyRequest.addEventListener("click", () => navigator.clipboard.writeText(ui.lastRequest.textContent.split("\n").slice(1).join("\n")));

function fitBounds(bbox) {
  if (!bbox) return false;
  map.fitBounds([[bbox.west, bbox.south], [bbox.east, bbox.north]], { padding: 48, maxZoom: 12, duration: 800 });
  return true;
}

function frameExtent(health) {
  const slug = health.manifest && health.manifest.extent;
  if (!slug || state.framed === slug) return;
  const name = extentName(slug);
  if (ui.routeHint) {
    ui.routeHint.textContent = `Click the map in ${name} to set a start, then a destination. Click again to move the destination, or drag either marker.`;
  }
  if (ui.isochroneHint) {
    ui.isochroneHint.textContent = `Click the map in ${name} to set an origin. Areas show where you can reach within each time.`;
  }
  if (fitBounds(health.manifest.bbox)) {
    state.framed = slug;
    return;
  }
  const view = EXTENT_VIEWS[slug];
  if (view) {
    map.easeTo({ ...view, duration: 800 });
    state.framed = slug;
  }
}

function showHealth(health) {
  if (health.manifest) {
    const { extent, osm_last_modified: snapshot } = health.manifest;
    ui.extent.textContent = `${extentName(extent)} · OpenStreetMap ${formatDate(snapshot)}`;
    frameExtent(health);
  }
  ui.status.dataset.state = health.state;
  ui.status.textContent = stateLabel(health);
  ui.status.title = health.detail || "";
}

async function pollHealth() {
  let delay = 3000;
  try {
    const health = await (await fetch(`${API}/health`)).json();
    showHealth(health);
    window.dispatchEvent(new CustomEvent("routing:health", { detail: health }));
    state.ready = health.state === "ready";
    if (health.state === "failed") showError(health.detail);
    if (state.ready) delay = 60000;
  } catch (error) {
    ui.status.dataset.state = "failed";
    ui.status.textContent = "Unreachable";
  }
  window.setTimeout(pollHealth, delay);
}

pollHealth();
