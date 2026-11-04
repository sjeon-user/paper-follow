"""Fetch a representative figure (Figure 1) for Open Access papers via Europe PMC / PMC.

Usage: python scripts/skin_figure.py --ids "PMC13569832,PMC12875335" [--outdir skin-img]

For each PMCID: reads the Europe PMC fullTextXML, takes the first <fig> graphic, and tries the
known image hosts in order. Writes <outdir>/<PMCID>.png and prints the figure caption so the
caller can check it. Papers that are not Open Access have no retrievable figure - leave image "".
"""
import argparse, io, os, re, sys, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
UA = {"User-Agent": "Mozilla/5.0 (paper-follow figure fetch)"}
XML = "https://www.ebi.ac.uk/europepmc/webservices/rest/%s/fullTextXML"
HOSTS = [
    "https://europepmc.org/articles/%s/bin/%s",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/%s/bin/%s",
    "https://pmc.ncbi.nlm.nih.gov/articles/%s/bin/%s",
]
EXTS = [".jpg", ".png", ".gif", ".jpeg", ""]


def get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def first_figure(pmcid):
    """-> (graphic basename, caption) of the first <fig> in the full text, or (None, '')."""
    try:
        xml = get(XML % pmcid).decode("utf-8", "ignore")
    except Exception as e:
        print("  XML FAIL:", e)
        return None, ""
    m = re.search(r"<fig\b.*?</fig>", xml, re.S)
    if not m:
        return None, ""
    fig = m.group(0)
    g = re.search(r'<graphic[^>]*xlink:href="([^"]+)"', fig)
    cap = re.sub(r"<[^>]+>", " ", re.search(r"<caption>.*?</caption>", fig, re.S).group(0)) if "<caption>" in fig else ""
    return (g.group(1) if g else None), re.sub(r"\s+", " ", cap).strip()


def download(pmcid, base, outdir):
    for host in HOSTS:
        for ext in EXTS:
            name = base if base.lower().endswith(tuple(e for e in EXTS if e)) else base + ext
            url = host % (pmcid, name)
            try:
                data = get(url, 90)
            except Exception:
                continue
            if len(data) < 8000:
                continue
            dst = os.path.join(outdir, pmcid + ".png")
            with open(dst, "wb") as f:
                f.write(data)
            return dst, url, len(data)
    return None, None, 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="comma-separated PMCIDs")
    ap.add_argument("--outdir", default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skin-img"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    for pmcid in [x.strip() for x in a.ids.split(",") if x.strip()]:
        print("=====", pmcid)
        base, cap = first_figure(pmcid)
        if not base:
            print("  NO FIGURE in full text (not OA or no <fig>) -> leave image \"\"")
            continue
        dst, url, n = download(pmcid, base, a.outdir)
        if dst:
            print("  -> %s (%d KB) from %s" % (dst, n // 1024, url))
        else:
            print("  DOWNLOAD FAILED for graphic %r -> leave image \"\"" % base)
        if cap:
            print("  caption:", cap[:300])


if __name__ == "__main__":
    main()
