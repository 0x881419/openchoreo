---
title: How to observe — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# How to observe — OpenChoreo

Feature documents: `docs/OpenChoreo-Specs/architect/feature_v1.2.0_F-007_architect.md` and
`docs/OpenChoreo-Specs/ddd/domain_DOM-003-plane-connectivity.md`.

The observer service fronts the observability plane with its own contract — 15 public
operations [D: openapi/observer-api.yaml:1] and 5 internal ones
[D: openapi/observer-internal-api.yaml:1]. Alerting is declarative: `ObservabilityAlertRule`
[D: api/v1alpha1/observabilityalertrule_types.go:216] and
`ObservabilityAlertsNotificationChannel`
[D: api/v1alpha1/observabilityalertsnotificationchannel_types.go:209].

Locally [D: docs/contributors/contribute.md:132]:

```sh
make k3d.logs.observer
# Observer API   http://localhost:11080
# OpenSearch     http://localhost:11082
```

Telemetry libraries in use: OpenTelemetry, Prometheus client, zap [D: go.mod:9].

OPEN: which signals are first-class and which are adapters? Four adapter specs exist in
`openapi/` [D: openapi/observability-logs-adapter-api.yaml:1] with no statement of support level.

OPEN: what is the retention window in the observability plane, and who operates the store?
