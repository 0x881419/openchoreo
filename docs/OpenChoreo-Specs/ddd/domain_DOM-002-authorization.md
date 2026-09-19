---
title: Domain — Authorization
id: DOM-002
status: draft
kind: domain
features: [F-004, F-008, F-009, F-010]
owner: TBD
updated: 2026-09-19
---

# Domain — Authorization

> Reconstructed from the repository at commit `0c7e8a3e`. Rules are promoted from constraints
> the authors stated in comments and test names, each cited to the statement and to the code
> that enforces it. Covers F-004, and the authorization checks F-001 through F-010 rely on.

## Ubiquitous language

| Term | Meaning as used in code | Defined at |
| --- | --- | --- |
| AuthzRole | A named set of permitted actions, namespaced | [D: api/v1alpha1/authzrole_types.go:28] |
| ClusterAuthzRole | The same, fleet-wide | [D: api/v1alpha1/clusterauthzrole_types.go:28] |
| AuthzRoleBinding | Grants a role to subjects within a target scope | [D: api/v1alpha1/authzrolebinding_types.go:69] |
| TargetScope / ClusterTargetScope | Where a binding applies in the resource hierarchy | [D: internal/authz/core/types.go:26] |
| PDP | Policy decision point — answers "may this subject do this?" | [D: internal/authz/casbin/pdp.go:251] |
| PAP | Policy administration point — maintains the enforcer's rules | [D: internal/authz/casbin/pap.go:1] |
| Entitlement | One action evaluated against one request context | [D: internal/authz/casbin/pdp.go:251] |

## Actors

Subject types are enumerated by the API itself [D: openapi/openchoreo-api.yaml:3684].

OPEN: which subject types are expected in a production install — human users, service
accounts, AI agents — and does the platform distinguish them anywhere beyond the type name?

## Rules

- **DOM-002-R1** — A resource hierarchy must not set both Component and Resource: they are
  sibling sub-scopes under Project, and the invariant is enforced at the CRD layer via
  kubebuilder XValidation on TargetScope / ClusterTargetScope
  [D: internal/authz/core/types.go:26].
- **DOM-002-R2** — Policy evaluation fails closed on a malformed entry, and does so for the
  whole custom resource rather than per entry: "The error path is order-independent: a broken
  entry anywhere in the policy poisons the whole CR, even if a sibling entry cleanly matched.
  We don't know what the broken entry was meant to do, so we cannot trust the sibling result."
  [D: internal/authz/casbin/helpers_test.go:1559]
- **DOM-002-R3** — Removing a grouping policy that was never present is a no-op, not an error:
  "When an action to be removed was never in the enforcer, RemoveGroupingPolicy returns
  (false, nil) and the handler logs a debug message."
  [D: internal/authz/casbin/k8s_watcher_test.go:2412]
- **DOM-002-R4** — The request context is serialised once per request and reused across every
  entitlement evaluated for it [D: internal/authz/casbin/pdp.go:251].
- **DOM-002-R5** — Two data-plane routes are authenticated outside the standard middleware
  order, so that a rejected request never reaches the pattern-map-driven middleware. The code
  states why in its own words: "These two routes reach the data plane — a live shell and a live
  traffic stream" [D: cmd/openchoreo-api/main.go:338].

## Enforcement topology

I: authorization is applied at the API boundary and at admission, not inside reconcilers — basis: the PDP is constructed in the API server's startup path and the role-binding webhooks validate at admission, while no controller package imports the PDP [D: internal/webhook/authzrolebinding/suite_test.go:54].

**Structural note worth escalating:** the four authz kinds are the only CRD family in the
platform with no controller package. They are watched and pushed into the Casbin enforcer by
`SetupAuthzWatchers` rather than reconciled toward a desired state
[D: internal/authz/casbin/k8s_watcher.go:29].

## Open questions

OPEN: because the authz kinds are watched rather than reconciled, nothing reports drift if the
enforcer's in-memory state and the CRDs disagree. Is that an accepted property, and how would
an operator detect it?

OPEN: is deny-wins a stated product guarantee? The e2e suite exercises deny overrides, but a
test records behaviour, not a promise.

OPEN: what is the intended blast radius of the disabled authorizer
[D: internal/authz/disabled_authorizer.go:1] — local development only, or is there a supported
deployment that runs without a PDP?

OPEN: Casbin was chosen over Kubernetes RBAC, OPA/Rego and an in-house evaluator. The
repository retains no record of that comparison.
