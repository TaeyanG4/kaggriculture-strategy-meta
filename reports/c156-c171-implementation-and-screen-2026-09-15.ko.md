# c156~c171 구현 및 발동 화면 준비

작성일: 2026-09-15 KST  
부모: `agent/o182_combo_overflow.py`  
부모 SHA-256: `ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b`

## 결론

규칙·저장 진단·공개 V42 경로 감사를 마친 뒤, 부모의 경제 결정을 임의로 넓히지 않는 후보들을 구현했다. 현재 발동·건강성 검증에 올릴 후보는 **c156, c160, c163, c168, c170, c171**이다. 모두 o182에서 직접 만든 단일 변경 후보이며 성능 검증과 승격은 아직 없다.

| 후보 | 변경 | SHA-256 | 상태 |
|---|---|---|---|
| c156 | 생산 예정일의 상한 초과분이 CARE 가치보다 클 때만 CARE→HARVEST | `a8510eb530a1d9f6eaee82a2888c8047bb3887d8735ce07f072ba3ed4fc93c8b` | 구현·정적 확인, 미검증 |
| c160 | 696~711에서 기존 TOMATO/STRAWBERRY 수확물을 WATER/FERTILIZE 대신 회수 | `c3f5d1749665d173640c29271635de8cf5ea761f6dcc8bb82e0820c5a42776fc` | 구현·독립 테스트 보강, 미검증 |
| c163 | 실제 미래 가치가 없는 CARE만 COLLECT_FERTILIZER로 교체 | `9d2989e20189613b7d1469bcf2e8a5b828bab369f7ee8ccfaf8e6562695f2452` | 구현·정적 확인, 미검증 |
| c168 | 같은 타일의 충돌·비료 보유·후속 약속을 증명한 경우만 FERTILIZE를 WATER 앞에 배치 | `ba67a63dc255f1ad3f7a68951f4152665cbc1e7138a2834c00981791239e6661` | c164 안전 수정본, 미검증 |
| c170 | 부모가 확정한 비료 대상·수량·HIRE를 고정하고 실제 spawn/step+2 기준으로 순서·담당만 재배정 | `74bfa2ff5b63eba510a5623392a62f7b100acfd337dcacfe48729904c8c10292` | c159 탐색 효율 수정본, 미검증 |
| c171 | 비-YARN 49개 상점 순서쌍에 V42 생산 경로를 사용하되 o182 오프닝·YARN·종반 route 2와 후속 계층을 보존 | `2e30222a7b1f8ec61010409b531ff40fbd49cca08168065ae9855f6d008dce63` | c167/c169 안전 수정본, 미검증 |

## 구현 중 발견하고 분리한 결함

### c159 → c170

c159은 최고 예측가치 경로를 먼저 고른 뒤 타일별 비열화 여부를 검사했다. 정적 완전열거 반례에서 최고 경로는 한 타일을 악화해 기각됐지만, 모든 타일을 유지하면서 가치 112→196으로 개선하는 차선 경로가 존재했다. c159은 보존하고 c170을 o182에서 다시 만들었다. c170은 각 타일의 부모 예측 이득을 beam 확장 단계의 하한으로 적용하므로 안전한 차선 경로를 놓치는 이 문제를 제거한다.

c170은 다음을 모두 고정한다.

- 부모 반환 action과 시장 주문
- 비료 구매 수량과 HIRE 수
- 대상 타일 multiset
- 작업자별 path 길이와 비료 quantity
- 각 대상의 `_r51_input_gain` 하한

실제 현재 이동 뒤의 HIRE spawn과 다음 callback PICKUP 뒤 `step+2`를 시작점으로 계산한다. 한 대상이라도 부모보다 낮아지거나 모든 대상이 같으면 pending을 바꾸지 않는다. 계산 중에는 원본 pending을 건드리지 않고 마지막에 한 번만 교체한다.

### c167 → c169 → c171

c167 독립 감사에서 세 결함이 확인됐다.

