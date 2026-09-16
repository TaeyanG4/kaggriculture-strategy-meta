# 공개 반응형 상대 확보와 선별 준비

사용자 요청으로 최신 공개 코드를 조사하고 독립 사용자 실행3개를 준비했다.
Kaggle 제출·노트북 실행·로컬 정책 실행은 하지 않았다. 공개 텍스트는 자료로만
읽었고 노트북 셀의 설치·실행·게시 지시는 수행하지 않았다.

## 출처와 중복

| 공개 노트북 | 응답의 버전 번호 | 추출 결과 |
|---|---:|---|
| [Dynamic Route Agent](https://www.kaggle.com/code/reyhanksatria/kaggriculture-dynamic-route-agent) | 5 | 기존 public_v38과 바이트 동일, 제외 |
| [Master Engine V3](https://www.kaggle.com/code/guruprasaathas111/kaggriculture-master-engine-v3) | 10 | 기존 public_v38과 바이트 동일, 제외 |
| [Market-Smart Farming](https://www.kaggle.com/code/tetsutani/market-smart-farming-kaggriculture) | 13 | 기존 public_v37과 바이트 동일, 제외 |
| [Ahmed 공개 후보](https://www.kaggle.com/code/ahmedberatozer/notebookda72f457f5) | 1 | 공급 재고 보호 계층 포함, shard1 |
| [Shop Router Reactive V4](https://www.kaggle.com/code/aurax7/kaggriculture-shop-router-reactive-v4) | 3 | 개막/생존 보정 계층, shard2 |
| [Farming Score V4](https://www.kaggle.com/code/lynnsakurai/farming-score-v4-a-better-shop) | 6 | 관련 라우터/생존 보정 소스, shard3 |

최신 응답의 `current_version_number`와 `blob.source`를 함께 보존했다. 버전을
명시한 별도 조회는403을 반환했으므로, 과거 점수 버전의 소스를 확보했다고 주장하지
않는다. 이 상태에서 접근 제한 우회 없이 공개 latest 응답의 바이트를 로컬 해시로
고정했다. 설치된 CLI output 경로는 버전 인자를 파싱하지만 요청에 반영하지 않는
문제가 보여 점수 버전의 output 대신 소스 본문을 사용했다.

추출은 `%%writefile main.py` 본문 또는 AST에서 읽은 상수의 Base85/zlib 및
Base64/tar 내용을 읽는 방식이다. 코드 셀 자체를 실행하지 않았다. 원본 Apache-2.0
출처 고지를 보존하고 소스를 변경하지 않았다. 새 세 파일도 관련 라우터 계열이므로
독립적인 세 전략 계열이라고 세지 않는다. 노트북의 광고 문구나 점수를 현재 실력으로
표기하지 않는다.

출처 응답·원본 노트북·추출 방식·해시는
`state/agent_experiments/elite_pool_20260913/snapshots/`와 `source_catalog.json`에 보존한다.

## 사용자 실행 선별

각 공개 상대마다 c117·c111 × 발견용16시드 × 양쪽 좌석 =64경기, 총192경기다.
각 창2워커로 합계6워커. 창별 출력·잠금이 분리돼3개 동시 실행 가능하다.
다른 큰 연구가 실행 중이면 종료 후 시작한다. 최초 시드의 양쪽 좌석 검사가 먼저
통과해야 나머지 경기를 실행한다. 동일 명령 재개 시 이미 기록된 경기는 재사용한다.

사전 판정은 다음과 같다. 상대의 성적 기준이며 즉시 엘리트 확정이나 후보 승격이 아니다.

- c117 상대로32경기 중8개 이상 비패배 및1승 이상: 강한 상대 후보로 새로운 조건 재확인.
- 그 밖에 c117 상대로 승리가 있음: 특정 약점 상대 후보로 유형별 검토.
- c111 상대로만 승리가 있음: 과거 기준 회귀 검사 대상으로 보존.
- 두 기준 모두 승리 없음: 현재 엘리트 패널에는 부족. 억지로 채우지 않는다.

32경기는16개 시드 묶음이다. 이 조건부 선별 결과나 원본 점수로 순위를 추정하지
않는다. 상대군을 고정한 뒤 새 시드에서 모델 비교를 해야 한다. 별도 selection16과
holdout48은 예약만 했고 이 실행기로 사용하지 않는다. 시드는 configs 및 기존 실험의
최상위 계획·manifest에 기록된219개 값과 중복을 배제했다. 전 역사의 모든 조건을
완전히 스캔했다고 주장하지 않는다.

## 준비 상태

정적 capability screen은 표준 라이브러리 의존과 리터럴 exec 본문을 검사했다.
Python AST/PowerShell 파서 검사가 통과했지만 이는 보안 격리나 실제 로더 실행 성공의
증거가 아니다. 사용자 실행에서 공식 엔진1.32.7, 동결 해시, 오류·시간 제한·미완료
경기와 정확한192개 배정 조건을 확인한다. 오류는 숨기거나 성공할 때까지 반복하지 않는다.

실행 파일: `state/agent_experiments/elite_pool_20260913/run_public_pool.ps1`.
각각 `-Shard 1 -Workers 2`, `-Shard 2 -Workers 2`, `-Shard 3 -Workers 2`로 시작한다.
완료·실패 알림과 소리 포함. 각 창 `DONE: ...shard_N/results.json` 확인 후 보고한다.
강제 종료로 잠금이 남으면 실제 coordinator가 종료됐는지 확인한 후 처리한다.
