---
title: PRD v1.2.0 F-002 — Platform Abstractions and Templating
id: F-002
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-002 — Platform Abstractions and Templating
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: platform engineers extend the platform by writing declarative CEL templates with OpenAPI-v3-typed parameters rather than Go code, and every abstraction is offered in a namespaced and a cluster-scoped variant so the same definition can be shared or confined — basis: eight paired kinds each expose a `/schema` endpoint, and the render path evaluates CEL under an explicit cost budget [D: internal/template/budget.go:1].

## User stories

- **F-002-US1** — I: as a platform engineer I define a component type once and offer it to every team as a golden path — basis: inferred from componenttypes/clustercomponenttypes endpoints plus the render pipeline [D: internal/template/budget.go:1]
- **F-002-US2** — I: as a platform engineer I attach reusable behaviour to a component without changing its type — basis: inferred from traits/clustertraits endpoints and the trait patch stage [D: internal/template/budget.go:1]
- **F-002-US3** — I: as a developer I can discover exactly what parameters an abstraction accepts before using it — basis: inferred from the eight /schema endpoints [D: internal/template/budget.go:1]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-002-US1** — see the traceability matrix in `tests/test_v1.2.0_F-002.md`.
- **F-002-US2** — see the traceability matrix in `tests/test_v1.2.0_F-002.md`.
- **F-002-US3** — see the traceability matrix in `tests/test_v1.2.0_F-002.md`.

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
