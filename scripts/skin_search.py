"""Europe PMC search for the FT skin-model follow-up (journal scope: unrestricted).

Usage:
  python scripts/skin_search.py -k "fibroblast AND contraction AND skin equivalent" -Y 5 -n 60
  python scripts/skin_search.py -q 'TITLE_ABS:"skin irritation" AND TITLE_ABS:"OECD"' -Y 10

-k builds a TITLE_ABS query from a plain phrase list; -q passes a raw Europe PMC query through.
Prints a ranked candidate list and writes the full records to <TEMP>/pf_skin/results.json.
Already-featured ids (skin-seen.json) are marked SEEN so they can be skipped.
"""
import argparse, datetime, io, json, os, re, sys, time, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OUT = os.path.join(os.environ.get("TEMP", "."), "pf_skin")


def load_seen():
    p = os.path.join(ROOT, "skin-seen.json")
    if not os.path.exists(p):
        return set()
    return set(json.load(io.open(p, encoding="utf-8-sig")).get("featured", []))


def build_query(phrases, years):
    """phrases: list of plain strings -> TITLE_ABS:"..." joined by AND."""
    parts = []
    for ph in phrases:
        ph = ph.strip()
        if not ph:
            continue
        if any(op in ph for op in (" OR ", " AND ", ":")):
            parts.append("(%s)" % ph)
        else:
            parts.append('TITLE_ABS:"%s"' % ph)
    q = " AND ".join(parts)
    if years:
        y0 = datetime.date.today().year - years + 1
        q += " AND (FIRST_PDATE:[%d-01-01 TO 3000-12-31])" % y0
    return q


def search(query, n):
    got, cursor, out = 0, "*", []
    while got < n:
        params = {"query": query, "format": "json", "resultType": "core",
                  "pageSize": str(min(100, n - got)), "cursorMark": cursor,
                  "sort": "P_PDATE_D desc"}
        url = API + "?" + urllib.parse.urlencode(params)
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, timeout=60) as r:
                    data = json.loads(r.read().decode("utf-8"))
                break
            except Exception as e:
                print("retry:", e, file=sys.stderr); time.sleep(4)
        else:
            break
        res = data.get("resultList", {}).get("result", [])
        if not res:
            break
        out += res
        got += len(res)
        nxt = data.get("nextCursorMark")
        if not nxt or nxt == cursor:
            break
        cursor = nxt
        time.sleep(0.4)
    return out


def norm(r):
    doi = (r.get("doi") or "").strip()
    pmid = (r.get("pmid") or "").strip()
    pid = doi or (("PMID:" + pmid) if pmid else (r.get("id") or ""))
    journal = (r.get("journalInfo", {}) or {}).get("journal", {}).get("title") or r.get("bookOrReportDetails", {}).get("publisher") or ""
    if (r.get("source") or "") == "PPR":
        journal = (r.get("publisher") or journal or "preprint") + " (preprint)"
    return {
        "id": pid, "doi": doi, "pmid": pmid, "pmcid": r.get("pmcid") or "",
        "title": re.sub(r"\s+", " ", r.get("title") or "").strip().rstrip("."),
        "authors": r.get("authorString") or "",
        "journal": journal,
        "date": (r.get("firstPublicationDate") or r.get("pubYear") or "")[:10],
        "year": r.get("pubYear") or "",
        "type": r.get("pubTypeList", {}).get("pubType", []) if isinstance(r.get("pubTypeList"), dict) else [],
        "oa": (r.get("isOpenAccess") == "Y"),
        "url": ("https://doi.org/" + doi) if doi else (
            "https://europepmc.org/article/%s/%s" % (r.get("source", "MED"), r.get("id", ""))),
        "abstract": re.sub(r"\s+", " ", r.get("abstractText") or "").strip(),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--keywords", help='semicolon-separated phrases, e.g. "fibroblast;contraction;skin equivalent"')
    ap.add_argument("-q", "--query", help="raw Europe PMC query (overrides -k)")
    ap.add_argument("-Y", "--years", type=int, default=5, help="restrict to the last N years (0 = no limit)")
    ap.add_argument("-n", "--max", type=int, default=60)
    ap.add_argument("--all", action="store_true", help="also list already-featured papers")
    a = ap.parse_args()

    if a.query:
        q = a.query
        if a.years:
            y0 = datetime.date.today().year - a.years + 1
            q += " AND (FIRST_PDATE:[%d-01-01 TO 3000-12-31])" % y0
    elif a.keywords:
        q = build_query(a.keywords.split(";"), a.years)
    else:
        ap.error("need -k or -q")

    print("QUERY:", q)
    recs = [norm(r) for r in search(q, a.max)]
    seen = load_seen()
    os.makedirs(OUT, exist_ok=True)
    with io.open(os.path.join(OUT, "results.json"), "w", encoding="utf-8") as f:
        json.dump(recs, f, ensure_ascii=False, indent=1)

    new = [r for r in recs if r["id"] not in seen]
    print("TOTAL %d (new %d) -> %s" % (len(recs), len(new), os.path.join(OUT, "results.json")))
    for r in recs:
        if not a.all and r["id"] in seen:
            continue
        flags = ("SEEN " if r["id"] in seen else "     ") + ("OA " if r["oa"] else "   ")
        rev = "REVIEW " if any("review" in str(t).lower() for t in r["type"]) else ""
        print("%s%s %s | %s | %s%s" % (flags, r["date"][:7], r["id"][:42].ljust(42),
                                       r["journal"][:34], rev, r["title"][:95]))


if __name__ == "__main__":
    main()
