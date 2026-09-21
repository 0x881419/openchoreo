---
title: Project Charter — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Project Charter — OpenChoreo

> **Almost entirely open by design.** A charter records why a project exists, who it is for and
> what success looks like. None of that is in a repository. The questions below are the most
> valuable output of this reconstruction: they are what the organisation knows and has never
> written down.

## What is factually knowable

| Fact | Evidence |
| --- | --- |
| Apache-2.0 licensed | [D: LICENSE:1] |
| CNCF Sandbox project | [D: README.md:16] |
| Originated at WSO2, rewritten rather than forked from WSO2 Choreo | [D: README.md:52] |
| Governance and maintainer model are documented | [D: GOVERNANCE.md:1], [D: MAINTAINERS.md:1] |
| One-week sprints, two GitHub project boards, weekly triage | [D: docs/contributors/development-process.md:3-12] |
| Version 1.2.0; 3869 commits from 2025-01-08; 35 contributors | [D: VERSION:1] |
| Security policy and disclosure process exist | [D: SECURITY.md:1] |
| AI-assisted contribution is permitted and must be disclosed | [D: docs/contributors/AI-POLICY.md:10-27] |

## Purpose

OPEN: the README states a market narrative [D: README.md:38]. A charter needs the sponsor's
stated purpose, which is a different document and is not in this repository.

## Success criteria

OPEN: none exist in the repository. No adoption target, no SLO, no funding or sustainability
goal, no definition of what "working" means for this project.

## Stakeholders

OPEN: `MAINTAINERS.md` and `ADOPTERS.md` name people and organisations
[D: MAINTAINERS.md:1], [D: ADOPTERS.md:1], but a stakeholder analysis — who decides, who is
affected, who must be consulted — is not derivable from either.

## Constraints

OPEN: CNCF Sandbox status implies governance constraints [D: GOVERNANCE.md:1]. Which of them
actively shape roadmap decisions is not recorded.

## Risks

OPEN: no risk register exists. The reconstruction surfaced technical risks — an undocumented
CRD surface, a terminology split between README and code — but a project-level risk view is a
human artefact.
