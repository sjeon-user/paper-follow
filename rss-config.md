# RSS 학회 논문 팔로우업 설정 (rss-config)

`follow-config.md`(arXiv 브리핑)의 자매 설정입니다. 코워크(Claude)는 이 파일을 읽고,
**Robotics: Science and Systems(RSS) 최신 프로시딩**에서 논문을 골라 `rss-brief.html`을 채웁니다.
요약 형식·별점 기준·문투는 follow-config.md 7·7-1번과 동일합니다.

---

## 1. 소스 (Source)
- RSS 공식 온라인 프로시딩: https://www.roboticsproceedings.org/
- **최신 볼륨만** 대상 (예: RSS XXII = 2026, Sydney → `rss22/`). 새 볼륨이 올라오면 자동으로 그 볼륨으로 넘어갑니다.
- 볼륨 전체 목록(제목·저자·초록·DOI·PDF 링크)은 `rss-catalog.json`에 캐시합니다.
  `scripts\rss_catalog.ps1` 이 최신 볼륨을 감지해 필요할 때만(볼륨이 바뀌었거나 편수가 다를 때) 다시 수집합니다.

## 2. 선별 (Selection)
- 매회 **5편**, 카탈로그에서 **무작위** 추출 (`scripts\rss_pick.ps1 -N 5`)
- `rss-seen.json`의 `featured`에 있는 id(`rss22/p001` 형식)는 **제외** → 같은 논문을 두 번 소개하지 않음
- 주제 필터 없음 (학회 전체를 두루 보는 것이 목적). 남은 미소개 논문이 5편 미만이면 있는 만큼만, 0편이면 갱신 없이 종료.

## 3. 대표 그림 (Figure)
- 논문 PDF에서 **Figure 1**(캡션 "Fig. 1" 위 영역)을 추출: `python scripts\rss_figure.py --ids "rss22/p001,rss22/p045"`
- 저장 위치: `rss-img/<볼륨>-<번호>.png` (예: `rss-img/rss22-p001.png`)
- 추출 결과는 반드시 눈으로 확인. 개요/파이프라인/티저 그림이 아니면(로고·표·수식 조각 등) image를 `""`로 둠.

## 4. 요약 · 평가 (Summary / Rating)
- follow-config.md의 7번(배경·기존 문제 / 해결·방법과 결과, 친절한 존댓말, 담백·사실 위주)과
  7-1번(별 5점, 0.5 단위, 논리 일관성 + 근거 견고함, 근거 한 줄) 규칙을 그대로 적용
- 근거는 카탈로그의 초록(필요하면 PDF 본문)

## 5. 출력 (Output)
- `rss-brief.html` — `BRIEF_DATE`, `PAPERS`, `ARCHIVE`만 갱신 (HTML/CSS/렌더 스크립트는 그대로)
  - PAPERS 항목 필드: title, authors, rss_id, url, pdf, doi, date, venue, topics[], image, figcap, background, solution, rating, rating_reason
- **주제·검색 키워드 표기**: 회차마다 `themes.json`의 `rss` 항목에 `{label, title, keywords, note}`를 먼저 등록 → 상단 "🔎 이번 회차 주제" 박스(`BRIEF_THEME`)와 "지난 RSS 브리핑" 목록의 `날짜 (label)` 표기가 `scripts/add_theme.py`로 자동 채워짐. 무작위 회차는 label `무작위 N편`, 키워드 회차는 사용자가 준 키워드를 그대로 기록하고 note에 제외 조건·해당 논문 없음 등을 적음
- `rss-voice-script.md` — 한 편씩 소개하는 TTS 낭독 대본 (voice-script.md와 같은 구성·문체)
- `rss-seen.json` — 소개한 id를 `featured`에 추가

## 6. 보관 (Archive)
- 회차 스냅샷 `rss-brief-<날짜>.html` (루트에 저장, rss-img/ 상대경로 유지)
- `rss-brief-*.html`은 **최신 7개만 유지**, 오래된 것은 삭제
- 남은 `rss-brief-*.html`·`rss-brief.html` 어디서도 참조되지 않는 `rss-img/*.png`는 삭제
- `rss-brief.html`의 `ARCHIVE` = 현재 남아 있는 스냅샷 날짜(최신순, 최대 7개)
- arXiv 브리핑의 `brief-*.html`·`images/`·`keep*`는 이 정리와 **무관** (건드리지 않음)

## 7. 공유 (Publish)
- 공개 주소: https://sjeon-user.github.io/paper-follow/rss-brief.html
- arXiv 브리핑(`paper-brief.html`)·보관함(`keep.html`) 상단 "🏛 RSS 학회" 링크로 이동
- 커밋 메시지: `rss-brief: <날짜> (<편수>편)`
