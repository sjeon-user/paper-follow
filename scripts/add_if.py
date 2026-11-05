# -*- coding: utf-8 -*-
"""Append JCR 2024 JIF to the `venue` field of every skin-brief paper card."""
import io, os, re, glob, sys

ROOT = r"C:\Users\KIMM\Desktop\2026\연구 행정 스킬화\2026.07.22 physical AI 논문 팔로우업"

# JCR 2024 Journal Impact Factor. None = 수록되지 않거나 출처 간 불일치가 커서 넣지 않음.
IF = {
 "Advanced Science": 14.1,
 "Theranostics": 12.4,
 "Science Advances": 11.7,
 "Experimental & Molecular Medicine": 9.5,
 "Acta Biomaterialia": 9.7,
 "Royal Society Open Science": 2.9,
 "Cellular & Molecular Biology Letters": 9.2,
 "Advanced Healthcare Materials": 10.0,
 "Materials Today Bio": 8.7,
 "ACS Applied Materials & Interfaces": 8.3,
 "Biofabrication": 8.2,
 "International Journal of Biological Macromolecules": 7.7,
 "Stem Cell Research & Therapy": 7.1,
 "Journal of Tissue Engineering": 6.7,
 "International Journal of Nanomedicine": 6.6,
 "Lab on a Chip": 6.1,
 "Biomaterials Advances": 5.8,
 "ACS Biomaterials Science & Engineering": 5.4,
 "Colloids and Surfaces B": 5.4,
 "Cells": 5.1,
 "International Journal of Molecular Sciences": 4.9,
 "Journal of Functional Biomaterials": 4.8,
 "Polymers": 4.7,
 "The American Journal of Pathology": 4.7,
 "ACS Applied Bio Materials": 4.6,
 "Gels": 4.6,
 "Frontiers in Toxicology": 4.6,
 "Frontiers in Bioengineering and Biotechnology": 4.3,
 "J Biomed Mater Res A": 3.9,
 "Scientific Reports": 3.9,
 "Bioengineering": 3.8,
 "ACS Omega": 3.7,
 "Tissue Engineering Part A": 3.6,
 "Regenerative Therapy": 3.6,
 "Biotechnology and Bioengineering": 3.5,
 "Experimental Dermatology": 3.5,
 "Biomimetics": 3.4,
 "J Biomed Mater Res B Appl Biomater": 3.4,
 "J Mech Behav Biomed Mater": 3.3,
 "Adipocyte": 3.3,
 "Materials": 3.1,
 "Journal of Tissue Engineering and Regenerative Medicine": 3.1,
 "Annals of Biomedical Engineering": 3.0,
 "Journal of Tissue Viability": 2.4,
 "Journal of Visualized Experiments": 1.2,
}

# JIF가 없거나 신뢰할 만한 값을 확인하지 못한 저널 → 사유를 그대로 표기
NOTE = {
 "Biomaterials and Biosystems": "IF 미수재",
 "Biomedical Materials": "IF 미확인",
 "Journal of Burn Care & Research": "IF 미확인",
 "BioMed Research International": "IF 없음·JCR 제외",
 "Mutation Research Genetic Toxicology": "IF 미확인",
 "JID Innovations": "IF 미확인",
 "FASEB BioAdvances": "IF 미확인",
 "Progress in Biomaterials": "IF 미확인",
 "Giornale Italiano di Dermatologia e Venereologia": "IF 미확인",
 "Advanced Biosystems": "IF 없음·폐간",
 "Journal of Biomedical Nanotechnology": "IF 없음·폐간",
 "Materials Science & Engineering C": "IF 없음·개명",
 "Handbook of Experimental Pharmacology": "IF 없음·단행본",
 "bioRxiv": "IF 없음·프리프린트",
}

def base(venue):
    """Strip ' · YYYY' and any trailing parenthetical to recover the journal name."""
    s = venue
    s = re.sub(r"\s*\([^()]*\)\s*$", "", s)          # trailing (Elsevier, OA)
    s = re.sub(r"\s*[·•]\s*\d{4}.*$", "", s)          # ' · 2024'
    s = re.sub(r"\s*\([^()]*\)\s*$", "", s)          # a second trailing parenthetical
    return s.strip()

def tag(venue):
    if re.search(r"IF\s", venue):                     # already annotated
        return None
    b = base(venue)
    if b in IF:
        return "IF %.1f" % IF[b]
    if b in NOTE:
        return NOTE[b]
    for k, v in IF.items():                           # prefix fallback
        if b.startswith(k):
            return "IF %.1f" % v
    for k, v in NOTE.items():
        if b.startswith(k):
            return v
    return None

def patch(venue, unknown):
    t = tag(venue)
    if t is None:
        if not re.search(r"IF\s", venue):
            unknown.add(base(venue))
        return venue
    if venue.rstrip().endswith(")"):
        return re.sub(r"\)\s*$", ", %s)" % t, venue.rstrip())
    return venue.rstrip() + " (%s)" % t

dry = "--apply" not in sys.argv
unknown = set()
changed = 0
files = sorted(glob.glob(os.path.join(ROOT, "skin-brief*.html")))
for f in files:
    s = io.open(f, encoding="utf-8").read()
    n = [0]
    def repl(m):
        new = patch(m.group(1), unknown)
        if new != m.group(1):
            n[0] += 1
        return 'venue: "%s"' % new
    # only inside the PAPERS array: venue lines are indented with 4 spaces
    s2 = re.sub(r'venue:\s*"([^"]+)"', repl, s)
    if n[0]:
        changed += n[0]
        if not dry:
            io.open(f, "w", encoding="utf-8").write(s2)
    print("%-34s %3d" % (os.path.basename(f), n[0]))
print("TOTAL venue fields patched:", changed, "(dry run)" if dry else "(written)")
if unknown:
    print("UNMAPPED:")
    for u in sorted(unknown):
        print("   ", u)
