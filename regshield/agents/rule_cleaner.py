import json
from pathlib import Path
from datetime import datetime

def clean_mapped_file(in_path: Path, out_dir: Path) -> bool:
    try:
        data = json.loads(in_path.read_text(encoding="utf-8", errors="ignore"))

        # basic cleaning: keep meta + sections, remove full_text to make small
        cleaned = {
            "meta": data.get("meta", {}),
            "summary": data.get("summary", {}),
            "sections": data.get("sections", []),
            "cleaned_at": datetime.utcnow().isoformat() + "Z",
        }

        # remove empty sections
        cleaned["sections"] = [
            s for s in cleaned["sections"]
            if s.get("text", "").strip()
        ]

        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / in_path.name
        out_path.write_text(json.dumps(cleaned, indent=2), encoding="utf-8")
        print("Cleaned ->", out_path.name)
        return True
    except Exception as e:
        print("CLEAN ERROR:", in_path.name, "->", e)
        return False
