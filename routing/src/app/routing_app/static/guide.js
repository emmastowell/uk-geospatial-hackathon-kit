"use strict";

// Example requests for the console, all inside Great Britain.
const EXAMPLES = [
  {
    id: "route",
    label: "Route: walk from King's Cross to the British Museum",
    action: "route",
    body: {
      locations: [{ lat: 51.5308, lon: -0.1238 }, { lat: 51.5194, lon: -0.1270 }],
      costing: "pedestrian",
      directions_options: { units: "kilometers", language: "en-GB" },
    },
  },
  {
    id: "isochrone",
    label: "Isochrone: 15 minutes by bike from Bristol Temple Meads",
    action: "isochrone",
    body: { locations: [{ lat: 51.4491, lon: -2.5813 }], costing: "bicycle", contours: [{ time: 15 }], polygons: true },
  },
  {
    id: "matrix",
    label: "Matrix: London, Manchester and Glasgow to Birmingham and Leeds",
    action: "sources_to_targets",
    body: {
      sources: [{ lat: 51.5074, lon: -0.1278 }, { lat: 53.4808, lon: -2.2426 }, { lat: 55.8642, lon: -4.2518 }],
      targets: [{ lat: 52.4862, lon: -1.8904 }, { lat: 53.8008, lon: -1.5491 }],
      costing: "auto",
    },
  },
  {
    id: "optimised",
    label: "Optimised route: four stops in Manchester, back to the start",
    action: "optimized_route",
    body: {
      locations: [
        { lat: 53.4774, lon: -2.2309 },
        { lat: 53.4631, lon: -2.2913 },
        { lat: 53.4831, lon: -2.2004 },
        { lat: 53.4721, lon: -2.2980 },
        { lat: 53.4774, lon: -2.2309 },
      ],
      costing: "auto",
    },
  },
  {
    id: "locate",
    label: "Locate: where a point near Buckingham Palace lands on the network",
    action: "locate",
    body: { locations: [{ lat: 51.5014, lon: -0.1419 }], costing: "auto" },
  },
  {
    id: "trace",
    label: "Map matching: a GPS trace along The Mall",
    action: "trace_route",
    body: {
      shape: [
        { lat: 51.5058, lon: -0.1306 },
        { lat: 51.5047, lon: -0.1330 },
        { lat: 51.5036, lon: -0.1355 },
        { lat: 51.5025, lon: -0.1380 },
        { lat: 51.5017, lon: -0.1400 },
      ],
      costing: "auto",
      shape_match: "map_snap",
      directions_options: { units: "kilometers", language: "en-GB" },
    },
  },
  { id: "status", label: "Status: Valhalla's version and the tile date", action: "status", body: {} },
];

const COSTING_LABELS = { auto: "Car", pedestrian: "Walking", bicycle: "Cycling", bus: "Bus", truck: "Lorry" };
// Responses show this many items of a long list before shortening it.
const MAX_LIST_ITEMS = 6;
const numbers = new Intl.NumberFormat("en-GB");

const guide = {
  facts: document.getElementById("guide-facts"),
  limits: document.getElementById("guide-limits-body"),
  isochroneLimits: document.getElementById("guide-limits-isochrone"),
  traceLimits: document.getElementById("guide-limits-trace"),
  capacity: document.getElementById("guide-limits-capacity"),
  example: document.getElementById("console-example"),
  action: document.getElementById("console-action"),
  request: document.getElementById("console-request"),
  send: document.getElementById("console-run"),
  status: document.getElementById("console-status"),
  response: document.getElementById("console-response"),
};

function element(tag, ...children) {
  const created = document.createElement(tag);
  created.append(...children);
  return created;
}

function renderFacts(health) {
  const rows = [["Status", stateLabel(health)]];
  const manifest = health.manifest;
  if (manifest) {
    rows.push(
      ["Coverage", extentName(manifest.extent)],
      ["Road data", `OpenStreetMap snapshot of ${formatDate(manifest.osm_last_modified)}`],
      ["Tiles", `${(manifest.size_bytes / 1e9).toFixed(1)} GB, built on ${formatDate(manifest.built_at)} with Valhalla ${manifest.pyvalhalla_version}`],
    );
  }
  rows.push(["Capacity", `${health.actor_pool_size} requests at a time`]);
  guide.facts.replaceChildren(...rows.flatMap(([term, value]) => [element("dt", term), element("dd", value)]));
}

