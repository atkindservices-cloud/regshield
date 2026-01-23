from pathlib import Path
import re

RAW = Path("regshield/data/raw_rules_us")
CLEAN = Path("regshield/data/cleaned_rules_us")
CLEAN.mkdir(exist_ok=True)

def clean(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

count = 0
for f in RAW.glob("*.txt"):
    cleaned = clean(f.read_text(errors="ignore"))
    out = CLEAN / f.name
    out.write_text(cleaned)
    count += 1

print("CLEANED FILES:", count)
