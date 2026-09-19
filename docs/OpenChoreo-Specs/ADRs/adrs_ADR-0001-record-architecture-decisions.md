---
title: ADR-0001 — Kubernetes CRDs as the platform API
id: ADR-0001
status: accepted (reconstructed from code, 2026-09-19) — rationale not recovered
kind: adr
features: [F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010]
owner: TBD
updated: 2026-09-19
---

# ADR-0001 — Kubernetes CRDs as the platform API

Status: accepted (reconstructed from code, 2026-09-19) — rationale not recovered

## Context

The platform's entire public model is expressed as Kubernetes custom resources in the group
`openchoreo.dev`, version `v1alpha1`, scaffolded with Kubebuilder layout `go.kubebuilder.io/v4`
[D: PROJECT:5-7]. 37 root kinds are defined [D: api/v1alpha1/component_types.go:19] and
reconciled by 34 controller packages [D: internal/controller/component/controller.go:3].

No relational store, migration directory or ORM model exists anywhere in the repository. The
REST API is a facade: its handlers call services that read and write those custom resources
through a Kubernetes client [D: cmd/openchoreo-api/main.go:189-195].

These are facts about the code. They are stated here without motive.

## Decision

Platform state is Kubernetes custom resources, reconciled by controllers, with the API server's
etcd as the system of record. Every other surface — the REST API
[D: cmd/openchoreo-api/main.go:377], the `occ` CLI
[D: internal/occ/resources/client/openapi_client.go:16] and the MCP server
[D: cmd/openchoreo-api/main.go:260] — is a client of that model, not an alternative to it.

## Alternatives considered

OPEN: not recoverable — the code retains no record of what was rejected. A platform of this
shape could have been built on a relational store with a conventional API, and the repository
does not say whether that was considered.

## Consequences

Visible in the code today:

- Every kind gets Kubernetes-native validation, RBAC and admission for free — CRD validation
  expressions carry real domain rules [D: api/v1alpha1/resourcetype_types.go:49].
- Code generation is load-bearing: deepcopy, CRD manifests, RBAC, OpenAPI, mocks and audit
  tables are all generated and gated in CI [D: make/lint.mk:161], [D: make/lint.mk:164].
- Platform-scoped abstractions must be defined twice, namespaced and cluster-scoped, because
  Kubernetes scope is fixed per kind [D: api/v1alpha1/clustercomponenttype_types.go:141].
- Cross-cluster reach needs bespoke machinery — the gateway/agent fabric exists because the
  API server model does not span clusters [D: internal/cluster-gateway/fabric/fabric.go:117].

OPEN: was the twice-defined scope pairing accepted as a cost of this decision, or is it
considered a defect to be removed later?
