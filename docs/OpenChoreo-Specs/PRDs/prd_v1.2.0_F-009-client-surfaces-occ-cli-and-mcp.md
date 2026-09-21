---
title: PRD v1.2.0 F-009 — Client Surfaces occ CLI and MCP
id: F-009
status: draft
owner: TBD
updated: 2026-09-19
---

# PRD v1.2.0 F-009 — Client Surfaces occ CLI and MCP
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> This PRD was reconstructed from shipped code. A requirement is a statement about intent, and intent is not in a repository: the stories below are inferences from the surface that exists, and every question of value, priority and scope is OPEN.

## Summary
I: the CLI and the MCP server are two presentations of one service layer rather than two implementations: both route to `internal/openchoreo-api/services/*`, and both are audited through the same generated table — basis: `occ` consumes the generated OpenAPI client, the MCP handlers call the same service structs the HTTP handlers do, and audit has explicit MCP bindings alongside the HTTP ones [D: internal/openchoreo-api/audit/mcp_bindings.go:1].

## User stories

- **F-009-US1** — I: as a developer I use one CLI for every platform resource, with the same shape as the API — basis: inferred from 46 occ command groups over the generated client [D: internal/openchoreo-api/audit/mcp_bindings.go:1]
- **F-009-US2** — I: as an AI agent I operate the platform through typed tools rather than by shelling out — basis: inferred from 25 registered MCP tools and their handlers [D: internal/openchoreo-api/audit/mcp_bindings.go:1]
- **F-009-US3** — I: as a platform engineer every action is audited identically whoever performed it — basis: inferred from the MCP audit bindings beside the HTTP definitions [D: internal/openchoreo-api/audit/mcp_bindings.go:1]

## Acceptance criteria

Lifted from test names, which are evidence that the behaviour is wanted and not merely present. Where a story has no test naming it, that is recorded rather than filled.

- **F-009-US1** — see the traceability matrix in `tests/test_v1.2.0_F-009.md`.
- **F-009-US2** — see the traceability matrix in `tests/test_v1.2.0_F-009.md`.
- **F-009-US3** — see the traceability matrix in `tests/test_v1.2.0_F-009.md`.

OPEN: none of these criteria were agreed as criteria. They are behaviours observed in tests, promoted to criteria by this reconstruction. Confirm or replace them.

## Scope boundaries

OPEN: not recoverable. Code records what was built; it retains no record of what was ruled out of this feature, or why.

## Dependencies

- Kubernetes and the OpenChoreo custom resource definitions

Paths and versions for each of these live in the architecture documents; a PRD carries no file references of its own.

OPEN: the dependency list above is structural. Which of these are hard prerequisites for a supported install, and which are optional?

## Metrics

OPEN: no success metric for this feature is expressed anywhere in the repository — no SLO, no target, no dashboard definition. This is the single largest gap in reconstructing a PRD from code.
