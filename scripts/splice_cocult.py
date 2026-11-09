"""Fill cocult-brief.html: BRIEF_DATE / ARCHIVE / PAPERS, snapshot to cocult-brief-<date>.html, keep 30,
then delete cocult-img/*.png no longer referenced by any remaining snapshot.

Usage: python scripts/splice_cocult.py <date> <block.js> [<archive label>]
"""
import glob, io, os, re, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
date = sys.argv[1]
label = sys.argv[3] if len(sys.argv) > 3 else date
block = [l.rstrip("\r") for l in io.open(sys.argv[2], encoding="utf-8").read().rstrip("\r\n").split("\n")]

path = os.path.join(root, "cocult-brief.html")
src = io.open(path, encoding="utf-8", newline="").read()
eol = "\r\n" if "\r\n" in src else "\n"
lines = src.split(eol)

def idx(prefix):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            return i
    raise SystemExit("anchor not found: " + prefix)

# archive list = existing snapshots + today, newest first, max 30
snaps = sorted({re.search(r"cocult-brief-(\d{4}-\d{2}-\d{2}[a-z]?)\.html$", p).group(1)
                for p in glob.glob(os.path.join(root, "cocult-brief-*.html"))} | {date}, reverse=True)
KEEP = 30
keep, drop = snaps[:KEEP], snaps[KEEP:]

lines[idx("const BRIEF_DATE")] = f'const BRIEF_DATE = "{label}";'
lines[idx("const ARCHIVE")] = "const ARCHIVE = [" + ", ".join(f'"{d}"' for d in keep) + "];"
i = idx("const PAPERS = [")
j = idx("/* ====== 여기까지 ====== */")
lines = lines[:i] + block + lines[j:]
out = eol.join(lines)
for name in ("cocult-brief.html", f"cocult-brief-{date}.html"):
    with io.open(os.path.join(root, name), "w", encoding="utf-8", newline="") as f:
        f.write(out)
for d in drop:
    os.remove(os.path.join(root, f"cocult-brief-{d}.html"))

# orphan figure cleanup (cocult-img/ only)
refs = set()
for p in glob.glob(os.path.join(root, "cocult-brief-*.html")) + [path]:
    refs |= set(re.findall(r"cocult-img/([^\"']+\.png)", io.open(p, encoding="utf-8").read()))
removed = []
for p in glob.glob(os.path.join(root, "cocult-img", "*.png")):
    if os.path.basename(p) not in refs:
        os.remove(p); removed.append(os.path.basename(p))

print(f"cocult-brief.html + cocult-brief-{date}.html written ({len(block)} block lines); "
      f"ARCHIVE={keep}; pruned={drop}; removed images={removed}")

# theme box + archive labels from themes.json (see scripts/add_theme.py)
sys.path.insert(0, os.path.join(root, "scripts"))
import add_theme
for _name in ("cocult-brief.html", f"cocult-brief-{date}.html"):
    _label, _ = add_theme.apply("cocult", date, os.path.join(root, _name))
if not _label:
    print(f"WARNING: themes.json has no 'cocult' entry for {date} - add it and re-run to fill the theme box")
else:
    print(f"theme applied: {_label}")
