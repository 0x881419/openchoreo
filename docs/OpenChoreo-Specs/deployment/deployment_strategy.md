---
title: Deployment Strategy — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Deployment Strategy — OpenChoreo

> Derived from the Helm charts, Dockerfiles, make targets and release workflows. No deployment
> was performed during this reconstruction.

## Artefacts

Nine binaries build from one module [D: make/golang.mk:14-23]: `manager`, `occ`,
`openchoreo-api`, `observer`, `event-forwarder`, `cluster-gateway`, `cluster-agent`,
`remote-agent`, `remote-agent-router`.

Each ships as a container [D: Dockerfile:1], [D: cmd/observer/Dockerfile:1],
[D: cmd/cluster-gateway/Dockerfile:1]. Binaries are cross-compiled for six platforms
[D: make/golang.mk:11] and packaged as archives [D: make/golang.mk:120].

## Units of deployment

Four Helm charts, one per plane [D: install/helm/openchoreo-control-plane/Chart.yaml:1]:

| Chart | Plane |
| --- | --- |
| `openchoreo-control-plane` | Control |
| `openchoreo-data-plane` | Data |
| `openchoreo-workflow-plane` | Workflow (the README's "CI Plane") |
| `openchoreo-observability-plane` | Observability |

Charts are generated, not hand-written: `make helm-generate` builds them and their schemas
[D: make/helm.mk:1], and `make code.gen` includes that step [D: make/lint.mk:161].

## Prerequisites in a target cluster

Gateway API, cert-manager, External Secrets Operator and kgateway
[D: make/e2e.mk:100]. Cilium/Hubble is present for flow observability
[D: internal/cluster-agent/hubble.go:117].

## Topologies

- **Single cluster** — all four planes in one cluster, used by the k3d development environment
  and the default e2e run [D: docs/contributors/contribute.md:74].
- **Multi cluster** — four separate clusters, exercised by the multi-cluster e2e lifecycle
  [D: make/e2e.mk:100]. Planes reach each other through the gateway/agent fabric
  [D: internal/cluster-gateway/fabric/fabric.go:117].

OPEN: single-cluster is used as a development convenience throughout the repository. Is it a
*supported* production topology, or only a test harness?

## Release

Version comes from a single file [D: VERSION:1]. Release is orchestrated by workflows
[D: .github/workflows/release-orchestrator.yml:1], [D: .github/workflows/release.yml:1], with
a documented process [D: docs/contributors/release.md:1] and backports driven by a
`backport/release-vX.Y` label [D: docs/contributors/development-process.md:70].

Images can be retagged in the registry without a rebuild
[D: make/docker.mk:1] — `make docker.retag-registry SOURCE_TAG=… NEW_TAG=…`.

## Open questions

OPEN: no rollback procedure is documented. Helm rollback is implied by using Helm, but the
CRD-and-controller layer has its own state — what is the supported way back from a bad release?

OPEN: how are CRD schema changes handled across an upgrade? `v1alpha1` is the only version, so
no conversion webhook exists yet [D: PROJECT:11].

OPEN: what are the resource requirements for a production control plane? The chart values are
the only numbers in the repository and they are tuned for k3d.
