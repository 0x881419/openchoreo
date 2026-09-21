---
title: Feature Architecture v1.2.0 F-009 — Client Surfaces occ CLI and MCP
id: F-009
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-009 — Client Surfaces occ CLI and MCP
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: the CLI and the MCP server are two presentations of one service layer rather than two implementations: both route to `internal/openchoreo-api/services/*`, and both are audited through the same generated table — basis: `occ` consumes the generated OpenAPI client, the MCP handlers call the same service structs the HTTP handlers do, and audit has explicit MCP bindings alongside the HTTP ones [D: internal/openchoreo-api/audit/mcp_bindings.go:1].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
This feature serves no HTTP operations of its own.

OPEN: is that deliberate, or are its operations expected to arrive later?

## Data model
This feature defines no custom resources of its own; it operates on the kinds owned by other features.

## Sequence

Supporting code paths:

- occ talks to the control plane through the generated OpenAPI client — [D: internal/occ/resources/client/openapi_client.go:16]
- occ OIDC/PKCE login — [D: internal/occ/cmd/login/login.go:33]
- occ remote tunnel client — [D: internal/occ/cmd/remote/connect.go:896]
- occ filesystem mode — [D: internal/occ/fsmode]
- MCP HTTP server — [D: pkg/mcp/server.go:1]
- MCP toolset registration — [D: pkg/mcp/tools]
- MCP handlers over the same services — [D: internal/openchoreo-api/mcphandlers]
- MCP audit bindings — [D: internal/openchoreo-api/audit/mcp_bindings.go:1]
- MCP mounted on the API server — [D: cmd/openchoreo-api/main.go:260]

OPEN: the happy-path call order above is read off reconciler registration and ownership, not off a trace. A recorded trace from a running install would confirm or correct it.

## Failure modes
| Failure | Detection | Behaviour in code | Evidence |
| --- | --- | --- | --- |
| Upstream call fails | the client or transport returns an error | the error is surfaced to the caller; no partial state is written locally | [D: internal/occ/resources/client/openapi_client.go:16] |

OPEN: which of these failures page someone, and which are expected steady-state noise? No alerting rule in the repository distinguishes them.

## Observability
- Structured logging via logr/zap [D: go.mod:9]
- Prometheus metrics exposed by controller-runtime [D: config/prometheus]
- Audit events for every non-exempt API operation [D: internal/openchoreo-api/audit/definitions.gen.go:1]

OPEN: this feature emits no metric named for its own domain. Which signals should it own, as opposed to inheriting from the framework?

## Traceability
Satisfies the stories in `PRDs/prd_v1.2.0_F-009-client-surfaces-occ-cli-and-mcp.md`; exercised by `tests/test_v1.2.0_F-009.md`.

## Open questions

OPEN: the MCP toolset exposes 25 tools against an API with 214 operations. What was the selection rule — read-mostly, high-frequency, safe-to-automate? The registry records the choice and not the criterion.

OPEN: is `occ` intended to stay a thin client over the generated OpenAPI client, or to grow local behaviour? `fsmode` already suggests the latter.

OPEN: which MCP tools are considered safe for an unattended agent, and which require a human?

