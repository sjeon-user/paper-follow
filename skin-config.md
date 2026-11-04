# FT 피부 모델 논문 팔로우업 설정 (skin-config)

`follow-config.md`(arXiv)·`rss-config.md`(RSS)의 자매 설정입니다. 코워크(Claude)는 이 파일과
`skin-keywords.md`를 읽고 문헌 DB에서 논문을 골라 `skin-brief.html`을 채웁니다.

---

## 1. 큰 방향 (Direction)
FT(full-thickness, 전층) 인체 피부 모델의 **구조적 기하 불안정 → 분화·장벽 미흡 → 규제 적합성 미달**이라는
인과 사슬. 문제 분류와 일자별 키워드는 **`skin-keywords.md`**에 있습니다.

## 2. 검색 소스 (Source) — **저널 범위 제한 없음**
- **Europe PMC** REST API (주 소스). PubMed/MEDLINE + PMC + Agricola + 프리프린트(bioRxiv·medRxiv)를 함께 덮습니다.
  - 엔드포인트: `https://www.ebi.ac.uk/europepmc/webservices/rest/search`
  - API 키 불필요. `scripts/skin_search.py`가 호출합니다.
- 저널·임팩트팩터·출판사로 **거르지 않습니다.** 프리프린트도 포함하되 `venue`에 프리프린트임을 명시합니다.
- 리뷰 논문도 포함합니다(규제·검증 쟁점은 리뷰가 더 정확한 경우가 많음). 단 태그에 `review`를 붙입니다.

## 3. 최근 기준 (Recency)
- 기본 **최근 5년**(`-Y 5`). 규제(D 계열) 키워드는 TG 개정 이력을 봐야 하므로 **10년**까지 허용합니다.
- 고전 레퍼런스(FPCL 원전 등)는 회차 본문에서 인용만 하고 카드로는 싣지 않습니다.

## 4. 선별 (Selection)
- 매회 **최대 5편**. 조건에 맞는 논문이 적으면 있는 만큼만, 0편이면 갱신 없이 종료.
- `skin-seen.json`의 `featured`에 있는 id(DOI 우선, 없으면 `PMID:…`)는 **제외** → 같은 논문 반복 금지.
- 선별 기준: 그 회차 키워드가 **논문의 주제**여야 합니다. 초록에 단어만 한 번 스친 논문은 제외합니다.
- 가능하면 **정량 결과(수축률 %, TEER, 생존율 %, 두께 µm)가 있는 논문**을 우선합니다.

## 5. 대표 그림 (Figure) — **설명문 우선**
arXiv·RSS 브리핑과 달리 이 브리핑은 **그림 대신 Figure 1 설명문(caption)**을 기본으로 씁니다.

- `scripts/skin_figure.py --ids "PMC…"`가 Europe PMC 전문(fullTextXML)에서 **첫 번째 그림의 캡션**을 가져옵니다.
  → `figcap`에 넣으면 페이지가 파란 테두리 설명 상자로 렌더합니다.
- **이미지 파일은 대개 받을 수 없습니다.** PMC·Europe PMC의 이미지 호스트가 외부 요청을 403/404로 막습니다.
  스크립트는 시도 후 실패하면 조용히 넘어가고, 그때는 `image`를 `""`로 둡니다. **우회 수집은 하지 않습니다.**
- 예외적으로 이미지가 받아진 경우에만 `skin-img/<PMCID>.png`로 저장하고 `image`에 경로를 적되,
  반드시 눈으로 확인해 개요·구조 그림이 아니면 다시 `""`로 되돌립니다.
- 비(非)OA 논문은 캡션도 받을 수 없으므로 `figcap`을 비우거나, 초록에 근거해 **직접 쓴 한 줄 설명**을 넣고
  그 사실이 드러나도록 "그림 설명(초록 기반 요약)"처럼 적습니다.

## 6. 요약 · 평가 (Summary / Rating)
`follow-config.md` 7번·7-1번 규칙을 그대로 적용합니다.
- **배경·기존 문제** 2~3문장 / **해결·방법과 결과** 2~3문장, 친절한 존댓말, 담백·사실 위주
- 별 5점(0.5 단위) = 논리 일관성 + 근거 견고함, 옆에 근거 한 줄
- 추가 규칙: **이 회차 문제 진술과의 관련성**을 `solution` 마지막 문장에 한 줄로 적습니다
  (예: "수축률을 직접 보고했지만 장벽 기능 측정은 없어 C 계층 근거는 비어 있습니다").

## 7. 출력 (Output)
- `skin-brief.html` — `BRIEF_DATE`, `BRIEF_THEME`, `ARCHIVE`, `PAPERS`만 갱신 (HTML/CSS/렌더 스크립트는 그대로)
  - PAPERS 필드: title, authors, paper_id, url, doi, date, venue, topics[], image, figcap,
    background, solution, rating, rating_reason
  - `topics[0]`은 반드시 계층 라벨(`A.`~`E.`, `skin-keywords.md` 2번)
- 회차 주제는 `themes.json`의 `skin` 항목에 `{label, title, keywords, note}`로 먼저 등록합니다.
- `skin-seen.json` — 소개한 id를 `featured`에 추가
- 음성 대본은 **생성하지 않습니다** (arXiv·RSS와 동일).

## 8. 보관 (Archive)
- 회차 스냅샷 `skin-brief-<날짜>.html` (루트, `skin-img/` 상대경로 유지)
- **최신 30개만 유지**, 오래된 것은 삭제. 어디서도 참조되지 않는 `skin-img/*.png`도 삭제
- `brief-*.html`·`rss-brief-*.html`·`images/`·`rss-img/`·`keep*`는 이 정리와 **무관**

## 9. 공유 (Publish)
- 공개 주소: https://sjeon-user.github.io/paper-follow/skin-brief.html
- `paper-brief.html`·`rss-brief.html` 상단에 "🧫 FT 피부" 링크 추가
- 커밋 메시지: `skin-brief: <날짜> <label> (<편수>편)`

## 10. 실행 순서 (Runbook)
1. `skin-keywords.md`에서 `done`이 빈 **가장 위 키워드**를 고른다
2. `python scripts/skin_search.py -k "<검색어>" -Y 5 -n 60` → 후보 목록
3. 후보 초록을 읽고 4번 기준으로 최대 5편 선별 (기소개 제외)
4. OA면 `python scripts/skin_figure.py --ids "<id1>,<id2>"` → 그림, 눈으로 확인
5. `themes.json`의 `skin`에 회차 등록
6. `python scripts/splice_skin.py <날짜> <block.js> ` → HTML 갱신 + 스냅샷 + 보관 정리
7. `skin-seen.json`에 id 추가, `skin-keywords.md`의 `done`에 날짜 기록
8. 커밋 · push
