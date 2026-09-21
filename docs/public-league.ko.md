# Public Notebook League

공개 Kaggriculture 노트북을 Codex 없이 주기적으로 수집하고, 실제 agent 소스를 로컬 native reacting 경기로 비교하는 서비스다.

현행 계약은 `configs/public_league_v2.json`이다. `configs/public_league_v1.json`과 원시 경기 기록은 보존한다. v1의 정상 완료 단일파일 경기는 같은 공식 엔진의 관측값으로 BT 적합에 유지하지만, v2 match key는 별도라 캐시로 재사용하지 않는다. 부속파일 누락·외부 wall timeout 때문에 무효였던 행은 승패에 넣지 않는다.

## 동작

자동 수집 또는 **지금 수집** 한 번이 다음 단계를 순서대로 수행한다.

1. Kaggle Code 목록을 `scoreDescending`, `dateRun` 두 기준으로 수집한다.
   대회 연결 목록만으로는 검색 노트북이 빠질 수 있어 `kaggriculture` 검색 결과의 점수순·최신순도 합쳐 중복 제거한다.
2. 새 버전만 `kernels pull`로 받아 원본 디렉터리를 보존한다.
3. `main.py`와 함께 tar 멤버, 모든 `%%writefile`/`%%agentfile`, 독립 실행 가능한 direct-agent code cell, 정적으로 해제 가능한 gzip/base64 파일맵, 100 MiB 이하의 선언 dataset 부속파일을 복원한다. `/kaggle/working/...` writefile은 제출 archive-root 상대경로로 정규화한다. `main.py`가 없으면 독립 파싱되고 top-level 공식 entrypoint를 정의하는 writefile이 정확히 하나인 경우에만 그 파일을 `main.py`로 승격한다. Dataset 파일 목록은 Kaggle CLI의 CSV 앞 pagination 문구와 다음 페이지까지 읽고, 전체 크기를 확인한 뒤에만 내려받는다. 완료 표식이 없는 중단 다운로드는 완성본으로 간주하지 않는다. C++ source형은 고정 Docker 환경에서 `agent.so`를 빌드한다.
4. 단일 `main.py`는 기존 LF 정규화 source SHA를 유지한다. 다중 파일 제출은 정렬된 경로와 모든 런타임 파일 바이트로 artifact SHA를 계산한다. C++ 빌드 뒤 `.cpp/.hpp/.h/.inc`는 제출 런타임 신원에서 제외하고 `main.py + agent.so`로 식별한다. 미세 코드·asset 변경은 별도 agent다.
5. 컴파일과 Kaggle last-callable 로더에 더해 공식 native 관측으로 첫 행동을 실제 호출한 agent만 리그에 넣는다. Linux shared-library bundle은 엔진 1.32.7 Docker에서 실행한다.
6. 엔진·v2 규칙·설정·runner·두 artifact·시드·좌석이 같은 경기는 SQLite 캐시를 재사용한다. 모든 대결은 양 좌석이다.
7. 누적 경기 수가 적은 신규 후보를 우선 배정한다. 첫 배치 뒤 `archived`가 되어도 최대 32경기까지 catch-up 대진을 계속한다. 표본과 pair 수가 비슷하면 Bradley–Terry(BT) 점수가 가까운 상대를 우선한다. 유효 경기만 BT와 Wilson 승점률 구간에 반영한다.
8. 최소 경기 수를 채운 agent 중 상위 100개를 `active`로 유지한다. 나머지는 `archived`로 바꾸되 소스·노트북·전적은 삭제하지 않는다.

각 notebook version은 독립적으로 추출한다. 한 노트북의 압축 builder나 malformed artifact에서 추출 예외가 발생해도 그 버전만 오류로 보존하고 뒤의 신규 버전 처리를 계속한다. 압축 builder가 복원한 단일 `main.py`도 artifact dictionary로 정규화한 뒤 일반 QA와 동일하게 검사한다.

공개 노트북의 Kaggle 현재 점수와 최고 점수는 Kaggle의 연결 제출 정보에서 읽는다. 추천 수(`totalVotes`)와 구분하며 수집/스크린 우선순위에만 쓰고 로컬 BT에는 넣지 않는다. 대시보드는 로컬 BT, Kaggle 현재/최고 점수, 게시·갱신일을 각각 표시한다. 행동 fingerprint는 동일 artifact 판정에 쓰지 않는다.

