---
title: Domain — Plane Connectivity
id: DOM-003
status: draft
kind: domain
features: [F-005, F-007]
owner: TBD
updated: 2026-09-19
---

# Domain — Plane Connectivity

> Reconstructed from the repository at commit `0c7e8a3e`. This is the densest set of stated
> constraints in the codebase: the gateway fabric's tests are written as prose invariants, and
> they are quoted here with their citations because they are the clearest statement of intent
> the repository contains. Covers F-005.

## Ubiquitous language

| Term | Meaning as used in code | Defined at |
| --- | --- | --- |
| Plane | A cluster with a role: control, data, workflow, observability | [D: api/v1alpha1/dataplane_types.go:172] |
| Cluster agent | Runs in a managed cluster and dials out to the gateway | [D: internal/cluster-agent/agent.go:1] |
| Cluster gateway | Accepts agent connections and routes work to them | [D: internal/cluster-gateway/server.go:1] |
| Fabric | The gateway's peer mesh across its own replicas | [D: internal/cluster-gateway/fabric/fabric.go:117] |
| Registry | Replicated view of which pod owns which agent connection | [D: internal/cluster-gateway/fabric/fabric.go:117] |
| Capability | A control-plane-signed token scoping one `occ remote` session | [D: internal/remoteconnect/capability.go:1] |
| Remote agent | Per project+env tunnel endpoint in a data plane | [D: internal/remoteconnect/doc.go:5] |

## Transport model

Stated by the package itself, in three steps: `occ` resolves dependencies against the control
plane, which provisions a remote-agent and returns targets plus a signed capability; `occ`
dials that agent directly over TLS and multiplexes one yamux stream per connection; and for
each stream the agent calls the control plane to authorize before dialling the target
[D: internal/remoteconnect/doc.go:11-21].

I: the design separates the authorization path from the data path — basis: the package states that "the byte path does not traverse the control plane" while every stream still requires a control-plane authorize call [D: internal/remoteconnect/doc.go:15].

## Rules

- **DOM-003-R1** — Registry lookup must never block on the network: "The hot path (Lookup) must
  be local-memory fast: no request ever blocks on a network call to find out where an agent
  lives." [D: internal/cluster-gateway/fabric/fabric.go:117]
- **DOM-003-R2** — A consumer that stops reading must not wedge the informer, and must not be
  handed a stale view once it returns: "The channel keeps only the newest peer set, since an
  older one is never the right basis for reconciling links."
  [D: internal/cluster-gateway/fabric/discovery_test.go:329]
- **DOM-003-R3** — A peer that cannot be dialled is retried with a widening backoff, never in a
  tight loop: "during a rollout every replica briefly points at an address that is not
  accepting yet, and hammering it would turn a slow start into a thundering herd."
  [D: internal/cluster-gateway/fabric/mesh_test.go:1089]
- **DOM-003-R4** — A socket that never carried a frame is treated like a failed dial, because
  redialling immediately "would spin against a peer that is accepting connections but cannot
  serve them" [D: internal/cluster-gateway/fabric/mesh.go:564].
- **DOM-003-R5** — A forward to an owner this pod holds no link to fails immediately with a
  retryable sentinel: "the caller can try another replica, and the request provably never left
  this pod." [D: internal/cluster-gateway/fabric/mesh_test.go:1052]
- **DOM-003-R6** — "Never dispatched" and "outcome unknown" must remain distinguishable. A
  request already on the wire "must not be reported as something the caller may safely retry"
  [D: internal/cluster-gateway/fabric/mesh_test.go:1435], and the mid-request sentinel is kept
  distinct from `ErrNoLink` [D: internal/cluster-gateway/server_test.go:2108].
- **DOM-003-R7** — A sequence gap is repaired by requesting a full snapshot from the owner, and
  the gapped delta must not be applied: "routing to it would send requests to a peer whose real
  state we do not know." [D: internal/cluster-gateway/fabric/mesh_test.go:1315]
- **DOM-003-R8** — A draining pod's agents still count in status but must not receive new
  forwards [D: internal/cluster-gateway/fabric/registry_test.go:136].
- **DOM-003-R9** — Idempotent teardown throughout: unregistering something never registered,
  purging an owner the registry never heard of, and shutting down a mesh that never started
  must each be a no-op [D: internal/cluster-gateway/server_test.go:2213],
  [D: internal/cluster-gateway/fabric/mesh_test.go:1071],
  [D: internal/cluster-gateway/fabric/mesh_test.go:610].
- **DOM-003-R10** — Rebalancing tolerates a slack above fair share, without which "a fleet that
  cannot divide evenly (4 connections across 3 pods) would shed forever"
  [D: internal/cluster-gateway/server.go:1520].
- **DOM-003-R11** — Agent identity is parsed from client-controlled certificate subject data,
  and a quoted `;Cert=` inside it must not override the leaf
  [D: internal/cluster-gateway/agent_auth_test.go:182].

## Open questions

OPEN: this rule set describes a mature distributed system. Which of these invariants came from
observed production incidents and which were anticipated? The tests state the invariant and
never the incident, and that history is the most useful thing a new maintainer could have.

OPEN: what is the supported upper bound on connected planes and agents per gateway replica?
R10 implies a fairness target that is never stated as a number.

OPEN: what is the capability's lifetime, and what revokes one mid-session?

OPEN: is single-cluster (all planes co-located) a supported production topology, or only the
development convenience it is used as throughout the repository?
