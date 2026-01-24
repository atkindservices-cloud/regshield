def explain_rule(rule_id, status, evidence_missing=None):
    if status == "PASS":
        return f"Rule {rule_id} is satisfied. Required controls are present."

    if status == "FAIL":
        return (
            f"Rule {rule_id} failed due to missing evidence: "
            f"{', '.join(evidence_missing or [])}. "
            f"Recommended action: provide the missing controls."
        )

    return f"Rule {rule_id} is pending review."
