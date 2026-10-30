"use strict";

// Shared by the map (app.js) and the guide (guide.js).
const API = "/api";
const SMALL_WORDS = new Set(["and", "of", "the", "upon"]);

/** Turn an extent slug such as "isle-of-wight" into "Isle of Wight". */
function extentName(slug) {
  return slug.split("-")
    .map((word, index) => (index > 0 && SMALL_WORDS.has(word) ? word : word[0].toUpperCase() + word.slice(1)))
    .join(" ");
}

/** Format a date as "20 October 2026", read in UTC so a data snapshot keeps its own date. */
function formatDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" });
}

/** Describe the engine state that /api/health reports. */
function stateLabel(health) {
  switch (health.state) {
    case "ready": return "Ready";
    case "waiting_for_tiles": return "Waiting for the tile build job";
    case "downloading": {
      const total = health.manifest ? health.manifest.size_bytes : 0;
      return `Copying tiles ${total ? Math.floor((100 * health.bytes_copied) / total) : 0}%`;
    }
    case "loading": return "Loading tiles";
    case "failed": return "Failed";
    default: return "Starting";
  }
}

/** POST a Valhalla request; resolve with the HTTP response and its parsed JSON body. */
async function callApi(action, body) {
  const response = await fetch(`${API}/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
  const text = await response.text();
  try {
    return { response, payload: JSON.parse(text) };
  } catch {
    throw new Error("The App returned a page instead of JSON. Your session may have expired: reload the page.");
  }
}
