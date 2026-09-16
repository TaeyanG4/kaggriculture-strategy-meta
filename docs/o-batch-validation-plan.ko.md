# 좁은 개입(narrow intervention) 배치 검증 계획 — 장기 부재 시 실행용 (2026-09-15 작성)

> 검증 절차 자체는 `docs/o-validation-process.ko.md`(v1)를 따른다. 이 문서는 실행 큐와 판정 기록용.

## 목적
c150(불변 부모) 위에 역공학으로 검증된 결정 규칙을 **하나씩** 얹어 c150 대비 달러 효과를 재고, 통과한 것만 조합해
제출 후보를 만든다. 목표 기준: 엘리트 스위트 c150 대비 평균 마진 +3,000 이상, 패→승 40/88 이상, 다양 상대 풀 회귀 0.

## 실행 명령 (한 번에, 약 2시간; 진행바·남은 시간 표시)
```powershell
& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\o_tools\run_batch.ps1'
```
- 후보 지정: `-Candidates @("tag=agent\file.py", ...)`; 스위트만 빠르게: `-SkipPool`(~40분).
- 이미 완료된 후보(스위트 88경기 / 풀 `_summary.json`)는 자동으로 건너뜀. 중단 후 재실행해도 이어서 진행.
- 마지막 SUMMARY 블록을 `o_results/batch_<날짜>.txt`로 저장해 두면 다음 세션에서 그 파일만 읽으면 된다.

## 1차 배치 (구현 완료, 성능 미검증)
| tag | 파일 | 규칙 | 근거 |
|---|---|---|---|
| o159b | agent/o159b_feed_margin06.py | 급식 한계가치 게이트(0.6·밀) | 스위트 +902 확인, 풀 미검증 |
| o161 | agent/o161_harvest_only.py | CARE→HARVEST(거위≥3, 소/양≥5), 급식 없음 | 2×2 분리용 |
| o162 | agent/o162_goose_only.py | o159b + 거위만 수확 | o160의 승→패 8건 원인 분리 |
| r000 | agent/r000_terminal_hold.py | 26~27일 딸기/토마토/양모 보유 → 29일 분할 매도 | 1위 종반 +5.2k 메커니즘 |
| c155 | agent/c155_milk_externality.py | c132 급식 생략 + 우유 가격 외부효과 게이트 | 설계 담당 검증 대기 |

## 2차 배치 (아직 구현 전 — 1차 결과 뒤 순서 결정)
1. 6일차 거위-대-소 규칙: step ~151에서 BAKERY/BRUNCH/PET_CAFE 세계면 COW→GOOSE(V231 치환 구조 재사용). 근거: 최초 분기 9경기 평균 −5.3k(상관).
2. 종반 시비 확대: EXP182 `_R51_INPUT_MAX_WORKERS` 2→3, 가치비 1.5→1.2 스윕. 근거: 상대 FERTILIZE +9회/게임.
3. 분할 매도: R36/R37 예약 판매 배치를 줄여 더 많은 스텝에 분산. 근거: 상대 우유 단가 $93 vs $80.
4. 토마토 투기 파종: 상점 0~1개에도 8~10일차 4~8칸(V219 게이트 완화, SE 미구매). 근거: 1위 토마토 +4.3k(상관, 가장 불확실).

## 조합 단계
1·2차에서 통과(스위트 양수·풀 회귀 0)한 규칙끼리 `o_tools/build_overlay.py --parent agent/c150.py --overlay A --overlay B ...`로
묶어 같은 배치를 다시 돌린다(ablation: 전체 − 하나씩 뺀 버전). 상쇄가 있으면 그 쌍은 분리 유지.

## 판정 후
- 기준 통과 → `o_progress.md`에 근거 기록 후 제출 여부 결정(사용자 승인 필요).
- 토마토까지 넣어도 +1,500 미만 → 좁은 개입 한계로 보고 실행기(수확 동선·시비) 개선으로 전환.

## 관련 파일
- 스위트: `o_replays/elite_chunks/`(88경기, 불변), 기준 `o_results/elite_suite/c150/`, 요약 `o_tools/suite_summary.py <tag> c150`
- 풀: `o_tools/diverse_pool.json`, 기준 `o_results/diverse_vs_c150/`, 비교 `o_tools/compare_pool_results.py`
- 역공학 근거: `reports/r000-leader-reverse-engineering-2026-09-15.ko.md`, `reports/r001-leader-level2-clone-2026-09-15.ko.md`
- 주기 크롤러(선택): `o_tools/r_crawl.py` → `o_results/r_crawl/latest_summary.md`

## 추가 (2026-09-15 저녁): "우리가 위"라는 가정 폐기
- 공개 상위 노트북은 2주 만에 우리 계보와 동급이 됨: Farming Score V4(2670)·Market-Smart Farming(2656) 최신판은 c150 상대 8경기에서 2승 6패, 마진 −500대(09-02 구버전은 −2,800/−6,900).
  풀의 두 항목을 09-15 최신판으로 교체함(`o_tools/diverse_pool.json`).
- c129 2820은 09-13 시점 레이팅. 최종 판정에 **최신 공개 트리오(shop-router-v5·Farming Score V4·Market-Smart) paired 양의 마진(CI 하한>0)** 조건 추가.
- 제출 전 `o_tools/r_crawl.py`로 최신 라이브 패배(2750+)를 받아 스위트를 보강할 것(`o_replays/elite_losses_new/`).
