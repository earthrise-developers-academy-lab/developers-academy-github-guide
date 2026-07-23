# Project explorer dependency provenance

## Leaflet 1.9.4

The explorer vendors the stable Leaflet 1.9.4 browser distribution from the official GitHub release.

- Release: `https://github.com/Leaflet/Leaflet/releases/tag/v1.9.4`
- Release commit displayed by GitHub: `d15112c`
- Archive: `https://github.com/Leaflet/Leaflet/releases/download/v1.9.4/leaflet.zip`
- Retrieval date: 2026-07-22
- License: BSD 2-Clause; preserved verbatim at `assets/vendor/leaflet/1.9.4/LICENSE`
- Runtime inventory: `leaflet.css`, `leaflet.js`, layer images, marker images, and marker shadow
- Checksums: `assets/vendor/leaflet/1.9.4/SHA256SUMS`

Vendoring makes the static GitHub Pages result reproducible and avoids CDN availability, version drift, runtime package retrieval, and hidden external requests. Development sources, source maps, plugins, and package-manager metadata are intentionally excluded because the page does not need them at runtime.

### Update procedure

1. Open an approved dependency-update Issue.
2. Confirm the exact stable Leaflet release and read its release notes and license.
3. Retrieve the official release archive and copy only the unmodified runtime distribution files required by `leaflet.css`.
4. Preserve the upstream license, update `VERSION`, regenerate every SHA-256 entry, and record the retrieval date and source.
5. Run map-data validation, JavaScript checks, tests, Quarto rendering, browser-console inspection, keyboard review, and desktop/narrow layout review.
6. Review the complete diff through a pull request. Do not switch to a CDN or `latest` URL.

## Natural Earth reference geography

- Repository: `https://github.com/nvkelso/natural-earth-vector`
- Immutable commit: `693f11422f4e08d2da4566b854dda53eb7c39fb3`
- Source path: `geojson/ne_110m_land.geojson`
- Theme and scale: land polygons, 1:110m
- Retrieval date: 2026-07-22
- Rights: public domain; the source repository suggests the attribution “Made with Natural Earth”
- Transformation: none

The local land layer provides neutral geographic context without an external tile service. It is not an administrative layer, thematic product, project boundary source, or production basemap decision. See `data/reference/README.md` for the file-level record.

## Static adapter and future source replacement

`assets/js/project-data-adapter.js` owns every runtime resource URL and returns the project, service-area, and reference-geography contracts. A future approved REST, registry, SQLite/GeoPackage publication step, or PostgreSQL/PostGIS service can replace those loader functions if it returns the same validated contracts. Filters, map rendering, table synchronization, and details must remain independent of the storage source.

Any browser-accessible replacement may return only reviewed public-safe exports. Canonical private data must remain in a separate private organization-controlled repository or approved secure store; browser JavaScript must not fetch that private source or contain its credentials or private URLs. A deterministic allowlist-based publication exporter requires a separate bounded Issue. See the [publication lifecycle procedure](../operations/publication-lifecycle.md).

## HDS and USWDS staging

This `github.io` implementation is a reference site, not an official NASA property. The component applies outcomes emphasized by HDS/USWDS—semantic native controls, plain labels, squared controls, consistent spacing, visible focus, responsive layout, non-color cues, accessible alerts, reduced motion, and a semantic fallback table—without importing HDS Core.

A later authorized production migration would need to map the component's CSS variables, buttons, form controls, alerts, table, spacing, focus treatment, and data-visualization palette to approved HDS/USWDS tokens and components. It would also need governance for production data and basemap selection. This proof of concept makes no formal HDS, Section 508, or WCAG conformance claim and uses no NASA insignia, federal banner, agency header, or official footer.

## Recorded SHA-256 checksums

```text
1dbbe9d028e292f36fcba8f8b3a28d5e8932754fc2215b9ac69e4cdecf5107c6  images/layers.png
066daca850d8ffbef007af00b06eac0015728dee279c51f3cb6c716df7c42edf  images/layers-2x.png
574c3a5cca85f4114085b6841596d62f00d7c892c7b03f28cbfa301deb1dc437  images/marker-icon.png
00179c4c1ee830d3a108412ae0d294f55776cfeb085c60129a39aa6fc4ae2528  images/marker-icon-2x.png
264f5c640339f042dd729062cfc04c17f8ea0f29882b538e3848ed8f10edb4da  images/marker-shadow.png
a7837102824184820dfa198d1ebcd109ff6d0ff9a2672a074b9a1b4d147d04c6  leaflet.css
85d455b4522415f6badc42a0e7d17c919d100347d6b8958bd0dc738fdecd6d50  leaflet.js
53e8dc25862014e4324741ca18fbe3611e11d42ef69f59f86ea8c5389647d4cb  LICENSE
```
