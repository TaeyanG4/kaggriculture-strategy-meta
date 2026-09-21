# arena v1b — p001_mx2 vs base19 판정 기록 (2026-09-18, 실행 Claude)

설정 `configs/validation/live_weighted_arena_v1b_p001mx2.json` = v1 + `dmitrii-lb2700`을 행동 동일 단일 파일 번들로 교체(실행 오류 수정만; 상대·가중치·seed·규칙 불변). 1차 v1 캠페인(`arena_p001mx2_screen`)은 dmitrii 다중 파일 로더가 runner의 단일 파일 스냅샷에서 step 0 FileNotFoundError → 0/320, 기록 보존. 규칙 R1–R5는 `reports/o-p001-mx2-arena-plan-2026-09-18.ko.md`에 실행 전 고정.

## Screen (8 seeds × 10 상대 × 2 좌석 × 2 모델 = 320, 21:21–21:28)
- 건전성: 320/320 완료, 실패 0, 타임아웃 0, health failure 0, 최대 결정 시간 후보 0.23 s / 상대 0.72 s(actTimeout 1 s), 게임당 평균 8.5 s. 해시 전후 PASS(contract ca08fb0e60c6, config 51329346a9fe, `hashcheck-2026-09-18T122052Z/122808Z.json`).
- **primary p001-mx2 vs base19-planner**: family 가중 point delta **+0.037**, bootstrap CI **[0.00, 0.15]** → `inconclusive`(음수 아님). pooled paired margin **+402**, own **+2,234**, W→L 1, L→W 5, 승 48 → 54 / 160.

| 상대 (cluster) | n | base19 WR | MX2 WR | paired margin Δ (se) | own Δ | W→L / L→W |
|---|---|---|---|---|---|---|
| nagata-scheduler (c1) | 16 | 1.00 | 1.00 | +1,379 (1,484) | −250 | 0 / 0 |
| dmitrii-lb2700 (c1) | 16 | 0.31 | 0.25 | **−1,375** (1,275) | +1,436 | **1** / 0 |
| v46-reacting (c2) | 16 | 0.12 | 0.12 | +1,625 (706) | +3,332 | 0 / 0 |
| jaxa-k0006 (c2) | 16 | 0.12 | 0.12 | +966 (834) | +3,364 | 0 / 0 |
| v48-fast-climber (c3) | 16 | 0.94 | 1.00 | −318 (1,220) | +3,066 | 0 / 1 |
| shop-router-v5 (c3) | 16 | 0.00 | 0.12 | +1,088 (674) | +1,756 | 0 / 2 |
| v37-more-yield (c4) | 16 | 0.25 | 0.25 | −508 (997) | +1,794 | 0 / 0 |
| ahmed-v38 (c4) | 16 | 0.25 | 0.25 | +128 (799) | +4,272 | 0 / 0 |
| c129-benchmark (c5) | 16 | 0.00 | 0.12 | −386 (698) | +1,758 | 0 / 2 |
| o227-stealth (c5) | 16 | 0.00 | 0.12 | +1,421 (809) | +1,814 | 0 / 2 |

- 클러스터(설명용 가중치): elite +2 / own +593 (dmitrii −1,375 vs nagata +1,379), forks **+1,295** / +3,348, climbers +385 / +2,411, tapes **−190** / +3,033, anchors +518 / +1,786 → **가중 마진 +480, 가중 point +0.016**.
- 규칙: **R1 PASS**(inconclusive, 음수 아님) · **R2 PASS**(c2+c3 상대별 W→L ≤ L→W, pooled 마진 +) · **R3 PASS**(c1 마진 +2 ≥ 0, own +593 ≥ 0 — 마진은 간신히) · **R4 PASS**(anchors +518) · R5 기록만(v37 −508, v38 +128). **OVERALL PASS → confirm 진행.**
- 가장 크게 악화된 상대군: cluster4(v37 −508); 상대 단위 최악: dmitrii-lb2700 −1,375 (유일한 W→L). 참고: base19 자체의 이 arena 승률은 0.30(dmitrii 0.31·V46/K0006 0.12·shop-router/c129/o227 0.00) — MX2는 own을 +2.2k 올리지만 승패는 거의 바꾸지 못한다(+6승/160).

