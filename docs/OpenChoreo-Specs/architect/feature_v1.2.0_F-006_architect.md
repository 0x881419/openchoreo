---
title: Feature Architecture v1.2.0 F-006 — Build and Workflow Execution
id: F-006
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-006 — Build and Workflow Execution
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: builds are modelled as ordinary platform abstractions rather than a separate subsystem: a Workflow is a parameterised template like a ComponentType, and a WorkflowRun is its execution with status, logs and events exposed as sub-resources — basis: Workflow and ClusterWorkflow expose the same `/schema` endpoint as the other abstractions, and WorkflowRun carries three read-only sub-resources [D: api/v1alpha1/workflowrun_types.go:151].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
21 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/clusterworkflows` | [D: openapi/openchoreo-api.yaml:2227] |
| POST | `/api/v1/clusterworkflows` | [D: openapi/openchoreo-api.yaml:2252] |
| DELETE | `/api/v1/clusterworkflows/{clusterWorkflowName}` | [D: openapi/openchoreo-api.yaml:2342] |
| GET | `/api/v1/clusterworkflows/{clusterWorkflowName}` | [D: openapi/openchoreo-api.yaml:2284] |
| PUT | `/api/v1/clusterworkflows/{clusterWorkflowName}` | [D: openapi/openchoreo-api.yaml:2307] |
| GET | `/api/v1/clusterworkflows/{clusterWorkflowName}/schema` | [D: openapi/openchoreo-api.yaml:2362] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowruns` | [D: openapi/openchoreo-api.yaml:2560] |
| POST | `/api/v1/namespaces/{namespaceName}/workflowruns` | [D: openapi/openchoreo-api.yaml:2587] |
| DELETE | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}` | [D: openapi/openchoreo-api.yaml:2679] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}` | [D: openapi/openchoreo-api.yaml:2621] |
| PUT | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}` | [D: openapi/openchoreo-api.yaml:2645] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}/events` | [D: openapi/openchoreo-api.yaml:2764] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}/logs` | [D: openapi/openchoreo-api.yaml:2723] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowruns/{runName}/status` | [D: openapi/openchoreo-api.yaml:2700] |
| GET | `/api/v1/namespaces/{namespaceName}/workflows` | [D: openapi/openchoreo-api.yaml:2390] |
| POST | `/api/v1/namespaces/{namespaceName}/workflows` | [D: openapi/openchoreo-api.yaml:2416] |
| DELETE | `/api/v1/namespaces/{namespaceName}/workflows/{workflowName}` | [D: openapi/openchoreo-api.yaml:2510] |
| GET | `/api/v1/namespaces/{namespaceName}/workflows/{workflowName}` | [D: openapi/openchoreo-api.yaml:2450] |
| PUT | `/api/v1/namespaces/{namespaceName}/workflows/{workflowName}` | [D: openapi/openchoreo-api.yaml:2474] |
| GET | `/api/v1/namespaces/{namespaceName}/workflows/{workflowName}/schema` | [D: openapi/openchoreo-api.yaml:2531] |
| POST | `/api/v1alpha1/autobuild` | [D: openapi/openchoreo-api.yaml:3709] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| Workflow | `workflowPlaneRef`, `parameters`, `runTemplate`, `resources`, `externalRefs`, `ttlAfterCompletion` | [D: api/v1alpha1/workflow_types.go:155] |
| ClusterWorkflow | `workflowPlaneRef`, `parameters`, `runTemplate`, `resources`, `externalRefs`, `ttlAfterCompletion` | [D: api/v1alpha1/clusterworkflow_types.go:79] |
| WorkflowRun | `workflow`, `ttlAfterCompletion` | [D: api/v1alpha1/workflowrun_types.go:151] |
| WorkflowPlane | `planeID`, `clusterAgent`, `secretStoreRef`, `observabilityPlaneRef` | [D: api/v1alpha1/workflowplane_types.go:66] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `workflow` — [D: internal/controller/workflow/controller.go:1]
2. `clusterworkflow` — [D: internal/controller/clusterworkflow/controller.go:1]
3. `workflowrun` — [D: internal/controller/workflowrun/controller.go:1]
4. `workflowplane` — [D: internal/controller/workflowplane/controller.go:1]

Supporting code paths:

- Autobuild service — [D: internal/openchoreo-api/services/autobuild]
- Component source: git repository and container registry — [D: api/v1alpha1/component_types.go:163]
- Workflow configuration on a component — [D: api/v1alpha1/component_types.go:83]
- Build engine options — [D: docs/contributors/build-engines.md:1]
- Workflow template samples — [D: test/workflowtemplates]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-006-build-and-workflow-execution.md`; exercised by `tests/test_v1.2.0_F-006.md`.

## Open questions

OPEN: the CI plane is described as optional. What is lost when it is absent — image builds only, or any workflow execution?

OPEN: Argo Workflows and cloud native Buildpacks are the stated defaults. What is the supported path for replacing either, and is it a supported extension point or an implementation detail?

OPEN: what is the retention policy for WorkflowRun objects and their logs? The controller deletes runs, but no retention window is expressed anywhere.

