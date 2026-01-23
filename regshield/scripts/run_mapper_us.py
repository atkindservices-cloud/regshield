from pathlib import Path
import json

CLEAN_DIR = Path("regshield/data/cleaned_rules_us")
OUT_DIR = Path("regshield/data/mapped_rules_us")
OUT_DIR.mkdir(exist_ok=True)

def map_rule(text, filename):
    rule = {
        "rule_id": filename.replace(".txt", ""),
        "authority": "FTC / NIST",
        "scope": "US Businesses",
        "applies_if": [
            "Handles customer data",
            "Operates in the US"
        ],
        "required_controls": [
            "Access control",
            "Data encryption",
            "Incident response plan"
        ],
        "evidence_required": [
            "Security policy",
            "Encryption configuration",
            "Access logs"
        ],
        "risk_level": "HIGH",
        "penalty": "Regulatory action, fines"
    }
    return rule

count = 0
for f in CLEAN_DIR.glob("*.txt"):
    text = f.read_text(errors="ignore")
    mapped = map_rule(text, f.name)
    out = OUT_DIR / f"{f.stem}.json"
    out.write_text(json.dumps(mapped, indent=2))
    count += 1

print("MAPPED RULE FILES:", count)
