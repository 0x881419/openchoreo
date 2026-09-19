---
title: Tasks v1.2.0 F-004 — Authorization and Access Control
id: F-004
status: draft
owner: TBD
updated: 2026-09-19
---

# Tasks v1.2.0 F-004 — Authorization and Access Control
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **As-built inventory, not a plan.** Each row points at work that already shipped; the `done-when` column states the check that would prove it, and the status column is what that check actually returned here.

## Task list

| Task | Description | Artifact | Done-when | Status |
| --- | --- | --- | --- | --- |
| F-004-T1 | Define the custom resources | [D: api/v1alpha1/authzrole_types.go:28] | `make manifests` regenerates `config/crd/bases/` with no diff | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-004-T2 | Declare and generate the API surface | [D: openapi/openchoreo-api.yaml:191] | `make openapi-codegen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-004-T3 | Register the operations for audit | [D: internal/openchoreo-api/audit/definitions.gen.go:1] | `make audit-gen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-004-T4 | Implement the supporting code paths | [D: internal/authz/casbin/k8s_watcher.go:29] | the package's unit tests pass | done — go test ./internal/authz/casbin/... passed here |
| F-004-T5 | Expose the feature through `occ` | [D: internal/occ/cmd/authzrole] | the CLI e2e suite passes under `make e2e E2E_LABEL_FILTER='tier2'` | wip — unverified — the e2e suite needs a live cluster and was not run here; run make e2e |

## Execution order

I: the order above is the order a contributor adding a comparable feature would follow. Types first — every other layer imports them; then the reconcilers; then the spec-generated API; then the client surfaces [D: docs/contributors/adding-new-crd.md:1].

OPEN: that ordering is reconstructed from the contributor guide and the dependency direction, not from how this feature was actually built. The real sequence is in the git history of these paths, which ranks but does not prove.

## Definition of done

Applied to every row above — these are the checks CI enforces [D: make/lint.mk:78], [D: make/lint.mk:164], [D: make/lint.mk:166]:

- [ ] `make lint` passes
- [ ] `make code.gen-check` leaves the tree clean
- [ ] `make test` passes
- [ ] the PR title is a Conventional Commit and every commit is DCO signed off [D: docs/contributors/github_workflow.md:190]
