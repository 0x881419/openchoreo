---
title: Test Plan v1.2.0 F-009 — Client Surfaces occ CLI and MCP
id: F-009
status: draft
owner: TBD
updated: 2026-09-19
---

# Test Plan v1.2.0 F-009 — Client Surfaces occ CLI and MCP
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **This document is as-built.** It records the suite that exists, not a suite that was planned. Coverage holes are the point of it.

## Traceability matrix

| Story | Covering tests | Level | Status |
| --- | --- | --- | --- |
| F-009-US1 | see cases below | unit + envtest | wip — unverified, run make go.test |
| F-009-US2 | see cases below | unit + envtest | wip — unverified, run make go.test |
| F-009-US3 | see cases below | unit + envtest | wip — unverified, run make go.test |

## Test cases

Test packages backing this feature, with the result of the run performed here:

| Package | Result here |
| --- | --- |
| `internal/occ/fsmode` | passed |
| `internal/occ/fsmode/config` | passed |
| `internal/occ/fsmode/generator` | passed |
| `internal/occ/fsmode/output` | passed |
| `internal/occ/fsmode/pipeline` | passed |
| `internal/occ/fsmode/typed` | passed |
| `internal/openchoreo-api/mcphandlers` | passed |
| `pkg/mcp/tools` | passed |

OPEN: package-level results do not tell you which story a passing package actually covers. Mapping individual test cases to stories needs a human who knows the intent.

## Edge and negative cases

The repository states a number of negative rules in its own words. These are quoted, with the citation kept, because they are the clearest statement of intent the code contains:

- occ talks to the control plane through the generated OpenAPI client [D: internal/occ/resources/client/openapi_client.go:16]
- occ OIDC/PKCE login [D: internal/occ/cmd/login/login.go:33]
- occ remote tunnel client [D: internal/occ/cmd/remote/connect.go:896]
- occ filesystem mode [D: internal/occ/fsmode]

## Out of scope

- End-to-end behaviour against a live cluster — covered by `test/e2e/` and run by `make e2e` [D: test/e2e/README.md:1], not by this plan.

OPEN: is there an intended split between what must be proven by envtest and what must be proven end to end? The tiers in `test/e2e/README.md` imply one but never state the rule.
