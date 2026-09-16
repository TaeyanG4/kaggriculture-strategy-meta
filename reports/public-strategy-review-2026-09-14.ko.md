# 최신 공개 전략 적용 검토 — 2026-09-14 KST

## 결론

사용자가 보여준 공개 점수 상위 노트북5개의 최신 소스를 Kaggle CLI로 다시
받아 비교했다. 이 중 상위3개는 같은 V39 에이전트이며, 다섯 노트북 모두
기존에 확보·평가한 코드와 일치했다. 제목이나 게시 시각이 바뀌었다는 이유로
새로운 전략으로 세거나 이미 끝난 비교를 반복하지 않는다.

| 현재 노트북 | 생성되는 에이전트 | 기존에 보유한 이름 |
|---|---|---|
|[kaggriculture_utils_v1](https://www.kaggle.com/code/degnonguidi/kaggriculture-utils-v1)|V39 / 708c7485fa96…|ahmed_latest_v1|
|[V39 — Ready Before the Rush](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v39-ready-before-the-rush)|V39 / 708c7485fa96…|ahmed_latest_v1|
|[master-engine-v53e01d74d8f](https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v53e01d74d8f)|V39 / 708c7485fa96…|ahmed_latest_v1|
|[V38 Smarter Feed, Stronger Margins](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins)|V38 / a2047ebd8ca5…|public_v38 / dynamic_route / master_v3|
|[shop_router_reactive_v4](https://www.kaggle.com/code/aurax7/kaggriculture-shop-router-reactive-v4)|reactive_v4 / 3dd123c5b484…|reactive_v4_v3|

V39 전체 SHA-256:
`708c7485fa964853b193f175dcd83020602c005e159ce82e38dc350b22e970c8`

원본·메타데이터·추출 소스·차이는
`state/agent_experiments/public_review_20260914/`에 보존했다.
`static_sources.json`에 노트북/에이전트 해시와 중복 원본 이름이 있다.
셀은 실행하지 않았으며 `%%writefile main.py` 본문만 문자열로 추출하고
구문을 확인했다. 생성 에이전트는 기존 정적 능력 검사 및 실행 평가 대상과
동일하다. 소스의 Apache-2.0 고지와 기여자 표시는 유지해야 한다.

## 기존 평가를 재사용할 수 있는 범위

`elite_pool_20260913/shard_1/results.json`의 상대 SHA가 최신 V39와 같다.
당시16개 시드·양쪽 좌석에서 c117과 c111이 각각32승0패였다.
c117 평균 최종 마진+39499.1875, 최악+8816이었다. 반응형 실제 코드 대결이다.
이 결과는 통째 교체를 지지하지 않지만, 모든 상황에서 V39가 약하다는 증명도
아니다. c129가 V39와 직접 붙어 이겼다고 바꿔 쓰지 않는다.
새 c132 검증에는 이 동일 V39를 공통 상대로 포함해 현재 후보와의 상호작용을
확인한다. 같은 코드를 세 번 넣어 상대 다양성을 부풀리지 않는다.

## V39에서 분리해서 검토할 변경

V38 대비 약12KB의 변경은 큰 작물 전환 모델이 아니라 아래 운영 개선이다.

| 변경 | 실제 코드 동작 | 현재 적용 판단 |
|---|---|---|
|생산 달력 급여 비용|비생산일의 기존 돌봄 보너스를 이번 급여 비용에서 빼고, 종료 후에만 지급될 돌봄도 제외|원리는 타당. c132가 더 보수적인 별도 규칙으로 이미 구현됐으며 검증 진행|
|10~11일차 밀 구매 축소|앞으로48턴의 예정 픽업·판매와 추가 비축6개를 남긴 뒤 불필요한 구매량 축소|c129의 부족분 보충과 다른 기능. 과거 c126의 작은 비용 회귀도 있으므로 별도 가설·회귀 비교 전 이식하지 않음|
|다음 턴 픽업 보호|실제 현장 작업 후 재고와 야간 운반, 주문별 수량·자금·창고 여유를 계산해 밀 판매를 줄이거나 구매|c129와 목적이 겹치지만 방식·범위가 다름. 단순 중첩 시 과잉 비축/주문 상호작용 위험이 있어 한쪽씩 비교해야 함|
|주문10개인 턴 사전 확보|다음 턴 주문이 꽉 차면 그다음 턴 픽업까지 현재 턴에 미리 확보|현 조달 보완의 확장 후보. 현재 실패에 해당 사례가 있는지 먼저 진단하고 별도 후보로 비교|

V39의 공급 예산은 현재 보유 현금만 인정하고 보수적인 구매가를 적용한다.
예정 매출을 확정 현금으로 가정하지 않는 점은 유지할 가치가 있다. 반면
V39의13개 경로 자체는 유지되며, 이번 THIRD FARM CLUB의 당근 매출35540점
격차를 해결하는 수요 기반 대규모 작물 재배치 기능이 새로 생긴 것은 아니다.

## 실행 결정

- c129(ref56209242) 제출·서버 COMPLETE는 유지한다.
- V39 전체 교체나 동일 코드 중복 제출은 하지 않는다.
- c132는 기록 상대8패 중7개 개선,1개 동일, 오류0이었다. 기록 상대 진단만으로
  승격하지 않고 c129/c125/c117/V39 공통 상대와 양쪽 좌석을 검증한다.
- c130의 선택32시드512경기는 전 조건 동일했다. 오류나 퇴보는 없지만 필요한
  개선 증거가 없어 승격 실패. 관측 토마토 패배의 특수 복구 가설로 보존하며
  미관측 최종64시드는 열지 않는다.
- 큰 성능 개선 우선순위는 공급·수요를 예측한 작물 전환과 노동 재배치다.
  구체적 원장은 `c125-third-farm-macro-loss-2026-09-13.ko.md`에 기록했다.
