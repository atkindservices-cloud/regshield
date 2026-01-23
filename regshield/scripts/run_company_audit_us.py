import json
from pathlib import Path

from regshield.agents.report_agent import generate_report

COMPANY_DIR = Path("regshield/data/company_inputs")
AUDITED_RULES_DIR = Path("regshield/data/audited_rules_us")
OUTPUT_DIR = Path("regshield/data/company_reports_us")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    company_files = list(COMPANY_DIR.glob("*.json"))
    if not company_files:
        raise FileNotFoundError(f"No company files found in: {COMPANY_DIR}")

    company_file = company_files[0]
    company = json.loads(company_file.read_text(encoding="utf-8"))

    print("Company loaded:", company.get("company_name", company_file.name))

    success = 0
    for rule_file in AUDITED_RULES_DIR.glob("*.json"):
        print("Checking:", rule_file.name)

        ok = generate_report(
            input_path=rule_file,
            output_dir=OUTPUT_DIR,
            company=company
        )

        if ok:
            success += 1

    print("COMPANY REPORT SUCCESS COUNT:", success)


if __name__ == "__main__":
    main()
