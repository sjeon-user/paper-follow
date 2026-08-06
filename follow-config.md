# 논문 팔로우업 설정 (follow-config)

이 파일은 "논문 팔로우업" 자동화의 **설정 파일**입니다.
코워크(Claude)는 이 파일을 읽고, 아래 조건대로 arXiv에서 최근 논문을 찾아
`paper-brief.html`을 채웁니다. 값을 바꾸면 다음 실행부터 반영됩니다.

---

## 1. 큰 방향 (Direction)
Physical AI

## 2. 세부 주제 (Topics) — 2026-08-06 개정, 2026-08-07 imitation learning 추가
**아래 6가지 주제만** 팔로우합니다. 여기에 해당하지 않는 논문은 아무리 좋아도 선별하지 않습니다.
(이전에 보던 egocentric · motion capture · 일반 robot arm · self-driving lab · 일반 VLA는
**의도적으로 제외**했습니다.)

1. **diffusion VLA** (확산 기반 Vision-Language-Action 모델)
   - 검색어: `("vision-language-action" 또는 "vision language action") AND "diffusion"`
   - 두 조건을 **동시에** 걸어야 합니다. `vision-language-action`만 쓰면 일반 VLA가 대량으로 딸려옵니다.
   - **일부러 뺀 단어**: `flow matching` — 사촌 격이지만 주제어가 '확산'이므로 제외했습니다.
     필요해지면 이 줄의 조건에 `OR abs:"flow matching"`을 추가하면 됩니다.
2. **diffusion policy** (확산 정책 — 확산모델 기반 로봇 행동 생성)
   - 검색어: `"diffusion policy"` (+ cat:cs.RO 또는 cs.LG)
3. **Universal Manipulation Interface (UMI)**
   - 검색어: `"universal manipulation interface"` 또는 (`"UMI"` + cat:cs.RO)
   - **주의**: 약어 `UMI`는 다른 분야에서도 쓰이므로 반드시 cs.RO 조건과 함께 씁니다.
4. **handheld gripper / retargeting** (핸드헬드 시연 수집 장치 + 모션·손 리타게팅)
   - 검색어: `"handheld gripper"` / `"hand-held gripper"` / `"portable gripper"` /
     `"handheld demonstration"` / `"handheld data collection"` / `"retargeting"`
     (+ cat:cs.RO 또는 cs.CV)
   - 둘 다 "사람 시연을 로봇으로 옮기는" 같은 목적이라 하나의 주제로 묶었습니다.
5. **robotic manipulation of transparent object / liquid** (투명 물체·액체의 로봇 조작)
   - 태그는 `transparent object`와 `liquid manipulation` 둘로 나뉘어 표시됩니다.
   - liquid: 액체 조작은 학계에서 굳어진 대표어가 없어, 과제 어휘를 묶어 검색합니다 —
     `pouring` / `liquid` / `sloshing` / `stirring` / `scooping` (+ cat:cs.RO).
     **일부러 뺀 단어**: `fluid`(항공·유체역학 논문이 대량으로 딸려옴),
     `granular`·`viscous`(모래 위 보행 등 *이동* 논문이 섞임 — 조작이 아님)
   - transparent: `transparent object` / `glass object` / `glass segmentation` /
     `non-Lambertian` / `glassware` (+ 로봇 맥락: cat:cs.RO 이거나 grasping·manipulation 언급)
   - **주의**: `transparent`만 단독으로 쓰면 안 됩니다. 로보틱스에서 이 단어는
     광학적 투명이 아니라 **설명가능성**(투명한 의사결정, transparent autonomy)을
     뜻하는 경우가 훨씬 많아 오탐이 대량 발생합니다.
     로봇 맥락 조건을 빼면 순수 렌더링·Gaussian splatting 논문이 밀려듭니다.
   - 주제 5는 "**조작**"이 핵심이므로, 초록에 grasp/manipulate/pick/robot 계열 표현이
     한 번도 없는 순수 인식 논문은 걸러 냅니다(스크립트의 `filter2`).
     단, 투명 물체는 깊이 센서 실패가 핵심 난점이라 깊이 복원·유리 분할처럼
     조작을 목표로 한 인식 논문은 그대로 포함됩니다.
6. **imitation learning** (모방학습 — 시연 기반 정책 학습) — 2026-08-07 추가
   - 검색어: `"imitation learning"` (+ cat:cs.RO)
   - 용어 자체가 명확해서 어휘 필터는 걸지 않았지만 범위가 넓은 주제라,
     반드시 cs.RO 조건과 함께 씁니다. 이 조건을 빼면 cs.LG의 강화학습·역강화학습
     이론 논문이 대량으로 딸려옵니다.
   - **일부러 뺀 단어**: `behavior cloning` / `learning from demonstration` —
     사실상 같은 뜻이지만, 2026-08-06에 줄여 놓은 범위가 다시 '일반 조작'으로
     넓어지는 것을 막기 위해 정확히 이 표현만 검색합니다.
     넓히고 싶으면 검색어에 `OR abs:"behavior cloning" OR abs:"learning from demonstration"`을
     추가하면 됩니다.
   - **감수하는 오탐**: cs.RO 안에도 자율주행·시각 내비게이션 정책 논문이 섞여 들어옵니다.
     거슬리면 주제 5처럼 조작 맥락 `filter2`를 걸면 됩니다.

