# 액체 핸들링·신개념 파이펫 — 문제 분류 · 키워드 일정 (liquid-keywords)

`liquid-config.md`의 자매 파일입니다. 코워크(Claude)는 아래 일정에서 **키워드 1개**를 꺼내 `liquid-brief.html`을 채웁니다.

---

## 0. 출발 문제 진술 (Problem statement)

> 공기치환식 파이펫과 기존 액체 핸들러는 **물 같은 액체를 전제로 한 개루프(open-loop) 장치**다.
> 점도가 높거나(대략 100 cP 이상) 기포·거품·응괴가 섞이면 흡인·토출량이 틀어지는데,
> 장치는 그 사실을 **스스로 알지 못한다**. 사람이 '액체 클래스'를 경험으로 맞추는 것이 현재의 해법이다.
>
> → **액체 성질을 감지하고(센싱), 결과를 확인하고(검증), 조건을 스스로 고치는(폐루프)**
> 신개념 파이펫·액체 핸들러와, 그것을 다루는 **AI·로봇 기술**을 팔로우업한다.

팔로우업은 다섯 축으로 끊어서 봅니다.

```
[A] 점도 대응          고점도·비뉴턴 액체의 정확한 이송
      ├ 흡인/토출 속도·지연 등 파라미터 최적화 (액체 클래스 자동화)
      ├ 양변위(positive displacement)·비접촉·음향 등 원리 변경
      └ 점도 자체를 파이펫으로 추정 (proxy viscometry)

[B] 기포·오류 대응      기포·거품·응괴·팁 누락·부분 토출
      ├ 압력 파형 감시 (흡인 곡선, 응괴/공기 판정)
      ├ 영상 기반 검출 (팁 내 기포, 액면, 잔류)
      └ 정전용량·광학 액면 검출

[C] AI·폐루프 제어      측정 → 판단 → 보정
      ├ 베이즈 최적화·능동학습으로 파라미터 탐색
      ├ 실시간 피드백 보정 (체적 재조정, 재시도)
      └ LLM·VLM 기반 프로토콜 검증과 실행 감시

[D] 로봇 기술          갠트리형이 아닌 팔·모바일·휴머노이드
      ├ 협동로봇이 수동 파이펫을 다루는 방식
      ├ 강화학습·VLA 기반 조작 정책
      └ 시뮬레이션·벤치마크·디지털 트윈

[E] 플랫폼·검증        오픈소스 장비, 체적 검증, 표준화
      ├ 저가·오픈 하드웨어 (OT-2 계열, 3D 프린터 개조)
      ├ 하드웨어 독립 제어 계층 (PyLabRobot 등)
      └ 중량·광도 기반 체적 검증
```

---

## 1. 일자별 키워드 일정 (하루 1개, 위에서부터 순서대로)

| # | 계층 | label (브리핑 표시용) | 핵심 검색어 | done |
|---|---|---|---|---|
| 1 | — | 총론: 점도·기포·AI·로봇 | 다섯 축을 한 회차로 개관 (첫 회차) | 2026-11-13 (10편) |
| 2 | A | 고점도 이송 파라미터 최적화 | `viscous` + `pipetting robot` / `liquid transfer` + `optimization` | |
| 3 | A | 양변위·비접촉·음향 토출 | `positive displacement` / `acoustic droplet ejection` / `non-contact dispensing` + `viscous` | |
| 4 | A | 파이펫 기반 점도 추정 | `viscometry` / `rheology` + `pipetting robot` / `pipette tip` | |
| 5 | A | 바이오잉크·하이드로겔·세포현탁액 | `bioink` / `Matrigel` / `collagen` + `automated dispensing` | |
| 6 | B | 압력 파형 기반 오류 판정 | `pressure monitoring` / `aspiration curve` + `clot` / `bubble` / `foam` | |
| 7 | B | 영상 기반 기포·액면 검출 | `bubble detection` / `liquid level` + `vision` / `deep learning` + `pipette tip` | |
| 8 | B | 팁 표면·잔류·캐리오버 | `low retention` / `lubricant-infused` / `carryover` + `pipette tip` | |
| 9 | C | 베이즈 최적화·능동학습 | `Bayesian optimization` / `active learning` + `liquid handling parameters` | |
| 10 | C | 실시간 피드백 체적 보정 | `closed-loop` / `feedback` + `dispensing volume` / `pipetting` | |
| 11 | C | LLM·VLM 프로토콜 검증·감시 | `large language model` / `vision-language` + `liquid handler` / `lab automation` | |
| 12 | D | 협동로봇·양팔 로봇 파이펫팅 | `collaborative robot` / `dual-arm` + `pipette` | |
| 13 | D | 강화학습·VLA 실험실 조작 | `reinforcement learning` / `vision-language-action` + `laboratory` + `liquid` | |
| 14 | D | 시뮬레이션·디지털 트윈 | `simulation` / `digital twin` / `benchmark` + `wet-lab` / `liquid handling` | |
| 15 | D | 투명 액체·용기 인식 | `transparent` + `liquid` + `perception` + `laboratory` | |
| 16 | E | 오픈소스·저가 액체 핸들러 | `open-source` / `low-cost` + `liquid handler` / `pipetting robot` | |
| 17 | E | 체적 검증·SI 소급성 | `gravimetric` / `photometric` / `volume verification` + `automated liquid handling` | |
| 18 | E | 스케줄링·경로 최적화 | `scheduling` / `routing` / `tip usage` + `liquid handling` | |

