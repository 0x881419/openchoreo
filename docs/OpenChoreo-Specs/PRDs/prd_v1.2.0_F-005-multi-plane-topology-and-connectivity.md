---
title: PRD v1.2.0 F-005 — Multi-Plane Topology and Connectivity
id: F-005
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-005 — Multi-Plane Topology and Connectivity
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: the control plane never dials a managed cluster: the agent dials out and the gateway multiplexes work back over that connection, and `occ remote` bypasses the control plane for bytes while keeping it in the authorization path — basis: the remote-connect package comment states that "the byte path does not traverse the control plane" while each stream still calls back for authorization [D: internal/remoteconnect/doc.go:15].

## User stories

- **F-005-US1** — I: as a platform engineer I register a data plane and the control plane reaches it without inbound firewall rules — basis: inferred from dataplanes endpoints and the agent-dials-out gateway [D: internal/remoteconnect/doc.go:15]
- **F-005-US2** — I: as a platform engineer I define promotion order between environments once — basis: inferred from deploymentpipelines endpoints and PromotionPath [D: internal/remoteconnect/doc.go:15]
- **F-005-US3** — I: as a developer I can reach a dependency running in a data plane from my laptop, scoped to what I may already access — basis: inferred from the three remote-connect operations and the signed capability [D: internal/remoteconnect/doc.go:15]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-005-US1** — see the traceability matrix in `tests/test_v1.2.0_F-005.md`.
- **F-005-US2** — see the traceability matrix in `tests/test_v1.2.0_F-005.md`.
- **F-005-US3** — see the traceability matrix in `tests/test_v1.2.0_F-005.md`.

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
