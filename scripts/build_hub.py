"""Refresh the FALLBACK issue list embedded in index.html (the hub page).

The hub reads themes.json live when served over http(s); FALLBACK is only what it shows before that
fetch returns, or when the page is opened as a local file. Run after adding issues:
    python scripts/build_hub.py
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = {"arxiv": "brief-", "rss": "rss-brief-", "skin": "skin-brief-",
          "cocult": "cocult-brief-", "liquid": "liquid-brief-"}
themes = json.load(io.open(os.path.join(ROOT, "themes.json"), encoding="utf-8-sig"))
fb = {}
for kind, prefix in PREFIX.items():
    reg = themes.get(kind, {})
    dates = [d for d in sorted(reg, reverse=True)
             if os.path.exists(os.path.join(ROOT, "%s%s.html" % (prefix, d)))][:30]
    fb[kind] = {d: {"label": reg[d].get("label", "")} for d in dates}
path = os.path.join(ROOT, "index.html")
src = io.open(path, encoding="utf-8", newline="").read()
new, n = re.subn(r"const FALLBACK = .*?;(\r?\n)",
                 lambda m: "const FALLBACK = " + json.dumps(fb, ensure_ascii=False) + ";" + m.group(1), src, count=1)
if not n:
    raise SystemExit("FALLBACK anchor not found in index.html")
io.open(path, "w", encoding="utf-8", newline="").write(new)
print("hub fallback refreshed:", {k: len(v) for k, v in fb.items()})
