# 라이브 주류 빌드("B13/S8·S9") 출처 추적 (2026-09-18)

대상: `o_replays/live_frozen/live_b19/` 117경기(base17/base19 라이브)의 상대 117개 제출물. 방법: (1) 리플레이 ↔ 에피소드 메타데이터(`o_results/live_episodes_*.json`: agents→submissionId/teamId, submissions.dateSubmitted, teams.teamMembers)를 연결(117/117), (2) 보유한 공개 에이전트(공개 노트북 pull `state/o_dev/public_pull*`, donor 데이터셋 `state/o_dev/datasets/donor_agents/`, arena 상대)의 **첫 6개 시장 턴 지문**(seed 7000, PASS 상대, 좌석 0)과 라이브 상대의 첫 6턴을 대조, (3) 지문이 일치한 후보는 **라이브 에피소드를 후보 코드로 재생**(우리 행동 동결, `live_replay_audit.play`)해 720스텝 동일 여부로 검증. 도구: `o_tools/rival_source_trace.py`, 결과 `o_results/rival_source_trace.json`, `o_results/live_pool_groups.json`, `o_results/live_pool_trace.json`. 이번 추적에서 공개 노트북 2개를 추가로 pull(`state/o_dev/public_pull_4/`: yhay81 fieldbook, thomastschinkel 74.5%).

## 1. 결과: 개통 패턴 → 출처
| 그룹 (첫 6턴) | n | 출처 | 검증 |
|---|---|---|---|
| **C** `B13 ∥ S8,B7,HIRE×5,COW2,SHEEP2 ∥ S1 ∥ B29,S29,B1,MEL1 …` | 7 | Thomas Tschinkel, *93.8% Win Rate Public State Router* (`thomastschinkel/kaggriculture-93-8-win-rate-public-state-router`, 2026-09-07, main.py sha256 b87a27ed614a3332…, 보유 사본 `donor_agents/agents/tschinkel-router-v5.py` = 노트북 `%%writefile main.py` 셀과 동일 sha) | **Sybery_AI(ep 110295006) 720스텝 완전 동일**(최종 현금 103,869=103,869); trung(ep 110296106) 1스텝 차이(라이브에 `SELL WHEAT 0` 무효 주문 추가, 최종 현금 동일) → 같은 노트북의 사소한 변형. 95.5% 판(v5.5, sha 82412467…)은 d6 h21부터 갈라짐(다른 판) |
| **B** `B13 ∥ S9,B7,MEL12,HIRE×5,COW2,SHEEP2 ∥ . ∥ S1,B1 ∥ B1 ∥ S2,B1` | 8 | Thomas Tschinkel, *Public State Router (74.5%)* v3.1(`…-public-state-router-74-5-win-rate`, 2026-09-05, sha 197b1ceef97d2ee2… = 현재 판; y3uanm *market-impact-router-v4*도 같은 지문) | NiuLAI d6 h7부터 6스텝 차이(최종 88,646 vs 84,697), Foxure d25 h0부터 2스텝 차이 → **같은 계보의 다른 판/포크**(정확 재현 아님) |
| **A** `B13 ∥ S8,B7,MEL12,HIRE×5,COW2,SHEEP2 ∥ S1 ∥ B1 ∥ S1,B1 ∥ S1,B1` | 13 | fieldbook 코어(아래 F) + B13/S8 밀 왕복 접두. 보유 파일 중 정확 일치 없음. 최초 관측 제출 2026-09-04(Anna Currie 56007353) → 74.5% 노트북(09-05) 이전이므로 **thomastschinkel 초기 판(v2.x) 또는 yhay81 fieldbook 파생**으로 추정. Kaggle API는 과거 판을 주지 않아 **판 미확보** | 미검증 — "동결 테이프형"으로 유지 |
| **F** `. ∥ B5,B7,MEL12,HIRE×5,COW2,SHEEP2 ∥ S1 ∥ B1 …` | 10 | yhay81 *Fieldbook: Commit for Three Days*(2026-09-01; 테이프는 비공개 데이터셋, 출발점은 Milan Leonard 공개 에피소드 102248386) → flexonafft 재공개 *Adaptive Farm Intelligence*(donor `flexonafft-fieldbook-*`, sha d0b7ec84…/71bb7c8f…) | 4경기 6턴 지문 일치, 재생은 d0 h2 일손 주문 표기(`PICKUP COW` vs `PICKUP COW 1`)부터 차이 → 같은 계보의 다른 판 |
| **N** `B{16,30,43,45,52,53} ∥ S{N−5},…,B7,MEL12` | 17 | 밀 왕복 크기 N만 다른 변형(코어는 fieldbook형 `B7,MEL12` 또는 router형 `HIRE×5,COW2,SHEEP2`): boatlee *v29-r1-adaptive-market-hysteresis*(B53, sha c4a6964c…: dengddd/Kronki 6턴 일치, d6–d9부터 차이), prvsiyan *where-the-wheat-remembers-tomorrow*(B45) 등 | 계보 확인, 정확 판 미확보 |
| **X** `[B13,S13,B13]`/`[B5,B10,S60]`/`[B13,B30,S30]` 계열 | 7 | ahmedberatozer V4x / yhay81 shop-router / dmitriigluzdov lb2700 계보(arena의 shop-router-v5·ahmed-v38·dmitrii-lb2700이 이 계열) | bobodict/Shiru2: dmitrii lb2700 main.py와 d6 h0까지 동일 후 분기 |
| **V** v48 계열 `B4,HIRE,HIRE,MEL7,B5,SHEEP4` | 9 | kaitofukami v48 fast routes 계보(`state/o_dev/v48_public.py`) | 6턴 일치 5경기, d5/d10부터 차이(변형) |
| **P** `HIRE×5,COW2,SHEEP2,B7,MEL12,B6` | 9 | boatlee *v21-r1-public-state-route-portfolio* 계보 | d0 h1부터 차이(S2 vs S3) |
| **W** `B7,S2 ∥ B30,… ∥ S30` | 1 | V46(`state/o_dev/v46_public.py`) | **neibyr(ep 110208980) 720스텝 완전 동일** |
| O 기타 | 36 | 소량 패턴 다수 | — |

