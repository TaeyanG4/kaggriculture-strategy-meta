# Public League 대결·공식 리그 일치 감사

2026-09-21 09:54 KST / Codex. 사용자 요청: 코드 수정 없이 치명적 문제와 규칙 일치 확인.
이번 작업은 소스·기존 결과·읽기 전용 SQLite·공식 페이지/API 조회만 수행했다. 신규 시뮬레이션, 전략 변경, 설정 변경, 서비스 재시작/중지는 하지 않았다. 기존 연속 대결은 계속 실행 중이므로 아래 수치는 고정된 조회 시점의 값이다.

## 결론

빠른 단일 Python 소스로 정상 완주하는 모델들의 게임 계산과 승패 기록은 신뢰할 근거가 있다. 전체 결과를 폐기할 치명적인 승패 역전/엔진 불일치는 발견하지 못했다. 그러나 **모든 공개 모델을 온전하게 비교하거나 실전 실행 적합성을 판정하는 리그로는 중요한 결함**이 있다. 다중 파일 추출 누락과 짧은 전체 경기 제한이 일부 상대를 체계적으로 제외한다. 로컬 순위는 현재 공개 풀에 대한 선별 지표이며 공식 순위/점수 복제는 아니다.

## 확인한 정상 항목

- 설치된 `kaggle-environments`는 1.32.7. 공식 GitHub master의 `kaggriculture.py` 및 `kaggriculture.json`을 조회해 줄바꿈 정규화 후 로컬 파일과 동일함을 확인했다. GitHub가 곧 배포 서버라는 가정은 하지 않았으며 실제 최근 c358 episode **111420532**도 별도로 조회했다.
- 그 실전 replay의 module_version=1.32.7, episodeSteps=720, actTimeout=1, runTimeout=1200, boardSize=10, startingMoney=3000, marketOrders=10, shedCapacity=100, turnsPerDay=24, shop/center 소비 간격4/24, shop 해금3일, weedChance=.005, marketParams={}가 로컬 기본 설정과 일치한다. 초기 remainingOverageTime=60도 일치한다.
- `championship_league.run_match`는 공식 `make(...).run(agents)`를 호출한다. 두 모델 모두 관측을 보고 반응하며 상대 행동 동결, 미래 상점 고정, 숨은 seed 제공은 하지 않는다. 같은 seed의 양 좌석을 예약한다.
- SQLite 읽기 전용 스냅샷 **11,171 complete / 최대 complete id11438 / engine hash 1종**을 전수 판독했다. seed/resolved_seed, candidate seat, 보상 좌석 매핑, 최종 현금 차, 승/무/패 점수(1/.5/0), 720 states, 각719 calls, DONE/DONE, native_reacting, 수집된 예외 없음 조건에 불일치 **0**이었다. 이 검사는 저장 기록의 내부 일관성 검사이며 11,171경기를 다시 실행한 것은 아니다.
- 앞선 스냅샷에서 complete/complete 양좌석5,462쌍, complete/invalid1쌍, 한 좌석만 완료2쌍이었다. 진행 중이거나 중지/실패한 한 좌석은 제외되므로 모든 시점에서 완벽히 양좌석 균형인 것은 아니다. 현재 대규모 편향 증거는 없다.
- 실제 저장 설정은 자동수집3시간, workers8, batch240. 배치240은 순위 갱신 단위이며 연속 대결의 총 종료 한도가 아니다.

## 중요 문제 1 — 제출 묶음 누락·잘못된 소스 선택 (확인됨)

`public_league.py:850`의 archive 추출은 `main.py`만 가져온다. 노트북 writefile 추출도 main만 우선하고, 실행은 SHA 이름의 단일 파일을 공통 sources 폴더에서 수행한다. 공식 Getting Started는 helper.py/model_weights.pkl 등을 포함한 다중 파일 tar.gz 제출을 명시적으로 지원한다.

현재 quarantine9개를 정적으로 재검토했다.

- agent13/54/63/128: 노트북은 C++ 소스와 **agent.so를 함께 빌드·포장**하지만 리그에는 Python bridge만 있다. Windows에서 Linux .so를 그대로 실행할 수도 없다.
- agent67/75: 노트북은 **actions.json**을 함께 포함하지만 리그에는 없어서 실패한다.
- agent88 `Kaggriculture | 2476.8 Peak | LightGBM + XGBoost`: router_base.py, observation.py, actions.json, model.json 등의 제출 자산이 필요하지만 누락되어 실패한다.
- agent21: 과거 `extracted_main.py`라는 **제출물 생성 스크립트**를 플레이 정책으로 선택했다. 저장된 QA entrypoint는 `Path`이며 첫 행동에서 Struct를 경로로 넘기는 TypeError가 난다. `_qa_main`은 마지막 객체가 callable인지까지만 확인하므로 이 잘못된 추출을 통과시켰다. 이는 원래 전략의 TypeError라는 증거가 아니다.
- agent82 RL: 아래 전체 경기90초 제한으로 격리됐다.

