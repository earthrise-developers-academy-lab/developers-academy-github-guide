import { loadProjects, loadReferenceGeography, loadServiceAreas } from "./project-data-adapter.js";

const INITIAL_VIEW = Object.freeze({ center: [20, -20], zoom: 2 });
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const state = {
  projects: [],
  serviceAreas: [],
  filteredProjects: [],
  map: null,
  referenceLayer: null,
  projectLayer: null,
  selectedProjectId: null,
};

const elements = {};

function captureElements() {
  const ids = [
    "project-search", "from-year", "through-year", "topic-filter", "cohort-filter",
    "status-filter", "type-filter", "geography-filter", "clear-filters", "fit-results",
    "reset-map", "project-result-count", "project-live-status", "project-data-alert",
    "project-map", "project-map-fallback", "project-details", "project-empty-state",
  ];
  for (const id of ids) elements[id] = document.getElementById(id);
  elements.formControls = ids.slice(0, 8).map((id) => elements[id]);
  elements.rows = [...document.querySelectorAll("#project-explorer-table tbody tr[data-project-id]")];
  elements.detailButtons = [...document.querySelectorAll(".project-detail-button[data-project-id]")];
}

function normalize(value) {
  return String(value ?? "").trim().toLocaleLowerCase();
}

function projectYears(project) {
  return project.end_year === null
    ? `${project.start_year}–ongoing`
    : project.end_year === project.start_year
      ? String(project.start_year)
      : `${project.start_year}–${project.end_year}`;
}

function serviceAreasFor(projectId) {
  return state.serviceAreas.filter((feature) => feature?.properties?.project_id === projectId);
}

function searchableText(project) {
  return normalize([
    project.project_id, project.title, project.short_title, project.summary,
    ...(project.topics || []), ...(project.keywords || []),
  ].join(" "));
}

function currentFilters() {
  return {
    search: normalize(elements["project-search"].value),
    fromYear: Number(elements["from-year"].value) || null,
    throughYear: Number(elements["through-year"].value) || null,
    topic: elements["topic-filter"].value,
    cohort: elements["cohort-filter"].value,
    status: elements["status-filter"].value,
    type: elements["type-filter"].value,
    geography: elements["geography-filter"].value,
  };
}

function projectMatches(project, filters) {
  const effectiveEnd = project.end_year ?? 9999;
  if (filters.search && !searchableText(project).includes(filters.search)) return false;
  if (filters.fromYear && effectiveEnd < filters.fromYear) return false;
  if (filters.throughYear && project.start_year > filters.throughYear) return false;
  if (filters.topic && !project.topics.includes(filters.topic)) return false;
  if (filters.cohort && !project.cohorts.includes(filters.cohort)) return false;
  if (filters.status && project.status !== filters.status) return false;
  if (filters.type && project.project_type !== filters.type) return false;
  if (filters.geography) {
    const representations = serviceAreasFor(project.project_id)
      .map((feature) => feature.properties.geometry_representation);
    if (!representations.includes(filters.geography)) return false;
  }
  return true;
}

function filterProjects() {
  const filters = currentFilters();
  state.filteredProjects = state.projects.filter((project) => projectMatches(project, filters));
  renderProjectFeatures();
  synchronizeTable();
  updateResultStatus(true);
  updateEmptyState();
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b));
}

function populateSelect(select, values) {
  for (const value of uniqueSorted(values)) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    select.append(option);
  }
}

function populateFilters() {
  populateSelect(elements["topic-filter"], state.projects.flatMap((project) => project.topics));
  populateSelect(elements["cohort-filter"], state.projects.flatMap((project) => project.cohorts));
  populateSelect(elements["status-filter"], state.projects.map((project) => project.status));
  populateSelect(elements["type-filter"], state.projects.map((project) => project.project_type));
  populateSelect(elements["geography-filter"], state.serviceAreas.map((feature) => feature.properties?.geometry_representation));
}

function initializeMap() {
  if (!window.L) throw new Error("Leaflet 1.9.4 did not load");
  elements["project-map-fallback"]?.remove();
  state.map = window.L.map(elements["project-map"], {
    attributionControl: false,
    scrollWheelZoom: false,
    zoomAnimation: !reducedMotion,
    fadeAnimation: !reducedMotion,
    markerZoomAnimation: !reducedMotion,
  }).setView(INITIAL_VIEW.center, INITIAL_VIEW.zoom, { animate: false });
}

function renderReferenceLayer(reference) {
  if (!state.map) return;
  state.referenceLayer = window.L.geoJSON(reference, {
    interactive: false,
    style: { color: "#8a949b", weight: 1, fillColor: "#e6e8e6", fillOpacity: 1 },
  }).addTo(state.map);
  state.referenceLayer.bringToBack();
}