결론: 라이브 주류 "B13/S8·S9"는 **공개 노트북 테이프 라우터**(Thomas Tschinkel의 Public State Router 계열 v3.1/v5/v5.5 + yhay81 ShopForge Fieldbook 파생)이며, 반응형 강자가 아니다. 이들은 720턴 녹음 테이프를 재생하고 **고정 턴(144/216/226/360/433)에 공개 상태(개방 상점, 특정 상품 가격·재고)로 꼬리 테이프를 고른다**. 상대 행동에 직접 반응하지 않지만 **가격 트리거(예: 74.5%판 "턴 360 당근가 ≥ 42 → 당근 꼬리", "턴 433 우유 재고 ≥ 10067 → 우유 꼬리")는 우리 판매로 영향받을 수 있다** → 동결 풀 결과는 "우리가 상대의 꼬리 선택을 바꾸지 않는 한" 정확하며, MX2처럼 우유·딸기 판매 시점을 옮기는 후보는 이 트리거를 건드릴 수 있다(동결 풀의 한계로 기록).

## 2. 그룹별 동결 풀 성적 (기존 `eval_lb_*` 결과 재집계, 새 시뮬 없음)
| 그룹 | n | base19 승/마진 | MX2 승/마진 (Δ) | 미러 승/마진 (Δ) |
|---|---|---|---|---|
| C router v5 (검증됨) | 7 | 3/7 −1,696 | 4/7 +1,663 (+3,359) | 3/7 −1,088 (+608) |
| B 74.5% 계보 | 8 | 4/8 +6,124 | 4/8 +9,624 (+3,499) | 4/8 +6,298 (+174) |
| A fieldbook+B13/S8 | 13 | 9/13 +5,007 | 9/13 +5,731 (+724) | 9/13 +5,134 (+127) |
| F fieldbook 코어 | 10 | 8/10 +8,233 | 9/10 +9,763 (+1,530) | 10/10 +10,894 (+2,662) |
| N 왕복 N+코어 | 17 | 7/17 −32 | 8/17 +1,709 (+1,741) | 14/17 +11,882 (+11,914) |
| X V4x/shop-router | 7 | 2/7 −5,769 | 2/7 −2,850 (+2,919) | 2/7 −7,209 (−1,440) |
| V v48 계열 | 9 | 9/9 +22,085 | 9/9 +23,537 (+1,453) | 8/9 +18,140 (−3,945) |
| P v21-r1 계열 | 9 | 9/9 +19,957 | 9/9 +22,661 (+2,704) | 8/9 +14,239 (−5,719) |
| W V46 | 1 | 0/1 −16,886 | 0/1 −15,467 (+1,419) | 0/1 −22,200 (−5,314) |
| O 기타 | 36 | 25/36 +16,448 | 26/36 +18,490 (+2,042) | 27/36 +17,158 (+711) |

읽는 법: base19가 지는 곳은 **C(router v5, 3/7)·N(왕복 N+코어, 7/17)·X(V4x 계보, 2/7)·V46**이다. MX2는 모든 그룹에서 마진을 올리지만(+0.7~+3.5k) 승패를 거의 뒤집지 못한다(C 3→4, N 7→8, F 8→9). 미러는 N(+11.9k, 7→14승)·F에서만 크고 V/P/X/V46에서는 손해(미러의 상대 의존성 재확인).

## 3. 시사점 (arena·후속)
- arena v1의 상대 10종에는 **C(Tschinkel router v5)와 fieldbook 계보(A/F/N, 합 40/117 = 34%)가 없다**. router v5는 라이브 720스텝 재현이 검증된 파일(`donor_agents/agents/tschinkel-router-v5.py`)이 있으므로 다음 arena 판(v2)에 넣을 1순위 후보다(v1 설정은 이번 arena가 끝날 때까지 바꾸지 않는다).
- 그룹 A(13경기)의 정확 판은 미확보 → "동결 테이프형(fieldbook 계보)"으로 표기 유지. 확보 경로: 해당 팀들의 공개 노트북 포크 목록(`kaggle kernels list --user <username>`), 또는 thomastschinkel 노트북의 과거 판(웹 UI에서만 열람 가능).
- 출처 파일 보존: 위 sha256과 경로(`state/o_dev/datasets/donor_agents/donors.csv`의 source_url/license 포함). 새로 pull한 2개는 `state/o_dev/public_pull_4/`(원본 ipynb + kernel-metadata.json + 추출 main.py).
