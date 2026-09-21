---
title: Runbook DEV RB-001 — Local setup
id: RB-001
type: DEV
status: draft
kind: runbook
features: [F-001, F-002, F-003, F-004, F-005, F-006, F-007, F-008, F-009, F-010]
owner: TBD
updated: 2026-09-19
---

# Runbook DEV RB-001 — Local setup

> Derived from the repository's own make targets and contributor guide. **No command below was
> executed during this reconstruction** except where a step says otherwise; each is marked `I:`
> for that reason, and the verification step names what would prove it.

## Prerequisites

Go 1.26+, Docker 23+, Make 3.81+, Kubernetes 1.30+, kubectl 1.30+, Helm 3.16+, uv 0.8+
[D: docs/contributors/contribute.md:4-10]. The repository ships a checker:

```sh
./check-tools.sh
```

[D: docs/contributors/contribute.md:16]

## Bring up a local cluster

I: `make k3d` brings up the whole local environment in one step — basis: the contributor guide states that it creates the cluster, builds all components, loads images and installs OpenChoreo, in 5–15 minutes [D: docs/contributors/contribute.md:44].

```sh
make k3d
```

Step by step, if the single target fails partway
[D: docs/contributors/contribute.md:50-84]:

```sh
make k3d.up          # create the cluster
make k3d.build       # build all component images
make k3d.load        # import them into k3d
make k3d.install     # install control, data, workflow, observability planes
make k3d.configure   # register the DataPlane resource
make k3d.status      # verify
```

## Develop against it

Run the controller manager locally instead of in-cluster
[D: docs/contributors/contribute.md:98-107]:

```sh
kubectl --context k3d-openchoreo-dev -n openchoreo-control-plane \
  scale deployment openchoreo-controller-manager --replicas=0
make go.run.manager ENABLE_WEBHOOKS=false
```

Rebuild one component and restart it in place [D: make/k3d.mk:168]:

```sh
make k3d.update.controller        # or openchoreo-api, observer, cluster-gateway, cluster-agent
make k3d.logs.openchoreo-api
```

## Local endpoints

| Surface | Address | Evidence |
| --- | --- | --- |
| Control plane UI/API | `http://openchoreo.localhost:8080` | [D: docs/contributors/contribute.md:129] |
| Data plane workloads (kgateway) | `http://localhost:19080` | [D: docs/contributors/contribute.md:130] |
| Argo Workflows | `http://localhost:10081` | [D: docs/contributors/contribute.md:131] |
| Observer API | `http://localhost:11080` | [D: docs/contributors/contribute.md:132] |

## Before opening a pull request

```sh
make lint            # golangci-lint + license headers + newlines
make code.gen-check  # generated code must be current
make test            # Go + Python
```

[D: make/lint.mk:78], [D: make/lint.mk:164], [D: make/lint.mk:166]

## Teardown

```sh
make k3d.down
```

[D: docs/contributors/contribute.md:124]

## Verification status

`make test` was run during this reconstruction and its result is recorded per feature in the
test plans. Every other command in this runbook is `I:` — derived from the makefiles and the
contributor guide, never executed here.

OPEN: how long does `make k3d` actually take on a current machine, and what is the most common
way it fails? The guide gives a range; the failure modes are tribal knowledge.

OPEN: is there a supported path to run against an existing cluster that is not k3d?
