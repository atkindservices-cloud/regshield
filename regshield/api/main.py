from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import json
from pathlib import Path

app = FastAPI(title="RegShield AI")

class CompanyInput(BaseModel):
    name: str
    industry: str
    country: str

@app.post("/audit")
def run_audit(company: CompanyInput):
    # write temp company file
    company_file = Path("regshield/data/company.json")
    company_file.write_text(json.dumps(company.dict(), indent=2))

    # run full pipeline
    subprocess.run(["bash", "run_demo_us.sh"], check=True)

    # read final report
    report_path = Path("regshield/data/reports_us/company_report.json")
    report = json.loads(report_path.read_text())

    return report
