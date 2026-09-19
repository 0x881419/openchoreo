---
title: How to test — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# How to test — OpenChoreo

Full strategy: `docs/OpenChoreo-Specs/tests/testing_strategy.md`.

```sh
make test         # Go + Python                        [D: make/lint.mk:166]
make go.test      # Go only; provisions envtest assets [D: make/golang.mk:172]
make python.test  # the three agents (needs uv)        [D: make/python.mk:14]
make e2e          # setup -> test -> down              [D: make/e2e.mk:713]
make e2e.test E2E_LABEL_FILTER='tier1'                # [D: make/e2e.mk:44]
```

A single package:

```sh
go test ./internal/pipeline/component/... -run TestRender -v
```

**A bare `go test ./...` fails every controller suite.** Those suites need envtest binaries,
which `make go.test` provisions via `KUBEBUILDER_ASSETS` [D: make/golang.mk:173]. This was
confirmed during this reconstruction: 185 packages passed, and all 35 failures were
`unable to start control plane` in `internal/controller/*` and `internal/webhook/*`.

OPEN: is there a coverage target? Codecov is wired into the README badge
[D: README.md:33] but no threshold is configured.