## 3. 검색 소스 (Source)
- arXiv (주 대상 카테고리: cs.RO, cs.CV, cs.LG, cs.AI)

## 4. 최근 기준 (Recency)
- 최근 **60일** 이내에 arXiv에 처음 제출(submitted)된 논문

## 5. 선별 (Selection)
- 관련도 높은 순으로 정렬
- 최대 **6편** (조건에 맞는 논문이 그보다 적으면 있는 만큼만)
- 세부 주제가 한쪽으로 쏠리지 않도록 가능하면 다양하게
- 2026-08-06 주제 축소(+08-07 imitation learning 복구) 이후로는 하루 신규가 6편에 못 미치는 날이 정상입니다.
  **주제를 넓혀서 편수를 채우지 마세요.** 있는 만큼만 싣고, 0편이면 갱신 없이 종료합니다.

## 6. 대표 그림 (Figure)
- 각 논문에서 **대표 그림 1장** (보통 메인 개요/파이프라인 그림, Figure 1 우선)
- 이미지는 `images/` 폴더에 저장하고 HTML에서 상대경로로 참조

## 7. 요약 (Summary)
- 언어: **한국어**
- 구조: **두 부분으로 나눠서** 작성
  1) **배경 · 기존 문제** — 이 논문 이전에 어떤 문제/한계가 있었는지 (2~3문장)
  2) **해결 · 방법과 결과** — 저자들이 그것을 어떻게 풀었고 결과가 어땠는지 (2~3문장)
- 문투: 누군가에게 **설명/소개하듯 친절한 존댓말** (예: "기존에는 ~한 문제가 있었습니다", "저자들은 ~로 이를 해결했습니다")
- 톤: 담백하고 사실 위주 (과장 금지)

## 7-1. 평가 (Rating)
- 각 논문에 **별 5점** 부여 (0.5 단위 허용), 요약 아래 그래픽(별)로 표시
- 기준: **논문 전체 논리의 일관성 + 근거(실험·데이터·검증)의 견고함**
  (참신함/화제성이 아니라, 주장·방법·결과가 얼마나 탄탄히 뒷받침되는지)
- 참고 잣대: 벤치마크/실기기 검증 범위, 비교·소거(ablation)의 충실함, 한계의 정직한 서술
- 별점 옆에 **근거 한 줄**(왜 그 점수인지)을 함께 표기

## 8. 출력 (Output)
- `paper-brief.html`의 `PAPERS` 배열과 `BRIEF_DATE` 갱신
- `voice-script.md` — 논문을 한 편씩 소개하는 음성(TTS) 낭독용 대본 (숫자·기호는 말로 읽기 좋게 풀어서)
- 파일은 이 폴더에 저장

## 9. 공유 · 자동화 (Publish / Routine)
- GitHub Pages로 공개 → 폰·여러 PC에서 링크로 접근 (https://sjeon-user.github.io/paper-follow/)
- 매일 오전 10시 루틴으로 위 결과물 갱신 후 GitHub에 push

## 10. 보관 (Archive) — 최근 7일 누적
- 매일 최신본을 `brief-<날짜>.html`(예: brief-2026-07-21.html)로 스냅샷 저장 (루트에 두어 images/ 경로 유지)
- `brief-*.html`은 **최신 7일치만 유지**, 그보다 오래된 날짜 파일은 삭제
- 어떤 `brief-*.html`에서도 참조되지 않는 `images/*.png`는 함께 삭제(정리)
- `paper-brief.html`(=최신)/`index.html`은 항상 오늘치를 표시, 하단 "지난 브리핑" 목록에 최근 7일 링크
- 지난 날짜 전체 기록은 GitHub 커밋 히스토리에 남음

## 11. 보관함 (Keep) — 영구 보관, 7일 정리와 무관
사용자가 마음에 든 논문을 오래 남기고 싶을 때 쓰는 영구 보관함입니다.
- **입력**: `keep-list.md` — 사용자가 보관할 arXiv id를 한 줄에 하나씩 직접 적음
  (`#`/빈 줄 무시, `id · 메모` 형식으로 메모 첨부 가능)
- **출력**: `keep.html` — 보관함 페이지. 각 논문의 제목·저자·요약(배경/해결)·별점·대표 그림까지
  담아 렌더 (브리핑 PAPERS와 동일 형식의 `KEPT` 배열 + `note`/`kept_date` 선택 필드)
- **그림**: 보관 논문 그림은 `keep-img/<id>.png` 로 별도 저장 (images/ 정리와 분리)
- **동기화 규칙** (매 생성 시):
  - `keep-list.md`에 있으나 `keep.html`의 KEPT에 없는 id → 추가.
    데이터는 (a) 그날/현재 `brief-*.html`이나 이번 회차 요약에서 복사, 없으면 (b) arXiv에서 다시 수집해 요약/별점 재생성.
    그림은 `keep-img/<id>.png`로 저장(없으면 image "").
    `kept_date`는 처음 보관된 날짜로 기록(이후 유지).
  - `keep-list.md`에서 빠진 id → KEPT에서 제거하고 그 `keep-img/*.png`도 삭제.
- **정리 제외**: `keep.html`·`keep-list.md`·`keep-img/`는 10번의 7일 정리 대상이 **아님**(절대 삭제하지 않음).
- 최신 브리핑 페이지 상단의 "⭐ 보관함" 링크로 이동. 공개 주소: https://sjeon-user.github.io/paper-follow/keep.html