## Confirm (8 seeds, alpha .015, 320 games, 21:29–21:39)
- 건전성: 320/320, 실패 0, 타임아웃 0, 해시 전후 PASS(contract 79d266a32c68).
- **primary**: family 가중 point delta **+0.006**, CI [0, 0.025] → `inconclusive`; pooled paired margin **+1,166**, own +2,021, W→L 0, L→W 1.

| 상대 (cluster) | n | base19 WR | MX2 WR | paired margin Δ (se) | own Δ | W→L / L→W |
|---|---|---|---|---|---|---|
| nagata-scheduler (cluster1) | 16 | 1.00 | 1.00 | +1,142 (880) | +1,805 | 0 / 0 |
| dmitrii-lb2700 (cluster1) | 16 | 0.25 | 0.31 | +730 (807) | +4,801 | 0 / 1 |
| v46-reacting (cluster2) | 16 | 0.25 | 0.25 | +623 (565) | +925 | 0 / 0 |
| jaxa-k0006 (cluster2) | 16 | 0.25 | 0.25 | +3,398 (675) | +930 | 0 / 0 |
| v48-fast-climber (cluster3) | 16 | 1.00 | 1.00 | +1,168 (1,022) | +1,831 | 0 / 0 |
| shop-router-v5 (cluster3) | 16 | 0.25 | 0.25 | +1,744 (613) | +36 | 0 / 0 |
| v37-more-yield (cluster4) | 16 | 0.25 | 0.25 | +635 (781) | +4,853 | 0 / 0 |
| ahmed-v38 (cluster4) | 16 | 0.25 | 0.25 | +614 (760) | +4,813 | 0 / 0 |
| c129-benchmark (cluster5) | 16 | 0.38 | 0.38 | +87 (503) | +297 | 0 / 0 |
| o227-stealth (cluster5) | 16 | 0.25 | 0.25 | +1,519 (528) | -76 | 0 / 0 |

- 클러스터: elite +936 / own +3,303, forks +2,011 / +927, climbers +1,456 / +933, tapes +624 / +4,833, anchors +803 / +111 → 가중 마진 +1,292, 가중 point +0.011.
- 규칙: R1 PASS(inconclusive) · R2 PASS · R3 PASS · R4 PASS · R5 기록(v37 +635, v38 +614). **OVERALL PASS → final(16 seeds) 진행.** 마진은 10/10 상대에서 +, 승률 변화는 +1/160.

## 최종 blind 검증 설계 (final·C·D 결과를 보기 전에 고정, 21:50)
- 대상: `state/o_dev/p001_mx2.py`(448d6115…) vs 기준 `state/o_dev/p000_base19.py`(53d80342…). 후보·기준 파일은 변경하지 않는다.
- seed: **7240–7255**(16개, 미사용 확인: 상점 시퀀스 캐시·결과 파일·캠페인 manifest에 없음). 이 block은 이 한 번의 평가에만 쓴다. 결과를 보고 후보를 고치면 이 block은 개발 자료가 되고 수정 후보에는 다음 block(7256–7271)이 필요하다. 실패해도 재실행·은폐하지 않는다.
- 상대·도구(기존 도구 그대로, 8워커): (a) `o_tools/proxy_eval.py --a agent/o227_stealth_drop.py --seeds 7240-7255` 양좌석(핀 고정 세계는 이 실행이 처음 생성; 기준·후보 각 32경기), (b) `o_tools/mx_eval.py --seeds 7240-7255 --opps v46,k0006,v48,router_v5`(각 32경기, 기준·후보 각 128경기). 총 320경기.
- 판정(사전 고정): **B1** 후보−기준 pooled paired margin ≥ 0 **및** own ≥ 0(o227 32 + 반응형 128 = 160쌍); **B2** pooled W→L ≤ L→W; **B3** 상대 5종 중 paired margin < −1,000인 상대 없음. B1–B3 통과 시 제출 패키지(파일 바이트 동일 `main.py`), 미달 시 "제출 권고 없음, base19 유지".
- 진입 조건: arena final R1–R4 PASS, C·D에서 MX2 vs base19의 router 계보 회귀 없음(D의 router_tschinkel family W→L ≤ L→W, pooled margin ≥ 0).