## 명령

프로젝트 루트에서 실행한다.

```powershell
.venv\Scripts\python.exe tools\public_league.py init
.venv\Scripts\python.exe tools\public_league.py collect
.venv\Scripts\python.exe tools\public_league.py run --workers 8 --max-matches 240
.venv\Scripts\python.exe tools\public_league.py serve --port 8791
```

대시보드는 `http://127.0.0.1:8791`에서 본다. 화면의 공유 노트북 이름은 Kaggle 제목 그대로이며 제목을 누르면 원본 페이지가 열린다. 동일 agent 별칭도 전부 링크된다.

가장 간단한 실행법은 프로젝트 루트의 `public-league.html`을 더블클릭한 뒤 **리그 시작/열기**를 누르는 것이다. 서버가 이미 실행 중이면 바로 대시보드로 이동한다. 꺼져 있으면 Windows에 등록된 `kaggriculture-league://` 주소가 `public-league.vbs --no-browser`를 호출해 숨김 서버를 시작하고, HTML이 준비 상태를 확인한 뒤 대시보드로 이동한다. 브라우저가 처음 한 번 외부 앱 실행 여부를 물으면 허용한다.

`public-league.vbs`를 직접 더블클릭해도 된다. 이 경우 터미널 창 없이 서버를 시작하고 기본 브라우저에서 대시보드를 연다. 명령줄에서는 다음처럼 실행한다.

```powershell
wscript.exe .\public-league.vbs
```

HTML 실행 주소 등록이 사라졌다면 관리자 권한 없이 다음 명령으로 현재 사용자에게 다시 등록할 수 있다.

```powershell
powershell -ExecutionPolicy Bypass -File tools\register-public-league-protocol.ps1
```

마지막 대시보드 탭을 닫으면 `pagehide` 신호 뒤 5초의 새로고침 유예를 거쳐 서버와 연속 대결도 종료된다. 백그라운드 탭은 브라우저가 JavaScript 타이머를 1분 단위로 늦출 수 있으므로 heartbeat 만료는 3분이다. 예약 수집 작업은 별도이므로 계속 실행된다. 예약 작업도 `.venv/Scripts/pythonw.exe`를 사용하므로 주기 실행 중 콘솔 창이 나타나지 않는다.

대시보드 버튼은 역할이 분리되어 있다.

- **지금 수집**: Kaggle 목록·점수·새 버전·소스를 갱신하지만 경기를 시작하지 않는다.
- **대결 시작 / 대결 중지**: 하나의 토글 버튼이다. 시작하면 240경기 배치를 연속 실행하고, 각 배치가 끝날 때 BT를 다시 적합한 뒤 다음 배치를 자동으로 시작한다. 중지는 현재 실행 프로세스와 아직 시작하지 않은 작업을 정리하며, 부분 경기는 증거로 저장하지 않는다.
- **집중 측정**: 순위표의 한 agent만 중심으로 강한 active/challenger 상대를 덜 만난 순서로 편성한다. 입력값은 기존 누적 경기 수가 아니라 이번에 **추가할 유효 경기 수**다. 모든 seed를 양 좌석으로 실행하고 기존 match cache를 건너뛴다. 기본은 500경기이며 2~10,000의 짝수로 바꿀 수 있다. 240경기 내부 배치를 이어 실행해 목표에 도달하면 자동 종료하며 양 좌석 묶음 때문에 최대 1경기 초과할 수 있다. 같은 행의 **집중 중지** 또는 상단 대결 중지로 조기 종료한다. 다른 agent의 집중 버튼을 누르면 현재 배치를 정리한 뒤 대상을 바꾼다.
- **전적 보기**: 선택한 agent의 저장된 경기 기록을 최신순으로 보여 준다. 상대 제목·source 앞자리, 시드·좌석, 승패, 양쪽 최종 현금, 마진, 유효/무효와 오류를 확인할 수 있다.
- **노트북 검색·직접 추가**: 제목 검색 또는 Kaggle Code URL/`author/slug`를 입력한다. 같은 노트북 재수집, 같은 노트북의 동일 source, 다른 노트북의 exact-source 중복, 고유 source, 최신본에 agent source가 없고 이전 실행본만 있는 경우를 구분한다. **추가+집중**은 추출된 agent에 지정 경기 수의 집중 측정을 바로 시작한다.

