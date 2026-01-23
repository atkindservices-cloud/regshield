from pathlib import Path
import json
import re

def _tokens(s: str):
    # split by non-alphanumeric, keep meaningful tokens
    parts = re.split(r"[^a-zA-Z0-9]+", (s or "").lower())
    return [p for p in parts if len(p) >= 3]

def _has_evidence(rule_name: str, evidence_root: Path) -> bool:
    files = [p for p in evidence_root.rglob("*") if p.is_file()]
    if not files:
        return False

    rule = (rule_name or "").lower()
    all_names = " ".join(p.name.lower() for p in files)

    # base tokens from rule name
    keys = set(_tokens(rule_name))

    # add smart synonyms for your current demo rules
    if "glba" in rule or "safeguards" in rule or "16_cfr_part_314" in rule or "314" in rule:
        keys.update(["glba", "safeguards", "ftc", "314", "security", "program", "policy"])

    if "nist" in rule or "cybersecurity" in rule or "framework" in rule:
        keys.update(["nist", "csf", "cybersecurity", "framework", "policy"])

    return any(k in all_names for k in keys)

def audit_rule(rule_text: str, rule_name: str):
    evidence_root = Path("regshield/data/evidence_us")
    has_evidence = _has_evidence(rule_name, evidence_root)

    evidence_status = "PASS (manual evidence detected)" if has_evidence else "FAIL (no evidence found)"

    questions = [
        f"Explain how your company complies with {rule_name}.",
        f"What policies exist to enforce {rule_name}?",
        f"Who is responsible for compliance with {rule_name}?",
        f"What evidence can you provide for {rule_name} compliance?",
        f"What happens if this control fails?",
    ]

    return {
        "rule": rule_name,
        "questions": questions,
        "status": evidence_status,
    }
