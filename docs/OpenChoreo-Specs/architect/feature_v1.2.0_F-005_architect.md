---
title: Feature Architecture v1.2.0 F-005 — Multi-Plane Topology and Connectivity
id: F-005
status: draft
owner: TBD
updated: 2026-09-19
---

# Feature Architecture v1.2.0 F-005 — Multi-Plane Topology and Connectivity
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

## Design summary
I: the control plane never dials a managed cluster: the agent dials out and the gateway multiplexes work back over that connection, and `occ remote` bypasses the control plane for bytes while keeping it in the authorization path — basis: the remote-connect package comment states that "the byte path does not traverse the control plane" while each stream still calls back for authorization [D: internal/remoteconnect/doc.go:15].

What it rules out is visible only as absence, so it is recorded as a question rather than a claim — see Open questions.

## API contracts
47 operation(s), all declared in the in-repo OpenAPI specs, which outrank the Go route table: the server interface is generated from them [D: make/golang.mk:191] and mounted as a catch-all [D: cmd/openchoreo-api/main.go:377].

| Method | Path | Declared at |
| --- | --- | --- |
| GET | `/api/v1/clusterdataplanes` | [D: openapi/openchoreo-api.yaml:1129] |
| POST | `/api/v1/clusterdataplanes` | [D: openapi/openchoreo-api.yaml:1154] |
| DELETE | `/api/v1/clusterdataplanes/{cdpName}` | [D: openapi/openchoreo-api.yaml:1244] |
| GET | `/api/v1/clusterdataplanes/{cdpName}` | [D: openapi/openchoreo-api.yaml:1186] |
| PUT | `/api/v1/clusterdataplanes/{cdpName}` | [D: openapi/openchoreo-api.yaml:1209] |
| GET | `/api/v1/clusterobservabilityplanes` | [D: openapi/openchoreo-api.yaml:1422] |
| POST | `/api/v1/clusterobservabilityplanes` | [D: openapi/openchoreo-api.yaml:1447] |
| DELETE | `/api/v1/clusterobservabilityplanes/{clusterObservabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1537] |
| GET | `/api/v1/clusterobservabilityplanes/{clusterObservabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1479] |
| PUT | `/api/v1/clusterobservabilityplanes/{clusterObservabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1502] |
| GET | `/api/v1/clusterworkflowplanes` | [D: openapi/openchoreo-api.yaml:1268] |
| POST | `/api/v1/clusterworkflowplanes` | [D: openapi/openchoreo-api.yaml:1293] |
| DELETE | `/api/v1/clusterworkflowplanes/{clusterWorkflowPlaneName}` | [D: openapi/openchoreo-api.yaml:1393] |
| GET | `/api/v1/clusterworkflowplanes/{clusterWorkflowPlaneName}` | [D: openapi/openchoreo-api.yaml:1325] |
| PUT | `/api/v1/clusterworkflowplanes/{clusterWorkflowPlaneName}` | [D: openapi/openchoreo-api.yaml:1353] |
| GET | `/api/v1/namespaces` | [D: openapi/openchoreo-api.yaml:192] |
| POST | `/api/v1/namespaces` | [D: openapi/openchoreo-api.yaml:221] |
| GET | `/api/v1/namespaces/{namespaceName}/dataplanes` | [D: openapi/openchoreo-api.yaml:694] |
| POST | `/api/v1/namespaces/{namespaceName}/dataplanes` | [D: openapi/openchoreo-api.yaml:720] |
| DELETE | `/api/v1/namespaces/{namespaceName}/dataplanes/{dpName}` | [D: openapi/openchoreo-api.yaml:814] |
| GET | `/api/v1/namespaces/{namespaceName}/dataplanes/{dpName}` | [D: openapi/openchoreo-api.yaml:754] |
| PUT | `/api/v1/namespaces/{namespaceName}/dataplanes/{dpName}` | [D: openapi/openchoreo-api.yaml:778] |
| GET | `/api/v1/namespaces/{namespaceName}/deploymentpipelines` | [D: openapi/openchoreo-api.yaml:5776] |
| POST | `/api/v1/namespaces/{namespaceName}/deploymentpipelines` | [D: openapi/openchoreo-api.yaml:5802] |
| DELETE | `/api/v1/namespaces/{namespaceName}/deploymentpipelines/{deploymentPipelineName}` | [D: openapi/openchoreo-api.yaml:5894] |
| GET | `/api/v1/namespaces/{namespaceName}/deploymentpipelines/{deploymentPipelineName}` | [D: openapi/openchoreo-api.yaml:5836] |
| PUT | `/api/v1/namespaces/{namespaceName}/deploymentpipelines/{deploymentPipelineName}` | [D: openapi/openchoreo-api.yaml:5860] |
| GET | `/api/v1/namespaces/{namespaceName}/environments` | [D: openapi/openchoreo-api.yaml:549] |
| POST | `/api/v1/namespaces/{namespaceName}/environments` | [D: openapi/openchoreo-api.yaml:575] |
| DELETE | `/api/v1/namespaces/{namespaceName}/environments/{envName}` | [D: openapi/openchoreo-api.yaml:669] |
| GET | `/api/v1/namespaces/{namespaceName}/environments/{envName}` | [D: openapi/openchoreo-api.yaml:609] |
| PUT | `/api/v1/namespaces/{namespaceName}/environments/{envName}` | [D: openapi/openchoreo-api.yaml:633] |
| GET | `/api/v1/namespaces/{namespaceName}/observabilityplanes` | [D: openapi/openchoreo-api.yaml:984] |
| POST | `/api/v1/namespaces/{namespaceName}/observabilityplanes` | [D: openapi/openchoreo-api.yaml:1010] |
| DELETE | `/api/v1/namespaces/{namespaceName}/observabilityplanes/{observabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1104] |
| GET | `/api/v1/namespaces/{namespaceName}/observabilityplanes/{observabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1044] |
| PUT | `/api/v1/namespaces/{namespaceName}/observabilityplanes/{observabilityPlaneName}` | [D: openapi/openchoreo-api.yaml:1068] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowplanes` | [D: openapi/openchoreo-api.yaml:839] |
| POST | `/api/v1/namespaces/{namespaceName}/workflowplanes` | [D: openapi/openchoreo-api.yaml:865] |
| DELETE | `/api/v1/namespaces/{namespaceName}/workflowplanes/{workflowPlaneName}` | [D: openapi/openchoreo-api.yaml:959] |
| GET | `/api/v1/namespaces/{namespaceName}/workflowplanes/{workflowPlaneName}` | [D: openapi/openchoreo-api.yaml:899] |
| PUT | `/api/v1/namespaces/{namespaceName}/workflowplanes/{workflowPlaneName}` | [D: openapi/openchoreo-api.yaml:923] |
| GET | `/api/v1/namespaces/{namespace}/environments/{environment}/wirelogs` | [D: internal/openchoreo-api/api/handlers/exec_wirelogs_audit.go:20] |
| POST | `/api/v1/remote-connect:authorize` | [D: internal/remoteconnect/authorize.go:68] |
| POST | `/api/v1/remote-connect:heartbeat` | [D: internal/remoteconnect/authorize.go:85] |
| POST | `/api/v1/remote-connect:resolve` | [D: cmd/openchoreo-api/main.go:279] |
| GET | `/namespaces/ns/projects/p` | [D: agents/sre-agent/tests/test_clients.py:93] |

