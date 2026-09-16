# 재사용 검증 v1

새 후보마다 실행기를 복사하지 않는다. 공통 실행기 `tools/validation_v1.py`,
공통 분석기 `tools/validation_stats_v1.py`, PowerShell 진입점 `tools/run-validation.ps1`을
사용하고 설정 JSON과 결과 디렉터리만 새로 만든다. 기존 c155/o160 캠페인은 변경하지 않았다.

## 설정 작성

`configs/validation/c155-o160-v1.example.json`은 실제 현재 소스를 참조하는 예제다.
지금 실행 중인 검증을 대체하거나 다시 실행하라는 의미가 아니다.
새 실험에서는 이 파일을 새 이름으로 복사해 다음 항목을 편집한다.

- `models`: 이름 → 소스 경로와 정확한 SHA-256. 관측 전용 후보를 실수로 넣지 않는다.
- `opponents`: 이름 → 경로, SHA-256, 실제 구현 계열 `family`.
  동일 소스 중복 상대는 거부하며, 관련 변형은 같은 family로 명시한다.
- `comparisons`: candidate, parent, primary. 주 비교와 설명용 비교를 사전에 정한다.
- `stages`: screen/confirm/final별 서로 겹치지 않는 정수 시드와 alpha.
  버전 변경 후 본 시드로 튜닝했다면 해당 시드는 최종 검증에 사용할 수 없다.
- `engine`: 정확한 기존 엔진/Python identity. 버전 번호만 맞춰 해시를 생략하지 않는다.
- `workers`: 1..8, `timeout_seconds`: 경기 벽시계 제한.
- `configuration`: v1은 기본 720턴 환경으로 한정한다.

경기 수 = 모델 수 × 상대 수 × 해당 단계 시드 수 × 2좌석.
시드가 같은 반복 경기 수를 독립 표본 수로 세지 않는다. 각 단계 표본 수는 실행 전에
정하고 유의해지는 시점에 임의로 중단하지 않는다.

새 설정 내부의 시드 겹침은 자동 검사한다. 모든 과거 실험과의 미사용 여부나 상대의
진짜 독립 계보는 자동 증명하지 못하므로 설계 검토에서 확인한다.

## 명령

프로젝트 루트 PowerShell에서 아래 변수에 새 실험 파일/출력 경로를 지정한다.

```powershell
$validationConfig = 'H:\dev\kaggle-data\kaggriculture-strategy-meta\configs\validation\c155-o160-v1.example.json'
$validationOutput = 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\my_new_screen_v1'
& .\tools\run-validation.ps1 -Config $validationConfig -Out $validationOutput -Stage screen -Action Prepare
```

Prepare는 소스·엔진·러너·대진을 고정하며 게임을 실행하지 않는다. Check는 같은 계약을
재확인한다. 사용자에게 실행 명령을 전달할 때만 `-Action Run`을 쓴다.

```powershell
& .\tools\run-validation.ps1 -Config $validationConfig -Out $validationOutput -Stage screen -Action Run
```

같은 명령으로 재개한다. 해시와 건강성 검사를 통과한 결과만 캐시로 인정한다.
불완전/오류 결과를 성공으로 처리하거나 몰래 덮어쓰지 않는다. 실패 로그를 검토한 뒤
별도 실험을 준비하거나 결과 보존을 포함한 복구를 설계한다.

게임을 다시 실행하지 않고 완료 결과만 집계하려면 `-Action Analyze`를 쓴다.
Confirm과 Final은 각각 `-Stage confirm/final`과 새로운 Out을 지정하고 설계 검토 후
명시적으로 실행한다. 앞 단계가 끝났다고 다음 단계를 자동 실행하지 않는다.

## 실행 계약

- 단일 coordinator, 최대 8개의 fresh subprocess. 경기마다 job/log/result/TEMP 분리.
- 전역 launch 파일의 OS 배타 잠금 + 실제 Python 프로세스 검사로 중첩 실행 차단.
  예전 러너는 공통 잠금을 사용하지 않을 수 있으므로 예전 캠페인과 동시 시작하지 않는다.
- 소스는 출력 내 `sources/<sha>.py` 스냅샷을 실행한다. 원본 후보가 나중에 바뀌어도
  실행 중인 고정 후보는 바뀌지 않는다.
- worker마다 manifest/job/engine/source/support를 다시 확인한다.
- 시간 제한·실패 시 coordinator가 소유한 worker tree만 종료한다.
  강제 터미널 종료·OS 장애 후에는 다음 실행의 실제 프로세스 검사로 잔여 실행을 탐지한다.
- 진행률, 완료/전체, %, 캐시, 실패, 시간, 처리율, ETA, 성공/실패 알림음 제공.
- 건강한 720상태·719콜·양측 DONE만 분석한다. 성공 알림은 실행 성공을 뜻한다.

## 통계와 승격

승패와 마진, 하위 10% 마진, 상대/계열/좌석별 결과, 부모 대비 승점·현금 변화,
승→패·무→패, 행동 해시 변화와 숫자 telemetry를 공통 출력한다.
telemetry의 요청 수량은 실제 생산·판매로 해석하지 않는다.

주 통계는 시드별로 양 좌석과 상대를 묶고, 상대 계열별 동일 가중치를 적용한 승점 차이다.
bootstrap은 시드 묶음을 재표집한다. 단계 alpha / 주 비교 수로 Bonferroni 보정하며
예제의 screen/confirm/final alpha 합은 .05다. 관측 차이가 일정하면 과도한 확신을
피하기 위해 신뢰구간은 null, 판정은 inconclusive로 남긴다.

구간은 근사치이며 특히 작거나 희소한 표본에서 명목 유의수준을 정확히 보장하지 않는다.
후보를 반복 선택·수정하는 전체 연구의 다중검정 문제까지 이 보정으로 해결되는 것도 아니다.
설명용 비교와 하위 그룹은 유의성 판정에 사용하지 않는다.

positive 신호가 있어도 건강성·하위그룹·손실 꼬리·미사용 최종 조건의 검토가 필요하다.
모든 단계에서 `promotion=false`이며 Kaggle 제출은 이 도구에 없다.

## 유지 관리

고정 실험이 사용하는 v1/support 파일은 변경하지 않는다. 공통 실행 의미를 바꾸는 수정은
v2와 새 실험 계약으로 만든다. 해시 검사를 우회해 과거 결과와 섞지 않는다.
기전별 새 진단은 별도 도구로 추가하고 공통 승패 러너를 매번 복사하지 않는다.

검사: `python -m unittest discover -s tests -p test_validation_v1.py -v`.
합성 결과·가짜 프로세스로 검증하므로 실제 게임을 실행하지 않는다.