function representationStyle(feature) {
  const representation = feature?.properties?.geometry_representation;
  const styles = {
    "broad-service-region": { color: "#075985", weight: 3, dashArray: "8 5", fillColor: "#38bdf8", fillOpacity: .25 },
    "generalized-location": { color: "#7c2d12", weight: 4, dashArray: "3 5", fillColor: "#fb923c", fillOpacity: .28 },
    "representative-location": { color: "#365314", weight: 4, fillColor: "#84cc16", fillOpacity: .32 },
  };
  return styles[representation] || { color: "#374151", weight: 3, fillOpacity: .2 };
}

function activateProject(projectId, focusDetails = true) {
  const project = state.projects.find((item) => item.project_id === projectId);
  if (!project) return;
  state.selectedProjectId = projectId;
  renderProjectDetails(project);
  for (const row of elements.rows) {
    if (row.dataset.projectId === projectId) row.setAttribute("aria-selected", "true");
    else row.removeAttribute("aria-selected");
  }
  if (focusDetails) elements["project-details"].focus({ preventScroll: false });
}

function makePathAccessible(layer, feature) {
  if (typeof layer.getLayers === "function") {
    for (const child of layer.getLayers()) makePathAccessible(child, feature);
    return;
  }
  const apply = () => {
    const path = typeof layer.getElement === "function" ? layer.getElement() : null;
    if (!path) return;
    const project = state.projects.find((item) => item.project_id === feature.properties.project_id);
    path.setAttribute("tabindex", "0");
    path.setAttribute("role", "button");
    path.setAttribute("aria-label", `View ${project?.title || feature.properties.project_id}: ${feature.properties.label}`);
    path.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activateProject(feature.properties.project_id);
      }
    });
  };
  layer.on("add", apply);
  apply();
  layer.on("click", () => activateProject(feature.properties.project_id));
}

function renderProjectFeatures() {
  if (!state.map) return;
  if (state.projectLayer) state.projectLayer.remove();
  const visibleIds = new Set(state.filteredProjects.map((project) => project.project_id));
  const features = state.serviceAreas.filter((feature) => visibleIds.has(feature.properties?.project_id));
  state.projectLayer = window.L.geoJSON({ type: "FeatureCollection", features }, {
    style: representationStyle,
    pointToLayer(feature, latlng) {
      const project = state.projects.find((item) => item.project_id === feature.properties.project_id);
      return window.L.marker(latlng, {
        keyboard: true,
        title: `View ${project?.title || feature.properties.project_id}`,
        alt: `Synthetic project location for ${project?.title || feature.properties.project_id}`,
        autoPanOnFocus: true,
      });
    },
    onEachFeature(feature, layer) {
      makePathAccessible(layer, feature);
    },
  }).addTo(state.map);
}

function synchronizeTable() {
  const visibleIds = new Set(state.filteredProjects.map((project) => project.project_id));
  for (const row of elements.rows) row.hidden = !visibleIds.has(row.dataset.projectId);
}

function setDetailText(field, value) {
  const target = document.querySelector(`[data-detail="${field}"]`);
  if (target) target.textContent = value || "Not available";
}

function renderProjectDetails(project) {
  const features = serviceAreasFor(project.project_id);
  elements["project-details"].querySelector(".project-details-placeholder").hidden = true;
  elements["project-details"].querySelector(".project-details-content").hidden = false;
  setDetailText("project_id", project.project_id);
  setDetailText("title", project.title);
  setDetailText("summary", project.summary);
  setDetailText("years", projectYears(project));
  setDetailText("cohorts", project.cohorts.join(", "));
  setDetailText("topics", project.topics.join(", "));
  setDetailText("status", project.status);
  setDetailText("project_type", project.project_type);
  setDetailText("handoff_status", project.handoff_status);
  setDetailText("geography_labels", features.length ? features.map((item) => item.properties.label).join("; ") : "No mapped service area");
  setDetailText("representations", features.length ? uniqueSorted(features.map((item) => item.properties.geometry_representation)).join(", ") : "None");
  setDetailText("precisions", features.length ? uniqueSorted(features.map((item) => item.properties.geometry_precision)).join(", ") : "None");
  const links = elements["project-details"].querySelector(".project-detail-links");
  links.replaceChildren();
  const labels = { developedia_url: "Open local project record", handoff_url: "Open local handoff", repository_url: "Open repository", application_url: "Open application" };
  for (const [field, label] of Object.entries(labels)) {
    if (!project[field]) continue;
    const anchor = document.createElement("a");
    anchor.href = project[field];
    anchor.textContent = label;
    links.append(anchor);
  }
  if (!links.children.length) {
    const note = document.createElement("p");
    note.textContent = "No local project links are available for this synthetic record.";
    links.append(note);
  }
}

