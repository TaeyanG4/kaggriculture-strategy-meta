# 현재 에이전트 구현 공백 정적 감사 — 2026-09-14

## 판단

현재 에이전트의 문제는 기능 자체가 부족하다기보다 **이미 구현된 적응 기능이 매우 좁은 시점·상점 조합·부모 행동에 종속되어 실제 기회를 적게 잡는 것**에 더 가깝다.

이번 감사에서는 기존 소스와 완료된 결과만 읽었다. 새 정책 실행, 새 게임, 새 시뮬레이션, 제출은 수행하지 않았고 agent 소스도 수정하지 않았다.

현재 제출 기준은 c129이며, c145는 c129 계보의 연구 후보이다. c145의 47개 기록 진단은 3개 개선/44개 동일/0개 악화였지만, 기존 반응형 96쌍에서는 전부 비활성이어서 일반 강도 개선은 아직 확인되지 않았다.

## 1. 우유 수요용 COW 적응은 이미 구현되어 있고 실제로 발동했다

`agent/c129_feed_liquidity.py:1530-1612`의 `_v231_controller`는 단순한 고정 축종 정책이 아니다.

주요 발동 조건은 다음과 같다.

- step 216..227
- 열린 상점 3개 이상
- 현재 부모 market에 BUY_ANIMAL 주문이 정확히 1개
- 그 주문이 SHEEP
- 우유 소비 상점 2개 이상
- YARN_STORE 없음
- MILK 가격 >= WOOL 가격
- 이미 배치된 COW 4마리 이상, SHEEP 2마리 이상
- shed/cargo/pending/reserved 동물이 없어야 함

조건을 통과하면 SHEEP 구매를 COW로 바꾸고 PICKUP/PLACE도 COW로 연결하며, 그 추가 COW에서 실제 수확된 우유만 기존 우유 판매 슬롯에 더한다. 상한은 4마리이다.

완료된 `108652197_c129.json` telemetry에서는 다음이 실제로 기록됐다.

- `cattle_requested=1`
- `cattle_confirmed=1`
- `cattle_picked=1`
- `cattle_placed=1`
- `cattle_failed_placements=0`
- `cattle_extra_milk_harvested=21`
- `cattle_extra_milk_sale_requests=14`
- `cattle_milk_credit=7`

즉 108652197에서 V231은 비활성이 아니었다. 실제로 한 번 발동했고 구매·운반·배치까지 성공했다. 그런데도 완료 결과의 margin은 `-10179`였다.

따라서 부족한 부분은 “COW 적응기가 없다”가 아니다. **부모가 특정 12턴 창에 SHEEP 구매 하나를 제안해야만 바꿀 수 있다는 기회 구조**가 핵심 제약이다. cap은 4지만 이 경기에서 실제 요청은 1회뿐이었다.

## 2. V231은 일반 축종 할당기가 아니라 parent-order rewrite이다

V231이 놓치는 범위는 명확하다.

- step 216 이전과 227 이후에는 새 수요 정보가 있어도 신규 COW 선택을 하지 않는다.
- 부모가 BUY_ANIMAL SHEEP를 내지 않으면 COW 기회를 새로 만들지 않는다.
- BUY_ANIMAL 주문이 2개 이상이면 abstain한다.
- shed/cargo에 동물이 있거나 이전 치환의 예약/운반이 남아 있어도 abstain한다.
- COW와 SHEEP만 비교하며 GOOSE와의 자본/사료 기회비용까지 일반적으로 평가하지 않는다.
- 이후 추가로 공개되는 상점과 남은 회수기간을 보고 축종 목표치를 다시 계산하지 않는다.

108652197의 완료 shop sequence는 `PIZZA_SHOP, SMOOTHIE_SHOP, ICE_CREAM_SHOP, SMOOTHIE_SHOP, PIZZA_SHOP, PET_CAFE, FARMERS_MARKET, ICE_CREAM_SHOP`으로 우유 수요가 매우 강하다. 기존 장부에서도 우리 우유 수확/판매 266, 상대 309였고 우유 매출차 -11206 중 약 94.8%가 수량 항목이었다.

