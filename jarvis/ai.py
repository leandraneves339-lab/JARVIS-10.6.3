import json
import urllib.request
import urllib.error

class AIClient:
    """Optional generic JSON chat endpoint.

    Set JARVIS_API_URL and JARVIS_API_KEY in .env.
    The endpoint should accept:
      {"message": "...", "system": "..."}
    and return either {"reply": "..."} or {"text": "..."}.
    """

    def __init__(self, url="", key=""):
        self.url = url
        self.key = key

    def enabled(self):
        return bool(self.url)

    def ask(self, message, system="You are JARVIS 10.5, a concise personal assistant."):
        if not self.url:
            return None
        body = json.dumps({"message": message, "system": system}).encode("utf-8")
        req = urllib.request.Request(self.url, data=body,
                                     headers={"Content-Type":"application/json"})
        if self.key:
            req.add_header("Authorization", "Bearer " + self.key)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode("utf-8"))
            return data.get("reply") or data.get("text")
        except (urllib.error.URLError, TimeoutError, ValueError):
            return None
