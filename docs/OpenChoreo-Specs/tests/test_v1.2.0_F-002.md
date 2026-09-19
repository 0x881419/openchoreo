---
title: Test Plan v1.2.0 F-002 — Platform Abstractions and Templating
id: F-002
status: draft
owner: TBD
updated: 2026-09-19
---

# Test Plan v1.2.0 F-002 — Platform Abstractions and Templating
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **This document is as-built.** It records the suite that exists, not a suite that was planned. Coverage holes are the point of it.

## Traceability matrix

| Story | Covering tests | Level | Status |
| --- | --- | --- | --- |
| F-002-US1 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |
| F-002-US2 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |
| F-002-US3 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |

## Test cases

Test packages backing this feature, with the result of the run performed here:

| Package | Result here |
| --- | --- |
| `internal/controller/clustercomponenttype` | FAILED — see note |
| `internal/controller/clusterprojecttype` | FAILED — see note |
| `internal/controller/clusterresourcetype` | FAILED — see note |
| `internal/controller/clustertrait` | FAILED — see note |
| `internal/controller/componenttype` | FAILED — see note |
| `internal/controller/projecttype` | FAILED — see note |
| `internal/controller/resourcetype` | FAILED — see note |
| `internal/controller/trait` | FAILED — see note |

OPEN: package-level results do not tell you which story a passing package actually covers. Mapping individual test cases to stories needs a human who knows the intent.

## Edge and negative cases

The repository states a number of negative rules in its own words. These are quoted, with the citation kept, because they are the clearest statement of intent the code contains:

- CEL template engine [D: internal/template/engine.go:1]
- Render cost budget [D: internal/template/budget.go:1]
- Custom CEL functions [D: internal/template/custom_functions.go:1]
- OpenAPI v3 parameter schema handling [D: internal/schema/openapiv3.go:1]

## Out of scope

- End-to-end behaviour against a live cluster — covered by `test/e2e/` and run by `make e2e` [D: test/e2e/README.md:1], not by this plan.

OPEN: is there an intended split between what must be proven by envtest and what must be proven end to end? The tiers in `test/e2e/README.md` imply one but never state the rule.
