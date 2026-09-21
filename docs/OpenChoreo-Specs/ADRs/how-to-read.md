---
title: How to Read the ADRs
status: draft
owner: TBD
updated: 2026-09-19
---

# How to Read the ADRs

> Explain the ADR format and status lifecycle.

## Naming

<!-- `adrs_ADR-nnnn-<slug>.md`, immutable once Accepted. -->

In this hub every claim carries its epistemic class: `[D: path:line]` is derived from that location, `I: … — basis: …` is an inference with its leap written down, and `OPEN:` is a question the code cannot answer. An `OPEN:` line is not an omission — in a hub reconstructed from code it is the most valuable line on the page.

## Status lifecycle

Proposed → Accepted → Superseded. An accepted ADR is never edited in place; a later decision supersedes it. Records in this hub carry a fourth state in their status line — *accepted (reconstructed from code)* — which says the decision is in force and that its reasoning was not recovered.

## Format

Context, Decision, Alternatives, Consequences, Links. In a reconstructed record Context states facts about the code with citations and no motive, and Alternatives is `OPEN:` — the code retains no record of what was rejected.

## When an ADR is required

Any decision costly to reverse, or that constrains other work. Reversing a codebase also surfaces decisions already taken and never written down: where one is visible in code but its reasoning is not, write the record with an honest `OPEN:` for rationale rather than leaving it undocumented.