function clearSelection() {
  state.selectedProjectId = null;
  const content = elements["project-details"].querySelector(".project-details-content");
  const placeholder = elements["project-details"].querySelector(".project-details-placeholder");
  content.hidden = true;
  placeholder.hidden = false;
  for (const row of elements.rows) row.removeAttribute("aria-selected");
}

function updateResultStatus(announce) {
  const visibleIds = new Set(state.filteredProjects.map((project) => project.project_id));
  const mappedCount = visibleIds.size
    ? new Set(state.serviceAreas.filter((feature) => visibleIds.has(feature.properties?.project_id)).map((feature) => feature.properties.project_id)).size
    : 0;
  const message = `${state.filteredProjects.length} projects shown; ${mappedCount} have mapped service areas.`;
  elements["project-result-count"].textContent = message;
  if (announce) elements["project-live-status"].textContent = message;
  elements["fit-results"].disabled = mappedCount === 0 || !state.map;
}

function updateEmptyState() {
  elements["project-empty-state"].hidden = state.filteredProjects.length !== 0;
}

function showAlert(message) {
  elements["project-data-alert"].hidden = false;
  elements["project-data-alert"].textContent = message;
}

function disableInteractiveControls() {
  for (const control of [...elements.formControls, elements["clear-filters"], elements["fit-results"], elements["reset-map"]]) {
    control.disabled = true;
  }
}

function clearFilters() {
  for (const control of elements.formControls) control.value = "";
  filterProjects();
}

function fitMapToResults() {
  if (!state.map || !state.projectLayer || !state.projectLayer.getLayers().length) {
    elements["project-live-status"].textContent = "No mapped results are available to fit.";
    return;
  }
  state.map.fitBounds(state.projectLayer.getBounds(), { padding: [24, 24], animate: !reducedMotion });
}

function resetMap() {
  if (state.map) state.map.setView(INITIAL_VIEW.center, INITIAL_VIEW.zoom, { animate: !reducedMotion });
}

function bindEvents() {
  for (const control of elements.formControls) {
    control.addEventListener(control.type === "search" ? "input" : "change", filterProjects);
  }
  elements["clear-filters"].addEventListener("click", clearFilters);
  elements["fit-results"].addEventListener("click", fitMapToResults);
  elements["reset-map"].addEventListener("click", resetMap);
  for (const button of elements.detailButtons) {
    button.hidden = false;
    button.addEventListener("click", () => activateProject(button.dataset.projectId));
  }
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && state.selectedProjectId) {
      clearSelection();
      elements["project-live-status"].textContent = "Project selection cleared.";
    }
  });
}

async function initializeExplorer() {
  captureElements();
  if (!elements["project-map"] || !document.querySelector("[data-project-explorer]")) return;

  // Quarto 1.9 emits role="menu" on its narrow-screen toggle; a button role
  // preserves the generated control's actual semantics for this page.
  document.querySelector(".navbar-toggler")?.setAttribute("role", "button");

  const [projectsResult, serviceResult, referenceResult] = await Promise.allSettled([
    loadProjects(), loadServiceAreas(), loadReferenceGeography(),
  ]);
  if (projectsResult.status === "rejected") {
    disableInteractiveControls();
    showAlert("Interactive project filtering is unavailable because the local project registry could not be loaded. The complete static project table remains available below.");
    return;
  }

  state.projects = projectsResult.value.projects;
  state.filteredProjects = [...state.projects];
  if (serviceResult.status === "fulfilled") state.serviceAreas = serviceResult.value.features;
  else showAlert("Geographic features are unavailable. Project filtering, details, and the complete table remain available.");

  try {
    initializeMap();
    if (referenceResult.status === "fulfilled") renderReferenceLayer(referenceResult.value);
    else showAlert("The Natural Earth context layer is unavailable. Synthetic project features may still be used on a neutral map background.");
  } catch (error) {
    showAlert("The interactive map is unavailable. Project filters, details, and the complete static table remain available.");
  }

  populateFilters();
  bindEvents();
  renderProjectFeatures();
  synchronizeTable();
  updateResultStatus(false);
  updateEmptyState();
}

initializeExplorer().catch((error) => {
  console.error("Project explorer initialization failed.", error);
  captureElements();
  disableInteractiveControls();
  showAlert("The interactive explorer could not initialize. The complete static project table remains available below.");
});
