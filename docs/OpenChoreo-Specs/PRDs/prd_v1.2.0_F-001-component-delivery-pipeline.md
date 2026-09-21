---
title: PRD v1.2.0 F-001 — Component Delivery Pipeline
id: F-001
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-001 — Component Delivery Pipeline
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: the feature is a four-stage reduction from mutable developer intent to applied cluster state, with immutability introduced at stage two — basis: `Component` is edited freely, `ComponentRelease` is described by its own design doc as "an immutable snapshot… containing the frozen ComponentType, Traits, and Workload specifications", `ReleaseBinding` re-introduces variation per environment, and only `RenderedRelease` touches a data-plane cluster [D: docs/crds/renderedrelease.md:44].

## User stories

- **F-001-US1** — I: as a developer I declare a component once and have it deployed to every environment my pipeline defines — basis: inferred from components + releasebindings endpoints, and the four reconcilers [D: docs/crds/renderedrelease.md:44]
- **F-001-US2** — I: as a developer I can see the concrete Kubernetes objects my component produced, and their events and logs, without cluster access — basis: inferred from the three k8sresources sub-resources [D: docs/crds/renderedrelease.md:44]
- **F-001-US3** — I: as a developer I can cut a release of my component on demand — basis: inferred from generate-release and trigger endpoints [D: docs/crds/renderedrelease.md:44]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-001-US1** — see the traceability matrix in `tests/test_v1.2.0_F-001.md`.
- **F-001-US2** — see the traceability matrix in `tests/test_v1.2.0_F-001.md`.
- **F-001-US3** — see the traceability matrix in `tests/test_v1.2.0_F-001.md`.

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
