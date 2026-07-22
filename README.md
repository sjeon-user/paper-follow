# Physical AI 논문 팔로우업

arXiv에서 Physical AI 관련 최신 논문을 매일 자동으로 모아, 대표 그림과 한국어 요약(배경/해결)으로 정리하고 음성 낭독용 대본까지 만드는 개인용 브리핑입니다.

## 보기
- **브리핑 페이지**: [`paper-brief.html`](paper-brief.html) — 논문별 대표 그림 + 배경/해결 요약
- **음성 대본**: [`voice-script.md`](voice-script.md) — 논문을 한 편씩 소개하는 TTS 낭독용 대본
- GitHub Pages가 켜져 있으면 폰·PC 어디서든 링크로 접근할 수 있습니다.

## 구성
| 파일 | 설명 |
|---|---|
| `follow-config.md` | 주제·조건·요약 형식 설정 파일 (여기를 바꾸면 다음 생성부터 반영) |
| `paper-brief.html` | 결과 페이지 (`PAPERS` 배열 + `BRIEF_DATE`) |
| `voice-script.md` | 음성 낭독 대본 |
| `images/` | 각 논문 대표 그림 |

## 주제 (follow-config.md)
Physical AI — egocentric, motion capture, retargeting, robot arm, self-driving lab, VLA

## 자동화
매일 오전 10시, 설정에 따라 결과물을 새로 생성하고 이 저장소에 반영합니다.

*데이터 출처: arXiv (각 논문 라이선스/저작권은 원저작자에게 있습니다).*
