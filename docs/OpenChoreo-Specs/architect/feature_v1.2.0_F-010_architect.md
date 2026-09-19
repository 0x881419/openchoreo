---
title: Feature Architecture v1.2.0 F-010 — AI Agents
id: F-010
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-010 — AI Agents
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: the agents are three independent Python services that consume the platform's own APIs rather than privileged components inside the control plane, and each carries defensive rules about what it will not do with model output — basis: each has its own pyproject, Dockerfile and OpenAPI spec, and their test suites state guard rules such as never echoing raw exception text and never retrying an empty observability query [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
14 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/rca-agent/reports` | [D: agents/sre-agent/src/api/report_routes.py:48] |
| GET | `/api/v1/rca-agent/reports/{report_id}` | [D: agents/sre-agent/src/api/report_routes.py:90] |
| PUT | `/api/v1/rca-agent/reports/{report_id}` | [D: agents/sre-agent/src/api/report_routes.py:121] |
| POST | `/api/v1alpha1/analyses` | [D: agents/finops-agent/src/api/agent_routes.py:45] |
| POST | `/api/v1alpha1/portal-assistant/chat` | [D: agents/portal-assistant/src/api/agent_routes.py:277] |
| POST | `/api/v1alpha1/portal-assistant/warmup` | [D: agents/portal-assistant/src/api/agent_routes.py:299] |
| POST | `/api/v1alpha1/rca-agent/analyze` | [D: agents/sre-agent/src/api/agent_routes.py:75] |
| POST | `/api/v1alpha1/rca-agent/chat` | [D: agents/sre-agent/src/api/agent_routes.py:122] |
| GET | `/api/v1alpha1/reports` | [D: agents/finops-agent/src/api/report_routes.py:53] |
| GET | `/api/v1alpha1/reports/missing` | [D: agents/finops-agent/tests/test_report_routes.py:107] |
| GET | `/api/v1alpha1/reports/r1` | [D: agents/finops-agent/tests/test_report_routes.py:94] |
| PUT | `/api/v1alpha1/reports/r1` | [D: agents/finops-agent/tests/test_report_routes.py:136] |
| GET | `/api/v1alpha1/reports/{report_id}` | [D: agents/finops-agent/src/api/report_routes.py:88] |
| PUT | `/api/v1alpha1/reports/{report_id}` | [D: agents/finops-agent/src/api/report_routes.py:132] |

## Data model
This feature defines no custom resources of its own; it operates on the kinds owned by other features.

## Sequence

Supporting code paths:

- FinOps agent analysis endpoint — [D: agents/finops-agent/src/api/agent_routes.py:45]
- FinOps report endpoints — [D: agents/finops-agent/src/api/report_routes.py:53]
- Portal assistant chat endpoint — [D: agents/portal-assistant/src/api/agent_routes.py:277]
- Portal assistant orchestrator — [D: agents/portal-assistant/src/agent/orchestrator.py:119]
- Empty-result guard: when not to retry a query — [D: agents/portal-assistant/src/agent/middleware/empty_result_guard.py:16]
- SRE agent RCA endpoints — [D: agents/sre-agent/src/api/agent_routes.py:75]
- SRE agent MCP server and its FORBIDDEN surfacing rule — [D: agents/sre-agent/src/mcp_server.py:132]
- A dismissed action must not flip an applied one — [D: agents/finops-agent/tests/test_report_routes.py:205]
- Errors are generic; raw exception text is never echoed — [D: agents/finops-agent/tests/test_middleware.py:113]

OPEN: the happy-path call order above is read off reconciler registration and ownership, not off a trace. A recorded trace from a running install would confirm or correct it.

## Failure modes
| Failure | Detection | Behaviour in code | Evidence |
| --- | --- | --- | --- |
| Reconcile error | controller-runtime returns a non-nil error | requeue with backoff; condition recorded on the resource status | [D: internal/controller/conditions.go:1] |

OPEN: which of these failures page someone, and which are expected steady-state noise? No alerting rule in the repository distinguishes them.

## Observability
- Structured logging via logr/zap [D: go.mod:9]
- Prometheus metrics exposed by controller-runtime [D: config/prometheus]
- Audit events for every non-exempt API operation [D: internal/openchoreo-api/audit/definitions.gen.go:1]

OPEN: this feature emits no metric named for its own domain. Which signals should it own, as opposed to inheriting from the framework?

## Traceability
Satisfies the stories in `PRDs/prd_v1.2.0_F-010-ai-agents.md`; exercised by `tests/test_v1.2.0_F-010.md`.

## Open questions

OPEN: which LLM providers are supported, and is the model a deployment choice or a fixed one? Only the configuration key names are in the repository, never a value.

OPEN: what data leaves the cluster when an agent calls a model, and is there a redaction step on that path? The cluster agent redacts Hubble flows; no equivalent is visible here.

OPEN: are these agents GA, preview or experimental? Nothing in the repository states a support level, and the version numbers (0.1.0) suggest one thing while inclusion in the release suggests another.