따라서 이전 HANDOFF의 “실제 코드/의존성 오류라 유지”는 **현재 로컬 포장/환경에서 실패한다는 의미로 제한**해야 한다. 원본 제출의 결함이나 Kaggle 실행 불가를 입증한 것이 아니다. 특히 agent128도 원본 agent.so가 없는 로컬 bridge 실패다.

신원도 현재는 main 소스 SHA만 사용하므로 helper/model이 다르고 main이 같으면 구분하지 못한다. 실제 잘못 병합된 사례는 이번에 확정하지 않았다(agent13의 두 notebook은 점검한 C++ 자산도 같았다).

## 중요 문제 2 — 시간·실행 환경은 실전 재현이 아님 (확인됨)

- 공식 게임은 행동당1초 + **경기 전체에 걸쳐 사용할 초과시간60초**다. `agent.py`는 이번 행동의 (duration−1)이 남은 overage보다 크면 TIMEOUT 처리하며 `core.py`가 초과분을 차감한다. “한 번1초 초과=실전 탈락”은 잘못된 설명이다.
- 로컬도 이 공식 엔진 처리를 유지하지만, 별도로 max action>1.5이면 결과를 invalid 처리하고 4회·2상대 조건에 격리한다. 따라서 단발2초라도 overage가 충분하면 공식 엔진에서는 허용될 수 있는데 리그는 제외한다. 1.5는 사용자 요청의 로컬 운영 기준이며 공식 제한이 아니다.
- 더 큰 차이는 `public_league.py:1365`의 **전체 subprocess90초 제한**이다. 실전 replay의 runTimeout은1200이다. 예를 들어 행동당0.2초인 모델은 개별 제한에는 충분히 들어가도 719행동만으로143.8초여서 이 로컬 제한에 걸릴 수 있다. 이는 예시이며 실제 RL 실행시간의 측정치가 아니다.
- RL agent82는 17상대50경기가 전체90초 timeout이었다. 이것만으로 실전1초 실패나 원본 불량이라고 결론 낼 수 없다. 빠른 tape/branch 정책에 유리하고 계산량이 큰 정책을 제외할 수 있는 구조다.
- 로컬은 Windows, 한 match process에서 두 정책을 순차 호출하며8경기를 병렬 실행한다. Kaggle 공식 FAQ는 별도 Docker 환경을 안내한다. CPU 부하·라이브러리·파일/프로세스 격리가 다르므로 로컬 wall time을 실전 성능으로 환산하면 안 된다. 공유 모듈/난수 상태 간섭의 가능성은 있으나 이번에 특정 모델의 결과 오염을 입증하지 않았다.
- 임의 telemetry의 이름에 error가 들어가고 값이 양수면 health 실패로 보는 규칙도 공식 규칙이 아니다. 현재 양성 오류 집계를 전략 예외와 항상 동일시할 수 없다.

## 의도된 차이 — 상대 선정·점수·통계

공식 Evaluation 페이지를 이번에 직접 재조회했다: 비슷한 skill rating 상대와 대결, 최신2제출 활성, 신규 제출 더 자주 매칭, 승/패/무만 rating에 반영, 최종은 추가 경기 후 Bradley–Terry. 현금 차의 크기는 공식 점수에 직접 입력되지 않는다.

로컬은 최대50개 풀(기존 active 상위40 + challenger 슬롯)을 구성하고 경기 수 부족/덜 만난 pair를 우선한다. 신규 우선권은32경기까지이고 focus는 특정 모델 대전을 추가한다. 양좌석 동일seed는 좋은 비교 설계지만 Kaggle의 유사실력 매칭과 같지는 않다. 오래된 공개 버전/유사 계보/우리 과거 버전도 별도 소스로 남고 비공개 최신 강자는 빠진다. 동일 main만 중복 제거하므로 계보 가중치를 동일시할 수 없다.

