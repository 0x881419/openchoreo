---
title: Feature Architecture v1.2.0 F-007 — Observability and Alerting
id: F-007
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-007 — Observability and Alerting
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: observability is a queried plane rather than a shipped-logs pipeline: the observer service fronts the store with its own OpenAPI contract and an internal one, and alerting is expressed as CRDs that the control plane reconciles against that service — basis: two separate observer specs exist, one public and one internal, and the alert-rule controller reads the observer endpoint from configuration rather than embedding a client [D: internal/controller/observabilityalertrule/controller.go:353].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
23 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| POST | `/api/v1/events/query` | [D: openapi/observer-api.yaml:157] |
| POST | `/api/v1/logs/query` | [D: openapi/observer-api.yaml:95] |
| POST | `/api/v1/metrics/query` | [D: openapi/observer-api.yaml:229] |
| GET | `/api/v1/namespaces/{namespaceName}/observabilityalertsnotificationchannels` | [D: openapi/openchoreo-api.yaml:5919] |
| POST | `/api/v1/namespaces/{namespaceName}/observabilityalertsnotificationchannels` | [D: openapi/openchoreo-api.yaml:5945] |
| DELETE | `/api/v1/namespaces/{namespaceName}/observabilityalertsnotificationchannels/{observabilityAlertsNotificationChannelName}` | [D: openapi/openchoreo-api.yaml:6037] |
| GET | `/api/v1/namespaces/{namespaceName}/observabilityalertsnotificationchannels/{observabilityAlertsNotificationChannelName}` | [D: openapi/openchoreo-api.yaml:5979] |
| PUT | `/api/v1/namespaces/{namespaceName}/observabilityalertsnotificationchannels/{observabilityAlertsNotificationChannelName}` | [D: openapi/openchoreo-api.yaml:6003] |
| POST | `/api/v1alpha1/alerts/query` | [D: openapi/observer-api.yaml:782] |
| POST | `/api/v1alpha1/alerts/sources/{sourceType}/rules` | [D: openapi/observer-internal-api.yaml:57] |
| DELETE | `/api/v1alpha1/alerts/sources/{sourceType}/rules/{ruleName}` | [D: openapi/observer-internal-api.yaml:186] |
| GET | `/api/v1alpha1/alerts/sources/{sourceType}/rules/{ruleName}` | [D: openapi/observer-internal-api.yaml:114] |
| PUT | `/api/v1alpha1/alerts/sources/{sourceType}/rules/{ruleName}` | [D: openapi/observer-internal-api.yaml:145] |
| POST | `/api/v1alpha1/alerts/webhook` | [D: openapi/observer-internal-api.yaml:221] |
| GET | `/api/v1alpha1/costs/namespaces/{namespace}/environments/{environment}` | [D: openapi/observer-api.yaml:275] |
| GET | `/api/v1alpha1/costs/namespaces/{namespace}/environments/{environment}/recommendations` | [D: openapi/observer-api.yaml:331] |
| POST | `/api/v1alpha1/incidents/query` | [D: openapi/observer-api.yaml:666] |
| PUT | `/api/v1alpha1/incidents/{incidentId}` | [D: openapi/observer-api.yaml:724] |
| POST | `/api/v1alpha1/metrics/runtime-topology` | [D: openapi/observer-api.yaml:465] |
| GET | `/api/v1alpha1/platform-logs` | [D: openapi/observer-api.yaml:390] |
| POST | `/api/v1alpha1/traces/query` | [D: openapi/observer-api.yaml:516] |
| POST | `/api/v1alpha1/traces/{traceId}/spans/query` | [D: openapi/observer-api.yaml:561] |
| GET | `/api/v1alpha1/traces/{traceId}/spans/{spanId}` | [D: openapi/observer-api.yaml:613] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| ObservabilityAlertRule | `name`, `description`, `severity`, `enabled`, `source`, `condition`, `actions` | [D: api/v1alpha1/observabilityalertrule_types.go:216] |
| ObservabilityAlertsNotificationChannel | `environment`, `isEnvDefault`, `type`, `emailConfig`, `webhookConfig` | [D: api/v1alpha1/observabilityalertsnotificationchannel_types.go:209] |
| ObservabilityPlane | `planeID`, `clusterAgent`, `observerURL`, `rcaAgentURL`, `finOpsAgentURL` | [D: api/v1alpha1/observabilityplane_types.go:69] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `observabilityalertrule` — [D: internal/controller/observabilityalertrule/controller.go:353]
2. `observabilityalertsnotificationchannel` — [D: internal/controller/observabilityalertsnotificationchannel/controller.go:29]

Supporting code paths:

- Observer service — [D: internal/observer/service]
- Observer query store — [D: internal/observer/store]
- Observer notifications — [D: internal/observer/notifications]
- Event forwarder — [D: internal/eventforwarder]
- Alert source and condition model — [D: api/v1alpha1/observabilityalertrule_types.go:56]
- Cleanup finalizer on notification channels — [D: internal/controller/observabilityalertsnotificationchannel/controller.go:29]
- Hubble flow redaction in the cluster agent — [D: internal/cluster-agent/hubble_redact.go:1]

OPEN: the happy-path call order above is read off reconciler registration and ownership, not off a trace. A recorded trace from a running install would confirm or correct it.

## Failure modes
| Failure | Detection | Behaviour in code | Evidence |
| --- | --- | --- | --- |
| Reconcile error | controller-runtime returns a non-nil error | requeue with backoff; condition recorded on the resource status | [D: internal/controller/conditions.go:1] |
| Resource deleted while dependents exist | finalizer on the parent | cleanup runs before the object is released | [D: internal/controller/component/controller.go:1] |

OPEN: which of these failures page someone, and which are expected steady-state noise? No alerting rule in the repository distinguishes them.

## Observability
- Structured logging via logr/zap [D: go.mod:9]
- Prometheus metrics exposed by controller-runtime [D: config/prometheus]
- Audit events for every non-exempt API operation [D: internal/openchoreo-api/audit/definitions.gen.go:1]

OPEN: this feature emits no metric named for its own domain. Which signals should it own, as opposed to inheriting from the framework?

## Traceability
Satisfies the stories in `PRDs/prd_v1.2.0_F-007-observability-and-alerting.md`; exercised by `tests/test_v1.2.0_F-007.md`.

## Open questions

OPEN: which signals are first-class — logs, metrics, traces, cost — and which are adapters? Four adapter specs exist in openapi/, but no statement of which are supported.

OPEN: what is the data retention window in the observability plane, and who is expected to operate the store?

OPEN: the internal observer API exists alongside the public one. What is the trust boundary between them, and what may only be called internally?

