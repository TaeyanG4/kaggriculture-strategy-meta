# 연구 도구 사용 입구

현재 상태·결정·이력은 **HANDOFF.md 한 곳**에 기록한다. 이 파일은 명령 안내이며 작업 원장이 아니다.

## 독립 검증 기록을 League 전적·BT에 일괄 편입

`tools/import_validation_league.py`는 완료된 v2/v3 native reacting 캠페인을 기존 League DB로 가져온다. 경기 재실행이나 후보 자동 등록을 하지 않는다. 최종 리뷰와 적격 후보 로컬 등록 후, 모든 screen/confirm 경로를 한 호출에 전달한다. 이후 후보도 같은 코드를 재사용한다.

```powershell
.venv/Scripts/python.exe -X utf8 tools/import_validation_league.py check state/agent_experiments/NAME_screen state/agent_experiments/NAME_confirm
.venv/Scripts/python.exe -X utf8 tools/import_validation_league.py apply state/agent_experiments/NAME_screen state/agent_experiments/NAME_confirm
.venv/Scripts/python.exe -X utf8 tools/import_validation_league.py verify state/agent_experiments/NAME_screen state/agent_experiments/NAME_confirm
```

- `check`/`verify`는 읽기 전용이다. 전체 캠페인 완료·동결 계약/엔진/소스·등록 artifact·공식 DONE/좌석/현금/행동 신원을 확인한다. 미등록 소스가 있으면 `ready=false`와 누락 목록을 출력하며 `apply`는 전체 쓰기를 보류한다. 실행 sidecar가 있는 소스를 단일파일 검증과 동일시하지 않는다.
- 승·패·무를 모두 편입하며 같은 소스끼리 경기와 기존 중복은 제외한다. 승패별/상대별 선별 옵션은 없다. 같은 source SHA의 등록 artifact가 여러 개면 `--agent-map MAP.json`으로 정확한 기존 ID를 지정한다.
- 일반 League와 같은 잠금/경기 key를 사용한다. 한 SQL 트랜잭션으로 일괄 저장 후 기존 `update_rankings`를 한 번 호출한다. `validation_import_refs`에 원래 계약·경기·결과 SHA를 저장하므로 도중 중단이나 이후 League wrapper 변경에도 같은 결과를 중복 계산하지 않는다. 소유자 은퇴 명단과 운영 설정은 보존한다.
- `state/public_league/validation-imports/`에 전후 전적·점수와 검증된 key 영수증이 자동 저장된다. 추가경기 0으로 재실행하면 재적합도 생략하며, 행 저장 뒤 중단된 경우 같은 명령이 점수 계산을 마무리한다. `--state`/`--receipt`로 별도 DB/영수증을 지정할 수 있다.
- 이 전적은 고정 검증 상대·세계에서 얻은 자료다. provenance에 원래 캠페인과 조건을 남기며 일반 League의 다양한 상대 전적 또는 Kaggle 승률과 동일시하지 않는다. 공식 live 점수는 변경하지 않는다.

검증: `python -m unittest tests.test_validation_league_import`. 실제 완료 캐시를 임시 DB에서 검증하려면 `VALIDATION_IMPORT_INTEGRATION_CAMPAIGN` 환경 변수에 캠페인 경로를 지정한다. 미등록 후보는 테스트 DB에만 fixture로 넣고 실제 League 등록/경기 실행/DB 변경은 하지 않는다.

## Public League와 라이브 리플레이 재사용 지도 (2026-09-20)

새 수집기나 분석기를 만들기 전에 아래 도구의 입력·출력과 기존 캐시를 확인한다.