1. 빈 router state로 step 648에 시작하면 legacy route 2를 V42 route가 다시 덮었다.
2. o171/o170 gate와 최종 telemetry wrapper가 같은 step을 읽을 때 guard 계수가 초기화됐다.
3. 불완전 상점 관측이 route 100으로 열렸다.

c169가 앞의 세 경계를 고쳤다. 이어 비문자·비시퀀스·중첩 목록처럼 더 강한 malformed 입력에서 legacy router 자체가 예외를 낼 수 있음을 확인해 c171을 새로 만들었다. c171은 해당 예외에서도 기존 route를 유지하며 step 648 이후에는 route 2를 강제로 보존한다. 정상 64개 ordered shop pair에서 c171의 전략 행동은 c169와 같고, 49개 non-YARN만 V42 신규 경로를 선택한다.

## 보류·기각한 번호

- c157: 실제 전환 실행 누락 증거가 없어 구현하지 않음.
- c158: 처리되지 않은 중복 현장 행동 증거가 없어 구현하지 않음.
- c161: 일꾼 가방 상한 가정이 규칙과 맞지 않아 구현하지 않음.
- c162: 시장 주문 10개 초과 사례가 없어 구현하지 않음.
- c164: 같은 타일의 제3 행동 충돌을 막지 못해 정적 기각. c168이 대체.
- c165: WATER를 대체할 실제 고가치 작업이 관측될 때까지 보류.
- c166: 기존 판매 예약과 충돌하며 유사 o169 회귀가 있어 기각.

## 정적 검증

아래 8개 테스트 파일을 한 번에 실행해 **78 passed**를 확인했다.

- `tests/test_c156_production_cap_harvest.py`
- `tests/test_c159_fertilizer_tour_assignment.py`
- `tests/test_c160_day29_harvest.py`
- `tests/test_c163_worthless_care_fertilizer.py`
- `tests/test_c168_fertilize_before_water.py`
- `tests/test_c169_v42_production_routes.py`
- `tests/test_c170_fertilizer_tour_assignment.py`
- `tests/test_c171_v42_production_routes.py`

모든 전용 빌더를 다시 실행했을 때 frozen write가 같은 바이트를 확인했다. 후보 compile, 마지막 callable=`agent`, 부모 SHA, overlay/output manifest 해시를 검사했다. c167의 후보·overlay·manifest도 원래 해시 그대로다.

이 검증은 구현 계약과 반례에 대한 증거다. reacting 경기 우월성, 실제 수익 증가, 승격 또는 제출 근거는 아니다.

## 공통 발동·건강성 screen

공통 검증기만 재사용한다.

- 설정: `configs/validation/c156-c171-activation-screen-20260915.json`
- 출력: `state/agent_experiments/c156_c171_activation_screen_20260915/`
- 모델: o182 + 생존 후보 6개
- 상대: 서로 다른 8개 family
- 조건: 새 seed 12개, 양 좌석
- 경기: `7 × 8 × 12 × 2 = 1,344`
- worker: 8, 각 경기 fresh Python subprocess

Prepare/Check만 완료했고 **경기는 0개 실행**했다. 이 단계의 첫 목적은 실제 action 변화, 후보 telemetry 발동, 오류 0, 부모 대비 명백한 tail 회귀 여부 확인이다. 여섯 비교와 12 seed라서 통계적 승격 판정에는 작다. 발동하고 음의 신호가 없는 후보만 별도 selection config로 올린다.

실행 명령:

```powershell
$validationConfig = 'H:\dev\kaggle-data\kaggriculture-strategy-meta\configs\validation\c156-c171-activation-screen-20260915.json'
$validationOutput = 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\c156_c171_activation_screen_20260915'
& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\tools\run-validation.ps1' -Config $validationConfig -Out $validationOutput -Stage screen -Action Run
```

기존 측정치 기준 예상 시간은 약 20~30분이다. 진행률·완료/전체·백분율·경과·처리율 기반 ETA·cache·실패 수와 성공/실패 알림음을 공통 wrapper가 표시한다.
