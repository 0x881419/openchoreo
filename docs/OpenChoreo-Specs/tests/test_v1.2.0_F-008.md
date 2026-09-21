---
title: Test Plan v1.2.0 F-008 — Secrets Management
id: F-008
status: draft
owner: TBD
updated: 2026-09-19
---

# Test Plan v1.2.0 F-008 — Secrets Management
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **This document is as-built.** It records the suite that exists, not a suite that was planned. Coverage holes are the point of it.

## Traceability matrix

| Story | Covering tests | Level | Status |
| --- | --- | --- | --- |
| F-008-US1 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |
| F-008-US2 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |
| F-008-US3 | see cases below | unit + envtest | done — go test ./api/v1alpha1/... passed here |

## Test cases

Test packages backing this feature, with the result of the run performed here:

| Package | Result here |
| --- | --- |
| `internal/controller/secretreference` | FAILED — see note |
| `internal/occ/cmd/secret` | passed |
| `internal/occ/cmd/secretreference` | passed |
| `internal/openchoreo-api/services/gitsecret` | passed |
| `internal/openchoreo-api/services/secret` | passed |
| `internal/openchoreo-api/services/secretreference` | passed |

OPEN: package-level results do not tell you which story a passing package actually covers. Mapping individual test cases to stories needs a human who knows the intent.

## Edge and negative cases

The repository states a number of negative rules in its own words. These are quoted, with the citation kept, because they are the clearest statement of intent the code contains:

- Secret reference type and store binding [D: api/v1alpha1/secretreference_types.go:134]
- Value-from indirection [D: api/v1alpha1/dataplane_types.go:22]
- Git secret service [D: internal/openchoreo-api/services/gitsecret]
- Secret service [D: internal/openchoreo-api/services/secret]

## Out of scope

- End-to-end behaviour against a live cluster — covered by `test/e2e/` and run by `make e2e` [D: test/e2e/README.md:1], not by this plan.

OPEN: is there an intended split between what must be proven by envtest and what must be proven end to end? The tiers in `test/e2e/README.md` imply one but never state the rule.
