# c385 조사 — 로컬 상위 30위·새 공개 전략 검토

2026-09-23 Codex. **조사 번호이며 c385 후보는 만들지 않았다.** 후보/러너/리그 코드는 변경하지 않았고, 추가 시뮬레이션·Kaggle 제출 없이 저장된 실행 소스와 기존 경기만 분석했다.

## 결론

현재 c379/c384 계열을 교체할 근거는 부족하다. 다만 **More Wheat의 복수 판매예측, Moon의 최종 주문 정리, V57의 지출 순서 보호**는 우리 코드와 구분되는 검토 대상이다. 새 Herd-Safe ca20은 c384가 진 두 세계가 있어 우선 손실 원장을 확인할 부모 도전자다. 어느 쪽도 이번 정적 분석으로 성능 개선을 입증한 것은 아니다.

로컬 BT 상위 30개 행을 고정해 모두 기존 이력과 실제 실행 소스를 대조했다. 그중 우리 모델 9행, 공개 모델 21행이며 공개 main.py는 **18종**이다. 같은 main.py라도 부속 고지 파일로 artifact가 다른 3쌍은 전략 판단에서 중복 가중하지 않았다. 미세 제어가 다른 모델은 별개로 유지한다. 상위 행이 구버전인 노트북은 최신본도 추가했다. 따라서 Moon 최신261, Order Book Response259, 신규 Demand263도 범위에 포함된다.

순위 스냅샷: **10:02:54 KST**. 순위와 대진은 계속 변하며, 이 표는 공통 상대·공통 세계 검증이 아니다. 아래 전적은 별도 `top30-h2h-snapshot.json`을 읽은 시각까지의 저장된 유효 경기다. 양 좌석 두 경기는 한 세계로 센다.

## 우선 검토할 메커니즘

### 1. More Wheat, Smarter Sales — 최신 변화는 상대 판매 예측의 복수 가설

[노트북](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales), 최신 agent258 `83fb106f…`. 구버전247 `aa9b0716…`과 실제 차이는 `_v92_p_forecast` 및 진단 카운터다.

- 이전: 처음 두 상점이 같은 기록 라이브러리에서 최고 점수 **1개** 판매 경로를 선택.
- 최신: 최고 점수가 음수가 아니면 상위 3개 중 최고와 점수 차이 1 이하인 경로를 유지. 이 중 하나라도 다음 2턴에 4u 이상 판매를 예측하면 현재 보유량과 자기 미래 48턴의 예정 판매량 내에서 우유·양털·딸기를 앞당긴다. 예측 갱신 간격은 2턴이다.
- 따라서 제목과 달리 **직전 버전 대비 새 밀 생산 확대가 핵심이 아니다.** 기존 토마토 투자·주문 탐색·씨앗/시비 절약·7턴 구조는 유지된다. 하나의 경로만 확신하지 않는 것이 변경점이다.
- 우리 c384의 깊은 본체에는 기존 `_V92_P_TOP=1`이 남아 있다. 이 변화는 아직 없다. 다수결이 아니라 **하나라도 예측하면 발동**하므로 잘못된 조기 판매도 늘 수 있다. 공급 기록의 노후화·실제 자기판매 관측 오차도 그대로 주의해야 한다.
- 선행 c326은 같은 P층의 가격 제한이 상대 가격을 회복시켜 승점 −13.75pp/마진 −541로 기각됐다. c327/c367 관측 교정도 유효 음수이며, c328의 예측 개선은 정책 이익이 아니었다. 이번 복수 경로 선택은 그 변경들과 다르지만 예측 적중률만으로 채택하면 같은 시행착오다.

**판정:** 부품 검토 1순위. 먼저 기존 패배에서 추가 경로 때문에 달라질 판매와 자기/상대의 실현 수입을 분리한다. 실제 이식 시 독립 OFF 동일성·추가 발동 및 다중 반응 상대 검사가 필요하다. 현재 League c384 직접전 4승0패/2세계는 부모 교체 근거가 아니다.

### 2. Moon Counts Melons — 구버전의 큐 정리와 최신본의 최종 판매 정렬

