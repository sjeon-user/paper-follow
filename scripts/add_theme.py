"""Add / refresh the per-issue theme box and archive labels in a brief HTML (arXiv or RSS).

Usage:
  python scripts/add_theme.py <kind> <date> <html> [<html> ...]     kind = arxiv | rss
  python scripts/add_theme.py --all                                  refresh every brief + snapshot from themes.json

Reads themes.json (registry: kind -> date -> {label, title, keywords, note}). Idempotent: injects CSS, the
<div id="theme">, `const BRIEF_THEME`, the theme renderer, converts ARCHIVE entries to {d, t} objects labelled from
the registry, and makes the archive renderer print "date (label)". CRLF-safe (files are stored with CRLF on Windows).
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "themes.json")

CSS = """  .theme{margin-top:14px;padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:var(--card);font-size:.86rem;line-height:1.7}
  .theme .tlabel{font-weight:700;color:var(--muted);margin-right:6px}
  .theme .ttitle{font-weight:650}
  .theme .kw{display:inline-block;background:var(--tag);color:var(--tagtext);font-size:.75rem;padding:2px 8px;border-radius:999px;margin:2px 4px 2px 0}
  .theme .tnote{color:var(--muted);font-size:.8rem;margin-top:2px}
"""
DIV = '    <div id="theme" class="theme" hidden></div>'
RENDER = """(function renderTheme(){
  const el = document.getElementById("theme");
  if(!el || typeof BRIEF_THEME === "undefined" || !BRIEF_THEME || !(BRIEF_THEME.title || (BRIEF_THEME.keywords||[]).length)) return;
  const kws = (BRIEF_THEME.keywords||[]).map(k=>`<span class="kw">${k}</span>`).join("");
  el.innerHTML = `<div><span class="tlabel">🔎 이번 회차 주제</span><span class="ttitle">${BRIEF_THEME.title||""}</span></div>`
    + (kws ? `<div><span class="tlabel">검색 키워드</span>${kws}</div>` : ``)
    + (BRIEF_THEME.note ? `<div class="tnote">※ ${BRIEF_THEME.note}</div>` : ``);
  el.hidden = false;
})();
"""

def load_registry():
    return json.load(io.open(REG, encoding="utf-8-sig"))

def js_str(s):
    return json.dumps(s, ensure_ascii=False)

def apply(kind, date, path, reg=None):
    reg = reg or load_registry()
    themes = reg.get(kind, {})
    prefix = "brief-" if kind == "arxiv" else "rss-brief-"
    src = io.open(path, encoding="utf-8", newline="").read()
    eol = "\r\n" if "\r\n" in src else "\n"
    lines = src.split(eol)

    def find(prefix_text):
        for i, l in enumerate(lines):
            if l.startswith(prefix_text):
                return i
        return -1

    # 1. CSS (before .archive rule)
    if not any(l.startswith("  .theme{") for l in lines):
        i = find("  .archive{")
        if i >= 0:
            lines[i:i] = CSS.rstrip("\n").split("\n")
    # 2. DIV right after the topnav line
    if not any('id="theme"' in l for l in lines):
        i = find('    <div class="topnav">')
        if i >= 0:
            lines.insert(i + 1, DIV)
    # 3. BRIEF_THEME const (after BRIEF_DATE)
    th = themes.get(date, {})
    theme_line = "const BRIEF_THEME = " + json.dumps({"title": th.get("title", ""), "keywords": th.get("keywords", []), "note": th.get("note", "")}, ensure_ascii=False) + ";"
    i = find("const BRIEF_THEME = ")
    if i >= 0:
        lines[i] = theme_line
    else:
        i = find("const BRIEF_DATE = ")
        if i >= 0:
            lines[i + 1:i + 1] = ["/* 이번 회차 주제·검색 키워드 (themes.json에서 채움) */", theme_line]
    # 4. ARCHIVE -> {d, t} objects labelled from the registry
    i = find("const ARCHIVE = [")
    if i >= 0:
        dates, seen = [], set()
        for d in re.findall(r'"(\d{4}-\d{2}-\d{2}[a-z]?)"', lines[i]):
            if d not in seen:
                seen.add(d); dates.append(d)
        lines[i] = "const ARCHIVE = [" + ", ".join("{d:%s, t:%s}" % (js_str(d), js_str(themes.get(d, {}).get("label", ""))) for d in dates) + "];"
    # 5. archive renderer prints "date (label)" for object entries
    old_map = ("? list.map((d,i)=>`<a class=\"${i===0?'cur':''}\" href=\"" + prefix + "${d}.html\">${d}</a>`).join(\"\")")
    new_map = ('? list.map((x,i)=>{const d=(typeof x==="string")?x:x.d; const t=(typeof x==="string")?"":(x.t||""); '
               'return `<a class="${i===0?\'cur\':\'\'}" href="' + prefix + '${d}.html">${d}${t?` (${t})`:``}</a>`}).join("")')
    for k, l in enumerate(lines):
        if old_map in l:
            lines[k] = l.replace(old_map, new_map)
    # 6. theme renderer before the archive renderer
    if not any("renderTheme" in l for l in lines):
        i = find("(function renderArchive(){")
        if i >= 0:
            lines[i:i] = RENDER.rstrip("\n").split("\n") + [""]
    out = eol.join(lines)
    if out != src:
        io.open(path, "w", encoding="utf-8", newline="").write(out)
    return th.get("label", ""), out != src

def main():
    args = sys.argv[1:]
    reg = load_registry()
    if args and args[0] == "--all":
        jobs = []
        for p in glob.glob(os.path.join(ROOT, "brief-*.html")):
            jobs.append(("arxiv", re.search(r"brief-(\d{4}-\d{2}-\d{2}[a-z]?)\.html$", p).group(1), p))
        for p in glob.glob(os.path.join(ROOT, "rss-brief-*.html")):
            jobs.append(("rss", re.search(r"rss-brief-(\d{4}-\d{2}-\d{2}[a-z]?)\.html$", p).group(1), p))
        for kind, cur in (("arxiv", "paper-brief.html"), ("rss", "rss-brief.html")):
            path = os.path.join(ROOT, cur)
            d = re.search(r'^const BRIEF_DATE = "(\d{4}-\d{2}-\d{2}[a-z]?)', io.open(path, encoding="utf-8").read(), re.M)
            jobs.append((kind, d.group(1) if d else "", path))
    else:
        kind, date, files = args[0], args[1], args[2:]
        jobs = [(kind, date, f) for f in files]
    for kind, date, path in jobs:
        label, changed = apply(kind, date, path, reg)
        print(f"{'updated' if changed else 'ok     '} {os.path.basename(path):32s} {kind} {date} label={label!r}")

if __name__ == "__main__":
    main()
