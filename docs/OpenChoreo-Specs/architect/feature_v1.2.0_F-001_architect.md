---
title: Feature Architecture v1.2.0 F-001 — Component Delivery Pipeline
id: F-001
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-001 — Component Delivery Pipeline
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: the feature is a four-stage reduction from mutable developer intent to applied cluster state, with immutability introduced at stage two — basis: `Component` is edited freely, `ComponentRelease` is described by its own design doc as "an immutable snapshot… containing the frozen ComponentType, Traits, and Workload specifications", `ReleaseBinding` re-introduces variation per environment, and only `RenderedRelease` touches a data-plane cluster [D: docs/crds/renderedrelease.md:44].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
25 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/namespaces/{namespaceName}/componentreleases` | [D: openapi/openchoreo-api.yaml:4067] |
| POST | `/api/v1/namespaces/{namespaceName}/componentreleases` | [D: openapi/openchoreo-api.yaml:4095] |
| DELETE | `/api/v1/namespaces/{namespaceName}/componentreleases/{componentReleaseName}` | [D: openapi/openchoreo-api.yaml:4152] |
| GET | `/api/v1/namespaces/{namespaceName}/componentreleases/{componentReleaseName}` | [D: openapi/openchoreo-api.yaml:4129] |
| GET | `/api/v1/namespaces/{namespaceName}/components` | [D: openapi/openchoreo-api.yaml:482] |
| POST | `/api/v1/namespaces/{namespaceName}/components` | [D: openapi/openchoreo-api.yaml:511] |
| DELETE | `/api/v1/namespaces/{namespaceName}/components/{componentName}` | [D: openapi/openchoreo-api.yaml:2857] |
| GET | `/api/v1/namespaces/{namespaceName}/components/{componentName}` | [D: openapi/openchoreo-api.yaml:2797] |
| PUT | `/api/v1/namespaces/{namespaceName}/components/{componentName}` | [D: openapi/openchoreo-api.yaml:2821] |
| POST | `/api/v1/namespaces/{namespaceName}/components/{componentName}/generate-release` | [D: openapi/openchoreo-api.yaml:2903] |
| GET | `/api/v1/namespaces/{namespaceName}/components/{componentName}/schema` | [D: openapi/openchoreo-api.yaml:2878] |
| GET | `/api/v1/namespaces/{namespaceName}/releasebindings` | [D: openapi/openchoreo-api.yaml:4177] |
| POST | `/api/v1/namespaces/{namespaceName}/releasebindings` | [D: openapi/openchoreo-api.yaml:4206] |
| DELETE | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}` | [D: openapi/openchoreo-api.yaml:4298] |
| GET | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}` | [D: openapi/openchoreo-api.yaml:4240] |
| PUT | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}` | [D: openapi/openchoreo-api.yaml:4264] |
| GET | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}/k8sresources/events` | [D: openapi/openchoreo-api.yaml:4346] |
| GET | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}/k8sresources/logs` | [D: openapi/openchoreo-api.yaml:4397] |
| GET | `/api/v1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}/k8sresources/tree` | [D: openapi/openchoreo-api.yaml:4319] |
| GET | `/api/v1/namespaces/{namespaceName}/workloads` | [D: openapi/openchoreo-api.yaml:3921] |
| POST | `/api/v1/namespaces/{namespaceName}/workloads` | [D: openapi/openchoreo-api.yaml:3950] |
| DELETE | `/api/v1/namespaces/{namespaceName}/workloads/{workloadName}` | [D: openapi/openchoreo-api.yaml:4042] |
| GET | `/api/v1/namespaces/{namespaceName}/workloads/{workloadName}` | [D: openapi/openchoreo-api.yaml:3984] |
| PUT | `/api/v1/namespaces/{namespaceName}/workloads/{workloadName}` | [D: openapi/openchoreo-api.yaml:4008] |
| POST | `/api/v1alpha1/namespaces/{namespaceName}/releasebindings/{releaseBindingName}/trigger` | [D: openapi/openchoreo-api.yaml:4446] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| Component | `owner`, `componentType`, `autoDeploy`, `autoBuild`, `parameters`, `traits`, `workflow` | [D: api/v1alpha1/component_types.go:19] |
| ComponentRelease | `owner`, `componentType`, `traits`, `componentProfile`, `workload` | [D: api/v1alpha1/componentrelease_types.go:138] |
| ReleaseBinding | `owner`, `environment`, `releaseName`, `componentTypeEnvironmentConfigs`, `traitEnvironmentConfigs`, `workloadOverrides`, `state` | [D: api/v1alpha1/releasebinding_types.go:383] |
| RenderedRelease | `owner`, `environmentName`, `resources`, `interval`, `progressingInterval`, `targetPlane` | [D: api/v1alpha1/renderedrelease_types.go:66] |
| Workload | `owner` | [D: api/v1alpha1/workload_types.go:372] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `component` — [D: internal/controller/component/controller.go:52]
2. `componentrelease` — [D: internal/controller/componentrelease/controller.go:27]
3. `releasebinding` — [D: internal/controller/releasebinding/controller.go:130]
4. `renderedrelease` — [D: internal/controller/renderedrelease/controller.go:81]

Supporting code paths:

- Rendering pipeline entry point — [D: internal/pipeline/component/pipeline.go:96]
- Pipeline responsibilities, stated by its own package comment — [D: internal/pipeline/component/pipeline.go:5]
- ReleaseBinding emits a data-plane RenderedRelease — [D: internal/controller/releasebinding/controller.go:627]
- …and a second one for the observability plane — [D: internal/controller/releasebinding/controller.go:825]
- Endpoint-to-route-kind compatibility rule — [D: internal/controller/releasebinding/controller.go:5]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-001-component-delivery-pipeline.md`; exercised by `tests/test_v1.2.0_F-001.md`.

## Open questions

OPEN: why is the snapshot boundary at ComponentRelease rather than at ReleaseBinding? Both are plausible designs; the code records only the one that was built.

OPEN: what happens to a running workload when its ComponentRelease is deleted but its ReleaseBinding survives? The finalizer ordering is in the code; the intended operator experience is not.

OPEN: is the two-RenderedRelease split (data plane + observability plane) a permanent part of the model, or a step toward a single rendered artefact?

