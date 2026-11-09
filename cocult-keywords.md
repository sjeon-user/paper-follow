# 구획 배지 라인·시간차 공배양 제어 — 문제 분류 · 키워드 일정 (cocult-keywords)

`cocult-config.md`의 자매 파일입니다. **무엇을 문제로 보고 어떤 순서로 팔로우업할지**를 정의합니다.
코워크(Claude)는 아래 일정에서 **키워드 1개**를 꺼내 `cocult-brief.html`을 채웁니다.

출처: `261109 인공피부 난제정의·해결전략·역할분담 초안` (2026-11-09), 세부 난제 **S4**,
핵심기술 4 「생체재료·공배양 하드웨어 — 구획 배지 라인·시간차 공배양 스케줄링 제어기」.

---

## 0. 출발 문제 진술 (Problem statement)

> 대면적 인공피부는 **구획마다 요구하는 배양 조건이 서로 충돌**한다.
> 표피는 **기중(ALI)·고Ca²⁺·무혈청**을 요구하고, 진피 혈관은 **액상 관류·VEGF·전단 1–5 dyn/cm²**를 요구하며,
> 피하는 **지방 분화 배지**를 요구한다. 게다가 각 구획의 **세포 투입 시점이 서로 다르다**(D−10 ~ D8).
> 한 가지 배지를 한 시점에 공급하는 기존 공정으로는 이 상충을 해소할 수 없다.
>
> → **구획별 독립 배지 라인 + 액위·유량 제어 + 투입·전환 스케줄**을 장비가 결정하는
> **시간차 공배양 스케줄링 제어기**가 필요하다.

이 진술은 **세 축**으로 나뉩니다. 팔로우업은 축별로 끊어서 봅니다.

```
[A] 구획 분리 — 서로 다른 배지를 섞이지 않게 나누는 일
      ├ 기중(ALI) ↔ 액상 관류의 계면 유지
      ├ 2구획/3구획 인서트·칩 구조
      ├ 구획 간 누수·크로스토크 차단
      └ 액위(liquid level) 제어

[B] 배지 조성 상충 — 같은 조직 안에서 서로 다른 요구를 맞추는 일
      ├ Ca²⁺ 단계 상승 (표피 분화) vs 내피 요구
      ├ 혈청(FCS 5→2→0%) 단계 축소
      ├ VEGF·성장인자 구획 한정 전달
      └ 공통 배지(common medium) 탐색 — 상충을 피하는 반대 전략

[C] 시간차·스케줄 — 언제 넣고 언제 바꾸는가
      ├ 세포 투입 시점 분리 (sequential seeding)
      ├ ALI 전환 시점 최적화
      ├ 배지 교환 주기·관류 램프업
      └ 폐루프 제어 (센서 → 모델 → 스케줄 갱신)

[D] 장비·제어 구현 — 위 셋을 기계로 만드는 일
      ├ 다채널 펌프·밸브·유량 제어
      ├ 관류 베드·바이오리액터 하드웨어
      ├ 재순환·부산물 회수 관망
      └ 온라인 계측 포트와 공정 로그
```

**주의(사실 확인 필요)**: 피부 분야만으로는 사례가 부족할 수 있습니다.
간–신장·장–간 등 **멀티장기 칩(MPS)** 분야가 '구획별 배지 상충'과 '공통 배지' 문제를
훨씬 먼저 다뤘으므로, D 계열·B 계열 회차에서는 **장기칩 문헌을 함께 봅니다**.
그 경우 태그에 `인접(MPS)`를 붙여 피부 원저와 구분합니다.

---

## 1. 일자별 키워드 일정 (하루 1개, 위에서부터 순서대로)

`done` 열에 수행 날짜를 적습니다. 빈 칸이면 아직 안 한 회차이고, 다음 실행은 **빈 칸 중 가장 위**를 씁니다.

