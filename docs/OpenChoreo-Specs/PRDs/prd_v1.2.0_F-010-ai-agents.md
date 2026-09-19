---
title: PRD v1.2.0 F-010 — AI Agents
id: F-010
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-010 — AI Agents
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: the agents are three independent Python services that consume the platform's own APIs rather than privileged components inside the control plane, and each carries defensive rules about what it will not do with model output — basis: each has its own pyproject, Dockerfile and OpenAPI spec, and their test suites state guard rules such as never echoing raw exception text and never retrying an empty observability query [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16].

## User stories

- **F-010-US1** — I: as a platform user I ask the portal a question in plain language and get an answer grounded in my own platform state — basis: inferred from the portal-assistant chat and warmup endpoints [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16]
- **F-010-US2** — I: as an SRE I get a root-cause analysis for an incident without assembling the evidence myself — basis: inferred from the sre-agent analyze and chat endpoints [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16]
- **F-010-US3** — I: as a platform owner I see cost analyses and can dismiss a recommendation without it silently reappearing — basis: inferred from the finops-agent analyses and report endpoints, and the dismiss rule [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-010-US1** — see the traceability matrix in `tests/test_v1.2.0_F-010.md`.
- **F-010-US2** — see the traceability matrix in `tests/test_v1.2.0_F-010.md`.
- **F-010-US3** — see the traceability matrix in `tests/test_v1.2.0_F-010.md`.

OPEN: none of these criteria were agreed as criteria. They are behaviours observed in tests, promoted to criteria by this reconstruction. Confirm or replace them.

## Scope boundaries

OPEN: not recoverable. Code records what was built; it retains no record of what was ruled out of this feature, or why.

## Dependencies

- Kubernetes and the OpenChoreo custom resource definitions
- The control-plane API, which serves this feature's operations

Paths and versions for each of these live in the architecture documents; a PRD carries no file references of its own.

OPEN: the dependency list above is structural. Which of these are hard prerequisites for a supported install, and which are optional?

## Metrics

OPEN: no success metric for this feature is expressed anywhere in the repository — no SLO, no target, no dashboard definition. This is the single largest gap in reconstructing a PRD from code.