`update_rankings:1492`는 모두1500에서 시작해12회 일괄 Elo 업데이트하며 각 모델의 총 delta를 sqrt(경기수)로 나눈다. 공식 실시간 rating 및 최종 Bradley–Terry의 복제가 아니다. 별도 읽기 전용 재계산에서 반복11/12/13/24/60의 상위8 순서는 같았으나 점수 크기는 계속 변했다(예: agent117은12회2171.9,60회2509.1). 현재 상위 순위가 무너진다는 증거는 없지만 그 점수 차를 보정된 실전 확률로 읽으면 안 된다.

Wilson 구간은 양좌석의 공통 seed, 서로 다른 상대 난이도, 적응적 표집을 반영한 승격 검정이 아니다. 버전별 source SHA가 seed를 바꾸므로 리그 순위만으로 미세 개선의 paired 효과를 확정하지 않는다. 무효경기는 로컬 승패에서 제외되므로 실행 실패 위험도 점수와 분리되어 있다.

## 재현성·설정 문서의 보조 문제

- `configs/public_league_v1.json`은 현재 실행 모듈이 로드하는 설정 파일이 아니다. 실제 설정은 코드 기본값과 DB runtime_settings다. JSON의 runtime_failure_quarantine_threshold=2는 새 timing1.5초/4회/2상대 규칙을 표현하지 못한다. 현재3시간은 DB에 정상이나 빈 DB용 코드 기본값은 여전히0.5시간이다.
- match key에는 engine/source/seed/seat가 있지만 runner hash/설정/시간판정 버전은 없다. rating도 모든 engine의 complete를 합산한다. 현재 엔진은1종이므로 혼합 엔진 오염은 없었으나 향후 변경 때 계약 구분이 필요하다. normalize는 resolved_seed 조건을 재확인하지 않지만 이번 모든 complete 기록의 seed는 일치했다.

## 현재 실전 관측의 범위

공개 ListEpisodes에서 PUBLIC·COMPLETED이며 양쪽 보상이 있는 경기만 계산하고 validation self-play는 제외했다.

- c358 submission56402500: **92경기69승23패**, 최신완료2026-09-21 09:34:29 KST, updated score2741.7068, 상대 initial score 평균2381.4.
- c365 submission56407947: **17경기16승1패**, 최신완료09:48:08 KST, updated score1503.1161, 상대 initial score 평균1072.7.

로컬 상위가 실전에서도 잘한다는 관찰과 c358 기록은 양립한다. c365는 아직 다른 상대 대역에서 올라오는 중이므로 낮은 현재 점수로 로컬 순위를 반박하거나16/17로 c358 우위를 확정하면 안 된다. 여러 모델의 동시점·충분한 경기·상대층 보정 상관관계는 이번에 산출하지 않았다.

## 이후 수정한다면 우선순위 (이번에는 미실행)

1. 제출 bundle 전체와 Linux 실행 환경을 보존하고 source/asset 신원을 함께 관리. builder를 정책으로 선택하지 않도록 추출·QA 강화.
2. 운영용 시간 제한과 공식 실행 적합성 판정을 분리. 기존 quarantine은 원본불량/로컬자산누락/환경미지원/로컬시간제한을 구분.
3. 공식과 가까운 강자 매칭/별도 Bradley–Terry 검증을 추가하되 기존 승패 기록은 보존. 미세 개선 검증은 공통 seed·상대·양좌석 별도 패널로 수행.
4. 코드·설정·판정 규칙 버전과 결과 캐시 계약 통합.

## 출처

- [공식 Evaluation](https://www.kaggle.com/competitions/kaggriculture/overview/evaluation), [Getting Started](https://www.kaggle.com/competitions/kaggriculture/overview/getting-started-test-locally-submit), [FAQ](https://www.kaggle.com/competitions/kaggriculture/overview/frequently-asked-questions): 공개 `competitions.PageService/ListPages`, competitionId147734, page742992/743119/803810을2026-09-21 재조회.
- [공식 game source](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.py), [설정](https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kaggriculture/kaggriculture.json).
- [최근 실전 replay111420532](https://www.kaggleusercontent.com/episodes/111420532.json).
- 구현: `src/kaggriculture_meta/public_league.py`, `src/kaggriculture_meta/championship_league.py`; 상태: `state/public_league/league.sqlite3`(mode=ro); 노트북 원본: DB aliases/notebook_versions의 archive_path.
- 선행: HANDOFF START HERE, `reports/c300-public-research-2026-09-19.ko.md`, `state/c356_live_gap/results/summary.json`. 과거 감사 수치를 새 검증으로 세지 않았다.
