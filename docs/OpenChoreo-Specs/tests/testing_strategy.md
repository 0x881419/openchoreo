---
title: Testing Strategy — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Testing Strategy — OpenChoreo

> **As-built.** This describes the suite that exists, derived from its configuration and
> layout. It is not a plan anyone agreed to.

## Levels

| Level | Technology | Where | Evidence |
| --- | --- | --- | --- |
| Unit | testify + mockery mocks | beside the code, `mocks/` subdirectories | [D: .mockery.yaml:1] |
| Controller integration | Ginkgo + Gomega + envtest (k8s 1.36.0) | `suite_test.go` per controller package | [D: make/golang.mk:169] |
| End-to-end | Ginkgo against a real k3d cluster | `test/e2e/suites/` | [D: test/e2e/README.md:1] |
| UI | Playwright | `test/ui/` | [D: test/ui/playwright.config.ts:1] |
| Python | pytest per agent | `agents/*/tests/` | [D: make/python.mk:15] |

905 test files containing 10369 test cases were surveyed [D: go.mod:1].

## Commands

```sh
make test        # Go + Python
make go.test     # Go only; provisions envtest assets, excludes /e2e
make python.test # the three agents
make e2e         # full e2e lifecycle: setup -> test -> down
```

[D: make/lint.mk:166], [D: make/golang.mk:172], [D: make/python.mk:14], [D: make/e2e.mk:713]

`make go.test` sets `KUBEBUILDER_ASSETS` from a downloaded envtest binary set
[D: make/golang.mk:173]. A bare `go test ./...` will fail every controller suite for want of
those assets — which is exactly what happened during this reconstruction, and why the affected
rows read `wip — unverified` rather than `done`.

## E2E tiers

Suites carry Ginkgo labels `tier1`, `tier2`, `tier3` on their top-level `Describe`, so CI can
shard them and a developer can run a subset [D: make/e2e.mk:44].

```sh
make e2e.test E2E_LABEL_FILTER='tier1'
make e2e.test E2E_LABEL_FILTER='tier1 || tier2'
```

Tier 3 requires the workflow and observability planes:
`E2E_WITH_BUILD=true E2E_WITH_OBSERVABILITY=true` [D: make/e2e.mk:10-11].

## Gates in CI

18 workflows exist [D: .github/workflows/build-and-test.yml:1]. The ones that gate a change:
build-and-test, e2e-gate, lint-pr, codeql, trivy-image-scan
[D: .github/workflows/e2e-gate.yml:1], [D: .github/workflows/lint-pr.yml:1].

## Open questions

OPEN: no coverage threshold is configured anywhere, though Codecov is wired into the README
badge [D: README.md:33]. Is there a target?

OPEN: what is the intended split between envtest and e2e — which behaviours *must* be proven
against a real cluster? The tier labels imply a rule that is never stated.

OPEN: the UI suite is off by default (`E2E_WITH_UI=false`) [D: make/e2e.mk:14] and depends on
an image built in a separate repository [D: make/e2e.mk:17-21]. How is that cross-repo
dependency kept in step?
