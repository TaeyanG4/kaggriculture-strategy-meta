# o/r 시리즈 검증 프로세스 (v1, 2026-09-15) — 참고용, 강제 아님

Claude(o/r 시리즈) 세션이 쓰는 후보 검증 절차다. 다른 세션(Codex c-시리즈 등)은 자기 검증기를 그대로
쓰면 되고, 이 문서는 결과를 서로 읽을 때의 기준을 공유하기 위한 것이다. 기존 공통 검증기
(`tools/run-validation.ps1`, `validation_v1.py`)를 대체하지 않는다.

## 한 줄 요약
후보 = 불변 부모(c150) + 오버레이 1개. **① 엘리트 스위트 88경기 → ② lean 풀 21상대** 두 관문을 통과한 것만
조합(ablation)하고, 조합본이 다시 두 관문을 통과하면 제출 검토.

## 관문 ① 엘리트 스위트 — "점수를 결정하는 상대에게 효과가 있나"
- 데이터: 우리 라이브 제출본(c129/c146/c147/c152)이 **레이팅 2750+ 상대에게 진 88경기** 기록 (`o_replays/elite_chunks/`, 불변).
- 방식: `replay_lab` 고정상점·동결상대. 상대는 기록 행동을 반복, 우리 자리만 후보로 교체해 720스텝 재생. 시드·상점·상대가 같으므로 경기별 paired 비교.
- 판정: c150 대비 paired delta의 **부트스트랩 95% CI 하한 > 0**(`o_tools/suite_summary.py <tag> c150`). sd≈1,000/경기라 +300 이상이면 검출됨.
- 한계: 상대가 반응하지 않음 → 가격 외부효과(급식 생략→우유가 상승→상대 이득)나 상대의 전략 변경은 못 봄. 그래서 관문 ②가 필요.

## 관문 ② lean 풀 — "반응하는 상대에서 회귀가 없나, 동급 상대에 우위가 있나"
- 상대 21개 (`o_tools/pool_lean.json`), 8시드 × 양 좌석 = 상대당 16경기, c150 기준선(`o_results/pool_pool_lean_vs_c150/`)과 같은 시드.
  - A 동급·최근접 8: Farming Score V4·Market-Smart(09-15 최신판), shop-router-v5, yhay81-0913, v34, smaller-market-shock, harvest-nocturne, tschinkel v5/v55
  - B 우리 옛 챔피언 5: c125·c129·c146·c147·c152
  - C 카나리아 7: v35/36/38/39/40, aurax7-v4, yhay81-0911-simple (쉬운 상대지만 o155의 −5만~−8만 역전을 잡아낸 상대)
- 판정: (a) 어떤 상대에서도 delta ≤ −1,000 회귀 없음, (b) A그룹 중 최신 공개 트리오(shop-router-v5·Farming Score V4·Market-Smart)에 양의 delta.
  (`o_tools/compare_pool_results.py <c150 dir> <cand dir>`)
- 왜 풀을 줄였나: 원래 46개 중 25개는 c150이 −2만~−12만으로 이기고 어떤 변경에도 움직이지 않아 정보가 없었다. 필요하면 `o_tools/diverse_pool.json`(51개 전체)로 되돌릴 수 있다.

## 특수 검증: 세계별 시드 은행 — 필요할 때만 (2026-09-15 추가, 기본 관문 아님)
- `o_tools/world_bank.json`: 첫 4상점으로 분류한 시드(goose / one_milk / two_milk / yarn 배타, carrot / tomato 태그) 버킷당 36개.
- `python o_tools/stratified_pool.py run <tag> <agent.py>` → 상대 4(c150 미러·V43·Farming Score V4·Market-Smart) × 양좌석 × 버킷 시드, 결과 캐시 `o_results/strat/<tag>/`.
- `python o_tools/stratified_pool.py compare <tag> <base>` → 버킷별 paired delta·부트스트랩 CI·승수·상대별 delta. 엘리트 스위트가 못 보는 "미해결 세계(one_milk, yarn)"의 표본을 확보하는 용도. **기본 절차(스위트→풀→홀드아웃)에는 포함하지 않고**, 특정 세계를 겨냥한 후보이거나 스위트에 그 세계 표본이 부족할 때만 쓴다.

## 실행 (v2, 2026-09-15 저녁: 경량화)
```powershell
& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\o_toolsalidate.ps1' -Tag o2xx -File agent\o2xx.py -Base o199c
```
- 순서: 스위트 88 → **조기 기각 게이트**(CI 상한 < +50이면 중단, ~1.5분) → 빠른 풀(`pool_fast.json` 10상대: 공개 트리오·V43·FSV5·c129·c152·yhay 0913·tschinkel v55·카나리아 1) → 홀드아웃 40. 통과 후보만 ~5분, 기각은 1.5분.
- 왜 줄였나: lean 풀 23상대 중 카나리아 6개는 5만점대 압승이라 정보가 없고, 옛 챔피언 5개는 결과가 동일(c129·c146·c147·c152 같은 수치). 시드 은행·32시드 풀은 최종 후보에만.
- 판정: 스위트 CI 하한>0 → KEEP; CI가 0을 걸치면 풀 회귀 0·홀드아웃으로 결정; **승수 감소는 마진과 무관하게 기각**(o203 교훈).