- `src/kaggriculture_meta/public_league.py`: 공개 노트북 목록·점수·버전·exact-source alias·native 리그·대시보드의 통합 서비스. 예약 수집은 현재 3시간이며 배터리/절전 복귀를 지원한다. 대결은 수동 중지까지 연속 실행하고 백그라운드 탭 heartbeat는 3분까지 허용한다. agent를 추출할 수 없는 노트북은 `수집됨·대전 불가` 탭에서 확인한다.
- `o_tools/live_episodes.py`: submission ID의 공개 Episode 목록, W/L/T, 상대 submission/team/rating을 저장한다.
- `o_tools/fetch_current_elite.py`: 지정한 상위권 submission ID의 새 replay만 증분 다운로드한다. 출력의 `rating now`는 다운로드된 표본의 최대값이므로 현재 평점으로 사용하지 않는다.
- `o_tools/live_suite.py`: 우리 최근 제출의 승·패 전체 replay와 12개 chunk를 구성한다.
- `o_tools/r_crawl.py`: top-10 archive shard, 우리 제출 live loss, 기존 원장 도구를 하나의 증분 상태로 묶는다. 현재 leaderboard 상위 팀 전체를 자동 추적하는 서비스는 아니다.
- `o_tools/rival_source_trace.py`: 첫 K개 시장 행동 fingerprint를 공개 소스와 대조하고 선택적으로 720-step 재현한다. fingerprint 일치만으로 exact source라고 부르지 않는다.
- `o_tools/elite_profile.py`: replay를 엔진 실행 없이 읽어 checkpoint 농장 상태와 3구간 생산·구매·판매·작업 프로필을 만든다.
- `o_tools/branch_stats.py`: 상점 세계와 d6/d8/d10 축군 선택의 관측 통계를 만든다. 상관관계를 정책의 인과 분기로 단정하지 않는다.
- `o_tools/live_replay_audit.py`, `src/kaggriculture_meta/replay_accounting.py`: 로컬 소스의 live 행동 동일성과 실행 원장을 감사한다.

**2026-09-28 c524 정정:** Kaggle CLI의 team ID 조회와 달리, 읽기 전용 `POST https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard`에 `{"competitionId":147734}`를 보내면 `publicLeaderboard` 행에 표시 순위의 `teamId`·`submissionId`가 함께 나온다. HTTP200·10099행으로 직접 확인했다. 팀 이름은 응답의 `teams.teamId`로 연결한다(`teams.id`가 아님). 원 응답과 시점별 판독은 `state/c524/leaderboard-endpoint-readback.json`, `leaderboard-resolution-review.json`에 있다. 표시 제출ID와 팀의 최신 제출은 다를 수 있으며 조회 시점을 보존한다.

`EpisodeService/ListEpisodes`는 여전히 `submissionId`가 필요하므로 이 직접 매핑을 기존 `live_episodes.py`/`fetch_current_elite.py`에 사용한다. 직접 API를 사용할 수 없으면 알려진 활성 제출의 `teams`, `submissions`, episode agent 행으로 팀→submission 그래프를 증분 복원한다. 2026-09-20 점검의583경기에서 당시 Top10을 발견한 결과는 이 보조 경로의 근거다. 그래프의 국소 최고점이 전체1위라는 보장은 없고 새 제출 탐지가 늦을 수 있다. c524는 주기 감시 서비스나 수집기를 새로 구현하지 않았고 대량 리플레이도 받지 않았다.

라이브 유형 표시는 다음 신뢰도 순서를 지킨다.

1. 공개 소스와 720-step 행동 재현: exact verified.
2. 여러 경기의 행동 fingerprint·체크포인트가 알려진 계보와 일치: lineage likely.
3. 상점/가격/상대 행동에 따른 반복적인 선택 변화만 관측: behavioural reactive/router/planner-like.
4. 근거 부족: unknown private policy.

리플레이 한 경기의 평균 크기는 기존 자료에서 약 31MB다. 상위 10개 제출을 각각 최근 50경기까지 단순 수집하면 중복 전 최대 약 500경기·15GB이므로 episode ID 중복 제거와 증분 다운로드가 필수다.

## 읽기와 판독

