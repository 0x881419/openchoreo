---
title: How to deploy — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# How to deploy — OpenChoreo

Full strategy: `docs/OpenChoreo-Specs/deployment/deployment_strategy.md`.

Four Helm charts, one per plane [D: install/helm/openchoreo-control-plane/Chart.yaml:1].
Charts are generated, not hand-edited — `make helm-generate` [D: make/helm.mk:1].

Prerequisites in a target cluster: Gateway API, cert-manager, External Secrets Operator,
kgateway [D: make/e2e.mk:100].

```sh
make k3d.install                  # all planes locally  [D: make/k3d.mk:105]
make k3d.install.control-plane    # one plane
make docker.build-multiarch       # release images      [D: make/docker.mk:1]
```

Release is orchestrated by workflows [D: .github/workflows/release-orchestrator.yml:1] against
a single version file [D: VERSION:1], with a documented process
[D: docs/contributors/release.md:1].

OPEN: no rollback procedure is documented, and the CRD-plus-controller layer carries state that
a Helm rollback does not address. What is the supported way back from a bad release?

OPEN: what resources does a production control plane need? The chart values are tuned for k3d.