[Moon](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons) / [Soil](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-soil-remembers-rain). **상위 4위 행251 `bc80b476…`은 구버전**, 현재 두 URL은261 `178ae0f7…`에 연결된다. 같은 제목의228/231도 다른 과거 버전이다.

- 251: Pipe19 계열의 판매 선행을 3→4턴으로, 종료 씨앗 hedge를 2→0으로 바꾸고, 최종 단계에서 빈 주문·0수량·공급 불가능 SELL·이미 전부 개방된 BUY_LAND를 제거한다. 같은 턴 유닛 명령 이후의 창고를 투영한다. 앞에 불확실한 BUY_PRODUCT/BUY_ANIMAL이 있으면 해당 품목의 뒤 SELL을 함부로 죽은 주문으로 판단하지 않는 보호가 있다.
- 261: 위 전체 결과 **뒤**에서 연속 SELL 블록을 다시 최적화한다(step216 이후). 매입/고용 등의 슬롯과 판매 수량을 유지한다. 바뀐 실제 행동을 clone detector의 `prev_action`에 반영한다. `_V9_RACE`의 판매 복원까지 교정하는 것은 아니다.
- 우리 최종 시장층은 수량·가격 영향·수요를 이용한 `sell_impact_reorder`이며, 261의 복제 상대 주문 가정하의 lockstep 점수와 같지 않다. 기존 비용 절약/선행 판매 목적은 상당 부분 겹친다. 정리→정렬을 최종 큐에서 수행하는 위치와 **불확실 매입 뒤 SELL 보호**가 특히 참고할 점이다.
- 빈 주문은 경제적으로 무의미해 보여도 동시 시장의 절대 슬롯을 차지한다. 제거는 상대와의 가격 경로를 바꾼다. ‘noop 제거이므로 행동 동일’이라고 보아서는 안 된다. 261의 점수 함수도 상대 재고를 우리와 같다고 가정하고 현금 제한을 생략한다.
- 228은 압축을 정적으로 해제했다. 두 정책을 매턴 호출하고 최초 두 상점의 지정 7쌍에서 combined/hybrid를 선택하는 구조다. 일반적인 온라인 학습 플래너로 분류하지 않는다. 231은 V56에 종료 씨앗·비료 절약층을 붙인 구버전이다.

**판정:** 부품 검토 2순위. 최종 주문 정리와 SELL 정렬을 분리해야 원인이 보인다. c384 vs251은2승2패/2세계, vs261은20승2패/11세계다. 이 분포만으로 최신층이 약해졌다거나 251 부모가 낫다고 결론 내릴 수 없다.

### 3. V57·Order Book·V15 — 지출 실행 가능성을 보존해야 하는 주문 탐색

[V57](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v57-funding-order-invariant)248은 SELL을 HIRE/BUY_SEED/BUY_ANIMAL/BUY_LAND 사이에 옮기는 탐색에 **고정 지출이 원래 슬롯보다 빨라지지 않는 필터**를 더했다. 기존 생성기는 지출 사이 상대 순서만 지키므로 지출이 첫 판매보다 앞서갈 수 있다. 설명문의 ‘판매 선행은 현금을 늘리므로 안전’은 생성기 전체를 보장하지 않는다.