V231 한 번의 치환이 이 격차를 전부 해소하지 못했다는 것은 확인됐지만, 추가 COW가 최종적으로 이득이라고 아직 인과적으로 증명한 것은 아니다. 다음 단계는 새 대형 컨트롤러가 아니라 **기존 구매 기회에서 V231의 abstain 이유를 관측하는 것**이다.

## 3. day12의 6-SHEEP 확장도 이미 있지만 완전히 다른 특수 정책이다

`agent/c129_feed_liquidity.py:1937-1983`의 `_v233_eligible/_v233_request`는 다음 조건을 요구한다.

- day12 최초 commit
- YARN_STORE 2개 이상
- WOOL >= 220
- WHEAT <= 45
- 정확한 3-quadrant/locked-region 형상
- shed/inventory에 SHEEP 없음
- native day12..29 계획에 기존 BUY/PICKUP/PLACE SHEEP 없음
- 시장 주문 수, 창고 용량, 현금 budget을 모두 통과

통과하면 BUY_LAND + SHEEP 6 + WHEAT 6 + HIRE 2를 하나의 확장 묶음으로 요청한다.

108652197의 c129 telemetry에서는 `sheep_commit_requests=0`, `sheep_committed=0`, 관련 hire/feed counter도 전부 0이었다. 이 경기의 공개 shop sequence 자체가 YARN 없는 우유 중심이므로 이 기능은 우유 패배를 해결하는 기능이 아니다.

따라서 V233 존재를 근거로 일반 축종 적응이 이미 완성됐다고 볼 수 없지만, 반대로 새 “양 수요 확장기”를 다시 만드는 것도 중복이다.

## 4. exact YARN→PET 전환과 late feed 억제도 이미 존재한다

c129/c145 계보에는 exact opening에 대해 COW 2마리를 SHEEP 2마리로 치환하고 pickup/place까지 다시 쓰는 YARN/PET 전환도 있다. 108652197의 telemetry에서는 `yarn_pet_routes_seen=0`으로 이 경로가 아니었다.

또 c124 계층은 모든 상점이 공개된 late game에서 수요가 없고 feed 경제성이 나쁜 COW/SHEEP의 FEED를 억제한다. 108652197에서는 `livestock_margin_feed_skips=8`, 모두 SHEEP였고 COW skip은 0이었다. 즉 이미 “불필요한 양 급식 절약”은 일부 작동했다.

문제는 이 절약된 밀/노동/자본을 **다른 고가 생산 자산으로 재배분하는 일반 계획 계층은 아니라는 점**이다.

## 5. c145의 당근 적응도 같은 구조적 한계를 보여준다

c145는 이미 “현재 행동 뒤 빈 타일 + 부모의 다음 PLANT WHEAT + 수요/가격 + 두 번의 productive WATER + native HARVEST”를 인증해 WHEAT 1타일을 CARROT으로 바꾸는 좁은 allocator이다.

기록 47건에서는 3개 경기가 개선됐지만, 기존 반응형 96쌍에서는 c145가 전부 비활성이었다. 460개 certified route가 있었지만 모두 combined value/cash gate에서 거절됐다. 따라서 단순히 threshold를 낮춰 억지로 활성화할 근거는 없다.

여기서도 공백은 “당근 정책 부재”가 아니라 **현재 경제성 gate가 실제 반응형 조건에서 구분력을 만들지 못하고 있다는 점**이다.

## 6. 전략보다 먼저 고쳐야 할 실행 일관성 공백도 남아 있다

완료된 구조적 손실 감사에는 전략 선택과 별개의 실행 결함이 있다.

