# FT 피부 모델 문제 분류 · 키워드 일정 (skin-keywords)

`skin-config.md`의 자매 파일입니다. **무엇을 문제로 보고 어떤 순서로 팔로우업할지**를 정의합니다.
코워크(Claude)는 매일 아래 일정에서 **키워드 1개**를 꺼내 `skin-brief.html`을 채웁니다.

---

## 0. 출발 문제 진술 (Problem statement)

> FT(full-thickness, 전층) 피부 모델은 **섬유아세포·각질형성세포가 유발하는 스캐폴드 탈착과 수축**으로
> **구조적 기하가 불안정**하고, 그 결과 **표피 분화와 장벽 기능이 미흡**해
> **OECD TG 431/439 기준을 충족하는 규제 적합 검증**이 이루어지지 못하고 있다.

이 진술은 하나의 **인과 사슬**입니다. 팔로우업은 이 사슬을 층별로 끊어서 봅니다.

```
[A] 세포가 유발하는 기계적 불안정          (원인)
      ├ 섬유아세포 수축 (FPCL, α-SMA, 근섬유아세포)
      ├ 스캐폴드 탈착·가장자리 박리
      └ 각질형성세포 장력
            │
            ▼
[B] 기하 안정화 공학적 대응                (대응)
      ├ 기계적 고정·앵커링
      ├ 가교·강성 제어
      ├ 복합/보강 스캐폴드
      └ 무스캐폴드·공정 제어
            │
            ▼
[C] 표피 분화·장벽 기능 결과               (결과)
      ├ 분화 마커·층 구조
      ├ 장벽 정량 (TEER/TEWL/투과도/지질)
      └ 기하 ↔ 기능 상관
            │
            ▼
[D] OECD TG 431/439 규제 적합성            (판정)
      ├ TG 적합 기준 자체
      ├ 검증된 RhE 모델 · ME-too
      ├ FT 모델의 TG 미수재 간극
      └ 재현성·실험실 간 전이성
```

**주의(사실 확인 필요)**: TG 431(피부 부식성)·TG 439(피부 자극성)은 현재 **RhE(재구성 인체 표피)** 모델을
기준으로 쓰여 있습니다. 진피를 포함한 FT 모델은 이 TG의 검증 대상 모델로 수재되어 있지 않습니다.
즉 사용자가 지적한 "규제 적합 검증 미달"은 **(i) 모델 성능 부족**과 **(ii) TG 자체가 FT를 담고 있지 않음**
두 갈래로 나뉩니다. D 계열 회차에서 이 구분을 반드시 확인하고 최신 TG 개정판 기준으로 다시 검증합니다.

---

## 1. 일자별 키워드 일정 (하루 1개, 위에서부터 순서대로)

`done` 열에 수행 날짜를 적습니다. 빈 칸이면 아직 안 한 회차이고, 다음 실행은 **빈 칸 중 가장 위**를 씁니다.
한 바퀴를 다 돌면 1번으로 돌아가되 `skin-seen.json` 때문에 같은 논문은 다시 나오지 않습니다.

| # | 계층 | label (브리핑 표시용) | 핵심 검색어 | done |
|---|---|---|---|---|
| 1 | A | 섬유아세포 콜라겐 수축 | `fibroblast` + `collagen gel/lattice contraction` + `skin equivalent` | 2026-11-04 (5편) |
| 2 | A | 스캐폴드 탈착·박리 | `scaffold detachment` / `delamination` / `edge curling` + `skin model` | |
| 3 | A | 근섬유아세포 전환·장력 | `myofibroblast` / `alpha-SMA` / `contractile force` + `dermal equivalent` | |
| 4 | A | 각질형성세포 유발 장력 | `keratinocyte` + `traction force` / `epithelial tension` + `contraction` | |
| 5 | B | 기계적 고정·앵커링 | `anchoring` / `tethering` / `insert ring` / `mechanical constraint` + `skin equivalent` | |
| 6 | B | 가교로 수축 억제 | `crosslinking` (genipin, EDC/NHS, riboflavin) + `contraction` + `collagen scaffold` | |
| 7 | B | 보강·복합 스캐폴드 | `electrospun` / `reinforced` / `composite scaffold` / `PCL mesh` + `full-thickness skin` | |
| 8 | B | 탈세포 진피·천연 기질 | `decellularized dermal matrix` / `acellular dermis` + `skin model` | |
| 9 | B | 무스캐폴드·자가조립 | `scaffold-free` / `self-assembled` / `cell sheet` + `skin equivalent` | |
| 10 | B | 바이오프린팅 기하 제어 | `bioprinting` + `full-thickness skin` + `shape fidelity` / `geometry` | |
| 11 | C | 표피 분화 마커·층 구조 | `filaggrin` / `loricrin` / `involucrin` / `keratin 10` + `reconstructed skin` | |
| 12 | C | 장벽 기능 정량 | `barrier function` + `TEER` / `TEWL` / `permeability` + `skin model` | |
| 13 | C | 각질층 지질·세라마이드 | `stratum corneum lipid` / `ceramide profile` + `reconstructed human epidermis` | |
| 14 | C | 수축·기하가 분화에 미치는 영향 | `mechanical` / `substrate stiffness` / `strain` + `epidermal differentiation` | |
| 15 | C | 기중 배양(ALI) 조건 최적화 | `air-liquid interface` + `culture condition` / `optimization` + `skin equivalent` | |
| 16 | D | OECD TG 439 피부 자극성 | `OECD` + `TG 439` / `skin irritation` + `reconstructed human epidermis` | |
| 17 | D | OECD TG 431 피부 부식성 | `OECD` + `TG 431` / `skin corrosion` + `in vitro` | |
| 18 | D | ME-too 검증·신규 모델 등재 | `me-too validation` / `performance standards` + `skin irritation test method` | |
| 19 | D | FT 모델의 규제 적용 간극 | `full-thickness skin model` + `regulatory acceptance` / `validation` | |
| 20 | D | 재현성·실험실 간 전이성 | `reproducibility` / `inter-laboratory` / `transferability` + `reconstructed skin` | |
| 21 | E | 인접: 피부 OoC·관류 | `skin-on-a-chip` / `perfused` + `full-thickness` + `barrier` | |
| 22 | E | 인접: NAM·동물대체 전반 | `new approach methodology` / `animal-free` + `skin` + `regulatory` | |

---

## 2. 분류 라벨 규칙

브리핑의 각 논문에는 **계층 라벨을 첫 번째 태그로** 붙입니다. 한 논문이 여러 층에 걸치면
가장 중심이 되는 층 하나를 고르고, 나머지는 본문 요약에서 언급합니다.

- `A. 수축·탈착 원인`
- `B. 기하 안정화 대응`
- `C. 분화·장벽 결과`
- `D. 규제 적합성`
- `E. 인접 주제`

두 번째 이후 태그는 자유롭게 (모델 종류, 정량 지표, 핵심 수치 등).

---

## 3. 회차 운영 메모

- **하루 1키워드**가 원칙입니다. 같은 날 두 번 돌리면 날짜에 `b`, `c`를 붙입니다 (`skin-brief-2026-11-04b.html`).
- 해당 키워드로 **조건에 맞는 논문이 5편 미만**이면 있는 만큼만 싣고, 주제 메모(note)에 그 사실을 적습니다.
- **0편이면** 갱신하지 않고 그 키워드를 `done`에 `해당 없음`으로 표시한 뒤 다음 키워드로 넘어갑니다.
- 키워드를 추가·수정하고 싶으면 이 표를 직접 고치면 됩니다. 다음 실행부터 반영됩니다.
