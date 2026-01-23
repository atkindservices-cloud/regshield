import json
import re
from pathlib import Path
from datetime import datetime

def _clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def _extract_simple_sections(text: str):
    """
    Very simple heuristic:
    - Uses headings like ALL CAPS lines or lines ending with ':' as section titles
    """
    lines = text.splitlines()
    sections = []
    current = {"title": "INTRO", "content": []}

    def push():
        nonlocal current
        if current["content"]:
            sections.append({
                "title": current["title"],
                "text": _clean_text("\n".join(current["content"]))
            })

    for line in lines:
        s = line.strip()
        if not s:
            current["content"].append("")
            continue

        # headings (basic heuristic)
        if (len(s) < 80 and s.isupper()) or (len(s) < 80 and s.endswith(":")):
            push()
            current = {"title": s.strip(":").strip(), "content": []}
        else:
            current["content"].append(s)

    push()
    return sections

def map_rule(in_path: Path, out_dir: Path) -> bool:
    """
    US-first mapper:
    Reads raw .txt -> saves a .json with sections + metadata.
    """
    try:
        raw = in_path.read_text(encoding="utf-8", errors="ignore")
        raw = _clean_text(raw)

        data = {
            "meta": {
                "source_file": in_path.name,
                "mapped_at": datetime.utcnow().isoformat() + "Z",
            },
            "summary": {
                "chars": len(raw),
                "lines": raw.count("\n") + 1,
            },
            "sections": _extract_simple_sections(raw),
            "full_text": raw[:20000]  # keep first 20k chars (safe)
        }

        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / (in_path.stem + ".json")
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print("Mapped ->", out_path.name)
        return True
    except Exception as e:
        print("MAP ERROR:", in_path.name, "->", e)
        return False
