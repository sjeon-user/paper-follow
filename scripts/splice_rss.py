"""Fill rss-brief.html: BRIEF_DATE / ARCHIVE / PAPERS, then snapshot to rss-brief-<date>.html and prune to 7."""
import glob, io, os, re, sys
root = r"C:\Users\KIMM\Desktop\2026\연구 행정 스킬화\2026.07.22 physical AI 논문 팔로우업"
date = sys.argv[1]
label = sys.argv[3] if len(sys.argv) > 3 else date
block = [l.rstrip("\r") for l in io.open(sys.argv[2], encoding="utf-8").read().rstrip("\r\n").split("\n")]

path = os.path.join(root, "rss-brief.html")
src = io.open(path, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in src else "\n"
lines = src.split(eol)

def idx(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            return i
    raise SystemExit("anchor not found: " + prefix)

# archive list = existing snapshots + today, newest first, max 7
snaps = sorted({re.search(r"rss-brief-(\d{4}-\d{2}-\d{2}[a-z]?)\.html$", p).group(1) for p in glob.glob(os.path.join(root, "rss-brief-*.html"))} | {date}, reverse=True)
keep, drop = snaps[:7], snaps[7:]

lines[idx("const BRIEF_DATE")] = f'const BRIEF_DATE = "{label}";'
lines[idx("const ARCHIVE")] = "const ARCHIVE = [" + ", ".join(f'"{d}"' for d in keep) + "];"
i = idx("const PAPERS = [")
j = idx("/* ====== 여기까지 ====== */")
lines = lines[:i] + block + lines[j:]
out = eol.join(lines)
for name in ("rss-brief.html", f"rss-brief-{date}.html"):
    with io.open(os.path.join(root, name), "w", encoding="utf-8", newline="") as f:
        f.write(out)
for d in drop:
    os.remove(os.path.join(root, f"rss-brief-{d}.html"))
print(f"rss-brief.html + rss-brief-{date}.html written ({len(block)} block lines); ARCHIVE={keep}; pruned={drop}")

# theme box + archive labels from themes.json (see scripts/add_theme.py)
sys.path.insert(0, os.path.join(root, "scripts"))
import add_theme
_kind = "arxiv" if os.path.basename(path) == "paper-brief.html" else "rss"
_prefix = "brief-" if _kind == "arxiv" else "rss-brief-"
for _name in (os.path.basename(path), f"{_prefix}{date}.html"):
    _label, _ = add_theme.apply(_kind, date, os.path.join(root, _name))
if not _label:
    print(f"WARNING: themes.json has no '{_kind}' entry for {date} - add it and re-run to fill the theme box")
else:
    print(f"theme applied: {_label}")