| # | 계층 | label (브리핑 표시용) | 핵심 검색어 | done |
|---|---|---|---|---|
| 1 | — | 총론: 구획 배지·시간차 제어 | 아래 네 축을 한 회차로 개관 (첫 회차) | 2026-11-10 (10편) |
| 2 | A | ALI ↔ 관류 계면 유지 | `air-liquid interface` + `perfusion` + `skin` / `co-culture` | |
| 3 | A | 2·3구획 인서트·칩 구조 | `dual-chamber` / `two-compartment` / `basolateral` + `skin equivalent` | |
| 4 | A | 구획 간 누수·크로스토크 | `crosstalk` / `leakage` / `compartment isolation` + `microphysiological` | |
| 5 | B | Ca²⁺ 단계 상승과 내피 상충 | `calcium switch` / `high calcium` + `keratinocyte differentiation` + `endothelial` | |
| 6 | B | 무혈청·혈청 단계 축소 | `serum reduction` / `serum-free` + `co-culture` + `skin` | |
| 7 | B | 공통 배지(common medium) 탐색 | `common medium` / `universal medium` / `medium compatibility` + `multi-organ` | |
| 8 | B | 성장인자 구획 한정 전달 | `VEGF gradient` / `compartment-specific delivery` + `vascularized skin` | |
| 9 | C | 순차 파종·투입 시점 | `sequential seeding` / `staggered seeding` / `timing of seeding` + `co-culture` | |
| 10 | C | ALI 전환 시점 최적화 | `ALI switch` / `submerged to air-liquid` + `timing` + `epidermis` | |
| 11 | C | 배지 교환 주기·관류 램프업 | `medium exchange frequency` / `flow ramp` / `shear conditioning` | |
| 12 | C | 폐루프 스케줄 갱신 | `closed-loop control` / `feedback control` + `bioreactor` + `tissue` | |
| 13 | D | 다채널 펌프·밸브 제어 | `multichannel perfusion` / `microvalve` / `programmable pump` + `organ-on-chip` | |
| 14 | D | 관류 베드·바이오리액터 | `perfusion bioreactor` + `skin` / `large-area tissue` | |
| 15 | D | 재순환·부산물 회수 | `recirculation` / `metabolite clearance` / `venous return` + `perfusion culture` | |
| 16 | D | 온라인 계측 포트·공정 로그 | `in-line sensor` / `online monitoring` (O₂·pH·lactate) + `bioreactor` | |
| 17 | E | 인접: 멀티장기 칩 배지 전략 | `multi-organ-on-chip` + `common medium` / `media formulation` | |
| 18 | E | 인접: 디지털 트윈·물리모델 | `digital twin` / `reaction-diffusion model` + `perfusion` + `tissue culture` | |

---

## 2. 분류 라벨 규칙

브리핑의 각 논문에는 **계층 라벨을 첫 번째 태그로** 붙입니다.
한 논문이 여러 축에 걸치면 가장 중심이 되는 축 하나를 고르고, 나머지는 본문에서 언급합니다.

- `A. 구획 분리`
- `B. 배지 조성 상충`
- `C. 시간차·스케줄`
- `D. 장비·제어 구현`
- `E. 인접 주제`

두 번째 이후 태그는 자유롭게 (모델 종류, 정량 지표, 핵심 수치 등).
피부가 아닌 장기칩 논문에는 `인접(MPS)` 태그를 함께 붙입니다.

---

## 3. 회차 운영 메모

- **하루 1키워드**가 원칙입니다. 같은 날 두 번 돌리면 날짜에 `b`, `c`를 붙입니다.
- 해당 키워드로 **조건에 맞는 논문이 5편 미만**이면 있는 만큼만 싣고 주제 메모(note)에 그 사실을 적습니다.
- **0편이면** 갱신하지 않고 그 키워드를 `done`에 `해당 없음`으로 표시한 뒤 다음으로 넘어갑니다.
- 사업 문서(`261109 …초안`)가 개정되면 0번 문제 진술과 일정표를 먼저 맞춥니다.

---

## 4. 1회차에서 확인된 것 (2026-11-10)

- **C축(시간차·스케줄)이 거의 비어 있습니다.** `sequential seeding / staggered / culture schedule`로 좁힌
  질의에서 **피부 공배양의 투입 시점을 변수로 비교한 논문을 찾지 못했습니다.**
  `10.1039/d5lc00606f`는 순차 파종을 쓰지만 순서만 기술하고 간격은 비교하지 않았고,
  시점을 실제 설계 변수로 다룬 것은 미생물 2구획 바이오리액터(`10.1007/s00449-024-03008-1`) 한 편뿐이었습니다.
  → 기획서의 '시간차 공배양 스케줄링 제어기'는 **선행 사례가 드문 영역**입니다. 신규성 근거로 쓸 수 있습니다.
- **B축은 반대 전략이 주류입니다.** 구획을 나누는 대신 **공통 배지로 상충을 회피**하는 쪽이고,
  3편 모두 멀티장기 칩 문헌이었습니다. `10.2144/fsoa-2019-0065`에서 네 조직 중 **신장만 실패**한 사실은
  공통 배지 전략의 한계를 보여 주므로, 우리 접근의 비교군으로 유용합니다.
- **성능 지표를 조심해야 합니다.** `10.1159/000476071`은 관류로 분화 표지(인볼루크린·필라그린·클라우딘1)는
  올랐지만 **장벽 기능은 개선되지 않았다**고 보고했습니다(저자 표현 "unexpectedly").
  제어기 성능을 정의할 때 분화 표지와 장벽을 분리해 평가해야 합니다.
- 다음 회차는 일정표 2번 **ALI ↔ 관류 계면 유지**입니다.
