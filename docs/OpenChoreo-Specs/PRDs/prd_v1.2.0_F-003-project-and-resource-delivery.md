---
title: PRD v1.2.0 F-003 — Project and Resource Delivery
id: F-003
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-003 — Project and Resource Delivery
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: projects and backing resources reuse the Component pipeline's exact shape — definition, immutable release, per-environment binding, rendered output — so a reader who understands one understands all three — basis: three parallel CRD triples, three parallel binding controllers, and all three converge on the same `RenderedRelease` kind [D: internal/controller/projectreleasebinding/controller_render.go:82].

## User stories

- **F-003-US1** — I: as a developer I group components into a project and get isolation and shared networking without configuring either — basis: inferred from projects endpoints plus the project pipeline's gateway stage [D: internal/controller/projectreleasebinding/controller_render.go:82]
- **F-003-US2** — I: as a developer I declare a dependency on a database or queue and receive its connection details in my workload — basis: inferred from resources endpoints and ResolvedResourceOutput [D: internal/controller/projectreleasebinding/controller_render.go:82]
- **F-003-US3** — I: as a platform engineer I control which backing resources are offerable, per namespace or fleet-wide — basis: inferred from resourcetypes/clusterresourcetypes, shared with F-002 [D: internal/controller/projectreleasebinding/controller_render.go:82]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-003-US1** — see the traceability matrix in `tests/test_v1.2.0_F-003.md`.
- **F-003-US2** — see the traceability matrix in `tests/test_v1.2.0_F-003.md`.
- **F-003-US3** — see the traceability matrix in `tests/test_v1.2.0_F-003.md`.

OPEN: none of these criteria were agreed as criteria. They are behaviours observed in tests, promoted to criteria by this reconstruction. Confirm or replace them.

## Scope boundaries

OPEN: not recoverable. Code records what was built; it retains no record of what was ruled out of this feature, or why.

## Dependencies

- Kubernetes and the OpenChoreo custom resource definitions
- The control-plane manager, which hosts this feature's reconcilers
- The control-plane API, which serves this feature's operations

Paths and versions for each of these live in the architecture documents; a PRD carries no file references of its own.

OPEN: the dependency list above is structural. Which of these are hard prerequisites for a supported install, and which are optional?

## Metrics

OPEN: no success metric for this feature is expressed anywhere in the repository — no SLO, no target, no dashboard definition. This is the single largest gap in reconstructing a PRD from code.
