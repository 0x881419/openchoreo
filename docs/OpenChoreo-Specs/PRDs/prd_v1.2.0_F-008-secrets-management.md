---
title: PRD v1.2.0 F-008 — Secrets Management
id: F-008
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-008 — Secrets Management
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: no secret value is stored in an OpenChoreo resource: every kind carries a reference into an external store that External Secrets Operator resolves in the data plane — basis: the CRDs model only store references and key names, and the e2e suite resolves them through ESO into a running workload rather than through the control plane [D: api/v1alpha1/secretreference_types.go:134].

## User stories

- **F-008-US1** — I: as a developer I reference a secret by name and it appears in my workload without ever passing through a manifest I edit — basis: inferred from secretreferences endpoints and the ESO resolution path [D: api/v1alpha1/secretreference_types.go:134]
- **F-008-US2** — I: as a developer I register credentials for a private git repository once — basis: inferred from the three gitsecrets operations [D: api/v1alpha1/secretreference_types.go:134]
- **F-008-US3** — I: as a platform engineer I choose the backing secret store per data plane — basis: inferred from SecretStoreRef on DataPlane [D: api/v1alpha1/secretreference_types.go:134]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-008-US1** — see the traceability matrix in `tests/test_v1.2.0_F-008.md`.
- **F-008-US2** — see the traceability matrix in `tests/test_v1.2.0_F-008.md`.
- **F-008-US3** — see the traceability matrix in `tests/test_v1.2.0_F-008.md`.

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
