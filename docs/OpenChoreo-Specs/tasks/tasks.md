---
title: Task Index — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Task Index — OpenChoreo

> **As-built inventory.** Every row in the per-feature files points at work that already
> shipped. The status column records what the named check returned *here*, during the
> reconstruction — not what anyone believes about the code.

| Feature | Tasks file |
| --- | --- |
| F-001 | `tasks_v1.2.0_F-001.md` |
| F-002 | `tasks_v1.2.0_F-002.md` |
| F-003 | `tasks_v1.2.0_F-003.md` |
| F-004 | `tasks_v1.2.0_F-004.md` |
| F-005 | `tasks_v1.2.0_F-005.md` |
| F-006 | `tasks_v1.2.0_F-006.md` |
| F-007 | `tasks_v1.2.0_F-007.md` |
| F-008 | `tasks_v1.2.0_F-008.md` |
| F-009 | `tasks_v1.2.0_F-009.md` |
| F-010 | `tasks_v1.2.0_F-010.md` |

## How status was assigned

`done` is claimed only where the check named in that row's *done-when* column was run here and
passed. The Go suite was run (`go test ./...` excluding `/e2e`): 185 packages passed, 35
failed, and every failure was `unable to start control plane` — the envtest binaries are not
provisioned by a bare `go test`. Rows whose check is a make target or the e2e suite were not
run at all.

The result is 9 `done` and 41 `wip — unverified`, each `wip` naming the command that would
settle it.

OPEN: running `make go.test` and `make e2e` in a provisioned environment would move most of
these rows. Until then, treat `wip` as unknown rather than as incomplete.
