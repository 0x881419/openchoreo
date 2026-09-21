---
title: Product Backlog — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Product Backlog — OpenChoreo v1.2.0

> **As-built backlog.** These rows are not planned work — they are the feature clusters this
> reconstruction found already shipped, sized by the surface each one presents. Value and
> priority are `OPEN:` in every row, because a repository records what was built and never what
> it was worth.

| ID | Feature | API ops | CRDs | Reconcilers | Value | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| F-001 | Component Delivery Pipeline | 25 | 5 | 4 | OPEN | OPEN |
| F-002 | Platform Abstractions and Templating | 48 | 8 | 8 | OPEN | OPEN |
| F-003 | Project and Resource Delivery | 28 | 6 | 6 | OPEN | OPEN |
| F-004 | Authorization and Access Control | 24 | 4 | 4 | OPEN | OPEN |
| F-005 | Multi-Plane Topology and Connectivity | 42 + 5 | 8 | 6 | OPEN | OPEN |
| F-006 | Build and Workflow Execution | 21 | 4 | 4 | OPEN | OPEN |
| F-007 | Observability and Alerting | 5 + 20 | 3 | 2 | OPEN | OPEN |
| F-008 | Secrets Management | 13 | 3 | 1 | OPEN | OPEN |
| F-009 | Client Surfaces — occ CLI and MCP | — | — | — | OPEN | OPEN |
| F-010 | AI Agents | 16 | — | — | OPEN | OPEN |

Counts derive from the in-repo OpenAPI specs [D: openapi/openchoreo-api.yaml:191], the root
CRD kinds [D: api/v1alpha1/component_types.go:19] and the controller packages
[D: internal/controller/component/controller.go:3]. F-005 and F-007 carry a second number for
operations declared outside the main spec [D: internal/remoteconnect/authorize.go:68],
[D: openapi/observer-api.yaml:1].

## Known holes, carried as real backlog

These are gaps this reconstruction found, not features. Each is a candidate row for a real
backlog.

- The published CRD design notes cover 1 of 37 kinds [D: docs/crds/README.md:6].
- `docs/crds/renderedrelease.md` documents only the component path to RenderedRelease; the
  project and resource paths, and the second observability-plane release, are undocumented
  [D: internal/controller/projectreleasebinding/controller_render.go:82].
- README and code disagree on the name of the build plane — "CI Plane" versus "workflow plane"
  [D: README.md:65], [D: api/v1alpha1/workflowplane_types.go:66].
- `docs/contributors/contribute.md` lists three buildable components; the make targets build
  seven [D: make/k3d.mk:39].
- 40 surveyed API operations appear in no document in this hub — listed in the reverse-docs
  coverage report, not here.

## Open questions

OPEN: is there a real backlog, and does it agree with this split? If the team's own
decomposition differs, theirs is right and this one should be re-cut to match.

OPEN: priority ordering across these ten is not inferable. Churn ranks `agents/*` and
`install/helm/*` highest [D: go.mod:1], but churn measures activity, not importance, and
published precision for history-derived prediction is around 29%.
