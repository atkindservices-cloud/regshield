


def evidence_satisfied(rule):
    evidence_dir = Path("regshield/data/evidence_us") / company["name"].replace(" ", "_")
    if not evidence_dir.exists():
        return False

    files = [
        f.stem.lower().replace(" ", "_")
        for f in evidence_dir.iterdir()
        if f.is_file()
    ]

    required = [
        r.lower().replace(" ", "_")
        for r in rule.get("missing_evidence", [])
    ]

    for req in required:
        if not any(req in f for f in files):
            return False

    return True



from regshield.agents.explainer import explain_rule
from pathlib import Path
import json
from regshield.agents.report_agent import generate_report
from regshield.agents.reasoning_agent import explain_result

AUDIT_DIR = Path("regshield/data/audited_rules_us")
OUT_DIR = Path("regshield/data/reports_us")
OUT_DIR.mkdir(exist_ok=True)

company = {
    "name": "Demo SaaS Inc",
    "country": "US",
    "industry": "SaaS"
}


def check_evidence(rule_id):
    evidence_dir = Path("regshield/data/evidence_us") / company["name"].replace(" ", "_")
    return evidence_dir.exists() and any(evidence_dir.iterdir())

audits = []

for f in AUDIT_DIR.glob("*.json"):
    data = json.loads(f.read_text())
if isinstance(data, dict):
    audits.append(data)
elif isinstance(data, list):
    audits.extend([d for d in data if isinstance(d, dict)])



passed = []
failed = []

for a in audits:
    if evidence_satisfied(a):
        a["status"] = "PASS"
        a["missing_evidence"] = []
        passed.append(a)
    else:
        a["status"] = "FAIL"
        failed.append(a)


report = generate_report(failed, company)

# ===== FINAL AGGREGATION =====
report["failed_rules"] = failed
report["score"] = int(100 * (1 - len(failed) / max(1, len(audits))))




out = OUT_DIR / "company_report.json"
report['explanations'] = explain_result(report)

# ===== FINAL REPORT AGGREGATION =====
report["failed_rules"] = failed
report["status"] = "PASS" if len(failed) == 0 else "FAIL"
report["score"] = int(100 * (1 - len(failed) / max(1, len(audits))))

out.write_text(json.dumps(report, indent=2))

print("REPORT GENERATED:", out)
