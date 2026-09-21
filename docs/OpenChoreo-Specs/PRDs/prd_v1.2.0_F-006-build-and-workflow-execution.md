---
title: PRD v1.2.0 F-006 — Build and Workflow Execution
id: F-006
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-006 — Build and Workflow Execution
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: builds are modelled as ordinary platform abstractions rather than a separate subsystem: a Workflow is a parameterised template like a ComponentType, and a WorkflowRun is its execution with status, logs and events exposed as sub-resources — basis: Workflow and ClusterWorkflow expose the same `/schema` endpoint as the other abstractions, and WorkflowRun carries three read-only sub-resources [D: api/v1alpha1/workflowrun_types.go:151].

## User stories

- **F-006-US1** — I: as a developer I point at a git repository and get a running workload without writing a pipeline — basis: inferred from the autobuild endpoint and ComponentSource [D: api/v1alpha1/workflowrun_types.go:151]
- **F-006-US2** — I: as a developer I watch a build's logs and events without access to the workflow plane — basis: inferred from workflowruns logs, events and status sub-resources [D: api/v1alpha1/workflowrun_types.go:151]
- **F-006-US3** — I: as a platform engineer I define which build templates teams may use — basis: inferred from workflows/clusterworkflows endpoints [D: api/v1alpha1/workflowrun_types.go:151]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-006-US1** — see the traceability matrix in `tests/test_v1.2.0_F-006.md`.
- **F-006-US2** — see the traceability matrix in `tests/test_v1.2.0_F-006.md`.
- **F-006-US3** — see the traceability matrix in `tests/test_v1.2.0_F-006.md`.

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
