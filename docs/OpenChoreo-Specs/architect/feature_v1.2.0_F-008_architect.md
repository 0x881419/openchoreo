---
title: Feature Architecture v1.2.0 F-008 — Secrets Management
id: F-008
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-008 — Secrets Management
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: no secret value is stored in an OpenChoreo resource: every kind carries a reference into an external store that External Secrets Operator resolves in the data plane — basis: the CRDs model only store references and key names, and the e2e suite resolves them through ESO into a running workload rather than through the control plane [D: api/v1alpha1/secretreference_types.go:134].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
13 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/namespaces/{namespaceName}/secretreferences` | [D: openapi/openchoreo-api.yaml:3778] |
| POST | `/api/v1/namespaces/{namespaceName}/secretreferences` | [D: openapi/openchoreo-api.yaml:3804] |
| DELETE | `/api/v1/namespaces/{namespaceName}/secretreferences/{secretReferenceName}` | [D: openapi/openchoreo-api.yaml:3896] |
| GET | `/api/v1/namespaces/{namespaceName}/secretreferences/{secretReferenceName}` | [D: openapi/openchoreo-api.yaml:3838] |
| PUT | `/api/v1/namespaces/{namespaceName}/secretreferences/{secretReferenceName}` | [D: openapi/openchoreo-api.yaml:3862] |
| GET | `/api/v1alpha1/namespaces/{namespaceName}/gitsecrets` | [D: openapi/openchoreo-api.yaml:6061] |
| POST | `/api/v1alpha1/namespaces/{namespaceName}/gitsecrets` | [D: openapi/openchoreo-api.yaml:6082] |
| DELETE | `/api/v1alpha1/namespaces/{namespaceName}/gitsecrets/{gitSecretName}` | [D: openapi/openchoreo-api.yaml:6116] |
| GET | `/api/v1alpha1/namespaces/{namespaceName}/secrets` | [D: openapi/openchoreo-api.yaml:6140] |
| POST | `/api/v1alpha1/namespaces/{namespaceName}/secrets` | [D: openapi/openchoreo-api.yaml:6171] |
| DELETE | `/api/v1alpha1/namespaces/{namespaceName}/secrets/{secretName}` | [D: openapi/openchoreo-api.yaml:6281] |
| GET | `/api/v1alpha1/namespaces/{namespaceName}/secrets/{secretName}` | [D: openapi/openchoreo-api.yaml:6211] |
| PUT | `/api/v1alpha1/namespaces/{namespaceName}/secrets/{secretName}` | [D: openapi/openchoreo-api.yaml:6240] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| SecretReference | `targetPlane`, `template`, `data`, `refreshInterval` | [D: api/v1alpha1/secretreference_types.go:134] |
| SecretKeyReference | — | [D: api/v1alpha1/dataplane_types.go:11] |
| SecretStoreRef | — | [D: api/v1alpha1/dataplane_types.go:90] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `secretreference` — [D: internal/controller/secretreference/controller.go:1]

Supporting code paths:

- Secret reference type and store binding — [D: api/v1alpha1/secretreference_types.go:134]
- Value-from indirection — [D: api/v1alpha1/dataplane_types.go:22]
- Git secret service — [D: internal/openchoreo-api/services/gitsecret]
- Secret service — [D: internal/openchoreo-api/services/secret]
- occ secret command — [D: internal/occ/cmd/secret]
- External-secrets e2e suite — [D: test/e2e/suites/secrets]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-008-secrets-management.md`; exercised by `tests/test_v1.2.0_F-008.md`.

## Open questions

OPEN: `gitsecrets` supports GET, POST and DELETE but no PUT. Is rotation expected to be delete-then-create, and is that gap deliberate?

OPEN: OpenBao is used in the e2e suite. Is it the supported store, a test double, or one of several supported backends?

OPEN: what is the intended rotation and revocation story? Nothing in the repository expresses a secret lifetime.

