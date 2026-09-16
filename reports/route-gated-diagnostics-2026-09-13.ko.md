# 경로 제한 최종 후보 진단 — 2026-09-13

## 결론

`loss_diagnostics_v2`는 `complete`이며 10개 무결성·동작 게이트가 전부
통과했다. 이 결과는 c118~c120의 의도한 기계적 동작을 입증한다. 고정 상점과
기록 상대를 사용했으므로 실전 승률이나 1위권 우위를 입증하지는 않는다.

다음 단계는 이미 관측된 train4의 동일한 64개 반응형 경기에서 c112를
대조군으로 c118~c120을 값싸게 기각 검사하는 것이다. 이 단계는 192개 새
경기만 실행하고 selection16, holdout48, Kaggle 제출을 사용하지 않는다.

## 스킬 교체 확인

- 사용자 제공 ZIP: `G:/download2/kaggle-competition-ops.zip`
- ZIP SHA-256: `FC69A58916F0A2F2FC7E7907F57CC34901A0F57C6AF563B38BAD91A4749309AB`
- 설치 위치: `.agents/skills/kaggle-competition-ops/`
- 설치 파일: 29개
- ZIP의 29개 파일과 설치본을 파일별 SHA-256으로 대조: 29/29 일치, 누락·추가 0
- `quick_validate.py`: `Skill is valid!`
- 이전 `.agents/skills/kaggle-dataset-ops/` 빈 디렉터리까지 제거했다.
- `AGENTS.md`와 `HANDOFF.md`는 대회 전용 스킬을 기본 운영 틀로 참조한다.

## loss_diagnostics_v2

결과 경로:

- `state/agent_experiments/championship_final_20260913/loss_diagnostics_v2/results.json`
- `state/agent_experiments/championship_final_20260913/loss_diagnostics_v2/REPORT.md`

통과한 게이트:

1. 24/24 경기 유효
2. 모든 상점 순서 고정 확인
3. 정책 예외 0
4. 신규 내부 오류 0
5. 경로 분할 일치
6. horizon12 due-step 숫자형 telemetry 확인
7. YARN/PET 양 2마리 구매·운반·배치 완료
8. 알려진 종료 수확 이득 유지
9. 무관 overlay 완전 abstain
10. 공식 거래 장부 유효

경로 제한 horizon12 효과:

| 에피소드 | c112 | c118 | 변화 |
|---:|---:|---:|---:|
| 108323339 | -7,537 | -6,288 | +1,249 |
| 108324521 | -1,429 | -669 | +760 |
| 108387151 | -1,232 | +58 | +1,290 |

비대상 에피소드 108274758, 108285630, 108308172에서는 c118이 c112와
점수뿐 아니라 전체 행동 해시까지 같았다. 따라서 광범위 horizon12에서
나타났던 두 회귀 사례를 경로 제한이 차단했다.

c119는 108323339의 `YARN_STORE -> PET_CAFE`에서 c118 대비 +2,372를
추가했다. c120은 108274758에서 c119 대비 +269를 추가해 -17을 +252로
뒤집었다. 나머지 무관 사례에서는 두 overlay가 행동 해시까지 abstain했다.

## 공개 코드 정적 대조

`master_engine_v3`와 `dynamic_route_latest` 노트북은 셀을 실행하지 않았다.
AST로 리터럴 Base85 상수만 읽고, 압축 해제 크기를 2MB로 제한해 정적
비교했다.

- 두 Base85 payload는 완전히 동일하다.
- 디코딩된 두 소스도 SHA-256
  `a2047ebd8ca5720221e1421529655d9c67a7b2fedb74e874c7d3c55a8970ac7e`로 같다.
- 이는 이미 train screen에서 사용한 공개 V38과 byte-identical하다.
- 따라서 제목이 다른 두 노트북을 새 전략 계열이나 추가 독립 상대 증거로
  세지 않는다.

정적 영수증:
`state/agent_experiments/public_intel_20260913/source_analysis.json`.

## 현재 외부 관측

2026-09-13 이 보고서 작성 중 공식 Kaggle CLI의 읽기 전용 스냅샷:

- 1위 Majkel1337: 3225.2
- 2위 Mengfei Li: 3047.2
- c110 ref 56185728: COMPLETE, 조회 시점 2771.0
- c111 ref 56190992: COMPLETE, 조회 시점 2566.1

시뮬레이션 대회의 점수는 계속 변하므로 이 수치는 고정 성능 측정이 아니다.
c111의 높은 최근 승률과 낮은 rating, c110의 더 성숙한 고등급 노출은 서로
다른 표본에서 나온다. 이번 후보는 동일 job의 paired delta, 상대 계열, 좌석,
경로, 꼬리손실을 모두 통과한 뒤에만 외부 제출 후보가 된다.

## 다음 사용자 실행

```powershell
Set-Location 'H:\dev\kaggle-data\kaggriculture-strategy-meta'
& '.\state\agent_experiments\championship_final_20260913\run_finalist_train_screen.ps1' -Workers 4
```

정상 완료 표식:

```text
DONE: ...\finalist_train_v1\results.json status=complete
```

스크립트는 성공·실패를 구분하는 Windows 알림과 소리를 낸다. 완료 후
`results.json`과 `REPORT.md`에서 전체·경로·상대·계열·좌석별 회귀와 행동
변화를 판독한다. YARN/PET가 train4에 없으면 c119는 자동으로 미검증 처리하고
새 seed의 경로 층화 확인으로 보낸다.
