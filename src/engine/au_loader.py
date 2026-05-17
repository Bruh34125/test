import json
from pathlib import Path
from typing import Dict, Any


def load_aus(root: str = "aus") -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    root_path = Path(root)
    if not root_path.exists():
        return result

    for child in root_path.iterdir():
        if not child.is_dir():
            continue
        meta = child / "au.json"
        if meta.exists():
            data = json.loads(meta.read_text())
            result[data.get("id", child.name)] = data
    return result
