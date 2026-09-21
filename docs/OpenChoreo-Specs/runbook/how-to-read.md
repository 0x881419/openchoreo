---
title: How to Read the Runbooks
status: draft
owner: TBD
updated: 2026-09-19
---

# How to Read the Runbooks

> Explain runbook types and when an engineer or agent should reach for one.

## Naming

<!-- `runbook_<TYPE>_RB-nnn-<slug>.md`, TYPE ∈ DEV | TEST | TROUBLESHOOT | DEPLOY. -->

In this hub every claim carries its epistemic class: `[D: path:line]` is derived from that location, `I: … — basis: …` is an inference with its leap written down, and `OPEN:` is a question the code cannot answer. An `OPEN:` line is not an omission — in a hub reconstructed from code it is the most valuable line on the page.

## Contract

Every runbook states preconditions, numbered steps, a verification step and a rollback. A step whose command was not executed when the runbook was written is marked `I:`, and the verification section says so explicitly — a runbook that quietly implies it was tested is worse than one that admits it was not.

## When to write a new one

Any procedure done twice by hand. The reconstruction produced one (`RB-001`, local setup); troubleshooting and deploy runbooks are the obvious gaps, and both need someone who has actually performed the procedure.
