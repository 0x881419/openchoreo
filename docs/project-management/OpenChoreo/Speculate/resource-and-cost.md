---
title: Resources and Cost — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Resources and Cost — OpenChoreo

> Reconstructed from shipped code. This document records intent, and intent is not in a
> repository — the questions below are the output, and answering them is human work.

## What is knowable

Nothing about people or budget is in this repository. The only cost-shaped artefacts are
product features, not project costs: the FinOps agent analyses workload cost
[D: agents/finops-agent/src/api/agent_routes.py:45], and the template engine enforces a render
cost budget [D: internal/template/budget.go:1].

The e2e suite's own resource shape is visible — a four-cluster multi-cluster lifecycle with
settle gates between CPU-heavy installs [D: make/e2e.mk:30-36] — which says something about CI
cost and nothing about project cost.

## Open questions

OPEN: how many people work on this, and in what roles? 35 contributors appear in the surveyed
history, which counts commits, not commitment.

OPEN: what does CI cost to run? The e2e gate provisions k3d clusters per run
[D: .github/workflows/e2e-gate.yml:1].

OPEN: is there a funding or sustainability model beyond WSO2's sponsorship?