function renderLimits(health) {
  const limits = health.limits;
  if (!limits || !limits.costing) return;
  guide.limits.replaceChildren(...Object.entries(limits.costing).map(([costing, values]) => element(
    "tr",
    element("td", `${COSTING_LABELS[costing] || costing} `, element("code", costing)),
    element("td", numbers.format(values.route_locations)),
    element("td", `${numbers.format(values.route_km)} km`),
    element("td", numbers.format(values.matrix_pairs)),
    element("td", `${numbers.format(values.matrix_km)} km`),
  )));
  const { contours, minutes, km } = limits.isochrone;
  guide.isochroneLimits.textContent = `Isochrones: up to ${contours} contours from one location, each up to ${minutes} minutes or ${km} km.`;
  guide.traceLimits.textContent = `GPS traces: up to ${numbers.format(limits.trace.points)} points covering up to ${numbers.format(limits.trace.km)} km.`;
  guide.capacity.textContent = `The App serves ${health.actor_pool_size} requests at a time and queues the rest. The Databricks Apps proxy ends any request after 120 seconds, so split very large matrices into batches.`;
}

/** Shorten long lists and strings so a response stays readable. */
function abbreviate(value) {
  if (Array.isArray(value)) {
    if (value.length <= MAX_LIST_ITEMS) return value.map(abbreviate);
    return [...value.slice(0, 3).map(abbreviate), `… ${numbers.format(value.length - 3)} more`];
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, abbreviate(item)]));
  }
  if (typeof value === "string" && value.length > 120) {
    return `${value.slice(0, 60)}… (${numbers.format(value.length)} characters)`;
  }
  return value;
}

function selectedExample() {
  return EXAMPLES.find((example) => example.id === guide.example.value);
}

function loadExample() {
  const example = selectedExample();
  guide.action.textContent = example.action;
  guide.request.value = JSON.stringify(example.body, null, 2);
}

async function sendRequest() {
  guide.send.disabled = true;
  guide.status.textContent = "Sending…";
  delete guide.status.dataset.ok;
  const started = performance.now();
  try {
    const { response, payload } = await callApi(selectedExample().action, guide.request.value);
    const seconds = ((performance.now() - started) / 1000).toFixed(2);
    guide.status.textContent = `HTTP ${response.status} in ${seconds} s`;
    guide.status.dataset.ok = String(response.ok);
    guide.response.textContent = JSON.stringify(abbreviate(payload), null, 2);
  } catch (error) {
    guide.status.textContent = error.message;
    guide.status.dataset.ok = "false";
  } finally {
    guide.send.disabled = false;
  }
}

guide.example.replaceChildren(...EXAMPLES.map((example) => {
  const option = element("option", example.label);
  option.value = example.id;
  return option;
}));
guide.example.addEventListener("change", loadExample);
guide.send.addEventListener("click", sendRequest);
loadExample();

document.querySelectorAll("[data-base-url]").forEach((node) => { node.textContent = `${window.location.origin}${API}`; });

document.querySelectorAll("[data-copy]").forEach((button) => button.addEventListener("click", async () => {
  await navigator.clipboard.writeText(document.getElementById(button.dataset.copy).textContent);
  button.textContent = "Copied";
  window.setTimeout(() => { button.textContent = "Copy"; }, 1500);
}));

window.addEventListener("routing:health", (event) => {
  const health = event.detail;
  renderFacts(health);
  renderLimits(health);
  document.querySelectorAll("[data-tiles-dir]").forEach((node) => { node.textContent = health.tiles_dir; });
  // tiles_dir is /Volumes/<catalog>/<schema>/<volume>/tiles/<extent>.
  const [, root, catalog, schema, volume, , extent] = health.tiles_dir.split("/");
  if (root !== "Volumes" || !extent) return;
  document.querySelectorAll("[data-volume-name]").forEach((node) => { node.textContent = `${catalog}.${schema}.${volume}`; });
  document.querySelectorAll("[data-extent-slug]").forEach((node) => { node.textContent = extent; });
  document.querySelectorAll("[data-extent-name]").forEach((node) => { node.textContent = extentName(extent); });
});