- `tools/league_agent_audit.py --agent-id ID --expected-games N --out state/...json`: League DB를 읽기 전용으로 열어 경기/소스·전체 artifact/시드·좌석/현금/공식 DONE·호출·오류를 감사하고 공개 상대별 전적을 계산한다. `--since-id`(제외)와 `--through-id`(포함)로 집중 측정 코호트를 고정하고, 예약 결산 후보는 `--telemetry-prefix c405`로 결산/차감 균형도 검사한다. 기존 artifact·match-key·세계별 sign-test 함수를 재사용하며 순위·DB·대진을 변경하지 않는다. 두 좌석은 한 세계로 묶고 exact-source 별칭은 추가 상대로 세지 않는다. 상대별 시드와 선택 빈도가 다르므로 결과는 관측 전적이며 단순 전체 승률만으로 후보 개선/현재 실전 강도를 증명하지 않는다. 검증: 기존 c402 집중500의 445W41L14T/250세계/133상대와 소스·health 감사 일치. 전략의 전체 생산/급식 원장 검사는 별도다.

- `tools/build_c397_shadow_coverage.py`: 공개 정책 가정 추가 빌더. 기본 c397 바이트 재현을 유지하며 `--parent`, `--parent-sha256`, `--review-dir`, `--candidate-id`, `--source-ids`로 다음 후보에 재사용한다. review-dir의 provenance와 소스별719행동/private·718공개전이 검사를 요구한다. 추가 가정 진단은 전체 강도 개선 증거가 아니므로 native/OFF/회계와 독립검증을 별도로 수행한다.

먼저 아래 명령으로 관련 선행 시도 최대4개와 원문 줄번호를 찾는다. 검색 누락은 미시도 증명이 아니며 필요하면 `rg`로 도구/보고서까지 넓힌다.

```powershell
.venv/Scripts/python.exe -X utf8 tools/research_ops.py history "c353"
.venv/Scripts/python.exe -X utf8 tools/research_ops.py progress state/agent_experiments/CAMPAIGN
.venv/Scripts/python.exe -X utf8 tools/research_ops.py summary state/agent_experiments/CAMPAIGN --save state/EXPERIMENT/readout.json
```

summary는 기존 validation_v2의 계약/원자료 검사를 사용하고 통계를 재계산해 저장집계와 일치해야 출력한다. 완료 전 부분 성능은 판독하지 않는다. 출력은 전적/CI/마진/상대별 회귀이며 승격 여부는 원래 사전기준으로 판단한다. `--save`는 새로운 파생 JSON만 만들고 기존 파일은 덮어쓰지 않는다.

`excluding_named_parent_descriptive`는 2026-09-24부터 모델/상대 이름 대신 동결 source SHA로 정확 부모를 제외하며 `excluded_opponents`를 남긴다. 이전 readout은 `parent` 모델이 `c407` 같은 상대 별칭으로 등장하면 제외가 누락될 수 있으므로 필요할 때 새 파일로 재판독한다. 이는 정확 부모만 뺀 단순 기술통계이며 다른 우리 모델이나 같은 계보까지 제거한 공개 전용/독립 표본 통계가 아니다. 원래 승격 gate에는 이 보조 필드를 사용하지 않는다.

통과 모델만 다음 단계 실행에 남길 때 아래 명령을 쓴다. 원래 가설당 alpha를 유지하고 탈락 모델의 예산을 재배정하지 않는다. 기존 config/캠페인은 불변이며 새 경로를 사용한다.

```powershell
.venv/Scripts/python.exe -X utf8 tools/research_ops.py subset configs/validation/ORIGINAL.json --models candidate,parent --out configs/validation/NEW.json
./tools/run-validation-v2.ps1 -Config configs/validation/NEW.json -Out state/agent_experiments/NEW -Stage confirm -Action Run
```

## 재사용할 실행 기능

