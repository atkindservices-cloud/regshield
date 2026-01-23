from pathlib import Path
import json
from regshield.agents.audit_agent import audit_rule

RULES_DIR = Path("regshield/data/cleaned_rules_us")
OUT_DIR = Path("regshield/data/audited_rules_us")
OUT_DIR.mkdir(exist_ok=True)

count = 0
for f in RULES_DIR.glob("*.txt"):
    text = f.read_text(errors="ignore")
    result = audit_rule(text, f.stem)
    out = OUT_DIR / f"{f.stem}_audit.json"
    out.write_text(json.dumps(result, indent=2))
    count += 1

print("AUDITED RULES:", count)
