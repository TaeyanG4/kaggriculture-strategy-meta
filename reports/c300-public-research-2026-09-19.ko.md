# c300 공개 코드·디스커션 조사

최신 추가: [c312 공개 v9/4 독립 검증 및 상위 패배 원장](c312-public-v9-frontier-and-elite-losses-2026-09-19.ko.md). 과거 router_v5와 다른 공개 소스. V49 대비 두 패널 우세를 확인해 개발 기준선 갱신. 저자의 노동병목·플래너 분류는 미검증이고 일부 연구 수치가 동결 상대 기반이라는 한계를 보존한다.

확인일: 2026-09-19 KST. 단일 작업 원장은 [HANDOFF](../HANDOFF.md). 이 문서는 출처/정적 감사 결과의 색인이며 다른 작업 원장이 아니다. 읽기 전용 수집이며 게시/제출하지 않았다.

## 공식 평가에서 확인한 제약

- [Evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation): 점수에는 승/패/무가 들어가며 현금 마진 크기는 직접 입력되지 않는다. 하루 최대5제출, 최근2제출 활성/최종 평가 대상. 리더보드는 최고 점수 bot을 표시하므로 최신 제출과 표시 점수를 동일시하면 안 된다.
- 최종 제출: 2026-09-30 23:59 UTC(한국 10-01 08:59). 이후 약2주 경기를 추가해 수렴시킨 뒤 Bradley–Terry 평가. [공식 직원 설명](https://www.kaggle.com/competitions/kaggriculture/discussion/731587). 무승부 처리·정확한 경기 포함 구간은 여기서 추가 확인하지 못했으므로 추정하지 않는다.
- 실행 자원 안내: 1.6 vCPU, 6.5GiB, 제출100MiB. 현재 로컬 시간 제한 검증과 실제 서버 여유는 별개다.
- 결론: 과거 최고점·현재 snapshot·마진 평균을 최종1위 확률로 바로 바꿀 수 없다. 변경 가능한 공개 상대에 대한 승리와 비공개 상대 일반화도 분리한다. 동결 캠페인 기준은 변경하지 않는다.

## 확보한 코드와 해석

수집 위치: `state/c300/public_research_20260919/`. 기존 Kaggle CLI의 `kernels list/pull`, `datasets files/download` 재사용. 최신순30개·점수정렬25개 목록을 저장했다. 정렬 순위는 독립 라이브 강도의 증거가 아니다. 해시는 `source_manifest.json` 참고.

### V49: 최신 실행 비교 상대 후보

[노트북](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v49-funded-sale-timing-and-worker), 목록 실행 시각2026-09-18 21:26:53UTC. 내장 SOURCE_BYTES를 정적으로 추출하고 EXPECTED_MAIN_SHA256와 일치 확인. sha256 `7d5777978465a2dd18b85fbef9d354d3cc9e008c279630e7655e5a517058b960`. 노트북 자체를 실행하지 않았다.

- V48 계보 위 `_e342_weed`: 잡초 복구로 밀린 일손 명령을 같은 날 뒤의 PASS까지 한 칸 지연, 생산 명령을 버리지 않고 복구하려는 구조. 기존 `championship_placement`의 유휴 슬롯 복구와 관련되어 개념 자체가 새롭지 않다.
- `_e346_funded`: 미래 판매를 현금으로 미리 세지 않고 현재 현금이 예정 구매+예비1000을 충당할 때 판매 보호 해제. route가 바뀔 상점 공개 경계는 넘지 않는다. `_adv_apply`에서 호출되므로 단순 미사용 코드가 아니다.
- 최종 callable은 `_e346_agent`. canonical `agent` 이름이 중간 함수여도 전역 수정으로 동작이 연결될 수 있어 실제 로더/행동 QA가 필요하다.
- 저자 평가 주장: 공개8상대·새8세계·양좌석에서 이전 버전 대비 승점 +.1367, own +73.62/margin +102.24. 확인되지 않은 저자 보고이며 현재 비공개 상위권 검증이 아니다. 생산 플래너의 탄생으로 분류하지 않는다.
- 완료: 기존 `tools/c300_execution_audit.py` 재사용, 개발7000/7001×양좌석에서 native/fast-official/fast-legacy 12QA. 모두 정상 종료, 행동·관측·최종 상태 비교8/8동일, 관측 수정0, 최대 호출0.147초. 승격 평가와 분리. 내부에서 삼킨 모든 예외까지 계측한 것은 아니다. [결과](../state/c300/public_research_20260919/v49_qa/summary.json).

### Demand-preserving timing

[노트북](https://www.kaggle.com/code/tetsutani/demand-preserving-turn-sale-timing). 보통14턴 선행매도, BAKERY2면3턴, 후반 YARN 세계 WOOL 보존을 설명한다. 고정 생산 경로 위 판매 층이며, 내장 archive의 실제 코드는 아직 추출·동등성 검사하지 않았다. 720 selfplay가 강도 증거는 아니다.

### Discrete optimization: 명칭과 코드 분리

[노트북](https://www.kaggle.com/code/guruprasaathas111/game-theoretic-master-discrete-optimization). markdown은 DP·weather·portfolio 등을 서술하지만 실제 추출 main과 V48의 공통 top-level 함수/클래스110개 중109개가 AST동일, `Chassis`만 다르며 `_dec` 하나 추가. 압축 route 자료·Chassis 차이 때문에 전체 행동 동일성은 주장하지 않는다. 별개의 독립 플래너라고 분류할 근거도 없다. 날씨 등 글의 게임 설명을 엔진 사실로 채택하지 않는다.

### Eco7 Lite: 실제 일별 상태 플래너 참고 구현

[노트북](https://www.kaggle.com/code/premaananda108/rule-agent-ecobot-v7-arena-analytics), [소스 데이터셋](https://www.kaggle.com/datasets/premaananda108/kaggricult-eco7lite), 메타데이터 Apache2.0. 현재 원본 보존, 실행·부모 채택 안 함.

- `evaluator.py`: 현재 상점 수 기반 목표, 잉여 타일 밀/당근 spot 이익 비교, 이용률85%·현금 기반 확장. 다일 시장 최적화라고 보장하지 않는다.
- `dispatch.py`: `Task.actions`에 PLANT→WATER, WATER→HARVEST, HARVEST→PLANT→WATER, BUILD→PLACE를 묶음으로 표현한다. `_compile_route`가 물자 픽업·공유 창고 예약·이동·반납을 포함하고 일별 예산 내 삽입 비용으로 배정한다.
- `main.py`: h0/1/2 및 새 일손 발생 시 계획 생성, 나머지는 하루 경로를 소비한다. 주문 이후 재고를 예상하지만 실제 체결 실패까지 보장하는 계약은 추가 감사 필요.
- 기존 base19 VRP·`vrp_persist`·c300 예약·base18 급수·c146 경로 인증과 중복된다. 차이는 단일 작업 사후 우선순위가 아니라 **복합 작업의 자원/시간 비용을 함께 검증**하는 표현이다. 전체 코드 이식보다 실제 base19 누락 계약과 대조할 가치가 있다. 강한 상대 검증이 없어 바로 부모로 바꾸지 않는다.

## 디스커션의 경험담과 한계

- [RL silver 보고](https://www.kaggle.com/competitions/kaggriculture/discussion/741743): 저자는 macro RL, behavior cloning warmup, 약30만게임을 언급. 현재 보이는 순위와 제목 당시 순위가 달라 현재 상위권 증명은 아니다. 재현할 정책/데이터/평가 명세가 충분하지 않다.
- [RL 실험](https://www.kaggle.com/competitions/kaggriculture/discussion/740022): RTX3090·350M스텝, static 상대 약90k 대122k, 새 static 모델 상대로 약70k라고 저자 보고. 단일 고정 상대 대량 학습을 상위권 일반화로 읽으면 안 된다.
- [Replay pipeline 경험](https://www.kaggle.com/competitions/kaggriculture/discussion/739273): 공개14구현·96새seed round-robin에서 신버전 우위를 보고, 테이프 공개 후 빠른 점수 하락과 runtime planner의 생산 격차를 논의. 원자료 독립 감사는 하지 않았다. 댓글의 상대가 planner라는 주장도 소스 없는 분류일 뿐이다.
- 위 댓글의 day1급식 복구 제안은 우리 c111/c147/c153과 먼저 대조한다. 기존 시스템이 있는데 새 크롤러/경기 러너/RL학습기를 만들지 않는다.

## 다음 검토의 조건

아키텍처 이름 대신 정상 세계의 생산·현금 사슬 보존과 변동 상태에서 실제 회복을 확인한다. c300/c301/c304의 국소 배정 변경은 모두 후속 멜론/토마토 생산 손실이 있었다. 복합 작업 계획을 재시도한다면 먼저 기존 base19가 이미 묶은 작업과 빠뜨린 비용을 계측해야 한다. 테이프의 약한 상대를 이용한 점수 상승과 반응형 강자 승리도 구분한다. 공개 V49는 비교 상대의 최신화 자료이고 자동 제출 후보가 아니다.

## 외부 아이디어의 작은 반증 검사: PLANT→WATER

base19는 VRP 이전의 옛 작업 묶음 코드가 남아 있어, 함수명만으로 실제 계약을 판정할 수 없었다. EcoBot의 복합 작업과 c300/c301 예약 실패를 대조한 뒤, 기존 pair_trace로 7000/7001 좌석0만 읽기 전용2재생했다. 기존 c304 감사의 부모와 **양측 행동 해시·현금2/2동일**.

- 식재 성공179/267건 중 바로 다음 스텝 급수178/266건, 지연 각1건. 이 두 세계에서 파종→급수 단절을 큰 손실 원인으로 지목할 근거는 부족하다. 신규 후보/추가 확대 없음.
- 감사의 원시 `no_plant_day_water_observed`15/18건은 모두 h22파종→h23 WATER→다음 날 같은 PLANT 생존이다. 자정에 `watered_today`가 초기화되어 단순 관측 검사로 놓쳤다. 엔진 초기 `consecutive_unwatered=1`·무급수면 자정 WEED 규칙과 대조해 즉시 급수로 추론했다. 원본 관측 flag를 실제 누락으로 읽지 않는다.
- [정정 판독](../state/c300/public_research_20260919/plant_chain_verdict.json), [원시 감사](../state/c300/public_research_20260919/plant_chain_audit.json). 전략 변경 없이 감사 해석 오류를 바로잡았고 원자료는 보존했다. 다른 복합 작업·물자 예약까지 정상임을 증명한 것은 아니다.
