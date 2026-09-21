---
title: PRD v1.2.0 F-007 — Observability and Alerting
id: F-007
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-007 — Observability and Alerting
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: observability is a queried plane rather than a shipped-logs pipeline: the observer service fronts the store with its own OpenAPI contract and an internal one, and alerting is expressed as CRDs that the control plane reconciles against that service — basis: two separate observer specs exist, one public and one internal, and the alert-rule controller reads the observer endpoint from configuration rather than embedding a client [D: internal/controller/observabilityalertrule/controller.go:353].

## User stories

- **F-007-US1** — I: as an SRE I query logs and metrics for a component using the same names developers use — basis: inferred from the observer API's 15 operations [D: internal/controller/observabilityalertrule/controller.go:353]
- **F-007-US2** — I: as an SRE I declare an alert rule as a resource and receive it on a channel I registered — basis: inferred from ObservabilityAlertRule, notification channels and their endpoints [D: internal/controller/observabilityalertrule/controller.go:353]
- **F-007-US3** — I: as a platform engineer I attach an observability plane to an environment once — basis: inferred from observabilityplanes endpoints and the link step [D: internal/controller/observabilityalertrule/controller.go:353]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-007-US1** — see the traceability matrix in `tests/test_v1.2.0_F-007.md`.
- **F-007-US2** — see the traceability matrix in `tests/test_v1.2.0_F-007.md`.
- **F-007-US3** — see the traceability matrix in `tests/test_v1.2.0_F-007.md`.

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