- 108628622: 초기 현금 50 차이 -> HIRE 1명 누락 -> pasture BUILD 누락 -> step95 PLACE COW 실패 -> 해당 위치 우유 생산 0.
- 108609267: 새 양 운반/급식 과정에서 같은 턴 앞선 일꾼이 WHEAT를 먼저 가져가 대상 일꾼 PICKUP/FEED가 실패하고 양이 소실됨.
- c126 feed buffer는 미래 route의 PICKUP과 현재 관측을 제한적으로 보지만, 새 배치 예정 동물과 동일 턴 일꾼 간 자원 경쟁을 완전히 예약하지 않는다.

이런 실패는 새로운 상위권 전략을 붙여도 계획이 물리적으로 실행되지 않으면 그대로 남는다. 따라서 **실제 고용/건설/배치/급식 성공 확인과 의존성 복구**가 일반 축종 allocator보다 우선순위가 높다.

## 현재 코드의 실제 부족점 순위

1. **축종 선택의 opportunity coverage**: V231은 12턴 parent-SHEEP rewrite라 수요에 따른 신규/대체 투자 의사결정 범위가 좁다.
2. **실행 의존성 예약**: HIRE -> BUILD -> PLACE -> FEED와 같은 연쇄가 중간 실패 후 자동 복구되지 않는다.
3. **동일 턴 물자 경쟁 예약**: 일꾼별 WHEAT 수령/사용 순서를 완전하게 예약하지 않는다.
4. **작물 적응의 일반화**: c145는 유효한 좁은 구현이지만 반응형 조건에서 96/96 비활성이었다.
5. **수요 변화 뒤 재평가**: 초중반 고정 route/특수 overlay가 많고, 추가 상점 공개 후 생산 포트폴리오 전체를 다시 평가하는 통합 계층은 제한적이다.

## 가장 싼 다음 관측

새 정책을 만들기 전에 108652197의 step216..227에서 V231 각 guard를 기록만 하는 observation-only audit가 가장 싸다.

각 턴에 다음 값만 기록하면 된다.

- parent BUY_ANIMAL 주문 개수/품목/수량
- milk_shops, YARN 존재 여부, MILK/WOOL 가격
- COW/SHEEP 배치 수
- shed/cargo animal 수
- reserved/carrying/pending 상태
- rewrite 요청/확정 여부

이 관측으로 “추가 기회가 실제로 있었는데 좁은 guard가 막았는지”와 “부모 자체가 추가 동물 구매 기회를 만들지 않았는지”를 먼저 구분해야 한다.

V233는 day12 hour0..2에서 eligibility guard별 false 원인을 한 번 기록하면 충분하다. late BUY_ANIMAL payback gate는 기본13 route에서 day20 이후 주문 기회0이라는 기존 정적 결과가 있으므로 새 구현 우선순위가 아니다.

## 결론

현재 에이전트는 이미 많은 상위권 아이디어를 부분적으로 구현하고 있다. 가장 큰 개선 여지는 기능을 더 쌓는 것이 아니라 **특수 overlay들을 일반적인 “현재 수요 + 남은 회수기간 + 부모의 실제 실행 가능 행동” 판단으로 연결하고, 그 전에 실행 의존성 실패를 제거하는 것**이다.

첫 개발 후보를 고른다면 V231을 새로 만들지 말고 **기존 V231 opportunity audit -> parent-order 제약 완화 가능성 평가** 순서가 맞다. 동시에 HIRE/BUILD/PLACE/FEED 연쇄 복구는 별도 독립 후보로 유지해야 한다.

## 근거

- `agent/c129_feed_liquidity.py:1530-1612`
- `agent/c129_feed_liquidity.py:1937-1983`
- `agent/c145_carrot_min3.py:3336-3646`
- `reports/seven-new-loss-ledger-results-2026-09-14.ko.md`
- `reports/structural-loss-audit-and-improvement-plan-2026-09-14.ko.md`
- `reports/c145-resume-and-top2-review-2026-09-14.ko.md`
- `state/agent_experiments/c138_c139_commitment_20260914/108652197_c129.json`