**자동 수집·대결 설정**의 **자동 수집 ON/OFF** 버튼은 Windows의 `Kaggriculture Public League Collect` 예약 작업을 실제로 활성화하거나 비활성화한다. OFF여도 **지금 수집**은 사용할 수 있다. 수집 주기(0.25~168시간)와 대결 워커 수(1~12)를 바꿀 수 있으며, 저장하면 수집 전용 작업이 갱신된다. 워커 수는 연속 대결의 다음 배치부터 적용된다. 예약 작업은 대결을 시작하지 않으므로 **연속 대결 OFF** 뒤 자동으로 다시 시작되지 않는다.

**연속 대결 OFF · 시작 / ON · 중지** 버튼은 별도의 연속 대결 상태를 바꾼다. 시작하면 **사용자가 중지할 때까지 계속** 대결한다. 화면의 `현재 처리 묶음`은 종료 목표가 아니다. 내부적으로 `240경기`는 전 agent의 완전 상호 대전 수가 아니라 BT 재적합과 대진 재편성을 위한 계산량 상한이다. 스케줄러는 최대 100개 active/challenger 풀에서 한 모델 쌍을 선택하고 같은 seed를 양 좌석으로 실행하므로, 한 묶음은 최대 120쌍·240경기다. 신규 모델은 32경기까지 먼저 따라잡고 이후 일반 편성으로 내려간다. 중지하면 완료된 경기만 보존하고 대기·실행 중 경기는 제거한다. 모델별 Wilson 95% 구간도 함께 표시한다.

일반 매칭의 구체적인 우선순위는 다음과 같다.

1. QA-pass agent에서 현재 active 강자와 신규 candidate를 합쳐 최대 100개 풀을 만든다. 상위 100 자리를 모두 기존 강자로 채우지 않고 신규 challenger 자리를 10개 남긴다.
2. 누적 유효 경기 수가 가장 적은 모델을 먼저 고른다. 신규 또는 표본 부족 모델은 32경기까지 catch-up 우선권을 받는다.
3. 상대는 전체 유효 경기 수와 서로 맞붙은 수가 적은 순서로 고르고, 그 조건이 비슷하면 BT가 가까운 상대를 먼저 고른다. 따라잡기 중 세 번째 pair마다 더 경험 많은 강자를 anchor로 섞는다.
4. artifact 두 개·엔진·v2 계약·seed·좌석에서 결정되는 match key가 DB에 있으면 다음 결정적 seed로 넘어간다.
5. 같은 seed를 반드시 양 좌석으로 실행한다. 공식 엔진이 DONE으로 끝나고 행동 예외가 없는 경기만 BT와 W-L-T, Wilson 95% 구간에 넣는다.

기능을 켠 기준 시각 이후 수집되어 12시간이 지나지 않은 agent는 이름 옆에 **NEW**가 표시된다. 기능 도입 전에 이미 편입된 모델에는 붙이지 않는다. 새 노트북이 기존 agent와 exact source duplicate여도 새 alias가 발견된 시각을 기준으로 해당 agent에 NEW가 붙는다. 12시간이 지나면 자동으로 사라진다.

상단 상태도 실행 중에는 `대전 중 (완료/전체)`, 중지 요청 뒤에는 `대전 중지 중`, 실행 중인 배치가 없으면 `대기`로 표시한다. **현재 대전** 카드는 최신 실행 배치의 `완료+무효 / 전체`, 진행률, 남은 경기와 시작 시각을 표시하며 5초마다 갱신된다. 최근 경기와 수집 기록의 시각은 한국시간(KST)으로 표시한다. 무효 경기는 진행률에는 포함되지만 BT와 승패에는 포함되지 않는다.

상태 의미:

