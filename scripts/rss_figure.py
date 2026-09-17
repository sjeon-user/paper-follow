"""Extract a representative figure (Figure 1 preferred) from RSS proceedings PDFs.
Usage: python scripts/rss_figure.py --ids rss22/p001,rss22/p045 [--outdir rss-img] [--pages 3]
Writes <outdir>/<volume>-<num>.png and prints the strategy used per paper.
Strategies, in order: (1) render the region between the header/body text above and the 'Fig. 1' caption, within the
caption's column - the top edge is anchored to the figure's own graphics (images + vector drawings) so author lines or
footnotes right above the figure are excluded while labels inside the figure are kept; (2) raster panel(s) sitting just
above the caption, clipped to the caption's column; (3) largest sufficiently big raster image on the searched pages.
If none applies, no file is written and the paper is reported as NO FIGURE (leave image "").
"""
import argparse, os, sys, urllib.request
import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = "https://www.roboticsproceedings.org"
MIN_W, MIN_H = 220, 120   # points; a single column in the RSS template is ~252 pt wide

def fetch(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 10_000:
        return dst
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (paper-follow figure fetch)"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dst, "wb") as f:
        f.write(r.read())
    return dst

def find_caption(page):
    for b in page.get_text("blocks"):
        t = b[4].strip().lower().replace("\n", " ")
        if t.startswith(("fig. 1", "figure 1", "fig.1", "figure1")) and not t.startswith(("fig. 10", "figure 10", "fig. 11", "figure 11", "fig. 12", "figure 12")):
            return fitz.Rect(b[:4]), b[4].strip().replace("\n", " ")
    return None, ""

def raster_candidates(page):
    out = []
    for im in page.get_images(full=True):
        xref = im[0]
        for r in page.get_image_rects(xref):
            if r.width >= 60 and r.height >= 40:
                out.append((xref, r))
    return out

def overlaps_x(a, b):
    return a.x0 < b.x1 and a.x1 > b.x0

def graphics_top(page, col, cap):
    """Topmost y of images/drawings that belong to the figure above the caption (within its column)."""
    ys = []
    for _, r in raster_candidates(page):
        if r.y1 <= cap.y0 + 8 and overlaps_x(r, cap) and r.y0 >= page.rect.y0 + 20:
            ys.append(r.y0)
    for d in page.get_drawings():
        r = d.get("rect")
        if r is None or r.is_empty:
            continue
        if r.width * r.height < 100 or r.height < 2:      # skip hairlines / rules
            continue
        if r.y1 <= cap.y0 + 8 and r.y0 >= page.rect.y0 + 20 and overlaps_x(r, cap):
            ys.append(r.y0)
    return min(ys) if ys else None

def extract(doc, out_path, pages):
    for pno in range(min(pages, doc.page_count)):
        page = doc[pno]
        cap, cap_text = find_caption(page)
        if cap is None:
            continue
        col = fitz.Rect(cap.x0 - 6, page.rect.y0, cap.x1 + 6, page.rect.y1)  # the caption's column span
        # (1) region between text above the figure and the caption
        gtop = graphics_top(page, col, cap)
        top, found = None, False
        for b in page.get_text("blocks"):
            bb = fitz.Rect(b[:4]); txt = b[4].strip()
            if not (bb.y1 <= cap.y0 - 10 and overlaps_x(bb, cap)) or txt.lower().startswith(("fig", "figure")):
                continue
            is_header = gtop is not None and bb.y1 <= gtop + 3      # text entirely above the figure graphics
            is_body = len(txt) > 80 and (gtop is None or bb.y0 >= cap.y0 - 1 or bb.y1 <= gtop + 3)
            if is_header or is_body:
                top, found = (bb.y1 if top is None else max(top, bb.y1)), True
        if found:
            region = fitz.Rect(col.x0, top + 4, col.x1, cap.y0 - 2) & page.rect
            if region.height >= MIN_H * 0.6 and region.width >= MIN_W and region.height <= page.rect.height * 0.7:
                page.get_pixmap(clip=region, dpi=200).save(out_path)
                return f"p{pno+1}: rendered region above Fig.1 caption", cap_text
        # (2) raster panels directly above the caption, clipped to the caption's column
        above = [r for _, r in raster_candidates(page) if r.y1 <= cap.y0 + 8 and cap.y0 - r.y1 < 60 and overlaps_x(r, cap)]
        if above:
            u = fitz.Rect(above[0])
            for r in above[1:]:
                u |= r
            u = fitz.Rect(max(u.x0, col.x0), u.y0, min(u.x1, col.x1), u.y1)
            if u.width >= MIN_W and u.height >= MIN_H * 0.6:
                page.get_pixmap(clip=u, dpi=200).save(out_path)
                return f"p{pno+1}: raster panels above Fig.1 caption", cap_text
    # (3) largest big raster on the searched pages
    best = None
    for pno in range(min(pages, doc.page_count)):
        for _, r in raster_candidates(doc[pno]):
            area = r.width * r.height
            if best is None or area > best[0]:
                best = (area, pno, r)
    if best and best[2].width >= MIN_W and best[2].height >= MIN_H:
        doc[best[1]].get_pixmap(clip=best[2], dpi=200).save(out_path)
        return f"p{best[1]+1}: largest raster image (fallback)", ""
    return None, ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="comma-separated, e.g. rss22/p001,rss22/p045")
    ap.add_argument("--outdir", default="rss-img")
    ap.add_argument("--pages", type=int, default=3, help="how many leading pages to search for Fig. 1")
    ap.add_argument("--tmp", default=os.path.join(os.environ.get("TEMP", "."), "rss_pdf"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True); os.makedirs(a.tmp, exist_ok=True)
    for pid in [s.strip() for s in a.ids.split(",") if s.strip()]:
        vol, num = pid.split("/")
        out = os.path.join(a.outdir, f"{vol}-{num}.png")
        try:
            pdf = fetch(f"{BASE}/{vol}/{num}.pdf", os.path.join(a.tmp, f"{vol}-{num}.pdf"))
            doc = fitz.open(pdf)
            how, cap = extract(doc, out, a.pages)
            if how is None:
                if os.path.exists(out):
                    os.remove(out)
                print(f"{pid}: NO FIGURE found in first {a.pages} pages -> leave image \"\"")
                continue
            pix = fitz.Pixmap(out)
            print(f"{pid}: {how} -> {out} ({pix.width}x{pix.height}, {os.path.getsize(out)//1024} KB)")
            if cap:
                print(f"    caption: {cap[:220]}")
        except Exception as e:
            print(f"{pid}: FAIL {e}")

if __name__ == "__main__":
    main()