## Data model
Persisted state is Kubernetes custom resources; there is no relational store [D: PROJECT:5].

| Kind | Spec fields | Defined at |
| --- | --- | --- |
| DataPlane | `planeID`, `clusterAgent`, `gateway`, `secretStoreRef`, `observabilityPlaneRef` | [D: api/v1alpha1/dataplane_types.go:172] |
| ClusterDataPlane | `planeID`, `clusterAgent`, `gateway`, `secretStoreRef`, `observabilityPlaneRef` | [D: api/v1alpha1/clusterdataplane_types.go:75] |
| WorkflowPlane | `planeID`, `clusterAgent`, `secretStoreRef`, `observabilityPlaneRef` | [D: api/v1alpha1/workflowplane_types.go:66] |
| ClusterWorkflowPlane | `planeID`, `clusterAgent`, `secretStoreRef`, `observabilityPlaneRef` | [D: api/v1alpha1/clusterworkflowplane_types.go:71] |
| ObservabilityPlane | `planeID`, `clusterAgent`, `observerURL`, `rcaAgentURL`, `finOpsAgentURL` | [D: api/v1alpha1/observabilityplane_types.go:69] |
| ClusterObservabilityPlane | `planeID`, `clusterAgent`, `observerURL`, `rcaAgentURL`, `finOpsAgentURL` | [D: api/v1alpha1/clusterobservabilityplane_types.go:66] |
| Environment | `dataPlaneRef`, `isProduction`, `gateway` | [D: api/v1alpha1/environment_types.go:37] |
| DeploymentPipeline | `promotionPaths` | [D: api/v1alpha1/deploymentpipeline_types.go:59] |

Field lists are the top-level `json:` names on each kind's `Spec`. Nested shapes are in the type file at the citation, deliberately not copied here.

## Sequence
Reconcilers participating, in the order a change propagates:

1. `dataplane` — [D: internal/controller/dataplane/controller.go:1]
2. `clusterdataplane` — [D: internal/controller/clusterdataplane/controller.go:1]
3. `environment` — [D: internal/controller/environment/controller.go:1]
4. `deploymentpipeline` — [D: internal/controller/deploymentpipeline/controller.go:1]
5. `observabilityplane` — [D: internal/controller/observabilityplane/controller.go:1]
6. `clusterobservabilityplane` — [D: internal/controller/clusterobservabilityplane/controller.go:1]

Supporting code paths:

- Remote-connect wire contract and transport model — [D: internal/remoteconnect/doc.go:5]
- CP-signed capability scoping a session — [D: internal/remoteconnect/capability.go:1]
- Per-stream authorize callback path — [D: internal/remoteconnect/authorize.go:68]
- Gateway connection manager — [D: internal/cluster-gateway/connection_manager.go:1]
- Gateway mesh: redial backoff rule — [D: internal/cluster-gateway/fabric/mesh.go:564]
- Registry lookup must never block on the network — [D: internal/cluster-gateway/fabric/fabric.go:117]
- Rebalance slack, and why a fleet that cannot divide evenly would shed forever — [D: internal/cluster-gateway/server.go:1520]
- Agent mTLS identity parsing — [D: internal/cluster-gateway/agent_auth.go:1]
- Promotion path between environments — [D: api/v1alpha1/deploymentpipeline_types.go:27]

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
Satisfies the stories in `PRDs/prd_v1.2.0_F-005-multi-plane-topology-and-connectivity.md`; exercised by `tests/test_v1.2.0_F-005.md`.

## Open questions

OPEN: the gateway fabric implements peer discovery, gap repair, rebalancing and backoff — a substantial distributed system. Which failure modes were observed in production and drove it, and which were anticipated? The tests state the invariants, never the incidents.

OPEN: what is the supported upper bound on connected planes and agents per gateway replica? `rebalanceSlack` implies a fairness target that is never stated as a number.

OPEN: is single-cluster (all planes in one k3d cluster) a supported production topology or a development convenience only?

