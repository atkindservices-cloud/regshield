
from regshield.agents.llm_agent import llm_explain

def chat(query, report):
    q = query.lower()
    failed = report.get("failed_rules", [])
    fixes = report.get("fixes", [])

    if "why" in q or "fail" in q:
        if not failed:
            return "You passed all checks. No failed rules."
        return "You failed because of: " + ", ".join(r["id"] for r in failed)

    if "document" in q or "upload" in q:
        if not fixes:
            return "No documents required."
        docs = []
        for f in fixes:
            docs.extend(f.get("upload", []))
        return "You need to upload: " + ", ".join(docs)

    if "pass" in q:
        if not fixes:
            return "You already pass."
        return "Upload the required documents and re-run the audit."

    if "status" in q:
        return f"Company status: {report.get('status')}"

    if "score" in q:
        return f"Compliance score: {report.get('score')}"

    return llm_explain(query, report)
