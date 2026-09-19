---
title: Release Plan — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Release Plan — OpenChoreo

> Reconstructed from shipped code. This document records intent, and intent is not in a
> repository — the questions below are the output, and answering them is human work.

## What is knowable

Version is a single file, currently 1.2.0 [D: VERSION:1]. Releases are orchestrated by
workflows [D: .github/workflows/release-orchestrator.yml:1], [D: .github/workflows/release.yml:1]
and documented [D: docs/contributors/release.md:1]. Next-version preparation is itself a
workflow [D: .github/workflows/prepare-next-version.yml:1].

Backports are label-driven: `backport/release-vX.Y` on an issue triggers the process
[D: docs/contributors/development-process.md:70].

Development runs in one-week sprints with Monday retrospective and planning
[D: docs/contributors/development-process.md:5].

## Open questions

OPEN: what is the release cadence — per sprint, per quarter, on demand? The machinery is
documented and the rhythm is not.

OPEN: what is the support window for a released minor version, and how many are supported at
once? The backport mechanism implies more than one.

OPEN: `v1alpha1` is the only API version [D: PROJECT:11]. What triggers a move to beta, and
what compatibility promise would come with it?
