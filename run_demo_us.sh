#!/bin/bash
set -e

echo "Running RegShield US Demo..."

python -m regshield.scripts.run_mapper_us
python -m regshield.scripts.run_audit_us

echo ""
echo "FINAL REPORT"

python - << 'EOF'

import json

from pathlib import Path

p = Path("regshield/data/reports_us/company_report.json")

data = json.loads(p.read_text())

print("Company:", data.get("company"))

print("Status:", data.get("status"))

print("Score:", data.get("score"))

print("Failed Rules:", len(data.get("failed_rules", [])))

EOF
