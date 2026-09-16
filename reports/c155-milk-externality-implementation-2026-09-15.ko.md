# c155 우유 외부효과 급식 게이트 — 구현 완료·성능 미검증 (2026-09-15)

역할: 코드 구현만. 게임 실행·아레나·제출은 하지 않았다. 아래 정적 검사(구문, 합성 관측 단위검사,
저장 리플레이 1건 shadow)만 수행했다. **개선 여부는 미검증**이며 설계 담당 Codex의 검토와
검증 명령 제공 후 사용자가 실행한다.

## 산출물 (절대 경로, SHA-256)

| 파일 | 역할 | SHA-256 |
|---|---|---|
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\agent\c150.py` | 잠정 부모 (수정 없음) | `9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b` |
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\agent\overlays\c155_milk_externality_gate.py` | 오버레이 (신규) | `7f3d68266508eeae6e08013261025f0e582ae5cd46272b86b6f0281d9100d615` |
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\agent\c155_milk_externality.py` | 후보 (적용 모드, 제출용 기본) | `886e71c8d14ad7092c28ebe3b6365a36d5d996716c31416735b3eea2271c07cd` |
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\agent\c155_milk_externality_observe.py` | 관측 전용 쌍둥이 (`_C155_APPLY = False`) | `746673e47ab2a27f79afd11aa5fad0cfe2eee710ca15cca4cb0a50059195a4d5` |
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\tools\build_c155_milk_externality.py` | 재현 빌드 (부모 SHA 고정, frozen write, `--observe`) | `0bdaf92ff18cdbf16c2071b68b28c86c8172296f86ff0c499f8021b2d27a3994` |
| `H:\dev\kaggle-data\kaggriculture-strategy-meta\tools\c155_shadow.py` | 저장 리플레이 관측 진단 도구 (엔진 미사용) | `07026d5c85fa6f92c8397050e82af3ff9cc6c26ac31d26895a197770ef6d81f3` |

빌드: `.venv\Scripts\python.exe tools\build_c155_milk_externality.py --observe`
(후보 = 헤더 1줄 + c150 원문 + 오버레이. 기존 산출물과 바이트가 다르면 빌드가 중단된다.)

## 부모 선택

- HANDOFF는 c129(라이브 2820.3)를 기준선으로 유지한다고 적혀 있고, c153/c154는 c129 위에 만들어졌다.
- c150은 헤더상 "UNTESTED; NOT SELECTED" 로컬 가설이지만, 이번 세션의 로컬 측정에서 c129·c146과
  32/32 경기 **정확히 동일 마진(0)** 으로 행동상 구별되지 않았고, 88경기 엘리트 패배 스위트의
  기준선도 c150으로 완료돼 있다(`o_results/elite_suite/c150/`).
- c129와 c150 중 어느 쪽이 더 강한지 판정할 완료된 공통 대진 근거는 없으므로 지시대로
  **c150을 잠정 부모**로 썼다. c150에는 c132/c135가 포함돼 있지 않아(모듈 상수 `_C132_*` 없음)
  중복 적용은 없다. c150의 C124(504~695, 상점 없는 저마진 축종 급식 생략)는 이미 PASS로 바꾼
  행동을 내보내므로 c155의 "부모가 제안한 FEED" 후보에 들어오지 않는다.
- c129를 부모로 바꾸려면 빌드 스크립트의 `PARENT`/`PARENT_SHA` 두 줄만 바꾸면 된다(오버레이는
  `_r37_market_price`, `_R37_MARKET_PARAMS`, `copy` 이외의 부모 내부에 의존하지 않는다).

## 변경 범위 (기존 동작 → 변경 동작)

- 기존(c150): 테이프가 제안한 모든 COW FEED를 그대로 실행.
- 변경: step 336~671, 부모가 제안한 FEED 중 **성숙한 COW(age ≥ 0)·비생산일(age % 2 == 1)·
  fed_today 아님·consecutive_unfed == 0·작업자 인벤토리 WHEAT ≥ 1** 인 것만 검토하고,
  경제성 통과 시 그 작업자의 명령만 `['PASS']`로 바꾼다. 나머지 명령·시장 주문은 원본 그대로.
  미성숙 소, 생산일, 이미 하루 굶은 소, 다른 축종, 구매·고용·이동·작물·판매는 손대지 않는다.
- `age = day + 1 - placed_day - 8` (c132와 동일; 생산일은 age % 2 == 0).

## 구현 구조 (파일: overlays/c155_milk_externality_gate.py)

| 함수 | 역할 |
|---|---|
| `_c155_candidates(observation, parent_action)` | 위 범위 조건을 만족하는 (actor, x, y) 목록 |
| `_c155_rival_exposure(observation)` | 상대 소 타일의 공개 `yield_units` 합(ready), 오늘 밤 생산 소 수(due), exposure = ready + 2·due |
| `_c155_market_params(observation)` | c150의 `_r37_quote_priority`와 같은 방식으로 관측의 `market.params` 패치를 병합한 가격 파라미터 |
| `evaluate_feed_skip(observation, actor, committed_skips, recent_max_milk)` | 반환: `allow_skip, reason, wheat_saved_value, own_production_loss, opponent_price_gain, uncertainty_buffer, estimated_relative_gain` (+진단용 `delta_p, rival_ready, rival_due`) |
| `_c155_evaluate_turn(observation, parent_action, recent_max_milk)` | 후보를 순서대로 평가, 허용된 결정마다 `committed_skips`를 1 늘려 다음 후보에 전달 |
| `_c155_set_mode('apply'|'observe')` | 모드 전환 진입점 |
| `agent(observation, configuration)` | 부모 호출 → 지원 설정 확인 → 창 확인 → 평가 → (적용 모드에서만) deepcopy 후 PASS 치환 |

- 지원하지 않는 설정(boardSize 10, turnsPerDay 24, townShopSellInterval 4, townCenterSellInterval 24가 아님):
  부모 행동 유지, `unsupported` 계수.
- 24스텝 MILK 가격 이력이 없으면 `price_history` 사유로 차단(부모 유지).
- 예외는 삼키지 않고 `errors` 계수를 올린 뒤 부모 행동을 반환한다.
- observation과 부모 action 객체는 직접 변경하지 않는다(적용 시 deepcopy; 단위검사에서 확인).

## 경제 계산과 모든 계수

엔진(1.32.7 `_daily_refresh_animals`) 확인 사항: 소는 급식 여부와 무관하게 2일마다 생산한다.
급식은 (a) `consecutive_unfed` 리셋(2 이상이면 탈출), (b) 케어 보너스 적립(케어+급식 → pending+1)과
소비(생산일 급식 시 yield += 1 + pending; 생산일 미급식 시 pending 소멸)만 담당한다.
**비생산일 급식 1회 생략이 줄이는 우유량은 정확히 최대 1단위**(그날 케어가 적립했을 pending 1)이며,
`consecutive_unfed == 0` 조건이 그 한 번의 생략으로 탈출이 불가능함을 보장한다(다음 날 테이프가
급식한다는 전제; 테이프가 다음 날도 안 주면 c155가 아니라 테이프 문제이고, 그 경우 후보 조건
`consecutive_unfed == 0`이 두 번째 생략을 막는다).

| 계수 | 값 | 의미 | 출처 |
|---|---|---|---|
| `_C155_WINDOW` | (336, 672) | 검토 창 | c132 |
| `_C155_WHEAT_REALIZATION` | 0.8 | 절약한 밀 1개를 현재 WHEAT 가격의 80%로 평가 | c132 (8·wheat) |
| `_C155_OWN_LOSS_UNITS` | 2 | 생략당 차감할 MILK 단위. 엔진 정확값은 ≤1이나 보수적으로 2 | c132 (20·milk) |
| MILK 평가가격 | 최근 24스텝 MILK 최고가 | c132 규칙 | c132 |
| `_C155_SHOCK_UNITS` | 2 | 국소 가격충격 추정에 쓰는 공급 감소량 | 보고서 |
| `_C155_RIVAL_DUE_UNITS` | 2 | 오늘 밤 생산하는 상대 소 1마리당 노출 단위(기본 1 + 보너스 1 가정) | 보고서 |
| `_C155_ATTRIBUTION` | 0.5 | 명목 상대 노출 이익 중 이번 생략에 귀속하는 비율(상대가 실제로 수확·판매할지 모름) | 보고서 |
| `_C155_BUFFER` | 5 (현금) | 불확실성 여유 | 보고서(10배 단위 +50) |

```
wheat_saved_value       = 0.8 · WHEAT가격                                  [현금]
own_production_loss     = 2 · max(MILK가격, 최근 24스텝)                    [현금]
delta_p                 = max(0, price(MILK, inv − 2·committed − 2) − price(MILK, inv − 2·committed))  [현금/단위]
rival_exposure          = Σ 상대 소 yield_units + 2 · (오늘 밤 생산 상대 소 수)  [단위]
opponent_price_gain     = 0.5 · rival_exposure · delta_p                    [현금]
estimated_relative_gain = wheat_saved_value − own_production_loss − opponent_price_gain − 5
allow_skip              = estimated_relative_gain ≥ 0
```
차단 사유: `gross_edge`(0.8·wheat − 2·milk ≤ 0, c132 기본 조건 미달), `externality`(상대 이익 차감 후 음수),
`price_history`(이력 부족). 보고서의 `gross_edge10 ≥ externality10 + 50`을 10으로 나눈 것과 동일하다.

c135와의 차이(지시 반영): 4일치 상점 수요를 재고에서 빼지 않고, 지난 턴들의 누적 생략량도 다시 빼지 않는다
(현재 관측 재고에 이미 반영됨). 같은 턴 안에서만 앞서 허용한 생략의 −2씩을 `committed_skips`로 누적해
다음 후보를 더 낮은 재고(더 가파른 가격)에서 평가한다. **이 계산은 공개 관측 기반 근사치이며 수익 보증이
아니다. 계수는 두 회귀 시드를 설명하도록 정한 개발값이지 검증된 최적값이 아니다**(코드 docstring에도 명시).

## 기록 항목 (telemetry, 계수만 유지 — 매 턴 로그 없음)

`milk_externality_mode, reviewed, allowed, applied, blocked, blocked_gross_edge, blocked_externality,
blocked_price_history, wheat_saved_sum, own_loss_sum, opp_gain_sum, max_committed_turn, unsupported, errors`
(부모 telemetry에 병합). 상세 결정별 진단은 `tools/c155_shadow.py`가 저장 리플레이에서 출력한다.

## 관측 전용 모드 사용법

1. `agent/c155_milk_externality_observe.py` (빌드 `--observe`): 판단·계수는 동일, 행동은 항상 부모 그대로.
2. 코드에서: `_c155_set_mode('observe')` / `_c155_set_mode('apply')`.
3. 저장 리플레이 shadow(엔진 없음):
   `.venv\Scripts\python.exe tools\c155_shadow.py --candidate agent\c155_milk_externality_observe.py --replay <replay.json> --team Taeyang`
   (`--replay-dir <dir> --summary`로 집계). 기록된 행동을 부모 제안으로 간주하므로 c129/c150 행동 리플레이에서만 유효하다.

## 정적 검사 결과

- `py_compile` 통과; 두 빌드 모두 import 성공, `_C155_APPLY` True/False 확인.
- 합성 관측 단위검사: 후보 필터가 age 3(비생산일)만 선택하고 age 2(생산일)·unfed 1을 제외; 손계산 일치
  (wheat 33.6 − loss 20 − opp 0.5·7·4 = 14 − 5 = −5.4 → externality 차단; 상대 노출 0이면 +8.6 허용;
  `committed_skips=1`이면 delta_p 4 → 5로 커져 더 보수적).
- 적용 모드는 deepcopy 결과에 PASS, 관측 모드는 부모 객체 그대로 반환; observation 미변경 확인.
- 저장 리플레이 1건(108735977, 2750+ 상대 패배) shadow: 검토 55, 허용 2, gross_edge 차단 24, externality 차단 29.

## 미해결 문제 / 검토 요청

1. **게이트가 매우 보수적일 수 있다.** 위 1건에서 c132 원 규칙이면 31/55 허용될 것을 c155는 2/55만
   허용했다(상대 소 6~8마리의 공개 보유 우유 8 × delta_p 4 × 0.5 ≈ 16이 절약분을 잠식). 보고서 자체가
   "양수 시드 보존율은 실행 전 주장 불가"라고 했으므로, 검증에서 **c132 양수 마진 합 보존율**을 반드시 봐야 한다.
2. `_C155_OWN_LOSS_UNITS = 2`는 엔진 정확값(≤1)의 2배다. 1로 낮추면 허용이 크게 늘어난다 — 감도 검사 대상.
3. `recent_max_milk`(24스텝 최고가)는 c132 관행이며, 실현 판매가의 좋은 추정치인지 미검증.
4. 상대 노출의 `due` 계산은 상대 소가 오늘 밤 실제로 급식·수확될지 모른 채 2단위를 가정한다.
5. 부모 c150 vs c129 선택은 잠정이다. c129 위에 다시 빌드하려면 `PARENT`/`PARENT_SHA`만 교체.
6. 창 336~671 밖(특히 28일차 이후)의 비생산일 급식은 검토하지 않는다(c132 범위 유지).

## 비교 검증에서 반드시 확인할 항목

- 보고서의 세 회귀 시드(802709669, 1489188767, 897800751)에서 상대 현금 증가가 사라지는지와,
  양수 시드(1593104859, 1823700906, 1341431059, 1253822844, 748991926)의 c132 이득 보존율(목표 ≥ 50%).
- `milk_externality_applied` > 0 인 경기 수(실제 발동률)와 `errors == 0`, `unsupported == 0`.
- 같은 시드·같은 상대·양 좌석 paired 비교(부모 c150 및 c129 대비), 관측 전용 쌍둥이가 부모와 byte-동일 행동인지.
- 88경기 엘리트 패배 스위트(`o_replays/elite_chunks`, 기준 `o_results/elite_suite/c150`)에서의 마진 변화.