[Order Book](https://www.kaggle.com/code/shiiin9/your-market-list-is-an-order-book)232 및 같은 코드의 [Fixed + Flexible](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible)은 800후보 한도의 주문 재배정과 예상 토마토 매출을 사용한다. 추가259는 첫 정렬에 대한 상대의 재정렬 응답을 한 번 더 가정하며, 지출 앞당김 제한도 있다. 실제 상대가 그 가정대로 반응한다는 증거는 아니다.

[V15](https://www.kaggle.com/code/harveyel/kaggriculture-v15-market-stack)252/260은 같은 main.py다. 여러 함수가 있지만 기본 설정에서 초기 토지 확장·네 번째 토지 차단·idle작업·비료예산·premium보류·종료정리가 OFF이고 clone 선행만 ON인 부분이 있다. 이후 씨앗/시비 절약, 넘침 회수, 3턴 판매 선행, 주문 탐색, 예상 토마토 매출층이 추가된다. 우리 c368/c371/c384가 이미 같은 목적의 일부 기능을 갖고 있으므로 이름별로 재이식하면 중복이다. 마지막 telemetry wrapper는 예외 시 부모를 다시 호출한다. 첫 호출이 상태를 일부 바꾼 뒤 실패하는 경우 재호출의 안전성은 별도 확인이 필요하다(발생 증거는 없음).

**판정:** V57의 지출 보호는 주문 탐색을 도입할 때 우선 참고한다. 단, 슬롯 보호도 매입 가격·판매 현금·용량까지 보장하지 않는다. c361 전체 시장 스택 이식은 fresh confirm W→L20/own·마진 음수로 실패했고, c362 단순 정렬과 c364 품목 순서는 독립 개선이 없었다. 이번에는 최종 큐·예측 가정·실행 가능성이라는 다른 부분을 분리해야 재시도 가치가 있다.

### 4. 신규 Herd-Safe race ca20 — 부모 도전자, 아직 우세 미확정

[노트북](https://www.kaggle.com/code/statma/kaggriculture-herd-safe-sale-window-race-ca20), agent264 `29454a13…`. 기존 Herd-Safe255/Rescue254 `1cac2765…`와 **실제 차이는 `_CA_MARGIN=-15→-20` 한 줄**이다. 밀 대비 당근 재배의 수익 판정을 더 쉽게 통과시킨다. 판매 시각이나 레이스 길이를20으로 바꾼 것이 아니다(레이스44 유지).

공개 부모의 개막 BUY8/SELL3/밀씨앗1도 유지된다. 이는 그 이전247의 개막과 별도 변화다. 우리 c384의 당근 margin은−5이므로−20을 바로 넣으면 공개의−15→−20보다 훨씬 큰 개입이다.

c384가 seed789731835에서 양좌석−1615/−1628, seed729857713에서−204/−473으로 **0승4패/2세계**였다. 완료 DONE/예외0이지만 두 세계의 전체 원장은 아직 없다. 이 패배를 당근 한 줄 때문이라고 단정할 수 없다. 같은 세계에서 c384/255/264를 비교해 축군·작물·시드·급식·판매/고용을 분리해야 한다. 기존 c365의 사료 예비2→1과는 다른 규칙이다.

**판정:** 최초 부모 도전자/손실 감사 대상으로 보존. 현행 부모를 즉시 교체하지 않는다. c380의 구형 More Wheat/Hybrid 부모 교체 실패는 최신264를 평가했다는 뜻이 아니다.

### 5. 신규 Demand-Preserving Turn Sale Timing — 복수 가정 최악값과 비료 상쇄

[노트북](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing), agent263 `939c4457…`, 마지막 실행 함수 `_v350_agent`.

본체는 고정 경로와 다수 조건부 층의 합성이다. 마지막 층은 자기 주문 복제·판매 먼저·판매 나중·역순 판매 먼저의 네 상대 주문을 가정하고 **최악 마진을 최대화**, 동점이면 원래 순서 가정의 마진으로 고른다. 같은 턴 비료 매도/매입의 겹치는 요청량을 상쇄하고, 상쇄가 생긴 턴만 남은 주문을 다시 최적화한다.

주의할 실제 코드 계약:

- `_v44y_lockstep`/`_v44y_factor_margin`은 명시적으로 **현금·공통 창고용량 무제한**, 상대 품목 재고도 우리 재고로 가정한다. 전체 공식 엔진을 정확히 복제한 가치 함수가 아니다.
- 상쇄는 **요청 수량** 기준이다. 현금/재고 부족으로 실제 체결량이 다르면 순재고 불변이 보장되지 않는다. 매도 수입이 중간 고용을 지급하고 나중에 비료를 사는 구조에서는 끝 재고가 같아도 중간 현금이 다르다.
- 0수량을 빈 주문으로 바꾼 다음 `live+dead`로 정리하므로 절대 슬롯도 이동한다. 네 상대 가정·상쇄·빈 슬롯 이동·재정렬은 각각 다른 개입이다.
- 깊은 당근 사료 예비가 **2일**로 우리 c365 이후1일과 다르고, 토마토 자격도 현재 우리 예상 매출 gate와 다르다. 마지막 정렬만 보고 전체 부모 우세를 추정하면 안 된다.

기존 c383/c384 정밀 재생 원장에 비료를 같은 턴 양방향 거래한 사례가 실제 있다(선택 c384 두 조건 각각18턴, 겹침43/44u). 다만 step151/174 일부는 순현금0이었다. 왕복 모두가 손실 또는 제거 가능한 이익이라는 근거는 아니다. 공개 노트북의 자체720턴 검증은 PASS 상대 1경기이므로 강도 확인 자료가 아니다. 로컬 c384 직접전은2승0패/1세계다.

**판정:** 최종 큐에 맞춰 다시 최적화하는 발상은 유용하나 전체 이식 우선순위는 낮다. 우선 실제 체결·현금 경로를 감사할 별도 연구 대상이다.

## 기타 상위 코드와 중복된 시도

- **V56 / Clone Race Horizon:** 씨앗·무효 시비 절약은 c368/c371에 이미 반영한 목적이며 Clone의41→48만 늘리는 변경은 c372 연구와 겹친다. 새 메커니즘 없이 반복하지 않는다.
- **Kaggriculture(evgen,221):** V56과 AST를 대조하면 주석/docstring을 제외한 실행 구문은 같다. 원시 source는 별개로 보존하고 리그 중복 설정을 변경하지 않았다. 독립 전략군으로 가중하지 않는다.
- **Pipe19:** 자정 창고 넘침 회수,3턴 판매 선행, 개막 복구. seed prefund 함수는 존재하지만 `_R148_SEEDS=False`로 비활성이다. o306의 넘침 회수는 우리 상태에서 창고가 아니라 일손 짐에 물품이 있어 no-op이었던 이력과 대조해야 한다.
- **Farmer John and the Idle Seller:** 임시 개막 밀 식재가 실패하면 step29 목초를 복구하고 step84–91의 불필요한 우회를 억제한다. c373/o301 복구 목적과 겹치며 단순 이중 적용하지 않는다.
- **The 2965 Master Hybrid Engine:** Pipe19+종료 씨앗/비료 절약 계열이며 c380에서 exact93831c18 부모 비교가 유효 음수였다. 새 버전이 아니므로 같은 전체 교체를 반복할 이유가 없다.
- **92% seed leak / 구Moon231:** 종료 파종 가능량을 세어 씨앗 예비와 마지막날 비료를 줄인다. c368/c374 등과 대조해 실제 추가 절감만 남겨야 한다.
- 우리 상위9행(c379/c384/c374/o302/c371/o301/c368/c369/c370)은 기존 후보별 보고서·이번 source SHA와 연결했다. 예를 들어 c384가 o301에0승4패/2세계인 사실은 후기 기능을 무조건 좋다고 볼 수 없다는 손실 감사 단서다. 이것도 부모 교체 결론은 아니다.

## 후속 작업 순서와 한계

1. 현재 저장된 ca20·Moon·o301 패배 세계를 기존 `pair_trace`/`replay_accounting`으로 감사한다. 같은 세계 공개 부모와 미세 수정본을 비교해 실제 효과를 귀속한다. 일반/집중 리그와 별도 캠페인을 겹치지 않는다.
2. 부품 탐색은 More Wheat 복수 예측, Moon 최종 큐, 지출 안전 순서로 한 개씩 분리한다. 순수익뿐 아니라 상대 가격 회복, 실패 주문, 뒤의 일손·생산·운반 누락을 검증한다. 기능을 모두 합쳐 효과를 잃어버리지 않는다.
3. 전체 부모 후보는264와 최신258/251/261을 고유 실행 소스 기준 공통 상대/새 세계에서 대조해야 한다. 지금의 2세계 대전과 BT는 탐색 선택 자료다. 과거 공개 whole-policy 실패는 해당 버전에만 적용한다.
4. 유효한 소폭 개선이면 로컬 후보, 독립적으로 확실한 개선일 때만 Kaggle 제출이라는 현행 기준을 유지한다. 모든 상대95%는 아직 입증되지 않았다.

분석 노트북 X-ray your agent / top10-replay-dataset-archive / What2600+FarmsDoDifferently도 확인했다. 공개 행동·일별 생산·버전 drift 추적에 참고할 만하나 기존 수집/프로파일/원장 도구로 가능한 부분이 많다. 행동 변화율로 내부 planner/tape를 확정하거나 관측 cohort 평균을 인과 개선으로 쓰지 않는다. 데이터 분석 노트북에 실행 agent가 없어 `no_source`인 것은 수집 결함이 아니다. 대용량 새 리플레이는 받지 않았다.

원자료는 `state/c385/`: 고정 순위/별칭·전체 source SHA·정적 함수 인덱스·압축 해제본·버전 간 diff·기존 원장 거래·직접전 스냅샷. 원본 공개 파일을 import/실행하지 않고 AST와 기존 bounded decoder로 읽었다. 이후 경기 검증 없이는 예외가 안 보였다는 이유만으로 전 코드 정상이라고 할 수 없다.

## 상위 30행별 확인표

아래 순위는 10:02:54 KST 고정값이다. 전적은 **c384 관점 W–L–T / 독립 seed 수**, 다음 검증용 탐색 자료이며 승격 검정이 아니다. 현재 링크가 가리키는 코드와 구버전 순위 행을 구분한다.

| 순위·ID | 노트북/모델 | source SHA 앞8 | 확인 내용 | c384 직접전 / 세계 |
|---|---|---|---|---|
| 1 · 245 | [c379 Terminal Schedule [Kaggle 56462946]](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56462946) | `9cbc9171` | 기준 제출본; 종료 경로 압축 | 2–0–2 / 2 |
| 2 · 262 | c384 Predictive Tomato [로컬 후보·제출 보류] | `05b8d6ee` | 현재 로컬 후보; cargo 수리+토마토 gate | — |
| 3 · 237 | c374 Terminal Fertilizer [탐색 후보] | `8789bc82` | 마지막날 비료 절약; 독립 개선 미확정 | 4–0–0 / 2 |
| 4 · 251 | [Kaggriculture Frontier \| The Moon Counts Melons](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons) | `bc80b476` | 구Moon:4턴 선행+최종 큐 정리; 최신261 별도 | 2–2–0 / 2 |
| 5 · 230 | [우리] o302 Farmer Feed Topup (o301 hire floor + d26 pickup) | `2cdb9e5d` | 개막 고용 바닥+농부 사료 픽업 수리 | 4–0–0 / 2 |
| 6 · 258 | [Kaggriculture: More Wheat, Smarter Sales](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales) | `83fb106f` | 최신: 유력 판매 예측 최대3개; 부품 우선 | 4–0–0 / 2 |
| 7 · 252 | [Kaggriculture V15 Market Stack](https://www.kaggle.com/code/harveyel/kaggriculture-v15-market-stack) | `d6565929` | V15 합성;260과main.py 동일 | 4–0–0 / 2 |
| 8 · 254 | [Kaggriculture: 7-Turn Rescue \| Historical LB 2800+](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800) | `1cac2765` | Rescue+개막 BUY8/SELL3;255와동일 | 4–0–0 / 2 |
| 9 · 224 | [[우리] c371 Resource Budget](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56444327) | `e23cc84b` | 토마토 유지 고용/급수·시비 절약 | 4–0–0 / 2 |
| 10 · 238 | o301 Hire Floor [탐색 후보] | `383d6fef` | 개막 고용 복구; 현재2세계 손실 감사 대상 | 0–4–0 / 2 |
| 11 · 260 | [kaggriculture v15stack submit](https://www.kaggle.com/code/wzhengbiao/kaggriculture-v15stack-submit) | `d6565929` | 252와main.py 동일·sidecar 차이 | 4–0–0 / 2 |
| 12 · 247 | [Kaggriculture: More Wheat, Smarter Sales](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales) | `aa9b0716` | 구More Wheat;243과동일;258 변경점 분리 | 4–0–0 / 2 |
| 13 · 248 | [Kaggriculture V57 — Funding-Order Invariant](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v57-funding-order-invariant) | `2ee689fd` | 고정 지출 앞당김 차단; 안전 조건 참고 | 4–0–0 / 2 |
| 14 · 227 | [Kaggriculture Pipe19 Sale Advance Overflow](https://www.kaggle.com/code/nathanjacob/kaggriculture-pipe19-sale-advance-overflow) | `111863bd` | 넘침 회수+3턴 선행+개막 복구 | 2–2–0 / 2 |
| 15 · 223 | [Kaggriculture: Clone Race Horizon](https://www.kaggle.com/code/nihilisticneuralnet/kaggriculture-clone-race-horizon) | `0070f9e1` | V56 레이스41→48; c372 선행 | 4–0–0 / 2 |
| 16 · 255 | [Kaggriculture: Herd-Safe Sale Window \| LB 2700](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-herd-safe-sale-window-lb-2700) | `1cac2765` | 254와main.py 동일;ca20의직접부모 | 4–0–0 / 2 |
| 17 · 243 | [Kaggriculture: 7-Turn Rescue \| Historical LB 2800+](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800) | `aa9b0716` | 구Rescue;247과동일 | 4–0–0 / 2 |
| 18 · 241 | [Kaggriculture: More Wheat, Smarter Sales](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales) | `a414ce1b` | 구More Wheat;c380 exact 부모교체 기각 | 4–0–0 / 2 |
| 19 · 209 | [[우리] c368 Terminal Seed Budget](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56432202) | `fed4a96f` | 종료 씨앗 예비 절약; 후속부모에 포함 | 4–0–0 / 2 |
| 20 · 216 | [Kaggriculture V56 — Smarter Seeds and Fertilizer](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer) | `a1ad0fd1` | 씨앗/시비 절약;c371 참고원본 | 2–2–0 / 2 |
| 21 · 210 | c369_shop_herd_submission.tar.gz | `e3bc73c9` | 축군 선택층;c371 이후부모에 포함 | 3–1–0 / 2 |
| 22 · 228 | [Kaggriculture Frontier \| The Moon Counts Melons](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons) | `d1d7c4d4` | 구Moon:7상점쌍에서두정책선택;정적복원 | 2–2–0 / 2 |
| 23 · 242 | [The 2965 Master Hybrid Engine](https://www.kaggle.com/code/haideptry/the-2965-master-hybrid-engine) | `93831c18` | Pipe19+종료절약;c380 exact 부모교체 기각 | 2–2–0 / 2 |
| 24 · 235 | c370 Tomato Maintenance [탐색 후보] | `16f83e39` | 토마토 유지비 절약;c371 합성 | 4–0–0 / 2 |
| 25 · 221 | [Kaggriculture](https://www.kaggle.com/code/evgendvorkin/kaggriculture) | `dac787a4` | V56과실행AST동일(주석/문서문자열제외) | 4–0–0 / 2 |
| 26 · 231 | [Kaggriculture Frontier \| The Moon Counts Melons](https://www.kaggle.com/code/prvsiyan/kaggriculture-frontier-the-moon-counts-melons) | `565b416c` | 구Moon:V56+종료씨앗/비료절약 | 2–2–0 / 2 |
| 27 · 264 | [Kaggriculture: Herd-Safe Sale Window race ca20](https://www.kaggle.com/code/statma/kaggriculture-herd-safe-sale-window-race-ca20) | `29454a13` | 신규 ca20;당근전환 margin−15→−20 | 0–4–0 / 2 |
| 28 · 219 | [92% vs the best public farm: a seed leak in V54](https://www.kaggle.com/code/busyaprime/92-vs-the-best-public-farm-a-seed-leak-in-v54) | `562f34ad` | 종료 씨앗부족/과잉방지;기존c368과대조 | 4–0–0 / 2 |
| 29 · 233 | [Farmer John and the Idle Seller](https://www.kaggle.com/code/lynnsakurai/farmer-john-and-the-idle-seller) | `1cb133e9` | 개막목초복구+실패후우회억제 | 2–2–0 / 2 |
| 30 · 232 | [❄️🔥 A Song of Ice and Fire \| Fixed + Flexible](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-flexible) | `a16e0e9b` | Order Book동일코드별칭;주문탐색+토마토예측 | 2–2–0 / 2 |