- `active`: 최소 8개 유효 경기를 마치고 현재 상위 100에 포함됨.
- `candidate`: 컴파일·공식 loader·첫 행동 QA는 통과했지만 아직 8경기 미만이거나 도전자 대기열에 있음.
- `archived`: 검증을 마쳤으나 현재 상위 100 밖임. 파일과 전적은 보존됨.
- `quarantine`: 컴파일/loader/첫 행동 QA 실패나 agent에 귀속되는 코드 예외가 반복되어 순위에서 격리됨. 공식 엔진이 DONE 처리한 경기의 로컬 1초 경고나 자체 telemetry 이름만으로는 격리하지 않는다.
- `no_source`: 분석용 노트북 등에서 지원하는 형태의 실행 가능한 agent를 찾지 못한 버전. agent 순위표에는 나타나지 않음. `FILES['main.py']`에 base85+zlib로 넣은 공개 artifact builder는 AST의 literal payload와 고정 SHA를 읽어 공개 코드를 실행하지 않고 추출한다.

`수집됨·대전 불가` 탭은 최신 버전 파일까지 받았지만 실행 가능한 agent를 찾지 못했거나 추출/QA에 실패한 노트북을 보여준다. Kaggle 목록에서 사라진 것이 아니라 대전할 실행 소스가 없어서 랭킹에서 제외된 경우를 여기서 구분한다.

이미 받아 둔 공개 노트북은 다운로드 없이 가져올 수 있다.

```powershell
.venv\Scripts\python.exe tools\public_league.py import-existing state\o_dev\public_pull state\o_dev\public_pull_2 state\c300\public_research_20260919
.venv\Scripts\python.exe tools\public_league.py extract
```

Windows 자동 실행 설치/삭제:

```powershell
powershell -ExecutionPolicy Bypass -File tools\install-public-league-tasks.ps1 -EveryMinutes 180 -Workers 8
powershell -ExecutionPolicy Bypass -File tools\remove-public-league-tasks.ps1
```

작업 스케줄러는 수집 중복 실행을 막는다. 한 번의 수집이 끝나지 않았으면 다음 주기를 겹쳐 실행하지 않는다. 배터리 사용 중에도 실행하며, 절전 중 놓친 실행은 깨어난 뒤 따라잡도록 설정되어 있다. 리그도 별도 프로세스 잠금으로 중복 대결을 막는다. 기본 상태는 `state/public_league/league.sqlite3`, 원본은 `state/public_league/notebooks/`, 단일 파일 agent는 `state/public_league/sources/`, 다중 파일 artifact는 `state/public_league/artifacts/`에 보존된다.

우리 제출물 비교 기준은 `configs/public_league_local_agents.json`에 둔다. 현재 c129, o219, o227, o238, o239_50, o240, g000, g001, c358, c365의 고유 소스를 포함한다. 제출된 로컬 agent는 submission URL도 함께 기록한다. `c312_public_v9_4`처럼 공개 노트북 agent와 전체 소스 SHA-256이 같은 파일은 별도 참가자로 추가하지 않고 공개 alias 그룹 하나로만 평가한다. 한 줄이라도 실제 코드가 달라 SHA가 바뀐 미세 조정본은 별도 agent로 남긴다.

## 실패 처리

- Kaggle 수집 실패는 기존 DB와 순위를 바꾸지 않고 event로 기록한다.
- 소스가 없으면 `no_source`, 컴파일/loader 실패는 `quarantine`으로 표시한다.
- 공식 status/행동 예외/720-step 계약 실패 경기는 `invalid`이며 승리로 계산하지 않는다. 외부 wall cap은 공식 `runTimeout=1200`보다 긴 1220초다.
- 공식 DONE·719회 호출·행동 예외 0이면 로컬 `over_one_second`와 이름에 `error`가 들어간 자체 telemetry는 경고로만 남긴다. 공식 환경의 행동당 1초와 누적 overage 60초 판정은 엔진 status가 담당한다.
- 외부 전체 경기 timeout은 어느 좌석이 원인인지 알 수 없어 자동 격리 근거로 쓰지 않는다. 행동 예외·잘못된 반환처럼 agent에 직접 귀속되는 코드 오류가 2경기에서 반복되면 격리한다.
- 대결 중지는 Windows 워커 프로세스 트리 전체를 종료하고, Linux artifact 경기의 결정적 이름 Docker container도 강제 제거한 뒤 예약된 `running` 행을 정리한다.
- 노트북이 갱신되면 새 version 행과 새 소스를 추가하고 과거 버전은 덮어쓰지 않는다.
- 자동 Kaggle 제출은 이 서비스 범위에 포함하지 않는다. 제출 후보는 충분한 로컬 증거와 exact source readback을 별도 승격 단계에서 처리한다.
