# Public League 현행 quarantine 전수 재감사 (2026-09-21)

## 범위와 판정 기준

- 재감사 시작 시점의 최신 notebook version quarantine 9개와 runtime agent quarantine 8개를 검사했다.
- notebook cell 전체를 실행하지 않았다. 현재 추출기가 정적으로 복원한 exact artifact만 컴파일, 공식 loader, 공식 native 첫 행동 QA로 검사했다.
- 과거 무효 경기와 불완전 artifact는 삭제하지 않았다. 완전한 후속 artifact가 확인된 과거 신원은 `superseded/archived`로 남겼다.
- 재감사 전 DB: `state/public_league/league-pre-quarantine-reaudit-20260921-163826.sqlite3`
- Linux 실행 판별 수정 전 DB: `state/public_league/league-pre-sigalrm-reaudit-20260921-164344.sqlite3`

## 결과

최신판 9개 가운데 8개를 정상 agent 또는 exact duplicate alias로 복구했다. 현재 최신판 quarantine은 1개뿐이며, agent 테이블의 runtime quarantine은 0개다.

복구된 고유 agent:

- [Kaggriculture: Herd-Safe Sale Window | LB 2700](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-herd-safe-sale-window-lb-2700): agent196, 7파일 bundle, QA pass.
- [Kaggriculture: Two Coins, One Sheep | LB 2600](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-two-coins-one-sheep-lb-2600): agent199, 7파일 bundle, QA pass.
- [Kaggriculture: 7-Turn Rescue | Historical LB 2800+](https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-7-turn-rescue-historical-lb-2800): agent198, 9파일 bundle, QA pass.
- [God's mode. Hacked stores.](https://www.kaggle.com/code/crystalbaby/god-s-mode-hacked-stores): agent197, 4파일 bundle, QA pass.
- [TokenJunkieLabs Farm Manager](https://www.kaggle.com/code/tokenjunkielabs/tokenjunkielabs-farm-manager): agent200, 101파일 bundle, Linux QA pass, 완전한 720-step 양 좌석 2/2 valid.

복구된 exact duplicate 또는 기존 agent alias:

- [leoprovorov / God's mode. Hacked stores.](https://www.kaggle.com/code/leoprovorov/god-s-mode-hacked-stores): agent197과 exact artifact.
- [A Song of Ice and Fire | Fixed vs Flexible](https://www.kaggle.com/code/leoprovorov/a-song-of-ice-and-fire-fixed-vs-flexible): agent198과 exact artifact.
- [Kaggriculture: Breaking the Tie](https://www.kaggle.com/code/andrewsokolovsky/kaggriculture-breaking-the-tie): 공개 notebook Output의 `main.py`를 복원해 기존 agent123 alias로 편입.

## 남은 실제 quarantine

- [Kaggriculture Baseline](https://www.kaggle.com/code/pavloivanin/kaggriculture-baseline): 최고 공개 점수 996.7. 복원된 `submission.py`는 `CropCycleAgent`, `MockFarmEnvironment`와 `__main__` 데모만 포함하며 Kaggriculture 제출 entrypoint가 없다. 공식 loader가 마지막 callable class를 선택해도 첫 행동이 `None`이다. 수집 실패가 아니라 실행 가능한 제출 agent가 없는 소스이므로 quarantine을 유지한다.

과거 version quarantine 3개도 DB에 남아 있다. 모두 현재판이 아니며, 당시 bundle에서 `base_agent`나 부속파일이 빠져 실패한 immutable version이다. 같은 notebook의 최신판은 이번 재감사에서 agent197/198로 복구됐다.

## 거짓 격리 원인과 수정

TokenJunkie artifact의 첫 행동이 Windows host에서 `None`으로 보인 실제 원인은 `reference/titan-current/deadline_adapter.py`의 `signal.SIGALRM` 접근이었다. Windows Python에는 `SIGALRM`이 없지만 Kaggle Linux에는 있다. 기존 수집기는 `.so/.dylib`가 있을 때만 Docker Linux를 선택해 순수 Python POSIX-signal bundle을 잘못 격리했다.

`public_league.py`에 Python AST 기반 판별을 추가했다. `signal.SIGALRM`, `alarm`, `setitimer`, POSIX interval timer 상수를 실제 import/attribute로 사용하는 bundle만 Linux로 보내고 일반 Python bundle은 host 경로를 유지한다. 문자열 검색만으로 플랫폼을 바꾸지 않는다.

재감사 과정에서 `superseded` agent의 보존된 과거 무효 경기가 모든 league batch 종료 때 다시 runtime quarantine을 만드는 결함도 발견했다. 자동 runtime 격리는 현재 `qa_status='pass'`인 agent에만 적용하도록 고치고 회귀 테스트를 추가했다.

## 과거 runtime quarantine 정리

아래 8개는 구형 추출기가 `main.py`만 저장하거나 builder callable을 agent로 고른 불완전 historical identity다. 각각 완전한 후속 artifact가 공식 QA를 통과했고 32~470개의 유효 경기까지 보유한다.

- agent13 → agent137 (`agent.so` 포함 완전본)
- agent21 → agent118 (올바른 정책 entrypoint)
- agent54 → agent138 (`agent.so` 포함 완전본)
- agent63 → agent139 (`agent.so` 포함 완전본)
- agent67 → agent134 (`actions.json` 포함 완전본)
- agent75 → agent132 (`actions.json` 포함 완전본)
- agent88 → agent135 (`router_base.py` 등 sidecar 포함 완전본)
- agent128 → agent140 (`agent.so` 포함 완전본)

구형 신원은 `qa_status='superseded'`, `status='archived'`로 바꾸고 대체 agent ID를 `qa_error`에 기록했다. 소스, 별칭, 무효 경기 기록은 보존했다.

## 검증

- `tests.test_public_league`: 71/71 PASS.
- 변경 Python `py_compile`: PASS.
- TokenJunkie: Linux 첫 행동 QA pass, 공식 720-step 양 좌석 2/2 complete, invalid 0.
- SQLite `PRAGMA integrity_check`: `ok`.
- 수정된 서비스의 첫 연속대결 batch: 8 workers, 240/240 complete, invalid 0, batch 종료 후 runtime quarantine 0. 구형 8개 신원도 모두 `superseded/archived`를 유지했다.
- 최종 현행 상태: latest `quarantine` 1, latest `no_source` 24, runtime agent quarantine 0.
