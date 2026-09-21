#!/usr/bin/env python3
"""Rule config for v1.2.0 F-005.

Config only — the logic lives in route.py. Add paths to EXTRA as the feature's
document set grows, then re-run this file to regenerate the JSON.

    python rule_v1.2.0_F-005.py
"""
from route import build, emit

VERSION = "v1.2.0"
FEATURE_ID = "F-005"
FEATURE_TITLE = "Multi-Plane Topology and Connectivity"

EXTRA = {
    "domain": ["docs/OpenChoreo-Specs/ddd/domain_DOM-003-plane-connectivity.md"],
    "adrs": ["docs/OpenChoreo-Specs/ADRs/adrs_ADR-0001-record-architecture-decisions.md"],
    "runbooks": ["docs/OpenChoreo-Specs/runbook/runbook_DEV_RB-001-local-setup.md"],
    "tests": ["docs/OpenChoreo-Specs/tests/test_v1.2.0_F-005.md"],
}

if __name__ == "__main__":
    emit(build(VERSION, FEATURE_ID, FEATURE_TITLE, EXTRA))