---

## 2. 분류 라벨 규칙

각 논문의 **첫 번째 태그는 계층 라벨**입니다.

- `A. 점도 대응`
- `B. 기포·오류 대응`
- `C. AI·폐루프 제어`
- `D. 로봇 기술`
- `E. 플랫폼·검증`

한 논문이 여러 축에 걸치면 중심 축 하나를 고르고 나머지는 본문에서 언급합니다.
바이오 실험실이 아닌 분야(접착제 도포, 식품, 3D 프린팅)에서 온 논문에는 `인접` 태그를 붙입니다.

---

## 3. 회차 운영 메모

- **하루 1키워드** 원칙. 같은 날 두 번 돌리면 날짜에 `b`, `c`를 붙입니다.
- 조건에 맞는 논문이 5편 미만이면 있는 만큼만 싣고 주제 메모에 적습니다. 0편이면 `해당 없음`으로 표시하고 넘어갑니다.
- **상용 장비의 압력 기반 감시(Hamilton TADM, Tecan 등)는 논문보다 특허·기술문서에 많습니다.**
  논문이 드문 축이므로, 6번 회차에서는 그 사실을 명시하고 필요하면 특허 조사를 별도로 제안합니다.

---

## 4. 1회차에서 확인된 것 (2026-11-13)

- **점도 + AI + 폐루프가 한 논문에서 만난 사례는 사실상 1편**입니다 (`10.1039/D3DD00255A`):
  204~1275 cP 점도 표준액에 대해 다목적 베이즈 최적화로 흡인·토출 속도를 찾고, 자동 저울을 붙여 폐루프를 닫았습니다.
  이 논문은 **Europe PMC에 색인돼 있지 않아** 웹 검색으로 찾았습니다 → 화학 자동화 저널(Digital Discovery 등)은
  Europe PMC만으로는 누락되므로 **arXiv·ChemRxiv·웹 검색 병행이 필수**입니다.
- **기포 검출은 '영상'이 주류**이고(`arXiv:2512.02018` 정확도 99.6%), **압력 파형 기반 논문은 드뭅니다**
  (2018년 `10.1038/s41598-018-24145-0` 정도). 상용 장비에는 이미 들어가 있지만 학술 문헌은 얇습니다.
- **저가 장비(OT-2)는 압력 감시가 없어 개루프**라는 점이 여러 논문의 공통 출발점입니다
  (`arXiv:2607.15620`, `10.1007/s10489-025-06334-3`). 카메라로 그 공백을 메우는 흐름입니다.
- **투명한 액체는 정면 카메라로 볼 수 없다**는 한계가 명시돼 있습니다(`arXiv:2607.15620`).
- **로봇 쪽은 '팁 장착'이 병목**입니다. 협동로봇(`arXiv:2207.01214`)도 강화학습(`arXiv:2603.00719`)도
  팁 부착 정밀도를 핵심 난제로 다룹니다. 액체 자체의 물성(점도·기포)을 로봇 정책이 다룬 사례는 아직 없습니다.
