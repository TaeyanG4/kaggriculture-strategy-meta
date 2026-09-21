# 최종 판정 (2026-09-18 22:17, 실행·판정 Claude) — 제출 권고 없음, base19 유지

모든 판정 기준은 결과 전에 고정된 것(`o-p001-mx2-arena-plan` R1–R5, `o-p002-panel-plan` L1–L4, blind B1–B3)만 적용했고, 가중치·상대·seed·후보 파라미터는 바꾸지 않았다. 실행 오류 2건(다중 파일 상대 로더, 상대의 진단용 telemetry 키)은 행동 동일성이 검증된 단일 파일 래퍼로만 수정했다(v1b, v1c). 모든 캠페인은 실행 전후 해시 일치, 실패·타임아웃 0, health failure 0.

## 1. 후보별 상태
| 후보 | 상태 | 근거 |
|---|---|---|
| **p001_mx2 (MX2)** | **보류** — arena gate 최종 불통과, 제출 권고 없음 | screen PASS, confirm PASS, **final R2 FAIL**(V46 W→L 2/L→W 0, shop-router-v5 W→L 2/L→W 1; 모두 seed 44142014 한 세계). own·마진은 모든 단계·패널·풀에서 +(아래 표) |
| **p002_cow1 (조건부 소 1마리)** | **폐기** | B own −1,487·마진 −115·W→L 2; D own −2,281·마진 −1,294·W→L 11; frozen −114·W→L 2. 6/6 상대군 own 손실 |
| **p002_cow1_mx2 (MX2+p002)** | **폐기** | MX2 위 증분 음수(B own −1,529·마진 −144; D own −1,152·마진 −1,132), 상호작용 ≈0 |
| p003 (축군 라인) | **미착수, 라인 종료** | 주원인이 구조적(우유 가격 −2.1/u 선형 → 추가 단위가 기존 축군 단가를 함께 낮춤; +19u → +$57), 일관된 이득 조건 없음 |
| 공식 champion | **base19 유지** | gate 미충족 후보는 제출 권고 대상 아님 |

Blind 7240–7255: **미사용 유지**(통과 후보가 없어 진입하지 않음).

## 2. MX2 증거 요약 (base19 대비, paired)
| 세트 | n | own Δ | 마진 Δ | W→L / L→W | 규칙 |
|---|---|---|---|---|---|
| arena v1b screen (8 seeds) | 320 | +2,234 | +402 | 1 / 5 | R1–R4 PASS |
| arena v1b confirm (8 seeds) | 320 | +2,021 | +1,166 | 0 / 1 | R1–R4 PASS |
| **arena v1c final (16 seeds)** | 640 | +1,389 | +992 | **7 / 18** | **R2 FAIL** (V46 −352 마진, 2/0; shop-router 2/1) |
| B mx_eval(v46·k0006·v48·router_v5 + 동결 MG·Majkel) | 208 | +1,953 | +1,367 | 0 / 4 | — |
| D 라이브 계보 패널(router v5·v3.1, boatlee, prvsiyan, v48, V46) | 96쌍 | +1,129 | +2,085 | 0 / 8 | router_tschinkel +3,240, V46 −184 |
| C frozen 라이브 풀 117(개발 자료) | 117 | +2,450 | +2,039 | 0 / 4 | fieldbook A/F +724/+1,530 |
승률은 어디서도 유의하게 오르지 않는다(point delta +0.006~+0.037, CI가 0 포함). 특히 하드 반응형 포크 V46은 arena 0.34→0.28, 패널 0/16(전 모델). MX2는 "더 벌기"이지 "지는 경기 이기기"가 아니며, final의 R2 위반은 1 세계(44142014)에서 V46·shop-router·K0006 모두에 대해 마진 −0.9~−2.1k로 뒤집힌 사례다(다음 개발의 단서).

## 3. 남은 패배 원인 (다음 개발 대상 후보, 하나만 고를 것)
- **V46형 하드 포크에 대한 구조적 열세**: base19가 arena final에서 V46에 평균 −3.9k(중앙 −3.5k, ±2k 이내 8/32), 패널 0/16, 라이브 동결 V46 경기 −16.9k. MX2·p002 어느 쪽도 이 벽을 움직이지 못했다. 다음 개발은 이 한 상대군의 실제 패배 메커니즘(같은 세계 원장: 딸기·우유 물량과 판매 시점, d10 멜론, 축군 규모)을 대상으로 한다.
- MX2 실패 세계 44142014의 원장 분해(왜 MX2의 보류 판매가 손해였는지)는 MX2를 다시 후보로 올릴 때의 첫 분석 항목.

## 4. 기록·파일
- arena: `reports/o-arena-v1b-mx2-results-2026-09-18.ko.md`; 캠페인 `state/agent_experiments/arena_p001mx2_{screen_v1b,confirm_v1b,final_v1c}` (+ 중단된 `arena_p001mx2_screen`, `arena_p001mx2_final_v1b` 보존), 설정 `configs/validation/live_weighted_arena_v1{b,c}_p001mx2.json`, 래퍼 `state/o_dev/opponents/{dmitrii_lb2700_bundle,o227_stealth_arena}.py`(+`.check.json`).
- B: `reports/o-p002-B-verdict-2026-09-18.ko.md`, `o_results/mx/eval_*_r5.json`, `o_results/mx/p002_report_B_2026-09-18.txt`.
- D: `state/agent_experiments/panel_p002_screen/results.json`, `o_results/panel_p002_screen_report.txt`. C: `o_results/elite_pool/eval_lb_{cow1,cow1_mx2}.json`, `o_results/elite_pool/lineage_report_2026-09-18.txt`.
- 후보 파일은 그대로(`agent/p001_mx2.py` 448d6115…, `agent/p002_cow1.py` f1ca4735…, `agent/p002_cow1_mx2.py` 88991c8e…).
