def generate_report(audit_results: list, company: dict):
    # Normalize status so report never crashes
    norm = []
    for r in audit_results:
        if "status" not in r:
            r["status"] = "UNKNOWN"
        norm.append(r)

    failed = [r for r in norm if "FAIL" in str(r.get("status", ""))]

    score = max(0, 100 - len(failed) * 20)

    return {
        "company": company,
        "summary": {
            "total_rules_checked": len(norm),
            "failed_rules": len(failed),
            "compliance_score": score,
            "status": "PASS" if score >= 80 else "FAIL"
        },
        "failed_details": failed,
        "note": "Advisory only. Not legal opinion."
    }
