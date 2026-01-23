from typing import Dict, List

def explain_result(report: Dict) -> str:
    summary = report.get("summary", {})
    failed = summary.get("failed_rules", 0)

    if failed == 0:
        return (
            "✅ Your company appears compliant based on provided evidence. "
            "All evaluated controls are satisfied. Continue maintaining policies and logs."
        )

    explanations = []
    for rule in report.get("failed_details", []):
        explanations.append(
            f"- Rule '{rule.get('rule')}' failed because required evidence was missing."
        )

    return (
        "⚠️ Compliance gaps detected:\n"
        + "\n".join(explanations)
        + "\n\nSuggested Action: Upload missing policies, logs, or procedures."
    )
