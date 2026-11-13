# 액체 핸들링·신개념 파이펫 논문 팔로우업 설정 (liquid-config)

`skin-config.md`·`cocult-config.md`의 자매 설정입니다. 코워크(Claude)는 이 파일과
`liquid-keywords.md`를 읽고 `liquid-brief.html`을 채웁니다.

## 1. 큰 방향
점도 대응, 기포 대응, 신개념 파이펫·액체 핸들러. 특히 **AI·폐루프 제어**와 **로봇 기술**이 들어간 것을 우선합니다.
문제 분류와 키워드 일정은 **`liquid-keywords.md`**에 있습니다.

## 2. 검색 소스 — 세 갈래를 반드시 병행
이 주제는 한 DB로 덮이지 않습니다.
1. **Europe PMC** (`scripts/skin_search.py`) — SLAS Technology, Lab on a Chip, Analytical Chemistry, HardwareX, bioRxiv
2. **arXiv API** (`http://export.arxiv.org/api/query`) — 로봇·비전·강화학습 쪽 (cs.RO, cs.CV)
3. **웹 검색** — Digital Discovery 등 화학 자동화 저널과 ChemRxiv는 Europe PMC에 **색인되지 않습니다.**
   점도 대응 핵심 논문이 여기 있으므로 매 회차 한두 번은 웹 검색으로 보충합니다.

저널·IF·출판사로 거르지 않습니다. 프리프린트는 `venue`에 명시합니다.

## 3. 최근 기준
기본 **최근 5년**. 압력 감시·체적 검증처럼 원전이 오래된 주제는 10년까지 허용합니다.

## 4. 선별
- 매회 최대 10편. `liquid-seen.json`의 `featured`에 있는 id(DOI 또는 `arXiv:번호`)는 제외합니다.
- **액체 핸들링 기술 자체가 주제**여야 합니다. 파이펫을 도구로 쓴 분석법 논문(팁 고상추출 등)은 제외합니다.
- 임상 용어 혼입에 주의: aspiration(흡인성 폐렴·세침흡인), dispensing(조제·투약)은 걸러냅니다.
- **정량 결과가 있는 논문 우선**: 점도(cP·mPa·s), 체적 오차(%), CV(%), 검출 정확도, 성공률.
- 논문에 없는 수치를 지어내지 않습니다. 초록에서 확인되지 않는 내용은 쓰지 않습니다.

## 5. 대표 그림
`skin-config.md` 5번과 동일 — Figure 1 캡션 우선, 없으면 "그림 설명(초록 기반 요약)"으로 명시. 우회 수집 금지.

## 6. 요약 · 평가
- **배경·기존 문제** 2~3문장 / **해결·방법과 결과** 2~3문장, 존댓말, 사실 위주
- 별 5점(0.5 단위) + 근거 한 줄
- `solution` 마지막 문장에 **이 팔로우업의 관심사(점도·기포·AI 폐루프·로봇)와의 관련성**을 한 줄로 적습니다.

## 6-1. IF 표기
`scripts/add_if.py` (skin·cocult·liquid 공용). `--apply` 없이 돌리면 미리보기.
JCR 미수재·불확실한 저널은 숫자를 지어내지 않고 사유를 적습니다. arXiv는 `IF 없음·프리프린트`.

## 7. 출력
- `liquid-brief.html` — `BRIEF_DATE`, `BRIEF_THEME`, `ARCHIVE`, `PAPERS`만 갱신. `topics[0]`은 계층 라벨(`A.`~`E.`)
- `themes.json`의 **`liquid`** 항목에 회차 등록 → `python scripts/splice_liquid.py <날짜> <block.js>`
- `liquid-seen.json` 갱신, 음성 대본은 생성하지 않습니다.

## 8. 보관
스냅샷 `liquid-brief-<날짜>.html`, 최신 30개 유지, 고아 `liquid-img/*.png` 삭제.

## 9. 공유
- 공개 주소: https://sjeon-user.github.io/paper-follow/liquid-brief.html
- 커밋 메시지: `liquid-brief: <날짜> <label> (<편수>편)`
- **push는 사용자가 직접 실행합니다** (자동 승인에서 차단됨). 커밋까지 해 두고 push를 요청합니다.
