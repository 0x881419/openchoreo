---
title: System Architecture — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# System Architecture — OpenChoreo

> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived,
> `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer.

## Context

OpenChoreo is a control plane that translates high-level developer and platform intent,
expressed as `openchoreo.dev/v1alpha1` custom resources, into Kubernetes objects applied to
one or more managed clusters [D: PROJECT:5]. 37 root custom resource kinds are defined
[D: api/v1alpha1/component_types.go:19], reconciled by 34 controller packages
[D: internal/controller/component/controller.go:3], and exposed through 214 HTTP operations
declared in a single OpenAPI document [D: openapi/openchoreo-api.yaml:191].

## Components

| Component | Binary | Responsibility | Owns | Evidence |
| --- | --- | --- | --- | --- |
| Controller manager | `manager` | Runs all reconcilers and admission webhooks | every CRD's lifecycle | [D: cmd/main.go:280] |
| Control-plane API | `openchoreo-api` | Serves the REST contract, the MCP endpoint and remote-connect | no state of its own | [D: cmd/openchoreo-api/main.go:377] |
| Observer | `observer` | Queries logs, metrics and cost from the observability plane | its own store | [D: cmd/observer/main.go:322] |
| Cluster gateway | `cluster-gateway` | Accepts agent connections, multiplexes API/exec/log traffic to managed clusters | connection registry | [D: internal/cluster-gateway/connection_manager.go:1] |
| Cluster agent | `cluster-agent` | Dials out from a managed cluster; relays Hubble flows | — | [D: internal/cluster-agent/agent.go:1] |
| Remote agent / router | `remote-agent`, `remote-agent-router` | Terminates `occ remote` tunnels inside a project+env namespace | — | [D: internal/remoteconnect/doc.go:5] |
| Event forwarder | `event-forwarder` | Forwards cluster events toward the observability plane | — | [D: internal/eventforwarder] |
| CLI | `occ` | Operates every resource through the generated API client | local config | [D: internal/occ/resources/client/openapi_client.go:16] |
| Agents | 3 Python services | FinOps analysis, portal assistance, SRE root-cause analysis | their own report stores | [D: agents/finops-agent/src/main.py:103] |

## Planes

The README describes five planes: Experience, Control, Data, Observability and an optional
CI plane [D: README.md:59-67]. Four are packaged as Helm charts
[D: install/helm/openchoreo-control-plane/Chart.yaml:1].

**Terminology divergence, worth resolving:** the README calls the build plane the *CI Plane*
[D: README.md:65]. Every artefact in the repository calls it the *workflow plane* — the chart
is `openchoreo-workflow-plane`, the kind is `WorkflowPlane`
[D: api/v1alpha1/workflowplane_types.go:66], and the make target is `k3d.install.workflow-plane`
[D: make/k3d.mk:126]. A reader moving between the README and the code has to translate.

OPEN: which name is the intended product term? One of the two should change.

## The central flow

Developer intent reduces to applied cluster state in four stages, each a custom resource with
its own reconciler:

```
Component ──▶ ComponentRelease ──▶ ReleaseBinding ──▶ RenderedRelease ──▶ data plane
 (mutable)     (immutable snapshot)  (× Environment)    (concrete objects)
```

[D: docs/crds/renderedrelease.md:44-48]

Rendering is not performed by the controllers. `internal/pipeline/component` combines the
ComponentType, Traits, Workload and ReleaseBinding into resolved manifests by building CEL
evaluation contexts, rendering base resources, applying trait patches and post-processing
[D: internal/pipeline/component/pipeline.go:5], entered at
[D: internal/pipeline/component/pipeline.go:96].

**Undocumented elsewhere:** the same `RenderedRelease` kind is the convergence point for three
pipelines, not one. `ReleaseBinding` [D: internal/controller/releasebinding/controller.go:627],
`ProjectReleaseBinding` [D: internal/controller/projectreleasebinding/controller_render.go:82]
and `ResourceReleaseBinding` [D: internal/controller/resourcereleasebinding/controller.go:264]
each create one. `ReleaseBinding` creates two — one for the data plane and one for the
observability plane [D: internal/controller/releasebinding/controller.go:825]. The existing
design note covers only the component path
[D: docs/crds/renderedrelease.md:1].

## Trust boundaries

- I: the control plane never initiates a connection into a managed cluster — basis: the
  cluster agent dials out and the gateway multiplexes work back over that connection, and the
  remote-connect package states that for `occ remote` "the byte path does not traverse the
  control plane" while each stream still calls back for authorization
  [D: internal/remoteconnect/doc.go:15].
- I: authorization is a single chokepoint rather than a per-handler concern — basis: a Casbin
  PDP serialises one request context for all entitlements
  [D: internal/authz/casbin/pdp.go:251], and role bindings are validated at admission
  [D: internal/webhook/authzrolebinding/suite_test.go:54].
- Two routes deliberately sit outside the OpenAPI mux and the standard middleware order,
  because they reach the data plane directly — a live shell and a live traffic stream
  [D: cmd/openchoreo-api/main.go:338].

OPEN: why is the boundary drawn at agent-dials-out rather than control-plane-dials-in?
The consequence is visible throughout the gateway fabric; the reasoning is not recorded.

## Stores

I: there is no relational database in the control plane — basis: the survey found no DDL,
migration or ORM model anywhere in the repository, and every persisted kind is a custom
resource reconciled through the Kubernetes API [D: PROJECT:5]. State lives in the API server's
etcd. The observer and the Python agents carry their own stores
[D: internal/observer/store], [D: agents/finops-agent/src/api/report_routes.py:53].

OPEN: what is the observability plane's storage engine in a supported install, and who
operates it? OpenSearch appears in the local development setup
[D: docs/contributors/contribute.md:137] but the supported production choice is not stated.

## Cross-cutting mechanisms

| Mechanism | How it works | Evidence |
| --- | --- | --- |
| API generation | `openapi/*.yaml` → models, server interface, client | [D: make/golang.mk:184-206] |
| Audit | operation table generated per service from its spec; exemptions hand-maintained | [D: make/golang.mk:213-220] |
| Authorization | Casbin PDP fed by CRDs, CEL conditions | [D: internal/authz/casbin/pdp.go:251] |
| Templating | CEL with an explicit render cost budget | [D: internal/template/budget.go:1] |
| Configuration | koanf: defaults, file, env | [D: internal/auditconfig/audit.go:1] |
| RBAC | `+kubebuilder:rbac` markers → `config/rbac/` | [D: internal/controller/component/controller.go:6] |

## Open questions

OPEN: the multi-plane split is presented as architecture, but nothing states which planes may
be collapsed. Is all-planes-in-one-cluster a supported production topology, or only the k3d
development convenience it is used as [D: docs/contributors/contribute.md:74]?

OPEN: 37 kinds is a large surface for users to learn. Was the namespaced/cluster-scoped pairing
of eight abstractions an alternative to a scope field on one kind, and if so, what decided it?

OPEN: no quality-attribute targets exist anywhere — no latency budget for a reconcile, no
ceiling on managed clusters per gateway, no availability target. `rebalanceSlack`
[D: internal/cluster-gateway/server.go:1520] implies a fairness goal that is never stated as a
number.

OPEN: deployment topology beyond what the Helm charts express, and anything about team
ownership or operational process, is not recoverable from this repository.
