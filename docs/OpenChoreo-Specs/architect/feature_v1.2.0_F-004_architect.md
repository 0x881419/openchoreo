---
title: Feature Architecture v1.2.0 F-004 — Authorization and Access Control
id: F-004
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-004 — Authorization and Access Control
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: authorization is centralised in a Casbin PDP fed by CRDs and validated at admission, rather than scattered across handlers, and it fails closed on a malformed policy — basis: the PDP serialises one request context for all entitlements, and the test suite states that "a broken entry anywhere in the policy poisons the whole CR, even if a sibling entry cleanly matched" [D: internal/authz/casbin/helpers_test.go:1559].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
24 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/authn/subject-types` | [D: openapi/openchoreo-api.yaml:3685] |
| GET | `/api/v1/authz/actions` | [D: openapi/openchoreo-api.yaml:2941] |
| POST | `/api/v1/authz/evaluates` | [D: openapi/openchoreo-api.yaml:2963] |
| GET | `/api/v1/authz/profile` | [D: openapi/openchoreo-api.yaml:2995] |
| GET | `/api/v1/clusterauthzrolebindings` | [D: openapi/openchoreo-api.yaml:3202] |
| POST | `/api/v1/clusterauthzrolebindings` | [D: openapi/openchoreo-api.yaml:3227] |
| DELETE | `/api/v1/clusterauthzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3329] |
| GET | `/api/v1/clusterauthzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3259] |
| PUT | `/api/v1/clusterauthzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3288] |
| GET | `/api/v1/clusterauthzroles` | [D: openapi/openchoreo-api.yaml:3049] |
| POST | `/api/v1/clusterauthzroles` | [D: openapi/openchoreo-api.yaml:3074] |
| DELETE | `/api/v1/clusterauthzroles/{name}` | [D: openapi/openchoreo-api.yaml:3174] |
| GET | `/api/v1/clusterauthzroles/{name}` | [D: openapi/openchoreo-api.yaml:3106] |
| PUT | `/api/v1/clusterauthzroles/{name}` | [D: openapi/openchoreo-api.yaml:3135] |
| GET | `/api/v1/namespaces/{namespaceName}/authzrolebindings` | [D: openapi/openchoreo-api.yaml:3518] |
| POST | `/api/v1/namespaces/{namespaceName}/authzrolebindings` | [D: openapi/openchoreo-api.yaml:3544] |
| DELETE | `/api/v1/namespaces/{namespaceName}/authzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3652] |
| GET | `/api/v1/namespaces/{namespaceName}/authzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3578] |
| PUT | `/api/v1/namespaces/{namespaceName}/authzrolebindings/{name}` | [D: openapi/openchoreo-api.yaml:3610] |
| GET | `/api/v1/namespaces/{namespaceName}/authzroles` | [D: openapi/openchoreo-api.yaml:3355] |
| POST | `/api/v1/namespaces/{namespaceName}/authzroles` | [D: openapi/openchoreo-api.yaml:3381] |
| DELETE | `/api/v1/namespaces/{namespaceName}/authzroles/{name}` | [D: openapi/openchoreo-api.yaml:3487] |
| GET | `/api/v1/namespaces/{namespaceName}/authzroles/{name}` | [D: openapi/openchoreo-api.yaml:3415] |
| PUT | `/api/v1/namespaces/{namespaceName}/authzroles/{name}` | [D: openapi/openchoreo-api.yaml:3447] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| AuthzRole | `actions`, `description` | [D: api/v1alpha1/authzrole_types.go:28] |
| AuthzRoleBinding | `entitlement`, `roleMappings`, `effect` | [D: api/v1alpha1/authzrolebinding_types.go:69] |
| ClusterAuthzRole | `actions`, `description` | [D: api/v1alpha1/clusterauthzrole_types.go:28] |
| ClusterAuthzRoleBinding | `entitlement`, `roleMappings`, `effect` | [D: api/v1alpha1/clusterauthzrolebinding_types.go:74] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence

Supporting code paths:

- Policy watchers registered on the manager — this feature has no reconciler — [D: internal/authz/casbin/k8s_watcher.go:29]
- Casbin policy decision point — [D: internal/authz/casbin/pdp.go:251]
- Kubernetes policy watcher — [D: internal/authz/casbin/k8s_watcher_test.go:2412]
- Resource hierarchy, with the sibling invariant stated — [D: internal/authz/core/types.go:26]
- Disabled-authorizer fallback — [D: internal/authz/disabled_authorizer.go:1]
- Admission webhook for role bindings — [D: internal/webhook/authzrolebinding/suite_test.go:54]
- Fail-closed on a malformed policy entry — [D: internal/authz/casbin/helpers_test.go:1559]

OPEN: the happy-path call order above is read off reconciler registration and ownership, not off a trace. A recorded trace from a running install would confirm or correct it.

## Failure modes
| Failure | Detection | Behaviour in code | Evidence |
| --- | --- | --- | --- |
| Resource deleted while dependents exist | finalizer on the parent | cleanup runs before the object is released | [D: internal/controller/component/controller.go:1] |

OPEN: which of these failures page someone, and which are expected steady-state noise? No alerting rule in the repository distinguishes them.

## Observability
- Structured logging via logr/zap [D: go.mod:9]
- Prometheus metrics exposed by controller-runtime [D: config/prometheus]
- Audit events for every non-exempt API operation [D: internal/openchoreo-api/audit/definitions.gen.go:1]

OPEN: this feature emits no metric named for its own domain. Which signals should it own, as opposed to inheriting from the framework?

## Traceability
Satisfies the stories in `PRDs/prd_v1.2.0_F-004-authorization-and-access-control.md`; exercised by `tests/test_v1.2.0_F-004.md`.

## Open questions

OPEN: this is the only CRD family in the platform with no controller package: the four authz kinds are watched and pushed into the Casbin enforcer rather than reconciled toward a desired state. Is that a deliberate split, and what reports drift if the enforcer and the CRDs disagree?

OPEN: Casbin was chosen over Kubernetes RBAC, OPA/Rego and an in-house evaluator. No record of that comparison exists in the repository.

OPEN: what is the intended blast radius of the disabled authorizer — local development only, or is there a supported deployment that runs without a PDP?

OPEN: deny-override semantics are exercised by the e2e suite. Is deny-wins a stated product guarantee, or current behaviour that could change?

