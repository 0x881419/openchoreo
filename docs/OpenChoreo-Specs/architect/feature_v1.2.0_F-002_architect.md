---
title: Feature Architecture v1.2.0 F-002 — Platform Abstractions and Templating
id: F-002
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-002 — Platform Abstractions and Templating
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: platform engineers extend the platform by writing declarative CEL templates with OpenAPI-v3-typed parameters rather than Go code, and every abstraction is offered in a namespaced and a cluster-scoped variant so the same definition can be shared or confined — basis: eight paired kinds each expose a `/schema` endpoint, and the render path evaluates CEL under an explicit cost budget [D: internal/template/budget.go:1].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
48 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/clustercomponenttypes` | [D: openapi/openchoreo-api.yaml:1561] |
| POST | `/api/v1/clustercomponenttypes` | [D: openapi/openchoreo-api.yaml:1586] |
| DELETE | `/api/v1/clustercomponenttypes/{cctName}` | [D: openapi/openchoreo-api.yaml:1676] |
| GET | `/api/v1/clustercomponenttypes/{cctName}` | [D: openapi/openchoreo-api.yaml:1618] |
| PUT | `/api/v1/clustercomponenttypes/{cctName}` | [D: openapi/openchoreo-api.yaml:1641] |
| GET | `/api/v1/clustercomponenttypes/{cctName}/schema` | [D: openapi/openchoreo-api.yaml:1696] |
| GET | `/api/v1/clusterprojecttypes` | [D: openapi/openchoreo-api.yaml:4651] |
| POST | `/api/v1/clusterprojecttypes` | [D: openapi/openchoreo-api.yaml:4676] |
| DELETE | `/api/v1/clusterprojecttypes/{cptName}` | [D: openapi/openchoreo-api.yaml:4762] |
| GET | `/api/v1/clusterprojecttypes/{cptName}` | [D: openapi/openchoreo-api.yaml:4706] |
| PUT | `/api/v1/clusterprojecttypes/{cptName}` | [D: openapi/openchoreo-api.yaml:4729] |
| GET | `/api/v1/clusterprojecttypes/{cptName}/schema` | [D: openapi/openchoreo-api.yaml:4782] |
| GET | `/api/v1/clusterresourcetypes` | [D: openapi/openchoreo-api.yaml:4492] |
| POST | `/api/v1/clusterresourcetypes` | [D: openapi/openchoreo-api.yaml:4517] |
| DELETE | `/api/v1/clusterresourcetypes/{crtName}` | [D: openapi/openchoreo-api.yaml:4603] |
| GET | `/api/v1/clusterresourcetypes/{crtName}` | [D: openapi/openchoreo-api.yaml:4547] |
| PUT | `/api/v1/clusterresourcetypes/{crtName}` | [D: openapi/openchoreo-api.yaml:4570] |
| GET | `/api/v1/clusterresourcetypes/{crtName}/schema` | [D: openapi/openchoreo-api.yaml:4623] |
| GET | `/api/v1/clustertraits` | [D: openapi/openchoreo-api.yaml:1724] |
| POST | `/api/v1/clustertraits` | [D: openapi/openchoreo-api.yaml:1749] |
| DELETE | `/api/v1/clustertraits/{clusterTraitName}` | [D: openapi/openchoreo-api.yaml:1839] |
| GET | `/api/v1/clustertraits/{clusterTraitName}` | [D: openapi/openchoreo-api.yaml:1781] |
| PUT | `/api/v1/clustertraits/{clusterTraitName}` | [D: openapi/openchoreo-api.yaml:1804] |
| GET | `/api/v1/clustertraits/{clusterTraitName}/schema` | [D: openapi/openchoreo-api.yaml:1859] |
| GET | `/api/v1/namespaces/{namespaceName}/componenttypes` | [D: openapi/openchoreo-api.yaml:1887] |
| POST | `/api/v1/namespaces/{namespaceName}/componenttypes` | [D: openapi/openchoreo-api.yaml:1913] |
| DELETE | `/api/v1/namespaces/{namespaceName}/componenttypes/{ctName}` | [D: openapi/openchoreo-api.yaml:2007] |
| GET | `/api/v1/namespaces/{namespaceName}/componenttypes/{ctName}` | [D: openapi/openchoreo-api.yaml:1947] |
| PUT | `/api/v1/namespaces/{namespaceName}/componenttypes/{ctName}` | [D: openapi/openchoreo-api.yaml:1971] |
| GET | `/api/v1/namespaces/{namespaceName}/componenttypes/{ctName}/schema` | [D: openapi/openchoreo-api.yaml:2028] |
| GET | `/api/v1/namespaces/{namespaceName}/projecttypes` | [D: openapi/openchoreo-api.yaml:4810] |
| POST | `/api/v1/namespaces/{namespaceName}/projecttypes` | [D: openapi/openchoreo-api.yaml:4836] |
| DELETE | `/api/v1/namespaces/{namespaceName}/projecttypes/{ptName}` | [D: openapi/openchoreo-api.yaml:4926] |
| GET | `/api/v1/namespaces/{namespaceName}/projecttypes/{ptName}` | [D: openapi/openchoreo-api.yaml:4868] |
| PUT | `/api/v1/namespaces/{namespaceName}/projecttypes/{ptName}` | [D: openapi/openchoreo-api.yaml:4892] |
| GET | `/api/v1/namespaces/{namespaceName}/projecttypes/{ptName}/schema` | [D: openapi/openchoreo-api.yaml:4947] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcetypes` | [D: openapi/openchoreo-api.yaml:5222] |
| POST | `/api/v1/namespaces/{namespaceName}/resourcetypes` | [D: openapi/openchoreo-api.yaml:5248] |
| DELETE | `/api/v1/namespaces/{namespaceName}/resourcetypes/{rtName}` | [D: openapi/openchoreo-api.yaml:5338] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcetypes/{rtName}` | [D: openapi/openchoreo-api.yaml:5280] |
| PUT | `/api/v1/namespaces/{namespaceName}/resourcetypes/{rtName}` | [D: openapi/openchoreo-api.yaml:5304] |
| GET | `/api/v1/namespaces/{namespaceName}/resourcetypes/{rtName}/schema` | [D: openapi/openchoreo-api.yaml:5359] |
| GET | `/api/v1/namespaces/{namespaceName}/traits` | [D: openapi/openchoreo-api.yaml:2057] |
| POST | `/api/v1/namespaces/{namespaceName}/traits` | [D: openapi/openchoreo-api.yaml:2083] |
| DELETE | `/api/v1/namespaces/{namespaceName}/traits/{traitName}` | [D: openapi/openchoreo-api.yaml:2177] |
| GET | `/api/v1/namespaces/{namespaceName}/traits/{traitName}` | [D: openapi/openchoreo-api.yaml:2117] |
| PUT | `/api/v1/namespaces/{namespaceName}/traits/{traitName}` | [D: openapi/openchoreo-api.yaml:2141] |
| GET | `/api/v1/namespaces/{namespaceName}/traits/{traitName}/schema` | [D: openapi/openchoreo-api.yaml:2198] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| ComponentType | `workloadType`, `allowedWorkflows`, `parameters`, `environmentConfigs`, `traits`, `allowedTraits`, `validations`, `preRenderValidations`… | [D: api/v1alpha1/componenttype_types.go:265] |
| ClusterComponentType | `workloadType`, `allowedWorkflows`, `parameters`, `environmentConfigs`, `traits`, `allowedTraits`, `validations`, `preRenderValidations`… | [D: api/v1alpha1/clustercomponenttype_types.go:141] |
| Trait | `parameters`, `environmentConfigs`, `validations`, `preRenderValidations`, `postRenderValidations`, `creates`, `patches`, `removes` | [D: api/v1alpha1/trait_types.go:301] |
| ClusterTrait | `parameters`, `environmentConfigs`, `validations`, `preRenderValidations`, `postRenderValidations`, `creates`, `patches`, `removes` | [D: api/v1alpha1/clustertrait_types.go:65] |
| ResourceType | `parameters`, `environmentConfigs`, `retainPolicy`, `outputs`, `resources` | [D: api/v1alpha1/resourcetype_types.go:132] |
| ClusterResourceType | `parameters`, `environmentConfigs`, `retainPolicy`, `outputs`, `resources` | [D: api/v1alpha1/clusterresourcetype_types.go:61] |
| ProjectType | `parameters`, `environmentConfigs`, `validations`, `resources` | [D: api/v1alpha1/projecttype_types.go:52] |
| ClusterProjectType | `parameters`, `environmentConfigs`, `validations`, `resources` | [D: api/v1alpha1/clusterprojecttype_types.go:52] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `componenttype` — [D: internal/controller/componenttype/controller.go:1]
2. `clustercomponenttype` — [D: internal/controller/clustercomponenttype/controller.go:1]
3. `trait` — [D: internal/controller/trait/controller.go:1]
4. `clustertrait` — [D: internal/controller/clustertrait/controller.go:1]
5. `resourcetype` — [D: internal/controller/resourcetype/controller.go:1]
6. `clusterresourcetype` — [D: internal/controller/clusterresourcetype/controller.go:1]
7. `projecttype` — [D: internal/controller/projecttype/controller.go:1]
8. `clusterprojecttype` — [D: internal/controller/clusterprojecttype/controller.go:1]

Supporting code paths:

- CEL template engine — [D: internal/template/engine.go:1]
- Render cost budget — [D: internal/template/budget.go:1]
- Custom CEL functions — [D: internal/template/custom_functions.go:1]
- OpenAPI v3 parameter schema handling — [D: internal/schema/openapiv3.go:1]
- Schema $ref resolution — [D: internal/schema/ref_resolver.go:1]
- Exactly-one-of output rule on ResourceType — [D: api/v1alpha1/resourcetype_types.go:49]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-002-platform-abstractions-and-templating.md`; exercised by `tests/test_v1.2.0_F-002.md`.

## Open questions

OPEN: what is the cost budget's unit and its default ceiling, and what happens to a tenant whose template exceeds it — is it a guardrail against accident or against abuse?

OPEN: CEL was chosen over Go plugins, CUE, Helm templating and Kustomize. The code records CEL; it records nothing about what was weighed.

OPEN: when does an abstraction belong at cluster scope rather than namespace scope? The pairing is mechanical; the governance rule for choosing is not in the repository.

