---
title: Feature Architecture v1.2.0 F-003 — Project and Resource Delivery
id: F-003
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-003 — Project and Resource Delivery
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: projects and backing resources reuse the Component pipeline's exact shape — definition, immutable release, per-environment binding, rendered output — so a reader who understands one understands all three — basis: three parallel CRD triples, three parallel binding controllers, and all three converge on the same `RenderedRelease` kind [D: internal/controller/projectreleasebinding/controller_render.go:82].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
28 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/namespaces/{namespaceName}/projectreleasebindings` | [D: openapi/openchoreo-api.yaml:5082] |
| POST | `/api/v1/namespaces/{namespaceName}/projectreleasebindings` | [D: openapi/openchoreo-api.yaml:5109] |
| DELETE | `/api/v1/namespaces/{namespaceName}/projectreleasebindings/{projectReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5197] |
| GET | `/api/v1/namespaces/{namespaceName}/projectreleasebindings/{projectReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5141] |
| PUT | `/api/v1/namespaces/{namespaceName}/projectreleasebindings/{projectReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5165] |
| GET | `/api/v1/namespaces/{namespaceName}/projectreleases` | [D: openapi/openchoreo-api.yaml:4976] |
| POST | `/api/v1/namespaces/{namespaceName}/projectreleases` | [D: openapi/openchoreo-api.yaml:5002] |
| DELETE | `/api/v1/namespaces/{namespaceName}/projectreleases/{projectReleaseName}` | [D: openapi/openchoreo-api.yaml:5057] |
| GET | `/api/v1/namespaces/{namespaceName}/projectreleases/{projectReleaseName}` | [D: openapi/openchoreo-api.yaml:5034] |
| GET | `/api/v1/namespaces/{namespaceName}/projects` | [D: openapi/openchoreo-api.yaml:335] |
| POST | `/api/v1/namespaces/{namespaceName}/projects` | [D: openapi/openchoreo-api.yaml:363] |
| DELETE | `/api/v1/namespaces/{namespaceName}/projects/{projectName}` | [D: openapi/openchoreo-api.yaml:457] |
| GET | `/api/v1/namespaces/{namespaceName}/projects/{projectName}` | [D: openapi/openchoreo-api.yaml:397] |
| PUT | `/api/v1/namespaces/{namespaceName}/projects/{projectName}` | [D: openapi/openchoreo-api.yaml:421] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcereleasebindings` | [D: openapi/openchoreo-api.yaml:5636] |
| POST | `/api/v1/namespaces/{namespaceName}/resourcereleasebindings` | [D: openapi/openchoreo-api.yaml:5663] |
| DELETE | `/api/v1/namespaces/{namespaceName}/resourcereleasebindings/{resourceReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5751] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcereleasebindings/{resourceReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5695] |
| PUT | `/api/v1/namespaces/{namespaceName}/resourcereleasebindings/{resourceReleaseBindingName}` | [D: openapi/openchoreo-api.yaml:5719] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcereleases` | [D: openapi/openchoreo-api.yaml:5530] |
| POST | `/api/v1/namespaces/{namespaceName}/resourcereleases` | [D: openapi/openchoreo-api.yaml:5556] |
| DELETE | `/api/v1/namespaces/{namespaceName}/resourcereleases/{resourceReleaseName}` | [D: openapi/openchoreo-api.yaml:5611] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcereleases/{resourceReleaseName}` | [D: openapi/openchoreo-api.yaml:5588] |
| GET | `/api/v1/namespaces/{namespaceName}/resources` | [D: openapi/openchoreo-api.yaml:5388] |
| POST | `/api/v1/namespaces/{namespaceName}/resources` | [D: openapi/openchoreo-api.yaml:5417] |
| DELETE | `/api/v1/namespaces/{namespaceName}/resources/{resourceName}` | [D: openapi/openchoreo-api.yaml:5505] |
| GET | `/api/v1/namespaces/{namespaceName}/resources/{resourceName}` | [D: openapi/openchoreo-api.yaml:5449] |
| PUT | `/api/v1/namespaces/{namespaceName}/resources/{resourceName}` | [D: openapi/openchoreo-api.yaml:5473] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| Project | `deploymentPipelineRef`, `type`, `parameters` | [D: api/v1alpha1/project_types.go:70] |
| ProjectRelease | `owner`, `projectType`, `parameters` | [D: api/v1alpha1/projectrelease_types.go:82] |
| ProjectReleaseBinding | `owner`, `environment`, `projectRelease`, `environmentConfigs` | [D: api/v1alpha1/projectreleasebinding_types.go:93] |
| Resource | `owner`, `type`, `parameters` | [D: api/v1alpha1/resource_types.go:83] |
| ResourceRelease | `owner`, `resourceType`, `parameters` | [D: api/v1alpha1/resourcerelease_types.go:90] |
| ResourceReleaseBinding | `owner`, `environment`, `resourceRelease`, `retainPolicy`, `resourceTypeEnvironmentConfigs` | [D: api/v1alpha1/resourcereleasebinding_types.go:131] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `project` — [D: internal/controller/project/controller.go:1]
2. `projectrelease` — [D: internal/controller/projectrelease/controller.go:1]
3. `projectreleasebinding` — [D: internal/controller/projectreleasebinding/controller.go:1]
4. `resource` — [D: internal/controller/resource/controller.go:1]
5. `resourcerelease` — [D: internal/controller/resourcerelease/controller.go:1]
6. `resourcereleasebinding` — [D: internal/controller/resourcereleasebinding/controller.go:1]

Supporting code paths:

- Project render pipeline — [D: internal/pipeline/project/pipeline.go:1]
- Project gateway wiring — [D: internal/pipeline/project/gateway.go:1]
- Resource render pipeline — [D: internal/pipeline/resource]
- ProjectReleaseBinding emits a RenderedRelease — [D: internal/controller/projectreleasebinding/controller_render.go:82]
- ResourceReleaseBinding emits a RenderedRelease — [D: internal/controller/resourcereleasebinding/controller.go:264]
- Resolved resource outputs are surfaced back on the binding — [D: api/v1alpha1/resourcereleasebinding_types.go:94]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-003-project-and-resource-delivery.md`; exercised by `tests/test_v1.2.0_F-003.md`.

## Open questions

OPEN: is the three-way symmetry with F-001 intentional design or convergent evolution? Nothing in the repository records a decision to unify them.

OPEN: resource outputs can be a literal value, a Secret key or a ConfigMap key. Which is the expected default for a credential, and is the literal path meant for production at all?

OPEN: what is the intended lifecycle when a Resource is deleted while components still declare a dependency on it?

