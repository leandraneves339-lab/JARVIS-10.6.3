import json
import os
from pathlib import Path

class Memory:
    def __init__(self, filename="jarvis_memory.json"):
        base = Path(os.getenv("JARVIS_DATA_DIR", "."))
        base.mkdir(parents=True, exist_ok=True)
        self.path = base / filename
        self.data = {"notes": [], "preferences": {}}
        self.load()

    def load(self):
        try:
            if self.path.exists():
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            self.data = {"notes": [], "preferences": {}}

    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    def remember(self, note):
        note = note.strip()
        if note:
            self.data.setdefault("notes", []).append(note)
            self.data["notes"] = self.data["notes"][-100:]
            self.save()

    def recent(self, limit=10):
        return self.data.get("notes", [])[-limit:]
