---
title: Tasks v1.2.0 F-008 — Secrets Management
id: F-008
status: draft
owner: TBD
updated: 2026-09-21
---

# Tasks v1.2.0 F-008 — Secrets Management
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **As-built inventory, not a plan.** Each row points at work that already shipped; the `done-when` column states the check that would prove it, and the status column is what that check actually returned here.

## Task list

| Task | Description | Artifact | Done-when | Status |
| --- | --- | --- | --- | --- |
| F-008-T1 | Define the custom resources | [D: api/v1alpha1/secretreference_types.go:134] | `make manifests` regenerates `config/crd/bases/` with no diff | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-008-T2 | Implement the reconcilers | [D: internal/controller/secretreference] | the controller's envtest suite passes under `make go.test` | wip — unverified — go test ./internal/controller/secretreference/... needs envtest assets; run make go.test, which provisions them |
| F-008-T3 | Declare and generate the API surface | [D: openapi/openchoreo-api.yaml:191] | `make openapi-codegen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-008-T4 | Register the operations for audit | [D: internal/openchoreo-api/audit/definitions.gen.go:1] | `make audit-gen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-008-T5 | Implement the supporting code paths | [D: api/v1alpha1/secretreference_types.go:134] | the package's unit tests pass | done — go test ./api/v1alpha1/... passed here |
| F-008-T6 | Expose the feature through `occ` | [D: internal/occ/cmd/secret] | the CLI e2e suite passes under `make e2e E2E_LABEL_FILTER='tier2'` | wip — unverified — the e2e suite needs a live cluster and was not run here; run make e2e |

## Execution order

I: the order above is the order a contributor adding a comparable feature would follow. Types first — every other layer imports them; then the reconcilers; then the spec-generated API; then the client surfaces [D: docs/contributors/adding-new-crd.md:1].

OPEN: that ordering is reconstructed from the contributor guide and the dependency direction, not from how this feature was actually built. The real sequence is in the git history of these paths, which ranks but does not prove.

## Definition of done

Applied to every row above — these are the checks CI enforces [D: make/lint.mk:78], [D: make/lint.mk:164], [D: make/lint.mk:166]:

- [ ] `make lint` passes
- [ ] `make code.gen-check` leaves the tree clean
- [ ] `make test` passes
- [ ] the PR title is a Conventional Commit and every commit is DCO signed off [D: docs/contributors/github_workflow.md:190]
