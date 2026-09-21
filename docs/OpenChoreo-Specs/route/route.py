#!/usr/bin/env python3
"""Route entrypoint.

A route is the ordered list of documents an agent must read before it touches a
feature. This file is the shared engine; one thin `rule_<VERSION>_<ID>.py` per
feature supplies the config.

    python rule_v0.1_F-001.py              # (re)generate rule_v0.1_F-001.json
    python route.py --version v0.1 --id F-001   # print the reading list, verify paths exist
"""
import argparse
import json
from pathlib import Path

ROUTE_DIR = Path(__file__).resolve().parent
SPEC_DIR = ROUTE_DIR.parent
REPO_ROOT = SPEC_DIR.parent.parent
TEMPLATE = ROUTE_DIR / "rule.template.json"

READ_ORDER = ["domain", "prd", "adrs", "architecture", "tasks", "tests", "runbooks"]


def build(version, feature_id, feature_title="", extra=None):
    """Render the rule template for one feature. `extra` appends to any list key."""
    raw = TEMPLATE.read_text(encoding="utf-8")
    for token, value in (
        ("{{VERSION}}", version),
        ("{{FEATURE_ID}}", feature_id),
        ("{{FEATURE_TITLE}}", feature_title or feature_id),
    ):
        raw = raw.replace(token, value)
    rule = json.loads(raw)
    for key, items in (extra or {}).items():
        target = rule["reads"] if key in rule["reads"] else rule
        target.setdefault(key, [])
        target[key] = list(dict.fromkeys(target[key] + list(items)))
    for group, paths in rule["reads"].items():
        rule["reads"][group] = [p for path in paths for p in _expand(path)]
    return rule


def _expand(pattern):
    """Globs let the template stay slug-agnostic; unmatched globs are kept so `show` flags them."""
    if "*" not in pattern:
        return [pattern]
    hits = sorted(str(p.relative_to(REPO_ROOT)) for p in REPO_ROOT.glob(pattern))
    return hits or [pattern]


def emit(rule):
    out = ROUTE_DIR / f"rule_{rule['version']}_{rule['feature_id']}.json"
    out.write_text(json.dumps(rule, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(REPO_ROOT)}")
    return out


def load(version, feature_id):
    path = ROUTE_DIR / f"rule_{version}_{feature_id}.json"
    if not path.exists():
        raise SystemExit(f"missing {path.name} — run rule_{version}_{feature_id}.py first")
    return json.loads(path.read_text(encoding="utf-8"))


def show(rule):
    print(f"# Route {rule['version']} {rule['feature_id']} — {rule['feature_title']}")
    print(f"objective: {rule['objective']}\n")
    n, missing = 0, []
    for group in READ_ORDER:
        for rel in rule["reads"].get(group, []):
            n += 1
            ok = (REPO_ROOT / rel).exists()
            missing.append(rel) if not ok else None
            print(f"{n:>2}. [{group}] {rel}{'' if ok else '   <-- MISSING'}")
    print("\nguardrails:")
    for g in rule.get("guardrails", []):
        print(f"  - {g}")
    print("\nexit criteria:")
    for c in rule.get("exit_criteria", []):
        print(f"  - {c}")
    if missing:
        raise SystemExit(f"\n{len(missing)} referenced document(s) missing")
    print(f"\nall {n} referenced documents present")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--version", required=True)
    p.add_argument("--id", required=True, dest="feature_id")
    a = p.parse_args()
    show(load(a.version, a.feature_id))
