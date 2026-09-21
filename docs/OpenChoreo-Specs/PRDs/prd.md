---
title: Master PRD — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Master PRD — OpenChoreo v1.2.0

> **Reconstructed from shipped code.** A PRD states intent, and intent is not in a repository.
> Almost every section below is therefore a question. That is the honest output, and the
> questions are the deliverable: they are the things this organisation knows and has never
> written down.

## Problem

The README states the problem in the project's own words: Kubernetes primitives are "too
low-level for most developers", so platform teams build a bespoke platform from scratch and
own the glue indefinitely [D: README.md:38-42].

OPEN: that is a market narrative written for a README. What problem did the *first* users
actually bring, and does the current shape still match it?

## Product summary

I: OpenChoreo is a complete platform rather than a toolkit — basis: 37 CRDs, 34 reconcilers, 214 API operations, a CLI, an MCP server and four Helm-packaged planes ship from one repository under one version [D: VERSION:1].

It ships the abstractions, the delivery pipeline, the connectivity fabric, authorization,
observability and the client surfaces as one system rather than as assembly instructions.

## Feature set as shipped

| ID | Feature | Evidence of existence |
| --- | --- | --- |
| F-001 | Component Delivery Pipeline | [D: internal/controller/releasebinding/controller.go:130] |
| F-002 | Platform Abstractions and Templating | [D: internal/template/engine.go:1] |
| F-003 | Project and Resource Delivery | [D: internal/controller/projectreleasebinding/controller_render.go:82] |
| F-004 | Authorization and Access Control | [D: internal/authz/casbin/pdp.go:251] |
| F-005 | Multi-Plane Topology and Connectivity | [D: internal/remoteconnect/doc.go:5] |
| F-006 | Build and Workflow Execution | [D: api/v1alpha1/workflowrun_types.go:151] |
| F-007 | Observability and Alerting | [D: api/v1alpha1/observabilityalertrule_types.go:216] |
| F-008 | Secrets Management | [D: api/v1alpha1/secretreference_types.go:134] |
| F-009 | Client Surfaces — occ CLI and MCP | [D: internal/occ/resources/client/openapi_client.go:16] |
| F-010 | AI Agents | [D: agents/portal-assistant/src/api/agent_routes.py:277] |

OPEN: this split is a reconstruction. It matches how the code is organised; whether it matches
how the team thinks about the product is unknown and worth confirming before anyone plans
against it.

## MVP

OPEN: not recoverable. The product is at 1.2.0 [D: VERSION:1] with 3869 commits since
2025-01-08; the repository does not record what the first shippable slice was.

## Non-functional requirements

Each row is `OPEN:` unless a number is literally configured somewhere.

| Concern | Status |
| --- | --- |
| Reconcile latency | OPEN: no target expressed anywhere |
| API latency / throughput | OPEN: no SLO in the repository |
| Availability | OPEN: not stated |
| Managed clusters per gateway replica | OPEN: `rebalanceSlack` implies a fairness target [D: internal/cluster-gateway/server.go:1520] but states no ceiling |
| Template render cost | Bounded by an explicit budget [D: internal/template/budget.go:1] — the mechanism is `D:`, the chosen ceiling is OPEN |
| E2E suite runtime | 20 minutes default [D: make/e2e.mk:28] |
| Log retention per container in diagnostics | 20000 lines [D: make/e2e.mk:43] |
| Max pod log bytes | 10 MB [D: internal/clients/gateway/client.go:22] |
| Supported Kubernetes | ≥1.30 [D: docs/contributors/contribute.md:8] |

The last four are real finds: they are the only quantified limits in the repository, and three
of them are test-harness settings rather than product guarantees.

## Metrics

OPEN: no success metric, funnel, adoption target or dashboard definition exists anywhere in
the repository. Nothing in the code can tell you whether this product is working.

## Scope boundaries

OPEN: not recoverable. The repository records what was built and retains no record of what was
declined.

## Dependencies and constraints

- Kubernetes ≥1.30, Helm ≥3.16, Go 1.26 [D: docs/contributors/contribute.md:4-10]
- Gateway API, cert-manager, External Secrets Operator, kgateway as prerequisites
  [D: make/e2e.mk:100]
- Argo Workflows and cloud native Buildpacks for the optional build plane [D: README.md:65]
- CNCF Sandbox governance [D: GOVERNANCE.md:1]

OPEN: which of these are replaceable and which are structural? The e2e setup installs all of
them unconditionally, which tells you they are required for the tests, not whether they are
required for the product.