## Final (16 seeds, alpha .025, 640 games, v1c = v1b + o227 telemetry 래퍼, 21:54–22:06)
- 1차 final(v1b)은 437/640에서 중단: base19 vs o227(seed 1382149642, 좌석0)에서 o227의 자기점검 카운터 `overflow_contract_errors`=1 → runner health 규칙이 게임을 invalid 처리. o227 원문 + 그 키만 개명하는 래퍼(`state/o_dev/opponents/o227_stealth_arena.py`, 4경기 행동 동일 검증)로 v1c 구성, 다른 상대·가중치·seed·규칙 불변. 중단 캠페인은 보존(판정에 미사용).
- 건전성: 640/640, 실패 0, 타임아웃 0, health 0, 최대 결정 0.146 s, 해시 전후 PASS(contract 9142da46140a).
- **primary**: family 가중 point delta **+0.034**, CI [-0.047, +0.103] → `inconclusive`; pooled paired margin **+992**, own +1,389, W→L 7, L→W 18.

| 상대 (cluster) | n | base19 WR | MX2 WR | paired margin Δ (se) | own Δ | W→L / L→W |
|---|---|---|---|---|---|---|
| nagata-scheduler (cluster1) | 32 | 1.00 | 1.00 | +1,937 (694) | +2,060 | 0 / 0 |
| dmitrii-lb2700 (cluster1) | 32 | 0.47 | 0.53 | +1,028 (476) | +984 | 0 / 2 |
| v46-reacting (cluster2) | 32 | 0.34 | 0.28 | -352 (344) | +230 | 2 / 0 |
| jaxa-k0006 (cluster2) | 32 | 0.38 | 0.41 | +1,966 (346) | +2,219 | 2 / 3 |
| v48-fast-climber (cluster3) | 32 | 0.94 | 0.94 | +517 (791) | +1,364 | 1 / 1 |
| shop-router-v5 (cluster3) | 32 | 0.50 | 0.47 | +1,984 (502) | +2,796 | 2 / 1 |
| v37-more-yield (cluster4) | 32 | 0.25 | 0.38 | +515 (485) | +306 | 0 / 4 |
| ahmed-v38 (cluster4) | 32 | 0.25 | 0.38 | +570 (416) | +370 | 0 / 4 |
| c129-benchmark (cluster5) | 32 | 0.53 | 0.59 | +1,228 (486) | +2,173 | 0 / 2 |
| o227-stealth (cluster5) | 32 | 0.34 | 0.38 | +527 (258) | +1,388 | 0 / 1 |

- 클러스터: elite +1,483 / own +1,522, forks +807 / +1,225 (point −0.016), climbers +1,250 / +2,080 (point −0.016), tapes +542 / +338 (point +0.125), anchors +878 / +1,780 → 가중 마진 +1,091, 가중 point +0.021.
- 규칙: R1 PASS(inconclusive) · **R2 FAIL**(V46 W→L 2 > L→W 0, shop-router-v5 W→L 2 > L→W 1; c2+c3 pooled 마진은 +) · R3 PASS · R4 PASS · R5 기록(v37 +515, v38 +570, 각 L→W 4). **OVERALL FAIL → arena gate 불통과. 규칙·가중치·상대·seed는 바꾸지 않는다.**
- 해석: MX2는 세 단계 모두 own(+1.4~2.2k)·마진(+0.4~1.2k)을 올리지만 승률 효과는 +0.006~+0.037로 CI가 0을 포함하고, 최종 단계에서 하드 반응형 포크(V46 0.34→0.28)와 shop-router-v5에서 W→L이 L→W를 넘었다. 시장 실행기의 이득은 "더 많이 벌기"이지 "지는 경기를 이기기"가 아니다.
