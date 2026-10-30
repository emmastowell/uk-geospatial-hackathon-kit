"use strict";

// The URL hash picks the view: #guide and #guide-<section> show the guide, anything else
// shows the map. Hashes keep the back button working and let people link to a section.
const VIEWS = {
  map: document.getElementById("map-view"),
  guide: document.getElementById("guide-view"),
};

function showView() {
  const hash = window.location.hash;
  const name = hash.startsWith("#guide") ? "guide" : "map";
  Object.entries(VIEWS).forEach(([key, view]) => { view.hidden = key !== name; });
  document.querySelectorAll("[data-view]").forEach((link) => {
    if (link.dataset.view === name) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  if (name === "map") {
    map.resize();
    return;
  }
  const section = hash.length > 1 ? document.getElementById(hash.slice(1)) : null;
  if (section) section.scrollIntoView();
  else VIEWS.guide.scrollTop = 0;
}

window.addEventListener("hashchange", showView);
showView();
