# 구획 배지·시간차 공배양 제어 논문 팔로우업 설정 (cocult-config)

`follow-config.md`(arXiv)·`rss-config.md`(RSS)·`skin-config.md`(FT 피부)의 자매 설정입니다.
코워크(Claude)는 이 파일과 `cocult-keywords.md`를 읽고 `cocult-brief.html`을 채웁니다.

---

## 1. 큰 방향 (Direction)
대면적 인공피부의 **구획 간 배양조건 상충(S4)**을 장비·공정으로 푸는 문제.
문제 분류와 일자별 키워드는 **`cocult-keywords.md`**에 있습니다.
근거 문서: `261109 인공피부 난제정의·해결전략·역할분담 초안`, 핵심기술 4 (전 박사 담당안).

## 2. 검색 소스 (Source) — **저널 범위 제한 없음**
- **Europe PMC** REST API (주 소스). `scripts/skin_search.py`를 그대로 씁니다.
- 저널·임팩트팩터·출판사로 **거르지 않습니다.** 프리프린트도 포함하되 `venue`에 명시합니다.
- 피부 문헌만으로 부족하면 **멀티장기 칩(MPS)·조직공학 일반**으로 넓히되 `인접(MPS)` 태그를 붙입니다.

## 3. 최근 기준 (Recency)
- 기본 **최근 10년**. 공통 배지·순차 파종처럼 원전이 오래된 주제는 **15년**까지 허용합니다.

## 4. 선별 (Selection)
- 매회 **최대 10편**(특집 성격). 정규 회차는 5편도 가능합니다.
- `cocult-seen.json`의 `featured`에 있는 id는 **제외** → 같은 논문 반복 금지.
- 선별 기준: 그 회차 키워드가 **논문의 주제**여야 합니다. 단어만 스친 논문은 제외합니다.
- 가능하면 **정량 결과(유량 µL/min, 전단 dyn/cm², Ca²⁺ mM, 전환 시점 day, TEER)가 있는 논문**을 우선합니다.
- **`skin-seen.json`과는 별개 목록입니다.** FT 피부 브리핑에 이미 나온 논문이라도,
  이 주제의 관점에서 새로 읽을 가치가 있으면 다시 실을 수 있습니다. 단 본문에 그 사실을 적습니다.

## 5. 대표 그림 (Figure) — **설명문 우선**
`skin-config.md` 5번과 동일합니다. 이미지 호스트가 외부 요청을 막으므로
**Figure 1 설명문(caption)**을 기본으로 쓰고, 받을 수 없으면 초록 기반 한 줄 설명을
"그림 설명(초록 기반 요약)"으로 명시해 적습니다. **우회 수집은 하지 않습니다.**

## 6. 요약 · 평가 (Summary / Rating)
- **배경·기존 문제** 2~3문장 / **해결·방법과 결과** 2~3문장, 친절한 존댓말, 담백·사실 위주
- 별 5점(0.5 단위) = 논리 일관성 + 근거 견고함, 옆에 근거 한 줄
- 추가 규칙: **이 회차 문제 진술과의 관련성**을 `solution` 마지막 문장에 한 줄로 적습니다
  (예: "구획 분리는 보였지만 투입 시점을 변수로 다루지 않아 C 계층 근거는 비어 있습니다").

## 6-1. 저널 임팩트 팩터 (IF) 표기
`skin-config.md` 6-1번과 동일한 규칙·동일한 스크립트를 씁니다.
- `python scripts/add_if.py` → 미리보기 (UNMAPPED 확인) / `--apply` → 반영
- `scripts/add_if.py`는 `skin-brief*.html`과 `cocult-brief*.html`을 모두 처리합니다.
- JCR 미수재·출처 불일치 저널은 **숫자를 지어내지 않고** 사유를 적습니다.

## 7. 출력 (Output)
- `cocult-brief.html` — `BRIEF_DATE`, `BRIEF_THEME`, `ARCHIVE`, `PAPERS`만 갱신
  - `topics[0]`은 반드시 계층 라벨(`A.`~`E.`, `cocult-keywords.md` 2번)
- 회차 주제는 `themes.json`의 **`cocult`** 항목에 `{label, title, keywords, note}`로 먼저 등록합니다.
- `cocult-seen.json` — 소개한 id를 `featured`에 추가
- 음성 대본은 **생성하지 않습니다**.

## 8. 보관 (Archive)
- 회차 스냅샷 `cocult-brief-<날짜>.html` (루트, `cocult-img/` 상대경로 유지)
- **최신 30개만 유지**, 어디서도 참조되지 않는 `cocult-img/*.png`도 삭제
- 다른 브리핑(`brief-*`·`rss-brief-*`·`skin-brief-*`)과 **무관**하게 동작합니다.

## 9. 공유 (Publish)
- 공개 주소: https://sjeon-user.github.io/paper-follow/cocult-brief.html
- 다른 브리핑 상단에 "🧪 공배양 제어" 링크 추가 (이미 반영)
- 커밋 메시지: `cocult-brief: <날짜> <label> (<편수>편)`

## 10. 실행 순서 (Runbook)
1. `cocult-keywords.md`에서 `done`이 빈 **가장 위 키워드**를 고른다
2. `python scripts/skin_search.py -k "<검색어>" -Y 10 -n 60` → 후보 목록
3. 후보 초록을 읽고 4번 기준으로 선별 (기소개 제외)
4. OA면 `python scripts/skin_figure.py --ids "<PMCID>"` → 캡션
5. `themes.json`의 `cocult`에 회차 등록
6. `python scripts/splice_cocult.py <날짜> <block.js>` → HTML 갱신 + 스냅샷 + 보관 정리
7. `python scripts/add_if.py --apply` → IF 표기
8. `cocult-seen.json`에 id 추가, `cocult-keywords.md`의 `done`에 날짜 기록
9. 커밋 · push