- 반응형 경기: `tools/validation_v2.py` + `tools/run-validation-v2.ps1`, 현재 기본8워커이며 경합 시6 등으로 낮춘 별도 계약을 만든다. 동결 러너 수정 금지.
- 2026-09-23부터 새 시간계약은 `validation_v3.py` + `run-validation-v3.ps1`로 공식 overage 판정을 따른다. v2 실행/해시/통계를 재사용하며 **DONE720·719calls·예외0·seed일치**일 때만 단발1초초과를 경고로 보존한다. 실제 TIMEOUT·내부오류counter·신원불일치는 계속 실패다. 기존 v2 캠페인의 실패를 덮어쓰지 않고 새 config에 `arena_meta.validation_health_policy=official_overage_v3`를 명시한다. `research_ops.py summary`는 이 필드로 올바른 계약을 선택하고 경고 경기 수도 보고한다. c384의 중단2회는 성능증거에서 제외됐다.
- 새 League 상대를 연구 runner로 옮기기 전 `agents.artifact_files_json`과 실제 파일을 확인한다. League v2의 다중 파일 실행과 달리 연구 validation_v2는 단일 소스 snapshot이므로 `main.py` 경로만 복사하면 helper를 잃을 수 있다. 다중 파일 상대는 기존 modular/bundle QA 방식으로 독립 namespace·데이터를 보존한 번들을 만들고 양좌석 전체 행동/최종상태 동일성을 확인한 뒤 새 계약에 고정한다. Fieldcraft `mirror_plan.py` 사례: `state/c371/fieldcraft_bundle_qa.py`; 실패 원본/부분결과는 보존하고 성능 판정에 쓰지 않는다.
- 원본/계측·native/fast 동일성: `tools/c300_execution_audit.py`의 `game`, `compare`.
- 공개 경기 목록/리플레이: `o_tools/fetch_current_elite.py` (`--max 0`은 목록만), `o_tools/live_episodes.py`.
- 제출 행동 재현: `o_tools/live_replay_audit.py`, 계측 재사용 예 `state/c312/audit_live_identity.py`.
- 동결 상대 진단: `o_tools/elite_pool.py`; 반응형 강도 증거와 구분.
- 오라클 진단(o401, 2026-09-24): `o_tools/proxy_eval.py`는 `PROXY_ENGINE_CFG`(JSON, 엔진 설정 병합·양 플레이어에 적용, 예 `{"farmHandCostMult": 0}`)와 `PROXY_ENGINE_PATCH`(`apply(engine[, seat_b])`를 가진 파일, 예 `state/o401/engine_patch.py`의 TELEPORT 명령·`engine_patch_sales.py`의 기준가 판매)를 지원하며 두 값은 설정됐을 때만 캐시 키에 들어간다. 플래너 사본 `state/o401/p401_planner.py`의 `sw_tp1/sw_tp0` 스위치와 함께 상한 진단에만 쓰고 후보 성능으로 읽지 않는다. 판독 `state/o401/readout.json`.
- 원장: 기존 `replay_accounting` 계열을 검색해 사용. 단순 현금차를 특정 개입 비용으로 해석하지 않는다.
- Kaggle replay JSON은 재고 키 순서를 정렬할 수 있다. 용량 제한 입고 순서에 민감한 정책을 저장 관측으로 재호출했을 때 행동이 다르면 소스 불일치로 단정하지 않는다. 공식 엔진에서 원래 행동을 처음부터 재생하고 모든 경제 관측 값·보상을 대조해 삽입 순서를 복원한 뒤 재검사한다. c329 및 c415의 38패 중 4건 사례; 재사용 예 `state/c415/restore_live_order.py`. 원본 JSON은 보존하고 복원본을 분리한다.
- 공동 생산·경로: c353이 c340 공동선택/c341 생성/c344 물리검사/c352 점유검사를 재사용. 새 알고리즘 전에 해당 입력 계약을 확인한다.

## 출력과 사용량 규칙

- 모든 후속 세션은 [CPU 완료 후 자동 재개 절차](completion-driven-research.ko.md)를 따른다. 대기 중 모델의 반복 `wait`/`sleep`/`progress` 호출을 피하고, 도구/프로세스 내부 대기 → 완료·실패 이벤트 한 번 → 자동 리뷰·다음 작업으로 연결한다. 감지기만 실행하고 앱 후속 메시지 연결을 빠뜨리지 않는다.
- 전체 HANDOFF·큰 JSON·전체 소스를 반복 출력하지 않는다. 현재 상태, 관련 이력, 변경 함수, 실패 조건 순서로 읽는다.
- 오래 걸리는 명령은 stdout/stderr를 해당 실험 로그에 저장한다. 기본 도구 출력은 완료 요약 또는 실패 tail만. 라이브러리 초기화 로그를 대화로 흘리지 않는다.
- 한 캠페인씩 실행한다. 긴 실행은 기존 진행률/종료 도구를 쓰고, 반복 polling은 최소화한다. 필요한 사용자 진행 보고는 유지한다.
- 같은 결과 수치를 별도 집계 코드로 다시 구현하지 않는다. 파생 readout JSON을 근거로 HANDOFF에 판정·한계·다음 지점만 짧게 쓴다.
- 연구 도구 정리는 최소 범위로 하고 곧바로 전략 연구로 복귀한다. 토큰 절감률은 실측 전 주장하지 않는다. 모델을 자동 전환한다고 가정하지 않는다.


