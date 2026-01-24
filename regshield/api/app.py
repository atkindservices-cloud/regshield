from fastapi import FastAPI
from regshield.scripts.run_report_us import generate_report

app = FastAPI(title="RegShield AI")

@app.post("/audit")
def audit(payload: dict):
    report = generate_report(
        audit_results=[],
        company=payload.get("company", {})
    )
    return report
