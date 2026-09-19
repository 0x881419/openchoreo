---
title: Test Plan v1.2.0 F-001 — Component Delivery Pipeline
id: F-001
status: draft
owner: TBD
updated: 2026-09-19
---

# Test Plan v1.2.0 F-001 — Component Delivery Pipeline
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **This document is as-built.** It records the suite that exists, not a suite that was planned. Coverage holes are the point of it.

## Traceability matrix

| Story | Covering tests | Level | Status |
| --- | --- | --- | --- |
| F-001-US1 | see cases below | unit + envtest | wip — unverified — go test ./internal/controller/clustercomponenttype/... needs envtest assets; run make go.test, which provisions them |
| F-001-US2 | see cases below | unit + envtest | wip — unverified — go test ./internal/controller/clustercomponenttype/... needs envtest assets; run make go.test, which provisions them |
| F-001-US3 | see cases below | unit + envtest | wip — unverified — go test ./internal/controller/clustercomponenttype/... needs envtest assets; run make go.test, which provisions them |

## Test cases

Test packages backing this feature, with the result of the run performed here:

| Package | Result here |
| --- | --- |
| — | no Go test package maps to this feature's paths |

OPEN: package-level results do not tell you which story a passing package actually covers. Mapping individual test cases to stories needs a human who knows the intent.

## Edge and negative cases

The repository states a number of negative rules in its own words. These are quoted, with the citation kept, because they are the clearest statement of intent the code contains:

- Rendering pipeline entry point [D: internal/pipeline/component/pipeline.go:96]
- Pipeline responsibilities, stated by its own package comment [D: internal/pipeline/component/pipeline.go:5]
- ReleaseBinding emits a data-plane RenderedRelease [D: internal/controller/releasebinding/controller.go:627]
- …and a second one for the observability plane [D: internal/controller/releasebinding/controller.go:825]

## Out of scope

- End-to-end behaviour against a live cluster — covered by `test/e2e/` and run by `make e2e` [D: test/e2e/README.md:1], not by this plan.

OPEN: is there an intended split between what must be proven by envtest and what must be proven end to end? The tiers in `test/e2e/README.md` imply one but never state the rule.
