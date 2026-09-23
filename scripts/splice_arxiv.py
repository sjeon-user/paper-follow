"""Fill paper-brief.html (arXiv brief): BRIEF_DATE / ARCHIVE / PAPERS; snapshot brief-<date>.html; keep 7 snapshots;
delete images/*.png not referenced by any remaining brief-*.html / paper-brief.html (keep.html / keep-img untouched)."""
import glob, io, os, re, sys
root = r"C:\Users\KIMM\Desktop\2026\연구 행정 스킬화\2026.07.22 physical AI 논문 팔로우업"
date = sys.argv[1]
block = [l.rstrip("\r") for l in io.open(sys.argv[2], encoding="utf-8").read().rstrip("\r\n").split("\n")]

path = os.path.join(root, "paper-brief.html")
src = io.open(path, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in src else "\n"
lines = src.split(eol)

def idx(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            return i
    raise SystemExit("anchor not found: " + prefix)

snaps = sorted({re.search(r"brief-(\d{4}-\d{2}-\d{2}[a-z]?)\.html$", p).group(1) for p in glob.glob(os.path.join(root, "brief-*.html"))} | {date}, reverse=True)
keep, drop = snaps[:7], snaps[7:]

lines[idx("const BRIEF_DATE")] = f'const BRIEF_DATE = "{date}";'
lines[idx("const ARCHIVE")] = "const ARCHIVE = [" + ", ".join(f'"{d}"' for d in keep) + "];"
i = idx("const PAPERS = [")
j = idx("/* ====== 여기까지 ====== */")
lines = lines[:i] + block + lines[j:]
out = eol.join(lines)
for name in ("paper-brief.html", f"brief-{date}.html"):
    with io.open(os.path.join(root, name), "w", encoding="utf-8", newline="") as f:
        f.write(out)
for d in drop:
    os.remove(os.path.join(root, f"brief-{d}.html"))

# orphan image cleanup (images/ only)
refs = set()
for p in glob.glob(os.path.join(root, "brief-*.html")) + [path]:
    refs |= set(re.findall(r"images/([^\"']+\.png)", io.open(p, encoding="utf-8").read()))
removed = []
for p in glob.glob(os.path.join(root, "images", "*.png")):
    if os.path.basename(p) not in refs:
        os.remove(p); removed.append(os.path.basename(p))
print(f"paper-brief.html + brief-{date}.html written ({len(block)} block lines); ARCHIVE={keep}; pruned briefs={drop}; removed images={removed}")

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
