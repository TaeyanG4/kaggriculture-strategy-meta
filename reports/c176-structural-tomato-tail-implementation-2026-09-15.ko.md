# c176 구조적 토마토 tail 구현 — 2026-09-15

## 목적

`o199c_carrot_price2.py`를 불변 부모로 두고, 구조 변경을 단일 overlay로 던진 뒤
부모 tail을 그대로 따르는 문제를 피하기 위한 첫 coherent-tail 후보를 만들었다.

`o214`는 작은 TOMATO commit도 실제로는 `BUY_LAND(SE) + V219` 전체를 켜서
$4,000 토지 고정비가 붙었다. c176은 반대로 **새 토지를 절대 사지 않는다.**
day18 이후 이미 열린 3개 구역에서 부모가 실제로 실행하려는 late `PLANT WHEAT`
일부만 TOMATO로 바꾸고, 그 변화 때문에 새로 필요한 씨앗·유지 노동·밀 안전재고·
수확·반납·판매까지 같은 regime이 책임진다.

## 후보

- 부모: `agent/o199c_carrot_price2.py`
  - SHA-256 `1429673c3c1057c07f0a644124a4fd497b111b1646451bac1de852e5c035a41d`
- overlay: `agent/overlays/c176_structural_tomato_tail.py`
- 후보: `agent/c176_structural_tomato_tail.py`
- manifest: `agent/c176_structural_tomato_tail.manifest.json`
- builder: `tools/build_c176_structural_tomato_tail.py`
- 상태: `implemented_unvalidated`

## AUTO regime

step432/day18에 한 번만 결정한다.

- 보유 토지: NW/NE/SW만 열린 상태, SE 미구매
- 현금 >= $7,000
- PIZZA_SHOP/FARMERS_MARKET 합계 >= 2
- TOMATO 현재가 >= 70
- o199c의 CARROT hot 조건은 비활성

조건을 통과하면:

- tomato-demand shop 2개: 목표 8칸
- 3개 이상: 목표 10칸
- day18~20에 **실제로 빈 타일에서 실행될 부모의 `PLANT WHEAT`만** TOMATO로 치환
- c176이 활성인 step432에는 기존 V219의 SE 투자만 억제

강제 비교용 환경변수:

- `KAGG_C176_FORCE=KEEP|REALLOC`
- `KAGG_C176_SIZE=1..10`

강제 REALLOC도 토지/현금/표준 설정 같은 물리적 안전조건은 우회하지 않는다.

## coherent tail 범위

1. **씨앗**: day18에 TOMATO 목표 수량을 미리 매입한다. 엔진의 field-before-market
   순서를 지켜 같은 턴에 산 씨앗을 같은 턴 파종에 사용하지 않는다.
2. **파종**: 최종 o199c action이 여전히 `PLANT WHEAT`이고 현재 타일이 비었을 때만
   치환한다. o199c CARROT 전환을 덮어쓰지 않는다.
3. **유지 노동**: 기존 route worker를 임의로 빼지 않고 c176 전용 hand를 매일 1~2명
   추가해 관측된 TOMATO 타일만 WATER/HARVEST/반납한다. 새 worker index는 실제 HIRE
   성공 다음 callback에서 확인한다.
4. **밀/사료 안전**: 전환 칸당 WHEAT 최대 6개를 고정비처럼 사지 않는다. 대신 현재
   own route의 앞으로 48 step `PICKUP WHEAT` 물리 의무를 세어 부족분만 하루 최대
   12개까지 보충한다.
5. **판매**: 실제 projected shed의 TOMATO만 판매하고, 추가 판매 후 기존
   `_v224_sales_first`/`_r37_reorder_sales`를 다시 적용한다.
6. **금지**: BUY_LAND, 축종 변경, opening 변경, 상대 ID/seed/replay/future shop 사용.

## 구현 검증 상태

성능 시뮬레이션은 실행하지 않았다. 현재 돌아가는 로컬 검증 자원을 건드리지 않았다.

정적/함수 계약만 확인했다.

- builder compile 성공
- 후보 import 성공
- 마지막 callable이 `agent`
- o199c 부모 hash 일치
- overlay 실행 코드에 `BUY_LAND` action 없음
- AUTO 2-shop -> REALLOC/8칸 결정 확인
- 활성 step432 -> V219 gate 억제 확인
- field-before-market 때문에 seed 구매와 실제 crop swap이 2단계로 동작함을 확인
- 테스트 6개를 pytest 없이 직접 호출해 모두 통과

로컬 성능·승패·worker 비용·feed top-up 과잉 여부는 아직 미검증이다.

## 첫 성능 검증에서 볼 것

첫 cheap screen에서 평균 margin보다 먼저 다음을 본다.

- `c176_plant_swaps`, `plants_confirmed`, `lost_targets`
- `hire_requests/confirmed/shortfalls`, 추가 hand 비용
- `wheat_topup_units` 및 기존 feed/pickup 손상 여부
- 실제 TOMATO 생산/판매량
- o199c 대비 W->L / L->W
- >=3 tomato-shop 세계에서 V219 SE 투자 제거가 실제로 이득인지
- 2-shop 세계에서 o214와 달리 새 토지 없이 구조적 손실을 고치는지

명백한 기계 실패나 W->L 증가가 보이면 확대 검증 없이 중단한다.