## 관측 지원조건의 새 확인 공통체인

`tools/supported_confirmation.py --out state/<실험>`은 동결 plan/config-template과 probe/trace entry를 받아 보상 없는 조건 접두선정→기존validation_v3 screen/confirm→기존정확재현/회계→completion/error를 한 OS체인으로 잇는다. c499가 첫 적용이다. 기존c495의144상점/c493고정 분기를 새후보마다 복사하는 대신 지원조건 모듈과설정을 추가한다. 단일전역lease/8worker/소스계약검증·완료캐시를 유지하고 등록/전적편입/제출하지 않는다. 입력gate와평가구현을동결전에함께검토한다. Windows알림은기존공통notifier를 실제coordinator PID로 별도숨김연결한다.


## 2026-09-28 빠른 개선·동일 실행검증

소유자 요청: 총8CPU, 약16반응경기, 중복양좌석 없이 최신패배/관련상대/양수대조에 집중한다. 작은 표본의 통계적 확신은128경기와 같지 않다. 이미 정확한 동일 부모/엔진/조건/좌석 캐시를 재사용하고 공식 최초경기에 리플레이를 저장해 회계용 재대결을 없앤다. 경기수를 줄여도 공식DONE/시간/소스hash/추가무효·급식·자금·탈출·야간폐기·종료검사와 모든 계획결과 보고는 유지한다.

`tools/research_response_audit.py:trace`는 기존c470/c526의719턴 응답/상대private/관측불변 검사를 한 번 수행하고, `extract`로 같은 실행의 서비스 상태를 회수한다. 선택적인 `prepare/on_step` 관측기를 붙이면 추가 전체재생 없이 원인기록을 수집한다. c538에서 기존응답원자료와 서비스원자료의 정확동일성을 검증한다. 동결된 과거chain은 수정하지 않는다. 원점수·계약·blind 불변이며 새시장정책에 재사용할 때 상대key/지원범위를 명시한다.

실측 c53316경기+회계+후처리는215.59초, c5374경로저장진단30.96초. 단일pass는 두 번이던719정책호출을 한 번으로 줄이지만 전체속도 개선율은 아직 측정하지 않았다. 모델의 설계·리뷰 시간도 전체개선속도의 일부이며 CPU대기만으로 처리량을 설명하지 않는다.


### 명시적 단좌석 소규모 검증 편입

`tools/import_validation_league.py seal-bounded state/CHAIN`은 이미 완료된 명시적 `plan.jobs` 일정의 원본/완료자료를 `bounded-import.json`으로 봉인한다. 이후 같은 공통 `check/apply/verify state/CHAIN`을 사용한다. 게임·등록을 실행하지 않으며 v2의 양좌석 일정을 가공해 만든 것처럼 표시하지 않는다. 원identity의plan/source/support, 계약·job해시, 공식DONE720/719timing/health/보상·양측actionhash, 전일정의완료를 검사한다. 캐시는 원공식manifest의계약·job을재검증하고 source/engine/seed/seat/config를대조한다. 원cachedcontract/match/resultSHA를 편입참조로 유지해 과거편입경기를 다시평가하지 않는다. 도구지원: `tools/bounded_validation_import.py`. 24경기요청은후속사전동결계약에적용하며기존16완료계약을변경하지않는다.

봉인된 bounded 부모의 첫경기공식결과도 캐시로 편입할 수 있다. 공통 adapter가 부모전체seal/plan/engine/source/완료결과를 재귀검증하고 원contract/match/resultSHA를 유지한다. 순환참조·부모봉인변경·다른조건매핑은 거절하며 과거전적을 재계산하지 않는다.
