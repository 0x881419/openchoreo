---
title: How to Read the Domain Docs
status: draft
owner: TBD
updated: 2026-09-19
---

# How to Read the Domain Docs

> Orient a human or agent in the business-domain folder.

## Naming

<!-- `domain_DOM-nnn-<slug>.md`, one bounded context or process per file. -->

In this hub every claim carries its epistemic class: `[D: path:line]` is derived from that location, `I: … — basis: …` is an inference with its leap written down, and `OPEN:` is a question the code cannot answer. An `OPEN:` line is not an omission — in a hub reconstructed from code it is the most valuable line on the page.

## Reading order

Ubiquitous language first — it is the vocabulary the rest of the hub uses. Then actors, then the rules. Each rule cites both the place the constraint was *stated* (usually a comment or a test name) and the code that enforces it; a rule with a statement and no enforcement is recorded as an OPEN question, not as a rule.

## What belongs here / what does not

Belongs: vocabulary, actors, invariants, and rules with their enforcement. Does not belong: API paths and schemas (those are the architecture documents), business justification (that is the PRD layer, and here it is almost entirely OPEN), and field lists.
