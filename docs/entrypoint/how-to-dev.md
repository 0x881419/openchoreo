---
title: How to develop — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# How to develop — OpenChoreo

Start here: `docs/OpenChoreo-Specs/architect/architect_common.md` for the standards, then
`docs/OpenChoreo-Specs/route/route_v1.2.0_<F-id>.md` for the feature you are touching.

```sh
./check-tools.sh     # verify tool versions            [D: docs/contributors/contribute.md:16]
make help            # every target, grouped           [D: make/common.mk:52]
make k3d             # cluster + build + load + install [D: docs/contributors/contribute.md:44]
make go.run.occ GO_RUN_ARGS="version"                 # [D: make/golang.mk:135]
make k3d.update.controller                            # [D: make/k3d.mk:168]
```

Before a pull request: `make lint`, `make code.gen-check`, `make test`
[D: make/lint.mk:78], [D: make/lint.mk:164], [D: make/lint.mk:166].

Adding a CRD follows a documented refactor: scaffold with Kubebuilder, then move the generated
controller to `internal/controller/<kind>/controller.go` and rename the struct to `Reconciler`
[D: docs/contributors/adding-new-crd.md:60-72]. Adding an MCP tool has its own guide
[D: docs/contributors/adding-new-mcp-tools.md:1].

OPEN: what is the expected first task for a new contributor, and who reviews it? The
contribution mechanics are documented; the on-ramp is not.
