# c484 현재계열 로컬 패배 감사

c470 로컬12패와 첫4승 대조의 양좌석 행동 해시·보상·720상태 회계가 모두 재현됐다. 정확 캐시2건을 재사용하고14건을 새로 감사했다. 자기 행동11,504개, 잔여 현금 오차0. 이것은 실행 재현이며 모든 명령이 유효했다는 뜻은 아니다.

| 경기 | 상대 | 마진 | 판정 |
|---|---:|---:|---|
| 203346 | 340 | -198 | milk/berry sale timing, production nearly equal |
| 203348 | 340 | -198 | milk/berry sale timing, production nearly equal |
| 203350 | 267 | -147 | milk sale timing, own milk production +1 |
| 203352 | 267 | -147 | milk sale timing, own milk production +1 |
| 203418 | 326 | -2464 | milk production deficit17 with wool surplus15; production allocation hypothesis |
| 203420 | 326 | -2464 | milk production deficit17 with wool surplus15; production allocation hypothesis |
| 203473 | 333 | -52 | same production, wool sale revenue -54 |
| 203480 | 342 | -1188 | weed-interrupted PLANT abandoned at179; missing6 berries |
| 203484 | 325 | -1 | same main production, one-cash sale-timing difference |
| 203495 | 344 | -141 | wheat quantity/timing or one-cash carrot sale difference |
| 203499 | 344 | -1 | wheat quantity/timing or one-cash carrot sale difference |
| 203500 | 344 | -1 | wheat quantity/timing or one-cash carrot sale difference |
| 203354 | 326 | +13123 | winning control; inherited ineffective commands also present |
| 203356 | 326 | +13123 | winning control; inherited ineffective commands also present |
| 203358 | 322 | +710 | winning control; inherited ineffective commands also present |
| 203360 | 322 | +710 | winning control; inherited ineffective commands also present |

203480의 시비 실패를 비료 부족으로 해석하면 잘못이다. 398턴 일꾼9은 비료1을 갖고 있었으나 대상[8,1]은 빈 땅이었다. 168턴 잡초가 생겼고, 178턴 딸기 파종이 DIG로 바뀌었다. 179턴은 WATER, 180턴은 EAST여서 기존 복구기가 파종 대기열을 버렸다. 반대 좌석은 잡초가 없어서 파종에 성공했다. 딸기 생산243 대249, 딸기 매출−1,321이 관측 마진−1,188의 대부분을 설명한다. 새 시장예측이 만든 회귀라고 단정할 근거는 없다.

c485는 같은 날 첫 PASS를 사용해 PLANT→WATER와 기존 동선을 유지할 수 있는 경우만 복구한다. c373의 초반 BUILD 복구와 구별하며, 급식·수확·입고·주문 이동과 다른 일꾼의 공동 타일 작업을 금지한다. 새 관측·반응형 상대에서 재검증한다. 잡초 RNG/상점 변화도 결과에 포함하며 생산 복구만으로 승률 개선이라고 하지 않는다.

c481 급식/탈출, shane18 ICE/PIZZA 생산, 공개318노트북 건별 흡수, 이후 실전 패배는 계속 미완료 항목이다. 연구 중 등록·검증기록 편입0, Kaggle은 소유자만 제출한다. c484 임시 알람은 완료 확인 후 삭제했다.