## 실행 (v1)
```powershell
$r='H:\dev\kaggle-data\kaggriculture-strategy-meta'; & "$r\o_tools\run_batch.ps1" -Candidates @("tag=agent\file.py", ...)
```
- 스위트 ~1.5분(12청크 `o_replays/elite_chunks12/` + 원본 재현 캐시 `o_results/_verify_cache/`, `KAGG_VERIFY_CACHE`로 켜짐) + 풀 ~4분(12워커) = 후보당 약 6분. 옛 결과(c0..c5 6청크)는 그대로 유효(요약은 `c*` 글롭). 완료된 항목은 자동 건너뜀(중단 후 재실행 가능). `-SkipPool`로 스위트만, `-Pool o_tools\diverse_pool.json -Seeds 12`로 전체 풀.
- 마지막 SUMMARY 블록을 `o_results/batch_<이름>.txt`로 저장하면 다음 세션은 그 파일만 읽으면 된다.

## 표본과 검정력 (왜 이 설계인가)
- 게임은 결정적이라 같은 시드·같은 두 에이전트는 항상 같은 결과다. 반복은 **시드·상대 축**으로만 정보가 늘어난다.
- paired(같은 시드·상대·자리에서 후보 vs c150) delta의 sd≈1,000이므로 88쌍이면 SE≈105 → +300 효과 검출. 독립 표본이면 수천 경기가 필요하다.
- lean 풀은 상대당 16경기(SE≈250~500)라 **상대별 미세 순위는 읽지 않고** −1,000 이하 회귀 탐지에만 쓴다.
- 최종 후보의 최신 공개 트리오 우위는 **시드 32~64개**로 따로 확인한다(`tools/o_arena.py <cand> <trio> --seeds 32`, ~10분).

## 판정 규칙 요약
| 단계 | 조건 |
|---|---|
| 단독 후보 KEEP | 스위트 CI 하한 > 0 AND 풀 회귀 0 |
| 조합 | KEEP끼리 묶고, 전체−하나씩 뺀 ablation으로 상쇄 확인 |
| 제출 검토 | 조합본 스위트 c150 대비 +3,000·패→승 40/88 AND 풀 회귀 0 AND 최신 공개 트리오 양의 delta; 제출 전 `o_tools/r_crawl.py`로 최신 2750+ 패배를 받아 스위트 보강 |

## 알려진 함정 (실측)
- 스텝0/오프닝 변경은 lockstep 시장 때문에 상대 현금을 몇 달러 바꿔 상대 정책의 분기를 뒤집는다(o155: 미러전 156/160 승 → 풀에서 10/44 상대 −5만 이상). 미러전만으로 판단 금지.
- 오버레이가 공유 자원(밀·비료·일꾼)을 건드리면 다른 오버레이가 무효화된다(o152: 비료 2개 판매 → EXP182 시비 no-op, −5k~−10k).
- 급식 생략은 가격 폭락 구간에서 동물을 버리면 안 된다(o158 −15k → o159 폐기 조건 제한 후 +900).
- 1,600경기 계보 아레나의 승점률 차이 3~4%p는 SE≈2%p라 유의하지 않다. 후보 간 순위는 스위트 paired CI로 본다.
- 로컬 무패 ≠ 라이브 우위: 공개 상위 노트북은 2주 만에 동급이 됐다(Farming Score V4·Market-Smart 최신판 c150 상대 2승 6패 −500대). 우리 라이브 레이팅(09-13 시점)을 현재 우위의 근거로 쓰지 않는다.

## 산출물 위치
- 스위트 결과: `o_results/elite_suite/<tag>/c0..c5/results.json` · 풀: `o_results/pool_pool_lean_vs_<tag>/`
- 후보 원장: `o_experiments.jsonl` · 진행 요약: `o_progress.md` · 역공학 근거: `reports/r000-*.md`, `reports/r001-*.md`

## v3 추가 (2026-09-16) — 게이트 확장과 판정 원칙
- **관문 ③ 32시드 풀(최종)**: `o_tools/pool_lean32.json` 23상대 × 32시드 × 양좌석 = 1,344경기(`run_batch.ps1 -Seeds 32`). 판정은 승수 우선(W→L 0), 마진은 그다음.
- **관문 ④ 세계 은행(특수)**: 세계 조건부 규칙은 해당 버킷(`stratified_pool.py --buckets`)에서 SIG+이어야 한다.
- **관문 ⑤ 동결 Majkel(1위 정책 상대)**: `replay_lab --mode fixed_shops_frozen_opponent_weeds`로 Majkel 289경기 재생(상점·Majkel 잡초 원본 고정). Majkel 현금이 원본보다 ~15% 낮으므로 후보 간 paired 비교에만 사용. 기준: c150 65%/+19.5k, o227 70%/+21.0k. 세계 부분집합(PET·PIZZA)으로 세계 조건부 후보 스크리닝.
- **관문 ⑥ 고정 세계 A/B**: `o_tools/proxy_eval.py`(상점 순서 시드별 고정) — 엔진 상점 추첨이 양 농장 타일 점유에 의존하므로 고정 없이는 같은 시드도 다른 세계가 된다.
- **원칙 추가**: (a) 동결 스위트만의 +는 채택 근거가 아니다(o220: 스위트 +71, 반응형 풀 W→L 6). (b) 대칭 개선(양쪽 다 나아져 미러 마진에 안 보이는 것)은 절대 현금·V44 승률·동결 Majkel로 본다. (c) 공급 축소·보류류 변경은 미러 외부효과로 항상 손해였다(V233 제거 −2.2k, 비료 보류·매도 지연 무효) — 산출 추가와 비대칭 타이밍만 시험한다. (d) 상대 감지기가 있는 공개 메커니즘(V44 race arm)에는 이식이 아니라 트리거 은닉으로 대응한다(o227).
