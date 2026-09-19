---
title: Research Notes — OpenChoreo
status: draft
owner: TBD
updated: 2026-09-19
---

# Research Notes — OpenChoreo

This hub was produced by reversing the codebase, not by forward research. The raw survey
artefacts are not committed; they are reproducible:

```sh
python3 .claude/skills/product-reverse-docs/scripts/reverse.py survey --root . --out <dir>
python3 .claude/skills/product-reverse-docs/scripts/reverse.py verify --root . \
    --evidence <dir>/evidence.json --docs docs
```

Two extraction gaps had to be closed by hand before the survey was usable here, and anyone
re-running it will hit the same two:

1. The HTTP route table is not in the Go source. `openchoreo-api` mounts an oapi-codegen
   dispatcher at `/` [D: cmd/openchoreo-api/main.go:377], so the real surface is
   `openapi/openchoreo-api.yaml` — 214 operations — plus the observer specs and five routes
   registered outside the generated mux [D: internal/remoteconnect/authorize.go:68].
2. There is no DDL, migration or ORM model. The data model is 37 Kubernetes custom resource
   kinds under `api/v1alpha1/` [D: api/v1alpha1/component_types.go:19].

OPEN: is there prior design research — RFCs, proposals, competitive analysis — held outside
this repository? `docs/proposals/` holds one numbered proposal
[D: docs/proposals/0142-standardize-build-conditions.md:1], which suggests a process whose
other artefacts live elsewhere.
