# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

OpenChoreo is a Kubernetes-native internal developer platform: a set of CRDs plus controllers
(Kubebuilder/controller-runtime), a REST+MCP control-plane API, a CLI (`occ`), an observability
service, and cross-cluster connectivity agents. Go 1.26; Python (uv) only for `agents/*`.

## Commands

Everything goes through `make` (targets live in `make/*.mk`; `make help` lists them all).

```sh
make test                  # go.test + python.test
make go.test               # Go unit + envtest suites (runs manifests/generate/fmt/vet first)
make lint / make lint-fix  # golangci-lint + license headers + trailing newlines
make code.gen              # regenerate CRDs, deepcopy, OpenAPI, helm, mocks, audit tables, samples
make code.gen-check        # CI gate: code.gen must leave the tree clean
make go.build              # all binaries into bin/dist/<os>/<arch>
make go.run.occ GO_RUN_ARGS="version"
make go.run.manager ENABLE_WEBHOOKS=false
```

Run one Go test package/case directly (envtest suites need `KUBEBUILDER_ASSETS`, which
`make go.test` sets; `make envtest` downloads the binaries):

```sh
go test ./internal/pipeline/component/... -run TestRender -v
go test ./internal/controller/releasebinding/... -v    # Ginkgo + envtest
```

`make code.gen` must be run after touching `api/v1alpha1/*_types.go`, `openapi/*.yaml`,
`.mockery.yaml`, mocked interfaces, or `samples/getting-started/*`. Never hand-edit
`*.gen.go`, `zz_generated.*`, `config/crd/bases/`, or generated helm chart output.

### Local cluster (k3d)

```sh
make k3d                   # up + build + load + install + configure (5-15 min)
make k3d.update.controller # rebuild one component, load into k3d, restart it
make k3d.status / make k3d.logs.<controller|openchoreo-api|observer>
make k3d.down
```

Components: `controller`, `openchoreo-api`, `observer`, `cluster-gateway`, `cluster-agent`,
`remote-agent`, `remote-agent-router`. Planes: `control-plane`, `data-plane`, `workflow-plane`,
`observability-plane`.

### E2E

Separate cluster (`openchoreo-e2e`) from the dev k3d cluster. See `test/e2e/README.md`.

```sh
make e2e                                  # setup → test → down
make e2e.test E2E_LABEL_FILTER='tier1'    # Ginkgo label expr; suites are tier1/tier2/tier3
make e2e.diagnostics                      # dump logs/events when something breaks
```

Tier 3 needs `E2E_WITH_BUILD=true E2E_WITH_OBSERVABILITY=true`.

## Architecture

### Delivery pipeline (the core of the control plane)

Developer intent flows through a chain of CRDs, each with its own reconciler under
`internal/controller/<kind>/`:

```
Component + ComponentType + Traits + Workload
  → ComponentRelease   (immutable snapshot of type+traits+workload)
  → ReleaseBinding     (snapshot × Environment, with env overrides)
  → RenderedRelease    (concrete K8s manifests)
  → applied to a data-plane cluster
```

The rendering itself is *not* in the controllers — it lives in `internal/pipeline/component`
(and `internal/pipeline/project`, `.../resource`, `.../workflow`). That pipeline builds CEL
evaluation contexts, renders ComponentType base resources, applies trait creates/patches, then
post-processes (validation, labels, annotations). The CEL/templating engine and its cost budget
are in `internal/template`; docs in `docs/templating/`. `internal/schema` handles the OpenAPI v3
parameter schemas that ComponentTypes and Traits declare.

Platform-scoped kinds come in namespaced and `Cluster*` variants (ComponentType/ClusterComponentType,
Trait/ClusterTrait, …) — changes usually need both, plus the matching service and `occ` command.

### Services and binaries (`cmd/*`)

- **manager** (`cmd/main.go`) — all controllers + webhooks (`internal/webhook`).
- **openchoreo-api** — control-plane REST API, OpenAPI-first. `openapi/openchoreo-api.yaml` is the
  source of truth → `internal/openchoreo-api/api/gen/{models,server,client}.gen.go`. Layering:
  `api/handlers/` (generated strict-handler impls) → `services/<domain>/` (business logic,
  mockery-mocked) → k8s clients. Also serves `/mcp` (`pkg/mcp` + `internal/openchoreo-api/mcphandlers`;
  see `docs/contributors/adding-new-mcp-tools.md`) and the remote-connect endpoints.
- **observer** — logs/metrics/FinOps query API (`internal/observer`), same OpenAPI-gen layering.
- **occ** — CLI (`internal/occ`); talks to openchoreo-api through the generated client
  (`internal/occ/resources/client`), not to the cluster directly. Commands in `internal/occ/cmd/<kind>/`.
- **cluster-gateway / cluster-agent** — control plane ↔ remote plane clusters. The agent dials out
  from the managed cluster; the gateway multiplexes API/exec/log traffic back over that connection
  (`internal/clients/gateway` is the control-plane-side client).
- **remote-agent / remote-agent-router** — `occ remote` tunnelling. Wire contract and the security
  model (CP-signed capability, per-stream authorize callback) are documented in
  `internal/remoteconnect/doc.go`.

### Cross-cutting

- **Authorization**: Casbin-based, `internal/authz` (core/PDP/PAP) with CEL conditions; the
  AuthzRole/AuthzRoleBinding CRDs (and Cluster variants) are the policy source.
- **Audit**: operation tables are *generated* from each service's OpenAPI spec by
  `tools/auditgen` into `<service>/audit/definitions.gen.go`; exemptions are hand-maintained in
  `exemptions.go`. Adding an endpoint means rerunning `make audit-gen`. Middleware lives in
  `internal/server/middleware/audit`.
- **Config**: koanf (file + env + defaults) via `internal/config`; each service has its own
  `config` package.

## Conventions

- Every Go file needs the Apache-2.0 header (`make license-fix` adds it); files must end in a newline.
- New CRDs follow `docs/contributors/adding-new-crd.md`: Kubebuilder scaffolds, then the controller is
  moved to `internal/controller/<kind>/controller.go` with the struct renamed to `Reconciler`.
- Controller tests: Ginkgo + envtest (`suite_test.go` per package). Service/handler tests: testify +
  mockery mocks (`mocks/` subdirs, regenerated by `make mockery-gen`).
- RBAC comes from `+kubebuilder:rbac` markers on reconcilers — add markers, then `make manifests`.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/) (the PR title becomes the
  squashed commit message and is CI-validated) and **every commit must be DCO signed off**
  (`git commit -s`). AI-assisted changes must tick the AI box in the PR template — see
  `docs/contributors/AI-POLICY.md`.
