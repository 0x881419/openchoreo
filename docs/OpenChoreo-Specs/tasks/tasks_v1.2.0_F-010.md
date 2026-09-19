---
title: Tasks v1.2.0 F-010 — AI Agents
id: F-010
status: draft
owner: TBD
updated: 2026-09-19
---

# Tasks v1.2.0 F-010 — AI Agents
> Reconstructed from the repository at commit `0c7e8a3e`. `[D: path:line]` is derived, `I:` is an inference with its basis stated, `OPEN:` is a question the code cannot answer. Nothing here was verified against a running system unless a status note says so.

> **As-built inventory, not a plan.** Each row points at work that already shipped; the `done-when` column states the check that would prove it, and the status column is what that check actually returned here.

## Task list

| Task | Description | Artifact | Done-when | Status |
| --- | --- | --- | --- | --- |
| F-010-T1 | Declare and generate the API surface | [D: openapi/openchoreo-api.yaml:191] | `make openapi-codegen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-010-T2 | Register the operations for audit | [D: internal/openchoreo-api/audit/definitions.gen.go:1] | `make audit-gen` leaves the tree clean | wip — unverified — this check is a make target that was not run here; run make code.gen-check |
| F-010-T3 | Implement the supporting code paths | [D: agents/finops-agent/src/api/agent_routes.py:45] | the package's unit tests pass | wip — unverified, run make go.test |

## Execution order

I: the order above is the order a contributor adding a comparable feature would follow. Types first — every other layer imports them; then the reconcilers; then the spec-generated API; then the client surfaces [D: docs/contributors/adding-new-crd.md:1].

OPEN: that ordering is reconstructed from the contributor guide and the dependency direction, not from how this feature was actually built. The real sequence is in the git history of these paths, which ranks but does not prove.

## Definition of done

Applied to every row above — these are the checks CI enforces [D: make/lint.mk:78], [D: make/lint.mk:164], [D: make/lint.mk:166]:

- [ ] `make lint` passes
- [ ] `make code.gen-check` leaves the tree clean
- [ ] `make test` passes
- [ ] the PR title is a Conventional Commit and every commit is DCO signed off [D: docs/contributors/github_workflow.md:190]
