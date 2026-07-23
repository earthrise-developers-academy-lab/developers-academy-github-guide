const RESOURCE_URLS = Object.freeze({
  projects: new URL("../../data/projects.json", import.meta.url),
  serviceAreas: new URL("../../data/project-service-areas.geojson", import.meta.url),
  referenceGeography: new URL("../../data/reference/natural-earth-land-110m.geojson", import.meta.url),
});

export class ProjectDataError extends Error {
  constructor(resource, message, cause) {
    super(`${resource}: ${message}`, { cause });
    this.name = "ProjectDataError";
    this.resource = resource;
  }
}

async function loadJson(resource, url, validate) {
  let response;
  try {
    response = await fetch(url, { credentials: "same-origin" });
  } catch (error) {
    throw new ProjectDataError(resource, "network request failed", error);
  }
  if (!response.ok) {
    throw new ProjectDataError(resource, `request returned ${response.status}`);
  }
  let value;
  try {
    value = await response.json();
  } catch (error) {
    throw new ProjectDataError(resource, "response was not valid JSON", error);
  }
  if (!validate(value)) {
    throw new ProjectDataError(resource, "response did not match the expected top-level shape");
  }
  return value;
}

export function loadProjects() {
  return loadJson("Project registry", RESOURCE_URLS.projects, (value) =>
    value && value.schema_version === "1.0.0" && Array.isArray(value.projects));
}

export function loadServiceAreas() {
  return loadJson("Project service areas", RESOURCE_URLS.serviceAreas, (value) =>
    value && value.type === "FeatureCollection" && Array.isArray(value.features));
}

export function loadReferenceGeography() {
  return loadJson("Natural Earth reference geography", RESOURCE_URLS.referenceGeography, (value) =>
    value && value.type === "FeatureCollection" && Array.isArray(value.features));
}

// A future API adapter can replace these three functions while returning the same
// contracts; filtering, table synchronization, details, and rendering need not change.
