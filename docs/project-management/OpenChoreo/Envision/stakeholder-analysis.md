---
title: Stakeholder Analysis — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Stakeholder Analysis — OpenChoreo

> Reconstructed from shipped code. This document records intent, and intent is not in a
> repository — the questions below are the output, and answering them is human work.

## What is knowable

| Group | Evidence |
| --- | --- |
| Maintainers | [D: MAINTAINERS.md:1] |
| Adopters | [D: ADOPTERS.md:1] |
| Contributors — 35 in the surveyed history | [D: GOVERNANCE.md:1] |
| CNCF, as Sandbox host | [D: README.md:16] |
| WSO2, as originator | [D: README.md:52] |

The code also implies four user roles, inferred from resource ownership and endpoint grouping
and recorded in `ddd/domain_DOM-001-component-delivery-pipeline.md`: developer, platform
engineer, SRE and AI agent.

## Open questions

OPEN: who decides scope — maintainers by consensus, a sponsoring company, or a technical
steering body? `GOVERNANCE.md` describes a structure; it does not say where product direction
is actually set.

OPEN: who are the adopters' *users*? The platform's end users are developers inside adopting
organisations, and nothing in this repository reaches them.

OPEN: what does WSO2's continued involvement mean for prioritisation?
