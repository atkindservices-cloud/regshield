from __future__ import annotations
import json, sys
from pathlib import Path

REPORT_PATH = Path("regshield/data/reports_us/company_report.json")

REQUIRED_TOP_KEYS = {
    "company": (str, dict),     # allow string or dict
    "status": (str,),
    "score": (int, float),
    "failed_rules": (list,),
}

ALLOWED_STATUS = {"PASS", "FAIL", "PENDING"}

def fail(msg: str) -> None:
    print(f"❌ STEP-1 FAIL: {msg}")
    sys.exit(1)

def ok(msg: str) -> None:
    print(f"✅ {msg}")

def main() -> None:
    if not REPORT_PATH.exists():
        fail(f"Missing report file: {REPORT_PATH}")

    raw = REPORT_PATH.read_text(encoding="utf-8").strip()
    if not raw:
        fail("Report file is empty")

    try:
        report = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON in report: {e}")

    if not isinstance(report, dict):
        fail(f"Report must be a JSON object (dict), got {type(report).__name__}")

    for k, allowed_types in REQUIRED_TOP_KEYS.items():
        if k not in report:
            fail(f"Missing top-level key: '{k}'")
        if not isinstance(report[k], allowed_types):
            fail(f"Key '{k}' must be {allowed_types}, got {type(report[k]).__name__}")

    status = report["status"]
    if status not in ALLOWED_STATUS:
        fail(f"status must be one of {sorted(ALLOWED_STATUS)}, got '{status}'")

    score = report["score"]
    if isinstance(score, bool):
        fail("score cannot be boolean")
    if not (0 <= float(score) <= 100):
        fail(f"score must be between 0 and 100, got {score}")

    failed_rules = report["failed_rules"]
    if not isinstance(failed_rules, list):
        fail("failed_rules must be a list")

    if status == "FAIL" and len(failed_rules) == 0:
        fail("status is FAIL but failed_rules is empty (inconsistent)")

    for i, item in enumerate(failed_rules):
        if not isinstance(item, dict):
            fail(f"failed_rules[{i}] must be an object/dict, got {type(item).__name__}")
        if "id" not in item or not isinstance(item["id"], str) or not item["id"].strip():
            fail(f"failed_rules[{i}] missing/invalid 'id'")
        if "status" not in item or item["status"] not in {"FAIL", "PENDING", "PASS"}:
            fail(f"failed_rules[{i}] missing/invalid 'status'")
        if "missing_evidence" in item and not isinstance(item["missing_evidence"], list):
            fail(f"failed_rules[{i}].missing_evidence must be a list if present")

    if "explanations" in report:
        if not isinstance(report["explanations"], list):
            fail("explanations must be a list if present")
        if len(failed_rules) > 0 and len(report["explanations"]) == 0:
            fail("failed_rules exists but explanations list is empty")

    ok("Report file exists and JSON is valid")
    ok("Top-level keys and types look correct")
    ok(f"Status={status}, Score={score}, FailedRules={len(failed_rules)}")
    print("✅ STEP-1 PASS: report structure is OK")

if __name__ == "__main__":
    main()
