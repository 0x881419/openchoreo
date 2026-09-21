---
title: Domain — Component Delivery
id: DOM-001
status: draft
kind: domain
features: [F-001, F-002, F-003, F-006, F-008]
owner: TBD
updated: 2026-09-19
---

# Domain — Component Delivery

> Reconstructed from the repository at commit `0c7e8a3e`. Rules below were promoted from
> constraints the authors stated in their own comments and test names; each cites both the
> statement and the code that enforces it. A rule with no enforcement is recorded as a
> question, not as a rule.

## Ubiquitous language

| Term | Meaning as used in code | Defined at |
| --- | --- | --- |
| Component | A developer's unit of deployment — service, worker, scheduled task | [D: api/v1alpha1/component_types.go:19] |
| ComponentType | A platform-authored template that a Component instantiates | [D: api/v1alpha1/componenttype_types.go:265] |
| Trait | Reusable behaviour patched onto a rendered component | [D: api/v1alpha1/trait_types.go:301] |
| Workload | The runtime shape: containers, endpoints, connections | [D: api/v1alpha1/workload_types.go:372] |
| ComponentRelease | An immutable snapshot of type, traits and workload | [D: api/v1alpha1/componentrelease_types.go:138] |
| ReleaseBinding | A release bound to one Environment, with overrides | [D: api/v1alpha1/releasebinding_types.go:383] |
| RenderedRelease | Concrete Kubernetes objects destined for one plane | [D: api/v1alpha1/renderedrelease_types.go:66] |
| Environment | A deployment target within a data plane | [D: api/v1alpha1/environment_types.go:37] |
| DeploymentPipeline | The permitted promotion order between environments | [D: api/v1alpha1/deploymentpipeline_types.go:59] |
| Project | The isolation and networking boundary around components | [D: api/v1alpha1/project_types.go:70] |
| Connection | A declared dependency on another component's endpoint | [D: api/v1alpha1/releasebinding_types.go:12] |

I: the language is consistently *definition → release → binding → rendered* — basis: the same four-part naming recurs across three independent CRD families and their three binding controllers [D: api/v1alpha1/projectreleasebinding_types.go:93].

## Actors

| Actor | Evidence |
| --- | --- |
| Developer — owns Components, Workloads, ReleaseBindings | [D: api/v1alpha1/component_types.go:133] |
| Platform engineer — owns ComponentTypes, Traits, planes, policy | [D: api/v1alpha1/clustercomponenttype_types.go:141] |
| SRE — consumes observability and alerting | [D: api/v1alpha1/observabilityalertrule_types.go:216] |
| AI agent — operates the platform through MCP tools | [D: cmd/openchoreo-api/main.go:260] |

OPEN: these four are inferred from resource ownership and endpoint grouping. The repository
contains no persona definition, so the boundary between "developer" and "platform engineer"
in a real organisation using OpenChoreo is not knowable from here.

## Rules

Each rule is stated where the authors stated it, and cited to the code that enforces it.

- **DOM-001-R1** — A ResourceType output must set exactly one of `value`, `secretKeyRef` or
  `configMapKeyRef`. Stated and enforced as a CRD validation expression:
  `"(has(self.value)?1:0) + (has(self.secretKeyRef)?1:0) + (has(self.configMapKeyRef)?1:0) == 1"`
  [D: api/v1alpha1/resourcetype_types.go:49].
- **DOM-001-R2** — A resource hierarchy must not set both Component and Resource: they are
  sibling sub-scopes under Project. Stated in the type comment and enforced at the CRD layer
  via kubebuilder XValidation on TargetScope / ClusterTargetScope
  [D: internal/authz/core/types.go:26].
- **DOM-001-R3** — An endpoint is exposed by at most one route kind per visibility.
  HTTPRoute and GRPCRoute attach to the http and https gateway listeners; TLSRoute attaches to
  the tls listener for SNI passthrough, and the TLS trait swaps one for the other when the
  application terminates TLS [D: internal/controller/releasebinding/controller.go:5].
- **DOM-001-R4** — A malformed authorization policy poisons the whole custom resource, even
  where a sibling entry matched cleanly: "We don't know what the broken entry was meant to do,
  so we cannot trust the sibling result" [D: internal/authz/casbin/helpers_test.go:1559].
- **DOM-001-R5** — A ComponentRelease is an immutable snapshot; environment-specific variation
  is expressed on the ReleaseBinding, never by editing the release
  [D: docs/crds/renderedrelease.md:44-48], [D: api/v1alpha1/componentrelease_types.go:52].

I: R5 is the load-bearing invariant of the whole delivery model — basis: it is what makes a
promotion between environments a re-binding rather than a re-render, and the three release
families all repeat the pattern [D: api/v1alpha1/projectrelease_types.go:82].

## Invariants enforced by the platform

- Project-to-project traffic isolation is enforced by generated NetworkPolicies rather than
  configured by users [D: internal/networkpolicy].
- Finalizers gate deletion of every release-bearing kind, so rendered objects are removed from
  a data plane before the owning resource is released
  [D: internal/controller/renderedrelease/controller_finalize.go:1].

## Open questions

OPEN: what is the intended behaviour when a DeploymentPipeline's promotion path is edited while
bindings already exist downstream of the removed edge? The code reconciles; the product
expectation is unstated.

OPEN: 2401 further constraint-shaped comments were ranked below the extraction cut
[D: internal/controller/releasebinding/controller.go:5]. The rules above are the strongest
stated ones, not the complete set — the rest of this domain lives in code, not in prose.

OPEN: every rule above is enforced. Which rules does the business follow that the platform does
*not* enforce? That set is invisible from a repository and is usually where incidents come from.

OPEN: why does R1 exist — is a single-source output a security boundary, a rendering
constraint, or both? The validation expression states the rule and not the motive.
