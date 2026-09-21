# HANDOFF — 단일 작업 원장 / START HERE

갱신: 2026-09-21 16:33 KST. **Codex·Claude·다른 세션 모두 이 파일 한 곳에 현재 상태와 작업 기록을 남긴다.** 분리 원장은 보관 구간으로 통합됐으며 재생성하지 않는다.

## START HERE — Public Notebook League 전환 (2026-09-20 12:32 KST)

- **[2026-09-21 16:33 Codex / `no_source` 전수 재감사·수집 복구]** 현행 85개 `no_source`를 notebook source, 선언 dataset, 정적 압축/literal, pinned remote, 공개 notebook Output까지 다시 검사했다. zlib/gzip/lzma+base85/a85/base64, 분할 literal/join, raw map/tar/nested payload, dataset backfill, C++ 재빌드, Fieldbook/V23 명시 조립, 고정 GitHub release, 단독 `submission.py`, `*_agent` direct cell을 지원하고 QA를 공식 `env.run` 첫 행동으로 교정했다. 특히 `kernels pull`에 없는 saved notebook Output의 제출 파일과 런타임 sidecar를 제한 다운로드하는 경로를 추가했으며 Windows Kaggle CLI UTF-8/모든 Docker·CLI 무창 실행을 적용했다. V14/Adaptive Guard/Yummers/A Wonderful Life/Story of Seasons/Six-Day Fieldbook 등과 No Cow/FlyFarmer/Sovereign/Building AI/V66/Getting Started/P&L baseline을 복구해 **현재 `no_source` 24개**가 남았다. 이 중 23개는 분석·dataset·simulator notebook이라 제출 artifact가 없음을 source+Output으로 확인했고, MetaCounter R1만 Output API 403이라 external Output 유무가 미확정이다. Pavlo baseline은 source를 찾았으나 첫 행동 `None`으로 quarantine. 68 tests·py_compile PASS, DB integrity ok. 상세 [최종 링크·사유](reports/public-league-current-no-source-2026-09-21.ko.md). 백업 `league-pre-full-nosource-reaudit-*`, `league-pre-published-output-recovery-*`, `league-pre-output-identity-fix-*`.
- **[2026-09-21 15:38 Codex / 과거 미편입 agent 복구·실측]** 기존 추출기가 `%%writefile /kaggle/working/main.py`, 단독 `submission.py`/임의 파일명 agent, `%%agentfile`, 독립 code-cell `def agent`를 제출 artifact로 보지 못해 실행 코드가 있는 노트북을 `no_source`로 남긴 결함을 수정했다. Kaggle working 절대경로는 archive-root 상대경로로만 정규화하고, `main.py`가 없을 때는 독립 파싱되고 top-level 공식 entrypoint를 가진 writefile이 정확히 하나일 때만 `main.py`로 승격한다. 독립 direct-agent cell도 일반 compile/공식 loader/첫 행동 QA를 그대로 거친다. 57 tests와 py_compile PASS. 재감사 15 versions에서 고유 agent 143–145 세 개와 exact alias 두 개(agent4 public v9/4, agent38 V47)를 복구했고, 나머지 10개는 공식 첫 행동의 2-인자 호출에서 실제 TypeError라 격리 유지했다. 앞선 builder 복구의 신규 141/142와 이번 143–145를 각각 최소 128 집중 유효 경기로 측정(전체 invalid 0): 141 `Farmer John and the Idle Seller` 128-32, BT2112, 26/133; 142 `More Wheat, Smarter Sales` 140-18-2, BT2420, 8/133; 143 `Precomputed Schedule Policy` 11-117, BT919, archived; 144 `notebook6cc8bf1c92` 74-56, BT1442, active; 145 `Kaggriculture Starter` 0-132, BT689, archived. exact duplicate는 기존 agent 전적을 공유하므로 별도 대전을 만들지 않았다. DB 백업 `league-pre-direct-cell-*`, `league-pre-writefile-reextract-*`; active 100·workers 8·자동수집 3시간 계약 유지.
- **[2026-09-21 15:18 Codex / 미편입 agent 복구 + active 100]** 14:47 수집된 `guruprasaathas111/kaggriculture-top-2-master-engine-v4`와 `haideptry/the-2965-master-hybrid-engine`이 화면에서 agent 없음으로 보인 원인은 소스 부재가 아니었다. 앞선 압축 builder fallback이 `(origin, bytes)`를 반환했는데 artifact 정렬기는 `(origin, files dict)`를 기대해 `bytes.values()` AttributeError로 extract 전체가 중단됐고 뒤 7 versions가 `pulled`에 남았다. fallback을 단일 `main.py` artifact dict로 정규화하고 version별 예외 격리를 추가했다(회귀 테스트 포함, 53 tests PASS). 대기 7개 재처리 결과 new agent 2, duplicate alias 4, 실제 QA 실패 1. 두 문의 노트북은 각각 기존 agent55 exact V48 SHA `4b540288...`와 agent113 SHA `949e2eed...`의 동일 artifact라 새 행 대신 별칭으로 정상 편입됐다. 이어 과거 alias 없는 no_source/quarantine 136 versions를 최신 추출기로 전수 재감사해 artifact 복원 가능 14개를 재심사했다. 3개(`best-agent-ranking`, `Kaggriculture V8`, `Beyond V43`)는 기존 agent55/73 exact alias로 편입, 나머지 11개는 missing `base_agent`, FileNotFoundError, incomplete template 또는 syntax error로 loader/첫 행동 QA 실패를 재확인해 격리 유지했다. 재감사 전 DB 백업 `state/public_league/league-pre-reextract-<timestamp>.sqlite3`. owner 요청으로 v2 active 정원과 기본 scheduler pool을 **50→100**으로 확대했고 challenger slots 10·cycle 240·workers 8은 유지했다.
- **[2026-09-21 14:45 Codex / GitHub 작업물 스냅샷]** 현재까지의 후보·설정·도구·테스트·문서·보고서와 Public League v2 구현을 Git에 포함했다. 로컬 runtime/state, notebook 원본, replay, 결과 캐시, SQLite, 임시 파일과 제출용 tar는 재생성 가능하거나 대용량이므로 `.gitignore`에 명시해 제외했다. 업로드 묶음은 292개·약 19.9 MiB이며 개별 5 MiB 초과 파일과 credential 패턴은 없었다. 변경 Python 전부 `py_compile`, Public League 51 tests, research_ops 4 tests PASS. `agent/overlays/r001_leader_rules.py`는 기존 `%()` 생성 템플릿이라 전체 `compileall` 대상에서는 SyntaxError가 나지만 이번 변경 파일이 아니다.
- **[2026-09-21 12:49 Codex / Public League v2 공식환경 보완 완료]** 09:54 공식 일치 감사에서 확인한 실행환경·평가 차이를 기존 v1 보존 상태에서 `configs/public_league_v2.json` / `RULES_VERSION=public_league_v2`로 보완했다. 수집기는 tar 전체 멤버·여러 `%%writefile`·literal gzip/base64 JSON map·dataset 부속 파일을 artifact로 보존하고, 첫 실제 행동 QA로 builder helper 오선택을 막는다. Linux `agent.so`는 Docker engine 1.32.7에서 `main.py+agent.so`로 실행·식별한다(C++ 빌드 소스는 provenance만 보존). 잘못된 과거 source-only 신원 130/131/133/136은 `superseded/archived`로 보존하되 화면에서 숨겼고, 교정된 137/138/139/140은 각각 `linux · 2파일`로 편입했다. 공식 DONE/DONE·720 states·719 calls·예외0이면 로컬 timing 경고는 유효, 외부 1220초 wall timeout은 자동 격리 근거에서 제외한다. 순위는 정규화 Bradley–Terry, 매칭은 표본 부족 우선 후 BT 근접 상대다. 대형 dataset CSV 앞의 pagination 문구를 header로 오인해 size=0 처리하던 결함도 수정해 실제 header부터 pagination하고 100MiB 이하·완료 marker 있는 다운로드만 사용한다. v2 실제 24경기 complete/0 invalid(누적 complete 14,906, invalid 320), Linux 네 모델 각 6 valid, DB integrity `ok`; 마지막 필터·중지 보완 뒤 `py_compile`과 51 tests PASS. 서버 재시작 중 Windows venv launcher만 죽여 Docker/실제 Python 자식이 남는 결함을 추가 발견해 `/T` 프로세스 트리 종료 + 결정적 Docker container 이름/강제 제거로 수정했고, API 중지 실증에서 worker0/container0/running row0을 확인했다. 현재 화면은 BT·artifact 파일 수를 표시하고 130/131/133/136을 숨기며, **자동 수집 ON·3시간 / 연속 대결 ON·8 workers**다. 최신 240경기 묶음은 실행 중이며 blind 7240–7255는 미사용. 백업은 `state/public_league/league-pre-v2-20260921.sqlite3`, `league-pre-runtime-identity-fix-20260921.sqlite3`.
- **[2026-09-21 09:54 Codex / Public League 공식 일치 읽기 전용 감사]** 사용자 요청으로 코드·설정 변경/새 시뮬/서비스 조작 없이 감사했다. 공식 최신 source와 로컬 game py/json 동일, 최근 실전 episode111420532도 engine1.32.7/게임 설정 동일. complete11,171건 seed·좌석·현금·승패·720states/719calls·오류 기록 내부일관성 불일치0. **중요 정정:** quarantine9개 중7개는 원본에 포함된 agent.so/actions.json/helper/model을 로컬이 main.py만 추출해 누락한 실행환경 문제이고, agent21은 builder를 정책으로 잘못 선택(QA entrypoint=Path), agent82는 로컬 전체90초 제한이다. 이전 “원본 코드불량” 해석은 철회하며 Kaggle 실행 불가로 단정하지 않는다. 공식은 행동1초+누적초과여유60초/runTimeout1200이고 로컬의 별도1.5초/전체90초는 다르다. 로컬 경기수 균형 매칭·12회 batch Elo도 공식 유사실력 매칭·최종 Bradley–Terry와 다르다. 기존 빠른 단일파일 모델 경기 결과를 폐기할 근거는 없으나 전체 공개풀 포괄성/실전 실행 적합성 한계가 확인됐다. 코드수정은 미실행, 기존 연속대결 유지. 상세 [감사 보고서](reports/public-league-live-parity-audit-2026-09-21.ko.md). 현재 PUBLIC 완료: c358 69W/23L·2741.7, c365 16W/1L·1503.1(초기17경기/낮은 상대층이므로 점수 직접비교 금지).
- **[2026-09-21 09:28 Codex / Public League 기능·격리 재감사]** 검색/직접 추가, agent별 전적, 지정 횟수 집중 측정(기본 추가 유효 500), 진행 상태와 폭 축소 UI를 구현하고 37 tests PASS. `Soil Remembers Rain`·`Moon Counts Melons` 최신본은 source가 없고 과거 실행 가능 버전이 exact SHA `02b1fee4...`로 같았다. agent15 집중 측정은 기존 91경기에 501 valid를 추가해 592경기 118-474, Elo1243, archived로 종료했다(양 좌석 묶음으로 +1). 시간 격리는 1.0초/2회에서 **1.5초 초과·4회·서로 다른 상대 2개 이상**으로 완화하고 1.5초 이하 invalid 13경기를 복구했다. 코드 예외는 2회 유지. 현재 runtime quarantine 11개를 재감사해 timing-only agent 33(1.007~1.073s), 116(1.004~1.015s), 86(3.79~3.85s 2회·한 상대)를 복구했고, 외부파일/타입 오류 7개와 90초 timeout 1개는 유지했다. c365 제출 `56407947` COMPLETE·초기 1156.7, c358 local 2위권·620+게임. 자동 수집 3시간/8워커 유지.
- **[2026-09-21 09:32 Codex / Public League 운영 재개]** 페이지를 명시적으로 새로고침해 UI의 격리 설명이 `1.5초 초과·여러 상대·4회`로 바뀐 것을 확인했다. 상태는 active 50/candidate 2/archived 69/quarantine 8, 자동 수집 ON·3시간·8워커다. 겹치는 수집/대결이 없는 상태에서 연속 대결을 재개했고 새 cycle 240경기가 `running`으로 생성됐다. `unittest tests.test_public_league` 37/37 PASS와 `py_compile` PASS를 다시 확인했다.
- **[2026-09-21 09:36 Codex / 새 코드 오류 자동 격리 확인]** 재개 첫 cycle은 207 valid/33 invalid로 끝났고 runtime quarantine 1건을 만들었다. invalid 32건은 새 후보 `Kaggriculture`(agent128, SHA `8059ac1d...`)가 step0에서 외부 `agent.so`를 찾지 못한 실제 코드/의존성 오류였으며, cycle 종료 즉시 `runtime_failed/quarantine`으로 전환됐다. 나머지 1건은 복구된 agent86의 1.5초 초과 1회로 4회·2상대 기준 미달이라 격리되지 않았다. 다음 240경기 cycle은 agent128을 제외하고 8워커로 자동 시작됐으며 초기 invalid 0이다. 현재 quarantine은 9개다.
- **[2026-09-21 08:42 Codex / 현재 상태]** c365(`agent/c365_feed_reserve.py`, SHA `d48e66c3...`)를 사용자 명시 지시로 Kaggle submission `56407947`에 live validation 제출했다. 접수 당시 `PENDING`; 사전 통계 gate 하한0 FAIL은 그대로 보존하며 제출을 gate 통과로 재해석하지 않는다. 직접 제출용 단일 `main.py` 패키지는 `state/c365/c365_feed_reserve_submission.tar.gz`(SHA `752d5d1b...`, 내부 SHA=후보)다. 이전 제출 c358은 `56402500`, 현재 표시 2743.4다. Public League c358 agent 114가 복구 뒤 다시 quarantine됐지만, 이전 watermark 6674 이후 c358 관련 경기는 128 complete/0 invalid였고 유일한 새 invalid는 c358과 무관한 agent116 Local Best 1.015초였다. 따라서 거짓 재격리로 판정해 watermark 6888로 다시 복구했다. 앞으로 모든 동결 제출 후보는 단일 `main.py` tar.gz를 함께 만들고 절대 경로·원본/멤버/archive SHA를 보고한다. 설정은 **3시간 자동 수집 ON / 8 workers**이며 제출 작업 뒤 연속 대결을 재개한다. 보호 blind 7240–7255는 미사용이다.
- **[2026-09-21 07:12 Codex / c359–c364]** c359는 임시 밀을 하루 더 성숙시켜 승점 +1.5625%p, own +21, margin +22였지만 CI가 0을 포함해 종료했다. c360은 c358/Metav4 시작 정책 라우터가 shop 관측 전 step0에서 갈려 구현 불가 판정했다. c361(V54 본체+Local Best 전체 market stack)은 screen +25%p/margin +451 뒤 fresh confirm +1.56%p/margin -101/own -342/W→L20으로 기각했다. c362(V54+generic sell-impact reorder)는 +3.91%p/margin -16/own -42/W→L4로 기각했다. c363의 첫 분기 시각은 6/8세계에서 step207로 같아 분류력이 부족하고 과적합 위험이 커 구현하지 않았다. 새 공개 Local Best `89a50e92...`는 이전 `41dd60f7...`에 `WHEAT>FERTILIZER` 순서 규칙 하나만 추가한 exact chain이다. 이를 c358 개막과 결합한 c364(`ae1485b9...`)는 off/활성 QA를 통과했으나 fresh 8-worker 256게임에서 c358과 93W/35L로 같고 승점0, own +1.625, margin +3.016, flip0이라 폐기했다. SELL 순서 변형은 더 튜닝하지 않는다.
- **[2026-09-21 07:51 Codex / c365 완료]** `crop_lane_trace.py`로 후기 당근 부족을 CARROT2의 2일 사료 예비 차단으로 좁혔다. c365는 개발 두 세계에서 차단 감소·당근 +16u/밀 −20u·사료비0·일말 미급식0을 확인했다. 정식 screen/confirm/final은 모두 8워커, 1,024/1,024 valid, 최대 후보0.835초였다. 단계별 승점 +1.56/+10.16/+3.125%p, own +177/+61/+182, margin +90/+851/+143, W→L0. 효과가 드문 seed에 집중되어 pooled 99% 하한0이라 보류한다. 첫 screen은 c358 한 결정1.124초로 전략 판정 전 중단·보존했고 동일 계약 v1b는 최대0.803초로 완주했다. | c365 제출 없음, c358 유지, blind 미사용 | Public League 신규 우선 대진으로 추가 증거를 모은다.
- **[2026-09-21 / c357 보관 전제]** 당시 새 개발 부모 후보는 V54 exact `949e2eed...`였다. 이것은 Metav4 v13 `9d634946...`에 d0–d2 유휴 일손으로 미래 pasture 자리 `(2,4)`에 임시 밀을 심고 수확·복원·판매하는 `HybridOpening`을 추가한 정책이다. Pipe16 `827ddf29...`도 사실상 같은 실행 정책이므로 독립 강도 증거로 중복 계산하지 않았다. 가장 가까운 선행 c324는 새 공개 ed89be8c 전체정책이 v9 대비 승점 CI에 0을 포함하고 마진도 음수여서 종료됐다. 이 항목은 c358 완료 전 계획 기록이며 현재 지시가 아니다.
- **[2026-09-21 02:34 Codex / c357–c358 완료·제출]** c357은 V54가 Metav4 v13보다 승점 +7.81%p, 마진 +56.15, own +39.24, W→L 0, 99% seed CI `[+6.25,+12.5]%p`임을 256 fresh native games에서 확인했다. Local Best `41dd60f7...`의 중첩 base85+lzma payload를 AST literal로 해제해 실제 계층을 감사하고, 그 시장 스택과 V54의 한 타일 Productive Idle opening을 결합한 `agent/c358_localbest_hybrid.py`(SHA `680a4f71...`)를 만들었다. off wrapper는 원본과 4/4 행동·현금 동일, 활성 opening은 전 경기 2u 수확/복원/판매, 오류 0. 12-worker 첫 screen은 CPU 경합 1.0106초 1회로 중단·보존하고 동일 계약을 8-worker v1b로 재실행했다. screen/confirm/final 총 960/960 valid, health0, 후보 최대0.965초; 1-worker 감사 최대0.581초. 부모 대비 단계별 family-weighted 승점 +8.33/+6.25/+3.47%p, 마진 +53.8/+76.9/+18.9, W→L 0/0/2. final CI 하한0으로 사전 무회귀 증분 gate는 FAIL이지만 pooled 후보 절대전적 406-74이고 V54/Pipe16/Metav4 각각34-14, LocalBest/g001 각각46-2다. 사용자 요청의 공개-frontier 직접 우위를 충족해 제출 ID `56402500`으로 제출했다. `SubmissionStatus.COMPLETE`, 최초표시600.0(대진전 초기값). 산출물 SHA `b283e8d3...`, tar 내부 main SHA=후보. 제출 설명의 pooled `419W`는 합산 오기이며 실제 `406W-74L`; 중복 제출하지 않는다. c358은 local league candidate/0경기로 편입했다. 정적 갱신 의도로 legacy `refresh`를 호출해 league batch도 시작되는 것을 발견하고 즉시 중단했으며 worker 없음/연속 토글 off를 확인했다. 상세 [보고서](reports/c358-localbest-hybrid-2026-09-21.ko.md). blind 7240–7255 미사용. 자동 수집은 유지.

- 사용자가 c300+ 단일 가설 개발을 중단하고, 최신 Kaggle 공개 노트북을 자동 수집해 로컬 리그로 계속 선별하는 운영으로 전환했다. 현재 규칙은 `configs/public_league_v1.json`으로 고정했다. 변경 시 기존 DB/결과를 덮지 말고 v2로 분리한다.
- 서비스: `src/kaggriculture_meta/public_league.py`, 실행기 `tools/public_league.py`, 설명 `docs/public-league.ko.md`. DB/원본/고유 소스/HTML은 `state/public_league/`. 대시보드 `http://127.0.0.1:8791`.
- 신원 규칙: 정규화한 **전체 실행 소스 SHA-256이 같은 경우만** 한 agent로 중복 제거하고 모든 Kaggle 노트북 제목·작성자·링크를 alias로 묶는다. 임계값·판매 시각·경로 한 줄 등 미세 코드 차이도 별도 agent다. 행동 fingerprint/초반 유사성은 중복 근거가 아니다. 원본·과거 버전·탈락 소스는 삭제하지 않는다.
- 리그 규칙: 공식 native reacting, 결정적 신규 seed, 양 좌석, **8 workers**, cycle당 최대 240경기, top 50, 신규 challenger 슬롯 10, 최소 8경기. `game_deficit_balanced_pairing`이 누적 경기 수가 가장 적은 모델과 덜 만난 pair를 먼저 채우고, 세 번 중 한 번은 경험 많은 강자와 붙인다. 첫 배치 뒤 `archived`가 되어도 활성군 중앙 경기 수에 도달할 때까지 주기 사이 catch-up을 계속하며, 격차가 닫히면 우선순위가 자동으로 내려간다. 유효 경기만 batch Elo 및 승점률 Wilson 95% 구간에 반영한다. agent 귀속 코드 오류는 2경기, 단일 행동 1.5초 초과는 서로 다른 상대를 포함한 4경기에서 quarantine한다. 12워커는 이 PC에서 CPU 경합 거짓 실패를 만들었으므로 다시 쓰지 않는다.
- 현재 자료(09-21 07:10): 213 notebook ref / 271 version / 116 unique agent, 총 valid 6,429경기(연속 대결 대기). Pipe16, Metav4 v13, More Wheat, V51/V52/V53, Local Best 등이 신규 후보로 편입됐다. Metav4 v13·Master Engine V4·Autonomous AI 최신본은 exact source `9d634946...` 하나로 묶였다. `notebookdb6965aa8e`는 처음에 `FILES['main.py']`의 base85+zlib 포장을 추출기가 읽지 못해 `no_source`로 오분류했다. AST literal만 읽는 비실행 추출기를 추가해 V52와 현재 V54를 각각 고유 candidate(`c81dbb01782d...`, `949e2eed4101...`)로 편입했다. 과거 버전 추출이 current alias를 덮는 결함도 함께 수정했다.
- 최신 실행: 우리 8개를 처음 넣은 cycle은 206/240 valid, 34 invalid였다. 신규 모델은 각각 약 28~32경기를 우선 배정받았다. invalid 중 다수는 `Pure RL agent: BC + PPO self-play`가 17개 상대와 50경기 모두 90초 전체 경기 제한을 넘긴 것으로 특정되어 자동 quarantine했다. 완주·719회 호출·행동 예외 0인데 `overflow_contract_errors` 자기진단 키만 양수였던 2경기는 경고로 낮춰 복구했고, o238의 30경기 전적도 정상 복원했다. 신규 우선권은 배치 도중에도 최대 32경기이며 도달 즉시 focus/opponent 우선순위에서 내려가 일반 선발로 전환한다. 27 unit tests PASS. 초기 순위는 표본이 작아 제출 근거가 아니다.
- 자동화: Windows `Kaggriculture Public League Collect` 작업이 기본 **3시간** 주기로 **수집만** 실행하고 겹침을 금지한다. 09-21 감사에서 작업이 배터리 실행 금지/배터리 전환 중지/WakeToRun off라 약 11시간 실행되지 않은 원인을 확인해 `AllowStartIfOnBatteries`, `DontStopIfGoingOnBatteries`, `WakeToRun`, `StartWhenAvailable`로 고쳤다. 대시보드에서 예약 작업을 **자동 수집 ON/OFF**로 실제 활성/비활성화하며, OFF여도 수동 `지금 수집`은 가능하다. 대결은 단일 **연속 대결 OFF·시작 / ON·중지** 토글이 관리한다. 240은 완전 리그가 아니라 최대 50개 풀에서 120쌍을 양 좌석으로 실행하는 배치 상한이며, 배치 종료 후 순위 갱신→다음 240경기를 재편성한다. 브라우저 heartbeat의 종전 15초 만료는 백그라운드 탭 타이머 절전 조절을 탭 종료로 오인해 연속 대결을 끊었다. 만료를 180초로 늘리고 명시적 pagehide는 새로고침 유예 5초 뒤 종료하도록 수정했다. 마지막 브라우저 탭 종료 시 실행/대기 worker를 정리한다. 신규 catch-up 우선권은 32경기까지만 적용되고 이후 일반 선발로 낮아진다. 2026-09-20 13:50 KST 기준 이후 편입된 agent만 12시간 동안 `NEW`로 표시한다. 루트 `public-league.html` 또는 VBS로 콘솔 없이 연다. 현재 UI 설정은 사용자가 선택한 **3시간/8 workers**, 자동 수집 ON, 연속 대결 ON이다.
- 리더보드 경기 모니터 타당성 감사(구현 보류): CLI leaderboard에서 team/score/date를 얻고, 공개 `ListEpisodes`는 submission ID에서 상대의 submission ID까지 확장할 수 있다. 기존 29개 episode index에도 1,833팀/2,826 team-submission 연결이 있고 `live_episodes.py`, `fetch_current_elite.py`, `live_suite.py`, `rival_source_trace.py` 등을 재사용할 수 있다. 최소 증분 수집·기본 행동 분류·대시보드 표시는 약 3~5시간, 버전 변경/재시도/중복/exact-source 검증까지 넣은 안정판은 약 8~12시간 예상이다. Top10×최근50 최초 backfill은 중복 전 약 15GB·30~90분 예상. push API는 없어 5~15분 polling이고 private agent는 exact/likely lineage/behavioural/unknown의 신뢰도로 표시해야 한다. 사용자가 구현 전 소요만 요구했으므로 아직 구현하지 않았다.
- 최신 g000(56381011) vs 최신 우리 v9/4(56371746) 감사: 18:14 KST 재조회 현재 점수는 g000 2707.6(73경기 54/19/0), v9 2451.9(118경기 80/29/9). 고정 진단 스냅샷은 g000 70경기 53/17/0(승점 .757), v9 116경기 79/28/9(.720)이며 95% 구간이 크게 겹친다. 정확 상대 submission 교집합은 1개뿐이다. g000은 2600~2800 상대 35경기에서 21승14패, v9은 2600+ 상대 0경기로 서로 다른 matchmaking 층에 있었다. 각 제출 first16+latest16의 64세계에 기존 frozen-live verifier로 두 정책을 모두 재생했고 제출 행동 신원은 양쪽 32/32 완전 일치했다. g000-v9은 전체 승점 +7.03%p/margin +64.5/own -42.6이나 bootstrap95가 [0,+14.84]로 0 포함. g000의 latest16 고평점 세계에서는 9점 vs v9 4점, margin +418.9/own +120.2, L->W 5건; v9 latest16 세계에서는 g000 7점 vs v9 7.5점이다. 원인은 (a) 서로 다른 시각·상대·초기 경로가 만든 adaptive-rating 층 분리와 (b) g000의 유일한 활성 차이인 1~2턴 premium SELL 선행이 현재 고평점 판매 경쟁 세계의 좁은 패배를 일부 뒤집은 효과가 함께 있는 것으로 제한한다. 동결 상대라 실제 반응효과는 확정하지 않으며 약 256점 차이 전부를 코드효과로 보지 않는다. 로컬 public league도 g000 1968.5/147경기와 v9 1954.6/152경기로 소폭 차이이며 직접전은 한 seed 양좌석 g000 2승(+904)뿐이다. 자료: `state/c356_live_gap/`, `o_replays/c356_live_gap/`, `o_results/live_episodes_{56381011,56371746}.json`.
- Kaggle 점수 정정(13:08, 표시 수정 13:31): 초기 수집기는 목록의 `totalVotes`를 `public_score`로 잘못 읽었다. 이제 `LegacyKernelsService/GetKernelViewModel`의 연결 제출에서 현재/최고 Public Score를 읽고 추천 수와 분리한다(159/159 조회 성공). 대시보드는 **로컬 Elo**, **Kaggle 현재/최고 점수**, **게시·갱신일**을 각각 표시한다. 작성자의 다음 제출에 따라 현재 점수가 즉시 바뀌므로 전체 "공개 1위" 카드는 제거했다. 행별 점수도 시점 의존 참고값이며 로컬 리그 순위와 같은 뜻이 아니다.
- 우리 비교군(13:08): `configs/public_league_local_agents.json`에서 c129, o219, o227, o238, o239_50, o240, g000, g001의 고유 소스 8개를 `[우리]` alias로 편입했다. c312는 공개 v9/4와 exact source duplicate라 별도 agent로 추가하지 않았다. 전체 소스 SHA가 같아야 중복이며, 실제 코드가 조금이라도 다른 미세 조정본은 별도 agent다. 현재 자동 cycle이 이 8개를 우선 평가 중이다.
- c355는 성능 후보가 아닌 생산계획 실행 감사로 종료: retry_v3에서 예상 tomato/carrot/strawberry/wheat 60/14/8/5 대비 실제 45/13/8/3, fertilizer 18 시도 중 9 성공, fixed-shop도 생산량 동일. retry_v1 10-slot 초과, retry_v2 조기 land guard 결함은 수리됐지만 경쟁력 증거가 없어 새 리그 우선순위로 대체됐다.

## 현재 목표와 운영 규칙 (긴급 개편 및 절대 원칙)

- **[2026-09-20 12:05 KST 정규 Confirm 전수 완료 및 분석] g003_calibrated_turnover 결과, 기준선 c312(v9/4) 대조 및 Kaggle 미제출 보류:**
  - **후보 파일**: `agent/g003_calibrated_turnover.py` (SHA-256 `b059b17deca6b1e3a2210b9b3542ae68f1c5546cee3c91a7e28af81a78d99ded`).
  - **실행 디렉터리**: `state/agent_experiments/frontier_g003_confirm_clean` (256경기 12워커 하위프로세스 격리 전수 완료, 128조건 페어드 분석).
  - **공식 기준선 원칙 준수**: 사용자 지침에 따라 우리의 참된 공식 개발 기준선은 **`c312(state/c312/public_v9_4.py)`**임을 재확인.
  - **정식 Confirm 검증 지표 (vs V48 모체)**:
    * `mean_point_delta`: **+0.15625** (+15.63%p 승점률 대폭 상승, 58승 54패 16무 vs 30승 66패 32무)
    * `mean_margin_delta`: **+$346.70** (후반 밀 포기 대비 당근 고속 회전 이익 창출)
    * `mean_own_cash_delta`: **+$299.95**
    * `win_to_loss`: **0건** (128조건 전수에서 승리->패배 역전 0건, 무결성 완벽 유지)
    * `tie_to_loss`: **0건** (무승부->패배 역전 0건)
    * 98.5% Bootstrap CI: **[+0.046875, +0.28125]** (전구간 완벽한 양수, `signal: "positive"`, 통계적 유의성 확보).
  - **상대별 세부 성적 (Subgroups vs 4개 프론티어 군)**:
    * vs **v9 (c312 / public_v9_4)**: 승점 델타 **+0.0625** (+6.25%p, 4승 28패 vs 2승 30패), 마진 델타 **+$450.50**, 현금 델타 +$340.50, W->L 0건.
    * vs **v48**: 승점 델타 **+0.25** (+25.0%p, 10승 2패 20무 vs 2승 2패 28무), 마진 델타 **+$364.19**, 현금 델타 +$452.88.
    * vs **o239_50**: 승점 델타 **+0.0625** (24승 8패 vs 22승 10패), 마진 델타 **+$296.75**, 현금 델타 +$137.81.
    * vs **v49**: 승점 델타 **+0.25** (+25.0%p, 20승 12패 vs 12승 20패, +8승 추가 대역전), 마진 델타 **+$275.38**, 현금 델타 +$268.63.
  - **텔레메트리 전수 분석**:
    * `conversions`: **498회** 당근 회전 파종 성공.
    * `confirmed_plants`: **498회** (100% 정상 파종 확인).
    * `harvest_units_requested`: **1,626u** 당근 수확 달성.
    * `noop_harvest_suppressed`: **1,262회** 빈 타일 헛수확 억제.
    * `purchase_or_route_unfulfilled`: **48회** (시장 시세/재고에 따른 정상 조건부 스킵, 헬스 게이트 분리).
    * `errors`: **0회** (런타임 오류 0건).
  - **Kaggle 미제출 결정 사유 (사용자 절대 원칙 준수)**:
    * 사용자 지침: *"앞으로 검증을 확실하게하고 확실히 좋아진게 아니라면 제출하지마"*, *"참고로 우리의 기준은 c312(v9/4)야"*.
    * g003은 V48 대비 전구간 양수 CI(+0.047 ~ +0.281)와 0회귀, 마진 +$346.70으로 V48 기준 승격을 입증함.
    * **그러나 우리의 참된 기준선인 `c312(v9/4)`와의 직접 대결에서는 V48 차체 자체의 한계로 인해 4승 28패(승률 12.5%, 마진 -$2,128.2)로 여전히 열세임.**
    * 따라서 `c312(v9/4)`를 넘어서지 못한 모델을 성급히 제출하는 것은 live ladder에서 1위를 달성할 수 없으므로 **Kaggle 제출을 엄격히 보류(WITHHELD)**함.
  - **최종 결론 및 차기 과제 (g004)**:
    * g003을 통해 "경제성 게이트 현실화(`value < cost + 15`)와 헛수확 억제, 경로 인증 수확" 메커니즘이 모체 대비 확실한 이익(+$346.70)을 낸다는 것을 완벽히 입증함.
    * 리더보드 1위 공략을 위한 차기 작업: 이 검증된 고속 회전 메커니즘을 V48이 아닌 공식 기준선인 **`c312(public_v9_4)` 차체**에 직접 이식하여 c312의 초반 막강한 경제력 + g003의 후반 작물 회전을 결합하는 `g004` 개발이 최우선 과제임.

- **[2026-09-20 07:55 KST 정규 Screen 2차 전수 완료 및 분석] g002_screen_v2 결과, 병목 원인 규명 및 Kaggle 미제출 보류:**
  - **후보 파일**: `agent/g002_route_certified_turnover.py` (SHA-256 `c1a8aef3c5c0c8ccef757fe43d427d19b99d035e15da4fad84c04aaa0ec6f866`, 376,700 bytes).
  - **실행 디렉터리**: `state/agent_experiments/frontier_g002_screen_v2` (256경기 전수 완료, 128조건 페어드 분석).
  - **정식 검증 지표 (vs V48 모체)**:
    * `mean_point_delta`: **+0.0078125** (+0.78% 승점률 상승)
    * `mean_margin_delta`: **+$14.62** (1차 +$9.27 대비 +$5.35 추가 향상)
    * `mean_own_cash_delta`: **+$7.71** (1차 +$6.41 대비 향상)
    * `win_to_loss`: **0건** (128조건 전수에서 승리->패배 역전 0건, 무결성 유지)
    * `tie_to_loss`: **0건** (무승부->패배 역전 0건)
    * 99% Bootstrap CI: `[0.0, 0.03125]` (`signal: "inconclusive"`, `promotion: false`).
  - **상대별 세부 성적 (Subgroups)**:
    * vs **v49**: 승점 델타 **+0.03125** (6승 26패 vs 5승 27패, +1승 추가 달성), 마진 델타 **+$38.78**, 현금 델타 +$12.59.
    * vs **o239_50**: 승점률 75.0% (24승 8패), 마진 델타 **+$19.69**, 현금 델타 **+$18.25**.
    * vs **v48**: 승점 델타 +0.0, 마진 델타 +$0.0 (32경기 2승 2패 28무 완전 대등).
    * vs **v9**: 승점 델타 +0.0, 마진 델타 +$0.0 (32경기 4승 28패).
  - **텔레메트리 전수 분석 및 병목/실패 원인 완전 규명**:
    * `noop_harvest_suppressed`: **528회** 억제 (빈 타일 헛수확 완벽 차단).
    * `carrot_rotation_certified_routes`: **2,291회** 경로 인증 통과.
    * `carrot_rotation_gate_value`: **2,257회 차단 (98.5% 차단율!)**.
    * `carrot_rotation_conversions`: **8회** (시드 1626853671에서만 8회 발동, 해당 시드 vs v49 마진 +$1,241.0 대역전승).
    * **[핵심 병목 원인 (Root Cause)]**:
      - `_c146_control` 내 경제성 평가식: `cost = 20 + scheduled_wheat * grain_quote` (~$105).
      - `value_failed = value < cost + 100`!
      - 3개 수확 당근의 기본 가치는 ~$105인데, 밀 포기 기회비용(~$105) 대비 무려 **+$100의 비현실적 추가 마진(총 $205 이상)**을 요구하도록 하드코딩되어 있었음.
      - 또한 `supply` 계산식에 `+ 32`라는 가상의 경쟁 작물 페널티가 추가되어 당근 예상 시장 가격을 30% 이상 인위적으로 폭락시킴.
      - 이로 인해 16개 시드 중 15개 시드에서 2,257개의 유효 인증 경로가 경제성 게이트에서 전부 기각되어 단 1건도 회전하지 못함.
  - **Kaggle 미제출 결정 (사용자 절대 원칙 준수)**:
    - 사용자 지침: *"앞으로 검증을 확실하게하고 확실히 좋아진게 아니라면 제출하지마 다시 작업을 시작해"*
    - g002는 V48 대비 0회귀, 마진 +$14.62 우위를 보였으나, 99% CI 하한이 0.0에 머물러 통계적 유의성(`signal: "inconclusive"`)을 달성하지 못했으므로 **Kaggle 제출을 엄격히 보류(WITHHELD)**함.
  - **차기 개선 과제 (g003)**:
    1. 경제성 평가 임계치 현실화: `value < cost + 15` (밀 대비 실질 +$15 이상 순이익 시 회전 허용) 및 가상 `+ 32` 공급 페널티 제거.
    2. 주문 충돌 게이트 완화: 부모 정책의 사료/가축 주문과 충돌하지 않는 한 안전하게 당근 씨앗 1개 병합 허용.
    3. 능동적 경로 스케줄링(Active Route Scheduling): 수동적 편승을 넘어 d20+ 놀고 있는 일꾼 손에 능동적으로 급수/수확 경로를 배정.



- **[2026-09-20 07:15 KST 전면 감사 및 검증 체계 정상화] g000/g001 라이브 실패 원인 규명 및 프론티어 패널 확립:**
  - **실패 원인 완전 규명**:
    - 선행 제출된 `g000_apex_frontier`(2439.2) 및 `g001_dynamic_liquidation`(2496.0)은 구형 기준선인 `public_v9_4`(2596.7)를 상대로만 평가되었고, 상대 패널 또한 과거 2300-2400대 상대(k0006, v49, o240, v9)로만 구성되어 **치명적인 로컬 위양성(false positive)** 신호를 발생시켰음.
    - 정밀 다중 시드 검증 결과 (단일 시드 편향 교정):
      * 선행 보고는 시드 1542303036 단 1개만 실행한 결과(-$573.0)를 전면 패배로 일반화했던 치명적 오류가 있었음.
      * 실제 다중 시드 정밀 측정 결과: 시드 1384849883에서 g001은 V48을 상대로 양 좌석 모두 +$3,238.0 대승, 시드 416733134에서도 양 좌석 +$474.0 승리하여 3개 시드 평균 마진 +$1,046.3 기록.
      * 반면 o239_50 상대 대전에서 V48은 시드 1542303036에서는 +$526.0 승리했으나 시드 1384849883에서는 -$2,445.0으로 참패. 반면 g001은 o239_50을 상대로 두 시드 모두 승리(+$473.0, +$1,254.0).
      * g001의 라이브 래더 부진(2496.0)의 진정한 원인은 V48 대비 마진 부족이 아니라, 모체인 public_v9_4의 구형 개막 라운드트립 구조가 라이브 상위권 메타(개막 0-1턴 스왑)에서 체계적으로 공략당하기 때문임.
    - 또한 c129(9월 13일 2820.3)는 현재 래더 메타(오프닝 라운드트립 등) 변화로 오늘 제출 시 ~1400-1500점대로 추락하는 완전 구형 모델임(p000_base19가 1381.6으로 폭락한 것과 동일).
  - **현재 검증된 경쟁 프론티어 (Verified Competitive Frontier)**:
    1. **현재 메타 최강 라이브 봇**: `agent/o239_open_roundtrip_50.py` (라이브 2660 ~ 2754).
    2. **최강 로컬 5정책 H2H 기준선**: `V48` (`agent/p005_v48_exact.py` / `state/o_dev/v48_clearqueue_public.py`, 라이브 사본 2560 ~ 2760, 로컬 대전 승점률 90.6%).
    3. **최종 1위 목표**: `Majkel1337` (3278.5) (d20+ 고속 작물 회전: 밀 73.3회, 당근 39.9회 파종, 후반 d20-29 마진 +$3478 폭증).
  - **절대 운영 규칙**:
    - **앞으로 검증을 확실하게 하고, 실제 강한 기준선(V48 및 o239_50)과 최신 엘리트 반응 상대에 대해 확실히 좋아진 것이 입증되지 않는다면 절대 제출하지 않는다.**
    - 정식 검증 기준선(Primary Parent)을 구형 `public_v9_4`에서 실질 최강인 `V48`(`agent/p005_v48_exact.py`)로 교체하고, 상대 패널을 `o239_50`, `v48`, `v49`, `v9`로 전면 개편.
    - 새 정식 검증 설정: `configs/validation/frontier_elite_arena_v1.json` 확립.
    - 사용자 지침: 시뮬레이션 캠페인은 사용자가 직접 실행하며(12 CPU 워커), 에이전트는 검증 설계와 명령어를 완벽히 준비하고 handoff한다.

- **Majkel(3278.5) 1위 공략 기전 분석 및 d20+ 고속 회전 연구**:
  - **V48의 한계 규명**: V48은 큐 정리(`_e334_compact`)로 중반까지 매우 강력하나, 후반 d20-29에 무려 104회의 PASS 명령을 수행하며 d29에는 36개 타일이 완전히 비어있는 채 방치됨.
  - **Majkel의 압도적 우위**: Majkel은 d20-29에 PASS가 18회에 불과하며, 딸기/토마토 수확 후 빈 타일을 즉시 밀(2일 완성) 73.3회, 당근(2일 완성) 39.9회로 3~4회 연속 재파종하여 후반 현금 폭증(+$3,478)을 달성.
  - **단순 휴리스틱의 실패와 경로 인증의 필요성**: 단순 PASS 가로채기(임의 밀 파종) 프로토타입 시험 결과, 급수/수확 경로가 보장되지 않은 미완성 파종으로 인해 씨앗값 낭비 및 마진 -$2174 손실 발생. 따라서 c306에서 입증된 바와 같이 **경로 인증(Certified Route)을 기반으로 한 후반 수확 및 재파종 계약**만이 회귀 없이 안전하게 초과 이익을 실현할 수 있음.

- **g001_dynamic_liquidation 및 g000_apex_frontier 라이브 실측 결과 (참고/교훈):**
  - g000 라이브 평점 2439.2, g001 라이브 평점 2496.0 기록. public_v9_4(2596.7) 기반 개조는 라이브 상위권(2600~2800+)의 라운드트립 개막과 고속 큐 정리를 넘어서지 못하고 역효과 발생. 향후 모든 연구는 V48 및 o239_50 기반으로 전면 전환.


- **g000_apex_frontier 정식 감사·정식 검증·제출 확인 완료 (2026-09-20 00:30 KST):**
  - **후보 파일**: `agent/g000_apex_frontier.py` (SHA-256 `1ac340d0b213f7a63dddfccd26e8341305a479ef87543f817751360b0ed450e4`).
  - **핵심 기전**: 창고 내 이미 물리적으로 존재하는 프리미엄 작물(딸기·양털·달걀·우유·멜론·당근·토마토)의 계획 판매 시점을 1~2스텝 안전하게 앞당겨 시장 가격 감쇄를 선점하는 물리적 재고 전진(Physical Inventory Sale Advance). 주문 뭉침(bunching) 방지를 위해 추가 매도 주문을 기존 테이프 주문 뒤에 안전하게 추가(`cur = cur + extra`)하고 가축 전환은 안전 기준(`milk_shops >= 3`) 준수.
  - **선행 보고 감사 및 정식 검증 재실행 (`state/agent_experiments/g000_apex_confirm_v2`)**:
    - 선행 시도 감사를 통해 기존 `g000_apex_confirm` 폴더의 결과가 소 전환 완화(`V9_HERD_MIN_MILK_SHOPS = 2`)된 초기 프로토타입(`f177b767`)으로 실행되어 `promotion: false`, `win_to_loss: 6`으로 실패했던 기록임을 적발.
    - 정식 후보(`1ac340d0`)에 대해 12 CPU 워커 하위프로세스 격리 canonical validation(`validation_v2.py`, 256경기) 전수 실행 완료.
    - `confirm` 단계 (16개 미공개 독립 시드, 256경기): 126승 2패 0무 (승률 98.44%), 평균 마진 +$3,105.7 vs v9 +$2,952.2 (+153.5 delta), win_to_loss: 0건 (회귀 0), tie_to_loss: 2건 (시드 729160656 좌석0/1), bootstrap 98.5% CI [+0.0625, +0.125] (전구간 양수, signal: "positive"), vs v9 기준선 30승 2패 (마진 +$551.9), vs k0006/o240/v49 전승 (각 32승 0패).
    - `screen` 단계 (16개 개발 시드, 128경기): 106승 20패 2무 (83.59%), vs v9 기준선 24승 6패 2무 (마진 +$127.4).
    - 양 단계 합산 런타임 오류 0건, 타임아웃 0건, 해시 계약 일치.
  - **Kaggle 제출 상태 확인**: Ref ID `56363144` (`submission.tar.gz`), `SubmissionStatus.COMPLETE` 확인, 초기 레이팅 688.9로 래더 진입 후 1600.3으로 상승 중.

- 목표: Kaggriculture 리더보드 1위. v9/4 baseline 대비 검증된 g000_apex_frontier를 필두로 연구·구현·검증을 지속한다.
- 과거 2800점대 기록·V48 점수·base19 champion 명칭은 현재 경쟁력의 보증이 아니다. 부모와 구조는 재검토 중이며 과거 부모 결정 대기가 연구를 막지 않는다.
- 모든 새 작업은 아래 **최신 작업 기록**에 `시각 | 작성자 | 변경/증거 | 판정 | 다음` 형식으로 쓴다. 최신 상태도 함께 갱신한다. 별도 c/o 작업 원장을 다시 만들지 않는다.
- 새 도구 전에 `tools`, `o_tools`, `src`, 기존 보고서/산출물을 검색한다. 필요한 기능이 없는 경우만 확장하고 이유를 기록한다. 기존 구현도 정확성을 전제하지 않는다.
- **모든 실험 전 이력 확인:** 가장 가까운 선행 시도, 실제 실행/검증 범위, 구체적 코드·데이터·검증 오류 근거, 이번에 달라지는 점과 재시도 가치를 먼저 기록한다. 이름/부모만 바꾸는 것은 근거가 아니다. 미실행·무동작·파손·정상 음수 결과를 구분하고, 오류를 추측만으로 단정하지 않는다.
- 토큰/CPU: 필요한 부분만 읽고, 기존 결과→작은 재현/발동 확인→넓은 검증 순서. 한 캠페인씩. 최신 사용자 지시 **기본 8워커**. `validation_v2.py`/`run-validation-v2.ps1`는 더 큰 값도 지원하지만 이 PC에서는 12워커가 1초 제한의 거짓 실패를 만들었으므로 새 정식 검증과 Public League는 8을 쓴다. 과거 v1·동결계약과 이미 완료된 12워커 결과는 수정하지 않는다. 소수 진단 재생은 순차 가능. 기존 동결 후보/결과 보존.
- **조건 의존성:** 상대 제출/버전·상점·시드·좌석을 함께 기록한다. 서로 다른 세계의 생산·현금 차액을 회복 가능한 인과 효과로 읽지 않는다. 정책이 미래 상점 경로까지 바꿀 수 있어 native 동일 시드도 같은 전체 세계를 보장하지 않는다. 전체 성능과 고정 상점 기전 진단을 분리하며, 사후 상점 조합으로 고른 부분집합은 탐색용으로만 쓴다.
- 보호 blind 7240–7255 미사용 유지. **최신 소유자 위임: 검증으로 개선이 확인되면 Codex가 즉시 Kaggle에 제출해 라이브 검증하고, 제출 뒤에도 1위를 향해 개발을 계속한다. 과거 소유자전용 조항을 대체.** c300+ 새 구현·로컬 검증은 사용자 위임 범위에서 진행한다.

## c300 현재 확인 결과

- **c351–352 미래녹음없는 경로지원:** 현재소스12세계 위치7,602일치·추가고용69누락. 매턴 창고접근점유보존으로 시간대추정회피, 전수375/원본1,327구간지원. 아직생산/자원/부모고용결과·강도미입증. [결과](reports/c351-c352-prospective-route-contract-2026-09-19.ko.md).

- **c346–350 부모통합/현금오독방지:** 변경관측shadow50영역밖/197시장차이→실부모실행40/15생산동일. 정확LOCAL회계719전이/잔차0에서큰own+26947은4스무디/우유+21590가주요동반변화. 공통상점+입력예약으로own+1169/margin+1331·여전히패배. 예약은555매도1보류→557수령2→562시비복구. [보고서](reports/c346-c350-parent-integration-2026-09-19.ko.md).

- **c345 당일관측지원 감사:** 원본소스719행동일치후 currentobs+초기화된자기경로로114구간640좌표모두예측·HIRE차이0,동작차5/lease밖6구간12스텝. 미초기화helper의빈테이프결과폐기. 변경정책관측/다일계약은미검증. [보고서](reports/c345-observable-contract-support-2026-09-19.ko.md).

- **c344 첫선택계획 공유실행PASS:** d21/23/24 작업종류·유한수령·비료흐름·필수DROP1칸앞당김. 실제40토마토/15당근·시비11/11·식재11/11·위치114/출생263일치. 현재관측정책/경쟁수익미검증. 타일검사재고삭제키카운터오류수리,원DP예산/공유시비집계는영향없음. [보고서](reports/c344-typed-routes-and-input-carry-2026-09-19.ko.md).

- **c343 유한투입 복구/현재배정 한계:** 경로여유만으로비료5u실수령·시비7/11·실제34토마토/12당근,위치계약유지. 남은4구간의입력운반/잡초포함정확하한은1개가능/3개용량초과(4순열검사일치). 전략/구조한계가아니며도착재고·배정변경은미검증. [보고서](reports/c343-finite-input-and-window-slack-2026-09-19.ko.md).

- **c342 고용 경계 수리:** 원본75→113구간·32고용singleton, 토큰동일/KEEP지원. 생성84문제 중72재사용·12신규. 모든구간 시작/끝113과 출생263일치. 남은 시비8/식재1실패를 비료 운반/잡초로 분리. [보고서](reports/c342-hire-boundary-contract-2026-09-19.ko.md).

- **c341 비KEEP공동계획/실행FAIL:** 작업17–20최고만출력하던DP의저노동대안누락수리,0–20frontier로다른생산선택. 분리타일46토마토/34당근→공유농장18/25,263HIRE중18출생좌표차이·끝위치6불일치. 미래사후/고정매도probe현금은강도아님. [보고서](reports/c341-route-conditioned-production-frontier-2026-09-19.ko.md).

- **c340 공동선택 구현:** KEEP지원증명→warmstart로3모델최적,대체최대화도0이라경제FAIL아닌입력일정경로미지원. 509/533개개별필요조건실패,나머지공유제약충돌. 다음은방문가능일반영생성. [보고서](reports/c340-joint-programme-route-selection-2026-09-19.ko.md).

- **c339 비동기계약:** 원본컴파일12동일·재고/씨앗체결감사. 당일예측은 courier/후속작물과충돌해영역분리, 개발912+추가310구간동일. 후보성능아님·예측고용누락유지·경로변경fallback미검증. [보고서](reports/c339-asynchronous-region-contract-2026-09-19.ko.md).

- **c338 공동계획 지원검사:** 한칸 자유일정48재생일치·13칸 경로163문제완료/2timeout해결. 동기화모형은 원본 d12/13분할관리를표현못하므로 성능판정없음. 다음은 타일별비동기지원부터. [보고서](reports/c338-production-and-route-support-2026-09-19.ko.md).

- **c337 경로 하한:** 원본12 재사용/신규대결0. 일꾼별구간 d18/19 절감0, 두일꾼123쌍 d18평균0.40·d19전부0. 고정 작업/끝위치 내 이동압축 기회는 작음; 작업교체·끝위치변경·전체공동최적의 불가능성아님. [보고서](reports/c337-task-preserving-route-capacity-2026-09-19.ko.md).

- **c336 범위 감사:** 원본12/12·해시PASS, 밀/멜론 추가급수0·당근2u/경기, 바로 쓸 PASS0. 조기당근전환 지지범위는 별도 미확인. 후보 미구현. [보고서](reports/c336-harvest-service-scope-2026-09-19.ko.md).

- **c335 현재증거갱신:** 이전API이후Majkel56216119 신규14경기모두14/14상태·현금재현,12승2패/8버전6팀. d11현금우세1회·d20+평균마진회복3478,밀생산상대보다−82.6u. 소스/플래너구조증명아님·평균차인과해석금지. [보고서](reports/c335-current-leader-evidence-2026-09-19.ko.md).

- **c334 공동방문후보기각:** 고용·입력·부모번호계약정상,추가토마토23/25u. 대조own+300/margin−583.5,원본margin−11457.5. QA20/원장12재현·전환대조와상점동일,원본과상점변화. 물리계획성공≠경제적선택성공. [보고서](reports/c334-joint-crop-service-2026-09-19.ko.md).

- **c333 지원범위진단:** 기존방문+시비시각자유는토마토총+1u. 같은비료예산·타일당최대2추가정오작업을허용하면13칸65/64→91/92u,딸기는102유지. 실행경로/물류/시장없는사후물리상한이지이득아님. 초기PASS누락수리후c313대조12/12일치. [보고서](reports/c333-input-and-service-calendar-2026-09-19.ko.md).

- **c332 새공개정책기각:** Market Rhythm f3be6392 원본/계측4쌍·모드8쌍동일QA16,새16세계256native에서v9직접1승31패/승점−19.53%p CI전부음수·마진−2855. 해시PASS/오류0/상점128쌍동일. confirm없음. [보고서](reports/c332-market-rhythm-public-policy-2026-09-19.ko.md).

- **c331 기각:** 초기밀재파종1칸 조기딸기4u 실행성공에도2개발세계평균 own−435/margin−579. 상점/가축구매불변·일손/비료/후속작물기회비용포함. 확대없음. [보고서](reports/c331-early-wheat-berry-lane-2026-09-19.ko.md).

- **c330 완료:** 현재v9 courier계획은 최종명령까지정상실행,입고단순누락기회3턴뿐. 우리수확후판매가대체로빠르지만딸기생산이후기저가격구간에집중. 원본12행동/전이/FIFO보존확인,새banking후보없음. [보고서](reports/c330-transport-and-production-calendar-2026-09-19.ko.md).

- **c329 완료:** 원본12경기719전이 재현 후1,692개3턴구간 분기. 재고/주문제약 충족242변경 중현금외종료상태(키순서포함)일치233개, 사후기회합 평균+$30.75/양수6경기로확대중단. JSON 중간상태의 키순서 손실 오류를 격리·수리. [보고서](reports/c329-local-sale-opportunity-2026-09-19.ko.md).

- **c328 완료:** 203재사용 원장/210,100행 단기매도 학습. 24평가경기에서 우유·딸기 확률오차 개선, 양털 악화로 전체기준FAIL. 평균개선양수와 정책가치는 구분, 품목 사후선택 안함. [보고서](reports/c328-short-horizon-sale-learning-2026-09-19.ko.md).

- **c327 완료:** 실제최종자기매도/가격1검열로원본12매도복원오차0(사용23,396품목턴)이지만320native 성능gateFAIL(승점+0.625%p CI0포함·마진−15). 행동100/160변경,무동작아님. [보고서](reports/c327-final-sale-observer-2026-09-19.ko.md).

- **c326 완료:** 내장P단기예측기 가격gate 후보320native기각(승점−13.75%p/마진−541). 첫세계20원장수확/판매수량불변·상대가격회복관찰. 과거매도복원180오차는모두자기시장유입예측차이로설명되나이번후보에서는미수정. [보고서](reports/c326-short-sale-predictor-contract-2026-09-19.ko.md).

- **c325 완료:** c176부모대조를별도폴더에서발견해역사현금8/8재현. 전용일손과부모번호중복129/실제명령차이116을수리했지만부모대비마진−14.5k/−17.1k로기각유지. 미검증이아닌실제실패+부분실행결함이다. [보고서](reports/c325-historical-worker-contract-audit-2026-09-19.ko.md).

- **c324 완료 / 새 공개 소스 우위 미확보:** 두노트북동일ed89be8c,QA16 원본4쌍/실행모드8쌍동일. 새16세계4소스양좌석256native 승점+3.91%p(CI−4.69..+13.28),own−19/margin−79,직접v9 16승16패. 해시PASS·health0/max0.233초·128쌍상점동일. confirm/final없음,비교상대보존·부모v9유지. [보고서](reports/c324-public-revision-2026-09-19.ko.md). 보호blind미사용.

- **c323 완료 / 초기 집단 무신호 중단:** 탐색기세대누락무시뮬36/36재현·수리,중립지원512/QA16후64세계512조건×12조합6144훈련. KEEP512행동/현금동일,11변형모두승점≤0·승점/마진동시양수0. 사전중단규칙적용,교배세대/확인/final없음. [보고서](reports/c323-search-support-audit-2026-09-19.ko.md). 기준선v9유지·예약확인32시드/보호blind미사용.

- **c322 완료 / 진화 탐색 후보 독립 확인 기각:** 36훈련조합 중 사전선택trial30은576native확인에서 승점−15.28%p(24seed CI[−28.13,−3.47]),own+560/margin−188,W→L45/L→W1. 해시PASS·최종실행오류0/max0.234초·미발동108동일. 훈련8세계중발동4/승점이득1세계에집중. 첫활성24원장모두재현:own+5.46k지만상대+11.17k. o240진단키충돌로v2중단→행동불변어댑터QA8쌍후v3완료,원계약보존. [보고서](reports/c322-portfolio-search-2026-09-19.ko.md). 기준선v9유지·다른훈련후보선택/final/제출없음·현재캠페인없음·blind보존.

- **c321 완료 / 고정 생산 프로필5종 기각:** 생성190개 물리검증 뒤 관측 실행기를 연결. 개발28/off4동일·nativeQA14/14일치. 새8시드×4실행상대×양좌석×6모델384 native에서 모두음수: balanced own−554/margin−1288/승점−18.75%p;기타마진−626~−1742. 오류0/max0.155초/해시PASS·미발동160원본동일·구매확인1312레인/파종2336/실패0. 첫발동세계24원장양측행동·현금재현:새작물생산·판매실재하나미래상점경로와타품목수입도변화. 사후최선선택+3.125%p도v9에만있어선택기학습안함. [보고서](reports/c321-production-sequence-synthesis-2026-09-19.ko.md). confirm/final/제출없음·기준선v9유지·현재CPU작업없음·blind보존.

- **c320 순차재배 전체정책 기각:** 새16시드·4실행소스·양좌석·3정책384native, 해시PASS/오류0/max0.189초. 기존c177조건부전환 위 토마토종료→당근 부품은 own+166/margin+199/승점0이나 전체 vsKEEP own−881/margin−1125/승점−15.625%p·W→L18/L→W0. 미발동96/96행동동일,부품대비상점128/128동일. 첫활성시드24원장native재현:당근+16u/매출+767/씨앗+160,토마토불변·달걀−2u. QA12·off4/4동일. [보고서](reports/c320-sequential-crop-plan-2026-09-19.ko.md). confirm/final없음,기준선c312 v9유지·실행중캠페인없음·blind보존.

- **c319 완료:** 192/192·해시 PASS·KEEP64/64와 원래 동일shop 대안24/24의 양측행동/현금 재현. 고정shop 2칸 전환 own+580/margin+450/승점0, 전체 own+1944/margin+0.44/승점−3.125%p. native 대비 부호반전2/64·8/64. oracle 승점 양쪽+10.94%p. 상점변화만으로 c317실패를 설명하지 못하며 기존FAIL 유지·재학습없음. [보고서](reports/c319-common-shop-sensitivity-2026-09-19.ko.md).

- **c318 신규공개검증/DP분리 완료:** Enhancedv2 원본/계측행동4/4·실행모드8/8동일(QA16). 공통256native에서v9대비승점−17.19%p/마진−1554,직접4승28패→기준선v9유지. K0006은32승(v9 28/4)이지만DP만on/off128진단에서마진+$1.47·승점0(ON64기존행동일치/미발동19OFF동일). DP이식안함,비교상대보존.400실행오류0,confirm/final미실행. [보고서](reports/c318-enhanced-public-frontier-2026-09-19.ko.md). 현재캠페인없음·blind보존.

- **c317 직접선택학습FAIL:**16QA8조건원본행동동일+768native(32새시드/4실행상대/양좌석/3선택),오류0·max0.233초미만. 결정상태/접두256조건동일,189관측벡터. OOF승점+1.5625%p(CI−5.86..+7.81),margin+27.87;v9+9.375%p만양수/V49−3.125/나머지0→사전gateFAIL. oracle+10.55%p는대부분v9상대·미래결과진단. 2칸/전체전환의미래상점224/256·210/256변화,own+1631을순수효율로읽지않음. [보고서](reports/c317-direct-crop-action-learning-2026-09-19.ko.md). 모델/기준재튜닝·독립확인없음,현재캠페인없음·blind보존.

- **c316 자료확장 재시도FAIL:** 기존179경기/71버전/59팀(33원장재사용+146재현)으로RF설정불변학습. 별도24버전24경기 원장24/24일치;d27공개농장MAE 토마토14.18/딸기41.28,시장만28.87/29.92. 옛모델58.87/52.31보다개선했지만딸기시장만대조미달로사전gateFAIL. 모델/품목사후선택·정책적용안함. [보고서](reports/c316-expanded-supply-learning-2026-09-19.ko.md). 203정확원장/신규반사실게임0,현재캠페인없음·blind보존.

- **c315 학습 추가확인FAIL:** 제출버전중복31경기제거,train25경기50관점/9버전→첫test12에서d27토마토MAE19.54(시장21.90)/딸기42.90(50.98)개선. 모델동결후다른상대8버전8경기(정확원장8/8)에서는26.69(21.07)/57.40(56.24)로회귀. 모델정책적용/설정튜닝안함. [보고서](reports/c315-future-supply-learning-2026-09-19.ko.md). 기존로컬에서평가버전제외179경기/71버전확장가능자료발견,아직원장감사/학습안함. 현재캠페인없음·blind보존.

- **c314 예측감사 완료:** 12검증라이브×4시점×2품목 시장/상품보존식96/96일치. $1판매는시장재고에추가되지않음: d11→27딸기838u/순판매4724u. d27토마토수확86.2%/딸기21.6%는d11이후식재. 현재가고정딸기MAE114.69;공급시나리오오차/오차상쇄를확인했으나선택모델채택안함. HERD2기존공급floor비대칭그림자재현12/12행동동일·점수26/26동일이라확대안함. [보고서](reports/c314-production-forecast-audit-2026-09-19.ko.md). 제출후보없음·실행중캠페인없음·blind보존.

- **c313 32개발게임 완료:** 부모/off16의양측행동·현금이기존native와일치,해시PASS·관측변조/노출오류0. 같은2칸전환에수명수확수정은토마토+2u/실매출+70.75/margin+288/승점0. 그러나전환묶음은부모대비own−609.5/margin−146.75라제출/확대안함. 기전부품만보존,수량증가≠경제적선택성공. [보고서](reports/c313-crop-lane-contract-2026-09-19.ko.md). 현재실행중캠페인없음,blind미사용.

- **c312 완료 / 개발 기준선 갱신:** 공개 v9/4(bfee70e9)는 V49와 독립 두 단계 직접59승5패, 공통4상대 승점 +21.09/+31.25%p(각 시드CI>0),512실행 오류0. 공개 원본을 더 강한 기준선으로 사용; 제출후보 아님. 최신4+상위상대12 라이브719결정·양측현금 동일. 상위12 원장 전이/현금12/12일치: d11현금11/12우세이나2승10패, 평균마진−6402. 현재소스3000+ 기록3/31로#1급 미확보. [보고서](reports/c312-public-v9-frontier-and-elite-losses-2026-09-19.ko.md). 현재 캠페인 없음·blind보존.

- **c311 기준선 감사 완료:** 현재o240은V49와직접6승26패,부모대체FAIL. 최신4라이브행동재현을확인했으나최근관측점수2523은09-18경기기록이다. 새공개Tschinkel v9/4는예전router_v5와구분,c312실행QA통과후native비교중. [보고서](reports/c311-existing-frontier-audit-2026-09-19.ko.md).

- **c310 결정 지연 감사 완료:** 48개발게임에서 두 경로의 d6→d9 지연은 전체행동을 보존하면서 추가 상점을 관측할 수 있었다. 무조건전환 승점이득0, 확인된 선택여력은 한시드에 집중되어 확대학습하지 않는다. 다음은 기존 계획 생성/컴파일 도구가 새 경제 계획을 만드는 범위와 과거 결과 감사. [보고서](reports/c310-late-plan-compatibility-2026-09-19.ko.md). 현재 실행중 캠페인 없음·제출후보 없음·blind보존. 아래c309 종료시점의 c310미구현 표시는 역사 상태다.

- **c309 학습 선택 실패(13:15):** V49의 같은 개막을 공유하는 KEEP+7개 전체 생산 계획을 8새시드·4실행상대·양좌석에서 비교했다(512게임, 오류0, 최대0.195초 미만). 결정 관측/행동 접두 64조건 모두 동일. 시드 제외8fold RF 선택은 KEEP 대비 승점−4.69%p/마진+243, 사전 기준FAIL. 독립 배포 평가/제출로 진행하지 않는다. 사후oracle +20.31%p는 미래 정답을 본 진단일 뿐이다. [보고서](reports/c309-plan-choice-learning-2026-09-19.ko.md). 64행이 실제로는31특징벡터이고 다른시드에서 반복된 특징은3개뿐이었다. c310 미구현·실행중캠페인없음·blind보존.

- **c308 완료·고정 복제본 확대 중단(12:59):** 검증된Majkel단일시연의고용현금·경로별사료수령전제를수리해8상대32개발조건의d6구성2C3S12M8B복구. 그러나전체48게임(3정책×16조건)에서raw0승16패,수리본0승16패,V49 12승4무. 수리본은raw보다own+24.2k/margin+34.6k이나V49보다−14.4k/−46.3k. 노출오류0·max0.180초미만·해시일치. [보고서](reports/c308-plan-execution-contract-2026-09-19.ko.md). 단일시연의전체정책은승격안함,실행전제요소만보존. 보호blind미사용·제출후보없음. 다음번호c309,미구현.

- **Majkel 구조 정정(11:38):** 비공개 구현 미확정. r000의 행동접두분기와 O보관의 yhay불일치는 탐색플래너 증명이 아니다. [출처·62경기 행동 감사·상대거래 가설](reports/c308-majkel-architecture-evidence-2026-09-19.ko.md). 다음 학습준비는 공통개막의 실행전제/예외복원을 우선하며 날짜고정base19인계/녹음재생 반복을피한다. 조건부테이프·규칙컨트롤러도후보구조다.

- 실행 QA: base19/V48/o239의 개발 조건 6개 × native/fast-official/fast-legacy = 18게임. 관측(벽시계 잔여 시간 제외)·행동·최종 상태 비교 12/12 동일, 관측 수정 0. 전체 정책/핀 고정/과거 캐시까지 검증한 것은 아니다. [원자료](state/c300/execution_audit_v1/summary.json).
- 기존 3캠페인 1,952행을 독립 재집계: 소스/행 신원·승패 집계 불일치 없음. 상호 대전 400행은 고유 물리 조건 200개를 두 번 기록한 것(두 단계 각각 동일). 정책별 승률은 유지되지만 전체 행 수를 독립 표본 수로 쓰면 안 된다. [원자료](state/c300/evidence_audit_v1/campaigns.json).
- 캐시 단서: `proxy_eval` 키에 실행기/support·native/fast 모드가 빠짐. 캐시만으로 실행기 동등성을 주장하지 않음. 과거 결과 전체가 틀렸다는 판정은 아님.
- 최신 확인 리더보드 CSV2026-09-19 11:08:55UTC:1위Majkel1337 3278.5,10위3029.7. score제출56216119 최근3278.526/533완료,최근제출56332038 3160.619/162완료. v9소스대응56269928은09-17최종201완료/200유효로현재강도미확인. [현재증거](reports/c335-current-leader-evidence-2026-09-19.ko.md).
- 현재 4개 상위권 제출의 최근 2900+ 상대 경기 12개를 기존 `fetch_current_elite.py`로 수집(중복 제외 11경기). 기존 `replay_accounting`으로 11/11 전체 관측 재현·현금 잔차 0 확인. 전략 성능 평가가 아닌 원장 검증이다.
- **구형 원장 오차 발견:** 같은 2경기에서 `tools/o_revenue.py` 매출 오차 최대 +6628, 현금 재구성 잔차 최대 8294. `elite_revenue` 등 이 경로를 사용한 품목별 설명은 재확인 필요. 최종 현금/승패나 다른 엔진 훅 원장까지 일괄 무효화하지 않음. [교차검사](state/c300/accounting/legacy_comparison.json).
- Kaggle OAuth 로그인 완료, 읽기 전용 API 조회 가능. 인증정보를 문서/로그에 기록하지 않는다.
- 최신 elite 동결 진단 36게임(부모별 12, 전부 실행 유효): o239 12승이지만 11/12에서 녹음 상대 현금이 원본보다 1만 이상 감소했다(V48 4/12, base19 1/12). DSM 사례는 원본 135163 → o239 상대 0. **동결 상대의 자원·실행 경로 붕괴 때문에 이 승률로 실제 상위권 경쟁력이나 부모 순위를 판정할 수 없다.** paired 비교만으로 이 왜곡이 제거되지 않는다. [원자료](state/c300/frozen_parent_diagnostic/summary_rows.json).
- **c300 첫 전략 구현 기각:** [c300_head_commit](agent/c300_head_commit.py)은 base19의 전체 경로 대신 물자를 가진 이동 중 첫 작업만 보존한다. V48 실행 상대, 개발 7000/7001 양좌석: 자연 세계 own +9702 / rival +15435 / margin −5734, 2승→0승. 행동 변화로 미래 상점 경로도 달라져 own 증가는 실행 개선 증거가 아니다. 상점 고정 원인 진단 own −226 / margin −761, 0승→0승. 이동 직후 유효 작업 재배정은 455–553→54–66회로 줄었지만 수익 개선 실패. off 4조건의 일별 엔진 원장·최종 현금은 부모와 동일(모든 행동 해시 동등성까지 검증한 것은 아님). [결과·한계·해시](state/c300/headcommit_result.json). 확인/최종/제출로 진행하지 않는다.
- **c301 현장 작업 우선 기각:** base19의 VRP에서 현재 위치·물자 조건이 충족된 작업을 먼저 배정. 고정 세계 개발 4조건 own +1625 / rival +3150 / margin −1524. 2601–2824회 명령 발동, off 일별 원장·현금 동일. 멜론 −6u 등 투자 사슬 손실이 남아 확대 평가 중단. [결과](state/c301/result.json). c300/c301은 규칙 기반 상태 플래너의 배차 수정이지 다일 최적 계획이 아니다.
- **c302 gate 실패:** [V48+기존 o171e/o170c 묶음](agent/c302_v48_herd_bundle.py)은 선택한 기전 4조건 own +6112 / margin +7179, 0승→4승이었지만, 별도 native screen192(16시드/3상대)에서는 own −348 / margin +295 / 승점 +0.0104(CI −0.0313..+0.0625). W→L0, T→L2. 사전 own>0 조건 미달로 confirm/final 미실행. 최악 세계 1143946805의 mismatch4는 부모가 이미 PLACE GOOSE로 복구한 것이라 실패 배치가 아니다. 같은 세계·같은 상점에서 geese 교체가 상대 우유 경쟁을 풀어 줘 V48 상대 −11378. [판정](state/c302/screen_verdict.json). 제출 후보 아님.
- **최신 공개 자료 반영:** V49 원본 해시 확인 및 native/fast QA12게임·비교8/8동일, 최대0.147초. 비교 상대 사용 가능성이 확인됐을 뿐 강도/승격 미검증. EcoBot 복합 작업을 참고한 base19 파종→급수 감사2재생은 즉시급수178/179·266/267로 해당 단절 가설 근거 부족. [출처·해시·한계](reports/c300-public-research-2026-09-19.ko.md).

## 다음 작업

- **최신(c327 종료):** 같은복원수정조합/품목재튜닝중단. c328검토는기존c315/c316(장기공급)·c308(요청모방)과구분되는짧은실제시장유입예측. 기존203원장/사전특징에농장과일손좌표가이미있다. 새가치는최근이력·관측시점정렬·짧은지평·버전독립확인으로증명해야하며,시간표/최근주기대조보다나은지먼저검사한다. 현재새학습/후보없음.

- **최신(c326 종료):** 동일P가격gate/품목별튜닝중단. c327은 기존c308·c314–316의긴예측/행동모방한계와 비교해, 짧은구간의상대매도·공개농장/수확변화로 보이는 재고를 추정할 근거를 검토한다. 실제정책변경 전 관측가능 입력·실제체결 label·제출버전독립확인·가격1시장유입/전체판매 차이를 분리한다. 단순자기수입최적화는상대가격회복을놓치므로 정책평가는양측마진/승점으로한다. 다음후보미구현.

- **최신(c325 종료):** 같은 후기 작물전환 미세수리 확대 중단. 현재 elite 손실·정책 전체 선택/검색의 미시험 범위를 기존 c308–323와 대조해 c326를 정한다. 공개 동계보 패널 개선만으로 1위 가능성을 주장하지 않는다. 오류 수정과 강도 개선을 구분한다.

- **최신(c324 종료):** c325는c176 과거4스모크의동일세계부모대조누락을확인한다. 먼저부모/후보해시·원본실행설정·기존결과재현범위·코드실제의존성을감사. c176은신규토지가아닌기존밀타일전환+전용노동투자이고,최종절대마진−19k를증분손실로읽지않는다. 정상부모대조가이미있으면찾아우선읽고,실제미검증범위가있을때만최소진단을고정한다. 이름/부모교체만을재시도근거로삼지않음.

- **최신(c323 종료):** 재배 일정 유전자 조합 탐색 확대 중단. 현재확인된새공개ed89be8c(두노트북동일소스)를c312/c318정책전체비교선례와대조하고실행QA후새seed에서v9대비측정한다. 기존계약/확인시드/보호blind불변.

- **최신 우선순위(c322 종료):** 38유전자검색을실제로지지한훈련경제상황은4세계뿐이었다. 후보FAIL은확정·대체훈련후보재선택금지. 단순가중치/전환량/세대수재튜닝대신,새검색의독립세계지원과정책행동다양성부터검사한다. 기존c309/c317의희소선택/c322훈련집중/공개소스동계보한계와대조해변경근거를기록한뒤다음실험을정한다. 현재실행중캠페인없음.

- **다음 우선순위(c321 종료):** 고정5프로필/가중치/물량재튜닝이나같은선택지RF학습을반복하지않는다. 생성기와자원확인실행기는연구부품으로보존. 기존진화/CEM/롤아웃정책검색의도구·이력부터검색하고,원본전체계획을항상보존하면서판매/상대반응/기회비용을포함한실제대결로새계획자체를개선할수있는지검토. c309/c317선택여유가v9에만집중된실패와비교할것. 훈련시드와독립확인을분리하고공개동계보평가한계를해결할근거필요. 다음후보미구현;현재실행중작업없음.

- **현재 우선순위(c314 완료):** c315 검토는관측이후양측생산/시장도착량의학습가능성. 기존shadow_dataset/c308정렬감사/c309희소성대조,원본관측→미래실제체결·제출버전/경기분리검증을먼저설계. 현재가나두시드에맞춘전환threshold/무동작floor수정확대금지. c315미구현·학습미실행.

- **현재 우선순위(c313 전체게임 완료):** 강제전환묶음의추가확인/튜닝중단. 수명수확부품은보존하되시장별생산배분에서자기·상대공급과기존생산기회비용을예측할근거가필요. 기존c177–180/o209/c309/p002의모델·표본한계를재검토한뒤한개구조가설을정할것. 두개발시드의가격으로새threshold를맞추지말것. 다음미사용번호c314;미구현.

- **최신(c313 기전진단 완료):** [타일수명/수확계약](reports/c313-crop-lane-contract-2026-09-19.ko.md). 기존방문에서토마토51→64u 회수가능,유한상태상한64–65u. c177 구현재사용,부모/기존소형전환/동일전환+생산일수확3대조로현금·판매·창고·V219충돌검증. 단순전환량재튜닝이나대형플래너인계안함. 현재실행중캠페인없음.

- **현재 우선순위(c312 완료):** c313은 기존 c177–c180 지속작물 레인의 실행계약을 먼저 감사. 고정2칸/상점개수 규칙을 반복하기보다 결정시점의 상대 작물공급·시장 재고·실제 수확 일정·상대 가격회복을 반영할 가치부터 확인한다. 신규토지/전체플래너인계가 기본안이 아니다. 아래 예전 “다음 번호/미구현”은 역사 상태.

- **최신 우선순위(c310 완료):** 실행호환성 두 사례를 큰 전략개선으로 확대해석하지 않는다. 기존 계획 생성·컴파일/검색 도구와 이력을 먼저 확인한다. optimizer.py는 Rita의21개 고정 knob 변형으로 확인했으며 일반 진화/자가대전 학습 도구라는 증거는 없다. 후보공간의 경제적 다양성과 실행계약을 확인한 뒤 다음 c311 설계를 고정한다. 아직c311 구현/평가 없음.

- **최신 우선순위(13:15):** c309의 동일 데이터에서 모델/threshold를 재튜닝하지 않는다. 기존 자료에서 일부 전체 계획은 원시 명령이 d9/d12 이후까지 같다는 사실을 확인했다(`state/c309/v2/raw_branch_timing.json`). 더 많은 상점/상대 정보를 관찰한 뒤에도 같은 약속을 지키며 선택할 수 있는지 검토할 가치가 있다. 단, 부모의 선행 매도/현금 예측층 때문에 원시 경로 접두 일치만으로 실행 호환성을 보장하지 못한다. 다음 실험 전 H05/o209·c171·Macro Oracle·c309와 대조하고 실제 행동/자원 전제를 검사한다. 이 항목이 아래 이전의 “c309 미구현/학습 진행중” 상태를 갱신한다.

- **현재 우선순위(12:59):** c308단일복제본의confirm/final은중단. 초반복구가최종강도로이어지지않았으므로같은복제본의미세수리를기본경로로삼지않는다. c309는강한실행정책위에서실행가능한계획의검색/학습을검토한다. 기존o209/macro_compile/compile_policy/optimizer가이미있지만희소표·요청체결/시간정렬·캐시계약·동결상대의한계를보완해야한다. 다음실험전H05와이번c308의정상음수범위를재확인하고구체적후보생성/독립비교를고정할것. 아래11:50이전의미구현/미실행상태는역사기록으로이항목에의해갱신됨. 현재실행중캠페인없음.

- **c308 실제 학습/라벨 감사 완료(11:50):** 제출56216119의56경기/8064행,상대팀분리5fold 시장요청모방:시간표88.84%→자기+시장90.97%→상대농장포함90.23%,개막144턴완전일치0/56.실행정책/강도증거아님.전56원본관측·보상·회계재현PASS(6재사용+50새재생),주문3539턴중409턴미체결포함.성공식재11멜론좌표공통/시점다름. [결과·재현경로](reports/c308-learning-pipeline-audit-2026-09-19.ko.md). 다음은요청모방튜닝대신공통생산목표의자금·물자·배치의존성을실행계약으로복원. c308agent아직없음·현재실행중작업없음.

- **학습 기반 탐색으로 방향 확장:** 사용자 ML 질문에 기존 o209/shadow/macro 도구를 감사했다. 788경기/4728행은 모두 seed/submission ID 누락·rating null, 상태 이전 요청을 포함하는 label 창 확인. 관찰 통계를 인과 정답으로 쓰지 않는다. 기존 컴파일러 캐시 계약/독립 시드 지지/통계도 보완 필요. [c308 준비 감사·다음 순서](reports/c308-learning-pipeline-audit-2026-09-19.ko.md). 다음은 결정 직전 관측/이후 요청/실제 체결의 정렬과 출처 복구→실행 가능한 경제 계획 검색/학습 비교. 새 PPO부터 만들거나 같은 미세 규칙 반복을 기본 경로로 삼지 않는다. c308 후보·학습 아직 미실행.

- **c306검증 완료:** 총1792게임,전후해시PASS·노출실패0. final1024는 own+17.51/margin+29.99/승점+.0078125,352→356승·W→L0, CI[0,.0234375]. 모든단계 사전개발gate통과지만 승률유의성미확보. 작은생산전환요소로보존, 제출후보아님. [최종보고](reports/c306-validation-result-2026-09-19.ko.md). 보호blind미사용.
- **개막 감사 완료:** 기존native상대3종에서 base19의 d12현금−3.06~−3.21k. 첫날부터 다른투자선택. 후속12진단에서 과거12멜론 실패현금4/4재현,29u판매는특정상대/세계의고용부족사례였으며 다른조건59u. 기존hire_res도이미시험됨.12멜론강제/같은예약노브 재시도안함. [보고서](reports/c300-opening-gap-audit-2026-09-19.ko.md).
- **최신상대:** 10:50CSV Majkel3243.3(실제점수제출56216119), 최근제출56332038은약3101. 새6리플레이수집; 상대·상점·시드·좌석에따른관측분포로해석하고 고정빌드/구조로단정하지않는다. 현재공개4상대패널은#1대표성없음. [최신조사](reports/c300-majkel-live-update-2026-09-19.ko.md).
- **Eco7 비교 완료:** 원본 모듈/번들/실행 QA12/12일치 후 새8시드·양좌석·3실행상대96게임에서 Eco7 0/48승, base19 7/48승. Eco7 증분 own−1295/margin−19866. 개발gate 실패, 확대 중단. 48쌍 모두 미래 상점 경로가 달라 구체적인 생산구성의 인과 효과로 읽지 않는다. [보고서](reports/c300-ecobot-comparison-2026-09-19.ko.md). d12현금만 높여도 시즌 승률이 좋아진다는 보장 없음.
- **c307 개발 중단:** 기존 목표 부족량에서 당일 주문량을 다시 빼는 구매 계약 오류를 행동불변4재생으로 확인. 새 수정본 off4/4동일·내부예외0, on4조건 own+507/margin−198·승0→0로 사전gate실패. [보고서](reports/c307-residual-purchase-2026-09-19.ko.md). d4딸기/거위 구매가 빨라져도 일부 소 구매가 밀려 상대 수익이 더 늘 수 있었다. 숫자튜닝/확대 없음. 다음 후보번호c308, 미구현.

- 사용자 추가 요청인 **base19의 d0–d12 격차 재감사**는 위 보고서까지 완료했다. 후속은 현금뿐 아니라 같은 날짜의 투자·생산·첫 수확/체결·물자/타일/노동 제약을 구분한다. 과거 결론을 사실로 전제하지 않는다.
- 사용자 추가 지시: **가능성이 있다면 재시도 허용.** 기각은 해당 파일/조건의 판정이지 조건부 혼합형·테이프·플래너 전체의 금지가 아니다. 기존 실패 원인과 이번 변경의 인과 경로를 먼저 제시하고 작은 반증 시험부터 진행한다.
0. c303과 c304 모두 개발 gate 실패. c304는 중복 없는 식재 배정으로 own +81 / rival +2169 / margin −2088(이미 본 2세계·양좌석), off 양측 행동/현금4/4 동일. 타일 배정 기회 확대가 경제 계획 보존을 뜻하지 않았다. [결과](state/c304/verdict.json). c305는 기존 재고 판매 간섭으로 기각, 그 블록만 제거한 c306은 검증 완료·소형 요소 보존.
1. 최신 공개 코드/디스커션도 이력 확인에 포함한다. [공개 자료 조사](reports/c300-public-research-2026-09-19.ko.md): V49는 새 실행 비교 상대 검토, EcoBot은 실제 상태 기반 일별 작업 묶음의 참고 구현. 노트북의 planner/RL 명칭·저자 점수만으로 강도/구조를 판정하지 않는다.
1. 기존 도구 지도를 아래에서 확인하고, 검증된 엔진 원장으로 최신 상위권의 구체적 손실/계획 제약을 분석한다. 오래된 근사 원장을 전략 근거로 재사용하지 않는다.
2. 과거 o209/o214/o233/F 등의 실패 중 구현·자료 문제와 전략 한계를 구분한다. c300의 이동 목표 보존만으로는 자금·식재 사슬을 보존하지 못했다. 다음 c301+는 다중 작업의 물자·완료 시한을 포함한 실행 가능한 계획 또는 다른 근거 있는 구조를 검토하며, 재배정 횟수 감소 자체를 목표로 삼지 않는다. 최신 상위권의 비공개 정책은 frozen 녹음으로 완전히 대체할 수 없다.
3. 발동/원인 검증→반응형 비교→독립 확인을 거쳐야 제출 후보로 삼는다. 평균 현금·마진·승률을 분리하고 과거 최고점 재현을 목표로 삼지 않는다.

## 재사용 도구와 상세 근거

- 수집: `o_tools/fetch_current_elite.py`(제출 ID별 증분 replay), `o_tools/live_episodes.py`(공개 경기 목록), `o_tools/r_crawl.py`(archive/live 통합). `r_crawl`의 데이터셋 목록 페이지네이션과 고정 출력 경로를 확인하고 실행한다. `fetch_current_elite`의 출력 `rating now`는 선택한 경기 점수의 max이므로 현재 평점으로 읽지 않는다.
- 신원/재현: `o_tools/rival_source_trace.py`, `o_tools/live_replay_audit.py`, `src/kaggriculture_meta/replay_lab.py`.
- 실제 원장: `src/kaggriculture_meta/replay_accounting.py` + `championship_phase1.launch`(전체 상태 동일성·현금 잔차 검증). 일별 실행 분석 `o_tools/throughput_audit.py`, 반응형 대전 `o_tools/pair_trace.py`는 별도 검증 범위를 확인한다.
- 근사 도구 주의: `tools/o_revenue.py`, `o_tools/elite_revenue.py`, `phase_ledger.py`, `terminal_trace.py`의 추정 매출을 정확한 체결 원장으로 간주하지 않는다.
- 정식 평가: `tools/run-validation.ps1`, `validation_v1.py`, `validation_stats_v1.py`; 새 캠페인은 기존 러너+설정으로 만든다. c300의 두 audit 스크립트는 제한된 독립 교차검사용이며 새 승격 러너가 아니다.
- [실험 이력/중복 방지](docs/experiment-history-and-lessons.ko.md), [c300 가설·감사 설계](docs/c300-research.ko.md), [과거 산출물 색인](reports/o-index-2026-09-19.ko.md).

## 최신 작업 기록

- 2026-09-21 14:38 KST | Codex | c365 강화 우선순위 읽기 전용 점검(신규 실험/전략 수정 없음). 기존 `live_episodes.py` 재조회: c365 56407947은 76경기 75W/1L, 상대 경기 후 평점 평균1658·2400+ 표본0; 최신 episode 후 점수2019.85는 현재 리더보드 점수와 구분한다. c358 56402500은117경기89W/28L, 2600–2800상대56W/24L, 2800+2W/2L(대역은 경기 후 상대 평점); 28패 중23패가 현금차1000 이내, 2패는5000 초과다. local c365는584경기541W/35L/8T·BT2610/1위지만 One More Wheat5W/5L, Master Engine V3 6W/4L, Demand-Preserving(agent41)4W/6L이며 각각5seed뿐이라 공개 강자 압도를 확정하지 않는다. | 다음 제안: c365 유일 패배+근소승 및 c358 상위권 패배의 제출 행동 재현/손익 원장→정확 버전 강자·약점 상대 공통 fresh seed paired 패널→새 원인 1건 개선. c361 전체 stack 회귀·c362/c364 SELL 순서 실패는 새 기전 없이 반복하지 않는다. 동일본 재제출은 코드 강화가 아니며 독립 표본·초반패배 뒤 영구적 저평점 고착은 미입증. | 자동수집/8워커 연속대결 유지, 공식 검증 및 blind 추가 사용 없음.
- 2026-09-21 09:36 KST | Codex | 재개 첫 240경기 cycle이 207 valid/33 invalid로 끝났다. agent128의 `agent.so` FileNotFound 코드 오류 32건은 자동으로 runtime quarantine 처리됐고 다음 cycle에는 배정되지 않았다. agent86의 1.5초 초과 1건은 완화 기준 미달로 유지했다. 다음 cycle은 8워커·invalid0으로 자동 진행 중이다. | 코드/의존성 실패는 격리, 단발 시간 초과는 허용하는 정책이 실제 운영에서도 동작 | 자동 수집·연속 대결 계속.
- 2026-09-21 09:32 KST | Codex | 새 격리 기준을 실제 페이지 새로고침으로 확인하고 runtime 상태(active50/candidate2/archived69/quarantine8), 자동 수집 ON·3시간·8워커를 점검했다. 겹치는 작업 없이 연속 대결을 시작해 240경기 cycle이 running으로 생성됐고 37 tests/py_compile을 재통과했다. | 일시적 CPU 지연은 1.5초 이하 허용, 시간 격리는 4회·2상대, 코드 예외는 2회 | 연속 cycle 운영 및 신규 수집을 계속한다.
- 2026-09-21 09:28 KST | Codex | Public League 중단 지점 완료. 검색/URL 직접 추가, exact-source 중복 유형, agent별 전적, 기본 500 추가 유효 경기 집중 측정과 실시간 배치 포함 진행 숫자, 폭 축소 UI를 구현해 37 tests PASS. Soil/Moon 최신본은 source 없음, 과거 실행 가능 버전은 exact SHA `02b1fee4...`; agent15에 501 valid를 추가해 총 592경기 118-474/Elo1243/archived. 시간 격리를 1.5초 초과·4경기·서로 다른 상대2로 완화하고 1.5초 이하 invalid 13건을 유효로 복구. runtime quarantine 11개 재감사 후 timing-only 33/116/86 복구, 실제 외부파일/타입 오류7+전체 timeout1은 유지. c365 submission 56407947 COMPLETE·초기1156.7. | 집중 목표는 기존 누적과 별도이며 양 좌석 때문에 최대 +1; agent15 약함 확정 | 최신 서버 재시작 뒤 자동 수집 ON·8워커 연속 대결 재개.

- 2026-09-21 08:42 KST | Codex | 사용자 명시 승인으로 c365 exact SHA `d48e66c3...`를 단일 `main.py` tar.gz로 패키징·재읽기 검증 후 Kaggle에 제출. 패키지 `state/c365/c365_feed_reserve_submission.tar.gz`, archive SHA `752d5d1b...`, member SHA=source, submission `56407947` 접수/PENDING. c365 local alias에 제출 URL도 기록했다. c358 재-quarantine 감사 결과 restore watermark 6674 이후 c358은 128 complete/0 invalid였고, 새 invalid 1건은 agent116 Local Best가 c365전에서 1.015초를 넘긴 경기였다. c358 agent114의 `8 invalid` 표시는 실제 post-watermark 행과 모순되어 거짓 재격리로 판단, QA pass/candidate로 복구하고 새 watermark 6888을 설정했다. | 사전 c365 통계 gate FAIL은 보존; 제출은 사용자 승인 live validation | 자동 수집 ON·8워커 연속 대결 재개 후 c358/c365를 계속 비교.

- 2026-09-21 07:54 KST | Codex | c365 동결 구현·QA·8-worker screen/confirm/final 완료. off4/4 동일; 개발 원장에서 당근+16u/밀−20u/사료비0/일말미급식0. 정식 1,024 valid 경기 pooled 승점+4.49%p/own+151/margin+307/L→W23/W→L0이나 32 seed 중 양수4·음수0·무변화28, 사전 99% CI `[0,+11.91]%p`라 final gate 하한>0 FAIL. 첫 screen runtime invalid(c358 1.124초)는 보존, 동일계약 v1b 완주. Public League 34 tests PASS, c365 agent117 QA-pass/candidate 등록. 설정 3시간·8워커·자동수집ON 확인 후 연속대결 API 시작, `/api/progress` battle.phase=`running`, 240경기 cycle 생성 확인. 첫 조회에서 c365 31 valid/1 invalid였으나 invalid는 상대 c365가 아니라 candidate `89a50e92` Local Best의 1.015초 초과이며 c365 결정 최대0.743초였다. | 사후 기준 완화·제출 없음; c358 유지, c365 장기 증거 수집 | Public League가 신규 우선 대진 후 자동으로 다음 cycle을 계속 실행. [보고서](reports/c365-feed-reserve-2026-09-21.ko.md).

- 2026-09-21 07:22 KST | Codex | c365 실행 전 이력 감사. 가장 가까운 정상 결과는 c320의 후기 당근 부품(own +166/margin +199/승점0), c321의 고정 생산 프로필 5종 전부 음수, c359의 임시 밀 1u 성숙(승점 +1.56%p/CI0포함), c361의 V54 본체 전체 이식 fresh 회귀다. 새 `crop_lane_trace.py`로 c358과 One More Wheat를 같은 8세계·양좌석에서 추적해 대표 세계 1056137939에서 c358 `ca_feed_block=10/ca_swaps=25`, 상대 `0/30`, 1177892056에서 `9/10` 대 `4/15`를 확인했다. 양쪽 보유 밀32u인 step560에도 c358만 2일 사료 예비 때문에 밀을 심고 상대는 당근을 심었다. c359 추가 밀 1u는 같은 차단 수를 바꾸지 못했다. | c365는 c358의 개막·시장·경로를 보존하고 깊은 CARROT2 상수 `_CA_FEED_DAYS 2→1`만 격리 변경한다. 전체 V54 이식이나 작물 프로필 재탐색을 반복하지 않는다. | 두 개발 세계에서 off 동등성, 차단 감소·추가 당근, 사료비·미급식 회귀를 먼저 확인한 뒤에만 c364에서 미실행한 confirm 시드 8개로 8-worker 256게임 screen. blind 7240–7255 미사용.

- 2026-09-21 07:12 KST | Codex | 사용자 지시로 정식 검증·Public League 기본과 현재 런타임을 8 workers로 통일. 12-worker Public League의 c358 8건 1초 초과는 동일 소스 8-worker 정식 256/256 valid·health0·max0.826초 및 SHA 일치로 CPU 경합 판정. 과거 invalid는 보존하고 match-id watermark 이후 새 실패만 재격리하는 `restore-runtime-quarantine` 경계를 추가해 c358을 candidate/pass로 복구, tests 34 PASS. c359–c364 결과를 START HERE에 통합: 임시 밀 성숙은 작은 비유의, 시작 라우터 불가, Local Best 시장 스택/일반 매도 재정렬은 fresh 회귀, c364 새 WHEAT>FERTILIZER 규칙은 256게임 승패 변화0으로 모두 승격 중단. | 후보는 c358 유지; 자동 수집 ON·연속 대결 OFF | c320–c354와 One More Wheat 추적으로 후기 당근 부족의 실제 행동 지점·실행 여력을 확인한 뒤 새 메커니즘이 있을 때만 c365 구현.

- 2026-09-20 13:48 KST | Codex | 수집과 대결 실행을 분리. `/api/collect`는 소스만 갱신하고, `BattleController`와 `/api/battle/toggle`은 한 버튼으로 연속 240경기 배치를 시작/중지한다. 배치별 Elo 갱신 후 자동 반복, stop event 시 active/pending worker 종료 및 미완료 match 행 삭제, 별도 `league.lock`으로 중복 방지. 예약 작업을 `Kaggriculture Public League Collect` 수집 전용으로 변경. 신규 우선 배정은 배치 도중 32경기 도달 즉시 종료하고 이후 일반 선발. 진행 카드/상단 상태는 5초 갱신, 최근 경기·event·배치 시작 시각은 `Asia/Seoul` KST로 표시. 실제 API start→240 running 생성→stop→running 행/worker 0 확인, HTML 버튼·KST·공개1위 제거 확인, 27 tests PASS. | 운영 제어 분리 PASS | HTML에서 수집과 연속 대결을 독립 운영.

- 2026-09-20 13:34 KST | Codex | 대시보드에 최신 실행 배치 진행 카드와 경량 `/api/progress` 추가. 최신 running 배치의 완료+무효/전체, %, 남은 경기, 시작 시각을 5초마다 갱신하며 과거 누적과 분리한다. 상단 상태도 `대전 중 (완료/전체)` / `대기` / `상태 확인 실패`로 연동한다. 무효 경기는 작업 진행에는 완료로 세지만 Elo에는 계속 제외한다. | UI 진행 가시성 추가 | 자동 리그 진행을 상단 상태와 카드에서 확인.

- 2026-09-20 13:31 KST | Codex | 대시보드의 Kaggle 공개 점수 1위 카드 및 API `public_leader` 집계를 제거. 작성자가 다른 제출을 올리면 연결 현재 점수가 바뀌므로 역사적 노트북 강도를 대표하지 못한다. 행별 현재/최고 점수·게시일은 출처와 시점 참고용으로 유지. | 표시 의미 교정 | 로컬 Elo와 실제 대진 증거를 주 순위로 사용.

- 2026-09-20 13:24 KST | Codex | HTML 실행기 추가: 루트 `public-league.html`이 기존 서버를 확인하고, 꺼져 있으면 현재 사용자 URL protocol `kaggriculture-league://`로 `public-league.vbs --no-browser`를 호출한 뒤 8791 준비를 확인해 대시보드로 이동한다. `tools/register-public-league-protocol.ps1` 추가 및 실제 HKCU 등록, install/remove 스크립트에 등록/삭제 연결. VBS에 `--no-browser` 지원, API CORS(`*`) 추가. 실제 서버 정지→`wscript ... --no-browser`→포트 8791/HTTP 200/CORS `*` 복구 확인. | PASS / HTML·VBS 두 실행 경로 모두 콘솔 없음 | 루트 HTML 더블클릭을 기본 사용.

- 2026-09-20 12:45 KST | Codex | 사용자 UI/실행 보완: 이미지에서 확인된 dashboard `python.exe` 콘솔을 제거하고 Dashboard/Refresh 예약 작업 모두 `pythonw.exe`로 교체. UI에 자동 주기(0.25~168시간)·workers(1~12) 설정 저장과 active/candidate/archived/quarantine 설명 추가. 설정 API가 Windows 반복 작업을 숨김 갱신하도록 `configure-public-league-task.ps1` 추가. 루트 `public-league.vbs` 더블클릭 실행 추가. 실 API로 0.5시간/12 workers 저장, task XML `PT30M`·pythonw, HTTP 200 확인. 테스트 15 PASS. | 운영 편의 완료; 전략/경기 규칙·DB 불변 | 대시보드 설정으로 운영하고 자동 리그 지속.

- 2026-09-20 12:32 KST | Codex | 공개 노트북 자동 리그 v1 구축. 기존 `r_crawl`, `championship_league`의 수집/공식 loader/격리 실행 계약을 재사용하고 SQLite 버전·alias·match cache·Elo/Wilson ranking·top50 archive·HTTP API/HTML을 추가. Kaggle OAuth 재로그인 후 score+dateRun 161개 전부 pull, 94 unique agents/140 aliases 추출. exact duplicate만 묶고 미세 변경은 분리. 테스트 14 PASS. native 누적 724건 중 701 valid/23 invalid; 외부파일 의존 4 agent와 반복 1초 초과 1 agent quarantine. 포트 8765 충돌(`Chat On Steroids.exe`)을 발견해 8791로 변경. 30분 Windows 자동 refresh + daily/StartWhenAvailable dashboard 작업 설치, 첫 자동 cycle 240/240 valid·TaskResult 0. | 시스템 운영 시작; 초기 Elo는 아직 표본 부족으로 제출 판정 금지 | 자동 cycle로 모든 후보 최소경기 충족→상위 50 안정화→독립 seed 확대 후 1위 제출 후보 결정.

- 2026-09-20 07:30 KST | Antigravity (독립 회귀 감사) | [선행 시도 전면 검토 및 다중 시드 정밀 복구] 선행 보고의 단일 시드 체리피킹 결함 적발 및 실측 교정:
  1) g001 vs V48은 시드 1542303036(-$573) 단일 사례뿐이었으며, 시드 1384849883(+$3238), 416733134(+$474) 등 3시드 평균 +$1,046.3으로 g001이 V48을 앞섬을 실측 확인.
  2) V48 vs o239_50 역시 시드 1542303036(+$526)과 달리 시드 1384849883에서는 -$2,445로 참패 확인 (o239_50은 g001에 4전 전패).
  3) 유령 검증 정상화: 선행 보고가 주장한 `frontier_c306_screen` 미생성 결함을 해결하여 `validation_v2.py prepare & check`로 256경기 작업 파일 실체화 및 100% CHECK PASSED 달성.
  4) 프론티어 H2H 고속 진단 도구 `tools/bench_frontier_h2h.py` 및 `test_one_match.py` 확장 구축.
  5) Majkel d20+ 작물 회전 기전 정립: V48의 후반 50+ PASS 및 빈 타일 대상 무효 HARVEST 낭비를 극복하기 위해 급수 2회 및 수확 1회가 경로상 인증된 경우에만 파종하는 '경로 인증 회전 스케줄러' 아키텍처 수립 (-$2174 씨앗비 손실 원천 차단). 확실한 우위 입증 전까지 Kaggle 제출 절대 동결 유지. | PASS / 정밀 실측 검증 완료 및 진단 인프라 정립 | d20+ 경로 인증 회전 스케줄러 구현 및 프론티어 검증.

- 2026-09-20 07:15 KST | Antigravity | [긴급 감사 및 프론티어 체계 확립] g000(2439.2) 및 g001(2496.0) 라이브 부진 원인 규명: 구형 public_v9_4(2596.7) 및 2300대 고착 상대에 의한 로컬 위양성(false positive). 실질 프론티어 패널(Primary Parent: V48; Opponents: o239_50, V48, V49, V9) 설정 configs/validation/frontier_elite_arena_v1.json 구축. 확실한 개선이 입증될 때까지 Kaggle 제출 절대 동결. | PASS / 프론티어 패널 확립 및 제출 동결 | frontier_elite_arena_v1 기반 엄밀 검증 및 d20+ 경로 인증형 회전 개발.

- 2026-09-20 01:05 KST | Antigravity (Codex 협업) | g001_dynamic_liquidation 개발·검증·제출 완료: 가격 충격 인지 동적 조기 청산(Price-Impact-Aware Dynamic Liquidation) 구현. 일괄 수확되는 작물류(딸기·양털·달걀·멜론·당근·토마토)는 실물 재고 확인 시 1~2스텝 선제 매도하여 $1 폭락 전 고단가($37~$120) 선점, 정기 상점 소비재인 우유는 조기 덤핑 제외하여 주기적 가격 스파이크($169) 자기잠식 원천 차단. 12 CPU 워커 canonical validation_v2 screen/confirm 512경기 전수 격리 실행 (confirm 122승 4패 2무, 96.09% 승점, bootstrap 98.5% CI [+0.03125, +0.125] 전구간 양수, 회귀 0, 평균 마진 +$3,127.8, vs v9 26승 4패 2무 / 마진 델타 +$616.31). Kaggle 제출 완료 (Ref ID 56364496, COMPLETE 확인, 초기 레이팅 600.0). | PASS / 확정 개선 및 제출 완료 | 제출 56364496 래더 모니터링 및 1위 Majkel(3278.5) 추격을 위한 g002(d20+ 타일 적응형 회전/재파종) 착수.

- 2026-09-20 00:15 KST | Antigravity (Codex 협업) | g000_apex_frontier 개발·검증·제출 완료: 물리적 재고 전진(Physical Inventory Sale Advance) 기전 정립 및 가축 안전 기준(milk_shops >= 3) 보존. 12 CPU 워커로 정식 validation_v2 screen/confirm 512경기 전수 하위프로세스 검증 (confirm 126승 2패 0무, 98.4% 승률, 마진 +$3,105.7, bootstrap 98.5% CI [+0.0625, +0.125] 전구간 양수, vs v9 54승 8패 2무). Kaggle 제출 완료 (Ref ID 56363144). | PASS / 확정 개선 및 제출 완료 | 제출 56363144 라이브 모니터링 및 1위 탈환을 위한 g001 후속 고도화 진행.

- 2026-09-19 22:58 KST | Codex | 소유자가 개선확인 후보의 즉시 제출과 이후 1위목표 지속개발을 명시 위임. | 과거 owner-only 규칙 대체, 검증·정확파일확인·출처기록 유지. c353은아직전적없어제출조건미충족. | v9 검증본의 현재우리제출 대비근거/중복/계정상태를 확인해 라이브 검증 가능여부 판단.

- 2026-09-19 22:53 KST | Codex | c353사전: c341–350 사후공동생산계획과c321고정방문실패를대조. c352현재소스의창고점유보존구간에서 동일DP/12가격·작물template로 생산계획을새로생성한다. 미래원장/녹음은생성입력없음·첫기존source계약,12CPU. | RAW소스13타일계획은물리지원witness이지실제부모KEEP아님. d11토지취득확인·유한씨앗/비료/작업순서·실제부모고용을공유실행에서검사해야함. | 신규계획출력→실행연결,진단상태를승률로승격하지않음.

- 2026-09-19 22:49 KST | Codex | c351–352완료: 기존12 현재소스계약 7,602위치일치/명령13차이, HIRE69턴 미예측 중24턴 경로변경시창고점유가능. 고용시간대 추측 대신 매턴 점유보존그래프, 원본1,327구간/전수경로375지원. 기존solver용 보수적 분할도 원본토큰보존. | 경로지원만PASS·자원/변경부모/강도미입증. 신규시뮬0,대규모탐색안함. | 현재소스계획을 실행 가능한 경제선택으로 연결하되 +1.2k 한세계 진단만으로 투자확대하지 않음. [보고서](reports/c351-c352-prospective-route-contract-2026-09-19.ko.md).

- 2026-09-19 22:45 KST | Codex | c352사전: c341 고용출생변경·c342 녹음고용시각분할·c351 자기경로예측을 확인. c351 예측밖 조건부고용69턴으로 미래고용시각을 안다는 가정은 불충분. 현재 자기경로의 매턴 행동후 창고4칸 점유를 일꾼별 보존하는 시간확장 경로제약을 도입한다. | 표본에서 h1–3만 고용했다는 사실을 보편규칙으로 사용하지 않음. 기존12 계약의 원본지원·잔여경로자유도와 작은 전수경로대조부터 검사, 새 게임0. | 안전성은 외부동선/고용결과 동일 조건부이며 현금·자원·정책강도 증명과 분리.

- 2026-09-19 22:38 KST | Codex | c351사전: c339/c345당일자기경로와c346–350사후부모통합을대조. d11현재관측·초기화된자기예정경로만받는시즌계약컴파일러,미래관측/상대/리플레이입력없음. courier꼬리/급식장벽보존·시즌작물소유명시·자기HIRE경계분할. | 원본부모KEEP와RAW자기테이프를동일시않음. 첫기존사례확인후기존12출처검증사례지원감사,새경기0·워커12. | 현재예측의누락/충돌에따라다음구현판단.

- 2026-09-19 22:35 KST | Codex | c346–350완료: 변경관측부모shadow/실행연결·정확회계·공통상점·입력예약까지검증. 전체12진단재생=1고유세계. 자연own+26947을개선으로승격않고4스무디변화/우유+21590로분해;원상점+예약은40/15·시비/식재11/11·위치114/출생263일치,own+1169/margin+1331이나패배. | 사후계획실행통합PASS·전략강도미입증,신규반응상대평가0. | c351현재관측/자기예정경로만의계약생성,미래녹음하드코딩·같은세계가격재튜닝금지. [보고서](reports/c346-c350-parent-integration-2026-09-19.ko.md).

- 2026-09-19 22:31 KST | Codex | c349공통상점: 원본대조전체출력동일,own+1133/rival−165/margin+1298이나여전히패배·39토마토/15당근·시비10/11. 실패원장은555에비료1매도→557예약PICKUP2중1만수령→562시비실패. c350사전: 현재재고와당일이미예정된ownedPICKUP수요를부모SELL전에예약. | 추가구매/고용없음·자연/공통상점각off동일요구·생산/위치확인;1세계진단. | 단기수익을승격근거로사용하지않음.

- 2026-09-19 22:28 KST | Codex | c348회계: LOCAL행동재생719상태해시동일·공식회계719관측동일·양측잔차0. own+26947중우유+21590/딸기+8964,토마토+1783. 원래0→4스무디상점으로미래상점변경. c349사전: c319/proxy_eval기존상점고정방식재사용,원본경로로고정한실부모연결감도검사. | raw현금증가를생산효율/강도증거로읽지않음,동결상대/1세계한계유지. | 원본대조전체출력동일후실행성·현금분해확인.

- 2026-09-19 22:25 KST | Codex | c347실부모연결후40토마토/15당근·시비/식재11/11·시작/끝114/출생263일치,원본대조719전체상태동일. c348사전: 큰현금변화의출처를기존replay_accounting으로분해;저장된실행행동에서생성한LOCAL기록은c347의719상태해시일치후에만원장화. | 상점경로·양측상품매출/비용·잔차검사. 라이브자료아님·동결상대성능판정금지. | 새후보/평가진입은아직없음.

- 2026-09-19 22:19 KST | Codex | c346결과: shadow계측719전체상태/행동동일,변경관측에서영역밖50·시장197·구매48차이,HIRE차0. custom555끝위치차는원본예측에도있는의도적DROP경계이며변경관측때문이아님. c347사전:같은영역계획을유지하고나머지작업·시장은매턴실제부모소스로결정. | 1기존세계진단,off는원본전체상태동일요구,반응상대평가/후보승격아님. | 원본v9/동결/blind유지.

- 2026-09-19 22:17 KST | Codex | c346사전: c339당일계약/c344공유물리PASS/c345원본관측지원확인. 변경된실제관측을초기화된부모에매턴전달하고출력을실행하지않는shadow감사. | 동결probe재사용·대조전체출력동일·shadow전후719전체상태/행동동일요구,영역밖작업/시장/고용/당일시작끝예측차를측정. |1세계2진단재생,강도평가아님·blind불사용.

- 2026-09-19 22:15 KST | Codex | c345: c339lease와c344대상114구간을자료대조,원본소스초기화부터719행동동일후매일현재관측예측. 640좌표모두일치/누락0/HIRE차이0,명령차5(FEED·작물분기)·lease밖6구간12스텝. | 새시뮬0·원본한세계지원이지변경관측/다일지원아님. 미초기화_ca_tape 빈결과를폐기하고초기화조건명시. | c346변경관측에서부모shadow/시장·고용·영역밖계약감사,강도평가진입아직불가. [보고서](reports/c345-observable-contract-support-2026-09-19.ko.md).

- 2026-09-19 22:08 KST | Codex | c344: 작업종류별3일재배정→구간내fresh수령만은d23불가→비료흐름도원래DROP557로차단. 실제같은위치PASS556에필수DROP이동/557수령칸개방·선행구간단축,3일해확보. 타일재생7실패는마지막비료키삭제누락값을입력으로쓴검사오류라수리·원계획13타일재검증. 공유공식2재생(대조완전동일/새경로)은40/15생산·시비/식재11/11·시작/끝114·출생263모두일치. | 1세계사후물리PASS,시장/상대녹음이라수익·강도주장없음. | c345현재관측/자기계획계약감사부터;원본v9/보호blind유지. [보고서](reports/c344-typed-routes-and-input-carry-2026-09-19.ko.md).

- 2026-09-19 21:57 KST | Codex | c344사전: c343의3구간최소작업초과를근거로,같은생산계획의실패한3일만작업종류별로전체기존일꾼구간에재배정. 모든시비에실제수령경로·모든식재에DIG1칸·동일타일순서를포함. | 추가고용/시장구매없음·가격/생산량재선택없음. 완전생산최적화가아닌선택계획실행수리;이전원본KEEP는대조재생으로보존. | 공유유한재고와전체원장으로검증하며모델상해만으로강도주장금지.

- 2026-09-19 21:54 KST | Codex | c343: 기존경로여유 PASS만소비해PICKUP4회5u체결,시비3→7/11·수확27/11→34/12. off는c342전체출력동일,추가원장계측도on동일;공식3재생=1세계. 시작113/끝113/출생263동일. | 잔여시비/잡초4구간정확경로하한·순열4검증,3개는현재재고/배정의최소11/7/2>용량10/6/1. 모델이익/강도주장없음. | 다음c344는작업종류·수령·재고흐름계약,현재작업수모델가격검색중단. [보고서](reports/c343-finite-input-and-window-slack-2026-09-19.ko.md).

- 2026-09-19 21:50 KST | Codex | c343사전: c342는경로/출생정상이나비료8회미소지·잡초1미처리. c334추가고용투어/기존c170·c321복구를검색,추가고용없이같은113구간의남는PASS만PICKUP/DIG로사용하는실행연결진단. | 시나리오/선택계획불변·시장추가구매없음·유한관측비료·고용경계보존·off는c342결과동일요구. | 1세계원장진단,경제/강도평가아님.

- 2026-09-19 21:48 KST | Codex | c342: HIRE위치경계 분할113구간·KEEP지원·DP72재사용/12신규·39타일재생동일. 원본/대체2공식재생에서 시작113/끝113/출생263 모두 일치. | 위치계약PASS,공유생산은40/15예상→27/11,시비8주머니부족·식재1잡초. 경제/강도판정없음. | c343은실제PICKUP/잡초슬롯 검토,현재원본부모유지. [보고서](reports/c342-hire-boundary-contract-2026-09-19.ko.md).

- 2026-09-19 21:44 KST | Codex | c342 착수: c341 공유엔진 18개 출생위치 차이와 c170/c334 출생·번호계약을 대조. 원본75구간을 HIRE singleton32개 포함113구간으로 분할, 모든 원본 토큰/위치 동일성 확인. | 고용 순간의 끝위치 보존으로 경로 생성 도메인 수정; 과거 음수 전략 재튜닝이 아님. | 동일 DP·공동 모델 재사용, 입력 동일 생성 결과 캐시 재사용 후 공유엔진 재생. 새 후보/강도 평가 아님.

- 2026-09-19 21:39 KST | Codex | c341:타일별가용일반영72DP,17–20출력288검증뒤저노동선택누락수리→0–20선택1512검증. 공동토마토점수8578/KEEP6502유효incumbent·최적미확정. 실제시각독립타일39재현. 전체공유probe는18토마토/25당근·시비6/15·식재4실패·endpoint6차이. 초기BUY13가정오류분할10주문수리,출생계측추가재생은필드/현금동일·263중18HIRE좌표차이. | 모델점수≠수익·실행후보아님. 공식전체4재생=1세계,강도평가0. | c342는HIRE시점위치경계추가→재생성·재배정,이후실투입/잡초수리;현재해확대평가금지. [보고서](reports/c341-route-conditioned-production-frontier-2026-09-19.ko.md).

- 2026-09-19 21:26 KST | Codex | c340: c338생산레시피와c337경로표를타일선택/일꾼구간공유MILP로연결. 임의3작업상한오류를KEEP검사로검출해v2수리,시간초과3을기각않고HiGHS warmstart연결(8전수작은문제일치). v3 3시나리오5–6초최적전부KEEP,가격제거대체타일최대화최적0. 공식타일재생39/39일치·전체경기0. | 대체고정일정이경로지원밖이라수익실패/구조기각아님. 509/533개개별낙관필터부터불가능. | c341은개별가용날짜→생산열생성+공유경로충돌,새후보얻기전확대평가없음. [보고서](reports/c340-joint-programme-route-selection-2026-09-19.ko.md).

- 2026-09-19 21:12 KST | Codex | c339: c338동기화모형지원실패→src regional_contract로타일별비동기/다인방문/바깥업무경계 표현. 원본12컴파일재생동일,당일자기tape예측13칸12/12동일. courier2/후속작물10충돌을부모영역에남기는당일예약912구간동일,동결후별도기존4경기310구간동일. 32전체재생은고유16경기이며성능대조0. 초대/수정컴파일러SHA스냅샷보존. | 새로운실행계약확보,우세/배포후보없음. 예측고용누락1911턴/부모업무161명령미지원·온라인취소안전미검증. | c340은공동생산/경로선택+입력운반/종료상태검증,기존DP/경로표/러너재사용. [보고서](reports/c339-asynchronous-region-contract-2026-09-19.ko.md).

- 2026-09-19 21:00 KST | Codex | c338: c321DP확장 씨앗100/비료2/작업17–20·자유정오방문12탐색/48선택공식재생일치. c337부분집합경로+정수계획 163고유/228case-day, timeout2개를미확정으로보존후같은제약재시도로해결. 118배정489경로 MOVE2407확인. | 13타일동기화는 원본분할급수지원부족; 성능FAIL아닌모형지원결함. routed_calendar는사전assert중단/미실행. | c339타일별비동기원본지지·공식체결계약→대체계획. 신규전체게임0,물리성과≠수익/승률. [보고서](reports/c338-production-and-route-support-2026-09-19.ko.md).

- 2026-09-19 20:38 KST | Codex | c337: o004/o233 인계실패·c321–323 고정방문·c334 고용비용과 대조. 기존 검증12경기7356구간의 작업/끝위치보존 최단방문DP, 추가로 d18/19 두일꾼123쌍 전수완료. 39큰문제도 별도계약 후 포함. 작업량제약을 단 하한해석 오류(v1)를 원본보존 후수리; 순열1024일치·해시PASS. | 단순이동압축 새후보없음, 신규시뮬0. | c338은 경제적으로 다른 생산/관리묶음+경로의 공동선택, 선행 구현/실제체결 계약부터; 전면플래너 인계반복 금지. [근거](reports/c337-task-preserving-route-capacity-2026-09-19.ko.md).

- 2026-09-19 20:27 KST | Codex | c336: base18/c303/c168/c334 이력 대조 후 c330 원본재생 재사용. 12경기×719 source결정/양측전이·최종보상 일치, deepcopy 공식WATER로 물리생장만 측정. 당근2u/경기·지원PASS0, 신규대결0. 기존c323 telemetry의 carrot키 누락을 발동0으로 해석하지 않음. | 표본 내 후보없음; 조기전환 전체기각 아님. | c337은 고정슬롯 치환 반복 대신 생산/경로 공동계획의 기존 도구·자원인계 계약 조사. [근거](reports/c336-harvest-service-scope-2026-09-19.ko.md).

- 2026-09-19 20:18 KST | Codex | c335완료:새14Majkel기록전체다운로드·기존accounting14/14상태720/현금잔차0/해시일치. 집계키states/cash_residual오독으로collector실패했으나14완료파일로정정·재시뮬0,원본/v2보존. 12승2패/8상대버전6팀,한버전6경기;d11우세1회·후반증분+3478/밀수확−82.6u. | 초반현금/밀최대량/플래너구조를승리조건으로단정않음. v9라이브기록은09-17이후없음. | 다음c336후반회전·원가/시장경쟁의실제미검증범위부터이력검색. 현재프로세스없음·제출후보없음·blind보존. [상세](reports/c335-current-leader-evidence-2026-09-19.ko.md).

- 2026-09-19 20:13 KST | Codex | c335선택고정:리더보드11:08:55UTC Majkel3278.5/10위3029.7. score56216119최신533경기·최근sub56332038은3160.6으로별개. v9기록201경기는09-17에종료. c317이후score신규14완료유효경기전부(상대반복버전포함)수집/공식원장재현. | 결과/평점선별없음,현재행동분포기술이며미공개구조/반응모델을단정않음. |기존pilot다운로드/phase1accounting재사용·네트워크2/CPU12·정책평가없음·blind보존.

- 2026-09-19 20:11 KST | Codex | c334완료:QA20 native/fast4/off4·접두436턴4동일·해시PASS/max0.197초미만. 원장12양측행동/현금재현. 13/12타일추가시비/급수·4고용모두확인/부모작업충돌0,토마토+25/23u. | own+300이지만상대+883.5/margin−583.5로사전gateFAIL,원본대비margin−11457.5. 새screen/confirm/final없음·수량/조건재튜닝안함. | [보고서](reports/c334-joint-crop-service-2026-09-19.ko.md). 다음c335현재대회증거갱신,기준선v9·blind유지.

- 2026-09-19 20:04 KST | Codex | c334후보동결:공동투어물리12사례64→89u,실이동/수령/행동확인·고용610~2207. c177/c179/c313재사용13칸전환대조와같은전환+age7시비/age8급수경로,원본v9분리. 부모당일route/fallback번호예약·pending guard·실고용/작업확인. | known2세계QA20→12native원장,생산/매출/own/margin대조양수+원본대비승점/own/margin양수시에만새screen. |12워커·고정후보/기준·blind보존,아직경기이득미확인.

- 2026-09-19 20:01 KST | Codex | c334사전계약:c333추가방문상한→c170출생/beam투어·c313공식물리재사용. 13칸모두d18시비/d19급수,원본h4위치에서최소1~2고용으로h23전완료·관측기반숙성시비→수확/마지막수확규칙. | 12원본고정방문진단이며비료구매/부모미래반응/경제성미검증. 모든경기+13u물리지원때만후보실행계약검토. |12워커·후보/전게임/blind없음.

- 2026-09-19 19:55 KST | Codex | c333완료:원본156타일수확일치·38일정각단계152정확탐색/선택열직선재생확인. v1PASS누락으로옛대조9개−1u→v2수리후12/12재현. 시비시각만완화시토마토+1u;별도v3타일당2추가작업완화는총+26/28u(65/64→91/92),딸기102불변. | 추가방문물리지원gate통과이지경제/배포gate아님. 첫표본추가24작업=d18시비11+d19급수11+수확2,이동/고용/물류미보장. | c334에서같은날시간창·공동경로·부모예정고용/물자예약을감사후에만후보검토. 현재프로세스없음·v9기준선·blind보존. [상세](reports/c333-input-and-service-calendar-2026-09-19.ko.md).

- 2026-09-19 19:53 KST | Codex | c333v3사전계약:시비시점만완화한v2는토마토총+1u뿐. 같은비료예산에age6..12정오각타일최대2추가작업을허용한물리상한고정;모든12경기13타일총+13u이상일때만경로실행가능성감사. 작업자이동/공동자원/고용미보장·정책아님. | 사후도달상한이지전략/예측아님;비료조기운반가능성·다른급수/자원경쟁미보장. |12워커단일물리진단,유의미한생산지원있을때만실행계약감사;새후보/전게임/보호blind없음.

- 2026-09-19 19:50 KST | Codex | c333사전계약: c313은시비일원본고정/c321·323은비료0의생산표현,정상음수판정유지. 12정확원장156레인의원본수확먼저재현. 같은방문슬롯·같은총비료예산에서시비일만완화한딸기/토마토정확물리상한과locked대조. | 사후도달상한이지전략/예측아님;비료조기운반가능성·다른급수/자원경쟁미보장. |12워커단일물리진단,유의미한생산지원있을때만실행계약감사;새후보/전게임/보호blind없음.

- 2026-09-19 19:49 KST | Codex | c333사전계약: c313은시비일원본고정/c321·323은비료0의생산표현,정상음수판정유지. 12정확원장156레인의원본수확먼저재현. 같은방문슬롯·같은총비료예산에서시비일만완화한딸기/토마토정확물리상한과locked대조. | 사후도달상한이지전략/예측아님;비료조기운반가능성·다른급수/자원경쟁미보장. |12워커단일물리진단,유의미한생산지원있을때만실행계약감사;새후보/전게임/보호blind없음.

- 2026-09-19 19:46 KST | Codex | c332완료:QA16후256native,해시PASS/노출오류0/max0.220초미만. 직접v9 1승31패·승점−19.53%p CI[−27.34,−14.06]/own−1217/margin−2855. 상점128쌍동일. | 사전gateFAIL,confirm/final미실행·source재튜닝/이식없음. 저자자체패널수치를현재상위강도로읽지않음. | v9유지·제출없음·blind보존. 다음c333고정경로/투입제약의탐색범위감사부터.

- 2026-09-19 19:41 KST | Codex | c332사전동결:새공개Market Rhythm f3be6392(기존First in Line53dc계보)의개막10+판매순서3시나리오,생산새구조아님. c318 DP+$1.47/c324ed89FAIL과대조;저자12seed144게임queue증분+$20.78 CI0포함. | 원본QA16후새16seed·4소스·양좌석·2정책256native. 승점95%seedCI하단>0/margin>0/상대회귀−6.25%p이내때만독립confirm. |12워커·단일캠페인·후보원본불변·blind보존.

- 2026-09-19 19:40 KST | Codex | c331완료:16QA 모드4쌍/off4쌍동일,8원장양측행동/현금재현·잔차0. 2개발세계양좌석평균own−435/margin−579;추가딸기4u실생산,상점/가축구매불변. primary달력은1종이아닌2종(10+2) 정정,둘다격리상한4u. | 동결후보기각·screen없음·같은좌표/수량재튜닝안함. | [보고서](reports/c331-early-wheat-berry-lane-2026-09-19.ko.md). 다음c332새공개소스감사.

- 2026-09-19 19:31 KST | Codex | c331 후보동결:12역사원장 primary달력은1종,밀재파종을딸기로바꾸기만하면3u/밀13u대체. harvest-first 관리시도는수분부족으로2u 조기고사(WEED처리누락실행오류도별도수정),채택안함. 기존c313정확탐색재사용상한4u/변경1슬롯(최종일HARVEST). | 본후보는t60씨앗1개교체/t61(0,1)실식재확인/원래경로와급수보존/마지막수확·잡초정리만. 초기추가90이소구매/사료를밀수있음. | 16QA+8원장으로4개발조건 own/margin양수·실발동을먼저확인,음수시같은후보튜닝안함·새screen도안함.

- 2026-09-19 19:21 KST | Codex | c331 사전계약: c330 생산달력차→첫밀수확후재파종1칸 조기딸기 가능성. base19 straw_open 멜론대체−9.2k/옛opening문서미실행계획/c313·317·321 후기전환실패와구분. 기존c313 공식물리 simulate로d2–4최초재파종7좌표 지원확인,primary는관측상가장이른(0,1)이지사후수익최대좌표아님. | 기존방문·비료가정의격리물리뿐,정책이득아님. d15전primary수확지원시에만 초기씨앗/사료/소구매 사슬검증 포함1칸후보검토. | 12원장재사용,새후보/시뮬아직없음·blind보존.

- 2026-09-19 19:18 KST | Codex | c330 완료:12원본719행동/전이/양측현금·FIFO수량/판매원장 동일. 기존courier45계획253명령,후속층덮임0,계획DROP3품목실입고282u. 창고옆PASS기회3턴9u뿐. 수확→판매는우유/양털/딸기 모두우리평균이더짧지만단가낮음. | 운반누락을주원인으로가정한새banking구현안함. 딸기d0–14수확우리0/상대125u,d21+우리1720/상대810u로생산시기차관측. | 단가차는인과이득아님. 다음 초기밀재파종의생산계약 가능성은 멜론대체/후기작물전환 실패와 구분해물리/자금/사료비부터감사. [상세](reports/c330-transport-and-production-calendar-2026-09-19.ko.md).

- 2026-09-19 19:10 KST | Codex | c330 사전계약: bank_am/fm_bank/c305·306/c329 이력 확인. 현재v9에 _v9_courier(정오이후·남은tape유휴일손귀환)가 이미 구현됨. 기존12정확원본에서 수확→운반→입고→매도 단위FIFO, 기존courier계획과 최종명령/실제입고를 감사한다. | 새입고규칙/모델/후보없음; 원본719행동/상태/양측현금·물품보존 필수. 지연차이는 회복가능이익으로 해석하지않음. | 12워커읽기전용,실제누락된작업기회가있을때만 별도개입검토.

- 2026-09-19 19:06 KST | Codex | c330 사전 탐색만: 생산→입고 경로를 바꾸는 계획의 검토 전 이력 검색. base19 bank_am은 아침 노동만 늘고 수확시각을 못당겨 음수, fm_bank는 임계400 음수/1000 own+0.3k, c305/306은 추가생산과 부모매도간섭을 분리했던 사례. o005/r001/c308 단순 강자계획 복제도 실패. | c329의 작은 기회는 이미창고재고/3턴 범위만의 결론. 이름/부모만 바꿔 같은 banking 규칙을 재시험하지 않는다. | 다음은 기존 원장으로 현재v9의 수확·입고·판매 지연과 실제 수정 가능한 경로를 확인하고, 과거 실패와 다른 실행 계약이 있을 때만 실험을 고정한다. c330 아직 미구현·미실행.

- 2026-09-19 19:05 KST | Codex | c329 완료: 보유창고≤8u/3턴판매재배분,12경기1,692구간·242분기(233종료동일/9불일치). 사후최선마진합 평균+$30.75,양수6/12로사전확대조건실패. | 처음JSON중간복원은t504재고불일치로중단. native시작재생 snapshot으로수리,private키순서정렬만으로딸기+1/밀−1 재현. 최종12원본719전이·KEEP3전이·해시PASS,키순서검사추가후판정불변. | 짧은기존창고판매타이밍범위중단,모든시장전략상한아님. 새정책/학습/제출없음·blind보존. [상세](reports/c329-local-sale-opportunity-2026-09-19.ko.md).

- 2026-09-19 18:57 KST | Codex | c329 사전계약: c326/327 실패·c328 부분예측신호 이후 실제 판매변경 기회부터 감사. 기존 market_impact_audit 상한은 재고·상태회복/정확 거래큐가 미반영. 검증12상위 원본에서4턴 간격3턴 공식엔진 fork, 이미 가진재고 최대8u 시점만 변경; 종료상태 현금외 전부 동일한 경우만 양측 현금기여. | 사후oracle는 기회 진단이지 실행정책/승률 아님. 평균 독립구간 합계≤1000 또는양수경기<8이면추가확대중단; 통과도기전연구만. | 12워커, c328모델미사용·새후보/제출없음·blind보존.

- 2026-09-19 18:54 KST | Codex | c328 완료: 203배열 재추출 동일·사용순유입742,033건 중 오차1. 179훈련/24평가, RF64/depth8/leaf32 고정. 우유 Brier .048857<.052331, 양털 .044619>.043881, 딸기 .050567<.059421. 전체평균개선 .003863, 경기CI [.002440,.005242]. | 사전3품목기준FAIL, 부분신호만 보존. 첫 로더의 열별압축해제 비효율은 모델생성 전 중단·파일당1회읽기로 수정; 설정/자료 불변·해시PASS. | 모델 적용/추가 확인/품목 선택 없음. 다음 연구는 이전 실패와 구체적 변경 근거를 먼저 확인. [상세](reports/c328-short-horizon-sale-learning-2026-09-19.ko.md).

- 2026-09-19 18:48 KST | Codex | c328추출 실행오류:203npz완성 뒤 numpy int64 집계JSON 직렬화 실패. v2는원본문자열 object-array의 안전기본로딩에서 중단. v3는명시적정수/Unicode문자열저장,자체생성원본비교만pickle허용. 원본/실패로그·계약보존,203배열전체값동일성검사. | 특징/대상/분할/모델/판정기준변경없음,새게임0. | 데이터gate후에만학습. 소유자최신지시:의견에맞추기보다검증근거로독립판단하며개선연구계속.

- 2026-09-19 18:43 KST | Codex | c328사전계약: c308요청모방/c315–316장기공급/c327관측수리와대조. 기존검증179train/24양측버전비중복test 재사용,obs[t]→t+1,t+2 실제순시장유입≥4u(우유/양털/딸기). 기존공개특징+관측가능최근이력,RF64/depth8/leaf32고정. | 4대조(전체율/시간표/직전3일동시각/clock-marketRF)보다양품목이아닌3품목Brier모두개선+경기묶음구간>0일때만새확인자료. label로이력오차수정금지·순유입오차1%초과시학습전중단. | 12워커자료생성→12jobs학습순차,후보/새평가시뮬없음·blind보존.

- 2026-09-19 18:38 KST | Codex | c327 완료:자기판매25884/25884·floor불확실제외상대순유입23396/23396일치. QA16/off4/모드4동일후320native 해시PASS/오류0/max0.222초;승점+0.625%p(CI−3.75..+5)/own−7.41/margin−14.52·W→L1/L→W2·직접v9 9/11/12. 자기판매기록수정812,160쌍중행동변화100/동일60. | 사전gateFAIL,confirm/final/조합재튜닝없음. [보고서](reports/c327-final-sale-observer-2026-09-19.ko.md). | c328아직미구현·현재CPU작업없음·부품보존/부모v9/보호blind유지.

- 2026-09-19 18:31 KST | Codex | c327 원본12역사읽기:자기최종action판매25884/25884·불확실floor제외상대순유입23396/23396일치(기존가격허용구간98.97%,물량95.55%). | 새후보=기존v9 복원식만수리;P가격gate없음. QA16뒤새16세계5실행소스양좌석320native,사전승점CI하단>0/own≥0/margin>0/상대회귀제약,실패시튜닝안함. | 12워커단일검증·blind보존.

- 2026-09-19 18:29 KST | Codex | c327사전이력:c326가격gate 정상음수와분리,같은threshold재시도아님. 확인된복원180오차는최종층전의우리판매량/가격1처분오차. 기존_ov_fields/_r97_market_stock 물리부품으로최종자기action의판매량을원장대조하고,소비전시장재고가가격1인구간은관측불확실로분리. | 기존exact12원본관측읽기전용·12워커,상대private/action은label에만·정책후보아직없음. own판매오차0/사용가능구간상대순유입오차0 확인전후보실행안함. | 장기공급모델/가격gate재튜닝없음.

- 2026-09-19 18:29 KST | Codex | c327사전이력:c326가격gate 정상음수와분리,같은threshold재시도아님. 확인된복원180오차는최종층전의우리판매량/가격1처분오차. 기존_ov_fields/_r97_market_stock 물리부품으로최종자기action의판매량을원장대조하고,소비전시장재고가가격1인구간은관측불확실로분리. | 기존exact12원본관측읽기전용·12워커,상대private/action은label에만·정책후보아직없음. own판매오차0/사용가능구간상대순유입오차0 확인전후보실행안함. | 장기공급모델/가격gate재튜닝없음.

- 2026-09-19 18:26 KST | Codex | c326 완료: Q외부lib없어비활성,내장P 원본12재현에서추가매도118/미래2턴적중15/기준가미만116. 기존가격gate를P에적용한후보QA16/off4/모드4동일후320native 승점−13.75%p(CI−21.25..−5.625)/own−55/margin−541,직접v9 3/29로FAIL. 첫시드원장20행동재현·수확/판매물량Δ0이나own+219/상대+965. | 예측정밀도낮음≠제거하면강해짐. confirm/final/품목·threshold튜닝없음. [보고서](reports/c326-short-sale-predictor-contract-2026-09-19.ko.md). | 다음c327,현재CPU작업없음·blind보존.09:22UTC새리더보드1위Majkel3281.0/10위QQ3027.5.

- 2026-09-19 18:24 KST | Codex | c326 screen320완료,해시PASS/health0/max0.235초. 승점−13.75%p(CI−21.25..−5.625),own−55/margin−541,W→L17/L→W4,직접v9 3/29로기각. | confirm/final/튜닝없음. 첫설정시드1910529953 5상대양좌석부모/후보20원장행동재현으로판매가격/상대회복을점검. | 보호blind미사용.

- 2026-09-19 18:18 KST | Codex | c326원본12재생일치:Q층외부라이브러리없어비활성,P층예측1199/정답327,실제추가매도118중미래2턴적중15·기준가미만116. 기존RACEGATE를뒤P층이우회한다. | 가격기준새튜닝없이동일gate를P에적용한단일후보동결. QA16후새16세계5실행소스양좌석320native. 사전gate=승점seed CI하단>0/own≥0/margin>0/상대−6.25%p미만회귀없음;통과때만별도confirm32. | 한캠페인12워커,보호blind불변.

- 2026-09-19 18:15 KST | Codex | c326 추가진단: Q층은V92_SELL_LIB 외부경로없어evs0/매도변경0 확인.실제로활성인내장P층으로동일12경기를관찰한다. 사전이력: MX2의상대가격회복/지속예측실패, c314–316 장기공급예측, c318 판매순서DP와대조. 이번범위=현재v9 PREDICT2의1–2턴매도예측·실제추가주문·과거매도복원정확도를기존exact12elite원장에직접대조. | 새모델/threshold/후보없음,기존live_replay_audit 재사용·719행동/현금동일필수·12워커읽기전용. | 예측발동/실제체결을확인한뒤에만다음개입결정.

- 2026-09-19 18:14 KST | Codex | c326 사전이력: MX2의상대가격회복/지속예측실패, c314–316 장기공급예측, c318 판매순서DP와대조. 이번범위=현재v9 PREDICT2의1–2턴매도예측·실제추가주문·과거매도복원정확도를기존exact12elite원장에직접대조. | 새모델/threshold/후보없음,기존live_replay_audit 재사용·719행동/현금동일필수·12워커읽기전용. | 예측발동/실제체결을확인한뒤에만다음개입결정.

- 2026-09-19 18:10 KST | Codex | c325 완료: 역사현금8/8·모드8/8·off4/4 QA20, 원장8/8행동재현. 별도부모파일발견으로 c176미대조 설명 정정. 7015 일손번호 중복129회 중 명령차이116회,7056 0회. 단일예약수리 QA8/원장4 동일·중복0,수리후부모대비마진−14535/−17054로gateFAIL. | 신규고용수량/전환량탐색·확인/final/제출없음. 첫helper-entrypoint 로더오류 계약/로그보존→v2별도QA. [보고서](reports/c325-historical-worker-contract-audit-2026-09-19.ko.md). | 다음c326,현재실행없음·v9기준선/보호blind유지.

- 2026-09-19 18:08 KST | Codex | c325원장8/8 QA행동·현금재현/회계잔차0.7015의추가일손이부모미래번호를선점해129비PASS명령덮음;7056충돌0도큰손실. 양세계토마토가부모보다49/47u감소:부모SE투자를억제한대체계획임. | 재시도근거=실제번호충돌.현재선택경로/후반fallback의당일예약번호확보뒤추가고용하는단일수리만2세계양좌석native/fast8QA. 다른수량/분기변경없음;부모대비own·margin모두회복못하면확대안함. | 역사결함기전진단·blind보존.

- 2026-09-19 18:07 KST | Codex | c325원장8/8 QA행동·현금재현/회계잔차0.7015의추가일손이부모미래번호를선점해129비PASS명령덮음;7056충돌0도큰손실. 양세계토마토가부모보다49/47u감소:부모SE투자를억제한대체계획임. | 재시도근거=실제번호충돌.현재선택경로/후반fallback의당일예약번호확보뒤추가고용하는단일수리만2세계양좌석native/fast8QA. 다른수량/분기변경없음;부모대비own·margin모두회복못하면확대안함. | 역사결함기전진단·blind보존.

- 2026-09-19 18:05 KST | Codex | c325 QA20 완료: 과거현금8/8·native/fast8/8·off4/4동일,해시PASS·최대0.143초. c176부모대조는별도파일에존재하며증분마진−26675/−17054 재현. | 미검증후보설명정정. 두역사세계양좌석부모/후보8건원장+읽기전용작업관찰을고정;현재QA행동해시/현금일치필수. | 비용·급수·부모작업간섭진단이며새후보탐색/현재강도평가아님.

- 2026-09-19 17:59 KST | Codex | c325감사에서c176부모대조누락설명정정:별도strat/o199c/tomato__c150.json(72행)에7015/7056양좌석부모4행존재. 부모/overlay/후보원본SHA모두manifest일치. | 원본8조건현금재현+off4동일+native/fast8비교총20QA를고정,새전략아님·기각후보재승격실험아님. |12워커단일감사·보호blind미사용.

- 2026-09-19 17:56 KST | Codex | c324256native완료/해시PASS/health0,승점+3.91%p이나CI0포함·마진−79·직접v9 16/16. | 사전gateFAIL,confirm/final/부모변경없음. | 기존경로내작물치환탐색확대중단. 다음c325는c176 기존땅+전용노동계획의부모대조누락/원본계약감사부터.현재작업없음·1위/제출미달성.

- 2026-09-19 17:53 KST | Codex | c324원본/계측전체관측·행동·현금4쌍동일, native/fast8쌍동일,QA16오류0/max0.152초. 설정준비시과거manifest의list형을dict로가정한AttributeError수리(설정생성전,기존소스동일assert). | 계약256native screen실행,전략수정없음. |12워커단일비교·blind보존.

- 2026-09-19 17:51 KST | Codex | c324사전계약:새공개ed89be8c(2노트북동일)vs기준선v9. c312/c318선례와대조,옛V49재실험아님. 양쪽기존진단계측/원본동일QA16후새16세계4소스양좌석256native. | 승점시드CI하단>0+margin>0+상대회귀제약때만독립confirm16. |12워커단일검증,실제강도아직미확인·blind보존.

- 2026-09-19 17:49 KST | Codex | c3236144훈련완료/해시PASS/KEEP512동일·예외/시간초과/미확인구매/파종실패0. 초기11변형승점−16.60~0%p,승점/마진동시양수0이라사전중단. | 후보없음·교배세대미실행·확인32seed보존. 같은작물조합탐색확대안함. | c324:새공개ed89be8c소스의원본/계측동일성→기존v9와신규세계비교.1위/제출미확보.

- 2026-09-19 17:46 KST | Codex | c323학습중공개목록20갱신,새2노트북pull/셀실행0/바이트literal+게시SHA검증. 두소스동일ed89be8c,구V49+v9경제층함수계보. | 새로운독립2전략으로세지않음·강도QA미실행. | 현재c323계약불변,후속비교대상1소스보존(public_manifest.json).

- 2026-09-19 17:29 KST | Codex | c323달력지원감사512완료/QA16행동동일,64세계중50발동가능·38서명중26개가4세계이상지원. | 수리된세대등록+지원유전자만검색하는별도계약동결:64세계/4소스/양좌석512조건,최대36후보,초기12에승점·마진동시양수없으면CPU중단. c322유전자재사용안함·확인32새seed미사용. |12워커단일검색,아직후보/개선없음·blind보존.

- 2026-09-19 17:26 KST | Codex | c323실험전: c322의정상음수후보결과와검색구현오류분리. SQLite/공개samplerAPI감사+무시뮬36/36재현:초기enqueue12에generation없어후속부모에서제외,trial12–23으로새무작위집단. before_trial세대등록toy수리PASS. | 새64세계/4소스/양좌석의행동중립달력지원감사,QA16원본재현후512기준선. 활성세계≥16/서명3개각≥4세계아니면검색중단. |12워커단일감사·별도확인32seed미사용·blind보존.

- 2026-09-19 17:21 KST | Codex | c322독립확인576완료/기각:승점−15.28%p(CI전부음수),own+560/margin−188,W→L45/L→W1,해시PASS/오류0. 원중단계약저장477행모두v3양측행동·현금동일. 첫활성24원장행동/회계재현;새생산실재하지만상대가더벌었다. | 훈련8세계중4발동/승점이득1세계집중,다른후보재선택/본확인재튜닝안함. | 다음은학습지지범위/상대다양성/계획표현의제약부터이력과대조;무작정세대수만증대안함. 기준선v9·blind보존.

- 2026-09-19 17:12 KST | Codex | c322 확인v2는476/576처리지점 중단: keep vs o240/1101544374/seat0,노출예외0·719호출·DONE이나 overflow_contract_errors=1로health FAIL. 실제소스R148은창고예측불일치진단카운터이며예외targeted_errors와별도. 옛o227어댑터재사용해그키만mismatch로명명,실패조건포함2seed×양좌석×2정책의8쌍(16native) 행동·관측·현금동일. 예측이정확했다는뜻아님. | 원계약/실패행보존,후보·24seed·상대행동·gate불변v3별도576native다시실행. 중복을독립표본으로세지않음. |12워커단일확인·runner불변·blind보존.

- 2026-09-19 17:01 KST | Codex | c322 수리후36훈련후보종료,전략계약불변·baseline64행동현금/첫12source동일. 사전선택trial30:훈련승점+0.0625/margin+1088.4,개선증명아님. | candidate.py를동결해미사용24확인seed·6소스(v9/o240미학습)·양좌석576native사전기준적용. 대체후보재선택안함. |12워커단일확인·blind보존.

- 2026-09-19 16:54 KST | Codex | c322 실행 장애: GEN1로그640/768 뒤pool child0·CPU1%·조정프로세스27892/28092만생존확인. 해당조정자만종료,baseline64·첫12소스·study/log보존. finite max_tasks_per_child=64의워커재생성문제의심(경기예외증거없음). 후보행이세대말까지RAM에만있던지속성한계도확인. | 전략/seed/NSGA-II/gate변경없이train_portfolio_v2 persistent12workers+즉시행JSONL저장. 별도v2해시계약,첫12소스동일·baseline64행동현금동일재확인. | 재실행은실행기수리이며새독립증거로중복계산하지않음.

- 2026-09-19 16:51 KST | Codex | 최신공개35+35목록과07:36:15UTC리더보드확인:1위Majkel3281.1/10위3027.8. auto-top1은v9바이트동일,Master는설명문제외순서AST동일이라대결중복안함. FirstInLine=V48+look8,기존demandSHA검증복원·훈련상대사용. Windowscp949목록오류는UTF8재조회,writefile마지막newline복원후게시digest검증. | 새명칭/게시점수를전략신규성으로읽지않음. | c322학습진행,소스/이력보고서갱신·제출없음.

- 2026-09-19 16:48 KST | Codex | c322 전 실험 이력/도구 감사: p_search/open_search/bucket_search의대결목적Optuna는기존이나o227·반복seed·파일존재cache한계. c170은비료tour, c309/c317은기존정책선택, c321은동질5프로필정상음수. 새개입은38자기달력각각KEEP/생성계획을조합하는전체포트폴리오,고정가중치재튜닝아님. KEEP앵커 QA4/4원본동일·native/fast8/8/20실행유효. | 새8훈련seed·4실행소스(v9제외)·양좌석에서NSGA-II36후보학습,별도24seed확인사전고정. search_manifest참조. |12워커단일학습·private elite대리한계/보호blind보존.

- 2026-09-19 16:33 KST | Codex | c321 생성→실행→native 검증 종료.384/384 해시PASS/오류0,5프로필 전부 사전gateFAIL;primary margin−1288/승점−18.75%p. 첫활성세계 원본/balanced/berry 24원장 행동·현금 재현:멜론+42u·당근+14u 실제판매,양털−4.9k는 마지막상점변화와동반해직접생산손실로단정금지. 관측된6정책 사후승점여유+3.125%p가v9상대에만존재. | 고정5정책 기각/선택기학습·confirm/final 안함,생성기부품보존.보고서/이력갱신. | 다음은기존전체정책검색도구감사와실제대결목적의새계획탐색검토,후보미구현.모든CPU작업종료·목표미달·blind보존.

- 2026-09-19 16:29 KST | Codex | c321동결screen384완료/해시PASS/오류0/max0.155초.5프로필전부사전gateFAIL,primary own−554/margin−1288/승점−18.75%p;미발동160경기부모양측행동·현금동일,추가구매미확인/파종실패/씨앗부족0. | 별도확인/최종/제출진입없음. | 결과좋은조건선택없이첫활성시드1128194241의원본/primary/생성딸기3대조×4상대양좌석24원장재현으로기존생산·판매·상대수입차이확인. 가중치재튜닝안함·blind보존.

- 2026-09-19 16:22 KST | Codex | c321실행진단28완료/off4행동·현금동일/오류0,후속native14/14양측행동·현금동일/개입전265step동일. 5프로필전체개발조건구매확인164레인·다음관측파종확인292;현재까지추가판매0. 개발2세계평균own이올라도상대가더오르는프로필존재,승격증거아님. | 동결executor_v1 및8새시드4상대양좌석6모델384native화면평가고정,사전gate설정참조. |12워커단일캠페인·blind보존.

- 2026-09-19 16:19 KST | Codex | c321실행연결 전 이력: c313/c317/c320 작물치환 전체정책 음수, c305 추가매도 기존재고간섭. 이번에는38자기달력×5고정생성가중치의반복파종계획을현재관측에서일치검사후연결. 원래d11씨앗100/타일예산만치환,10주문한도·동시씨앗검사·실구매확인·잡초복구기록·추가판매0. c179기존V219조건재사용. | 원본/off/5프로필,기존QA2시드양좌석28실행진단;강도검증아님. | 기존pair_trace 재사용·12워커단일작업·blind보존.

- 2026-09-19 16:09 KST | Codex | c321자기일정감사12원본재현/생산슬롯 WATER1627+HARVEST684+FERTILIZE312+DIG156=2779건완전일치.38일정5고정가중치190새작업열을씨앗100예산내공식엔진으로탐색·별도씨앗묶음직선재생190/190확인. | 가치가중치≠시장가격예측,분리타일생산≠실농장수입,확률잡초미모델링/운반·현금·판매연결미완료. | c321계속: 실행계약통합후원본과native대결. 현재프로세스종료·보호blind보존.

- 2026-09-19 16:00 KST | Codex | c321방문계약12/12원본재현:156레인3471예측/3480실방문,3425완전일치. 누락/추가 차이는PICKUP/PASS/DROP/구조종류이며 WATER/FERTILIZE/HARVEST/DIG 차이0. 미래실방문을입력하지않고현재관측+자기경로로예측한생산슬롯만재사용. 기존엔진타일탐색을종류·반복파종·정리·급수·수확·씨앗총100예산의동시탐색으로확장,고정5가격프로필은생성용가중치일뿐미래가격예측아님. 전후같은엔진별도직선재생검증. | 실제현금/운반/창고/판매/상대효과는아직미검증. |12워커단일컴파일·보호blind없음.

- 2026-09-19 15:54 KST | Codex | c321실험전검색: optimizer=21Rita노브,compile_policy=종선택표,c171=공개기존경로이식,c170=비료부분경로탐색,c313/c320=기록된미래방문상한. 새계획생성의전제감사로v9기존_ca_visits를d11식재관측에서질의하고12소스검증라이브156레인미래실방문과비교. 입력은현재관측+자기프로그램뿐,실제미래는정답으로만사용. 원본719행동/양측현금재현·시각/일꾼/명령분리. | 아직후보/승률평가없음. |12워커단일진단·blind보존,출처state/c321/visits_manifest.json.

- 2026-09-19 15:50 KST | Codex | c320완료:384새native+QA12. 전체vsKEEP margin−1125/승점−15.625%p라기각,후속부품만margin+199/승점0으로보존. 첫활성세계24원장양측행동/현금재현(당근+16u·토마토불변·달걀−2u). 원장첫24dispatch중1저장후정수/문자day키판독오류;별도v2에서1재사용+23재실행,원본실패로그보존. 후보/기준무변경·confirm미실행. | 미세수확성공≠전체정책승리,작물전환threshold재튜닝안함. | 다음c321은기존계획선택을넘는실행가능계획생성공간의근거검토;현재캠페인없음·blind보존.

- 2026-09-19 15:40 KST | Codex | c320 물리상한156레인/52스케줄: 토마토64u 보존+당근33u(추가13씨앗가정). 관측기반순차재배 구현,QA12게임 off4/4 양측행동·현금일치/관측수정0·max0.132초. c177 기존경제gate/8·10칸규칙 불변을 사용하고 KEEP/기존gate/+tail3대조로 새16시드4실행소스양좌석384native사전고정. 확대조건은설정arena_meta에명시,screen후gate/물량재튜닝금지. | 상한/요청을실생산으로읽지않음,추가판매명령없음(c305교훈). | 12워커 단일캠페인 실행·blind보존.

- 2026-09-19 15:34 KST | Codex | c319 종료: 192게임·오류0·native기준64/64재현. 고정shop에서도2칸승점0/전체음수, c317FAIL 유지. c320 실험 전 이력확인: c313 고정수명상한/c317·c319 정상음수/c146·c305·c306 밀대체/base19재파종 대조. 새 개입공간은 토마토 마지막 수확 후 기존방문을 DIG/PLANT/WATER/HARVEST로 다시 배정하는 순차재배. 기존 공식엔진 단일타일 도구 확장, 가격튜닝없음·상한당근1씨앗. 신규전체게임0. | 실행계약·씨앗·시장경쟁 검증 전 전략효과로 읽지 않음. | state/c320/manifest.json과 tail_bound.json 확인.

- 2026-09-19 15:25 KST | Codex | c319진단전고정: c300동일seed미래shop변화/c313핀세계2개/c317학습FAIL대조. c317원config첫8시드·4실행상대·양좌석·3기존선택=192고정shop진단,성패/변화여부선별없음. 기존pair_trace+c313실행재사용,KEEP native양측행동64/64·공통결정관측·원래동일shop대안동일성·원장·양측오류검사. shop만부모경로고정,잡초/정책유지. native효과와차이분해만하며재학습/새gate/승격없음.12워커·단일캠페인·blind보존.

- 2026-09-19 15:22 KST | Codex | c318완료: Enhancedv2 계측QA16(원본4/4·실행경로8/8동일),native256(v9대비승점−17.19%p CI−28.13..−3.13/마진−1554/직접4승28패). K0006 32승의기전분리DPon/off128: ON64기존동일·미발동19OFF동일,평균마진+$1.46875/own+$3.67/승점0,소스DP이식안함. 총400실행오류0;v9개발기준선유지/새소스비교상대보존. 저자팀2820.9점과기존제출56299728=2759.24는새소스신원미확정이라분리. 다음c317미래상점분산감사,현재캠페인없음·보호blind보존. 보고서c318-enhanced-public-frontier.

- 2026-09-19 15:17 KST | Codex | c318 screenFAIL:Enhancedv2직접4승28패vs v9,공통승점−17.19%p/마진−1554;K0006에는32승(v9 28/4). R37/o240선행대조:새DP는전슬롯대칭시나리오목적,기존가파른곡선우선과다르나발동119블록/128뿐. 원인분리로DP만on/off,관측한16시드전부×K0006/v9×양좌석128native고정(성공/실패세계선별안함). ON기존양측행동일치·원래미발동OFF동일성검사. pooled margin>=200+승점양수아니면v9이식우선안함. 블라인드/동결부모불변.

- 2026-09-19 15:09 KST | Codex | c318사전고정: 신규공개Enhancedv2(54d02878)원본전략보존,최종함수에기존오류카운터참조만연결. c312기준선갱신/c317학습FAIL대조,기존K0006그대로재실험아님.16QA(native/fast2종+원본4native동일성)→통과시v9/4와16새시드4실행상대(v9/enh/K0006/o240)양좌석256native. 승점시드CI하단>0+margin>0때만독립confirm검토;저자91.67%/현재강도전제않음.12워커/단일캠페인/blind보존.

- 2026-09-19 15:05 KST | Codex | c317완료: 학습768/768·오류0,12워커1.282게임/s,max0.233초미만.3대안결정관측/접두256/256동일,189특징벡터. 동결8foldRF학습승점+1.5625%p(CI−5.86..+7.81)/margin+27.87/own+1630.74,개선v9에만→사전gateFAIL. oracle+10.55%p는v9집중. 고정2칸−1.95%p/13칸−23.44%p;배포/확인/튜닝안함. 기존결과상점진단:변경512조건중434의미래shops변화;실제d11관측3개(사후진단초안4개가정정정,학습입력정상). 보고서c317-direct-crop-action-learning. 새공개Enhanced v2·구COK소스출처만확보,대전아직없음. 현재캠페인없음/보호blind미사용/제출없음.

- 2026-09-19 14:58 KST | Codex | c317실행중별도읽기조사: 현재LB05:53:25UTC Majkel3269.0/10위3025.4. 공개경기최신56216119=3269.047 vs최근56332038=3119.043(둘다05:33UTC). 최근노트북30개에서zihengedie/best-version갱신발견,실행없이상수복원432375B/공개SHA54d02878일치. K0006파생판매큐/DP배정코드,저자91.67%주장은미검증·환경1.32.4. 현재동결768게임상대/후보에추가않음,다음실행상대후보로보존. reports/c317-direct-crop-action-learning.

- 2026-09-19 14:50 KST | Codex | c317 prepare가단계alpha합계.06으로게임시작전거부됨. 원config보존,confirm alpha만.025→.015로고친v1b생성(합계.05). 후보/시드/OOF판정불변,새게임0·전략실패아님. runner_config_amendment.json에해시기록.

- 2026-09-19 14:49 KST | Codex | c317 실행전고정: c309 d6전체경로8시드실패/c310희소여력/c313 수확수리와전환경제분리/c316예측FAIL대조. 새학습=d11실제씨앗구매직전 관측→KEEP/기존2칸/기존인증13칸레인전환의실제최종승점. 수명수확·V219호환보존,상점순서/양농장입력,32새시드×4실행상대×양좌석×3=768native. 먼저KEEP동일성16QA. 모든대안결정상태/접두동일검사,8fold시드분리RF설정고정;OOF승점CI하단>0·margin>0·v9외포함2상대승점+여야독립확인검토. 사후oracle배포금지/같은자료튜닝금지/보호blind보존.

- 2026-09-19 14:45 KST | Codex | c316 완료: 기존179경기/71버전/59팀 정확원장검증(33재사용,146새재생)·동일RF358관점학습·모델동결후별도24버전24경기평가(24원장재현). 양측train/test버전·seed·episode비중복. d27공개농장MAE 토마토14.18/딸기41.28 vs시장만28.87/29.92 vs옛모델58.87/52.31. 자료확장효과는있으나양품목대조gateFAIL;사후품목별모델선택/튜닝/정책적용없음. 역사2750+표본·시계열전진/3000+현재강도검증아님.12워커CPU86–91%,170새원본재생/반사실대전0. 보고서c316-expanded-supply-learning. 다음직접행동가치학습타당성감사,현재캠페인없음·blind보존.

- 2026-09-19 14:43 KST | Codex | c316 자료감사/학습완료: 179경기 정확원장·API좌석보상일치,RF설정변경없이358관점학습. 모델해시동결,별도고정24경기 target미평가. 정책적용없음.

- 2026-09-19 14:39 KST | Codex | c316 실행 전 고정: c315 추가확인FAIL 후 자료 범위만 재시도. 기존179경기/71버전 원장감사·캐시재사용→같은RF/특징학습. 별도24상대버전(동결v9기록2750+,양측train/이전20버전비중복)최신순선정,값확인전고정. 양품목d27MAE가확장중앙값/시장만/옛모델모두보다낮아야다음검토. 역사자료·계보독립/3000+강도보증아님,정책/제출없음.

- 2026-09-19 14:33 KST | Codex | c315 완료:고정RF64/depth4/leaf4,train25(9버전)/첫test12 source-disjoint PASS후모델동결. 신규8원본검증8/8,재학습없이확인했으나d27공개농장MAE 토마토26.69vs시장21.07/딸기57.40vs56.24로사전gateFAIL. 배포/threshold튜닝안함. 학습전구리플레이seat1 step누락정규화실행오류만수정,원본훈련소스보존. 읽기전용inventory에서기존pool179고유경기/71버전(보존test양측버전제외)확인,자료확장재시도근거후보로기록. 보고서c315-future-supply-learning. 현재실행중없음/blind보존/목표미달성.

- 2026-09-19 14:27 KST | Codex | c315 첫분리평가gatePASS: d27양농장모델MAE 토마토19.54(시장만21.90/중앙25.33),딸기42.90(50.98/64.67). 학습전옛리플레이seat1 step키누락정규화만수정,실패manifest보존·설정불변. 모델동결후추가확인8경기선정:기존snapshot에서3000+이며train/test에없는상대제출버전별최신1개전부,결과최적화없음. 기존fetch_current_elite재사용,모델재학습없음/새반사실게임0.

- 2026-09-19 14:25 KST | Codex | c315 학습 전 고정: c308검증56중test12와어느한쪽제출버전공유31경기제외→train25경기50관점/test12관점. d11공개관측→상대토마토/딸기d19/23/27실시장유입($1매각제외)예측. c308특징·정확원장재사용,RF64/depth4/leaf4/12jobs고정. 중앙값/시장상점만/양측농장3비교,primary d27양품목모두두대조MAE개선시에만추가평가. seed/경기/양측제출버전비중복,기존서술관측test라blind/시계열확인아님. c309대비목표/시점/자료/분리변경,전략후보없음.

- 2026-09-19 14:24 KST | Codex | c315 학습 전 고정: c308검증56중test12와어느한쪽제출버전공유31경기제외→train25경기50관점/test12관점. d11공개관측→상대토마토/딸기d19/23/27실시장유입($1매각제외)예측. c308특징·정확원장재사용,RF64/depth4/leaf4/12jobs고정. 중앙값/시장상점만/양측농장3비교,primary d27양품목모두두대조MAE개선시에만추가평가. seed/경기/양측제출버전비중복,기존서술관측test라blind/시계열확인아님. c309대비목표/시점/자료/분리변경,전략후보없음.

- 2026-09-19 14:21 KST | Codex | c314 완료: 재사용12원본96구간시장/상품보존식일치;새진단의$1재고규칙누락과endpoint정렬수정. d27새식재토마토475/551u,딸기1052/4871u;딸기floor판매838u. 현재농장고정/현재가모델의미래투자오차확인. HERD2기존공급floor처리shadow를12게임행동불변재현했으나26점수모두동일(무동작),전략확대안함. 자료state/c314·보고서c314-production-forecast-audit. 다음c315학습자료/독립지지설계,아직미구현.

- 2026-09-19 14:18 KST | Codex | c314 감사 중 공식엔진 $1 SELL은시장재고불변확인(원장보존식실패→해당판매제외후96조건PASS). v9 HERD2는신규공급은floor처리하지만기존양측공급은무조건재고추가. 새그룹/축군확대가아닌이비대칭의실제결정영향을먼저감사: 기존점수로행동유지,shadow점수만기록,검증된12라이브재현. 12워커/신규반사실평가0/동결소스불변.

- 2026-09-19 14:14 KST | Codex | c314 예측감사 전: c151 공개농장공급/상점ticks,base19 EC2 양측공급/한계수익,_hd2_ev 동물공급모델이기존구현됨을확인. c151평균손실단위정정/EC2음수/p002공급이력0/c309선택학습희소성을대조. 새전략/가격threshold만들기전,검증된c312상위12원본에서d11관측→d19/21/23/27 토마토·딸기시장예측을분해. 공식가격함수+c151소비ticks재사용,보이는작물1~2u생산시나리오와미래상점기대만사용;실제미래식재/재고는오차원인판독전용. 전체재고·거래·소비보존식검증. 기존12자료재사용/새게임0/튜닝없음/blind보존.

- 2026-09-19 14:11 KST | Codex | c313 반응형기전32게임완료(2기존시드×V49/K0006×양좌석×4모델,부모상점고정). 부모/off16기존native양측행동·현금동일,원장합계잔차0,해시PASS/오류0/max0.085초미만. 수명수확vs기존전환:8/8발동·토마토+2u판매+2u·own+70.75/margin+288/승점0. 전환묶음vs부모own−609.5/margin−146.75로확대·제출안함. V21910칸80u와고용/토지동일확인. c180기존가드는두개발시드모두제외,사후가격threshold튜닝안함. 부품보존/선택경제성미해결,다음c314미구현.

- 2026-09-19 14:05 KST | Codex | c313 전체게임기전시험 전 동결: c177/c179 원본전환재사용,forced2칸으로 부모/off/기존전환/같은전환+수명수확 4모델×2기존시드×V49/K0006×양좌석32게임. 부모상점경로고정·상대실행,off양측행동/현금검증. 새메커니즘=토마토마지막생산일수확(51→64u진단),새부모만으로재시험아님. 사전gate manifest;12워커·단일캠페인·blind보존.

- 2026-09-19 14:03 KST | Codex | c313 타일계약진단: 현재v9/4 라이브12경기d11딸기156타일의공식엔진수확일/양156/156원장일치. 같은방문토마토51u vs딸기102u;마지막생산일부터급수/시비→수확64u. 동일비료/정지슬롯유한상태탐색상한64–65u(52일정,독립표본아님),큰탐색기추가가치0–1u라확대안함. c160은d29한정/과거무동작,c177–180은기존전환으로구분. 다음부모/기존전환/같은전환+수명수확3분해로새기전검증;전체게임성능/제출후보아직없음. 보고서 reports/c313-crop-lane-contract-2026-09-19.ko.md. 원본/계약/blind보존.

- 2026-09-19 13:59 KST | Codex | c313 실행계약 진단 전: 선행c177–180은d11딸기레인전환/후반매도/고정2칸가드,일부정상개선. 신규토지o214·밀대체실패와구분. 현재v9/4의13칸레인에서 원본 field_events와엔진타일함수로 딸기대조 수확일치부터검사하고 같은일정 토마토의생산/소멸/수확을측정한다. 가격·전체게임효과·상대정책은평가하지않음;관측이후일정을사용하는사후실행진단이며런타임미래정보아님. 기존원장재사용,동결후보무변경,blind보존.

- 2026-09-19 13:57 KST | Codex | c312 독립confirm256:승점+31.25%p(CI+26.56..37.50),margin+2667/own+1494,오류0;개발기준선v9/4로갱신. 최신상위12경기원장·719결정·보상12/12재현,phase회계잔차0. 초반현금우세11/12→최종2승10패,생산배분검토. c177–180/o214/저자실패내역대조완료;새부모라는이유만으로고정토마토변형재시도안함. c313실행계약감사부터진행. 보고서 c312-public-v9-frontier-and-elite-losses. 보호blind/제출권한불변.

- 2026-09-19 13:50 KST | Codex | c312 후속 원장감사 전 고정: 새source v9/4의공개제출56269928,당시상대updatedScore>=3000인최근12경기(2승10패/9팀) 원본관측·행동·원장재현. 과거base19/c308손실설명을새부모에전이하지않고,저자토마토/노동병목주장도검증대상. 기존replay_accounting+격리launch 재사용,12워커,정책변경/반사실강도평가아님. 기존녹음1재사용+11수집,선택ID고정,blind보존.

- 2026-09-19 13:45 KST | Codex | c312 screen완료256(오류0,max0.227초 미만):v9/4 vsV49직접27승5패,동일상대풀승점+21.09%p(CI+5.47..+33.59),margin+1737.31,own−2023.15. K0006 28/4(V49 32/0) 상성회귀명시. 최신4라이브719결정·양측보상4/4동일,보고되는내부오류105카운터씩모두0. screen신호에따라동결config의기존미사용confirm16시드256실행을이제선택; 코드/파라미터변경없음. 확인조건=승점CI하단>0 및margin>0,미달이면부모교체안함;소스별결과별도,제출gate아님. blind보존.

- 2026-09-19 13:42 KST | Codex | c311완료: 누락된현재o240(b7de2d7b) 실행QA12 전부유효/8동등/변조0; 제출56293679 최근4녹음 행동719결정·양측현금4/4동일. API유효167경기118/49,최근경기09-18 updatedScore2522.73. 새16시드256native(고유물리192)에서o240→V49대체FAIL: family승점−33.33%p(CI−50..−12.5),margin−1074.73;직접6승26패,K0006 12/20(V49 32/0),o239 32/0. V49유지,o240비교상대보존. 기존생성도구는 knob/슬롯/리터럴복원이며terminal모델은712..718만지원함을확인. 보고서 reports/c311-existing-frontier-audit-2026-09-19.ko.md. 이어최신공개v9/4의c312 QA12통과,256native실행중(별도캠페인,중첩없음). blind보존.

- 2026-09-19 13:40 KST | Codex | c312 실험 전 기록: 최신Kaggle목록에 이전조사이후 공개된Tschinkel v9/4(2945 Farm)가 있음. 과거router_v5와 동일시하지 않음. 노트북을 실행하지 않고main리터럴 복원·공개SHA bfee70e9 일치. 저자2944.7/96.1%·top10패배원인은 미검증 주장. 실행QA12→새16시드·4상대·양좌석256native screen 고정,시드cluster/대칭중복표시. 보호blind미사용·제출아님. 출처 state/c312/source_manifest.json.

- 2026-09-19 13:34 KST | Codex | c311 실험 전 기록: 기존 생성/최적화 도구 감사 중 최근 비교에서 누락된 o240_sale_race를 발견. 과거K0006/V46/o239 개선보고는 있으나 현재rawSHA b7de2d7b/LF ddf22d3c는 보관a0c03048과 달라 강도/제출신원을 전제하지 않는다. 새전략 생성보다 현재파일 실행QA12→V49와같은 새16시드·4상대·양좌석256게임screen으로 기준선 감사 우선. own_tape계보 두파일은 family중복가중하지 않고 시드cluster/대칭경기종속 표시. 기존후보 무변경, 기준 사전고정, blind보존. 계획 state/c311/frontier_plan.json.

- 2026-09-19 13:25 KST | Codex | c310 완료: 기존 두 개발시드·4실행상대·양좌석·3정책48게임, 오류0/max0.188초 미만/계약해시 일치. KEEP16조건 이전c309 양측행동·보상 동일, 미발동9 동일, 발동7에서early(d6)=delayed(d9) 전체행동·보상 동일하면서 세 번째 상점 관측 가능. 무조건전환 own−54.69/margin+145.63/승점0; 새확인아님. 기존64조건의 late-compatible 사후oracle+3.125%p/+87.41은 한시드양좌석에집중. 선택기 확대학습은우선하지않고 기존계획생성도구 감사로이동. 보고서 reports/c310-late-plan-compatibility-2026-09-19.ko.md. 실행중캠페인없음, 제출후보없음, blind보존.

- 2026-09-19 13:21 KST | Codex | c310 실험 전 이력 확인: H05/o209의 지연 종선택·c171 경로교체·Macro Oracle·c309 정상 음수 학습을 재확인. 차이점은 전체 경로104→101/107→123의 공통 원시 접두를 보존하며 step217/216까지 결정을 미룰 수 있는지 실제 예측층 행동으로 검증하는 것. 이미 본 c309 두 시드·4실행상대·양좌석·KEEP/early/delayed48게임 진단만 고정. 선행 매도층 때문에 원시 접두 일치만으로 호환성을 주장하지 않는다. 승격/학습/새시드 확인 아님, blind보존. 계획 `state/c310/audit_plan.json`.

- 2026-09-19 13:15 KST | Codex | c309 v2 학습 대전512/512 완료(세션57134 종료0), 원본 KEEP QA16게임 완료. 모든64조건에서8대안의 결정 관측/접두 행동 일치, 같은 선택 경로이면 전체 행동/보상도 일치. seed 제외8fold RF 학습 완료(설정 변경0). | OOF 승점−4.6875%p, 마진+243.20, seed bootstrap95%=[−9.375,0]%p로 사전FAIL. 사후oracle +20.3125%p/+1,676.69는 실행 성능 아님. 고정 대안7개도 전부KEEP보다 나쁨. 선택기 배포/confirm/final 안 함. | 읽기 전용 추가 감사:64행→31특징벡터, 반복seed 지지3벡터; 변경24조건 중8조건은 다른 학습시드에 같은 상점조합 없음. 일부 계획의 원시 명령 차이는216/217/288/433부터여서 늦은 결정 가능성만 남음(실제 예측층 간섭 미검증). c310 미구현, 다음번호 보존. [결과·재시도 조건](reports/c309-plan-choice-learning-2026-09-19.ko.md). 현재 실행중 작업없음,12워커 기본 유지,blind미사용,1위목표 active.

- 2026-09-19 13:09 KST | Codex | c309 v1은step0로더가마지막callable인router를선택해QA중단(전략결과아님). 기존캠페인보존,v2에서agent키삭제후최종등록. KEEP8대조조건의양측전체행동/보상/상점일치·분기1회확인. | QA PASS,v2학습512게임진행중(세션57134),12워커·16논리코어의단기전체CPU73.8%. 첫22완료조건에서8대안의결정관측/행동접두일치. | 학습기는결과전작성/설정고정. 전체종료후seed제외8fold를실행하고OOF판정. 목표는변함없이1위,기본12워커지시반영. [설계](reports/c309-plan-choice-learning-2026-09-19.ko.md).

- 2026-09-19 13:05 KST | Codex | c309구체적행동공간감사:V49의41내장route중40개가처음144명령완전동일(route1예외). 기존o209는동물구매슬롯별종선택,c171은고정상점매핑,base19 oracle은소수노브라전체분기공간의상한아님. 기존macro_compile의실행기대신해시/seed/예외계약이있는canonicalv2를재사용. | 새가설:같은개막에서경쟁공급·현재가격에따라전체생산계획선택이첫두상점고정매핑을개선할수있음. source변경만재시도가아니라구매/배치/작물/노동의일관된계획묶음을선택하고결정직전상태동일성검사. | 결과전고정:KEEP+route100/101/109/110/114/123/12(요청포트폴리오다양성으로선정),8새train시드×4실행상대×양좌석×8정책512게임. KEEP16게임QA후진행. split은seed단위8fold;RF64/depth4/minleaf4、승점차·마진차별도학습,予測승점양수때만변경. OOF승점·마진양수일때만별도배포스크린. oracle는진단만.정책입력은d6관측,team/seed/미래정보금지.추가학습/확인아직미실행.최신목표워커기본12지시일치.

- 2026-09-19 12:59 KST | Codex | 이전턴진전: c308두실행전제수리·다양성72개막·canonical전체48게임완료(세션90130종료0). raw0/16승→수리본0/16승,V49 12승4무. 수리본raw대비own+24,204/margin+34,637이나V49대비−14,440/−46,325. health0/max0.1794초·현재소스/계약해시일치. | 사전기준FAIL,단일시연정책확대/제출안함. 초반목표재현과우승강도를구분했고아키텍처금지로확대안함. 원래guide도말기양4마리감소하므로종료가축차이를모두운영버그로읽지않음. | [통합보고](reports/c308-plan-execution-contract-2026-09-19.ko.md). c309미구현,기존검색/학습도구재조사완료. 새정책은강한실행기준선+실행가능계획검색을우선검토하되구체적행동공간/실험차이를먼저정의. 현재작업종료·blind미사용·목표미달성/계속active.

- 2026-09-19 12:38 KST | Codex | 6追加실행상대72개막완료(12worker/13.1초): raw20/24→cash24/24→resource24/24가d6의2C3S12M8B구성달성. 새K0006의고용붕괴4조건을cash가복구. 다른5상대는대체로미발동. 개발o2394조건까지포함하면resource가8상대32조건에서구성목표충족이나일부결식·현금차이존재. | 같은개막반복이므로32독립전략이나시즌강도증거아님. 이전r001/o005전체실패와모순없음. | 추가작은수리반복전전체시즌반증:동일guide의일관된719행동(raw),처음144턴만검증한두전제수리(repaired),V49를4실행상대×개발2시드×양좌석=48경기로비교. 다른녹음검색/매도층/base19인계없음. 최종승점·마진이raw와V49모두보다좋지않으면이단일witness를강도후보로확대안함. 기존canonical12워커사용;새설정만동결,blind미사용.

- 2026-09-19 12:36 KST | Codex | c308 resource계약16개막완료: o2394/4에서2C3S12M8B목표회복(현금770,고용계약만832·양2). 양탈출은막았지만결식1남음. V494/4수정미발동·양측행동해시동일. | 실행가능성만부분확인,시즌손익/최신1위상대강도미측정. seed/좌석4조건의같은개막을독립4전략증거로세지않음. | 이전r001/o005는다른시장붕괴,이번차이는검증된현금·경로별사료전제수리. 숫자조정없이6추가실행상대(base19,K0006,routerv5,boatlee,prvsiyan,V46)×새2시드×양좌석×raw/cash/resource=72개막,12워커로다양성진단. 보호blind/기존후보변경없음;이후더작은규칙반복대신전체계획평가진입여부판정.

- 2026-09-19 12:09 KST | Codex | 이전턴은 진전: c308 고용현금 계약16개막 완료. V49 on/off d6동일4/4·미발동. o2394/4 고용0 붕괴를 복구해 d6멜론4→12/딸기5→8/소0→2이나 양은2(목표3). 계약은 씨앗구매를 건너뛸 뿐 상환없음; telemetry deferred_seeds=3은 동일현금에서 세 번 막은 요청량이며 부모보다 실제 씨앗3개 덜 샀다는 뜻이 아님. | 1위/승률 증거 아님, 부분실행 성공. 별도2재현의 체크포인트·상점·telemetry일치. 추적상step73 창고밀4에3/3/2 pickup, step97 창고6에4/3/2 pickup으로 일부 인부가 필요 이상 보유하는 동안 다음턴 농부 급식이 실패, 같은양 연속결식. | 선행pick_own(당시−2.2k)/feed_stock(−1.6k) 확인. 새시험은 일반몫+1이나 추가매수가 아니라 현재농장과 보존된 자기계획의 다음 pickup까지 실제 FEED 타일에서 필요한 양을 산출해 부족턴에만 pickup상한 적용. 동물/이동/시장 추가변경없음. 기존고용계약 대비8조건만 개발진단, 성공시 다양성검증; #1보상은 여전히 최종승률이며 prefix회복만으로 채택안함.

- 2026-09-19 12:02 KST | Codex | 단일witness110648924/보조층off/실행상대8개막완료.V49 4/4는d6목표2C3S12M8B재현,현금862(원본848).o239 4/4는d1시작현금0→고용0(원본3)→d6멜론4/딸기5/양2로붕괴. | 테이프전체불가능증거아님.새한계는실제재현된개막자금선행조건.사용자지적에휘둘리지말라는지시도반영:구조선택은독립증거/기대가치로,강자실행보존+검색/학습을우선가설로유지. | c139유사이력확인:그것은이미막힌부분씨앗주문만유예했고일반상대미발동.c308은충분히살수있는마지막씨앗도다음날검증된작업사슬을깨면유예한다.차이는부모명만이아닌full-affordable/future-hire조건이며1회개발진단한다.동일guide의d1최초수입전실제actor3명→필요고용비4를자동추출,day0밀씨앗구매에서만보존;필드명령/초기동물/판매불변.원본목표이식아님,실행전제복원.12워커/기존8조건on/off대조,새승률/승격아님.

- 2026-09-19 12:00 KST | Codex | 어댑터원본6게임×off/on=12재생완료.off양측전관측/행동일치6/6,on도d0/d1/d6체크포인트현금/타일6/6동일.후반매도변화로최종현금−19.8k~+47.0k(동결상대/미래세계변경가능,강도아님). | 이설정이옛초반붕괴원인이라는가설은지원안됨.초반복원은충실한명령실행을기준으로시장·자금차이에대한취약조건을직접검증할수있음. | 다음은대표녹음110648924의첫144턴고정witness를V49/o239실행상대,개발7000/7001양좌석8개막에서진단.학습모델/base19/수리층/녹음검색/날짜인계없음.시즌설정유지144전이만실행,최종승률보고안함.새계획실행기구현에필요한최초선행조건단절파악용,원본복제성공만으로강도주장금지.

- 2026-09-19 11:57 KST | Codex | r001어댑터56원본teacher-forced감사완료:모든층off는전719턴×56행동동일,r001설정은5886턴변경(시장5883/손3),초기144턴52변경.선행매도층만5728변경/초기0,clamp75/초기49. | 요청차이≠상태/손익차이.원래시장수정층이켜진복제를충실한기준선으로보면안됨. | 기존원장재사용6게임을사전고정(최근6캐시source56216119):동일원본route/원본상대에off대조와r001설정12재생,전관측off동일필수.실제early/final차이분리;새상대승률이나옛r001전체실패의인과증명으로사용금지.

- 2026-09-19 11:54 KST | Codex | 이전턴=진전(시장모방학습·56원본실체결감사). 사용자r/base저성과/테이프우위 지적 반영,base19위목표복제의자동재시도보류. r001빌더는기록원본에c150의hand_align/weed_repair/sell_lead/room_guard/clamp_sells/terminal을기본적용했다. | 새복제기를만들기전 이실행어댑터가원래Majkel상태에서도행동을바꾸는지검증한다.원래동일상태에서계획변조가있으면과거실패를플래너필요성으로읽을수없음. | 기존56경기obs→동일경기고정route,모든층off대조와r001설정비교(teacher-forced/전략강도아님). 특히손순서와선행매도간섭분리.새승률평가/보호blind없음.

- 2026-09-19 11:50 KST | Codex | c308 모방학습5fold완료+56게임실체결label감사완료.새원본재생50/기존6재사용,전관측·보상동일/양측잔차0.완료세션91445.요청/실체결409턴차이,성공PLANT공통좌표/시점추출까지완료. | 첫실제모방학습은대조대비+2.13%p이나독립대전강도아님.원래1위도부분고용→판매후추가고용하며요청전체를행동목표로삼지않음.r001현금4vs5설명은둘다3명가능하므로추가입증필요. [상세결과](reports/c308-learning-pipeline-audit-2026-09-19.ko.md). | 다음=공통목표/선행조건기반개막실행복원,미세노브튜닝아님.구조미확정유지·blind미사용·제출후보없음.

- 2026-09-19 11:45 KST | Codex | 실제모방학습5fold완료:56경기/8064행/7상대팀,시장전체요청정확도시간표88.84%→자기+시장90.97%→상대농장포함90.23%.유효주문행일치79.71/81.86/79.71%,144스텝완전일치경기모두0. | 학습도움은있으나현재모델그대로실행후보안됨.상대입력추가음수를“상대무시”증명으로해석금지.새6정확원장에서Majkel도현금5로다수HIRE요청→3명실체결→비료판매후추가고용함을확인. | 다음은56경기모두기존replay_accounting으로요청/실체결분리:일치하는기존6원장은재사용하고나머지만최대12새프로세스,전관측/보상/현금잔차0필수.역사r001의$4vs$5설명은고용비1,1,2,3상두경우모두3명이라추가인과확인필요.후보수정/신규승률평가아님·blind보존.

- 2026-09-19 11:42 KST | Codex | 이전목표턴=진전(분류근거정정/62경기접두감사). H05/o209·H08/r001 재독:일별녹음검색/중앙값목표와구별하여 결정직전상태→다음요청의실제모방학습을시험한다. 기존도구검색에표준분류학습기없어 sklearn1.7.2를프로젝트venv에설치(새학습알고리즘자작안함). | 실행전고정:제출56216119의56경기,d0–5,시장주문전체서명.상대팀GroupKFold5로경기/시드를통째분리; 시간표최빈대조 vs 자기상태+시장 vs 상대공개농장추가.RandomForest64/max_depth12/min_leaf4/random_state308,12CPU.시간/승패/episode/미래정보를입력에넣지않고time step만허용.요청모방이며체결/승리label아님. | 예측일치·비어있지않은주문일치·전체개막완전일치·seed별paired차이를보고한다.평가성능튜닝없음,약한모방이면실행후보로승격안함.최신별도제출6경기혼합금지·새대전0·blind보존.

- 2026-09-19 11:38 KST | Codex | 사용자 개막모방/플래너분류/상대구매반응 질문에 출처추적.09-13은구조미확정,09-15r000과O보관이접두분기/공개테이프불일치에서플래너로과잉추론했음을정정.기존62리플레이해시대조/접두감사완료. | 실제점수제출56경기는큰개막유사/시장요청step2최초차이,최신별도제출6경기는step0~39동일.첫차이두사례는자기첫명령동일/상대거래·가격·현금상이여서간접반응과양립하나인과입력미확정. [상세](reports/c308-majkel-architecture-evidence-2026-09-19.ko.md). | 공통개막목표/현금·재고전제/예외복원→학습계획후보.새시뮬0·blind보존·c308후보미구현.

- 2026-09-19 11:33 KST | Codex | 학습 도구/이력 감사 및 방향 기록. shadow 실제788경기/4728행 재집계, 상태보다 앞선 요청을 포함하는label창·요청/체결 혼동 위험·seed/제출버전 누락 확인. macro 캐시파일 존재 재사용/행bootstrap 한계도 코드 확인. | 과거 학습 결과 전체 무효나 RL불가라는 결론은 아님. 시간·체결·출처 계약을 보완한 경제 계획 학습을 다음 우선순위로 설정. [상세](reports/c308-learning-pipeline-audit-2026-09-19.ko.md). | 기존 도구 재사용, 작은 모델/검색 대조부터. 새시뮬0·blind미사용·제출후보없음.

- 2026-09-19 11:32 KST | Codex | V49 native 추적은8원본 저장 후 day29 end.money 누락으로 판독 실패. 원본 재실행 없이 `state/c308/read_current_losses.py`로복구, 양측행동/보상/상점8/8동일·모든구간현금잔차0. 최종현금은terminal reward, 없는day29구성은null. | 사후선택4시드 모두d12열세지만최종한세계우세, 후반토마토기여 큼. 특정개막목표만 학습보상으로 사용하지 않음. [원자료](state/c308/v49_native_trace/summary_recovered.json). | 기존실패로그보존·새평가아님. 공유재고 진단도 큰손실근거없어 c308전략 미구현.

- 2026-09-19 11:29 KST | Codex | 共有재고 감사4/4 양측행동/현금동일. 정적 경로재고 초과49/80스텝이나 실제 PICKUP 완전미체결은1/2회(150/171 PICKUP), 부분체결4/6회. | 이 사례로 큰 배차개선 가설을 지지하지 않아 c308 미구현. 이전V46 원장은 주로 오래된 고정7000대였고 현재V49는 판매/복구 층이 다름. 다음은 새로완료된native실행에서 확인된손실의 정확매출 경로를 재현하는 진단이며 재평가/구조 재시도 아님. | Eco7공통패널 base19/V49 셀에서 평균마진 최악2·중앙1·최선1 seed 양좌석8재생, 실제canonical행동/보상/상점과일치 요구. 선정된실패표본이므로 일반승률통계로사용금지. blind미사용·한캠페인씩.

- 2026-09-19 11:26 KST | Codex | c307은 오류 재현+수정 개발판정 완료로 이전 목표 턴 진전. 다음 코드/이력 검색: base10 vrp_preload 음수, c300/c301 목표 보존/현장 우선 음수, Eco7 공유 예약 표현은 있음. base19 경로비용은 물자 유무만 보고 개수 소모/다른 일손 창고 사용을 예약하지 않음. | 이 정적 한계가 실제 손실인지 미확인. 별도 c308 후보를 만들지 않고 기존 pair_trace에 읽기 전용 route/PICKUP 엔진 계측. 예상 재고 초과와 실제 미체결을 분리. | 기존7000/7001 V48 양좌석4재생, 원본 양측행동/현금동일 요구, 12워커 상한. 미래 수확·매수·재계획을 제외한 정적 초과를 누적 손실로 해석하지 않음. blind미사용.

- 2026-09-19 11:24 KST | Codex | c307 구현/검증 완료: 감사4재생+off/on8재생, 행동불변 대조통과·내부예외0. 기존 잔여목표 이중차감은 실제이나 수정on 평균own+507.25/rival+705.25/margin−198, 승0/4→0/4. 양측 품목원장 현금차 잔차0. [보고서](reports/c307-residual-purchase-2026-09-19.ko.md). | 사전 개발gate실패로 기각/보존, 7000음수·7001양수 구분. 목표실행 정확성과 승리경제의 차이. | 현재 실행 중 캠페인 없음. c308미구현·blind미사용. 다음은 같은 종류 분리/노브튜닝이 아니라 자원·마감·투자기회 비용을 함께 표현하는 계획에서 실제 누락을 찾을 것. d0 PRODUCT 반복요청은 코드상 존재하나 기존부모 d0현금에서는추가구매근거없음(밀지출83·급식3·기말재고0); 이를 새성능결함으로 단정/구현하지 않음.

- 2026-09-19 11:19 KST | Codex | 구매계약 계측4/4 양측행동·현금동일. d4h11 딸기 부족1인데 당일주문1을 다시 빼 left0, 예산220/공간1. 7000 d6거위·d9소,7001 d6거위·양에서도 예산/공간 있는 억제 확인. [계측](state/c307/purchase_audit/summary.json). | 같은 억제 상태의 반복 관측이지 전부 별도 손실 아님. c307 구현 승인 범위 내 진행: 기존 목표는 그대로, d1+동물·d1–5멜론/딸기의 잔여수량만 이중 차감 제거. 초기고정량/후반혼합쿼터 불변. | 동결base19→새파일, off/on4조건씩·새프로세스·12워커상한. off행동동일·내부예외0·pooled own/margin 양수일 때만 확대 검토; 아니면 중단, 노브 탐색 없음. blind미사용.

- 2026-09-19 11:17 KST | Codex | 새 실험 전 이력/구현 검색: H02 씨앗예약, p002 주문시도/실제구매, base20-F 목표증대와 비교. `animal_plan`과 d1–5 멜론/딸기는 보유량을 뺀 부족수량인데 `market_orders` 공통 `left=target-done`이 당일 주문량을 다시 뺀다. 해당 구매계약 불일치를 직접 감사한 기록은 검색에서 찾지 못함. | c307은 아직 후보 미구현. 목표 확대가 아닌 기존 목표 실행 지연 가능성을 읽기 전용으로 확인. 현금/타일 충분 조건의 억제 사건을 기록하고, 원본 양측 행동/최종현금 동등성을 검증한다. | 기존7000/7001 V48 양좌석 4재생, pair_trace재사용·12워커상한·새프로세스. 반복 시점의 억제량 합계를 누적 손실로 읽지 않음. blind미사용.

- 2026-09-19 11:14 KST | Codex | Eco7 공통 비교96/96 완료, 사전/사후해시PASS·노출health0·최대0.379s. base19 7/48승 vs Eco7 0/48승, own−1295/rival+18571/margin−19866, 99% CI[−.52083,0]. [보고서](reports/c300-ecobot-comparison-2026-09-19.ko.md). | 개발gate실패로 확대/채택중단. 모든쌍 후반상점상이, d12현금+3236은 고정세계 우위나 최종이익이 아님. 외부 플래너 구조 전체를 기각하지 않음. | 현재 캠페인 없음·c307미사용·blind미사용. 다음 후보전 base19/Majkel의 투자 사슬을 조건부 관측과 실제 고정세계 개입으로 분리할 것. herd 목표 추가/단순 배차 조정/Eco7 전체이식 반복하지 말고 구체적 자원·시한 계약 누락 근거를 먼저 확보.

- 2026-09-19 11:11 KST | Codex | Eco7 모듈↔저자 번들 및 native/fast QA16실행 완료, 12/12 비교 동일·관측수정0·예외0·최대0.331s. 전략 변경 없이 새8seed×양좌석×V49/o239/K0006×Eco7/base19 =96게임 공통 비교 시작, v2 12워커·해시 사전PASS. [고정 설정](configs/validation/c300_ecobot_comparison.json). | 개발 목적이며 현행 비공개 상위권의 대리 평가 아님. own/margin/승점 모두 양수·상대별margin≥−1000·실행정상일 때만 후속 확인을 검토, 결과 후 기준 변경 없음. | 원본 정책 보존, blind 미사용. 상대/세계 조건별 결과와 상점 경로 변화를 함께 판독.

- 2026-09-19 11:08 KST | Codex | 상대·상점·시드·좌석 의존성을 계속 분리. Majkel 정확원장 6경기 단계별 재집계는 `state/c300/majkel_exact_phase_chain.json`에 저장(추가 경기 없음). d0–5 비료 수입이 base19와 비슷한 사례여서 초기 실행 전반의 열세로 단정하지 않음. 다음은 Eco7 공개 원본의 실행/포장 QA. | 선행: 09-19 O 조사 당시 EcoBot 소스 미확보, c300은 확보 후 정적/파종급수 참고만 했으며 강도 평가 미실행. 새 근거는 실제 8개 모듈과 저자 bundler 확보. 새 플래너를 만들거나 원본 전략을 수정하지 않고 기존 QA로 모듈/번들 행동 동일성을 먼저 검사한다. | 개발 7000/V48·7001/o239 양좌석, 원본 모듈 native와 저자 bundle native/fast 16실행·12워커. 통과 후에만 소규모 새 조건 공통 패널 검토. blind/동결 후보 불변; c307 미사용.

- 2026-09-19 10:59 KST | Codex | Majkel색인62경기재집계:56216119는56seed/양좌석,d0구성4종·d12구성55종;56332038은6seed/양좌석,d12구성6종. 새6리플레이정확엔진재현6/6완료. [자료](state/c300/live_update_20260919_1050/expanded_profiles.json). | 사용자지시대로상대/상점/시드/좌석조건부관측으로해석. 구성이곧의도적분기는아님. | 현재실행중캠페인없음. c307미구현. 다음은새후보전최신56216119의실행/현금사슬을정확원장에서추적하며 base19와유사한d5수량이왜다른후속경로가되는지구체적기전확인. 보호blind미사용·제출없음.

- 2026-09-19 10:57 KST | Codex | c306 3단계 완료·해시PASS·노출health0, finalown+17.51/margin+29.99/352→356승·CI0포함. [최종보고](reports/c306-validation-result-2026-09-19.ko.md). 이후12멜론기전12진단 완료, 부모행동4/4동일·과거o227현금4/4동일. 29u판매는7000/o227의고용3명상태, V48또는7001에서는59u로 달라졌다. | c306소형요소보존·제출아님.12멜론조합다시채택하지않음; hire_res도기존구현. | 사용자조건부해석 지시 반영. 기존Majkel50경기+이번6경기+이전6경기의 관측분포 재집계, 새6리플레이만 기존exactaccounting으로 재현 확인. 동시캠페인없음·blind미사용.

- 2026-09-19 10:50–10:52 KST | Codex | 사용자 최신상대 지시 반영, 기존도구로 leaderboard 및 Majkel 두제출의 최신경기 재수집. 현재1위3243.3은09-13 제출56216119의 최신점수3243.374와 일치;09-18 제출56332038은3100.647. 최근2900+상대 각3리플레이 추가. [보고서](reports/c300-majkel-live-update-2026-09-19.ko.md). | 팀최고점과 최신제출 혼동 방지. 현재 상위권 모델 내용은 미확인. | 고정c306평가 불변; 다음상대풀은 최신성·실제행동 다양성 점검. 동결승률로 사적반응정책 대체 금지.

- 2026-09-19 10:40–10:42 KST | Codex | c306 confirm512완료,12워커 처리량1.267게임/s(screen8워커0.987; 세계차이 있어 엄밀벤치마크 아님). 노출health0·최대양측결정0.233s·해시PASS. own+17.81/margin+36.51/L→W4/W→L0, CI0포함. [판정](state/c306/confirm_verdict.json). | 사전gate통과, 작은 공개상대 개선만 관측. | 사전고정final64seed/1024게임12워커 시작. 동결후 조정없음, blind미사용.

- 2026-09-19 09:20–10:38 KST | Codex | c305는 기존c146 경로 인증을 재사용했으나 추가 SELL이 부모 당근 재고까지 조기 처분해 기전4조건 own−654/margin−165.5로 기각. c306은 해당 SELL만 제거, 발동2조건 own+756/+711·margin+1573/+1567, off양측 행동4/4동일. native screen256 해시전후PASS/실패0,79→81승이나 이득 전환은 한 세계 양좌석이며 CI0포함. 사전gate 통과 후 confirm512 실행. 사용자12워커 지시에 v2별도 생성, 실행/집계 함수 AST불변·설정검사 확인; 과거v1불변. | c306은 소형 공개 상대 개선 가설이며 제출 후보 아님. | confirm결과·해시 판정, 개막감사 병행. blind미사용.
- 2026-09-19 10:25–10:38 KST | Codex | 추가 시뮬 없이 기존native h2h 양관점 행동/보상 대조·중복제거, V48/V46/o239 각각16세계32조건 d12현금 격차 확인. 일별 엔진원장 현금일치 확인, feed_wheat 필드가 왕복포함 모든밀구매임을 정정. [개막감사](reports/c300-opening-gap-audit-2026-09-19.ko.md). | 같은계획 실행실패로 단정 불가: 첫날부터 투자선택이 다르다. 원장차액은 개입회복량이 아니다. | 기존12멜론/base20-F 실제 소스와 수확/입고 병목 증거를 우선 확인.

- 2026-09-19 09:12–09:18 KST | Codex | 공개4노트북·EcoBot 소스·공식 평가/RL 디스커션 조사와 해시 색인 저장. V49 QA12게임 정상/실행 비교8/8동일. EcoBot 파종→급수 묶음과 base19를 읽기 전용2재생 대조, 기존 부모의 양측 행동/현금 동일. 원시 급수 누락15/18건은 자정 flag 초기화 오판으로 정정: 실제 즉시급수178/179·266/267, 지연 각1. c151 원본64조건 재합산해 −4332는 마진 합계(평균−67.69)임을 명시. | 새 제출 후보 없음, c305 미구현. 외부 구현의 이름/평판 대신 코드·실행 증거 사용. | 최신 비교 상대 V49 확보. 다음 생산 계획 변경은 파종급수보다 아직 확인하지 않은 자원 예약/작업 사슬의 실제 손실 근거가 필요. blind·동결 소스·제출 불변.
- 2026-09-19 08:56–09:12 KST | Codex | c176 실제 스모크·c146/c151/c152 경로 인증 이력 확인 후 base19 식재 배정 감사8재생, c304 off/on8실행. off 양측 행동/현금4/4 동일, on own +80.75 / rival +2169 / margin −2088.25. 전 조건 멜론 −6u, 토마토 −8..−12u. [산출물](state/c304/verdict.json). | c304 기각, 확대/블라인드/제출 없음. 단순 타일 할당 수정은 초기 투자 사슬을 보존하지 못함. | 사용자 요청에 따라 최신 공개 노트북4개와 EcoBot 데이터셋, 디스커션/RL 보고·공식 평가 설명을 조사. 재시도 가능성을 구조 이름만으로 닫지 않음.
- 2026-09-19 08:52–08:55 KST | Codex | 사용자 지시를 AGENTS/본 원장에 영구 규칙으로 반영. o199c/o232/o236·base18 car_wf 및 엔진 급수 코드를 대조한 뒤, 새 전략 없이 기존 pair_trace에 읽기 전용 계측만 추가해 고정 2조건 원본/계측본 총4재생. 양측 행동 해시와 원래 현금 모두 동일. 강제 수확이 WATER를 53/38회 덮었고 전체 강제 수확의 미급수 잠재량은 71/48u. 다음 동일 위치 즉시 수확이 관측된 WATER는 16/9건(16/9u). [감사](state/c303/harvest_order_audit.json), [계측 코드](state/c303/harvest_order_audit.py). | 수확 순서 결함은 확인, 수정의 순수익은 미검증. 당일 quote×잠재량은 실현 매출/회복 상한이 아니며 이후 정책 경로도 바뀔 수 있다. c303 기각 유지, c304 생성·추가 screen 없음. | 단순 water-first/가격비 재탐색 중단. 경로 보존 가능한 생산 계획 변경을 검토하기 전 c176/c180/o214의 실제 실행 증거 확인. blind·동결 소스·제출 불변.
- 2026-09-19 08:25–08:52 KST | Codex | c303 = 원본 V48+기존 o199c. 개발 4조건 own −5493 / margin +2793로 사전 gate 실패. 미래 상점 변화가 있어 원본 상점을 고정한 추가 원인 진단 2쌍 실행: PET 세계 두 좌석 own −6797/−5969, margin +15908/−4717. CARROT +133/+84u 대신 WHEAT −303/−224u, 사료·씨앗 비용 증가. [개발](state/c303/mechanism.json), [고정 진단](state/c303/fixed_original_shops.json). | 후보 기각; broad screen/off QA 미실행. 마진 증가만으로 생산 개선이라 해석하지 않음. | 사용자 최신 지시를 AGENTS/본 원장에 반영. o199c의 age3 수확이 유효 급수를 덮는지 기존 base18 수정과 대조해 감사; 아직 오류 확정·수정 후보 없음.
- 2026-09-19 08:20–08:25 KST | Codex | c302 native screen192 완료, exported health failure0·최대 호출0.177s. own gate 미달로 중단. 추가 계측 native QA16: V48/c302 각각 4조건에서 원본·계측본의 양측 행동 해시 일치, 29/31개 REPORT·STATS를 노출해 표본 내 오류0 확인. 기존 V48 최종 callable telemetry 누락은 실제였으며 전체192의 내부 오류까지 검증했다는 의미는 아님. | c302 기각/보존. mismatch 진단2에서 4개 불일치는 이미 올바른 GOOSE 배치로 확인; 이식 버그로 오판하지 않음. | c303은 본체 V48의 3PET 작물 격차와 기존 o199c 모듈을 대조; c302를 부모로 쓰지 않음.
- 2026-09-19 08:12–08:20 KST | Codex | c301 구현/개발4/off4→기각. 기존 h2h V48 손실 3세계6조건 재현(최종 현금 모두 과거 native와 일치); 우유/계란 공급 선택 격차 확인. V48 최종 callable `_e335_agent`를 어댑터로 보존하고 기존 `build_overlay.py`·o171e/o170c를 그대로 재사용해 c302 생성. 기전4+비발동2 완료, native screen192 실행. | base19 배차 수정은 중단; c302는 아직 후보 검증 중이며 제출 후보 아님. | 화면의 프로세스/핸들 및 캠페인 산출물로 실제 완료 확인 후 집계. V48 원본은 마지막 callable에 telemetry가 없어 기존 h2h의 내부 오류 계수는 관측되지 않았다는 한계도 확인; 향후 계측 보완 시 행동 동등성 검증 필요.
- 2026-09-19 08:04–08:11 KST | Codex | 기존 `pair_trace` 재사용, VRP 측정→c300 구현→off QA→실행 상대/고정 세계 진단까지 32회 로컬 실행(전략 조건은 매번 같은 개발 2시드×2좌석; 초기 프로브 로더 실패 4회 포함, 성능 근거 제외). 새 평가 러너 없음, 최대 4워커·동시 캠페인 없음. | c300 기각: 고정 세계에서 멜론 −6u·토마토 −13u, 이동 오히려 +70.25회, own −226/margin −761. d0 밀 4→3타일, d1 멜론 씨앗 구매 h12→h18, 3→2개로 변하는 실행 사슬 관측. 경로 예약 개선과 경제 계획 보존은 다름. | c301+는 작업 묶음/의존성을 검토. 보호 blind·기존 동결 후보 불변.
- 2026-09-19 08:06 KST | Codex | 프로브 v0가 `proxy_eval.load_agent`의 마지막 callable 규칙 때문에 보조 함수를 에이전트로 선택하여 전부 PASS로 실패(부모 현금 3000). 별도 v1 파일에 마지막 2인자 entrypoint를 두어 수정, 부모와 일별 원장·현금 4/4 일치. | v0 결과 보존·전략 실패와 분리. 원래 로더/동결 runner 변경 없음. | 추가 오버레이는 마지막 callable과 실제 호출 경로 확인.
- 2026-09-19 08:03 KST | Codex | 세 원장 삭제·보관 구간 존재·AGENTS/CLAUDE의 HANDOFF 단일 기록 지침과 활성 문서 참조를 재확인. 기존 도구로 끝낸 동결 진단 36게임도 이 원장에 반영. | 문서 통합 완료; 동결 승률은 상위권 순위 증거로 사용 불가. 새 전략 후보 없음. | 후속 연구도 이 파일에만 기록하고 실제 실행 상대에 대한 근거를 확보.
- 2026-09-19 07:53 KST | Codex | 사용자 지시로 HANDOFF 단일 원장 전환. 이전 HANDOFF 및 C/O 세 원장의 전체 내용을 아래 보관 구간으로 통합하고 참조 수정 후 세 파일 삭제. | 새 작업은 이 절에만 기록. | c300 상위권 분석 계속.
- 2026-09-19 07:40–07:52 KST | Codex | 실행 동일성 18 QA게임, 3캠페인 1952행 독립 집계, 현재 leaderboard/4제출 12replay 수집, 고유 11replay 정확 원장 재현 완료. | 구형 품목 원장의 오차 확인; 새로운 전략 후보 아직 없음. | 검증된 기존 도구 재사용·최신 상대 실패 분석.

## 보관 기록 안내

아래는 당시 기록을 내용 누락 없이 옮긴 것이다. **당시 현재 상태·기록 위치·실행 권한·명명 규칙은 현재 지시가 아니다.** 오늘의 지시는 이 파일 맨 위와 최신 사용자 메시지가 우선한다. 긴 이력은 필요할 때 후보 ID로 검색하며 매번 전부 읽지 않는다.

<a id="previous-handoff"></a>
<details>
<summary>이전 HANDOFF 전체</summary>

# Kaggriculture Handoff — START HERE (2026-09-19 07:30 KST)

> **사용자 갱신 — c300부터 재검토:** Codex는 [c-working](#c300-history)에, Claude는 `o-working.md`에 기록한다. [c300 연구 문서](docs/c300-research.ko.md)에서 코드·자료·검증 신뢰성과 변화하는 상위권을 다시 조사하고 구조/부모 선택·구현·로컬 평가를 계속한다. 아래 점수·부모 후보·미결 결정은 이전 시점의 기록이며 현재 경쟁력이나 고정된 설계 전제가 아니다. 새 c300+ 후보는 허용, 기존 동결 파일·blind·제출 소유자 규칙은 유지.

처음 보는 사람·AI는 이 섹션만 읽으면 현재 상태를 알 수 있다. 상세는 `reports/o-index-2026-09-19.ko.md`(산출물 색인) → `reports/o-policy-compare-results-2026-09-19.ko.md`(현재 결론의 본문) → `docs/o-handoff-2026-09-16.ko.md`(시간순 상세) 순서로 연다. 이 섹션 아래의 옛 내용(2026-09-15 c-시리즈 인수인계)은 **보관용**이며 현재 상태가 아니다.

## 1. 한 줄 상태

새 실험을 제안하기 전에는 [실험 이력과 재시도 전 확인 사항](docs/experiment-history-and-lessons.ko.md)을 읽는다. C/O 원장을 함께 정리했으며, 테이프 보존·정책표·플래너 인계 등 선행 시도와 실패/무동작/파손/미실행을 구분한다. 같은 실험을 다시 하려면 기존 실패 원인이 무엇으로 달라졌는지 먼저 적는다.

- 목표: 리더보드 #1 (소유자, 2026-09-17). 아직 달성 경로 미확정.
- 공식 champion 표기는 **base19**(플래너, 소유자 지정)이나 **라이브 실측 ≈1,400**(sub 56319267, 75경기 38/37)이라 승격·제출 근거가 없다. 플래너 라인의 유지/보류/종료는 **소유자 결정 대기**.
- 우리 라이브 최강은 **tape 라인 o239_50**(`agent/o239_open_roundtrip_50.py`, sub 56278146, ≈2,660·최고 2,754).
- **개발 부모 후보 = 공개 V48 파일**(`state/o_dev/v48_clearqueue_public.py` = `state/o_dev/p005_v48_exact.py`, sha 4b540288…): 라이브 검증 강자 5정책 상호 대전 두 시드 집합에서 전승(V47 16-0, V46 16-0, o239_50 12-4, base19 14-2), 라이브 사본 6개 2,560–2,760. 단 그 라이브 수준은 우리 tape와 같고 2750+ 군에는 30% → **V48 채택만으로 #1이 되지 않는다.**
- **제출 후보 없음.** blind 시드 7240–7255 미사용. p004(V46 exact) 기록은 대체됨.
- 종료·보류: MX2(p001) 보류, p002·p003 폐기, V46 분기 공격 종료, router v5 약함(라이브 1,440).

## 2. 상태판

| 라인/파일 | sha 앞 8 | 로컬(상호 대전 승점, screen/confirm) | 라이브 | 상태 |
|---|---|---|---|---|
| base19 플래너 `state/o_dev/p000_base19.py` (개발 본체 `agent/p000_planner.py`, 스위치 off = 동일 행동) | 53d80342 | .250 / .125 | ≈1,400 | 소유자 결정 대기 |
| tape o239_50 `agent/o239_open_roundtrip_50.py` | 4e8bdfa3 | .469 / .438 | ≈2,660(최고 2,754) | 라이브 최강, 대안 부모 |
| V46 exact `state/o_dev/v46_public.py` (= p004) | 735c3703 | .375 / .375 | ≈2,430 | 기록(대체됨) |
| V47 `state/o_dev/v47_public.py` | f4ecd487 | .609 / .656 | 2,686(저자) | 참고 |
| **V48 `state/o_dev/v48_clearqueue_public.py` (= p005)** | 4b540288 | **.797 / .906** | 사본 2,560–2,760 | **개발 부모 후보** |

라이브 2400–2850 대역의 구성(276 상대 리플레이 지문): 공개 tape 계보의 라운드트립 개막 변형(B70/S70·B5/S5·B50/S50…), V46/V47/V48 계보, K0006, 공개 라우터. 2750+ 군은 사적 변형·사적 planner로 실행 소스가 없다(frozen 리플레이만: `o_replays/live_band2400/`).

## 3. 절대 규칙 (변경 금지)

1. **Kaggle 제출은 소유자만.** Claude/AI는 `kaggle competitions submit`을 실행하지 않는다(중복 제출 사고 09-17). 읽기 전용 API(에피소드·노트북 pull)는 허가 하에 가능.
2. blind 시드 **7240–7255**는 최종 동결 후보의 마지막 검증 전까지 사용 금지.
3. 정식 러너(`tools/validation_v1.py`)의 계약(1..8워커, 3단계 분리 시드, 건전성 규칙)을 바꾸지 않는다. 캠페인을 겹쳐 실행하지 않는다. 실패·중단 캠페인과 manifest도 보존한다. 기본 8워커, o_tools 긴 작업만 12.
4. `agent/c*.py`·`agent/o2*.py` tape 소스는 수정하지 않는다. 공개 소스 파일은 원본 그대로(어댑터가 필요하면 행동 동일성 확인 후 래퍼).
5. 판정 규칙·패널·시드는 **실행 전에 고정**하고 결과를 보고 바꾸지 않는다. 후보는 한 번에 하나, 개발 평가와 별도 확인을 분리.
6. Codex 로그는 `reports/c-working.md`, Claude 로그는 `reports/o-working.md`에 실제 시각으로 기록. 새 코드에 라이선스 블록 없음.
7. 결론은 "planner가 낫다/tape가 낫다"가 아니라 **정책 파일 단위**로 적는다.

## 4. 평가 방법의 현재 이해 (중요)

- 12상대 공통 패널(`configs/validation/policy_compare_v1/v2.json`)은 옛 버전 tape·약한 "elite"로 구성돼 **.9 위에서 포화**한다. 하위(base19 .42, router .40)는 가르지만 상위(V46 .906 / V47 .938 / V48 .938)는 못 가른다.
- 상위 순위는 **라이브 검증 강자 상호 대전**(`configs/validation/policy_h2h_v2.json`: base19·V46·V47·V48·o239_50, 두 시드 집합) + **라이브 기록**(`o_tools/live_episodes.py <sub>`, `o_tools/rival_source_trace.py --verify`)으로 판정한다.
- 로컬 승률과 라이브 평점은 다르다: V46은 패널 .92였지만 라이브 2,430. 패널 우세는 라이브 증명이 아니다.

## 5. 소유자 결정 대기 항목

1. 플래너(base19) 라인: 유지(초반 경제 구조의 구체적 설계 아이디어 1건 + 동등성 게이트) / 보류 / 종료.
2. 개발 부모: V48 파일 vs 우리 tape o239_50.
3. 다음 후보의 대상: 2750+ 군에 대한 구체적 손실 1건(리플레이 분석부터).

## 6. 정해지면 바로 할 일

- 부모 확정 → `reports/o-working.md`·이 섹션 갱신 → 2750+ 군 리플레이(`o_replays/live_band2400/o239_games` 2750+ 27경기 등)에서 손실 메커니즘 1건 규명 → 재현 가능한 대리 상대가 있을 때만 후보(p006+) 구현 → `policy_h2h_v2` 방식 + 라이브 사본 대조로 판정 → 통과 시에만 blind → QA → 소유자 제출.

---
# (보관) 이전 인수인계 — 2026-09-15 c-시리즈 기준, 현재 상태 아님


## Latest: c156~c171 candidates implemented; activation screen prepared (2026-09-15)

- Candidate discovery is closed at c171 by user request. No c172 artifact was created.
  The next action is the prepared 1,344-game screen after every other Kaggriculture
  coordinator/worker tree has exited; do not overlap the currently observed o207 run.
- Frozen local parent is `agent/o182_combo_overflow.py`, SHA-256
  `ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b`.
- Reacting-screen candidates built directly from that parent: c156 production-cap
  harvest, c160 day-29 persistent harvest, c163 worthless-CARE fertilizer recovery,
  c168 certified FERTILIZE-before-WATER, c170 exact-spawn fertilizer-tour assignment,
  and c171 safe V42 non-YARN production routes.
- c159 is an immutable conservative prototype superseded by c170: a static complete
  search found that post-select safety filtering could reject the global maximum and
  miss a safe improving runner-up. c170 applies every target's parent gain floor
  inside the beam search.
- c167/c169 are immutable intermediate V42 artifacts superseded by c171. c171 fixes
  cold-start step-648 reopening, same-step telemetry reset, incomplete-map fallback,
  and malformed shop types while keeping normal routes and all source hashes.
- Combined contract suite: 78 passed. All dedicated builders reran byte-identically.
  No reacting game or submission was performed; all promotion flags remain false.
- Common v1 activation/health screen is prepared and checked at
  `state/agent_experiments/c156_c171_activation_screen_20260915/`: 1,344 games =
  7 models x 8 independent-family opponents x 12 fresh seeds x both seats, 8 workers.
  Run only its `screen` stage. This is an activity/health filter, not promotion proof.
- Detail and exact user-run command:
  `reports/c156-c171-implementation-and-screen-2026-09-15.ko.md`.

## Latest: c160 day-29 harvest screen prepared (2026-09-15)

- Built `agent/c160_day29_harvest.py` from exact `o182_combo_overflow.py` plus a
  narrow overlay. SHA-256: `c3f5d1749665d173640c29271635de8cf5ea761f6dcc8bb82e0820c5a42776fc`.
- Only at steps 696..711, replace a parent `WATER`/`FERTILIZE` with `HARVEST`
  when that actor is standing on TOMATO/STRAWBERRY with existing yield. Market,
  movement, purchases, hiring, planting, and the step-712 terminal planner stay intact.
- Compile, last-callable, synthetic mechanism tests, reusable-runner 9-test suite,
  frozen manifest check, and `git diff --check` passed. No game result exists yet;
  `promotion=false`.
- Frozen native-reacting screen is prepared at
  `state/agent_experiments/c160_o182_long_screen_20260915/`: 4,096 games,
  128 fresh seeds x 8 distinct-author/family opponents x 2 models x both seats,
  8 workers. Config stages are disjoint and have no overlap with prior validation
  configs. Run only the screen first; confirm/final remain unused.
- Each game uses a fresh subprocess, immutable job/source hashes, and unique temp,
  logs, and results. Parallel workers execute a frozen schedule and cannot adapt to
  or read another worker's partial result. c159 fertilizer-tour work remains separate.

## Latest: c155/o160 screen reviewed (2026-09-15)

- 1152/1152 rows revalidated. W/L/T per 288: c150 157/51/80, c155 175/49/64,
  o159b 243/45/0, o160 256/32/0. o160 is strongest on this panel, not qualified elite champion.
- c155-c150 +3.47pp, approximate 97.5% CI +1.04..+6.60pp, win-to-loss 0.
  o160-c150 +20.49pp but win-to-loss 8; o160-o159b +4.51pp, CI crosses zero,
  win-to-loss 9 and worse loss tail. No promotion/submission.
- Next implementation-only design: o161=c150+harvest-only; o162=o159b+goose-only
  harvest (threshold3 unchanged). Separate feed/harvest interaction and species scope.
- Review: `reports/c155-o160-screen-review-2026-09-15.ko.md`.
  Copyable prompt: `reports/o161-o162-implementation-prompt-2026-09-15.ko.md`.
  No candidates implemented or simulations launched; await user implementation report.

## Latest: reusable validation v1 implemented (2026-09-15)

- All agents must reuse the framework rather than create candidate-specific tooling.
  See AGENTS.md's REUSE FIRST rules; CLAUDE.md points Claude Code to the same rules.

- New experiments use `tools/run-validation.ps1` + `tools/validation_v1.py` +
  `tools/validation_stats_v1.py`; change JSON config and output folder, not runner copies.
- Example: `configs/validation/c155-o160-v1.example.json`. Read
  `docs/reusable-validation.ko.md` for Prepare/Check/Run/Analyze and screen/confirm/final.
- Existing o160 and c155/o160 campaigns remain immutable. The example is not a request
  to rerun them. No games were launched for framework implementation.
- User implements agents; this session designs validation and reviews user-run results.
  Only the common framework implementation was explicitly delegated to this session.
- All automatic outcomes remain promotion=false; statistical signals require review.

## Latest: long-validation isolation contract (2026-09-15)

- The user accepts longer runs to reduce seed luck and allows up to the global cap of
  8 workers. Do not start a second campaign while any Kaggriculture worker tree exists.
- Every match must be a fresh Python subprocess with a unique immutable job JSON, log,
  result file/output directory, explicit seed, candidate seat and frozen source hashes.
  Do not use threaded in-process games or share imported agents, monkeypatches, module
  globals, temporary paths, or RNG state between parallel work.
- Baseline and candidate must use the same seed/opponent in both seats. Development,
  selection, and final seeds stay disjoint. Parallel chunks may execute frozen jobs but
  must not adapt from another chunk's partial results.
- At this checkpoint an `o158` fixed-shop elite suite owns six worker branches under
  `o_results/elite_suite/o158/`. Recheck its coordinator/child tree before preparing or
  starting any new campaign; do not infer activity from lock files alone.

## Latest: c154 maintenance-feed rejected (2026-09-15)

- Read-only audit of the 12 latest c153 losses confirms the inherited c129 gap grows
  mainly before the terminal seven turns. From steps 504..695, ours used 206 more
  feed WHEAT while harvesting +170 MILK/+32 WOOL but -97 WHEAT and using 86 less
  fertilizer. At step 712 the aggregate individually reachable harvest-value gap was
  only -66; both sides ended with zero harvestable yield.
- Built `agent/c154_maintenance_feed.py`, SHA-256
  `c4121ea5ec69cc2d1a90272309711f927566ab2319b08f9a902484eb6a66712b`.
  It retains c124's first low-margin feed skip, restoring only a second consecutive
  c124-confirmed skip to prevent escape. This is distinct from rejected c137, which
  restored every sheep feed.
- Recorded-observation shadow: active in 3/12 latest losses, changing only PASS->FEED
  at steps 603/608/612; c129/server mismatches 0. This proves scope/activity only.
- The six-game fixed-opponent mechanism probe completed healthy but failed its gate.
  Across the three paired episodes, c154 worsened margin by 69, 229 and 279
  (total -577) and own cash by 79, 291 and 153 (total -523). Every episode was
  worse and every candidate row reported `maintenance_feed_ambiguous=1`.
- Reject c154. Do not advance it to reacting validation or tune this maintenance-feed
  rule. The result reinforces that preserving low-value animals can cost more WHEAT
  than it returns, even when only the second consecutive skipped feed is restored.
- Evidence: `state/agent_experiments/c154_maintenance_feed_20260915/results.json`.
  This is fixed-shop/frozen-opponent mechanism evidence, not a broad win-rate estimate.
- Detail: `reports/c154-maintenance-feed-development-2026-09-15.ko.md`.

## Latest: c153 direction audit (2026-09-15)

- c153 live snapshot 2383.3 / 59W12L among 71 scored returned games; c129 2820.3.
  Different opponents/seeds/times prevent a causal rating comparison.
- Downloaded all 12 returned c153 losses. On all 719 observations in every game,
  c129 and c153 actions match each other and the actual submitted action exactly.
  These defeats are inherited behavior, not observed c153-triggered regressions.
- Prior c153 reacting gate was FALSE (0 changed conditions / 896); submitting it
  as an improvement was not justified by generalization evidence. Keep c129 baseline.
- Old c153 mechanism runner has unsafe in-process threaded engine monkeypatching.
  Fresh 8-game subprocess audit reproduced +5947/+2997 in BOTH native/fixed modes,
  all exact shop paths. Retract the old claim that candidate caused shop divergence.
- Direction: evaluate executable late-harvest/cash-recovery bundles, then middle-game
  production/reinvestment choices, with shared resource reservation. Require actual
  activity before large evaluation; tune only after reacting improvement evidence.
- See `reports/c153-regression-and-direction-audit-2026-09-15.ko.md` and
  `state/agent_experiments/c153_direction_audit_20260915/`. No new submission this audit.

## Latest: c153 validated and submitted (2026-09-14 night)

- Submitted `agent/c153_urgent_feed_exact1.py` once, Kaggle ref `56232526`.
  Server status is `COMPLETE` with initial rating 600.0; do not duplicate-submit it.
- Source SHA-256: `b31bbbe2f7c0f8ab93dd773cfc441e40e65d23caaf30c29e6ae42c44e25ed383`.
  Archive SHA-256: `3e7c482519a95468f271ba09941d3b52077bdec787e34075475cd4ebb418d4ca`.
  Server-downloaded archive and sole `main.py` match the local package exactly.
- Fresh reacting/public panel: 1,792/1,792 healthy games, 896 c129/c153 paired
  conditions, zero action/point/margin/cash changes and zero regressions. The
  mechanism was inactive, so this is non-regression evidence, not improvement.
- Requested public opponents: both c129 and c153 scored 76W/52L against each of
  shop-router-reactive-v5, V41 Review Candidate, and Dynamic Route Agent.
- Fixed-opponent mechanism cases passed: episode 108609267 improved margin +5,947
  and own cash +1,569; episode 108724215 improved margin +2,997 and own cash -305.
  Both confirmed purchase/pickup/feed/survival for three animals with zero contract
  failures. The former used native shops after its strict fixed-shop path diverged.
- Keep c129 as confirmed live champion until c153 accumulates enough Kaggle matches;
  the new-agent initial 600.0 is execution confirmation, not a performance comparison.
  Receipt: `state/submission_artifacts/c153_urgent_feed_exact1_20260914/receipt.json`.
  Detail: `reports/c153-autonomous-validation-submission-2026-09-14.ko.md`.

## Latest: c151 failed; c152 expansion-only probe ready (2026-09-14 evening)

- c151 probe completed 128/128 healthy games. Versus paired c146 baselines:
  point delta -3, margin -4,332, own cash -2,278, action changes 6, gate failed.
  c151 evaluated 1,200 certificates and rejected all; it suppressed c146's profitable
  seed 640603013 conversions. Do not submit or tune c151.
- Built `agent/c152_shop_expansion.py` from hash-guarded c146. SHA-256
  `785529ac46ca6731b8901836bab48a1eb647203e9a1b7c9395495a6f7c6ac2fa`.
  c146's demand>=25 branch is exact; the forecast only expands into lower-demand shops.
  Seven mechanism tests passed, including legacy behavior equality and fail-closed timing.
- Prepared and checked 64 new c152 games against 64 exact frozen c146 outputs:
  `& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\c152_shop_expansion_probe_20260914\run.ps1'`
  Eight workers, progress/ETA/cache/resume/notification, roughly 2-5 minutes.
- When complete, analyze `state/agent_experiments/c152_shop_expansion_probe_20260914/results.json`.
  First require legacy seed 640603013 non-regression, then inspect low-demand expansion
  requests, paired points/cash/margin, related/nagata subgroups and bottom tail.
- Detail: `reports/c151-result-and-c152-expansion-2026-09-14.ko.md`.

## Latest: c151 shop-demand development probe (2026-09-14)

This checkpoint supersedes the older runtime/candidate notes below for the next action.
Python 3.12.6 / kaggle-environments 1.32.7 is restored and exact engine identity verified.
The user runs simulations; none were launched in this implementation turn.

- Implemented `agent/c151_shop_forecast.py`, a c146 derivative, **not c150 + c146**.
  SHA-256 `47c1ee52c03f07d79482ec8e3625abdadb2d542387203946803a1a607cd3cab1`.
- Replaces fixed carrot shop threshold with exact known-shop consumption to harvest,
  public crop supply, stock/commitment deduplication, and wheat scarcity opportunity cost.
  Retains the 18-25 day window and physical purchase/plant/feed/harvest guards.
- 12 mechanism tests + 3 summary tests passed; PowerShell parse and frozen plan check passed.
  No reacting improvement, promotion, or rank-1 claim yet.
- Ready user command: `& 'H:\dev\kaggle-data\kaggriculture-strategy-meta\state\agent_experiments\c151_shop_probe_20260914\run.ps1'`
- 128 games = c146/c151 × 8 reused development seeds × c129/c150/c146/nagata × both seats;
  8 workers, estimated 5-10 minutes, progress/ETA/cache/resume and audible notifications.
  Sources/jobs/support/engine are frozen. Do not edit them; use a new experiment for changes.
- Analyze `state/agent_experiments/c151_shop_probe_20260914/results.json` when user completes.
  First check actual action changes and subgroup/tail regressions; do not tune inactive settings.
- Detail: `reports/c151-shop-forecast-development-2026-09-14.ko.md`.

## Older context (some snapshot and blocker notes below are historical)

Updated 2026-09-14 KST. This is a current-state index, not a chronological log.
Full pre-compaction files are preserved under
`state/context-archive/20260914-121406/`.

## Champion and live evidence

- Submitted champion: `agent/c129_feed_liquidity.py`.
- Kaggle submission ref: `56209242`; prior readback was COMPLETE with empty error and
  server archive/source match.
- SHA-256: `e9973586cbe2c0bbb034243f3d3e4c9fdcac4fcac432c0de32b0ba0e61f7ca61`.
- Its final pre-submission 64-seed/1024-game paired confirmation improved direct
  points 50% to 53.125% with no common win-to-loss. This was a small tested-pool
  gain, not proof of rank 1.
- Latest downloaded snapshot is
  `state/agent_experiments/c125_followup_20260913/snapshots/20260914T015403531994Z/`:
  c125 score 2833.6, 97W/43L/1T in 141 games; c129 score 2810.8,
  83W/36L in 119 games. Panels and times differ, so scores are not a paired model
  comparison.

## Loss evidence: 79 recorded defeats

The latest snapshot adds 32 losses to the earlier 47: c125 adds 17 and c129 adds
15. All 79 replay files exist locally. The read-only audit is:

- `state/agent_experiments/structural_loss_audit79_20260914/analyze_recorded.py`
- `state/agent_experiments/structural_loss_audit79_20260914/summary.json`
- `state/agent_experiments/structural_loss_audit79_20260914/results.json`

The script imports neither an agent nor the engine. It verifies 720 states and the
snapshot/replay margin, then records action/state transitions. Results are diagnostic,
not causal counterfactuals.

Key all-79 observations:

- Severity: 11 losses under 500, 55 from 500 to 4,999, and 13 at 5,000 or worse.
- 32 games were ahead at step 504 and still lost; 34 lost at least 2,000 cash from
  step 504 to the end. Aggregate late swing was -248,105.
- Opponent used less feed in 64/79 and more fertilizer in 60/79. Opponent recorded
  more successful harvested units in 34/79.
- Our traces contain 765 failed FEED transitions, 23 failed wheat pickups,
  6 failed animal placements, and 184 animal disappearances. These counts include
  repeated scheduled attempts and do not individually prove avoidable lost profit.
- New 32 are consistent with the inherited weakness: 15 late reversals, 15 late
  decays of at least 2,000, opponent less feed in 25, more fertilizer in 22, and
  our failed wheat pickups 16 versus rival 3.
- Repeated opponent submissions form useful clusters; see `repeated_opponent_submissions`
  in the summary. Do not count their games as independent families.

Current diagnosis: c125 and c129 share a production-allocation and execution-chain
weakness. The recurring path is market choice plus `HIRE -> BUILD -> PLACE -> FEED ->
HARVEST/SELL`, with wheat, feed, fertilizer, and late conversion competing for the
same labor and cash. Small timing losses and large structural losses require separate
objectives.

## Candidate state

### c145

`agent/c145_carrot_min3.py` passed the old 47 fixed-tape development gate:
3 improved, 44 same, 0 worse; margin +4,130 and own cash +932. Its 192 reacting
games were all inactive and identical to c129. It showed no broad effect and is not
a promotion candidate.

### c146 — strongest current diagnostic improvement

- Source: `agent/c146_carrot_sched3.py`
- SHA-256: `5e51caad786dac00f98639e8eb8ef911a169904f86cff3d2fe777853cd89a928`
- Result: `state/agent_experiments/c146_carrot_sched3_20260914/results.json`
- Old 47 tapes: 4 improved, 43 same, 0 worse; total margin +6,352; own cash
  +1,569; 11 conversions and 11 confirmed plants.
- This is the largest clean improvement among current unsubmitted fixed-tape
  candidates. It has no reacting qualification and is not champion.
- A 12-game realized-economics trace was prepared at
  `state/agent_experiments/c146_realized_trace_20260914/`, but its runner must use
  the exact restored runtime before execution.

### c147 — isolated feed commitment repair

- Source: `agent/c147_feed_commitment.py`
- SHA-256: `d055f46ce8340ed1e309b14d28f30521c424368c720cd45911952e7fbb89d3ea`
- It only buys a bounded wheat shortfall when the parent is already picking up a
  demanded cow/sheep and the route proves next-turn wheat pickup, placement, and
  first feed. Episode 108609267 should request exactly 2 wheat for 2 sheep.
- Static candidate build passed. No simulation result exists and no promotion claim
  is allowed.

### Rejected or limited directions

- c137 blanket late-sheep rescue worsened 14 of 15 activations; do not revive it.
- c139 improved synthetic opening stress but was inactive on the broad reacting
  panel and had a shared-seed regression cluster; do not promote it.
- c140/c141/c142 opening variants gained points in related pools but had major margin
  tails or win-to-loss regressions; keep as stress evidence.
- c143/c144 improved only one old tape while reducing own cash; their gates failed.

## Runtime blocker

The project `.venv` points to removed Python 3.12.6:
`C:/Users/Taeyang/AppData/Local/Programs/Python/Python312/python.exe`.
Bundled Python 3.12.14 can import `kaggle-environments==1.32.7` through the old
site-packages, but strict `engine_identity()` correctly rejects the Python version
change. Do not relax this check.

An attempt to install Python 3.12.6 inside `state/runtime/python` with `uv` could not
download under the restricted network. The escalated retry was unavailable because
automatic approval review had no active account. No runtime was changed.

Preferred recovery: install exact 3.12.6 into the project-local runtime and point
the wrappers at it, preserving existing identity. Alternative: freeze a new 3.12.14
engine contract and rerun every parent/candidate baseline on identical jobs; never
mix those results with 3.12.6 rows.

## Practical tuning space

The strongest current base for tuning is c146, while c147 must first pass its isolated
mechanism preflight.

Ten useful c146 knobs are: active day window, market-hour cutoff, conversion cap,
demand threshold, visible/competing carrot supply buffer, wheat shadow-inventory
shift, grain quote premium, value cushion, cash reserve, and shed-capacity headroom.
With three values each, a full grid is `3^10 = 59,049` configurations.

Seven useful c147 knobs are: active window, market-hour cutoff, wheat price ceiling,
benefit/cost ratio, route lookahead, maximum funded deficit, and combined cash/capacity
reserve policy. With three values each, this is `3^7 = 2,187`. A naive joint grid is
`3^17 = 129,140,163` configurations. Dormant c146 feed-topup thresholds are excluded
because that mechanism activated zero times in the old tape set.

Recommended search budget after runtime recovery:

1. One-factor screen for c146: baseline plus low/high alternatives for ten knobs =
   21 configurations on discovery conditions.
2. Keep the four knobs with stable subgroup effects; run their 3-level interaction
   grid = 81 configurations.
3. Advance at most six configurations to paired reacting development; reject any
   subgroup point regression, common win-to-loss, or worse loss tail.
4. Test c147 separately. Combine it with c146 only if its physical purchase/pickup/
   placement/feed contract and reacting gates pass.
5. Use untouched final seeds once for the last one or two candidates.

This is 102 discovery configurations before reacting qualification instead of 59,049
or 129 million. Do not tune directly for total margin over the observed 79 losses.
Use separate close-loss, structural-loss, late-reversal, and opponent-family slices.

## Execution rules and next actions

- The user currently runs simulations; do not launch a new campaign autonomously.
- Maximum 8 total workers, with no overlapping Kaggriculture campaign.
- Commands require progress bar, completed/total, percent, elapsed, cached-aware ETA,
  desktop notification, and sound.
- First recover exact Python 3.12.6 or deliberately establish a wholly new paired
  engine contract.
- Then run c147's three sequential preflights and the c146 realized trace.
- Expand the loss diagnostic contract from old 47 to all 79 before using the new
  32 as evidence for a candidate.
- Only after mechanism gates pass, run both seats against independent reacting
  opponents plus related regression controls. Preserve unused final conditions.
- No new submission or simulation was made during this handoff update.

## Current evidence index

- `reports/c145-resume-and-top2-review-2026-09-14.ko.md`
- `state/parallel-handoffs/collaboration-20260914/loss-forensics-47/report.md`
- `state/parallel-handoffs/collaboration-20260914/c146-trace/report.md`
- `state/parallel-handoffs/collaboration-20260914/validation-audit/report.md`
- `state/parallel-handoffs/collaboration-20260914/public-opponents/report.md`
- `docs/agent-validation-protocol.ko.md`

## o-series handoff (Claude, 2026-09-16)
Read `docs/o-handoff-2026-09-16.ko.md` first: current best agent (o227, submission 56264950), the six validation gates (incl. the weed-synced frozen-Majkel proxy and the pinned-world A/B harness), today's confirmed facts (market absorption, mirror externality, top cluster = planners, V44 race arm and the stealth response), the rejected-candidate table (o220–o237), the planner-proxy project status, data assets and the prioritized next steps. Ledger: `o_experiments.jsonl`; chronological log: `reports/o-working.md`.

</details>

<a id="c300-history"></a>
<details>
<summary>c300 초기 분리 원장 전체</summary>

# Codex 작업 원장 — c300부터

사용자 지시(2026-09-19): 1위 달성까지 연구·구현·검증을 지속한다. 과거 점수·구현·자료·판정의 정확성을 전제하지 않으며, 변화하는 상대를 고려해 tape/분기/반응형/planner 구조를 다시 선택한다. Codex는 이 파일, Claude는 `o-working.md`에 기록한다.

## 현재 작업

- c300 = 평가 신뢰성 감사와 새 전략 설계의 출발점. 아직 성능 후보나 제출물이 아니다.
- 먼저 공식 실행 경로와 기존 고속 실행 경로의 행동·관측·상태 동일성, 데이터 출처/시점, 평가 대표성을 검사한다. 오류를 발견해도 관련 없는 과거 결과까지 일괄 무효화하지 않는다.
- 개발 구조는 미정. base19/V48/o239 등은 역사적 기준선이며 현재 순위를 보증하지 않는다. 기존 부모 선택 대기보다 사용자의 이번 구조 재검토 지시가 우선한다.
- 제출은 현행 소유자 전용. blind 7240–7255 보존. 기존 후보·캠페인·러너 계약 불변. 로컬 실행은 이번 사용자 지시에 따라 Codex가 수행하며 다른 캠페인과 겹치지 않는다.
- 계산 원칙: 먼저 기존 자료와 작은 재현 검사, 다음 발동·기전 확인, 그 뒤 넓은 평가. CPU 부하와 실행 중인 작업을 보고 최대 8워커부터 사용한다. 큰 출력·반복 원문 읽기·무효 후보 전수평가는 피한다.

## 문서 지도

- [과거 C 원장](#c-history): c300 이전 보관 이력. 앞으로 여기에 새 작업을 쌓지 않는다.
- [Claude 원장](#o-history): 다른 작업자의 기록. Codex 새 작업은 이 파일에만 쓴다.
- [공통 실험 이력](docs/experiment-history-and-lessons.ko.md): 선행 시도와 재시도 조건. 부정확한 실험을 바로잡는 재검증도 정당한 재시도다.
- [c300 연구/검증 문서](docs/c300-research.ko.md): 가설·검증 계약·확인 결과·다음 결정. c300 관련 상세는 여기에 모은다.

## 작업 기록

- 2026-09-19 착수: 사용자 위임에 따라 c300 번호 사용, Codex 원장을 이 파일로 분리. 기존 작업 프로세스 조회에서 python 실행 없음. 첫 감사 대상은 `fastgame`의 공유 관측 참조/검증 우회와 native 실행의 차이, 캐시 키의 실행기 누락, 역사적 라이브 점수의 시점 문제. 아직 오류가 성능을 바꿨다고 확정하지 않음.

</details>

<a id="c-history"></a>
<details>
<summary>C 역사 원장 전체</summary>

# c 시리즈 작업 로그

> c300부터의 새 Codex 작업은 [c-working.md](#c300-history)에 기록한다(사용자 지시, 2026-09-19). 이 파일은 과거 원장으로 보존한다.

GPT/Codex 계열 후보와 검증 결정을 공유하기 위한 짧은 작업 원장이다. 상세 근거는 각 dated report와 `HANDOFF.md`에 둔다.

> **역사 원장 안내(2026-09-19):** 아래 09-15 상태표·명명 규칙은 당시 기록이며 현재 지시가 아니다. 현재 상태는 [HANDOFF START HERE](HANDOFF.md), 후속 결과는 [O 원장](#o-history)을 함께 본다. 새 실험 전 [실험 이력과 재시도 조건](docs/experiment-history-and-lessons.ko.md)을 읽는다. `c-working.md`가 아니라 이 파일이 C 원장이다.

명명 규칙: `c번호`는 GPT/Codex, `o번호`는 다른 세션(Claude) 후보다. 부모가 o 계열이어도 GPT가 개발하는 후보는 c번호를 사용한다. 설계·구현·검증 상태는 번호와 별도로 표시한다.

## 과거 상태표 (2026-09-15 기준, 보관용)

제출된 c 기준선은 **c129** (`agent/c129_feed_liquidity.py`, Kaggle ref `56209242`, 마지막 확인 public 2820.3)이다.
후속 로컬 기준은 c150에서 출발했으며, 교차 세션 결과상 o162와 o178이 이를 넘어섰다. o 계열 세부 진행은 [reports/o-working.md](#o-history)가 원장이다.

| tag | 파일 | 변경 유형 | 핵심 근거 | 상태 |
|---|---|---|---|---|
| c110 | `agent/c110_reserve8.py` | 기준 로직 | V37 계보 초기 강한 기준 | 과거 기준 |
| c111 | `agent/c111_opening_rescue.py` | 오프닝 로직 | 로컬 개선 뒤 라이브 첫 패배 시점 악화 관측 | 과거 제출 |
| c117 | `agent/c117_pasture_sale12.py` | 복합 로직 | pasture/sale12/yarn-pet/terminal 결합 | 과거 제출 |
| c125 | `agent/c125_livestock_margin_terminal.py` | 급식·종반 로직 | 구조적 패배 원장 기준 모델 | 과거 챔피언 |
| c129 | `agent/c129_feed_liquidity.py` | 급식 유동성 | 64 미사용 시드 확인 후 제출; ref 56209242 | 제출 c 기준선 |
| c132 | `agent/c132_cow_care_margin.py` | 소 경제성 | 우유 수요·급식 비용 가설 | 진단 계보 |
| c139 | `agent/c139_partial_seed_cash.py` | 오프닝 현금 | 합성 개선, 반응형 패널 무동작/회귀군 | 기각 |
| c146 | `agent/c146_carrot_sched3.py` | 당근 일정 | 47 동결 경기 4개 개선·43 동일·0 악화; 반응형 일반화 부족 | 진단 후보 |
| c147 | `agent/c147_feed_commitment.py` | 첫 급식 실행 연쇄 | 구매→픽업→배치→급식 연결 보정 | 미확정/제출됨 |
| c150 | `agent/c150.py` | 통합 기준 | o/r 개발의 불변 부모 | 로컬 부모 기준 |
| c151 | `agent/c151_shop_forecast.py` | 상점 예측 | 128경기에서 c146 대비 마진 -4,332 | 기각 |
| c152 | `agent/c152_shop_expansion.py` | 상점 확장 | 라이브 2682.9; 강한 개선 근거 부족 | 제출·기각 |
| c153 | `agent/c153_urgent_feed_exact1.py` | 첫 급식 복구 | 1,792 반응 경기에서 c129와 완전 동일; 기전 경기만 개선 | 무동작/제출 |
| c154 | `agent/c154_maintenance_feed.py` | 유지 급식 | 고정 기전 3쌍 모두 악화, 합계 마진 -577 | 기각 |
| c155 | `agent/c155_milk_externality.py` | 우유 외부효과 | c150 대비 screen +3.47%p, 작은 양의 신호; o162 위 적용은 무동작 | 보류 |

## 검증·승격 원칙

- 새 후보마다 검증기를 만들지 않는다. 기본 확인은 `tools/run-validation.ps1`과 `tools/validation_v1.py`를 재사용한다.
- 같은 시드·상대·양 좌석에서 부모와 paired 비교하고, 후보/엔진/대진 해시를 고정한다.
- 동결 상대·고정 상점 결과는 기전 확인에 사용하고, 반응형 상대의 일반화 성능과 구분한다.
- 요청 telemetry를 실현 생산·판매로 해석하지 않으며, 승패와 평균뿐 아니라 승→패·하위 꼬리·오류를 본다.
- 사용자가 시뮬레이션을 실행하고 이 세션은 설계·코드 검토·완료 결과 분석을 담당한다.
- 제출 전 패키지의 단일 `main.py`, 로컬/서버 archive와 source 해시를 재확인한다.

## 2026-09-15

- 사용자 지시에 따라 신규 후보 탐색은 c171에서 종료했다. c172는 설계·파일 모두 만들지 않았으며, 검증 집합은 o182와 구현 완료된 c156/c160/c163/c168/c170/c171으로 고정한다. 공통 1,344경기 screen은 Check와 모든 소스 해시가 통과했지만, 다른 세션의 o207 worker tree가 실행 중인 동안에는 시작하지 않는다.
- o182를 불변 부모로 c156, c160, c163, c168, c170, c171을 구현 후보로 확정했다. c159은 타일별 안전 검사를 최고 경로 선택 뒤 적용해 안전한 차선 경로를 놓치는 반례가 있어 c170이 대체한다. c167은 step-648 cold start와 telemetry, c169는 malformed shop type 경계 때문에 c171이 대체한다. 기존 산출물은 덮어쓰지 않았다.
- 생존 후보 6개와 중간 후보의 계약 테스트를 합쳐 78 passed, 모든 전용 빌더의 byte-identical 재실행과 manifest/부모 해시를 확인했다. 실제 reacting 성능은 아직 0경기이며 promotion=false다.
- 공통 v1 발동·건강성 화면 1,344경기를 `configs/validation/c156-c171-activation-screen-20260915.json`과 `state/agent_experiments/c156_c171_activation_screen_20260915/`에 Prepare/Check했다. 모델 7 × 독립 family 상대 8 × 새 seed 12 × 양 좌석, 8 workers다. 실행·결과 분석 전에는 어느 후보도 개선으로 부르지 않는다. 상세: `reports/c156-c171-implementation-and-screen-2026-09-15.ko.md`.

- 규칙 재감사로 c156~c162 설계를 개정하고 c163~c167을 예약했다. 상세: `reports/c156-c167-rule-audit-and-candidate-design-2026-09-15.ko.md`. 우선 c156(생산 상한·CARE 적립 수확), c163(무가치 CARE→비료 수거), c164(시비→물주기 순서); 큰 변경은 c167(V42 신규 생산 경로)로 분리한다. c165=지속 작물 WATER 재배정, c166=상점 소비 직후 소량 매도다. 모두 설계 상태다.
- **c161 정정**: 공식 엔진에는 일꾼 가방 상한이 없다. 이전 가방 용량 설계는 철회하고 낮 시간 DROP 손실을 부분 PLACE로 막는 조건부 후보로 변경했다. c157/c158/c161/c162는 구체적인 잔여 실패가 확인될 때만 구현한다.
- 기존 계보의 선택된 실제 패배88개를 파일만 읽어 감사: CARE 미적립 2,155 타일·일, 일말 상한 초과 생산 최소1,319개, 물주기 뒤 시비 잠재 지점449건. o181 궤적의 측정값이나 회수 가능한 이득은 아니다. o181 저장 진단88행에서는 o171 mismatch0, 비료 투입 오류0. 원본·분석은 `state/research/c156_rules_20260915/`에 보존했고 신규 경기는 실행하지 않았다.
- 장기 부재 8~9시간용 최초 후보 예약(이후 위 규칙 감사로 개정): c156 전환 가축 생산달력, c157 전환 실행 미완료 복구, c158 중복 현장 작업 제거, c159 동일 비료 예산 내 배분, c160 회수 불가능한 마지막 작기 투입 차단, c161 가방 용량 기반 수확(가정 오류로 철회·설계 교체), c162 시장 주문 슬롯 배분. 2026-09-15 당시 agent/reports/configs/tools 및 HANDOFF에서 번호 충돌을 확인했다. 모두 설계 상태이며 구현·성능 검증 완료를 의미하지 않는다.
- 부모는 o181을 우선 가정하되 검증된 우월성을 전제하지 않는다. o178 대비 회귀가 확인되면 후보를 o178 위 별도 빌드로 다시 확인한다. 기존 보호/플래너가 이미 처리하는 경우는 새 후보로 만들지 않으며, 각 가설의 발동과 실제 손실부터 확인한다. o174의 급식 순서·자금, o177 곡물 보유, o182 새벽 초과·atomic 파종 기능은 중복 구현하지 않는다.
- 검증 예산은 후보 수보다 발동 확인→소형 반응형 비교→미사용 시드 확인 순서에 배분한다. 공통 검증기 재사용, 전체 8워커 상한, Claude 큐와 겹치지 않는 단일 실행 큐. 이번 요청에서는 설계만 기록했으며 구현·경기 실행·추가 제출은 하지 않았다. 제출 금지 유지.

- 공통 검증기를 규격화했다: 설정 JSON만 추가하며 경기별 새 subprocess, 8워커, 진행률/ETA/캐시/알림을 제공한다.
- c155/o160 1,152경기에서 c155는 c150 대비 작은 양의 신호였고, o160은 승률이 높았으나 손실 꼬리가 악화됐다.
- 분해 검증 1,600경기에서 o162가 280승40패로 최상: o160 대비 승→패0, 하위10% 마진 개선. 후속 로컬 기준으로 선택했다.
- r000 종반 보유 512경기는 주 가설인 딸기·토마토 보류가 무동작이었고 승점률이 감소해 기각했다.
- o178은 o162 위 상점별 가축 전환을 결합했으며, 동결88경기와 반응형21상대 풀을 통과해 현재 제출 1순위다.
- o178/o181 공통 확인 3,072경기는 비용 대비 과해 실행하지 않기로 사용자와 결정했다.
- o178 패키지를 준비한 뒤 제출 명령이 사용자 중단으로 취소됐으나, 취소 전에 Kaggle이 ref `56241248`을 `PENDING`으로 접수했다. 이후 제출 명령은 실행하지 않는다. 소스 SHA `9a3960aa0628d5585c7af2f5b30b062e3c4838e24072a1a22894ab61f79e010d`, 로컬 archive SHA `52c129bb317aea0efcd56779a14858b4984d11e8ecc66ee2176d23b825aaced4`.

</details>

<a id="o-history"></a>
<details>
<summary>O 역사 원장 전체</summary>

# o/r 시리즈 작업 로그 (다른 세션 공유용, 항목당 1~2줄)

기준: o162 = c150 + 급식 게이트(0.6) + 거위 수확(≥3). 검증 절차 `docs/o-validation-process.ko.md`.

> **현재 상태는 `HANDOFF.md`의 START HERE(2026-09-19)를 본다.** 이 파일은 시간순 로그(항목당 1~2줄, 실제 시각)이며, 최신 항목은 파일 끝에 있다. 아래 '과거 상태표'는 2026-09-15 tape 시대의 보관 자료다.

새 실험 전 [실험 이력과 재시도 조건](docs/experiment-history-and-lessons.ko.md)을 읽는다. [C 원장](#c-history)의 준비 기록 이후 결과도 이 로그에 있으므로 양쪽에서 후보 ID를 검색한다.

## 과거 상태표 (2026-09-15 17:40 기준, 보관용 — 현재 상태 아님)
메인 후보 = **o199c** (`agent/o199c_carrot_price2.py`, 제출 ref 56247532). 계보: c150 → o162(+1,180) → o178(+2,888) → o182(+3,576) → o199c(+3,662, 58/88). 판정 = 스위트(88경기, o162 대비 paired CI) → 풀(lean 21상대). 상태: ✅완료 / 🔄진행중 / ⏳대기(큐에 있음) / ❌기각 / ⛔무효(재실행 필요)

| tag | 파일 | 내용 | 스위트 vs o162 | 풀 | 상태 |
|---|---|---|---|---|---|
| o168a/b, o169 | 시비 게이트 / 분할매도 | 파라미터 | +82 n.s. / −46 n.s. / −681 | −256 / −295 / −444 | ❌ |
| o170a | `o170a_day10.py` | 10일차 거위→양(YARN)/소(계란0·우유≥2) | **+502 [+71,+984]** 8/1 | ⏳ 큐2 | 🔄 |
| o170b | `o170b_day10_cow.py` | 소 조건 완화(우유≥2) | +489 [−43,+1,095] n.s. | — | ❌ |
| o170c | `o170c_day10_milk3.py` | 소는 3상점 전부 우유일 때만 | **+486 [+150,+888]** 6/0 | +1,397, 21/21 개선 | ✅ 두 관문 통과 |
| o171a | `o171a_day6.py` | 6일차 소2→거위2 (첫 2상점 우유 없음) | **+826 [+561,+1,107]** 11/0, 30경기 중 29 양수 | ⏳ 큐2 | 🔄 |
| o171b | `o171b_day6_egg.py` | + 계란 상점 필요 | +669 [+424,+931] 7/0 (a의 부분집합) | — | ✅ a보다 약함 |
| o171c | `o171c_day6_all.py` | 상점 조건 없이 항상 | −722 [−1,559,+85]; 우유상점 0/1/2개 세계별 +2,422/−572/−7,475 → 상점 규칙이 본질 | — | ❌ |
| o171d | `o171d_day6_all4.py` | 항상 + 7일차 소2도 거위(총 4) | −3,295 [−5,147,−1,508] | — | ❌ |
| o171e | `o171e_day6_4.py` | 상점 조건 + 4마리 | **+1,185 [+687,+1,715]** 15/2 | +344; 동급·챔피언 +566~+808, 카나리아(5만점대 압승) −750 | ✅ 두 관문 통과 |
| o172a/b | `o172a_tomato1.py` / `o172b_tomato2.py` | V219 토마토 게이트 상점 3→1/2 | 재실행: −360 [−581,−160] / −159 [−345,+1] | — | ❌ 토마토는 상점 3개 조건이 맞음 |
| o173a | `o173a_no_c126.py` | C126 급식버퍼 제거 | −91 [−232, 0] n.s., 84/88 동일 | — | ✅ 중립(제거 가능하나 이득 없음) |
| o173b | `o173b_no_c124.py` | C124 급식생략 제거 | −1, 86/88 동일 | — | ✅ 죽은 오버레이(o159가 대체) |
| o173c | `o173c_no_c115.py` | C115 미러예약 제거 | −98 [−260,+50] n.s. | — | ✅ 유지(약한 양의 기여) |
| o173d | `o173d_no_v219.py` | V219 토마토 제거 | **−1,969 [−3,463,−763]** (발동 12경기 평균 −14k) | — | ✅ V219는 핵심 → 확대(o172) 유망 |
| o181 | `o181_combo.py` | **조합 o178 + o174 + o177** | c150 대비 **+3,322 [+2,639,+4,026], 52/88**; o178 대비 +434 유의 | o162 대비 +2,133, 21/21; o178 대비 +282, 20/21 | ✅ 두 관문 통과. 홀드아웃 27/40 (+4,942) |
| o182 | `o182_combo_overflow.py` | o181 + V43 r148 새벽 창고 초과분 회수 | c150 대비 **+3,576 [+2,874,+4,277], 58/88**; o181 대비 +237 [+201,+274] 68/1 | o162 대비 +2,289, 21/21 | ✅ **제출 후보 1순위**. 홀드아웃 27/40 (+5,175 [+4,008,+6,337]; o181 대비 +232, 36/0) |
| o184 | `o184_goose6.py` | o181 기반, 거위 6 | −184 n.s. 1/10 | −166 | ❌ 거위 4가 최적 |
| o185a/b | — | 양모 루트 10일차 양→거위 | 스모크 −5.2k(외부효과) | — | ❌ 삭제 |
| o186 | `o186_tet_feed.py` | 테츠타니 급식 블록 | −221 [−268,−177] | −115 | ❌ |
| o187a/b | 급식 0.5 / 0.75 | 재튜닝 | −225 / −298 유의 | −217 / −198 | ❌ 0.6 확정 |
| o188 | `o188_goose4.py` | 거위 수확 임계 4 | +5 n.s. | −13 | ❌ 3 확정 |
| o189a/b | o181 − o174 / − o177 | ablation | −335 [−664,−82] / −105 [−164,−50] | | ✅ 두 부품 모두 실기여 |
| o193 | `o193_no_v233.py` | V233 제거 | −578 [−1,114,−22] | −420 | ❌ V233 유지 |
| o196a/b | — | 수요 없는 소/양 조기 포기 | 스모크 −5.7k~−8.9k(외부효과) | — | ❌ 삭제 |
| o197 | o184 + 창고회수 | 조합 | +24 n.s. | −38 | ❌ |
| o183, o190 | — | 3일차 소 거위화 / V219 현금 게이트 | 폐기(축사 시점·13/13 발동 확인) | | ❌ |
| **o199c** | `o199c_carrot_price2.py` | **밀→당근 스위치(당근가≥2×밀가)** = o182 + o199c | 전체 +86 n.s.; **발동 19/128경기 평균 +1,927(15/19 양수), −34k 당근 세계 +18.8k**; 홀드아웃 +727 | 0 (풀에선 미발동) | ✅ **새 메인 후보** (b: 2.5× 발동 11경기 +1,981) |
| o200 | o197 + o199b | 조합 | +56 n.s. | −38 | ❌ (o184 부품 때문) |
| o183, o198 | — | 3일차 소 거위화 / 딸기 기회 시비 | 폐기(축사 시점 / 격일 급수) | | ❌ |
| o179a/b | `o179a_yarn_cows.py` | 양모 루트 양→소 | 스모크 −5k~−22k(상대 양모가 +19k) | — | ❌ 큐 미투입 |
| o180 | `o180_c155_on_o162.py` | c155 외부효과 급식 게이트 | 무동작(전부 gross_edge 차단) | — | ❌ 큐 미투입 |
| o178 | `o178_goose4_day10.py` | 조합 o171e + o170c | c150 대비 +2,888, 48/88 | o162 대비 +1,851, 21/21, 16W 0L | ✅ 홀드아웃 26/40 (+4,552) |
| o174 | `o174_tet_funding.py` | 테츠타니 자금·주문순서 꼬리(r97/r124/r127/r128) | +296 [+65,+601] 4/0 | 동급·챔피언 양수, 5만점대 카나리아만 −170 | ✅ o181 부품 |
| o175 | `o175_tet_survival.py` | 테츠타니 r60 생존 가드 | −275 [−361,−200] W→L 8 | — | ❌ |
| o176 | `o176_tet_inputs.py` | 테츠타니 입력 플래너 보강 | 0 (88경기 동일, 무동작) | — | ❌ 무동작 |
| o177 | `o177_tet_grain.py` | 테츠타니 EXP226 곡물 보유 | +124 [+72,+180] | +278, 21/21 | ✅ o181 부품 |

큐(사용자 PC, 순차 실행): 큐1 `o_results/batch_layer3_suite.txt`(o170~o173 스위트) → 큐2 `batch_layer3b_suite.txt`(o170c·o171c/d/e 스위트) + `batch_layer3_pool.txt`(o170a·o171a 풀) → 큐3 `batch_tetsutani_suite.txt`(o174~o177). 큐4 `batch_layer4.txt`(o178 스위트+풀, o170c·o171e 풀) → o172a/b 재실행 `batch_o172_suite.txt` → 큐5 `batch_layer5.txt`(o181 스위트+풀, o174·o177 풀) → 홀드아웃 `batch_holdout.txt`(elite2 40경기: c150/o162/o178/o181) → 큐6 `batch_final_pool.txt`+`batch_holdout.txt` ✅ → 큐7(장기 부재 배치) `batch_layer7.txt`/`batch_layer7_holdout.txt`/`batch_pool32.txt`: 12후보(o184 o197 o188 o187a/b o193 o186 o189a/b o199b/c o200) 스위트+풀 → 홀드아웃 → c150·o162·o181·o182 32시드 풀. ✅ 완료 13:05. 큐8~10 ✅. 큐11(정책표 컴파일→o209) 🔄 → 큐12(o206 관문) → 큐13(c-시리즈 6종). o206 관문은 별도로 즉시 실행 중(`batch_o206_now*.txt`). **현재 메인 후보 = o199c** (`agent/o199c_carrot_price2.py`).
홀드아웃 = 09-15 08:41 크롤로 받은 **새 2750+ 패배 40경기**(`o_replays/elite2_chunks/`, 기존 88과 겹침 0, 후보 선택에 사용 안 함). 결과 `o_results/elite2_suite/`, 요약 `suite_summary.py <tag> <base> elite2_suite`.
요약 명령: `python o_tools/suite_summary.py <tag> o162`, 풀: `python o_tools/compare_pool_results.py o_results/pool_pool_lean_vs_o162 o_results/pool_pool_lean_vs_<tag>`.
주의: `o_tools/build_overlay.py`가 이제 "마지막 callable == agent"를 검사함. 오버레이 끝은 반드시 `agent = globals().pop('agent')`. o171a 스위트는 플래그 추가 전 빌드(sha 98210629)로 측정됐고 현재 파일(e66ff461)은 기본값이 동일 동작(3시드 액션 일치 확인).

## 2026-09-15
- o162 엘리트 스위트: c150 대비 +1,180 (CI [+952,+1,413]), 패→승 28/88; o159b 대비 +278 유의. 기준 후보로 확정.
- 1층 튜닝 6종(o163 시비 일꾼 3, o164 종반 보유, o165a/b 급식 임계 0.5/0.75, o166 거위 임계 2, o167 최근최고가 평가) 스위트: 전부 o162 이하. o162 파라미터가 국소 최적. o164 −18, o166 −159, o167 −241 유의 악화.
- 검증 풀 51→21(lean: 동급 8 + 옛 챔피언 c125/129/146/147/152 + 카나리아 7), 시드 8. 후보당 424경기(~10분). 공개 Farming Score V4·Market-Smart 최신판(09-15)으로 교체 — c150 상대 2승 6패로 동급 확인.
- 좌석 효과 측정: 528 paired 쌍 평균 −55(CI 0 포함), 4%는 |차|>1,000 → 양 좌석 유지.
- 2층 후보 구현: o168a/b(EXP182 시비 게이트 가치비 1.2/1.0·시작 12/10일), o169(딸기·우유·양모 매도 배치 6 캡+드립). 2시드 게이트: o168 시드별 −1,200~+600, o169 −200~−600. 스위트 대기.
- 역공학 r000(종반 보유) 스위트 결과: o164로 측정 시 −18 → 1위 메커니즘은 우리 계보 덤핑에 의존, 채택 불가.
- 2층 결과(o162 대비 스위트 / lean 풀 평균): o168a 시비 1.2 +82 n.s. / −256(미러·동급 악화), o168b 시비 1.0 −46 n.s. / −295, o169 분할매도 −681 유의(W→L 13) / −444. 전부 기각. 파라미터 튜닝 종료.
- o162 lean 풀 c150 대비 +640(21/21 상대 양수, 최신 공개 트리오 +911, 미러 +1,061) → 동결 스위트 이득이 반응 상대에서도 유지 확인.
- 엘리트 88경기를 상점 구성으로 분해: 계란 상점 0(5경기)·딸기 6(6경기) 0승, YARN 2(17경기) 18%, 우유 5 세계 o162 이득 소멸. c150 상점 대응 = 6일차 YARN 쌍 라우팅 1회뿐(64쌍 중 15개) → 수요 쏠린 세계에서 고정 포트폴리오가 짐.
- 새 논리 후보 구현(전부 o162 위): o170a/b 10일차 거위 3마리 블록 → YARN 관측 시 양, 계란상점 0·우유≥2(b: 우유≥2)면 소 (구매·픽업·배치·축사 일괄 치환, 현금 미달 시 유지); o171a/b 6일차 소 2 → 거위 2 (첫 2상점에 우유 상점 없을 때, b: +계란 상점 필요; 고정 일정 7건 치환, 위치 검증); o172a/b V219 토마토 게이트 상점 3→1/2; o173a~d 삭제 ablation(C126 급식버퍼, C124 급식 생략, C115 미러 예약, V219 토마토). 스모크: o170 소 치환 시드별 +8.2k/−2.7k, o171 3/3 시드 +1.1k~+3.6k.
- 3층 1차 결과(o162 대비 스위트): **o171a 6일차 소2→거위2(첫 2상점에 우유 상점 없을 때) +826, CI [+561,+1,107], 발동 30경기 중 29 양수, 패→승 11/0** — o162 이후 최대. **o170a 10일차 거위→양(YARN)/소(우유3) +502, CI [+71,+984]**: 양 치환 8경기 +2,344, 소 치환 13경기 +1,959이나 소는 최종 우유 상점 ≤3이면 −2~−5k. o170b(소 조건 완화) +489 n.s. → o170c(소는 알려진 3상점 전부 우유일 때만) 빌드.
- 실측(o162 4경기 평균): 체결가/기준가 양모 43%·우유 70%·비료 42%·딸기 93%(하루 30~84개 덤핑, 최저 $1) vs 계란 110%·당근 139%·밀 167%. 급식+돌봄 커버리지는 이미 거의 완전(소 162/210일), 유휴 PASS 498턴 중 일몰까지 미해결 기회 ~75턴뿐 → 노동 최적화 여지 작음. 남는 지렛대는 세계별 공급-수요 매칭.
- 테츠타니 Market-Smart(09-15) 분석: 우리 c-계보와 같은 공개 섀시(EXP182까지 코드 공통, `_router`·V219·V231·R36/R37·V233 동일), 꼬리 오버레이만 다름(그쪽: EXP193/216/217/219/226/231, r68/70/79, r124/127/128, r60; 우리: REPAIR/CP0/C115/C116/P0/C124/C126 + o159/o162). 스펙의 "정확 재고 투영·클램프·작물전환 게이트"는 c150에 대상 코드 없음(작물 전환 미탑재, projected_shed는 양쪽 동일) → 대신 테츠타니 고유 꼬리를 그룹별로 o162에 그대로 이식해 검증: o174(자금·주문 순서 r97/r124/r127/r128), o175(r60 생존 가드), o176(입력 플래너 보강 EXP193/r68/r70/r79), o177(EXP226 곡물 보유). 급식 그룹(EXP216/217/219)은 o159와 충돌 위험으로 보류. 스모크: 오류 0, o162 대비 변경 스텝 0~11.
- o171b +669 [+424,+931](reports/o171a 부분집합, a가 우월). o173a(C126 제거) −91 n.s.(84/88 동일) → 중립. o172a/b 첫 실행 무효: 오버레이가 `def _v219_qualifies`로 끝나 Kaggle `build_agent`(마지막 callable 선택)가 그 함수를 에이전트로 호출 → 전 경기 $3,000. 모든 오버레이 끝에 `agent = globals().pop('agent')` 추가, 빌더에 검사 추가, o172·o174~o177 재빌드, o172 결과 삭제(재실행 필요).
- 검증 속도: replay_lab에 원본 게임 재현 캐시(env `KAGG_VERIFY_CACHE`, 결과 동일 확인 12s→7s/경기), 스위트 6→12청크(`elite_chunks12`, 기존 c0..c5 결과 유지), 풀 워커 8→12. run_batch.ps1 기본값 반영, 큐2부터 적용. CPU 8코어/16스레드 98% 포화라 로컬 추가 병렬화 여지는 없음.
- o173b/c/d: C124 제거 −1(86/88 동일, 죽은 오버레이), C115 제거 −98 n.s.(유지), V219 제거 −1,969 유의(토마토 프로그램 발동 12경기 평균 −14k → 핵심 수익원, 게이트 확대 o172 재실행 가치 큼).
- 큐2: o171e(상점 규칙 + 거위 4마리) +1,185 [+687,+1,715] 15/2 → o171a(+826) 대체. o171c/d(상점 규칙 제거) −722/−3,295: 첫 2상점 우유 0/1/2개 세계에서 +2,422/−572/−7,475 → "초반 거위>소"가 아니라 "우유 수요 없는 세계에서만" 규칙이 본질. o170c(소는 우유 3상점일 때만) +486 [+150,+888] 6/0 → KEEP.
- 조합 o178 = o162 + o171e + o170c 빌드(3시드 상호작용 정상: 6일차 블록과 10일차 블록 독립). 큐4에 스위트+풀.
- o179a/b(양모 루트에서 9일차 이후 양→소, 우유 상점 ≥2/≥1) 스모크 3/3 참사(−5k~−22k) → 큐에 넣지 않고 기각. 분해: 우리 최종 현금은 −2.3k뿐인데 **상대(같은 계보) 현금 +19k** — 우리 양모 덤핑(최저 $1)이 사라지자 상대 양모가 $195에 팔림. 글럿 제품 덤핑은 같은 제품을 파는 상대의 수익을 깎는 무기이기도 함 → "글럿 공급 축소"류 아이디어(딸기 축소 등)는 미러·계보 상대에서 역효과 가능. 치환은 상대가 안 파는 제품(계란)으로 갈 때만 안전했던 이유.
- o180(o162 + c155 우유 외부효과 급식 게이트): 2시드에서 검토 28~50건 전부 gross_edge 차단(자체 손실 추정 2×우유 최고가 > 밀 절약) → 적용 0, o162와 동일 액션. 큐에 넣지 않음(무동작).
- 큐3/4 스위트: **o178(o171e+o170c) o162 대비 +1,707 [+1,094,+2,329] 22/2; c150 대비 +2,888 [+2,188,+3,588], 48/88 승** → 제출 기준선(+3,000·40/88)에 근접, 풀 대기. 테츠타니 이식: o174 자금·주문순서 +296 [+65,+601] KEEP, o177 곡물보유 +124 [+72,+180] KEEP, o175 생존가드 −275 기각, o176 무동작.
- o181 = o162 + o171e + o170c + o174 + o177 빌드(스모크 오류 0, 2시드 +0.9k/−0). 큐5에 o181 스위트+풀, o174·o177 풀.
- o178 lean 풀: o162 대비 평균 +1,851, 21/21 상대 개선, 회귀 0, 옛 챔피언 5개·공개 트리오 3개 전부 **16W 0L**(o162는 14W 2L). 두 관문 통과.
- 라이브 크롤(08:41): 새 2750+ 패배 40경기 확보(`elite_losses_new`, 기존 88과 겹침 0) → 홀드아웃 스위트 `elite2_chunks/`(12청크) 구성. run_batch `-ChunkDir/-SuiteDir`, suite_summary 3번째 인자로 홀드아웃 지원. 라이브 현황: 최신 제출 56231047은 2750+ 상대 2/17, 이전 제출들 ~50%.
- 공유 노트북 3종 검토: ashok205 archive(이미 사용), georgymamarin "2600+ farms"(데이터 대시보드, 전략 없음; 참고: georgymamarin/kaggriculture-episodes 전 경기 데이터셋·destbreso 45k 벤치마크 — 필요 시 크롤 대체 가능), ahmedberatozer V43(테츠타니와 같은 계보의 원저자 최신판; 새 것은 r148 "새벽 창고 초과분 회수"뿐, 저자 측정 +96~125/경기). 우리 실측 o178 새벽 초과 손실 ≈ 밀 7~10·계란 4·딸기 2/경기(~$300~750). r148을 o181 위에 이식 → **o182** (스모크 +85/+411, 회수 2~9단위, 오류 0). 큐6 대기.
- o172a/b 재실행: V219 게이트 상점 1/2로 완화 −360 유의 / −159 n.s. → 기각. 토마토 프로그램은 상점 3개 조건이 맞음(o173d: 발동 시 +14k는 그 조건 덕). o171e 풀 +344(동급·챔피언 +566~+808, 5만점대 카나리아만 −750, 회귀 기준 미달) 통과, o170c 풀 +1,397 21/21 통과.
- 큐6 결과: o181 풀 o162 대비 +2,133(21/21, o178 대비 +282); **o182(o181+창고 회수) 스위트 o181 대비 +237 [+201,+274] 68/1, c150 대비 +3,576·58/88, 풀 +2,289 21/21** → 제출 후보 1순위. o177 풀 +278 21/21, o174 풀 동급 양수(5만점대 카나리아 −170만).
- **홀드아웃(새 2750+ 패배 40경기, 후보 선택 미사용)**: c150 0/40 → o162 11/40(+1,070), o178 26/40(+4,552 [+3,508,+5,638]), o181 27/40(+4,942 [+3,789,+6,107]) → 88경기 과적합 아님, 새 패배에서 더 큼.
- 룰 재분석: 시장은 슬롯 단위 lockstep(양쪽 슬롯 0 매도 → 우선순위 지렛대 없음), 판매가 ≤$1이면 시장 재고 미증가(바닥 덤핑은 외부효과 없음), V219 현금 게이트 12k는 13/13 발동이라 비구속(o190 폐기), 3일차 소의 축사는 상점 전 건설이라 거위화 불가(o183 폐기). 우유 상점 없는 세계에서 남은 소 6마리 우유 체결가 $2~14(68/71 단위 기준가 절반 이하)·양모 $1~19 → **조기 포기 o196** 신설.
- 장기 부재 배치용 16후보 빌드(o184, o185a/b, o186, o187a/b, o188, o189a/b, o193, o196a/b, o195a/b/c). 스모크 진행 중.
- 스모크(c150 미러): o184 거위6 +1.8k(7007), o188 +247, o187a +86, o186 ≈0(급식 생략 0회), o189a·o193 해당 시드 무발동. **o185a/b 양모루트 양→거위 −5.2k, o196a/b 조기 포기 −5.7k~−8.9k** → o179와 같은 외부효과(우리 우유·양모 공급 감소 → 같은 계보 상대 가격 회복). 기각, 빌드 파일 삭제(o185·o196·o195). 교훈 확정: 글럿 제품 공급은 절대 줄이지 말 것(급식 생략은 가격 ≤$1 근처에서만 이득). o197 = o184 + 창고 회수 추가.
- o182 홀드아웃: c150 대비 +5,175 [+4,008,+6,337] 27/40, o181 대비 +232 [+180,+289] 36 better/0 worse → 세 관문 모두 통과, 현재 최강. 큐7(장기 부재 배치) 명령 전달: 9후보(o184, o186, o187a/b, o188, o189a/b, o193, o197) 스위트+풀 → 홀드아웃 → o182·o181·o162·c150 32시드 풀(`pool_lean32.json`, 결과 `pool_pool_lean32_vs_<tag>`).
- o183(3일차 소→거위) 최종 폐기: 배치가 3일차 마지막 시간(95스텝)이라 DIG+BUILD_COOP 삽입 불가, 거위 1마리 기대값 +180. o198(딸기 기회 시비) 폐기: 테이프가 딸기를 격일로만 물 줌(consecutive_unwatered==1에서 WATER) → WATER를 희생하면 잡초, 실제 기회 1회/경기.
- **홀드아웃 최악 −34k 분해: PET_CAFE×3 세계, 당근 가격 35→229(hinge), 상대는 당근 102칸(우리 31) 심어 323단위 ~$48k.** c146의 당근 전환은 18~25일·최대 8칸·인증서 조건이라 사실상 무동작(c150 vs c146 16무 원인). 새 논리 **o199 당근 스위치**: 당근 수요 6×(2PET+FM)≥24 또는 당근가≥2×밀가일 때 테이프의 밀 파종을 당근으로(씨앗 동반 구매, 3일령에 강제 수확 — 당근은 4일령부터 부패, 밀 수확 연령 2/3/4 = 36/54/70회), 초과 재고 매도 추가. 스모크 진행 중.
- o199 스모크: 수요 규칙(PET×2)로 대량 전환한 a는 −24k/−5k(밀 수입 $17k/경기 상실 + 사료 밀 구매, 당근가 53으로 붕괴) → 삭제. 3일령 강제 수확을 테이프 고유 당근(31칸)에도 적용한 버그 수정(우리가 바꾼 타일만). 가격 규칙만 남긴 **o199b(당근≥2.5×밀), o199c(≥2.0×)**: 미러전에선 0~3회 전환·중립(+48/+4). 실제 발동 여부는 동결 상대 스위트(−34k 세계 포함)에서 판정. 큐7에 추가.
- 구조물 배치 검증: BUILD_COOP/PASTURE 비용 0(빈 타일+턴 1), 병목은 매일 초기화되는 고용(피보나치: 10명 $143/일, 15명 $1,596/일). 엘리트 128경기 20일차: 우리·상대 모두 동물 17마리, 창고 거리 1.81칸(최대 3), 작물 4.6칸 — 상대 106/128이 같은 계보라 배치가 거울. 배치는 지렛대 아님; 차이는 마릿수·종류(o170/o171/o184 영역).
- o182 ㄴ자 구조물 배치 검증(재현): 153/155/156/159/160/161/177/182 BUILD→PLACE 전부 성공(거위 세계·소 세계·c150 동일 좌표 (5,4)(5,2)(6,2)(5,3)(6,4)(6,3)(7,4)), 128경기 o171_mismatch 0·오류 0, 빈 구조물은 7일차 5개(7~9일차 구매 대기용, 11일차까지 채워짐)뿐이고 20일차 0. 탈출 6건은 25~26일차 양 — c150도 동일(테이프가 마지막 생산 뒤 양 급식 중단, 의도된 동작). 버그 아님, 수정 후보 불필요.
- 배치 최적성: o182 20일차 동물 17마리 창고 거리 0:2 / 1:4 / 2:6 / 3:5(평균 1.82; 링 최밀 이론치 1.06), 일꾼 이동 2,882턴 vs 맨해튼 하한 2,839(비율 1.02 → 동선 낭비 없음). 동물 타일 작업 1,418/경기 vs 작물 ~1,700/경기라 "동물 안쪽·작물 바깥" 배치가 맞고, 완전 밀집으로 얻을 수 있는 상한은 이동 ~100~300턴(노동의 2~5%)이며 테이프 동선 재계획 없이는 회수 불가 → 오버레이 후보 없음.
- **o201 가축 EV 계산기** 구현: 6일차(소4)·8일차(양2)·10일차(거위3) 슬롯에서 종별 EV = 생산단위×투영단가(엔진 가격곡선 + 우리/상대 공급 − 상점 소비) − 구입비 − 사료비(급식계수) + **상대 손실**(우리 공급이 상대 제품 단가를 깎는 효과, 상대 점수 차감이라 가산) → argmax(마진 300/b:1000). 치환 스케줄은 o171/o184/o170 타일 매핑 재사용. 첫 버전은 외부효과 부호가 반대(비용으로 차감)라 전 세계 거위 선택 → 수정 후 스모크: 우유 3상점 세계 소×3슬롯 **+15,751**(o182 +9,009), 거위 세계 동일, (BAKERY,PIZZA) 세계 −3.6k(o182 +354; 우유 1상점 경계). 큐8: o201a/b 스위트+풀+홀드아웃.
- 코드 점검(o182~o201): 128경기 mismatch/오류 0, 스케줄 좌표 재검증 일치. 발견·수정: o201 외부효과 부호(수정 후 큐8), o199a 대량 전환(삭제). 미해결 소소한 비효율: o199 동반 당근 씨앗이 규칙 꺼진 뒤 남을 수 있음($20/개). **계보 회귀 발견**: 108629651(ICE,YARN,SMOOTHIE, V233 6양 발동) 기록 원본 144.7k vs c150/o182 123.7k(−21k) — c150 자체가 조상보다 못함, o193(V233 제거) 결과로 판정.
- o182 패배 원인(128경기 43패): 양모루트 9/19승·손실합 −48.6k(상대 5/6이 같은 계보 미러 → 시장 경주·V233 회귀), 우유1상점 세계 23/40(o171 미발동, o201 EV 대기), 거위 세계 37/44(−34k 당근 세계는 o199 대기), 우유2상점 16/25. o170c 스택 내 기여: 양 +3,087(6/8), 소 +4,996(5/5).
- 큐7 결과(o182 대비): **o199c 당근 스위치 KEEP** — 발동 19/128 평균 +1,927(15/19), −34k 세계 +18.8k, 홀드아웃 +727, 풀 회귀 0(미발동) → 새 메인 후보. 기각: o184 거위6 −184, o197/o200 n.s., o188 +5, o187a/b −225/−298(0.6 확정), o193 V233 제거 −578(V233 유지), o186 −221. ablation: o174 +335·o177 +105 실기여 확인.
- **32시드 풀(1,344경기)**: c150 68%(무승부 296) → o162 91% → o181 96% → **o182 97% (1300W 44L), 공개 트리오 186W 6L 평균 +3,519**.
- ahmedberatozer V43(09-15 최신, sha 919fc1d6, 이전 pull과 동일) 직접 대결 16시드×양좌석: **c150은 V43에 6승 26패(−1,824)** 로 밀리지만 **o182 22승 10패(+1,167), o199c 22승 10패(+1,536)**. V43을 lean 풀에 추가(22상대) — 다음 풀부터 기준선(c150/o162/o182)도 재실행 필요.
- 큐8 o201 EV 계산기: 전체 −641/−329 n.s., 홀드아웃 0, 풀 +690/+794(카나리아). 분해: (소,소,소) 12경기 +2,998(8/12, 우유 2상점 세계의 8일차 양→소)만 이득, 8일차 양→소 일반화(32경기 −1,031)·10일차 거위→양 EV 선택(7경기 −5,775)은 손실 → 양은 건드리면 짐(o179 교훈 재확인). **EV 모델보다 관측 규칙이 우월**, o201 기각. 남는 지렛대: "첫 2상점 모두 우유 → 8일차 양→소"(분산 큼, 후순위 o202).
- **메인 후보 갱신: o199c** = o182 + 당근 스위치. 다음: V43 포함 22상대 풀로 o199c·기준선 재실행 후 제출 판단.
- 라이브 패배 109149306(o182, YARN·PET 세계, 상대 같은 계보) 분석: 유일한 구매 차이 = 6일차 소2 vs 양2 — c150의 **C116**(루트10 YARN/PET에서 소쌍→양쌍) 때문. 이후 PIZZA×3·SMOOTHIE가 떠 우유 $191, 양모는 12+11마리 덤핑으로 $11 → 우유 −4.0k, 양모 +1.5k, 순 −2.7k. 6일차 2상점 정보로 양에 베팅한 것이 원인. **o202 = o199c + C116 무력화** 빌드(스위트 128경기 중 C116 발동 경기 수 확인 후 큐).
- o202(C116 무력화) YARN/PET 세계 6시드×양좌석 vs c150: **0승 12패 −3,961**, o199c(양 유지)는 10승 2패 +398 → 미러(양 상대)에선 양이 맞고(양모 덤핑 무기), 라이브 상대가 소를 고른 경기에서만 짐. 상대 구성에 따른 가위바위보라 C116 유지, o202 삭제. 발생 빈도 1.6%.
- **세계별 시드 은행 검증 도입(특수 검증, 기본 관문 아님 — 세계 겨냥 후보에만 사용)**: `o_tools/world_bank.py`(시드 7000~8500을 12일차까지만 돌려 첫 4상점으로 분류: goose/one_milk/two_milk/yarn 배타 + carrot(PET≥2)/tomato(≥3) 태그, 버킷당 36시드 → `o_tools/world_bank.json`), `o_tools/stratified_pool.py run <tag> <agent> / compare <tag> <base>`(상대 4: c150·V43·FSV4·MSF, 양좌석, (tag,bucket,opp) 캐시, 버킷별 paired CI → `o_results/strat/<tag>/`). 기준선 c150·o162·o199c 실행 중(백그라운드, ~40분).
- 라이브 패배 유형 분석(o182 15패/72, o178 14패/68, 둘 다 79% 승): **A 거위 베팅 실패 4건(o182, 합 −18k)** — 거위 세계인데 3·4번째 상점이 PIZZA/ICE라 우유가 올라 소를 유지한 상대에게 우유 −5.7~−6.8k(계란 +2~3k로 상쇄 못 함); **B 8일차 소 세계 2건(−5.2k, −6.3k)** — 첫 2상점 우유·상대가 8일차에 소2 구매, 우유 −4.7~−8.5k; **C 양모 루트 3건**(C116 베팅·미러); **D 미러 노이즈 18건**(구성 동일, 대부분 −1k 이내, 최대 −3.1k). 후보: **o203**(첫 2상점 모두 우유면 8일차 양2→소2, o199c 스택), **o204**(거위 4→2 헤지 = o171a). 큐9: 스위트·풀·홀드아웃 + 시드은행(거위/우유2 버킷 겨냥이라 특수검증 적용).
- D-2(매도 슬롯 순서)·D-1(상대 재고 조건부)은 c-계보 R37/V224가 이미 구현(매도 우선, 상대 가시 생산량으로 슬롯 순위) → 신규 후보 없음. C(구매 지연)는 테이프 일정 이동이 필요해 보류. 대신 **o205 10일차 헤지**: 거위 세계(o171 발동)에서 9일차 3번째 상점이 우유면 10일차 거위3→소3(유형 A 손실 4건 중 3건이 이 조건). 구현 중 o170 복제본의 전역 이름 충돌로 무한 재귀 → 접두사 분리, 빌더에 `_X_PARENT` 중복 검사 추가. 스모크 (PET,PET,PIZZA) +475. 큐9에 추가.
- 도구화: `o_tools/live_losses.py [--subs N | --sub id]` — 최근 제출의 **전 패배** 리플레이를 받아(캐시 `o_replays/live_recent/`) 세계·미러 여부·제품별 수익 차·첫 구매 분기·구간별 승률을 한 줄씩 출력(즉석 분석을 명령 하나로).
- 시드 은행 기준선(버킷당 36시드×상대 4×양좌석=288): **o162 vs c150** 거위 +1,941·당근 +1,442·우유1 +897·토마토 +649·우유2 +238 전부 유의, 양모루트 −320(V43·트리오에 −540, c150 미러엔 +337 → 급식 게이트가 반응 상대에겐 손해인 유일한 세계). **o199c vs o162** 전 버킷 유의 양수: 당근 +5,894, 거위 +4,727, 우유2 +3,326, 토마토 +2,009, 우유1 +650, 양모 +243; 승수 거위 186→240/288, 우유2 173→253, 우유1 204→232, 양모 232→242. 우유1(232/288=81%)·양모(84%)가 여전히 최저 버킷.
- **o199c 제출** (ref 56247532, 15:26, sha 1429673c…; 오늘 남은 슬롯 2). o203: 풀 +722 21/21, 홀드아웃 +993 유의 → 우유2 버킷 대기. o204: 스위트 −405·홀드아웃 −510 유의 → 기각. 라이브 패배 수집은 내일 `live_losses.py --subs 3`.
- 기록 128패 재대결: o199c는 o182와 동일 85승(새로 뒤집은 경기 0, 마진만 확대) → 남은 43패 = 우유1 17(−2,046)·양모 10(−4,858)·거위 7(−3,811)·우유2 9(−1,311). 구매 지연(C) 계산: 4마리 배치를 6→9일차로 미루면 생산 1~2회 손실 ≈ −$2~3.6k > 정보 가치(+390) → 폐기. 조합 **o207 = o199c + o205 + o203**, **o208 = o207 + o179a(양모루트·우유≥2면 후기 양→소; 미검증분 재시험)** 빌드(스모크 오류 0). 큐10: 스위트·풀·홀드아웃·시드 은행 + o199c/o207 32시드 풀.
- **A-1 착수: 가축 정책표 컴파일**. `agent/overlays/o209_policy.py` = o201의 슬롯 치환 기계 + 선택 = 표 조회(`_O209_TABLE`) → 없으면 손 규칙(o171e/o203/o205/o170c 동치; 스모크로 o207과 마진 동일 확인) → env `KAGG_O209_FORCE`로 강제(롤아웃용). `o_tools/compile_policy.py`: 비양모 첫2상점 28쌍 × 4시드 × 상대(c150, V43) × 양좌석 × 변형 10(기본 + 슬롯별 3종) ≈ 4,500경기 → 키(d6/d8: 첫2상점, d10: 첫3상점)별 평균 마진 argmax, 손 규칙보다 +200 이상일 때만 교체 → 표를 오버레이에 인라인 기록. 큐11: 컴파일 → o209 스위트·풀·홀드아웃·시드 은행 vs o207.
- o203(8일차 소, 우유2 세계) 시드 은행: 우유2 버킷 delta +547 n.s.이지만 **승수 253→198/288(−55)** — 마진 분산만 키우고 승률을 깎음 → 기각. o207/o208에서 o203 제거하고 재빌드(o207 = o199c + o205), o209 폴백의 d8도 SHEEP로 환원(표 컴파일이 키별로 COW를 시험함).
- 라이브 기록 활용 계획: ① `o_tools/live_suite.py`(신규) — 최근 제출들의 **전 경기(승+패)** 리플레이를 `o_replays/live_all/`에 모으고 `o_replays/live_chunks/` 12청크로 배치(run_batch `-ChunkDir o_replays\live_chunks -SuiteDir live_suite`) → 승리 경기의 W→L 회귀까지 보는 실전 분포 세트(~450경기); ② 정책표 컴파일을 롤아웃(c150·V43) 대신 이 기록 재생으로 전환(실제 상대 분포 대상); ③ 그 뒤 CPU 표(V219 커밋·초기 가축·급식 종×세계·당근 비율·매도 우선순위) 컴파일, 기준은 승수 우선. 5개 제출분 다운로드 진행 중(백그라운드).
- **관찰 통계 도구 `o_tools/branch_stats.py`**(리플레이 579개·양좌석 1,158행: 세계×6/8/10일차 구매 선택×상대 선택 → 승률). 결과: 거위 세계 4G 80%·4C 29%(우리 규칙 확인); **우유1 '4C+2G' 82%(n=97)·우유2 '6C' 87%(n=39)·양모 '2C+5S' 83% — 전부 Majkel1337(1위)**: 6~7일차에 6마리(우리 4), 8~9일차 소 3~4(우리 양 4). 우리 현금은 6~9일차 $578~2,300이라 추가 구매 불가(개막 테이프 고정) → 종 전환만 가능. o209 d8 슬롯을 8~9일차 양 4마리 전부로 확장(217/226 포함; 강제 COW 시 우유3 세계 +17,754 vs 9,009, 4마리 중 3마리 전환·mismatch 3은 시드별 일꾼 인덱스 차이로 안전 미적용). 라이브 전 경기 세트 수집 완료(`o_replays/live_all`, live_chunks 12청크).
- o205(10일차 헤지: 거위 세계+9일차 우유 상점→거위3→소3) 결과 o199c 대비: 스위트 −114 n.s.(뒤집힘 2/3), 홀드아웃 −177, 풀 +191, 시드 은행 거위 버킷 승수 240→248이나 delta −68 n.s., 당근 버킷 −177 유의 악화 → 기각. 유형 A(거위 베팅 뒤 우유 상점) 손실은 10일차 소 3마리로는 회복 안 됨.
- **o206(양모 루트에서 양 급식 생략 끄기) 시드 은행 yarn 버킷: +288 [+121,+471] 유의, 승수 242→267/288(+25)**; V43·FSV4·MSF 각 +505~512, c150 미러 −375. 스모크 2시드의 −1.1k는 노이즈였음. 스위트·홀드아웃·풀 관문 대기(큐12).
- 캐글 공개 노트북 조사(최근 60개): 우리와 겹치는 것 — (1) nathanjacob "Beyond V43"(상위 50팀 개막 144스텝 지문 클러스터링: 263팀→33클러스터, 81%가 v40 계보; C9 클러스터의 차이 = 0턴 밀 플립 제거 → V43 대비 96.5% 주장). 우리 테이프에 적용(o210)해보니 고용·가축이 이미 1턴에 있어 **현금 차이 $0~7, 마진 +1** → 무효, 삭제. (2) nathanjacob "How Many Twins"(같은 클러스터링 분석), (3) lynnsakurai Farming Score V5(잡초 동일일 복구 + 미러 확인 시 매도 순열 최적화 — R37과 같은 착상) → o199c 16승 0패 +3,386, lean 풀에 추가(23상대). (4) xuantianfengwu 계열(6소 배분기·종반 물류·4시 자금 배분·토지 배분 R10)은 별 계보, o199c 16승 0패 +11~12만(약함). alperen MetaCounter는 에이전트 셀 없음. 결론: 개막 지문이 같은 계보 안에서 차이는 극소, 우리 방향(세계별 분기·매도 순위)이 상위 클러스터와 일치.
- 다른 세션(c-시리즈) 후보 6종 확인: c156(생산 상한 선제 수확), c160(종반 지속작물 수확), c163(무가치 CARE→비료 수거), c168(FERTILIZE→WATER 순서), c170(비료 투어 재배정), c171(비-YARN 49쌍에 V42 상점별 생산 경로) — 전부 o182 위에 빌드(sha ef9d2aad 일치, c160만 구 빌드 748c 기준이나 동작 동일), 로더 마지막 callable = agent 확인. 큐13(큐12 뒤): 6종 스위트·풀·홀드아웃 vs o182/o199c. c171은 6일차 라우팅을 바꾸므로 o171e와 상호작용 확인 필요.
- 17:30 라이브: o199c 32경기(2400~2749 8/10), o182 101경기(2750+ 5/17), o178 93경기(2750+ 0/9). o199c가 낮아 보이는 건 경기 수 차이(신규 제출 레이팅 상승 중). 제출 계획: 1시간 뒤 o206(관문 통과 시), 6~7시간 뒤 통과분 조합본(o199c+o206+정책표/c-시리즈 통과분) 재검증 후 최종.
- o206 스위트 vs o199c: +1 n.s.(양모 루트 외 동일, 회귀 없음). 풀 13/23 진행.
- 개막 분석: 1위 7일차 동물 11(소 5.6·양 3.8·거위 1.7)·밀 2칸 vs 우리 8·밀 25칸 — 배분 차이 ≈ 경기당 $4.5~9k 추정. 개막 재탐색은 뒤 576스텝과 결합돼 B 규모(2~3주); "덧붙이기"(전담 일꾼+동물 2~3, V219 구조) 3~4일. 2주 마감 기준 후순위.
- o206 표준 관문: 스위트 +1 n.s., 홀드아웃 −36 n.s.(W→L 1), **lean 풀(8시드) −189, 21상대 중 20 악화(미러 −356, 트리오 −325)** — 시드 은행 yarn 버킷(+288, +25승)과 상충. 표본이 달라(8시드 vs 36시드×4상대) 확신 부족 → 1시간 뒤 제출 슬롯은 **건너뜀**, 최종 조합 전에 32시드 풀로 재판정.
- FSV5(lynnsakurai) 분석: 우리 계보(V43 꼬리 동일)에 r132(같은 날 잡초 복구 + **미러 확인 시 매도 순열 최적화**), r134(첫 2상점이 모두 계란 상점일 때 6일차 소2→거위2 — 우리 o171의 좁은 버전, 독립 발견), r151(정확한 삽입순서 창고 초과 회수, r148 개선) 추가. 우리 o199c가 16승 0패. r132·r151을 이식: **o211**(= o199c + r132), **o212**(= o211에서 r148 대신 r151). 스모크 오류 0. 큐14(c-시리즈 뒤).
- 검증 경량화: `o_tools/validate.ps1 -Tag -File [-Base o199c]` = 스위트 → 조기 기각 게이트(CI 상한<+50) → 빠른 풀 10상대(`pool_fast.json`; 카나리아 6·중복 챔피언 3 제거) → 홀드아웃. 통과 후보 ~5분·기각 ~1.5분(기존 ~12분). 기준선 풀 결과는 lean 풀에서 복사(같은 시드). 시드 은행·32시드는 최종 후보에만.
- 큐 재편(17:55): 대기 체인 5개 중단(o207/o208 시드 은행·32시드는 기각 후보라 낭비). 새 단일 체인 `o_results/lean_chain.txt`: 정책표 컴파일 → o209 → c156/c160/c163/c168/c170/c171 → o211/o212 (전부 `validate.ps1`, 조기 기각 게이트) → 32시드 풀 o199c·o206. 예상 ~2.5시간(기존 ~5시간).
- **Shadow planner 1단계 (관측 → 결정 경계)**: `o_tools/shadow_dataset.py` — 리플레이 788개·양좌석·6/8/10일차 슬롯 = 4,728행(상점 수요·가격·재고·현금·우리/상대 가축·남은 일수 → 실제 구매 종·승패). 승자의 선택 = 우리 규칙과 일치(d6 우유≥1 소 96~99%, 우유0 거위 52~64%; d8 양 60~80%; d10 거위 57~73%, 우유3 소 58%, YARN 양 65~78%). 상태별 P(승|선택): d6 우유0에서 거위* 76~92% vs 소 46%(상대가 소일 때), 상대가 거위여도 거위* 39~50% vs 소 14~17% → **상대 종과 무관하게 거위 우세(robust)**; d10 우유3 소* 79% vs 거위 34%; **o205 규칙(거위 세계+우유1 → 소)은 27% vs 거위 51%로 재확인 기각 → o209 폴백에서 제거**. 남은 가설: H2 d10 우유2→소(57% vs 44%, n=30/114), H4 d8 우유2→소(51% vs 48%), H5 d8 거위세계→거위(31%, 약함). `o_tools/shadow_cf.py`로 우리 실제 경기(동결 상대)에서 강제 재생 counterfactual 실행 중(`o_results/shadow/cf_log.txt`).
- 라이브 패배 수집(18:50): **o199c** 54경기 9패(2400~2749 23/30, 2750+ 0/2): 미러 5·양모 2·거위 1·우유1 1(−22.5k vs c0nrad: 0턴에 소3+양2 개막, 20일차 소 17마리, 딸기 −51k·밀 −20k — 규모형 이질 계보). **o182** 106경기 31패(2400~2749 46/65=71%, **2750+ 6/18=33%**): 미러 18·거위 베팅 6(합 −21k, 전부 상대가 소 유지+후반 우유 상점)·우유2 2(−14.2k vs ymg_aq(#2 클러스터): PIZZA×2 세계에서 **토마토 −15.9k** — V219는 토마토 상점 3개 필요)·양모 3·우유1 2. 2750+ 패배 18건 중 대부분이 마진 −3k 이내 미러 노이즈 → o211(미러 매도 순열)이 정확히 이 구간 대상.
- o209 업그레이드(반응형 구조): d8/d10 키에 **상대 6일차 종**(150스텝 스냅샷 대비 증가분) 추가, d8 결정을 150→**160스텝**(상대 155/156 배치 관측 후)으로 이동, `KAGG_O209_SHADOW=1` 모드(표 제안만 기록·폴백으로 행동), 텔레메트리 `o209_shadow_d*`=제안|폴백|사용키, `o209_disagree`. 판정 기준 선언: 표가 폴백 대비 승수 +5/128 미만이면 규칙 유지. 관측상 가축 선택은 세계 함수라 반응형 가치는 작을 것으로 예상 — 반응 논리의 실제 가치는 작물(토마토 2상점, 당근)·미러 매도 쪽으로 이동 예정.
- **매크로 플래너 계층 착수** (event → state → 후보 → robust 표 → override → 결정적 실행; 항상 KEEP=o199c): ① `o_tools/macro_compile.py` 공통 컴파일러(결정 무관: spec JSON{env, actions, key_tel, fired_tel}; 셀마다 support·paired delta·부트스트랩 CI·W/L 뒤집힘·승률 변화·상대 계통별 delta·최악 계통·발동 빈도; 채택 = support≥12 & CI 하한>0 & 승률 비감소 & 최악 계통 ≥ −150; dev 시드=은행 7000~8499, 홀드아웃 ≥9000 분리), `tools/o_arena.py`가 오버레이 텔레메트리를 경기 기록에 저장. ② **o214 토마토 커밋 규모 플래너**(후보 A): V219의 432스텝 결정에서 KEEP/SMALL(3칸)/MEDIUM(5칸) — V219 게이트·targets·씨앗 수량만 조정, 일꾼·판매 경로는 V219 그대로; 키 = 토마토 상점 수|가격|현금|밀 여유. 스모크 진행 중, 컴파일 spec `o_tools/specs_tomato.json`.
- **후보 A(o214 토마토 규모) 2단계 스크린 기각**: 발동 세계(토마토 상점 1~2)에서 SMALL(3칸) −5,474/−4,254, MEDIUM(5칸) −4,327/−4,071 vs KEEP +135/+863 (mechanics는 정상: 3/5칸 파종·판매 연결, 오류 0). 원인: V219는 SE 땅($4,000)을 사서 심는 구조라 10칸 미만이면 땅값을 못 갚음(3칸 수입 ≈ $1.8k). 다른 3구역엔 18일차 이후 빈 타일이 없어(작물 59.5+가축 17 ≈ 75칸) 땅 없이 심을 곳도 없음. ymg_aq의 +16k는 자기 땅의 작물 재배분(B 영역). → 토마토 규모 플래너는 SE 구매 자체가 기각 사유이므로 중단, 표 컴파일 미실행.
- H2 counterfactual(우리 실제 60경기, 동결 상대, d10 우유2→소): 평균 +1,411 [+237,+2,631]이지만 **W→L 12, 승수 59→47**, 상대 현금 −3,195 → o203과 같은 패턴(마진 분산↑·접전 패배) → 기각. 정책표 컴파일 결과: 오버라이드 14칸이나 support 1~4시드(4~16경기)로 robust 기준(≥12경기·CI 하한>0·승률 비감소·최악 계통 ≥−150) 미달, 게다가 재시작 전 롤아웃 10개가 구 폴백(o205 포함)으로 돌아 d10 기준선 혼입. **표 미채택, o209 = o199c 행동 유지. 가축 플래너 확장 중단**(사용자 기준: fresh 반응 아레나 승수 개선 없음). 이후 o209 validate 결과는 참고용.
- 큐 판정(19:25): o209(컴파일 표) 스위트 −405, W→L 5 → 기각 확정(o199c 유지). **c156(상한 선제수확)·c160(종반 지속작물 수확): 진짜 부모 o182 대비 88경기 전부 동일(무동작)** — 체인의 −86은 o199c의 당근 효과 차이일 뿐. c-시리즈는 o182 기반이라 판정은 vs o182로 읽어야 함(체인은 o199c 기준으로 돌지만 결과 파일로 재요약 가능).
- 큐 판정(19:45): **o211(FSV5 r132 미러 매도 순열+잡초 복구) 스위트 +57 [+22,+100] 유의, 15 better/0 worse, L→W 2, 풀 미러 +121·타 상대 0, 홀드아웃 0 → KEEP** (미러 전용 순수 이득). o212(r151 창고 회수)는 o211과 동일(+3) → r151은 r148 대비 추가 이득 없음, o211 채택으로 충분. c163 −94 n.s.·c168 무동작(−85=당근 차)·c170(비료 투어) vs o182 **+30 [+22,+40] 유의(52 better/2 worse)** 작지만 일관 → 조합 후보. **c171(V42 비-YARN 경로) vs o182: 승 58→67(+9, 우유1 세계 18→26)이나 평균 −927·최악 −24k(ICE,PIZZA)/−22.5k(FM,FM)/−17k(ICE,FM)** — 특정 쌍에서 V42 경로가 붕괴. c171의 `_C171_ROUTE_MAP`(첫2상점 순서쌍→V42 경로)을 시드 은행으로 쌍별 평가 후 **붕괴 쌍만 제거한 o215 = c171 + 쌍 가드 + o199c 당근** 계획. H4(d8 우유2→소) W→L 14·H5(d8 거위) −2,425 → 둘 다 기각(가축 종결).
- 32시드 풀(1,344경기): o199c 1300W 44L(+24,880) = o182와 승수 동일; **o206 1310W 34L(97.5%)** — 옛 챔피언 5개에서 각 +2승(58→60), 다른 상대 승수 동일, 마진은 −30~−80(카나리아)로 미세 감소. lean 풀 8시드의 −189는 표본 노이즈로 판명. **o206 채택**(양모 루트 양 급식 유지). 조합 후보: o199c + o206 + r132(o211) (+ c170 비료 투어, o182 기반이라 재빌드 필요).
- c171 시드 은행(거위·우유1·우유2 × 상대 4 × 양좌석) 쌍별 vs o199c: 43개 순서쌍 중 **16쌍 붕괴**(PIZZA+ICE n=51 −5,688 최악 −21k, PIZZA+SMOOTHIE −4,677, PIZZA+PIZZA −2,740 최악 −11k, BAKERY+PET −5,419 등), **27쌍 유지**(FM+PIZZA +1,852 승 16/8, BRUNCH+FM +3,154 승 18/8, PET+SMOOTHIE +1,179 승 24/16, ICE+FM +1,288 승 32/22 …). 가드 규칙: n≥8 & 최악>−8k & (승수>기준 또는 승수=기준&delta≥−300). **o215 = c171 + 쌍 가드 + 당근 + r132** 빌드. 체인3: o215 validate+은행, **o217 = o199c + o206 + r132(최종 조합 후보)** validate + 32시드.
- 체인3 결과: **o215(c171 가드 + 당근 + r132) vs o199c — 스위트 승 58→71(L→W 16, W→L 3), 홀드아웃 27→31(L→W 4, W→L 0), 은행 거위 240→268·우유1 232→286/288·우유2 253→264, 풀10 W/L 회귀 0(yhay 14→16W)**; 평균 마진은 +213 n.s.(꼬리: 스위트 (ICE,FM) −16.6k·(FM,SMOOTHIE) −9.5k 승→패, 홀드아웃 −5~−7.7k 마진 축소, 우유2 버킷 −205 유의). 오늘 최대 승수 개선. **o217(o199c+o206+r132)**: 스위트 +58(19/9, L→W 2), 32시드 1310W 34L(=o206). **o218 = o215 + o206** 빌드 → 체인4: validate + 32시드. 최종 후보는 o218(승수) vs o217(안전) 32시드 비교로 결정.
- **체인4: o218(c171 가드 경로 + 당근 + o206 + r132) 32시드 풀 1,344경기: 1328W 16L** (o217 1310/34, o199c 1300/44). 공개 트리오 각 62→64W(최악 경기 −2.9k → +0.2k), 옛 챔피언 5개 60→62W, 승수 감소 상대 0. 스위트 71/88(+13), 홀드아웃 31/40(+4). 128경기 오류 0, 최대 스텝 시간 정상. **최종 제출 후보 = o218.** 알려진 꼬리: 스위트 (ICE,FM)/(FM,SMOOTHIE) 승→패 2건, 우유2 버킷 마진 −205(승수는 +11).
- **o218 제출 → ref 56256113** (22:04, 오늘 1슬롯 남음). 코덱스 c180(o199c + c177 딸기2칸→토마토 레인 + c179 V219 재허용 + c180 딸기수요≤1 가드) 검토: 게이트 day11·토마토수요≥2·딸기수요≤1·가격≥60. **o219 = o218 + c177/c179/c180** 빌드(스모크 4경기 정상, 가드 작동). 체인5(분리 실행): c180 vs o199c, o219 vs o218 lean 검증 + 토마토 버킷 은행(특수검증, 활성화 희귀하므로) → `o_results/chain5.txt`.
- 체인5 결과: **c180 vs o199c** 스위트 +80(7↑/1↓, L→W 1/W→L 0), 풀10 +104, 홀드아웃 ±0(미발화), 토마토 버킷 +563 [+479,+648] SIG+ 승 246→258. **o219(o218+c177/c179/c180) vs o218** 스위트 +76(7↑/1↓, L→W 1/W→L 0), 풀10 +116(WORSE 0), 홀드아웃 ±0, 토마토 버킷 +466 [+379,+550] SIG+ 승 260→272, 4상대 전부 +. 발화: 토마토 버킷 146/288. → 32시드 풀(최종 게이트) 실행 중 `o_results/pool32_o219.txt`.
- 1위 격차 분석(리더보드 2758 #206 vs Artem 3151/Majkel 3146): Majkel 289경기 vs 우리 라이브 420경기 프로필(버킷별, 비paired) — 최종 현금 격차 YARN −12.8k, 거위 −8.7k, 우유1 −4.1k, 우유2/3 +2k. 시간대별 격차는 d9–15(+5k)와 d24–30(+6k), d0–9는 동일. 구조 차이: Majkel 일손 d9 10명/d12 11명(우리 8.2/9.2), 유휴 worker-step 0%(우리 d0–6 23%, d6–12 7%), 딸기 d0–6 12칸 파종(우리 4), 밀 age-2 시비 55/경기(우리 18; 시비 시 수확 3→6단위), 비료 판매가 68 vs 47, d21+ 가축 자연 이탈(18→11.6). Majkel 개막은 테이프가 아님(첫 72스텝 113가지) → 복사 불가, 상태기반 개막 재설계 필요. 동결 Majkel 재생(o218, 289경기): 216W 73L이나 동결 상대 현금이 70–90k로 붕괴해 증거력 낮음; 패배 73 중 YARN 26(−30k 꼬리) → YARN 세계가 1순위 표적.
- **o219 32시드 풀: 1332W 12L (o218 1328/16), paired 평균 +59, L→W 4(시드 7014 양좌석, dmitriigluzdov·lucifer19), W→L 0, 최악 경기값 5상대 개선·악화 0. 모든 게이트 W→L 0 → 오늘 마지막 슬롯에 o219 제출** (사용자 지시 "검증 후 마지막 하나 제출"). 결과: ref 56258013 (00:38, 오늘 슬롯 소진). 파일 sha 3bb47319…. 다음: 개막 재설계 계획 `docs/o-opening-redesign-plan.ko.md`(일손 램프 → 밀 시비 슬롯 → 조기 딸기, o218 기준 paired).
- 라이브 점검(09-16 새벽): **o218 2201은 성능 하락이 아니라 매치메이킹 경로** — 78경기 전부 2400 미만 상대(평균 1809), 74W 4L, 초반 8·14번째 경기에서 신규 제출(잠정 1477/1615)에 패해 레이팅 경로가 710→2174로 느림. 오류/타임아웃 0. o219는 67경기 58W 9L, 2400–2749 28/35, **2750+ 8/10**(o182 6/18, o199c 0/2). 패배 13건 리플레이 분석: o219 9패 = 미러 노이즈 7(−109~−1488, 모두 d21–29에 결정) + YARN 2(sdy623 −4.5k: V233 d16 땅+양6 확장이 미확장 미러에 못 미침). 미러 패배에서 사료/케어 강도(0.7–1.0/가축일), 일손, 땅 모두 동일; 후반 이탈 17마리는 전부 WOOL $1·MILK <$50 상황의 의도적 사료 스킵(unfed=1→2). 시스템적 누수 없음 → 승부는 동일 턴 매도 경주.
- 새 공개 노트북: **V44 "same-turn sale race"(2803)** = 클론 감지 시 R36 예약 지평 8, 경주 패배(우리 창고 입고 턴에 상대가 같은 품목 매도) 감지 시 24로 확대. 우리 스택엔 r37/c115의 8/12가 이미 있어 신규분은 확대 arm. **o220 = o219 + `overlays/o220_v44_race.py`** 빌드(스모크: 클론 감지 345–373턴, 확대 0, 마진 o219와 동일, 오류 0). 체인6: validate(base o219) + 32시드 → `o_results/chain6.txt`. Pipe-5 Terminal Boost(2670)·Turn-One(2703)는 후순위(Pipe-5는 `_shadow_terminal/_parent_liquidate`, 우리 r127 보유).
- 체인6 lean: **o220 vs o219** 스위트 +71(10↑/6↓, L→W 3, W→L 1), 홀드아웃 +28(2↑/6↓, flip 0), 풀10 n.s. → 32시드로 판정. 오프라인 검사: V44 lost-race 조건이 o219 미러 패배 8건 전부에서 발생(d12~25) → o220 확대 arm은 실제 패배 상황과 관련 있음.
- **가격 분석(머니 증가분 귀속, Majkel 289 vs 라이브 420)**: 거위 세계에서 Majkel은 우유 72u@$143·양털 55u@$157·딸기 104u@$131·비료 45u@$82, 우리는 우유 ~171u@$32·양털 119u@$29·딸기 131u@$64·비료 181u@$40(우리 단위수는 sell-all 주문 탓에 과대, $/u는 과소 가능). Majkel 창고 평균 재고 우유 5.5·딸기 12.9·양털 6.0 vs 우리 1.5. 시장 가격은 재고/목표(T) 함수라 T(우유 122·양털 105·딸기 100) 초과 공급의 한계수입 ≈ 0 → 상위권은 과잉공급을 안 하고, 미러 계보는 상호 덤핑 균형(일방 자제는 o179처럼 상대에게 이득). 시사점: 1등 격차의 본질은 "덤핑 계보의 포트폴리오 크기"이며, 개막/노동 재설계와 함께 생산 포트폴리오 재조정이 필요(단, 미러 상대 paired 마진이 아니라 절대 현금도 지표로 봐야 함 — 대칭 개선은 미러 마진에 안 보임).
- 밀 시비 대체안 검토: 물주기 워커가 비료를 들고 있는 경우 age1 ~10회/경기뿐 → +$550/경기 수준, 보류. 유휴 worker-step ~400/경기는 대부분 제자리 작업 불가 → 이동 스케줄 재설계 필요.
- **o220 탈락**: 32시드 풀 1326W 18L(o219 1332/12), W→L 6·L→W 0, 평균 −24 — 동결 스위트 +71은 비반응 상대 착시. 확대 발화 26/128. **핵심 발견: 공개 V44(=V43+race arm)를 상대로 o219는 46W 18L(+1,709, 최악 −2,970)** — V43은 64/64였으므로 race arm 하나가 우리 상대 18패를 만들어냄. V44 포크가 상위권에 퍼지면 위협 → o222(2회 패배 후 확대)·o223(확대 지평 16) 변형을 V44 상대로 비교 중.
- 시장 구조 확인: 자제형 프록시(미러+배치 매도 상한) 상대로 o219 64/64·우리 현금 102k(미러 상대 96.6k) → 상대가 덤핑 안 하면 우리 수입 +6~17k. 테이프 자체 유휴는 6–10%(대부분 1~2스텝 런), 테이프 고용은 d10에 11명(Majkel d12 11명) → 노동 램프 격차는 작음; 격차의 본질은 시장 흡수량(T) 대비 과잉공급과 실현가격.
- V44 race arm 이식 진단: o220의 32시드 W→L 6건은 전부 시드 7005(PIZZA,YARN,BRUNCH) × 비미러 3종(aurax7-v5/MSF/dmitrii, 같은 공개 테이프라 클론 게이트 통과) — 1회 오탐 lost-race 후 지평 24가 영구 고정되어 step 299 우유 6개를 즉시 매도(+523→−2,365). **o224 = 창 기반 확대(72스텝, lost-race마다 재장전)**: 7005 회귀 해소(+523), V44 상대 128경기 합산 o219 96W/32L → o224 102W/26L(L→W 8, W→L 0). o222(2회 트리거) 48/16, o223(지평 16) 46/18은 효과 없음. 체인7: o224 lean(full, base o219) + 32시드 → `o_results/chain7.txt`.
- r36/r37 메커니즘 정리: 예약 지평 N = 테이프가 N스텝 내에 팔 예정인 재고를 지금 앞당겨 매도(부채 기록). 미러 경주는 "누가 먼저 파나"라 지평이 긴 쪽이 이김(2→3→4→8→c115 12→V44 24). 비미러 상대에겐 앞당김이 테이프의 의도된 매도 시점을 깨서 손해 가능(7005 사례). 대칭 상황(둘 다 24)은 주문 슬롯 lockstep 동전던지기 → 미러 메타에서 압도적 우위는 생산 타이밍 차별화(테이프 이탈) 없이는 불가.
- 시드 7032(FM,BAKERY,ICE,ICE,BRUNCH,ICE,PIZZA,SMOOTHIE) o219 vs V43 −5,767 진단: 거위 베팅 역전(우리 거위7/소4 vs V43 거위4/소7, 늦게 우유 상점 5개) + d25–26 양 이탈(WOOL $1) — o182/o199c/o217 전부 동일 −5,767(c171·o206·당근 무관). d12 이후 소 추가 매수는 회수 불가(첫 우유 d20, 사료 17일) → 헤지 불가한 세계 복권. **o225(우유 상점≥2면 소 사료 스킵 금지, 달걀 상점≥2면 거위)**: 7032 −5,767→−5,612(무의미) → 아래 c150 16시드 비교 후 판단.
- o225 결과: c150 16시드×2 paired +72, flip 2/2, 절대 현금 −624 → 효과 없음, 폐기(라이브에서도 소 이탈은 d24+ 88건/420경기, 우유상점≥2 세계 23경기 중 21승이라 손실 원인 아님).
- **o224 판정: 스위트 +17(6↑/10↓, flip 0), 홀드아웃 +27(flip 0), 풀10 ±0, 32시드 1332W 12L = o219 동일(paired +2, flip 0), V44 상대 128경기 96W→102W(W→L 0), 오류 0·최대 스텝 0.41s.** 은행(거위/우유1/우유2/YARN) 진행 중 `o_results/bank_o224.txt`. 통과 시 09:45 슬롯 후보(승인 필요).
- o226(상대 적응형 매도 조절: 상대 매도량<우리 40%면 T 여유분까지만 매도): c150·자제 프록시·V44 8시드×2 모두 o224와 동일(발동 9~24턴, 캡이 재고보다 커서 무효) → 폐기. r36/r37이 드롭 턴에 재고를 즉시 앞당겨 팔기 때문에 후처리 캡으로는 공급 조절이 안 됨 — 공급 조절은 생산(가축·타일) 단계에서만 가능.
- **o224 은행 vs o219: 거위 +14 [+3,+27] SIG+(승 268=268), 우유1 0, 우유2 −1 n.s.(승 274=274), YARN 0 — 모든 버킷 승수 동일.** 최종: o224는 o219 대비 모든 게이트에서 회귀 0, V44 상대 +5pp(96→102/128), 거위 세계 소폭 +. **09:45 슬롯 후보 = o224**(`agent/o224_v44_race_window.py`, sha 8a561fb7…). 제출은 사용자 승인 후.
- 오늘(09-16 새벽) 결론: o219 라이브 84경기 2750+ 17/25(68%). "압도적" 후보는 만들지 못함 — 로컬 풀은 포화(1332/1344), 남은 패배는 미러 경주 노이즈·세계 복권·V44 포크. 근본 격차(실현 가격/포트폴리오·상대 스타일)는 `docs/o-opening-redesign-plan.ko.md`(06:00 갱신) 로드맵 B(T 인지 포트폴리오, 절대 현금 지표)로 이월.
- **o227 = o224 + 스텔스 앞당김**(`overlays/o227_stealth_drop.py`): 우리 액션이 경주 품목을 창고에 PLACE하는 "드롭 턴"(미러와 동일 턴)에는 네이티브 R36을 지평 8로 실행(공개 계보와 같은 양만 매도), 9~12스텝 앞당김은 다음 턴으로 미룸 → V44가 "패배한 경주"를 관측하지 못해 24로 확대하지 않음. 스모크: **V44 상대 32시드 50W14L → 58W6L(L→W 8, W→L 0, +585 = V44 클론감지 무력화 상한과 동일)**, c150 +252(flip 0), V43 −16(flip 0), 스텔스 턴 36/경기. 체인8: lean(full, base o219) + 32시드 + 은행 4버킷 + V44 확장 시드 → `o_results/chain8.txt`.
- **체인8 o227 판정 (vs o219): 32시드 풀 1342W 2L (o219 1332/12; L→W 10 = 시드 7012 own-c1xx 전부 회복, W→L 0, paired +61) · 은행 YARN +206 [+149,+264] SIG+ 승 267→276, 거위 +9 n.s.(flip 2건 ±100), 우유1/우유2 승수 동일 · 스위트 +16(flip W→L 1건: +92→−60), 홀드아웃 +30(flip 0), 풀10 +30 · V44 상대 128경기 114W 14L(89%; o219 75%, o224 80%) · 오류 0, 최대 스텝 0.20s.** 큰 회귀 없음(모든 게이트 최악 delta −463). → **09:45 슬롯 후보 = o227** (`agent/o227_stealth_drop.py`, sha 0f3f649d…). 제출은 승인 후.
- o228(딥 매도: 시장이 T 초과일 때 꼬리 보류, 재고가 0.5T 이하로 내려오면 방출, 24스텝 기한): c150/V44/자제 프록시 16시드×2 모두 **딥 방출 0**(재고가 절대 0.5T 아래로 안 내려옴), 70단위/경기 보류 후 전부 기한 방출, paired −67~−277, flip 없음 → 폐기. Majkel의 고가 매도는 상대 공급이 적어 시장이 목표 아래인 환경의 산물(Artem #1도 창고 ~1의 덤핑형이며 Majkel에 3/13 패). 우리 미러/V44 환경에선 총공급이 커서 딥이 생기지 않음 → 매도 타이밍 단독으론 불가, 생산 총량과 결합 필요(로드맵 B).
- 1위 Artem 프로필(보관 13경기, 전부 vs Majkel, 3승): 소 7.5·양 5.8·거위 0, 창고 평균 ~1(덤핑형), 수입 딸기 13.2k·밀 8.2k·멜론 8.1k·우유 7.2k. Majkel(자제형, 14마리)이 Artem(덤핑형)을 10/13 이김 → "정교한 자제(딥 매도)"는 덤핑형에게 이기지만 그 조건은 상대 공급이 버스트형일 때. 후속: 버스트 덤퍼 프록시(8스텝마다 일괄 매도) 상대로 o228 재검증.
- 버스트 덤퍼 프록시(8스텝마다 창고 전량 매도) 상대 o227→o228: 딥 방출 0, paired −54, flip 0. 프록시 자체는 창고 과적으로 붕괴(현금 50k)했고 우리 현금은 135k까지 상승 — 상대 공급이 우리 수입을 ~38k 억누른다는 외부효과 크기 확인. 딥 매도 계열(o226/o228) 종결: 우리 생산량 수준에서는 어떤 상대 유형에서도 시장이 0.5T 아래로 내려오지 않음. 매도 정책 개선은 생산 총량 설계(로드맵 B)와 함께만 의미 있음.
- o229(스텔스 유지 + 비드롭 턴 클론 지평 16/24): c150 +191/+145(flip 0)이나 **V44 W→L 4/6, aurax7 W→L 2/6** → 폐기. 비드롭 턴에 더 앞당겨 팔면 테이프가 의도한 소비 회복 후 매도 시점을 깨 손해. o227의 균형(드롭 8 / 평시 c115 12 / lost-race 후 24 창)이 국소 최적.
- **상위권 계보 판별(테이프 매칭, 오프셋 +1로 우리 라이브는 100% 일치 확인)**: Majkel·ymg_aq·SpaTaro·Unknown Mother-Goose·feel the agi·Artem·M&M&P&Q 전부 yhay 테이프와 1% 일치 → 상위 클러스터는 모두 비테이프 독자 플래너. 우리 로컬 풀(테이프 파생 + FSV/MSF)은 상위 클러스터를 대표하지 못함 → "1위 추격" 판정은 오프라인 불가가 구조적 이유. Artem 개막: d1에 일손 4명·목장 건설·비료 수집(우리와 다른 개막).
- **상위 클러스터 절대 현금 벤치마크(같은 세계 버킷, 상대 Majkel) vs o227(상대 V44/미러/FSV4/MSF), 단위 k**: 거위 — Artem n/a·ymg 84.8·SpaTaro 84.8·Majkel 96.0 | o227 90–92. 우유1 — Artem 91.2·ymg 95.8·Spa 91.2·Majkel 102.2 | o227 83–86. 우유2 — Artem 99.2·ymg 110.6·Spa 115.9·Majkel 117.9 | o227 101–110. 우유3 — Artem 122.7·ymg 119.4·Spa 127.5·Majkel 134.9 | o227 124–136. YARN — Artem 104.0·ymg 102.2·Spa 104.8·Majkel 115.0 | o227 95–102. M&M&P&Q(16경기, Majkel에 62% 승) 106/118/144/169/117로 최상위. 해석: o227의 절대 산출은 Artem/ymg_aq/SpaTaro 급(우유1·YARN은 다소 아래, 우유2/3은 위), Majkel(거위·YARN +5~15k)과 M&M&P&Q에는 못 미침. 1위 추격은 "가능성 있음, 미증명"이 정확한 표현.
- V233(YARN d16 땅+양6) 상대 조건부 가설 점검: 동결 스위트에서 V233 제거(o193) 시 YARN 세계 우리 현금 +1,321이지만 상대 +2,465(외부효과) → 마진 −1.1k, 승 −1. o227 32시드 풀에서 발화는 YARN 242경기 중 32(부자 세계 선택 효과). 비미러 상대에서도 상대의 양털 가격 이득이 남아 순효과 불명확·발화 희귀 → 오늘은 보류(로드맵 B에서 생산 총량과 함께 재검토).
- **V233 외부효과 정량(은행 YARN 288경기, o230=o227−V233 vs o227)**: 우리 현금 +3.6~4.3k / 상대 현금 +5.8~6.2k / 마진 −2.2k [−2,600,−1,685] SIG− / 승 276→212(−64), c150·V43·FSV4·MSF 4상대 모두 동일 방향. → V233(양 6마리 추가)의 가치는 전적으로 상대 양털 가격 억제. 양털을 파는 어떤 상대(Majkel 133단위 포함)에게도 작동하므로 유지. 시사점: 상위 자제형(Majkel YARN 115k)은 비덤핑 상대 기준 수치이며, 우리와 붙으면 양털 수입이 크게 깎임 → o227이 YARN에서 밀린다는 결론은 과장. 로드맵 B의 "생산 총량 축소"는 이 외부효과 때문에 상대가 안 파는 품목으로의 전환만 허용.
- **상위 플래너 vs 테이프 포크(top10 아카이브 09-11/12, 2,106경기)**: Majkel 13/14(+15.5k), ymg_aq 29/30(+13.6k), M&M&P&Q 2/2(+12.8k), THIRD FARM 11/13(+9.3k), Artem 10/13(+5.0k), SpaTaro 19/25(+4.2k), Mother-Goose 20/31(+4.4k); 플래너끼리는 ~50%. 우리(o227)의 테이프 포크 상대 마진은 +4k대 → Artem/SpaTaro 급, Majkel/ymg_aq 급(+13~15k)에는 못 미침. Majkel·ymg_aq vs 테이프 44경기 수입 분해: 최종 108.0k vs 93.8k. **비료 수입 17.7k vs 7.8k(+9.9k, 최대 단일 격차)**, 멜론은 총액 비슷하나 플래너는 d12–24에 분산 매도, 테이프는 d0–12 전량. 비료는 상점·타운센터 소비가 없어(TOWN_CENTER_PRODUCTS 제외) 재고가 줄지 않는 순수 선착순 시장 → 플래너는 d12–24에 소량(2.2단위)씩 선매도, 테이프는 후반 대량(10단위) 덤핑.
- **비료 경제 정량(라이브 150경기)**: 수집 383+구매 74−시비 91 → 매도 ~365단위/9.4k($26/u). 매도 호가 d0–9 $80–99, d12–18 $47–61, **d24–27 $7–15(40회 덤핑)**. ymg_aq(vs 테이프)는 276단위를 $84/u에 팔고 205회 시비. 비료는 소비가 없는 순수 선착순 시장이라 후반 단위의 매도 가치는 ~$10. **후반 비료를 밀 age1–2 시비(+2~3단위×$37–47)에 쓰면 단위당 +$65~130 → 100회 추가 시비 시 +6.5~13k/경기 가능성(최대 단일 지렛대).** 기존 R51 비료 투어 플래너가 정확히 이 용도인데 128경기 발화 0 → 게이트 계측 중.
- R51 계측: 시도 156회 중 경로 4~7타일·표적 12+ 확보되나 경제 게이트에서 74회 중 9회만 통과(비용 $250–415 = 비료 q×(호가+2) + 고용 fib, 가치 $320–470). **o231(창고 비료를 후반 덤핑가 $12로 평가, 부족분만 구매, 비율 1.2)**: c150 −654(W→L 2), V44 −193(W→L 4), FSV4 −184(W→L 2), 상대 현금 +400 → 폐기. 비료를 팔지 않고 쓰면 상대 비료 가격이 올라(외부효과) 마진이 깎이고, 투어 고용비가 가치를 잠식. 결론: 비료 지렛대도 미러 외부효과에 막힘 — 상위 플래너의 +13~15k(vs 테이프)는 오버레이가 아니라 생산·판매 아키텍처 차이.
- o232(당근 스위치 비율 2.0→1.4/1.6): c150 −1,648/−565, V44 −1,852/−480, FSV4 −1,482/−483, W→L 2~8, 우리 현금 −500~−900·상대 +40~+900 → 폐기(당근 추가 공급은 밀 사료 가치 상실 + 당근가 하락). 참고: o227 32시드 풀에서 기존 2.0 스위치 발화 0/1,344(현재 사실상 비활성 레이어).
- **정정**: "Majkel/ymg_aq가 테이프 포크를 +13~15k로 이긴다"는 09-11/12 표본은 대부분 2200~2800 포크(Gleb 2679, carlos 2628, Terry Luo 2203, chocolat 2585…) 상대였음. 최강 테이프 포크(Catalyst 2932·kyy666 2906·Zhongyi Dai 2804·Le Viet 2789·Himanshu 2786) 상대로는 상위 플래너 성적이 혼조: Majkel +32k(1경기), SpaTaro +15.3k/+3.8k/−1.8k, Artem +13.8k/−0.4k, feel the agi +0.4k, Otter Vibe +1.1k(1/2), binghua −5.0k(1/3). 즉 최강 포크는 상위 10위권과 대등하게 싸우며, o227은 공개 최강 포크 V44에 89%·+1.8~2.4k → o227의 위치는 "상위 10위권과 같은 경쟁 대역"으로 상향 정정. 표본이 1~3경기라 09-08~10 샤드 추가 후 재산출 예정.
- **강도 일치 벤치마크(top10 아카이브 09-08~12, 2750+ 테이프 포크 23종 상대 — Catalyst 2932·kyy666 2906·THIRD FARM 등)**: Majkel 10경기 90% +18.9k, M&M&P&Q 12경기 83% +5.0k, ymg_aq 29경기 76% +5.3k, Mengfei Li 72% +4.0k, SpaTaro 76경기 68% +3.2k, feel the agi 62% +3.7k, Artem 7경기 57% +3.1k, Otter Vibe 54% +2.6k, Mother-Goose 54% +2.3k, binghua 53% +3.8k. **o227 vs 공개 최강 포크 V44(2803): 89% +1.8~2.4k, V43 100%** → 같은 상대 클래스 기준 승률은 상위 10위권 상단(ymg_aq/M&M&P&Q/Majkel 대역), 마진은 SpaTaro/Otter/Mother-Goose 대역. 앞선 "Artem/SpaTaro 급, Majkel 급 아님" 결론을 이 표본 기준으로 상향 정정(단 Majkel 마진 +18.9k는 여전히 별격).
- 스무스 매도 프록시(버퍼 6·배치 4, 플래너식): o227 64/64 +11.6k(프록시 현금 89k), 미러 c150도 64/64 +6.4k → 매도 스무딩 자체는 우리 환경에서 손해. 플래너의 우위는 매도 방식이 아니라 생산·노동 구조.
- **플래너 프록시 프로젝트 착수**(사용자 지시): 계획 `docs/o-planner-proxy-plan.ko.md` — A안(규칙 추출형 독립 컨트롤러) 채택, D1 정책 통계 → D2–3 구현 → D4 충실도(프록시 vs c150/V44가 아카이브의 Majkel 90%/+18.9k 방향, 세계별 현금 ±10%) → D5 후보 평가 도입. 사전 실험: replay_lab에 잡초 동기화 동결 모드(`fixed_shops_frozen_opponent_weeds`) 추가했으나 Majkel 동결 현금 112.8k→95.1k(14경기)로 여전히 붕괴 → 동결 방식 폐기, 반응형 필수 확인.
- **플래너 프록시 D2 진행(`agent/opp_planner_proxy.py` v0.5)**: 테이프 없는 독립 컨트롤러 — 세계 인식 → 현금흐름 기반 JIT 구매(개막 소2양3·멜론8·밀10, d2–8 딸기, d6~ 땅 재시도, d6–14 세계별 목표 가축까지 부족분 구매) → 구역/스트립 배정 디스패처(가축 담당자 = 1+가축/4, 아침 밀 수령 후 급식·케어·수집·수확, 서 있는 타일 작업 우선) → 버퍼 매도(우유/양털 4, 배치 2–4, 현금 3k 미만이면 버퍼 0, d28~ 청산). 진단 도구 `o_tools/proxy_daily.py`(일별 급수/급식 커버리지·잡초·이동/작업), `proxy_trace_feeders.py`. 현재 vs c150: 최종 45–60k(c150 107–150k), 가축 15–16(목표 17), 급식 65–75%, 급수 75–85%, 이동이 스텝의 58%. 목표(세계별 96–135k)까지 남은 과제: 행 단위 급수 순회로 이동 감소, 급식 100%(케어 보너스), 시비(비료 수령) 도입, 멜론/딸기 조기 현금화. D2 계속.
- 프록시 v0.6: 급식 100%(d12~), 가축 13–14, 급수 90%+; 초기 경제 수정(멜론 12칸 d0–3 누적 구매, 멜론 age10·4단위 즉시 수확·전량 매도, 비료 연속 매도, d≤5 밀 예비 최소화) → **vs c150 73.1k**(c150 172k; 이전 45k). 같은 경기 수입 분해로 확인된 남은 격차: 멜론 초기 현금(c150 12개 11.7k), 비료 매도(c150 14k/경기, 수집 400 vs 우리 160), 딸기 후반. 액션 믹스는 Majkel 대비 WATER 80%·HARVEST 77%·CARE 70%·FEED 71%·PLANT 72%·COLLECT 40%·FERTILIZE 0%.
- 프록시 v0.7 체크포인트: 6시드×2 vs c150 현금 평균 64k(25k~89k) — 우유 상점 세계 78–89k, 달걀/당근 세계(7003 BRUNCH·PET·PIZZA) 25k로 붕괴, 좌석 무관(결정적). 급식 100%·급수 90%·가축 14–17은 안정. 남은 과제: 세계별 가축·작물 계획(비우유 세계에서 소 대신 거위/딸기/당근), 초기 현금 시퀀스, 수확·수집 처리량, 시비 도입. 측정 도구: `o_tools/proxy_daily.py`(PSEED 환경변수로 시드 지정).
- 프록시 v0.8: 급식 담당이 비료를 창고에 내려놓아 초기 현금원 확보(비료 $80–100/u), 딸기 d2–5 누적 8칸·d6 11칸, 딸기 생산일 시비 우선순위 2, 당근(PET/FM 세계) 도입, 소형 축사 군집. 7003(달걀/당근 세계) 24k→53k, d18 현금 18–25k(Majkel ~27k). 8시드×2 vs c150 결과는 아래 줄.
  → v0.8 8시드×2 vs c150: 프록시 현금 평균 59k(중앙 59k, 38–90k), c150 126k, 승 0/16. 세계별: ICE+SMOOTHIE 90k, ICE+BRUNCH 72k, SMOOTHIE+YARN 65–68k, BAKERY+SMOOTHIE 65k, BRUNCH+ICE 53k, BAKERY+PIZZA 45k, PET+YARN 44k, PET+ICE 38k. 목표(96–135k) 대비 55–70%. 다음(D3): 후반 수입(+5~7k/일 → Majkel +7~9k/일), 시비 실행률, 밀 사재기(20단위 유휴), 3번째 땅 시점, 비우유 세계 가축 구성.
- 프록시 v0.9(비료 창고 예비 8·d10 이후 밀 예비 축소): 8시드×2 vs c150 평균 68.9k(중앙 72k, 50–86k), c150 150k.
- 프록시 A/B(고정 세계 하네스 `o_tools/proxy_eval.py`, 상점 순서 시드별 캐시 `o_results/proxy/shop_seq.json`): base 59.3k / nostock 59.9k / nofeedskip 59.2k / straw_less 62.7k → straw_less 기본값. 버킷별 우유2 79–81k·우유3 71–75k·거위 55–59k·YARN 46–54k·우유1 41–48k(Majkel 118/135/96/115/102k). 컨트롤러 프록시는 아직 Majkel의 45–70%.
- **중간 프록시로 "잡초 동기화 동결 Majkel" 채택**: 동결 Majkel은 원본 대비 −15%(112.8k→95.1k)지만 행동 양식은 정확히 Majkel(자제 매도·17마리·시비)이라, 후보 간 *상대* 비교(paired)에는 유효. o227·c150·o219 vs 동결 Majkel 289경기 실행 중 → `o_results/majkel_frozenw/`. 컨트롤러 프록시(D3)는 병행.
- **o227 제출됨(사용자 직접) → ref 56264950** (09-16 오전). 라이브 추적 등록: `o_tools/live_episodes.py 56264950`. 150경기 전까지 레이팅 비교 무의미; 2750+ 구간 승률과 패배 유형만 추적.
- **o233(플래너 인계: d15/12/18부터 필드·구매를 플래너가, 매도는 테이프 유지) vs c150 고정 세계 8시드×2**: o227 103.0k(16/16승) → o233 d15 76.6k(0/16), d12 72.9k, d18 83.9k. 인계가 늦을수록 손실이 줄어드는 단조 관계 = **테이프의 d12–30 생산 루프가 현재 플래너보다 ~25k 강함**. 결론: "생산 아키텍처 재설계(플래너 인계)"는 플래너가 단독으로 테이프(103k)를 넘기 전엔 불가. Majkel의 우위는 매크로 통계가 아니라 실행 정밀도에 있음(우리 플래너는 Majkel 통계를 따르고도 60k). 인계 라인 중단; 플래너는 프록시(평가용)로만 계속.
- **동결 Majkel(잡초 동기화) 289경기 3자 비교**: c150 189W/100L(65%, +19.5k) · o227 201W/88L(70%, +21.0k; 세계별 거위 65%·우유1 77%·우유2 78%·우유3 57%·YARN 57%) · o219 128/163(79%, 유효 163). paired: o219−c150 +1,577(L→W 7/W→L 2), o227−o219 ±0(동결 상대는 경주하지 않으므로 o227의 개선은 무효과). 해석: Majkel의 기록된 정책을 상대로 o227은 ~70% 우세(상한 추정; 반응형 Majkel은 더 강함), 취약 세계는 YARN·우유3·거위. 이 비교를 검증 게이트의 "프록시 항목"으로 채택(`o_results/majkel_frozenw/`).
- 동결 Majkel 패배 프로필(o227): 최악 세계 = PET_CAFE 2~3개(−13.6k~−21.7k)와 YARN+PIZZA×2(−30k대). o199c 당근 스위치는 가격 규칙만 남아 풀에서 0/1,344 발화 → **o234 = o227 + `_O199_DEMAND=2`(PET/FM ≥2개면 밀→당근 전환)**. 체인9: o227/o234 vs 동결 Majkel PET 세계 76경기(paired), 은행 당근 버킷 288경기, lean 게이트(base o227) → `o_results/chain9.txt`, `o_results/majkel_pet/`.
- o234 폐기: `_O199_DEMAND=2`가 의도와 달리 거의 모든 세계에서 발화(123회/경기; `demand` 변수 의미가 PET/FM 개수가 아님) → 스위트 −14.5k(W→L 61), PET 동결 Majkel paired −14.9k. 게이트를 오버레이에서 직접(PET/FM ≥2) 계산하는 o235로 재시도.
- o235(PET≥2 당근 전환) 폐기: PET 동결 Majkel 76경기 paired −6.4k(W→L 13, 발화 60경기 평균 −8.1k), 고정 세계 미러 12/16(o227 16/16). "PET 세계 = 당근 부족" 가설 기각. 다음: 해당 세계 단일 경기 수입 분해(우리 vs Majkel)로 진짜 원인 탐색.
- o236(d16+ PET≥2 세계 밀 파종의 절반만 당근) 폐기: PET 동결 Majkel paired −3.6k(W→L 6), 고정 세계 미러 12/16. o199c 스위치 계열(o234/o235/o236) 종결 — 우리 테이프에서 밀은 사료·현금 양쪽이라 당근 대체는 어떤 강도로도 손해. 동결 Majkel 최악 6경기는 전부 YARN 우선 + 후속 우유 상점(PIZZA×2/ICE) 세계: Majkel은 소 7마리로 d24–30 우유 13.3k, 우리는 소 4마리 5.8k.
- 동결 Majkel YARN 세부(우유 상점 수별): yarn+milk0 10/18(+13.1k), +milk1 16/27(+12.3k), +milk2 10/19(+15.6k), +milk3 3/4 — 하위 클래스 무관하게 ~57%·평균 +12~16k(분산 큼). 단일 경기 진단(YARN,PET,PIZZA,PIZZA): Majkel은 d16~ 토마토 10~11칸·당근 23칸으로 d24–30 36.5k(토마토 6.9k·당근 7.4k·우유 13.3k), 우리는 19.7k. 당근 대체는 실패했으므로 **o237 = d16–22 PIZZA/FM ≥2 세계에서 밀 파종 8칸을 토마토로**(테이프의 급수·주기적 수확 재사용, 추가 SELL) 시도.
- o237(d16–22 PIZZA/FM≥2 세계 밀 8칸→토마토 레인) 폐기: PIZZA 동결 Majkel 108경기 paired −3.5k(W→L 9), 고정 세계 미러 12/16. 오늘 테이프 위 작물 전환 계열 4종(o234/235/236/237) 전부 손해 — 테이프의 밀 주기는 사료·현금·경로가 묶인 하중 구조라 부분 대체가 안 됨. Majkel식 후반 피벗은 플래너 아키텍처에서만 성립.
- **문서 최신화(사용자 요청)**: `docs/o-handoff-2026-09-16.ko.md` 신설(현재 최선·스택·6개 게이트·확정 사실·폐기 표·프록시 상태·데이터 자산·다음 할 일), `docs/o-validation-process.ko.md` v3 절, `docs/o-planner-proxy-plan.ko.md` 9절(상태), `docs/o-opening-redesign-plan.ko.md`(o232~o237), `HANDOFF.md` 포인터.
- 프록시 충실도 재측정(고정 세계 8시드×2): **프록시 vs 프록시 82.4k**(우유3 104k·우유2 94k·YARN 79k·거위 73k·우유1 64k) = Majkel 분포(135/118/115/96/102k)의 ~75%. vs c150 60k / vs 스무스 미러 65k는 덤핑 외부효과가 겹친 수치라 충실도 지표로 부적합 → 프록시 평가는 프록시-대-프록시 절대 현금으로. 부수 발견: 스무스 미러(테이프 계보)가 자제형 프록시 상대로 135k(미러 상대 97~103k) — 우리 계보는 자제형 상대에게 매우 큰 절대 산출을 냄(동결 Majkel +21k와 일치). 스트립 순회(circuit) 변형은 −2.2k라 opt-in으로만 유지.
- 09-16 13:10 프록시 D3 진단: Majkel 100경기 곡선(`o_results/proxy/majkel_curves.json`) 현금 d12 7~10k → d15 21~27k → d18 36~49k, d12-18 수입 29~44k(우유1: 우유 7k·딸기 10k·멜론 5k / YARN: 양털 20k). 프록시는 d12-18 5~12k. 시드 7001 추적: 양 12마리 양털이 d12-17 미회수(캡 6 도달, 판매 0), 소도 동일 → 급식자가 FEED/CARE만 하도록 제한한 'here' 규칙이 원인. 초반 밀 0타일(d7-9)로 사료 구매, d5 밀 매각 후 재구매도 확인.
- 09-16 13:15 패치: 급식자는 서 있는 타일의 HARVEST/비료 회수도 수행, 급식자 수 n/4.5→n/3.6, d0 밀 씨앗 6→10, d≤9 밀 매각 금지(예비 3×가축+2). '초반 급식자 2명' 시도는 82.4k→76.5k로 기각(되돌림).
- 09-16 14:10 절제 실험(고정 세계 16경기, 프록시-대-프록시): 마무리 회수(A) −2.4k, 급식자 n/3.6(C) −1.1k, d0 밀 10(D) 0, 초반 밀 매각 금지(G) +2.9k. 수확 시점 수정(밀 5·멜론 6·마지막 날 급수 후)+d6 가축 우선(F4b)은 79.8k / vs c150 59.2k로 악화 → F4b 되돌림. Majkel 리플레이로 딸기 시비는 **9일차**(생산일, 3일 유효 → 2회 생산 커버)임을 확인(정책 JSON의 '@6'은 캡 집계 오류).
- 09-16 14:20 판매 수량 비교(d12–18, Majkel 평균 vs 프록시): 우유1 327 vs 128(딸기 53 vs 6, 밀 90 vs 0, 우유 55 vs 23), YARN 349 vs 111(양털 93 vs 16) — 프록시 총생산은 Majkel의 ~55%. 감사 추적: 딸기 시비 하루 1~2회뿐(비료를 매일 매각·밀@1에 소모), d10–14 급식 누락 1~3마리(A 규칙 부작용), d1 양 3마리 미급식(사료 현금 0).
- 09-16 14:30 배치 B 적용: 딸기 시비를 생산일 나이(9/11/13/15)로, 밀 시비 나이 2로, 비료 창고 예비=당일 시비 수요, 마무리 회수는 수확량≥4 또는 급식 마무리 단계에서만, **개막을 Majkel식으로**(d0 소 2·양 3·사료 5·멜론 6·밀씨 11, d1–2 멜론 14), d≤7 급식자는 비료를 즉시 입고(현금화). 측정 중(pvp/vs c150/곡선/감사). o227 라이브 25경기 3패(2400–2749 1/3, <2400 21/22) — 아직 초기.
- 09-16 15:10 배치 B 결과: pvp 83.2k(제자리)·vs c150 61.6k(제자리). **판매 수량 비율(프록시/Majkel, 5세계)**: 전체 0.58 — 우유 0.95·양털 0.91·달걀 0.89·비료 0.86·멜론 0.96은 이미 동급, **딸기 0.54·밀 0.20·당근 0.44·토마토 0** 이 격차의 전부. 원인: d6에 땅 대신 딸기 씨앗 11개(심을 타일 없음) 구매 → 딸기 코호트 d9–10 파종(Majkel d6), 가축도 d7–8에 사서 창고 대기; 밀은 전량 사료로 소비(판매 0)·시비 소량.
- 09-16 15:30 배치 C(q3 전 d≤9 전량 매도, 땅 d6/d9 현금 저축·break, 타일 수 상한 구매): pvp 74.1k(−9k, 미러 동시 덤핑 효과)·vs c150 59.6k(제자리)·수량비 0.60. 배치 D 적용: 멜론 d0–2만 12개, 밀 시비 우선순위 ↑, PIZZA/FM 세계 d15–19 토마토 8칸, d≤9 급식자는 양털/우유 3개 이상이면 즉시 창고 입고. 측정 중.
- 09-16 16:20 배치 D(멜론 d0–2·토마토 레인·밀 시비↑·양털 즉시 입고) vs c150 63.4k, E(3사분면 d7부터 저축, 빈 타일 전부 밀, 밀 잉여 전량 매도) 63.3k·밀 수량비 0.32, F(딸기 26칸을 밀보다 먼저, 거위 우선 구매) **65.2k(최고)**·수량비 0.57(딸기 0.60·달걀 0.79). Majkel 밀 주기 확인(리플레이 3경기): 파종 198회/경기, 시비 56회(나이 2), 수확 (2일차 2개)·(3일차 5개 시비)·(3일차 3개), **1일차 급수 생략**(0일차 201·1일차 63·2일차 188), 밀 매도는 h22/h0. 이동 비율 Majkel 41~46%(하루 274행동 중 ~115 이동), 유휴 ~2.
- 09-16 16:40 배치 G(급수 경제: 파종일·수확창·잡초 직전만 급수; 딸기는 생산일만): pvp 82.1k(중앙값 88.8k 최고)·vs c150 63.5k·수량비 0.55 — d1 급식 1/5 실패로 가축 1마리 탈출→우유 0.60 회귀(원인 조사 중). 프록시 이동 비율 **55~71%**(Majkel 41~46%) → 경로 비효율이 남은 최대 노동 손실.
- 09-16 17:20 배치 H(농부 비료 보관은 d9부터·기회성 비료 픽업은 시비 수요 있을 때만·유휴 창고行 제한): **vs c150 69.0k(최고)**, vs o227 69.1k, pvp 84.7k(중앙값 91.6k). Majkel 리플레이: 우유·양털·비료는 낮에 즉시 입고(PLACE 94/89/57개/경기), 작물은 자정 자동 입고에 맡김; 사료 밀 구매 d6–12 120개.
- 09-16 17:50 배치 I(급식자가 밀 들고 있으면 옛 배정 무시 → d1 가축 탈출 버그 수정, 비료 회수는 d≤8 급식자 전담, d0 사료 10): vs c150 68.5k(제자리), 우유 수량비 0.90 회복, 멜론 0.83→0.48 회귀(NW 타일을 밀 씨앗이 선점). 'anim6'(d6 가축 우선) 64.2k → 기각(플래그로만 유지). 배치 J: d1–5 밀 씨앗은 멜론 12·딸기 8 확보 후에만, d≤8 밀은 사료 부족/씨앗 대기 시 2일차부터 수확(타일 회전). 측정 중(J, J+circuit).
- 09-16 18:30 배치 J vs c150 64.2k(악화)·J+circuit 65.0k(경로 순회 효과 ≈0). 배치 K(비료 픽업을 자기 스트립 수요만큼·잉여는 창고 반납·d0 사료 5): **vs c150 70.3k(최고)**, 수량비 0.61(멜론 0.91·딸기 0.62·비료 0.81), pvp 세계별 91/70/103/107/73k. K에서 조기 밀 수확(J3)만 뺀 K2는 68.5k → J3 유지. K를 `agent/opp_planner_proxy.py`로 승격. 사용자 지적으로 주 측정 상대를 **o227**로 전환(H에서 c150 69.0k ≈ o227 69.1k 확인).
- 09-16 19:20 배치 L(가축 계획 창 d14→d18): 5세계 곡선이 K와 동일(현금 제약으로 구매 시점 불변), **vs o227 70.4k**(vs c150 70.3k와 일치 → 이후 o227만 주 지표). 밀 회계(7002): 파종 129회(Majkel 198)·수확 380개(~600)·시비 83회(56)·비료 회수 260(~390)·밀 구매 96·판매 112(413) — 격차는 밀 타일 수·시작 시점과 종료일 인벤토리 손실(~100개). 딸기 시비 흐름(d15/17)은 정상(당일 due 2~4건 소화). 배치 M(d29 18시 이후 전원 창고 입고, d10–11 딸기 보충 2/일·d12 중단): 수량비 밀 0.35·토마토 0.54(↑)·딸기 0.46(↓), 총 0.61 유지; o227 대전 측정 중.
- 09-16 19:40 배치 M vs o227 70.3k(L 70.4k, 중립) → M1(d29 저녁 입고)만 본체에 병합, M2 기각. **오늘 최종: 프록시 vs o227 70.4k·수량비 0.61**. 계획서 11절·핸드오프 갱신. o227 라이브 36경기 5패(2400–2749 6/10).
- 09-16 20:30 **프록시 스크린(계획서 5.3 첫 사용)**: 고정 세계 8시드×2, 상대 = 프록시(비덤핑·반응형), 우리 현금 paired vs o227 — o231 비료투어 −520(se 273), o228 딥매도 −104, o237 토마토 −2,654, o235 당근 −1,446, o226 적응공급 0(무발동). **미러에서 기각된 자제/전환 오버레이는 비덤핑 상대에서도 전부 손해** → "플래너 상대에서는 방향이 다를 수 있다"는 가설 폐기. 도구: `o_tools/proxy_pair.py`(paired diff), `o_tools/proxy_screen.ps1`.
- 09-16 20:40 o227 라이브 비미러 패배 2건 진단(`loss_diag`): 109490582(−4.9k, Ian lin) = 동일 계보 포크, 9스텝에 양/소 베팅 분기 + 우리 후반 양 5→4 이탈, 3×YARN 세계에서 양털 −2.3k; 판매도 상대는 큰 배치(12단위)를 회복가에, 우리는 3~6단위를 자주(우유 75단위=상대 63단위 수입). 109494304(−1.6k, kwa) = Majkel형 플래너(d6 딸기 8·소2 양3, d24 토마토 12·밀 40): d12–24 +6k, 우리는 d6–12 멜론 +7k로 상쇄 못 함. 우리 계보 라이브 20경기 회계: 밀 파종 163·수확 561단위(Majkel 198/600)·밀 시비 24(56)·딸기 시비 61(60)·이동 42%·PASS 528/경기(Majkel ~60).
- 09-16 21:20 프록시 상대 스크린 2: o230(no V233)·o219는 o227과 **16경기 전부 동일 현금·시드 7005 720스텝 행동 0건 차이**(모듈 분리 로드 확인). 즉 V233 이탈·o224 경주 팔·o227 스텔스는 비덤핑 상대에게는 한 번도 발동하지 않는다 → 플래너형 상대에서 우리 스택의 실체는 o218 테이프 그대로. 플래너 로드맵 문서 신설: `docs/o-planner-candidate-roadmap.ko.md`(정량 목표·작업 순서·게이트).
- 09-16 21:50 배치 N(모든 빈 타일을 PLANT 후보로 + 씨앗 예산, 급식자 저녁까지 비료 회수): vs o227 68.0k, M 대비 paired **−2.3k**(se 1.3k, 10악화/5개선) → 기각(사이드 카피 `state/o_dev/opp_planner_proxy_n.py` 보존). 본체는 M 상태 유지(vs o227 70.4k).
- 09-16 22:20 병렬 측정 2건: (a) M+circuit vs o227 **66.7k**(M 70.4k, −3.7k; 단일 미러 경기에선 밀 +44%·+6k였으나 o227 상대에선 손해) → circuit 재기각(opt-in 유지). (b) 기준선 M 새 시드 7008–7015: **62.9k**(o227 117.4k) — 두 번째 시드셋이 더 어려움. 이후 프록시 A/B는 7000–7015 32경기 기준(기준선 M 합산 66.6k).
- 09-16 23:00 병렬 작업 브리프 `docs/o-planner-parallel-briefs.ko.md` 신설(WP1 밀 공장·WP2 노동 경로·WP3 딸기·WP4 후반 레인, 공통 규칙·합격 기준·기각 목록), `proxy_pair.py --side b` 추가. 스윕 진행: base 66.7k, feed=3.0 61.0k(기각).
- 09-16 23:40 노브 스윕 완료(11변형 × 32경기 vs o227, `o_results/proxy/sweep.txt`): base 66.7k; feed=4.5 67.6k·straw=32 67.1k·buf=2 67.0k(+0.3~0.9k, 노이즈), feed=3.0 61.0k·land3=9 63.5k·straw=20 63.9k·buf=6 64.5k·wheat_units=3 65.7k(악화). 결론: 숫자 노브는 국소 최적, 남은 이득은 구조 변경(브리프 WP1~4)뿐. 본체 변경 없음.
- 09-17 00:40 WP2 1차(route: 플랜터 스트립 순회·동물 구역 출입 금지·씨앗 예산·땅 인식 스트립): 미러 진단 밀 372→629단위·이동 150→125/일이었으나 **vs o227 32경기 −3.6k**(se 0.9k, 23악화) → 기각. o227 상대 감사(7002)로 원인 확인: o227이 d18 이후 딸기($7~11/단위)·우유($40~70) 시장을 홍수시켜 프록시의 딸기 148단위가 2.9k밖에 안 됨; 밀만 $39~47 유지(라우트의 밀 195단위=7.5k가 최대 수입원). 배치 P(상대 딸기≥10이면 딸기 중단, 상대 소≥6이면 소→양, 딸기 $25 바닥): **−20.2k**(30악화) → 양 10마리 양털 109단위 $17(양털 T=105 자체 포화). 교훈: 우유(122)·양털(105)·딸기(100)는 우리 물량만으로도 포화하는 소형 시장 — 상대 인식 배분은 '시장 잔여 용량(T−재고)' 모델 없이는 역효과. 사이드 카피 `state/o_dev/opp_planner_proxy_{route,p}.py` 보존, 본체 변경 없음.
- 09-17 01:30 배치 Q(상대 딸기≥10이면 딸기 중단, 상대 소≥6이면 소 부족분→거위, 딸기/우유/양털/멜론 가격<35%면 보류): 7002 감사에서 달걀 320단위 $35~47 판매(달걀은 log 하락이라 물량 시장 ✓)였으나 밀 424→284로 감소, **32경기 −21.2k**(최소 3.9k 붕괴 경기 포함) → 기각. 엔진 소비 규칙 확인: 상점 인스턴스당 품목 6개/일(단일품목 상점은 12), 타운센터 1개/일(비료 0) → 딸기 흡수 1~7/일, 멜론 1/일, 비료 0 — 소형 시장은 첫 판매자가 가치를 다 가져가고 나머지는 바닥. 오늘 구조 시도 4건(route/P/Q/N) 전부 o227 상대 기각; 공통 원인은 시장 용량 모델 부재. 본체 M 유지(66.7k/32경기).
- 09-17 09:30 o227 라이브(사용자 수집, 83경기): 19패, **2400–2749 39/57(68%)**, <2400 25/26, 2750+ 경기 아직 0. 패배 유형 미러 노이즈 14(대부분 −1k 이내, 동일 계보 포크와의 동전던지기), 세계/가축 베팅 5(양/소·거위/소 첫 구매 분기). o219 복귀 근거 없음 → o227 유지, 2750+ 표본 대기.
- 09-17 09:35 Codex c200~c208 = 프록시(`opp_planner_proxy.py`) 포크 9종(밀 재보충 c200/c201/c205, 창고 왕복 제거 c202, 전역 스트립 c203, 급식자 1/5 c204·세계별 c206, 딸기 시비 우선 c207/c208). c206 주석대로 7000–7015에서 선택됐으므로 **홀드아웃 7016–7031**(새 세계, 상점 시퀀스 자동 기록)과 선택셋 둘 다 vs o227 32경기로 측정 시작(백그라운드 2작업, ~80분). 판정: 홀드아웃 paired(`proxy_pair.py --side b hold_opp_planner_proxy hold_<c>`) ≥ +1.5k·악화 ≤10/32.
- 09-17 11:10 **c200~c208 검증 결과**(vs o227 32경기, paired 프록시 현금; 선택셋 7000–7015 / 홀드아웃 7016–7031): c200 −3.2k/−6.8k, c201 −3.4k/−5.5k, c203 −4.4k/−5.5k → 기각; c202 −0.1k/+0.0k 중립; c204 +1.7k/+0.0k, c205 +0.8k/−0.1k → 홀드아웃에서 소멸(선택 편향); **c206 +4.1k/+2.4k(8악화)**, **c207 +2.6k/+2.7k(se 0.7, 5악화, 22개선)**, c208 +2.7k/+1.4k(12악화). 합격: c207(= c206 세계별 급식자 비율 + 딸기 시비 우선). 버킷(홀드아웃): c207 우유1 +8.1k·우유0 +1.3k·우유2 +1.9k·YARN +1.0k·우유3 −4.9k(n2). 본체 병합 검토.
- 09-17 11:50 배치 R(c207 병합) 확인: 본체 vs o227 **홀드아웃 70.1k(+2.7k, se 0.7, 5악화/22개선)·선택셋 69.3k(+2.6k)** — c207 파일과 동일 결과(변경 2줄 그대로 이식됨). 새 기준선 라벨 `base2_hold`/`base2_sel`. 누적: 09-16 아침 60.5k → 69.3k(선택셋).
- WP4(c2) 시장 잔여용량: 매일 `floor_x-current_x+남은 상점/타운 소비`의 72%로 우유·양털 가축/딸기 상한, 초과 가축 슬롯은 거위 추가 없이 밀로 환류(기존 거위 상한 4, 가축/사료/노동 총량 비증가). **선택 +2,465(se 715, 악화 4/32; milk0/1/2/3/yarn +2.7/+5.1/+0.7/+2.8/+2.6k), 홀드 +2,232(se 454, 악화 2/32; +4.2/+1.7/+1.3/0/0k)** · 이동 56.0%/PASS 508 · `state/o_dev/opp_planner_proxy_c2_wp4.py` · eval `c2_wp4_5`/`c2_wp4_6`.
- 09-17 14:10 **c2-000(WP4 시장 잔여 용량) 병합 → base3**: 확인 측정 vs o227 **홀드아웃 72.3k(base2 70.1k, +2.2k)·선택셋 71.7k(69.3k, +2.5k)** — c2 보고와 일치. 누적 60.5k→71.7k. 백업 `state/o_dev/opp_planner_proxy_base2_backup.py`. c3-000(딸기 씨앗 슬롯 회계) 선택셋 +0.5k → 미달(c3 자체 판정). c1 WP1 보고서(`reports/c1-wp1-2026-09-16.ko.md`): 밀 시비→age3 5단위 이행률은 73%까지 올릴 수 있으나 현금 중립~악화, h22/h0 14단위 배치는 홀드 +1.65k/선택 +0.72k로 미달 — WP3/WP4 통합 뒤 재평가 권고.
- 09-17 14:15 o227 라이브 98경기: 22패, 2400–2749 51/70(73%), **2750+ 0/2**, <2400 25/26. 미러 노이즈 17.
- 09-17 14:20 공개 노트북 갱신 확인: **V45 "First-Turn Wheat Round Trip"**(09-15) — 0턴에 [BUY WHEAT 70, SELL WHEAT 70] 한 쌍으로 라운드트립. 테이프 계보의 분할 매수(부모 V44는 [5,10,60], 우리는 [13,10,30])의 두 번째 매수를 같은 턴 인터리브로 ~$60 비싸게 만들어 멜론 1개를 덜 심게 함(V45 vs V44 98%·+1.4k). 라이브 상대 2명이 이미 사용 중이라고 명시. 우리 o227에 미치는 효과 측정 중(vs V45·vs V44 32경기 병렬).
- 09-17 15:00 **V45 영향 실측**(고정 세계 32경기): o227 vs V44 30/32 +2.5k → **o227 vs V45 22/32 +1.3k**(중앙값 +417). 메커니즘 확인(시드 7005): 0턴 우리 [BUY13,BUY10,SELL30] vs V45 [BUY70,SELL70] → 0턴 후 현금 2993→**2940**, d1 멜론 12→**11**.
- 09-17 15:20 **o238_open_roundtrip** = o227 + `overlays/o238_open_roundtrip.py`(0턴 분할 매수를 [BUY 70, SELL 70] 한 쌍으로, 그 외 변경 없음; sha ddba8c40): **vs V45 30/32 +2.5k**(V44 수준 완전 회복), **vs o227 미러 32/32 +1.2k**(최소 +585; 미러가 멜론 11개가 됨), 0턴 후 현금 3000. 공개 계보 전체(분할 매수 개막)에 대한 비대칭 타이밍 이득. 린 검증(`validate.ps1 -Base o227 -Full`) 진행 중; 풀32·은행은 사용자 실행 예정.
- 09-17 16:10 o238 린 검증: 스위트 88 **+3,179**(CI [+1251,+5737] SIG+, L→W 8/W→L 1), 홀드아웃 40 **+4,834**(SIG+), 풀10은 승 158→148/160 — 전부 시드 7004(v43·aurax7·lynn v4/v5·tetsu, 우리 110k→90k·상대도 −20k)와 7006(v40)에서 발생. 추적 결과 **개막 라운드트립 자체는 의도대로 작동**(0턴 후 우리 3061·상대 2939)했고, 손실 원인은 상대의 타일 변화로 **상점 시퀀스가 바뀐 것**(7004: ICE,SMOOTHIE,FM → ICE,PET,YARN,PET,YARN) = 세계 변경 노이즈. 고정 세계 A/B(o227·o238 각각 vs 6개 풀 상대, 32경기)로 재판정 중.
- 09-17 18:30 **고정 세계 풀 A/B(o227→o238, 32경기씩)**: v43 30→32승(우리 +437·상대 −863), aurax7/lynn5/tetsu 32→32(+444/−870), **v40 32→32이나 우리 현금 131k→100k(−31k)**: o227 개막은 v40([13,30,30] 분할 매수)을 0턴 $2598로 몰아 d2 소 이탈 붕괴(78k)를 유발했는데, o238의 더 큰 타격($2517)은 v40이 멜론 10개만 심게 해 사료 현금이 남아 소를 지킴 → 정상 미러(98.5k)로 회복. 승패 무영향(레이팅은 승패), 마진만 축소. 풀10의 시드 7004/7006 패배는 세계 변경 노이즈로 확정(고정 세계에서 0패).
- 09-17 18:35 c1-222(밀 h22/h1 14단위 배치)를 base3에 이식해 측정: 선택셋 **+1.3k**(se 0.29, 6악화/22개선), 홀드아웃 **+0.7k**(se 0.26, 10악화) → 두 세트 모두 +1.5k 미달, 미병합(c1-219와 동일 결론). c1의 "+2.06k"는 8경기 값싼 게이트 수치.
- 09-17 18:50 **o238_open_roundtrip 제출(사용자 승인)** — `agent/o238_open_roundtrip.py` sha ddba8c40, 남은 슬롯 3. 라이브 추적: `o_tools/live_losses.py --sub <ref>`(ref는 제출 목록 첫 줄). 150경기 전 레이팅 비교 무의미; 볼 것은 (1) 2400+ 구간 승률이 o227(73%)보다 높은지, (2) 0턴 개막이 다른 계열(매도 후 재매수형)과 만났을 때의 초반 패배 여부, (3) V45 계열 상대 전적.
- 09-17 18:55 **중복 제출 사고**: 사용자 직접 제출(56275029)과 Claude 제출(56275012)이 겹쳐 같은 o238 파일이 2건 등록, 슬롯 1개 소모(남은 슬롯 2). 원인: "제출하자"를 실행 지시로 오독. 규칙 고정: Claude는 제출 명령을 실행하지 않는다(메모리 kaggriculture-never-submit). 라이브 추적은 두 ref 모두.
- 09-17 19:40 라운드트립 크기 매트릭스(시드 7005, 0턴 후 현금 우리/상대 · d1 멜론): 70 → o227형 2940(멜론 11)·c129형 2940(10)·**V45 3000/3000(중립)**·v40 2517(10); **50 → o227 2950(11)·V45 2925(11!)·c129 2950(12)**; 60 → o227 11·c129 10·V45 2956(12, 우리 +44); 40 이하는 분할 매수형에 무효. 즉 작은 쌍이 큰 쌍(V45)을 이기고, 큰 쌍이 분할 매수형을 이기는 '크기 게임'. o239_50/o239_60 빌드(sha a004686c/0d64d159). **체인10(6시간, 추적 백그라운드)**: (1) 크기 50/60/70 × 7상대 × 32고정경기, (2) o238 풀32, (3) o239_50/60 풀32, (4) o238 은행 버킷 vs o227. 로그 `o_results/chain10.txt`, 완료 마커 `chain10.done`.
- 09-17 19:50 체인10 1단계(크기 A/B, 3크기 × 7상대 × 32고정경기) 완료: **50이 전 상대에서 우세 또는 동률** — vs V45 32/32 +3.85k(70: 30/32 +2.5k), c129 +9.9k(+7.2k), yhay81 +14.6k(+9.9k), o227 +1.17k(≈), v43 +2.7k(+3.7k), v40 +5.1k(+5.5k), tschinkel 동일. 60은 70과 거의 동일. → **o239_50이 후보**. 2단계에서 bash의 `@(...)` 파싱 오류로 중단 → `-Command` 호출로 수정해 재시작(o239_50 풀32 → o238 풀32 → o239_50 은행 → o239_60 풀32 → o238 은행).
- 09-17 21:30 플래너 집중(사용자 지시, 하위 세션 종료; c3-000~010 전부 기각·c3-006 홀드아웃 +0.1k). o227 상대 수입 감사(양 좌석, 3세계)로 격차 분해: **멜론 첫 판매 시점**(o227 d10 h09–15에 72개 $232–272; 우리 d12+ $140), 딸기 코호트 지연, 급식 실패(d12–17 하루 2~3마리 미급식 → 배치 S에서 이탈 발생). 원인 추적: 멜론 급수가 스트립 소유자 1명에게만 배정돼 하루 1~2칸씩 급수(d9 4/12) → age10 도달 지연; 급식자 2명(세계 비율 6.0)이 **같은 동물을 따라다니며**(구제 급식 pr−1이 소유 규칙을 우회, FEED 뒤 CARE를 다른 급식자가) 하루 9~11/15만 급식.
- 09-17 21:35 수정(사이드 카피 T=base3+급식 수정, S=T+멜론 개막): 구제 급식(어제 미급식 동물 pr−1, h8 이후 전 워커), 급식자별 **안정 축군 분할**(전체 가축 스네이크 순, 소유 규칙을 구제·here에도 적용), 지연 시 FEED+CARE만; 멜론: d0 소2·양2·멜론12·양1, 멜론 창 급수 pr0(age≥10·오후 전 워커 공유), 익은 멜론 수확 pr0, 12개 단위 즉시 입고. 7002: 멜론 수입 1.2k→10.9k, 최종 51.1k→57.8k; 7006: 급식 9~11→12~13/15. T/S 선택셋·홀드아웃 32경기 측정 중.
- 09-17 22:10 T(base3+급식 수정)/S(T+멜론 개막) 32경기: T 선택 −1.3k/홀드 −3.3k, S −0.2k/−2.4k → **둘 다 기각**. 단일 세계(7002·7006)에서 확인한 개선이 32경기에선 역전 — 증분 패치의 부작용을 진단 없이는 볼 수 없다는 점을 재확인. 결론: 프록시는 재작성(planner_v2: 배분기·스케줄러·시장정책 3모듈)으로 전환, 측정은 스코어보드 1줄로 표준화, 숫자 노브는 무인 스윕.
- 09-17 22:30 체인10 풀32(비고정 세계): o239_50 패 2→27/1344, o238(192경기 시점) 0→14 — 전부 **상점 시퀀스가 바뀐 시드**(7025: BRUNCH,PIZZA,BRUNCH,PIZZA → BRUNCH,BRUNCH,PIZZA,PIZZA에서 상대 전원에게 근소 패; 7008·7031 동일)에서 발생. 0턴 주문 변경 → 상대 멜론 −1 → 타일 점유 변화 → 잡초 RNG → 상점 재추첨. 이 효과는 라이브에서도 양방향 무작위이며 후보의 실력과 무관하므로 **0턴 개막 변경의 게이트는 고정 세계 A/B로만 판정**(풀32는 세계 혼동). 고정 세계에서는 회귀 0.
- 09-17 23:00 **방향 확정(소유자)**: 목표 2주 내 1위, 플래너 라인만, 후보 넘버링 p000~. `AGENTS.md` 최상단에 목표·방식·넘버링·판정 규칙·마일스톤·문서 읽기 순서를 기록(Codex/Antigravity 공용). 테이프 체인10 중단(고정 홀드아웃으로 o239_50 판정 완료). 다음: p000 계획 탐색기 설계(14절) + 1줄 벤치.
- 09-17 23:40 **p000 생성**(`agent/p000_planner.py`, 스위치 9개+노브 8개, 전부 off = base3 동일 검증) + `o_tools/p_search.py`(optuna TPE, 선택셋 paired 목적, 25회마다 홀드아웃 확정). 400회 서치 시작(12워커, ~30초/회). 초기 랜덤 8회는 −2.4~−6.0k(무작위 조합은 base3보다 나쁨; TPE 수렴 대기).
- 09-18 00:20 p000 서치 앵커 결과(선택셋 32경기, base3 대비): **herd_split +1.1k(se .64)**, melon_water +0.9k, melon_harv0 +0.8k, fert_h0 +0.2k, behind 0, melon_bank −0.5k, pr0_share −0.6k, **rescue −2.9k**, **melon_open −2.1k**; 전부 on −0.2k. → 어제 T/S가 실패한 이유는 rescue(전 워커 구제 러시)와 12멜론 개막. 유망 조합(herd_split+melon_water+melon_harv0 ± fert_h0/behind/feed 4.5·5.0) 10건을 스터디에 큐잉. 서치 계속(12워커, ~30초/회).
- 09-18 01:30 **전략 전환(소유자)**: "o239_50으로 10위권 진입 후 방어". 근거: 10위 컷 ≈ 3000이고 테이프 포크(Tschinkel 2995·Catalyst 2965)가 바로 밑에 있음; 우리 라이브 패배 19건 중 14건이 미러 동전던지기 → o239_50(미러 32/32·V45 32/32·포크 6종 무회귀)이 이를 제거. 제출은 사용자 직접. 방어 규칙: 라이브 하루 2~3회(미러 패배 소멸·2400–2749 승률 85%+·새 개막 계열 감시), 공개 노트북 일 1회, 대응 판정은 고정 세계 A/B만. 플래너 서치는 백그라운드 지속(p000b), 구조 변경은 방어 신호 대응 뒤 순위.
- 09-18 01:30 p000b 서치 앵커 추가분: no_wheat_fert +0.5k, fert_batch +0.4k, sheep_plus 1 +0.4k(2·3: −0.9/−1.2k), room_f 0.5 +0.7k(1.0: −1.0k). 모든 요소 ≤ +1.1k → 48k 격차는 노브 밖(케어 보너스 손실 = 축군 분산 → 급식 80%). 다음 구조 변경 후보: 축군 블록 예약 배치(Fable 세션에서).
- 09-18 01:45 **o239_50 제출 → ref 56278146**(소유자 외출 중 명시 요청으로 Claude가 실행; 제출 전 중복 여부 확인). 오늘 남은 슬롯 1. 라이브 추적: `live_losses.py --sub 56278146 --sub 56275029 --sub 56275012`. 판정 포인트: 미러 패배 소멸, 2400–2749 승률 85%+, 새 개막 계열.
- 09-18 02:20 테이프 멜론 선점(o240 후보) 조사: 테이프는 d10 h05–07에 멜론 10칸 수확 → 운반자가 2~4칸 걸어 h09–13에 PLACE+SELL(드롭 턴). 배달은 이미 최단이고, 더 이른 판매는 age10 급수를 h00–02로 당기는 **경로 수술**이 필요 → 이동 명령 대본이 어긋나 불가(o231/route 계열과 같은 실패 구조). 멜론 시장은 상점 소비 0(타운센터 1/일)이라 보류도 손해. 결론: 테이프의 미러 대비 비대칭 레버는 0턴 개막(o238/o239)이 사실상 마지막. 테이프 순위는 라이브 수렴(경기 수)과 크기 게임 감시만 남음.
- 09-18 03:00 **p000b 서치 결과 → base4 승격**: TPE 282회 수렴 설정 {herd_split on, buf 2, room_f 0.5, wheat_units 3, straw 26} — 선택셋 **+3.7k**(se .8, 4악화) · 홀드아웃 **+2.0k**(se .6, 6악화) · **신규 시드 7032–7047 +2.0k**(se .6, 7악화) → 3세트 합격. `agent/p000_planner.py` 기본값에 반영(스위치 기본 on: herd_split), 기준선 라벨 `base4_sel/hold/fresh`(75.4k / 74.4k / 74.7k). 교훈: 서치 초반 선택셋 상위(+2~2.7k)는 전부 홀드아웃 실패(잡음 선택) — 앞으로 판정은 3세트(선택·홀드·신규)로. 서치 중단(노브 바닥 도달), 다음은 구조 변경.
- 09-18 05:30 **정확 수입 장부**(`o_tools/income_audit.py`: 엔진 `_commit_unit` 훅, 단위별 판매가 정확·구매·**창고 폐기**까지) + **축군 감사**(`o_tools/herd_audit.py`: 일별 급식/케어율·분산·배치도). o227 대비 4세계 8경기 격차 −47k 분해: FERTILIZER −11.7k(o227 346개 vs 144개; 시장 총 파이 ≈25k 제로섬), STRAWBERRY −9.3k(32.5주 vs 21주, 주당 7.6 vs 5.6개), MILK −8.9k(소 구매 3~5일 늦음; 소당 산출은 잠재치 도달), MELON −6.7k(선판매 경쟁), WHEAT −5.4k, WOOL −3.7k. base4 급식률 d6–28 90%(o227 87.7%!) → 급식은 주 격차가 아님. 노동: p000 이동 150/일 vs o227 105/일(생산 행동 2075 vs 2824/경기).
- 09-18 05:30 **축군 블록 예약(sw_herd_block) 기각**: v1(창고 링 d≤3 예약) 4세계 −4k(예약 타일 3~6일 유휴, 작물 손실); v3(건설 타일 클레임 + 축군 인접 대기 2칸) 선택셋 **−2.45k**(se .63, 23악화) — 급식 93%·양털 +18개는 얻지만 멜론/딸기/밀 손실이 더 큼. sw_d28_feed(d28 급식자 밀 보관 루프 수정) +0.1k(se .12) 무효. 둘 다 스위치 off 유지.
- 09-18 05:45 **창고 100칸 폐기 누수 발견 → sw_shed_cap**: 일말 인벤토리 드롭이 창고 상한(100)을 넘으면 폐기 — base4는 경기당 ~55개(밀 37·딸기 6·당근 5…) ≈ $3.4k 폐기(d17·18·21·26·27). h22–23 시장에서 초과분을 매도(밀은 내일 사료분만 보존 → 비료 → 저가 상품 순). 3세트: 선택 **+1.29k**(se .35, 5악화/19개선) · 홀드 **+0.99k**(se .37, 3악화) · 신규 **+1.31k**(se .27, **0악화**/15개선). 합격선(+1.5k) 미만이지만 96경기 일관 양수 → 다음 개선과 합산 판정. cap_target 80 동일(+1.30k).
- 09-18 07:30 멜론 러시(sw_melon_d9: d10 h1 전 플랜터가 age10 멜론 즉시 수확·입고·매시 전량 매도) 시험: 엔진상 수확은 age≥10(first_yield_day)이라 d9 저녁 판매 불가. d10 아침 러시는 인부 고용이 h0–h3에 분산(현금 부족)되고 왕복이 겹쳐 첫 판매 h8, 대부분 h8–14(o227 h9–15와 겹침). 4세계: 멜론 +1.5k·o227 −2.3k지만 딸기/양털 손실로 총액 0~−3k → **보류(off)**. sw_hire_res(전날 h8부터 내일 인부 전원 고용비 예약) 4세계 −0.9k → off. sw_d28_feed off. prw 노브(우선순위 가중치 2/3 vs 거리) 선택셋 −0.5~−2k(se .8) → 6 유지.
- 09-18 08:10 **이동 분류**(d10–27 일평균, 7000): p000 이동 153 = WATER행 40·**자정행(마지막 행동 뒤 걷기) 24**·HARVEST행 17·FEED행 17·**출근길 15**·FERTILIZE행 11·PLANT행 8·창고행 7; o227 108(자정행 6·출근길 4). → **sw_horizon**: 남은 시간(23−hour) 안에 도착·실행 못 할 작업은 배정하지 않음(고정 배정 포함). 자정행 24→16, 행동 수 동일, 4세계 +1.3k.
- 09-18 08:40 **base5 승격**: {shed_cap, horizon} 기본 on. 3세트(base4 대비): 선택 **+2.77k**(se .72, 5악화/24개선) · 홀드 **+2.60k**(se .66, 4악화/24개선) · 신규 **+3.40k**(se .44, **0악화**/28개선) → 합격. 상대(o227) 현금 −4.5~−6.8k(딸기 140개 판매로 공유 시장 가격 하락). 라벨 `base5_sel/hold/fresh`(78.5k / 77.0k / 78.1k). 남은 자정행 16·출근길 15·창고 왕복은 다음 노동 레버(방사형 스트립, 출근길 작업).
- 09-18 09:40 **base6 승격: sw_reserve** — 어떤 워커가 이미 걸어가고 있는 작업(전 스텝 배정)은 다른 워커의 점수 계산에서 제외(낮은 인덱스 워커가 가로채 → 재배정 → 오후 방황이 사라짐). 3세트(base5 대비): 선택 **+2.97k**(se .37, 1악화/27개선) · 홀드 **+2.51k**(se .74, 8악화/24개선) · 신규 **+3.19k**(se .40, 2악화/30개선) → 합격. p000 = 81.1k / 79.5k / 81.3k(base4 75.4/74.4/74.7 → +5.7k/+5.1k/+6.6k 누적). M1(85k) 근접.
- 09-18 11:30 단일 스위치 추가 시험(base6 대비, 선택셋): radial 스트립(창고에서 쐐기형) **−1.3k**, bank_cut(h22 이후 입고 걷기 중단) −0.2k, herd_first(d6–8 동물→땅→딸기 순) 선택 −0.2/홀드 +1.8/신규 0 → 기각, herd_angle(급식자 몫을 각도 쐐기로) 급식률 하락 → 기각, collect_here(급식자가 서 있는 칸의 비료를 즉시 수거) 비료 +47개·급식 −2.4pt → 선택 +1.0/홀드 +0.2/신규 +0.2 기각, prw 2/3/4 0/−0.1/−1.7k, melon_water+harv0(+bank) 멜론 72개(+2.6k)지만 딸기 손실로 총 −1.5k, straw 32·34 + room_f 1.0·1.4 **−2.7/−3.7k**(일부 세계 −18~−26k 붕괴).
- 09-18 12:10 **base7 승격: straw 30 + feed 4.5(전 세계)** 묶음. 3세트(base6 대비): 선택 **+1.99k**(se .60, 6악화/20개선) · 홀드 **+2.30k**(se .49, 4악화/24개선) · 신규 **+2.81k**(se .51, 3악화/25개선). p000 = **83.1k / 81.8k / 84.1k**(base4 대비 +7.7/+7.4/+9.4k). 단독으로는 straw 30 +0.9k, feed 4.5 +1.1k(합격선 미만) — 묶음 후보로 3세트 판정. M1(85k)까지 ~2k.
- 09-18 13:00 base7 장부(4세계): 총 −34.7k = 비료 −9.9k·우유 −7.6k·멜론 −6.3k·딸기 −4.5k·밀 −4.2k·양털 −2.3k; 폐기 밀 22개 재발(창고 잔량 부족: h23 매도는 창고분만 가능, 인벤토리 80+개는 못 팔음). 추가 시험(4세계): cap 여유 12/6 +0.9k(서치 앵커로), bank_pm(유휴 운반자 h16+ 입고) 0, herd_first v2(2번째 땅 우선 유지) **−2.2k**(우유 +14개·양털 +11개지만 양측 우유 단가 149→138: 공유 시장 포화), straw_open(멜론 대신 d0 딸기 6→14주) **−9.2k**(멜론 11k 손실, 딸기 +1.3k뿐), fert_buy(비료 ≤$60일 때 부족분 구매) 0(구매 $247). 멜론 pr1 창 급수+즉시 수확+입고 조합 0.
- 09-18 13:10 `o_tools/p_search.py` base7 기준으로 갱신(SWITCHES 15: 기존 8 + collect_here·herd_first·bank_pm·d28_feed·hire_res·herd_angle·herd_block; 노브 13: feed·straw·melons·land3·buf·wheat_units·melon_pr_age/hour·sheep_plus·room_f·cap_m23·cap_m·prw; 앵커 = base7·스위치 단독·근접 실패 조합). **스터디 p000c 300회 백그라운드 시작**(12워커, ~40초/회, 25회마다 홀드아웃). 보드: `o_results/p_search/board.txt`. 다음 세션: 보드 상위를 3세트로 확정 → base8.
- 09-18 14:50 **p000c 서치 300회 완료 → base8 승격**. 수렴 설정 t0126 = {room_f 0.4, sheep_plus 1, straw 32, land3 8, cap 여유 12/6, prw(오후) 8, collect_here·d28_feed·fert_batch on}. 3세트(base7 대비): 선택 **+3.49k**(se .46, 1악화/27개선) · 홀드 **+2.79k**(se .43, 2악화/27개선) · 신규 **+2.00k**(se .34, 5악화/25개선) → 합격. p000 = **86.6k / 84.6k / 86.1k** → **M1(85k) 도달**(홀드 −0.4k). 라벨 `base8_*`, 스냅샷 `state/o_dev/p000_base8.py`. 교훈: 단독으로 기각된 collect_here·d28_feed·fert_batch가 room_f 0.4(시장 여유를 더 보수적으로)·sheep_plus 1과 묶이면 통과 — 노브 상호작용은 서치가 잡는다. 서치 기준선을 base8로 갱신.
- 09-18 15:40 base8 위 추가 시험: melon_d9(d10 러시) 3세트 +0.05/+0.5/+0.3k → **기각(멜론 경주 종결)**: 인부는 매일 창고에서 출발(엔진: 일말에 인부 소멸·농부 (4,4) 리셋)하고 멜론은 거리 2~4라 첫 입고가 h8~13 → o227 h9 덤프와 겹침. melon_open(12멜론 d0)은 3번째 양이 d3+로 밀리고(저축 규칙 추가해도) 딸기 지연 → −1.7k. land4(4번째 사분면 $4000, d10~) 밀 +130개지만 딸기·우유 손실 → **−4.6k** 기각(o227도 안 삼). hire_res(d9 한정) 0.
- 09-18 15:45 서치 p000d(base8 기준, 경계 확장: room_f 0.3~0.5·straw 28~36·cap_m23 9~15·prw 6~10, 300회, 8워커) 진행 중. 남은 격차(base8, 4세계) −29.8k = 우유 −7.3k·비료 −7.0k·멜론 −6.4k·딸기 −4.8k·밀 −3.9k. 우유는 공유 시장 포화(양측 물량↑ → 단가↓)라 축군 확대의 순효과 작음.
- 09-18 16:40 **토마토 힌지(sw_tomato)**: 토마토 상점(PIZZA/FARMERS)마다 6/일 적자가 쌓여 후반 가격 $100~300(2~3상점)인데 양측 다 거의 안 팖. d13–18에 상점당 6주(최대 18, 밀 타일 대기 허용·토마토 먼저 심기), d26까지 보유 후 상점 소비 속도(1.5×상점/시간)로 매도. 8세계 토마토 60→68개 $100(7003: 91개 11.3k, 7005: 52개 7.5k). 3세트(base8 대비): 선택 **+1.56k**(se .45, 7악화) · 홀드 +0.82k(se .21, 2악화) · 신규 +0.61k(se .19, 6악화) → 일관 양수지만 합격선 미만 → **묶음 후보**(p000d 승자와 합산 판정). 상한: 적자는 상점 수·해금일에 좌우되고 o227도 4상점 세계에선 88개를 팖.
- 09-18 16:50 당근(sw_carrot: PET_CAFE 12/일 수요에 맞춘 회전 12칸) 7001(PET 2) 93→134개 +2k지만 FARMERS 전용 세계에서 base의 "항상 씨앗 8" 회전이 더 나음 → 총 +0.1k, **기각**. 결론: base의 당근 정책은 적정, 시장 잔여 여지는 PET 2개 세계뿐.
- 09-18 18:30 p000d(경계 확장) 300회: 최고 +0.97k(se .74) → 홀드 +0.25/신규 +0.57 → **무효**(base8은 노브 공간의 국소 최적). 토마토 묶음(pdtom) +3.7/+1.2/+1.1(se .7~.9) 미달.
- 09-18 19:30 격차가 큰 세계 7030(ICE_CREAM×2·YARN×2, o227 181k vs 126k: 양털 87k vs 56k) 추적 → **밀 사료 병목**: 창고 밀이 h6 이후 0(d12–14·19–26), 급식자마다 8개씩 집어 마지막 급식자는 빈손, 사료 보충 규칙이 플랜터 주머니의 수확 밀까지 재고로 셈, 시장 주문 10개 상한 때문에 고용이 h0–h2에 분산(인부 3~4명분 노동 손실·급식 몫 매시간 재분할). 수정 3종: hire_first(고용 먼저, 작은 매도 미룸), pick_own(자기 몫+1만 집기, h0–2는 예상 몫), feed_stock(미급식 수 − 창고 − 급식자 주머니(몫 한도)만큼 구매). 7030: 이탈 3→1, 134.0k(+7.5k). **그러나 3세트: 묶음 −1.4/−1.6/0(17·22악화)**; 단독 hire_first **+0.81/+0.77/+0.77k**(악화 4~5), pick_own **−2.2k**, feed_stock **−1.6k** → 사료 논리 변경은 기각, hire_first는 묶음 후보. hire_first+tomato: +3.2/+1.0/+1.1(홀드 −9.5k 1건) 미달.
- 09-18 19:40 서치 p000e(base8 + tomato·hire_first·pick_own·feed_stock 스위치 추가, 앵커 = tomato+hire_first 조합들, 250회, 12워커) 시작.
- 09-18 21:30 p000e 250회: 상위 설정 전부 tomato+hire_first(+bank_pm, straw 34, buf 4) 계열 — 선택 +3.2~3.8k이지만 **홀드 +0.9~1.36k(se .6)** → 전부 fail. 홀드의 7018(SMOOTHIE×2·PIZZA×2, 우유 $238 세계)에서 hire_first가 −5.2k: h0 매도를 미루면 창고 재고↑ → 시장 여유 상한(room_f)이 소 1마리를 덜 사고 급식 96.9→94.2%. hire_keep(상위 매도 3~5건 유지)로 7018은 회복되지만 선택셋 이득이 +0.8→+0.1k로 사라짐(이득의 출처가 고용이 아니라 h0 매도 지연이었던 셈; 잡음 수준). **base8 유지.** 기본값 재현 확인, 스냅샷 갱신.
- 09-18 21:35 결론: base8 부근에서 스위치/노브 단위 개선은 소진(p000d·p000e 두 서치 모두 홀드 미달). 다음은 (a) 런타임 계획 탐색 p001 설계 또는 (b) 첫 라이브 시험(사용자 제출)으로 실제 상대군 대비 위치 측정 — 소유자 판단 필요.
- 09-18 22:10 base8 vs 테이프 3종(선택 시드 32경기): V45 87.2k vs 111.4k, o239_50 86.6k vs 111.4k, c150 86.4k vs 107.7k — **전부 0/32**. 플래너는 아직 테이프 계보 전체(107~112k) 아래. cow5(d2–5에 소 2마리를 딸기보다 먼저) 4세계 −1.9k: 시장 여유 상한 때문에 총 소 수는 같고 딸기만 늦어짐 → 기각. 라이브 보정 제출은 정보 가치 낮음(모든 테이프에 패배 확정).
- 09-18 22:40 melon_near(d0 축군을 창고 링 밖(거리≥3)에, 멜론을 링 안에 → d10 러시 첫 판매 h4, h9까지 30개) 7000: 109.0k vs 110.4k — 급식자 매일 왕복 비용이 멜론 선판매 이득을 상쇄 → 기각. 멜론 경주 최종 종결.
- 09-19 라이브 점검(소유자 요청): o239_50(56278146) 102경기 89승 13패 = 87%(2400–2749 52/63 83%, 2750+ 1/1, <2400 36/38) 점수 **2670.5**(아직 강한 상대와 거의 안 붙어 저평가); o238 #2(56275029) 114경기 79승 35패(2750+ **13/30 43%**) **2755.3**; o238 #1(56275012) 51경기 45승 6패 2754.2; o227 99경기 76승 23패 2703.8. 팀 최고 점수는 o219 2795.9(09-15). 리더보드: 1위 Majkel 3189, 10위 컷 **~3031**(09-15 스냅샷 2983 → 상승 중), 2796은 스냅샷 기준 **~152위**, 2755 ~211위. 패배 유형: 미러 잡음(o238 17/35 → o239_50 5/13로 감소), **포트폴리오 베팅 상대**(goose/yarn 세계에서 당근 −15.8k·토마토 −16.2k·−9.2k 등 힌지 시장 대량 판매)에 −8~−12k 대패 — 테이프는 대응 불가, 플래너 토마토/당근 분석과 일치.
- 09-19 공개 노트북 재조사(소유자 요청, 플래너형 유무): 최신 16개 풀(`state/o_dev/public_pull_2/`, 추출본 `state/o_dev/public_agents2/`). **강한 상태 기반 플래너 공개 코드는 없음.** 상위 공개 코드는 전부 Shop Router 0909 계보(= 우리 o227 테이프)에 반응형 레이어를 얹은 것: V44/V45, "2820 score"(V44+레이어, 라이브 2801·~188위), "2900+"(압축 액션 테이프+프런트런), "7-turn rescue"(0909+말기 수거), "Fully Dynamic Autonomous Agent"(무테이프 주장이지만 25겹 레이어의 V계보 섀시 — 고정 세계에서 o227과 장부가 사실상 동일한 미러: 95.3k vs o227 98.6k, 0/32). 상태 기반: Pure RL(BC+PPO) **77.0k**(p000 86k 미만), 소형 규칙 에이전트 22~34k, EcoBot v7(목표 기반 매크로+일 1회 VRP 배차 — 우리 구조와 같음)는 소스가 미첨부 데이터셋이라 입수 불가. 1위 계보(Majkel 오프너) 소스도 여전히 미공개(r000과 동일). 결론: 플래너는 자체 개발뿐; 참고 가치는 EcoBot의 "일 1회 VRP 배차" 설계(WP2와 같은 방향).
- 09-19 **세계 적응형 포트폴리오 1라운드** + 조건부 규칙 판정 도구 `o_tools/cond_pair.py`(3세트 96경기를 "규칙이 발동한 경기(현금이 달라짐)"와 "비트 동일 경기"로 나누고 상점 특징별 이득 출력). 결과: **egg**(BAKERY/BRUNCH 수만큼 거위 2/4/6) 발동 32경기 +0.1k, 2상점 세계 −0.2k(6악화/0개선) → 기각(급식 용량 한계). **yarn2**(YARN 2개면 양 +6) 발동 4경기뿐: 4-YARN 세계 +11.7k, 2-YARN(7030) −1.5k → 보류. **carrot2**(PET_CAFE당 당근 회전 +6) v1은 free//2 캡에 막혀 발동 1경기; 밀을 밀어내게 바꾼 v2는 1-PET 세계 **−0.75k(14악화/1개선)**, 2-PET +0.3k → 기각. **tomato**(토마토 상점 ≥2에서만): 발동 86경기, 상점 수에 단조 증가 — 1개 +0.4k(매도 보류만), 2개 +1.9k, 3개 +3.6k(0악화/14개선), 4개 +12k; 주당 6/8/10 비교: 8주(최대 24)가 홀드 0악화로 가장 안정(합계 **+1.63k**, se .24, 6악화/55개선; 세트별 +2.56/+1.37/+0.95k).
- 09-19 **base9 승격: sw_tomato(≥2상점, 8주/상점, 최대 24, d26까지 보유, 소비속도 매도)**. 판정: 조건부 규칙 예외(문서화) — 96경기 합계 ≥ +1.5k(≥4 se), 세트별 ≥ +0.5k, 악화 ≤ 10%, 발동 특징에 단조 → 통과. p000 = 89.2k / 86.0k / 87.1k. 스냅샷 `state/o_dev/p000_base9.py`, 라벨 `base9_*`.
- 09-19 **WP2 착수: VRP 배차기(sw_vrp)** — `Proxy.dispatch_vrp`: 매 스텝 전 워커 경로를 새로 구성(비지속), 우선순위 순으로 각 작업을 "추가 비용(이동+행동+아이템 없으면 창고 우회) 최소" 워커·위치에 삽입하되 균형 상한(cap = 1.4×2.5×작업수/워커수, 하루 남은 시간 이내) 안에서만, 경로는 최근접 순서(긴급 pr≤0 우선)로 재정렬·초과분 절단, 창고에 없는 아이템 노드는 건너뜀, 유휴 워커는 운반물을 창고에 입고. 구역/스트립/급식자 분할 없이 누구나 급식. 시행착오: 최소 추가비용만 쓰면 한 워커에 몰림(7명 유휴, 67k) → makespan 최소화는 지역성 파괴(이동↑, 55k) → 지속 경로는 stale 노드로 예산 낭비(69k) → **균형 상한 + 최근접 정렬 + 유휴 입고**로 4세계 8경기 88.6k vs base9 87.3k(7/8 개선), 급식 95%, 딸기 255개(139), 이동 105~139/일(140), 유휴 18~50/일(작업 공급이 한계 → 포트폴리오 확대 여지). 3세트 96경기: **+0.32k**(se .21, 31악화/47개선) — 중립. 배차기 자체보다 그 위의 용량 노브 재조정이 필요 → 서치 p000f(vrp 고정 앵커 + straw 28~40·room_f 0.4~0.6·sheep_plus 0~3·egg/yarn2/carrot2, 200회) 시작.
- 09-19 **p000f(VRP 고정) 200회 → base10 승격**. 승자 t0067(sel +5.0k)은 홀드 +1.4k에서 7030(ICE_CREAM×2·YARN×2) −14.4k 한 경기 때문에 미달 → 절제 실험으로 원인 = yarn2(양 +6이 급식 용량 초과). **yarn2 제거판 f67b: 선택 +4.04k(se .55, 2악화/29개선) · 홀드 +2.26k(se .48, 5악화/23개선) · 신규 +3.14k(se .43, 2악화/27개선)** → 엄격 규칙 통과. herd_block까지 빼면 신규 +1.0k(−12k 이탈)로 나빠져 유지. base10 = VRP 배차기 + {straw 40, buf 4, wheat_units 4, land3 7, cap 9/6, prw 6, melon_pr_age 9/hour 12, egg·carrot2·herd_block·hire_first·feed_stock·bank_pm·melon_water·melon_bank on, fert_batch off}. **p000 = 93.2k / 88.2k / 90.2k**(base4 75.4/74.4/74.7 → +18/+14/+15k), 선택셋에서 o227 상대 첫 승 2/32. 교훈: 단독 기각됐던 스위치(egg·carrot2·herd_block·feed_stock·hire_first·melon_*)가 VRP 배차기의 여유 노동 위에서는 전부 살아남음 — 실행기 용량이 바뀌면 상위 규칙의 판정도 뒤집힌다.
- 09-19 **검증 절차 수정(소유자 지적)**: 7016–7031은 서치 자동 확인이 반복 조회해 홀드아웃이 아닌 2차 선택셋, 7032–7047도 30회 이상 조회해 blind 아님 → 승격마다 **한 번도 안 쓴 16시드 블록을 blind로 1회만 조회**(7048–7063부터, 수정 시 다음 블록). base10을 새 블록 7048–7063에서 base9와 재검증: **+3.43k(se .81, 6악화/23개선), 전 버킷 개선** → 승격 유지. `AGENTS.md` 시드 역할 절 추가.
- 09-19 base11 대기 중 실험(base10 위, 4세계/단일 세계): VRP 사전 적재(vrp_preload) −0.1k, 인부 상한 10/9명 **−1.6k/−5.6k**(11번째 인부도 비용 이상 생산), 2-opt −0.7k → 전부 off. yarn2 실패 원인 재분석: 7030에서 양 24마리는 급식 96.7%로 문제없고 **양털 시장 붕괴**(o227 ~380개 + 우리 374개 > 2 YARN 소비 576개)가 원인 → 시장 여유 모델이 상대 공급을 무시하고 있었음. **sw_opp_supply**: 시장 재고 변화 − 우리 판매 + 상점/타운 소비로 상대 공급률(일 단위, 최근 3일 평균)을 추정해 `market_room`에서 남은 기간의 상대 공급을 차감(축군·딸기 상한에 반영). 추정치 검증(7030): 양털 11~27/일·우유 6~12·비료 18~22로 o227 실제 체결과 부합. 7030 +0.6k(opp_f 1.5 +1.8k), 4세계 +1.2k(7001 +5k, 7000 −2.9k). yarn2는 opp_supply 위에서도 +3 마리조차 −9k → 기각 확정. opp_supply는 p000g 승자와 함께 3세트 판정 예정.
- 09-19 **p000g(base10 기준) 200회: 최고 +1.0k → 무효**(base10도 노브 공간의 국소 최적). **base11 승격 = base10 + sw_opp_supply(opp_f 1.0)**: 선택 +1.60k(se .58, 5악화/16개선) · 홀드 +1.90k(se .31, **0악화**/24개선) · 신규 +1.54k(se .43, 8악화/21개선) · **blind 7064–7079 +2.28k(se .52, 2악화/22개선)**. opp_f 1.5는 합계가 더 크지만(+2.07k) 7032에서 −9.1k, milk3 −0.8k라 1.0 채택. **주의: 마진은 거의 0** — 우리 현금 +1.5~1.9k와 함께 o227 현금도 +1.2~2.3k(과잉 공급을 줄이니 양쪽 가격이 오름). 자체 현금 규칙으로는 합격이지만 승률에는 중립. base12부터 3세트 보고에 마진(우리−상대)을 함께 적고, 마진이 음수면 승격하지 않기로 함. p000 = 94.8k / 90.1k / 91.7k.
- 09-19 base12 탐색(base11 위): 비료 선매도(fert_h0+batch) 자체 +0.16k·마진 +0.4k(잡음), 가격 보유(price_hold: 기준가 75% 미만이면 우유·양털·딸기·달걀 매도 보류) 7030 +0.15k(무효), herd_first −2.6k, cow5 −2.2k → 모두 off. **마진 분석**: base11의 o227 대비 마진 중앙값 −18.6k, 승리는 PIZZA×3 세계(7015)뿐, 최악은 YARN×2 세계(7030·7035 −36k). yarn2 재해석: YARN **3개** 세계(7008)에서는 +16.6k/+14.6k(마진도 동일, 2승 추가), 2개 세계(7030)에서는 −13k → `yarn2_min=3`으로 조건 강화(발동 2/48세계, 나머지 비트 동일).
- 09-19 **테이프 방어 업데이트(소유자 요청)**. 라이브: o239_50 132경기 86%(2750+ 8/13) **2754**, o238 #2 2717(2750+ 16/44), o238 #1 2754(51경기에서 정지), 팀 최고 o219 2796. 공개 신작 3종 입수(`state/o_dev/public_pull_3/`): **V46**(Özer: t0 [BUY 7, SELL 2] 사료 선매, t1 [BUY 30] 리프트, t2 [SELL 30], 3턴 내 예정 판매 즉시 실행), **K0006/Beyond-48**(jaxa623, 라이브 2780~2850: V43 부모 + 예약 지평 24턴 + 2턴 판매 선행 + 매도 주문 앞배치 + t0 [BUY 10, SELL 10]), 마이크로구조 전쟁 노트북. 고정 세계 측정: V46 vs o239_50 96경기 46승(48%, 마진 −0.6k → 위협 아님); **K0006 vs o239 22/32, vs o227 22/32, vs o238 24/32(약 69%)** — 마진 +0.15k의 동전던지기를 판매 타이밍으로 계속 이김.
- 09-19 **o240 = o239 계보 + `agent/overlays/o240_sale_race.py`**(자체 구현): (1) r36 예약 지평을 하루(24턴)로(`_R37_HORIZONS` 래핑), (2) 테이프가 t+1·t+2에 팔 프리미엄 상품(딸기·양털·달걀·우유·멜론·당근·토마토)이 창고에 있으면 지금 매도(첫 번째 매도 품목은 사료 신용 보호로 제외, h23 제외), (3) 매시 시장 주문을 SELL → BUY_PRODUCT/워시 → 나머지 순으로 재배열, (4) 개막 쌍 50 → **10**(단일 쌍 상대에게 50은 리프트를 두 번 지불: Jaxa 44% → 62%). 요소 절제(vs Jaxa 32경기): 전체 14/32, ADV0 10, FRONT0 10, H12 12, ADV3 14 → 세 요소 모두 필요. 사료 t0 선매(FEED0)는 테이프 현금 계획을 깨 44k → 폐기. **최종 o240(sha a0c03048)**: vs K0006 **56/96**(+0.7k), vs V46 **46/64**(+1.1k), vs V45 62/64(+2.8k), vs o227 미러 **56/64**(+0.75k), vs o239_50 **64/64**(+0.9k), vs c150 62/64(+4.4k). 제출은 소유자.
- 09-19 13:13 base12 탐색(base11 위, 4세계 자체/마진): o240 추가 개선 시험 2건(매도 순서 가파른 곡선 우선 17/64 **악화**, 지평 48턴 36/64 동일) → 추가 제출 없음(o240 = 56293679 제출됨). 플래너: wheat6(d6–8 유휴 타일에 밀 20주) 자체 −1.0k·마진 −5.5k(혼돈), melon_open 자체 +0.1k·마진 −7.1k, land3=10 −0.9k, term_pockets(마지막 날 창고 앞 운반물 동시 매도) +15(마지막 우유 6개는 $2짜리), melon_near(VRP에선 herd_block 예약이 우선해 무효) → 전부 off. 초반(d6–9) 유휴 40~50%는 노동이 아니라 현금·땅 저축 제약. 서치 p000h 30/200: 앵커 최고 +0.97k(yarn 3상점 규칙 포함 기본 +0.85k).
- 09-19 13:40 Majkel 정책표(`o_results/proxy/Majkel1337_policy.json`, 289경기) 재독: 축군은 d9 12.6(milk1)/14.3(yarn), d12 14.7/18 → 우리보다 1~2일 앞섬; d6에 땅+딸기 11+동물 6~7(≈4.3k 지출) — d0–5 현금이 우리보다 ~1k 많음. 차이 후보 = **d0 밀 수확을 사료분만 남기고 매도(wsell)**: 4세계 자체 **+1.6k·마진 +2.7k(8/8 개선)** → `sw_wsell`로 승격 후보, 3세트 4워커로 진행 중. Majkel의 다른 특징: 비료 창고 평균 0.2(즉시 매도), 당근 경기당 ~50주(전 세계), 멜론 8.9개 배치 판매, 인부 표는 우리와 동일. carrot_all(모든 세계 당근 회전) −0.5k → off. 서치 p000h 87/200: 홀드아웃 확인 5건 전부 fail(선택 +1.4~2.0k → 홀드 ~0).
- 09-19 13:44 추가 단발(4세계): fert_zero(비료 창고 예비 0, VRP는 주머니에서 시비) 자체 +0.35k·마진 +0.6k(묶음 후보), melons0 7·8(d0 예비 25→8로 7번째 멜론) **−1.3k/마진 −2.1k**(d0 밀 11주가 더 중요) → off.
- 09-19 14:00 wsell 3세트: 자체 +0.30k(se .15, 25악화/41개선), 마진 ≈ +1.0k(o227 −0.35~−1.0k) → 단독 미달. 서치 p000h 근접 후보 **t0088**(base11 + melons 14·prw 8·price_hold·yarn2(3상점)·tom_per 10·vrp_pr 4·vrp_w 2.0·wheat_units 3): 선택 +2.07k, 홀드 **+1.45k**(se .24, 3악화; 합격선 −$51), 4세계 자체 +2.8k·마진 +1.3k(8/8). wsell+fert_zero를 더하면 4세계 +2.0k/+0.7k로 오히려 감소 → t0088 단독을 base12 후보로 신규 세트+blind(7080–7095) 판정 예정.
- 09-19 14:09 t0088 신규 세트 +1.20k(se .26)이지만 **상대도 +1.15k(마진 0)** → 승격 불가. 절제(4세계): t0088 − price_hold = 자체 +1.5k·마진 +2.5k; 그중 **VRP 노브 둘(vrp_pr 4·vrp_w 2.0)만으로 자체 +1.6k·마진 +2.9k**(7000 +5.4k), 나머지(멜론 14·prw 8·토마토 10·밀 3단위·yarn3) ≈ 0, price_hold는 자체만 올리고 o227도 올림. 단독: vrp_pr 4 자체 +0.2/마진 +2.6, vrp_w 2.0 자체 +0.9/마진 +0.2 → 상호작용. **base12 후보 = base11 + vrp_pr 4 + vrp_w 2.0**, 서치 종료 후 3세트+blind.
- 09-17 14:38(재개; 시스템시각 기준) vk(vrp_pr 4·vrp_w 2.0) 3세트: 자체 +0.58/+0.72/+0.80k(se .3/.2/.3), 마진 +2.0/+1.6/+2.2k, 23/96 악화 → 단독 미달, 묶음 성분으로 보류. 평가 시간 재측정: **경기 ~15초, 16시드 세트 50초, 3세트 2.5분**(그동안 과대추정) → 후보는 단일 경기 대신 세트로 스크린.
- 09-17 14:20 7000 시간별 매도 장부: o227 멜론 d10 h9~15 60개 $270→230, 우리는 d10 매도 0(수확 조건 6단위 → d10 급수 후 수확 → 주머니 → 자정 반입 → d11 h0~2 $214→170, 나머지 d12/14 $147/107). 비료 −7.9k는 수거 부족이 아님(우리도 308개 수거, 시비 134개 소비; o227은 팔고 되사기 — 엔진이 매수를 사후가격으로 견적해 왕복 무손실).
- 09-17 14:35 **sw_melon_rush 구현**: d10 멜론 급수 pr −1 → 수확 pr −1(미급수 수확은 h8부터), VRP에서 pr<0 노드는 인부당 1개·경로 선두, 멜론 든 인부는 즉시 창고행, 창고 인접 인부의 멜론은 같은 스텝 SELL에 포함(행동이 시장보다 먼저 처리됨). (링에 멜론이 있으면 (4,4)는 h2, 링 5칸은 h5~h7; 기본 배치(축군이 링)에선 거리 2~4라 h6/h9/h10 — 그래도 o227 h9~15 덤프의 대부분보다 앞섬). d0 축군을 링 밖 북쪽 블록으로 옮긴 판(rush_ring 3)은 d0 배치·급식 지연 → d6 양털 하루 지연 → 땅·소 연쇄 지연으로 sel −0.5k/마진 −2.7k → 축군 배치는 그대로(ring 0).
- 09-17 14:50 rush(ring 0) 3세트: 자체 +0.81/+1.44/+1.38k(se .18/.16/.13, 악화 2/2/0), 마진 +3.0/+3.2/+3.1k. **rush + vk 묶음(hcut 8)**: sel +1.82k(se .30, 1악화)·hold +2.19k(se .20, 0)·fresh +1.82k(se .25, 2), 마진 +4.7/+4.8/+4.3k, 전 버킷 양수. 변형: hcut 6 +1.56k, melon_open(멜론 12·양 2) −1.5k/−2.5k(양 3마리의 d6 양털이 우선), melons0/melons 노브는 무효(현금·하드코드).
- 09-17 14:53 **blind 7080–7095: +1.54k(se .21), 0/32 악화, 마진 +3.9k → base12 승격**. 기본값 굽기(melon_rush on, melon_water10 1, melon_hcut 8, vrp_pr 4, vrp_w 2.0), 7080–83 비트동일 재현 확인, 스냅샷 `state/o_dev/p000_base12.py`, 라벨 base12_{sel,hold,fresh,blind3}, p_search BASE/DEFAULT_ON/앵커 갱신. base12 = 96.6k/92.3k/93.5k(o227 107~112k).
- 09-17 15:15 base13 스크린(sel, base12 대비 자체/마진): 조기 소 cows5=3 −2.2k/−1.4k(우유 +8개에 단가 −$10, 딸기 −1.3k 연쇄), =4 −3.2k; fert_zero −0.7k, +buy-back −0.4k; wsell −0.6k; d0 소1+멜론11 +0.56k/−1.6k(우유 공급 감소로 상대 단가↑); 노브 단발(room_f .5 −2.4k, buf 3/2 −.2/−.4k, opp_f 1.3 +.2/−.7k, tom_per 10 0, land3 8 −.3k, wheat_units 3 −.5k, straw 44/48·feed 5.0 무효); 거위 egg0 2/4 +.1/−.4k, egg1-3 3/6/8 −.25k; rush_all(d1–2 멜론도 익는 날 러시) −0.2/−0.6k → 전부 기각. 노브 공간 포화 → p000i 서치(base12 기준, 200회) 15:17 시작.
- 09-17 15:10 밀 장부(7000): d19 이후 같은 날 매수 16(feed_stock, VRP에서 주머니 밀 미계산)·매도 3~14(예비 초과분 h14+) 왕복 — 스프레드 손실은 ~$100이지만 A는 밀 386개 판매·139 매수, 우리는 216·208(재배 물량 자체가 적음: 파종 135 vs 163, 주당 2.7 vs 3.7단위).
- 09-17 15:45 base12 vs 공개 테이프(sel): V46 96.1k vs 107.5k(4/32승), K0006 95.9k vs 107.1k(4/32승) — o227과 동일한 −11k. 시간대별 매도 분포(7000): 양털·우유·딸기 모두 우리가 h0~4에 먼저 팔고 A는 늦게 팜(단가 동일) → 소비형 시장의 타이밍 레버 없음. 테이프 쪽 멜론 러시 이식은 불가(멜론 타일이 거리 3~5, 이동이 녹화된 테이프라 재배치 불가).
- 09-17 15:58 sw_carrot_hold(당근 힌지 T450: 펫카페 12/일·파머스 6/일 수요 ≥18이면 d26까지 보유(창고 50개 한도) 후 소비율 매도): 96경기 **+144(se 28)**, 발동 58경기 +239, 펫카페 0/1/2 = +9/+238/+314(단조), 악화 2, 마진 +0.2k → 기준 미달이지만 견고한 묶음 성분(변형 hold_max 80·rate 0.5·car_pet 10 동일, sell d24 +71). fert_h0 +160(se 52, 0악화)도 묶음 성분. price_hold는 자체 +0.4k에 상대 +2.2k(보류 = 상대에게 시장 양보) → 기각 확정.
- 09-17 16:30 최악 세계 7029(ICE_C·BAKERY·YARN·SMOOT·PET, −33k) 장부: 딸기 A 251개 $130 vs 우리 152개 $139(−11.4k) — 시장이 적자(재고<I0)라 단가가 안 떨어지는데 room_f 0.4가 우리 재배를 21주로 묶음. 딸기 전용 계수 straw_f 0.6/0.8/1.0(sel): 자체 −1.5/−4.1/−3.7k(승 30→28로 2승 추가, 세계별 ±14k). 7029에서 36주로 늘리면 총 520개 → 단가 $87/82로 붕괴: 우리 +2.3k 딸기·−3.8k 밀(타일 대체)·−2.7k 밀 매수 = 자체 −5.4k, A −8k(마진 +2.5k). 토마토 세계에선 타일을 뺏어 −10k. 딸기 증산은 '상대 타격용 과잉공급'이지 자체 이득이 아님 → 보류(세계 적응형으로 좁히면 마진 +1~2k 수준).
- 09-17 16:45 러시 배치 재시도: 현재 base12의 멜론은 거리 2~4라 매도가 h6/h9/h10(부분 러시). 축군을 북쪽 팔(x=4 열)로 몰아 (4,4)·(3,4)·(3,3)·(2,4)를 멜론에 주는 rush_arm: 멜론 매도 h4/h7/h10, 마진 +0.9k지만 자체 −0.7k(15악화) — 원인은 d6 양털 매도가 h0/h8→h7/h21로 밀려 당일 구매 연쇄가 하루 지연. 동물 수확 pr0(harv_pr0) 단독 −1.1k, +arm −0.9k → 기각. yarn2 2상점 −1.0k(7030 −17k) 재확인, 3상점은 7008 +16k 단독. 늦은 멜론 축소(melons_late 8/6) −1.9/−4.0k. 모든 신규 노브는 기본값에서 base12와 비트동일(7080–83 재현 확인).
- 09-17 17:01 **p000i(base12 기준, 200회) 종료**: 최고 t0185 sel +2.16k → hold +0.31k(se .42, 7악화) 실패; 홀드아웃 확인 8건 전부 실패(sel +1.3~2.2k가 hold −0.5~+0.5k). 노브 공간은 base12에서 소진. 후속 **p000j = 마진 목적함수**(P_OBJECTIVE=margin, paired (자체−상대) 차이; 공간에 straw_f 0.4~0.8·carrot_hold 추가) 17:01 시작, 200회.
- 09-17 17:40 말기 파종 연장 seed_last 26(밀 씨앗 구매 마지막 날 25→26): sel +314(se .11)·hold +683(se .11)·fresh **+883(se .07, 0악화)**, 마진 +0.15/+0.55/+0.85k → 견고한 묶음 성분(27은 −0.7k). 딸기 파종 연장(straw_last 16/18) −0.2/−1.1k 기각. 소유자: 보고 주기 1시간(정시)으로 변경, 외출 중이라 CPU 전부 사용 가능.
- 09-17 17:50 **base13 승격(묶음)**: seed_last 26 + carrot_hold + yarn2(3상점). 3세트 자체 +1.19k(se .48)/+0.95k(se .16)/+1.01k(se .08), 96경기 합산 **+1.05k(se .17, 6se), 3악화/70개선**, 마진 ≈ +1.0k; **blind 7096–7111 +1.59k(se .46), 0/32 악화**, 전 버킷 양수(yarn +6.0k). 세트별 +1.5k 기준엔 미달이지만 "소기준 항목 묶음" 조항 + blind 확인으로 승격(소유자 거부 시 되돌림 가능: 스냅샷 base12 보존). 굽기 후 7096–99 비트동일 확인, `state/o_dev/p000_base13.py`, 라벨 base13_{sel,hold,fresh,blind4}, p_search BASE/DEFAULT_ON/앵커 갱신. base13 = 97.8k/93.3k/94.6k.
- 09-17 18:00 p000j(마진 목적) 중간: t0062 {land3 8·prw 8·straw 36·vrp_len 16·wheat_units 3} base13 대비 마진 +1.9/+1.5/+2.4k(96경기 +1.9k, 10se, 9악화), 자체 −0.3k, 승 4→8/96. 절제(sel 마진): **land3 8 단독 +1.47k(자체 −0.15k, 2악화/25개선)**, wheat_units 3 +0.59k, prw 8 무효(VRP 경로에서 미사용), straw 36 −0.4k, vrp_len 16 0. land3 8 3세트 마진 +1.47/+1.79/+2.15k(96경기 +1.81k, 9.4se, 8악화); +wheat_units 3: +2.02/+1.89/+2.51k(+2.14k, 10.4se). 서치 후반 PASS: t0118 hold 마진 +5.2k(se .57, 0악화)/자체 −0.6k {sheep_plus 2, straw_f .5, straw 38, buf 2, feed 5, land3 8, melons 10, herd_block off, wheat_units 3}. 도구 `o_tools/margin_pair.py` 추가.
- 09-17 18:28 **p000j(마진 목적, 200회) 종료**: 수렴 설정 {land3 8, wheat_units 3, herd_block off, straw_f 0.5, straw 38, sheep_plus 2, buf 1~2}(t0118/t0175: hold 마진 +5.2k, 자체 −0.6~−0.8k). base13 대비 재판정(96경기 마진/자체/승): C1 land3 8+wheat_units 3 **+2.14k/−0.09k/+6승**, C2 +hb0 +2.64k/−0.18k(11악화), C3 +straw_f .5·straw 38 +3.80k/−0.58k(hold −1.2k)/+6승, C5 +sheep_plus 2 +4.02k/−0.77k, C6 +buf 2 +4.20k/−0.83k/+7승, C4(=t0118) +4.35k/−1.06k. blind 7112–7127: C1 마진 +3.3k(자체 +1.2k, 승 4→4), C3 +4.2k(자체 −0.08k, 20악화, 승 4→6). vs V46(sel): C1 마진 +1.7k(승 6→6), C3 +2.6k(승 6→4). 마진 초과분은 승수로 전환되지 않고 자체 현금 분산만 키움 → **base14 = C1**(land3 8·wheat_units 3) 승격, 굽기 후 7112–19 비트동일, 스냅샷 `state/o_dev/p000_base14.py`, 라벨 base14_{sel,hold,fresh,blind5}. base14 = 97.9k/93.0k/94.5k, 평균 마진 −7.6/−13.7/−14.9k. 마진 우선 규칙을 AGENTS.md에 기록(소유자 미확인 표시).
- 09-17 18:55 base14 세계별 마진(64세계 좌석평균): 중앙값 −13.3k, 양수 6(7112 FARMERS×5 **+80.8k**, 7127 +16k, 7008 +13.6k, 7015 +7.8k, 7018 +1.8k, 7009 +0.4k), −5k 이내 16. 뒤집을 수 있는 대역 = PET_CAFE/PIZZA/BAKERY/BRUNCH/FARMERS 조합(힌지 작물이 우리 강점), 절망 대역 = ICE_CREAM/SMOOTHIE/YARN(−25k+, 테이프의 물량). 7033 장부: 토마토 +10.3k·당근 +4.8k vs 비료 −8.6k·우유 −6.4k(딸기·양털 시장은 둘 다 죽음: A 딸기 249개 $15). 비료 레버 재시험(마진 관점): no_wheat_fert 96경기 +0.8k(2.1se)지만 fresh 7042에서 자체 −12.5k/마진 −21k(카오스 분기) → 기각; fert_h0 +0.1k 무효; 둘 다 +1.0k(2.8se, 승 +5)이나 같은 7042 위험 → 보류.
- 09-17 18:55 밀 시비 창 제한(nwf_lo/nwf_d: 해당 기간 밀 age-2 시비 생략): 전 기간 d20 이전 생략은 sel/hold 마진 +1.3~1.9k·자체 +0.1~0.5k·승 +6/+2지만 fresh 7042에서 자체 −12.5k(d2 시비 1회 생략 → d2 멜론 구매 4→2 → 연쇄; 초반 현금 칼날 민감성) → **d9–19만 생략(nw920)**: 마진 +0.46/+0.77/+1.15k(96경기 **+0.79k, 6.3se**, 11악화), 자체 +0.06/+0.29/+0.29k, 승 +3, 7042 무사. 전 기간(d9~) 생략 +0.3k, d9–15 +0.6k. base15 묶음 성분.
- 09-17 19:20 **base15 승격(마진 우선)** = base14 + 밀 시비 d9–19 생략(nwf_lo 9/nwf_d 20) + 매도 버퍼 buf 1(우유·양털). 마진 +1.07/+1.26/+1.74k(96경기 +1.36k, 9.8se, 10악화), 자체 −0.07k, 승 +7; **blind 7128–7143 마진 +1.95k(se .34, 6악화), 자체 +0.2k**; V46 상대 마진 +1.3k(승 유지). 96+32경기 합산 마진 +1.50k. 기각: +herd_block off(23악화), buf 2(+1.21k), cap_m23 12, opp_f 1.3, fert_zero(7042 카오스), wsell(39악화), straw 38. 굽기 후 7128–35 비트동일, 스냅샷 `state/o_dev/p000_base15.py`, 라벨 base15_{sel,hold,fresh,blind6}. base15 = 97.8k/93.1k/94.4k, 마진 −6.5/−12.5/−13.2k, 승 7/2/5.
- 09-17 19:35 base16 탐색(base15 위, sel 마진): 축군 하한 herd_min 8/10/12(비료값 목적) **−2.6/−3.4/−4.6k**(자체 −2.4~−5.2k), 당근 FARMERS 반영 car_fm2 무효(펫카페 분기·타일 상한), 토마토 상한 32 무효(타일 상한), 4번째 땅(마진 관점) −4.4k(30악화; 상대 +1.4k). 7013 장부: 토마토 +19.3k에도 비료 −10.2k(A 17마리 vs 9마리)·딸기 −7k(단가 동일 $201, 물량 216 vs 249)·우유 −6.6k. p000k(base15 마진 서치 150회) 19:15 시작.
- 09-17 19:50 늦은 소 추가(late_cows 2/4, d13+) **−4.7/−10.2k**(자체) 기각; 수요 조건부 딸기 계수(straw_f_hi) 무효(4상점 확정 시점엔 파종 창 종료). d28 급식 추적: d28 h0 전량 매도(terminal)로 우유·양털 단가가 밀값 아래로 떨어져 `worth` 조건이 급식을 막음(h16 이후 회복되며 재개) → d28 급식률 81%(17마리면 12%)의 원인. term_d 29(d28 정상 매도)는 +0.2k로 seed_last 단독(+0.3k)보다 못해 보류; 자체 큰 레버는 아님.
- 09-17 19:57 딸기 수요 조건부 늦파종(straw_last_hi 18: 딸기 상점 수요 ≥24/일이면 d18까지 하루 4주): 마진 +0.14/+0.38/+0.40k(96경기 +0.31k, 3.4se, 3악화), 자체 +0.18/+0.47/+0.42k → base16 묶음 성분(d20까지는 −0.1k). p000k(base15 마진 서치) 77/150: 최고 herd_block off +0.9k(6악화)뿐 → 마진 노브 공간도 소진.
- 09-17 20:20 rush_44((4,4)에 멜론, 5번째 동물은 한 칸 밖): **−3.2k 자체/−6.3k 마진(31악화)** — 원인은 러시가 아니라 d6 양털 매도 시각 변화(h8/h15 → h15~20) → d6 저녁에 땅+소2+거위2+딸기11을 한꺼번에 사서 d7–8 공백(base는 d6 딸기 → d7 땅 → d8 동물로 분산). arm 판과 같은 실패 모드: **d6 구매 순서가 우연한 타일 여유·매도 시각에 좌우되는 칼날 구조**. herd_block off +slh18 묶음 96경기 +0.8k(3.5se)지만 21악화 → 기각.
- 09-17 20:25 **p000k(base15 마진 서치 150회) 종료: 통과 없음**(t0100 hold +1.6k se .76 12악화). land_cool(땅 산 날 축군 구매 금지)·d6_geese(2번째 땅 전엔 거위만) 단독 0/−0.4k, rush_44/arm과 조합해도 회복 안 됨 → 링 멜론 배치는 보류 확정. **오늘 총합 확인(신규 시드 7144–7175, 64경기, base11 → base15)**: 자체 **+3.35k(se .47, 9악화)**, 상대 −5.64k, 마진 **+8.99k(se .54, 0악화/63개선)**, 승 0 → 6/64.
- 09-17 20:35 land2=7(2번째 땅을 d7로 고정) 단독 −1.6k(28악화) → base의 "d6 여유 생기면 즉시 땅" 타이밍이 맞음; rush_44/arm과 조합도 −2.7/−1.6k. 링 멜론 계열 종결. 전 신규 노브 기본값에서 base15와 blind 7128–7143 32경기 비트동일 재확인.
- 09-17 22:40 **Macro Oracle 하네스**(`o_tools/oracle.py`, `o_tools/oracle_report.py`): 플래너에 날짜 게이트 노브(`@D:knob=v`), 분기 옵션 노브(plus_cow/sheep/goose, straw_plus, car_plus, save_day, herd_stop, null_days=D:h[:w]) 추가(기본값 무변화, base15 비트동일 확인). d6/9/12/15/18에서 전략 5가지 vs 동일 개수 null 교란 5가지를 최종 마진 기준 탐욕 선택, 양 좌석 일별 현금·단계 상태특징 기록. 7000 좌석1 예비: 전략 오라클 +2.3k(STRAW+8 d6) vs null 오라클 +2.6k → 이 세계에선 카오스 수확이 전부; SHEEP+2 d6 −13.5k·SAVE −7.8k·LAND4 −8.8k. sel 32경기 본실행 22:38 시작(약 35분).
- 09-17 22:50 급식 가치 규칙 조기 적용(worth_d 24/22/20: 제품가<사료가면 급식 중단): 자체 +0.25~0.58k지만 **마진 −0.6~−1.1k**(우리가 늦게 우유·양털을 덤핑하지 않으면 상대 말기 단가 회복) → 기각. 7000 말기 가격: d26–28 우유 $1~45·양털 $1~5(양쪽 과잉공급), 밀 $48 — 말기 축군은 사료비 이상 못 벌지만 마진상 덤핑이 유리.
- 09-17 23:05 **Oracle 1라운드 결과(sel 32경기, base15)**: 완전정보 오라클 마진 +2.82k(se .47, 자체 +0.27k) vs **동일 개수 null 오라클 +2.23k(se .27, 자체 +1.29k)** → 순수 전략 상한 **+0.59k(se .56, 유의하지 않음)**. 전략−null ≥3k 세계 8/32, ≥5k 6/32(7005·7006·7013·7014: 딸기 상점 많은 세계의 d6 STRAW+8 +3~6k). **1일/2일 lookahead selector 회수율 −4.1/−5.8(음수: 단기 현금으로 고르면 KEEP보다 나쁜 가지를 고름, 65노드 중 정답 17/9)**. 선택 빈도: d6 STRAW+8 10·GOOSE+2 7·SHEEP+2 6, d9~18 대부분 KEEP(d12 TOM+4 8, d15 HERDSTOP 7, d18 TOM_D20 7). 판정: (a) 작고 (b) 회수 불가 → **p001 Macro-MPC 불채택**. d6 STRAW+8을 조건부 규칙(딸기 상점 선행·피자 없음, sc_plus 8/12, min_berry 2)으로 옮겨 3세트 판정: 96경기 마진 +0.0~+0.3k(se .3~.4), fresh 음수 → 일반화 안 됨(세계 특이/카오스).
- 09-17 23:17 Oracle 2라운드(감축/시점 옵션: STRAW−8·HERDSTOP·NOSTRAW·LAND3없음·FEEDCUT·TOM0·CAR0·SEED24·NOWFERT): 전략 오라클 +2.03k vs null +2.23k → **전략−null −0.2k(se .28)**, ≥3k 세계 0. 평균 델타 전부 음수(HERDSTOP d6 −32.5k, TOM0 −5.5k, LAND3없음 −10.8k, FEEDCUT −1.9~−3.5k). 결론: d6–18의 거시 분기(증감·시점)에는 base15 고정 일정 대비 활용 가능한 여유가 없음(카오스 수확만) → p001 Macro-MPC·분기형 라우터 모두 불채택. 상태특징 일관성도 낮음(d6 선택 버킷 내 최빈 33~50%). 남은 미탐색 구간 = **개막 d0–d12 번들** → 개막 노브(cows0·sheep0·melons0·w0seed·w0feed·d0_res·melons_late·straw_early·cows5·straw_d6/d79/d1012·land3) 추가(기본값 base15 비트동일), `o_tools/open_search.py`(마진 목적 TPE 150회, base15 라벨) 23:18 시작.
- 09-18 00:12 **open1(개막 번들 서치, 마진 목적, 150회) 종료**: 단일 편차 앵커는 전부 ≈0; 조합 t0100 {d0_res 5, land3 9, melons0 8, w0feed 3, w0seed 6} sel +1.54k·hold +1.55k PASS. 절제: melons0 8+d0_res 5만 −1.7k, +w0feed 3 +1.0k, land3 9 단독 +0.2k, w0seed 무관, melons0 7=8(8번째는 현금상 미구매 → 실효 d0 멜론 7). 3세트 마진 **+1.54/+1.55/+1.60k(96경기 +1.56k, 8se, 9악화)**, 자체 −0.47/−0.60/−1.18k, 승 +3. **blind 7176–7191(첫 사용) 마진 +2.50k(se .35, 2악화), 자체 −1.12k, 승 0→2.** w0feed 4 변형은 sel +1.5k/자체 +0.2k였으나 hold/fresh 0 → 기각. → **base16 승격(마진 우선; 자체 평균 −0.8k는 −1k 경계 부근, 기록)**. 굽기 후 7176–83 비트동일, 스냅샷 `state/o_dev/p000_base16.py`, 라벨 base16_{sel,hold,fresh,blind7}. 다음 blind 블록 7192–7207.
- 09-18 00:40 base16 위 재시험(sel 마진): 링 멜론 배치 rush_arm **−11.8k**·rush_ring −9.2k(새 개막에선 치명적), rush_44 −1.9k, herd_hold 0/1 −0.8/−0.2k → 창고 주변 배치는 현행 유지 확정. p000l(base16 기준 전 노브 마진 서치 150회) 시작.
- 09-18 01:00 base16 위 조건부/구조 시험(sel 마진): 깊은 우유시장 축군 계수 rf_deep .6/.8 −0.7/−0.6k, 깊은 딸기시장 계수 sf_deep .6 sel +0.5k → hold −0.1k(자체 −1.1k)/fresh +0.5k(96경기 +0.3k, 1.2se) 기각; 토마토 조기(d10) 무효·상한 40 −0.3k(주당 최대 4단위라 타일 외 확장 없음, 창고 상한). base16 4세계 장부: d27 현금 동률(+11), 최종 −3.5k는 d28–29에서 발생(A 밀 8.0k vs 4.8k, 사료 매수 차). 남은 항목: 비료 −3.9k·밀(순) −6.9k·우유 −3.2k·멜론 −2.9k / 토마토 +6.7k·달걀 +3.1k.
- 09-18 01:35 **p000l(base16 마진 서치 150회) 종료: 통과 없음** — 상위 후보는 또 과잉공급 영역(straw_f .5·sheep_plus 2·melons 14·opp_f .7), hold 마진 +0.9~1.7k(se .65)지만 **승 2→0**, 자체 −1k. 마진 목적은 승수로 전환되지 않는 후보를 고르므로 목적함수를 **softwin = 10000·tanh(마진/4k)**(승선 근처 경기만 가중)로 바꿔 p000m 시작(base16, 150회). 말기 전량 수확(term_harv d29/28) −0.3/−0.5k 기각.
- 09-18 02:00 2차 딸기 사이클(d19–21 또는 d17–19 재파종 8/16주): **−1.7~−3.5k**(d19 파종은 생산 1회뿐; 말기 시장 포화·밀 사이클 대체 손실). 당근 시점 후퇴도 기각. A의 말기 딸기 우위는 d11–14의 2차 대량 파종(13주)에서 옴 → 우리 cap(room) 내에서는 재현 불가.
- 09-18 02:40 **p000m(softwin 목적, base16) 종료: 통과 없음**(최고 t0094 sel +1.36k → hold −0.5k). base16 위 세 목적함수(자체·마진·softwin) 서치 모두 소진. open2(개막 공간 확대: melons0 5–10, w0feed 2/3/5, d0_res 0/5/25, melons_late 8–12, straw_early 4–16, straw_d1012 0/3/5, land3 8–10, land2 6/7; softwin 목적, 150회) 시작.
- 09-18 02:55 노동 분류(7000, d10–26 일평균): 플래너 행동 128·이동 111(작업행 102/69회 1.47칸, 창고행 8)·PASS 35 vs 테이프 행동 142·이동 108(1.56칸)·PASS 10. 경로 효율은 동급; 차이는 우리 h18–23 유휴 35스텝(할 일 소진). 타일·시장·작업 모두 포화 → 실행 계층에서도 남은 여유 없음. A의 우위는 같은 타일에서의 밀 사이클 수율(3.7 vs 2.7단위/파종; 우리는 마진용 wheat_units 3·d9–19 무시비 선택의 대가).
- 09-18 03:05 open2는 앵커 값(w0feed 8)이 확대 공간 밖이라 7회에서 크래시 → 앵커 수정(land2 6 포함) 후 03:03 재시작(t0000 = base16 비트동일 +0 확인).
- 09-18 04:05 **open2(확대 개막 공간, softwin) 종료: 통과 없음**(최고 t0088 sel +1.0k → hold −0.25k). 개막 번들도 base16에서 소진. 오라클을 hold 세트에서 재실행(독립 세계에서 무여유 판정 확인)하고, 이후 sel+hold 64경기 목적의 합동 서치를 밤새 돌림.
- 09-18 04:50 **base17 승격(오라클 유래 조건부 규칙)**: 알려진 상점에 딸기 상점이 있고 피자·얀 상점이 없고 스무디 ≤1이면 딸기 상한 +8(sc_plus 8). 3세트 마진 +0.70/+1.33/+1.29k(96경기 +1.11k, 4.5se, 7악화, 54경기 비트동일), 자체 +0.13/−0.37/+0.07k, 승 +5; **blind 7192–7207(첫 사용) 마진 +1.18k(se .43, 2악화)**, 자체 −0.4k. 강도 +6/+12·얀 허용 변형은 열등. 굽기 후 7192–99 비트동일, 스냅샷 `state/o_dev/p000_base17.py`, 라벨 base17_{sel,hold,fresh,blind8}. 다음 blind 7208–7223. hold 오라클(base16): 완전정보 +4.6k vs null +1.4k → 순수 +3.1k(4.4se), 대부분 d6 STRAW+8 → 이 규칙의 근거. 소유자 지시: 보고 없이 계속, **CPU 전부 사용(단독 실행은 16워커)**.
- 09-18 05:15 검증 시간 단축 작업(소유자 지시: 오라클 종료 후 CPU 빈 상태에서 측정): (1) 경기 결과 캐시(`proxy_eval.py`: 키 = 양 에이전트 파일 sha + PROXY_KNOBS/FLAGS + 엔진 파일 sha + 고정 상점열 + seed + seat, `o_results/proxy/cache/`), (2) `--seats` 옵션 + p_search 2단계 스크린(P_SCREEN=1: 좌석0 16경기 → 임계값 통과 시 좌석1 추가; 과거 826 트라이얼에서 좌석0-only vs 양좌석 paired delta Spearman **0.994**, 시드 8개 부분집합은 0.895 → 좌석 분할이 더 좋은 게이트; 임계 −1000(softwin −2000)에서 양성(≥+800) 손실 3%), (3) `o_tools/fastgame.py`: env.run의 스텝별 전체 상태 deepcopy(__get_shared_state, 부하 중 프로파일에서 경기 36.5s 중 15.5s)를 우회하는 직접 호출 루프 + 비트동일 검사 스크립트 `fastgame_check.py`. 승격 기준(3세트+새 blind+양좌석)은 그대로.
- 09-18 05:45 **검증 6배 가속(비트동일 검증 완료)**: (1) `o_tools/fastgame.py` 직접 루프(스텝별 상태 deepcopy·schema·structify 우회, 상대/우리 에이전트에 공유 필드 참조 뷰 전달): 경기 5.1s → 1.9s(7000·7013·7029 양좌석 보상·일별 현금 동일); (2) VRP 핫루프 정확 최적화(삽입 시 (over, add, cost) 하한 가지치기·거리 인라인·need 선행 검사 증분): 경기 1.9 → 1.7s, sel/hold 64경기 base17과 비트동일; (3) 경기 결과 캐시 + `--seats` + p_search 2단계 스크린(좌석0 16경기 → 임계 통과 시 좌석1). 유휴 CPU 벤치: 32경기 세트 8워커 13s·12워커 11s·16워커 11s → 12워커(단독 16 동률) → 최적화 후 **32경기 8s**(이전 ~50s). 프로파일(3회 중앙값 1.73s/경기): 플래너 1.06s(leg_cost 76만 호출)·테이프 0.48s·엔진 0.2s. oracle.py도 fast 루프로 전환(체인 2.3분 → 0.7분).
- 09-18 05:40 **세계 프로파일 라우터 도구**: 플래너에 버킷 게이트 노브(`#milk1:room_f=0.5` — 첫 3상점 확정 시점부터 해당 버킷에서만 적용; `world_bucket` = proxy_eval.bucket과 동일), proxy_eval `--seed-list`, `o_tools/build_pool.py`(튜닝 풀 = 7000–7047 + 신규 7300–7331, 홀드 7332–7363; base17 풀 라벨), `o_tools/bucket_search.py`(버킷별 TPE, softwin paired, 20회마다 버킷 홀드 확인). 풀 버킷 크기: tune milk0 17·milk1 23·milk2 18·milk3 7·yarn 15 / hold 7·8·7·3·7 시드. **신규 64시드(7300–63) base17: 마진 −9.85k, 승 14/128(11%)**. p000n(base17 합동 softwin 서치, 스크린 적용) 진행 중.
- 09-18 06:05 **p000n(base17 합동 공간·softwin·좌석0 스크린, 200회) 종료: 통과 없음**(최고 +0.67k softwin, 유의하지 않음). base17에서 전역 노브 서치는 소진. 오라클 3라운드(시장 타이밍 옵션, base17, sel+hold 64경기): 완전정보 +2.5k vs null +1.8k → 순수 +0.7k(2.3se); 힌트(nwf_d 15/16/18, carrot2 off, opp_f 0.7) 3세트 검증 모두 0. → **버킷별 프로파일 서치 5종 순차 실행 시작**(milk1→yarn→milk0→milk2→milk3, 각 80회, 16워커).
- 09-18 07:00 **버킷별 프로파일 서치 결과(base17_pool, softwin, 80회×5)**: milk1 +0.19k·milk2 +0.05k·milk3 +0.09k(무), yarn +1.1k은 room_f 0.6 과잉공급(자체 −6~−12k, 마진 음수) → 불가, milk0 `egg2=5`(거위 5)는 tune +0.8k/hold +1.0k(마진 +0.55k, 자체 +0.6k, 승 +2/28)였으나 3세트 검증 96경기 마진 +37(0.4se)·fresh 음수 → 일반화 안 됨(egg1 3 포함 변형 −0.24k). **세계 프로파일 라우터(노브 프로파일)는 base17 위에서 여유 없음** — 오라클 결론과 일치. 토마토 축소(tom_per 6/4, tom_max 16, tom_min 3) −0.2~−0.8k → 현행 토마토 배분 유지.
- 09-18 07:30 Majkel 289경기 개막 재추출(리플레이 아카이브): d0 COW2 SHE3 MEL6 + 밀 8.7(상품)+11(씨) + HIRE4 + 밀 5.7 매도(라운드트립), d1 MEL4.9, d2 MEL2 STR5, d3 STR4.4, d4 STR2, d5 STR0.5(누적 딸기 12), **d6 COW3.4 GOO1.6 SHE1.1 STR10 LAND1 + 양털 18 매도(≈4.6k 지출)**, d7 STR4, d8 밀 36 매수·우유 12 매도, d9 COW1.9 LAND(3번째). 인부 수 일별 4,4,6,6,6,6,8,9,9,10 = 우리 HANDS_BY_DAY와 동일. 일말 현금 d0–12: 6,45,22,76,345,749,210,251,1955,872,6600,8609,12694. 우리(base17, 7000) d6: h8 땅+딸기3, h9 딸기8+거위1, h11 소2 → 땅·소 시점은 이미 Majkel과 같고 차이는 d6 동물 2.5마리(현금 +$800: d0–5 밀 매수 15 vs 20단위·딸기 12 vs 8·비료 5 vs 4.5/일)뿐. 나머지 +30k는 중후반 실행(밀 시비 55회·0% 유휴·비료 $68·d21 이후 축군 방출)에서 나옴. null 오라클 분석: 농부의 d9–18 h0–4 한 스텝 지연이 평균 마진 −0.5~−1.4k(상대 +0.3~0.7k) — 아침 첫 시간대 계획이 극도로 민감; h0 농부 수확 우선(h0_harv) 시험은 −0.2k.
- 09-18 07:20 4번째 땅 재시험(밀 파종 상한으로 노동 과부하 방지, d12): wheat_day_cap 3/6 → **−7.1/−5.4k**(자체 −5.5/−3.9k); 상한 단독 −1.7k(빈 타일 전부 밀 파종이 옳음). 땅4 실패는 노동이 아니라 d12 현금 4000의 기회비용(축군·씨앗)과 SE 거리. 종결.
- 09-18 07:55 **p000o(base17, 합동 공간, softwin, 64경기 선택·fresh 홀드아웃, 200회) 종료: 통과 없음**(최고 +0.33k). Majkel 아카이브 중반 배분(예: d15 동물 19·밀 29·딸기 15·토마토 9; 일 행동 PASS 2·이동 120·급수 54·수확 22·급식 14·케어 14·수거 15·시비 8·파종 11)을 흉내낸 패키지(straw 26/30 + 밀 시비 상시 + wheat_units 4 ± d10–12 딸기 중단): **−1.4~−3.6k**(69~84/96 악화) → 우리 실행기·시장 모델에서는 딸기 35타일이 옳고 Majkel식 배분은 역효과. base17 라인의 탐색 종료 판단; 남은 것은 아키텍처 변경.
- 09-18 08:15 근접 패배 세계 장부(7007 FARME·BRUNC×3·FARME·BAKER): 테이프가 밀을 **1497개 매수·1810개 매도**(하루 300~350개 왕복; 매수 $43.6·매도 $44.8 → 스프레드 +$1.8k) — 소비 36/일인 밀 적자 시장의 일중 가격 상승을 이용한 회전. 총수입 −65k로 보이지만 순현금 차이는 −0.7k(우리 딸기 +7.9k·토마토 +11k·달걀 +4.1k vs 비료 −10.4k·밀 순 −13k). 밀 순생산 A 613 vs 우리 334(딸기 35·토마토 24 타일 대신). 밀 회전 자체는 세계당 +1~2k 수준의 추가 수입원(비제로섬)이나 창고 100칸·현금 점유 필요 → 후속 후보로 기록.
- 09-18 08:43 **p000p(base17, 합동, softwin, 64경기, 400회) 종료: 통과 없음**(최고 +0.1k). base17 위 모든 자동 서치 소진 확인. 현재 파일 = base17(7192–7207 32경기 비트동일 재확인, 스냅샷 갱신).
- 09-18 09:15 **Economic Controller v2(작물 배분만, sw_ec2) 1차 반증 완료 — 구조적 신호 없음.** 정확한 시장식(price_at)+코호트 공급 스케줄+상대 공급 prior(d16~ 0.75×수요)+타일 예산(당근 로테이션 예약)+한계수입(자기 물량의 가격 영향 포함) 순으로 모델 결함을 고쳐가며 sel 스크린: v1 −7.9k → v2 −2.7k → v4(MR) −1.1k → v5(토마토 7.3u/타일) −0.6k → **v6 자체 +0.8k/마진 +0.4k(se 0.8, 승 12→11)** → v7(상대 물량까지 마진 가치화) 자체 −0.6k/마진 +0.1k. 세계별로 딥 베리(7000/7006/7007) +5~8k가 매번 나오지만 나머지 13세계 −1~4k(7013 마진 −6.5k: 우리 물량이 줄면 테이프 토마토 60→80·딸기 +$23). 원인: 자기수입 최적 배분 ≈ base17 고정 상한(이미 마진 최적 근방), 잔차는 상대 물량·매도 타이밍(숨은 상태) 예측 오차. 배운 사실: 딸기 시장은 대부분 d22~ 포화(재고>10000 → $1~60), d12 이후 딸기는 밀보다 못함(딥 시장 제외); 토마토 실현 7.3u/타일, d26 적자 200~360($85~225); MR 없이 가격만 쓰면 S 46까지 과잉. 코드는 sw_ec2 off 시 base17 비트동일(스위치 기본 off, 컨트롤러는 ec2_targets에 보존). 다음: 리더(Majkel) 아카이브 세계를 그대로 핀 고정해 우리 플래너와 **수량 기준 격차 분해**(상품별·5일창 매도량, 축군/타일/시비/일손 궤적) → 모방 목표 컨트롤러의 목표 상태 결정.
- 09-18 09:38 **리더 격차 분해 도구 `o_tools/leader_gap.py`**(Majkel 289경기 세계를 상점 순서 그대로 핀 고정, base17 vs o227 양좌석 578경기, 수량 비교) → `o_results/leader_gap/Majkel1337_base17.{json,txt}`. 결과(그의 세계에서 우리 96.1k vs 그 110.2k, −14.1k; 현금 격차는 d12 0 → d18 −8.7k → d29 −14.1k): **밀 434 vs 255개 매도(−180)**, 밀 파종 187 vs 133/게임, 수확 3.50 vs 3.22u, 수확 즉시 재파종 100% vs 87%(1~3일 공백 12개), **일말 빈 타일 2~3 vs 4~8(d9 8 vs 21, d27 5 vs 26)**, 밀 타일 d18~27 18~33 vs 12~20; 당근 수확 2.59 vs **2.00u**(age3 급수 전에 수확), 토마토 2.23 vs 1.88u; 젖소 d9 7.8 vs 5.0(전 기간 +1.6), 멜론 12 vs 10; 시비 156 vs 96, 급수 1360 vs 839, **PASS 72 vs 1508**(우리 유휴 ≈1,400스텝/게임). 딸기 타일·단위는 비슷(가격차는 상대 차이). 결론: 격차는 작물 배분(EC2)이 아니라 **실행 처리량**(밀 엔진 회전·빈 타일·급수 적중·당근 급수 순서·후반 파종 지속). 다음: 수량 목표(빈 타일 ≤3/일, 밀 500u+, 당근 2.6u/수확)를 기준으로 실행 계층을 고친다 — 1) 당근 age3 급수 후 수확, 2) 밀 씨앗 선매수(당일 수확 예정 타일만큼)로 즉시 재파종, 3) d27까지 파종 + 마지막 날 2u 수확, 4) d9 새 분면 즉시 파종.
- 09-18 09:47 **base18 승격 = base17 + car_wf**(당근도 마지막 창 날(age3) 급수 후 수확 — 한 줄 실행 수정; 격차 분해의 "당근 2.0 vs 2.59u" 항목). 3세트 자체 +0.8/+1.5/+1.5k, 마진 +0.8/+1.7/+1.9k(풀 96경기 +1.46k, 8.1 se, 7/96 악화), 승 12→12/4→8/6→8; **블라인드 7208–7223(b9, 1회) 마진 +2.2k(se 0.3)/자체 +1.9k, 1/32 악화**, 승 4→4. 당근 수확 2.0→2.83u(리더 2.57 초과). 스냅샷 state/o_dev/p000_base18.py, 라벨 base18_sel/hold/fresh/blind9. 같이 시험해 기각: seed_ahead(당일 수확 타일 씨앗 선매수: 빈 타일 5.8→3.5로 줄지만 마진 +0.16k, 31/96 악화), d27 파종+마지막날 2u 수확(+0.03k), 당근 로테이션 축소 car_pet4/car_plus−2(+0.0k). 토마토 생산일 시비율은 이미 71~91%(누락은 age7 첫 생산일·d25+ 비료 고갈) — 소폭.
- 09-18 09:58 **base19 승격 = base18 + vrp_h23**(VRP 시간 예산 off-by-one 수정). 발견 경로: 격차 분해의 "빈 타일·PASS 1,500" → 작물 조기 고사 집계(64경기: h22 파종 밀 12.5·당근 3·멜론 0.9·딸기 0.7/게임이 당일 미급수로 고사; 당근 age4 미수확 2.6) → 시간대별 행동 집계(h23 유닛행동 299 중 PASS 292). 원인: dispatch_vrp의 `left = 23 - hour`(엔진은 h23 행동 후 일말 처리 → h23은 유효 스텝) → 매일 전 인원 h23 유휴 + h22 파종 미급수 고사. 수정: `left = 24 - hour` + h23 파종 금지(당일 급수 불가). 첫 시도(h23 파종 허용)는 자체 +1.7k/마진 +0.6k(h23 파종 16개/게임이 대신 고사, 멜론 12→13씨앗 부작용) → 파종 금지 후 **자체 +2.0/+2.4/+2.0k, 마진 +2.6/+2.8/+1.9k(풀 +2.46k, 11.3 se, 9/96 악화), 승 12→14/8→12/8→10; 블라인드 7224–7239(b10) 마진 +2.1k/자체 +2.2k, 4/32 악화, 승 8→11**. 스냅샷 state/o_dev/p000_base19.py, 라벨 base19_sel/hold/fresh/blind10. 다음 블라인드 7240–7255.
- 09-18 10:30 base19 위 재스크린: EC2 v6/v7(sw_ec2) 3세트 풀 마진 −0.8k/−0.2k(hold −2.4k) → 확정 기각(코드 보존, off). 개막 재서치 open3(base19, margin, wide, 80회): 최고 sel +1.2k가 hold −0.3k → 통과 없음(개막 공간 평탄 재확인). 4번째 땅 d12/14/16 −2.3~−3.9k(25타일이 15일간 +57밀뿐 = 타일이 아니라 노동/물류가 병목). 축군 +1(plus_cow/plus_sheep 노브는 매일 +1 누적 → 5마리 증가하는 결함 있는 시험이었음; room_f 0.5 −2.2k, rf_deep 0.6 +0.2k, herd_min 12 −4.3k). 거위 +1/+2 자체 +0.5k·마진 −0.2/−1.5k. wsell/wsell_d8/harv_pr0 0. **7020 진단**: 딸기 상한은 `market_room`이 '오늘 흡수량' 기준이라 사실상 8(+sc_plus 8)로 고정 — 테이프 40타일(231u, +12.4k) 대비 17타일; 그러나 EC2가 더 심으면 지므로(공유 시장 붕괴) 테이프의 선점 물량이 구조적 우위.
- 09-18 10:46 실행 처리량 후속(base19 위, 모두 sel 스크린): 일손 10명 자체 +0.05k/마진 −1.1k, 9명 −3.4k, 12명 −0.9k, 13명(d10~) −4.2k → 11번째 일손의 한계생산 ≈ 비용($89/일), 노동은 여유가 아니라 아침 피크가 병목. 4번째 땅(d12/14/16) −2.3~−3.9k: 25타일이 밀 +70u만 생산(새 분면 절반이 빈 채, 일말 잔여 작업 17~50개 vs 기본 0~7) — 일손 13명을 붙여도 동일(−4.1k). VRP 캡: vrp_len 20 +0.4k, vrp_bal 2.0 −3.4k, vrp_min 10 −3.9k(균형 캡이 핵심). **작업 공급 감사(task_audit.py)**: 하루 작업 90~135개, h20에 5~35개·h23에 1~27개 잔여 → 기본은 용량 ≈ 공급. 수확→같은 타일 재파종 연쇄(sw_replant, seed_ahead 동반): 빈 타일 d15–18 2.8~2.9(리더 2.2~2.8 수준)로 줄지만 +0.4k(n.s.) — 빈 타일 항목의 가치는 +0.2~0.5k뿐. 밀 파종 125 vs 183의 잔차는 리더의 age2 수확(33%, 회전수만 늘림)과 당근/토마토 타일 배분(d18 당근 10 vs 3)이며 배분 노브는 평탄. 결론: base19 실행 계층은 리더 수준에 근접(빈 타일·고사·h23), 남은 격차는 공유 시장 물량(테이프 선점)과 세계별 쌍봉 구조.
- 09-18 11:00 base19 폭넓은 확인: vs V46(public) sel 마진 +0.3k·승 14/32(base12 −11.3k·4/32), vs K0006 −1.6k·14/32; **비편향 64세계(7300–7363, 128경기): base17 −9.85k·승 14/128 → base19 −6.2k(se 0.7)·승 25/128(20%)**, 중앙값 −8.0k. env.run 경로와 fast 루프 비트동일 재확인. 추가 스크린(sel): 토마토 age6 시비(sw_tom_f6) +0.1k, h0 고용 우선(sw_hire0: 10주문 상한이 고용 1~2명을 h1로 밀어냄) 자체 +0.66/+0.44/+0.40k·마진 +0.2k, 소형 실행 번들(hire0+seed_ahead+replant+tom_f6) 자체 +1.3/+0.6/+0.8k·마진 +0.9/−0.3/+0.6k(풀 +0.4k) → 마진 기준 미달, 스위치 보존(off). 테이프식 d0 멜론 12개(sheep0 2): 러시가 12개를 못 처리(d10 29u만 매도, 나머지 d11 $189→78)하고 양 1마리 감소로 상대 +8k → −9.5k. 후반 토마토/당근 매도 d27/28: 자체 +0.2~0.4k·마진 0. 조기 가축(anim3/cow5) −1.1~−2.7k.
- 09-18 11:12 상대 폭 확인: base19 vs public v37 +2.0k(16/32), vs v27 kaito +29k(32/32), vs o219 −0.9k(14/32); 같은 세계에서 **o227 vs v37 +53k(32/32)**, o227 vs V46 +0.9k(12/32). 원인 추적: v37과 o227은 동일 계보(스텝별 주문이 동일)라 거울 경기가 되고, 스텝0 밀 왕복(13+30 매수/30 매도 vs 13+10/30)에서 v37이 −$45, 스텝1 동시 매도까지 겹쳐 d1 현금 12 → 일손 0 → 젖소 굶어 d2 이탈 → 98k 붕괴(칼날 현금 연쇄). 플래너에 스텝0 왕복만 이식(sw_t0war: 13+10 매수/20 매도, 사료 3 보유): vs v37 +2.0→+5.1k(v37 붕괴 안 함, 스텝1 동시 매도까지는 재현 불가), vs o227 3세트 마진 −0.8k(d0 현금 ±$50에 개막이 흔들림) → off 유지. 결론: 포크 붕괴는 테이프 계보의 거울 미세구조 효과이며 플래너의 레이팅(상위 클러스터 50%)과 무관.
- 09-18 11:18 잔여 탐침(base19, sel): fert_h0(h0 비료 잉여 일괄 매도) 자체 +0.76k·마진 +0.74k(sel) → 3세트 풀 +0.41k(3.1 se, hold 0, 승 −4) 미승격; fert_h23/fert_batch ±0; 후반 딸기 파종 노브(straw_late_n/straw_last)는 도달 불가 코드(효과 0), straw_d1012 0 −0.6k; 가축 구매→배치 지연 12%(h16+ 구매분, ≈1.8마리/게임, ~$0.3k) 무시; d0 멜론 12 + 젖소 1: 러시가 h6–h14에 걸쳐 72u(평균 $190 vs 기본 $167)로 +1.1k지만 젖소 1마리 감소로 상대 +8.8k. 현재 파일 = base19 스냅샷(신규 스위치 off, sel 비트동일 재확인).
- 09-18 11:22 **Majkel 상대 환경 정량화**: 아카이브 상대(ymg_aq 78·SpaTaro 56·feel the agi 32·Mother-Goose 30·Otter 20·M&M&P&Q 16…)의 딸기 200~245u·우유 150~218u·양털 125~175u = o227(246/207/165)과 동급 물량. 그럼에도 Majkel 110k(마진 +2~+10k, M&M&P&Q에게만 −4.6k) vs 우리 100k. 그의 단가가 높음(딸기 $172 vs 우리 $147, 양털 $159 vs $138)은 상대 차이가 아니라 **매도 시점**: 그는 w3 84·w4 53·w5 64(글럿 창 d20–24 회피, 후반 회복 시장에 매도), 우리는 67·89·26(글럿 창에 집중). 페이싱 규칙(sw_pace: 소시장 재고 ≥10000이면 보류, 27일 전·재고 <60): **자체 +1.8k(sel)이지만 o227 +4.6k → 마진 −2.7k(26/32 악화)** — 덤핑 상대에겐 보류가 시장을 넘겨줌(price_hold 기각과 동일 구조). 코호트 시점 이동(d10–12 파종을 d6–9로)은 개막 서치 공간이었고 통과 없음. 결론: 라이브 상대가 덤퍼면 페이싱 불리, 페이서면 유리 — 상대 유형 감지(딸기 재고 ≥10000 시점의 상대 매도율)가 있어야 조건부로 쓸 수 있음(미구현).
- 09-18 11:28 **상대 유형 데이터**(라이브 371경기 + 아카이브 289): 소시장 재고 ≥10000 상태에서의 매도 비중 — 우리 테이프 ~50%(딸기 355/373), Majkel 15%(174/31), M&M&P&Q 4%, ymg_aq 37%, SpaTaro/feel the agi 23%, Otter 15%. 상위 클러스터는 페이싱, 우리는 글럿. 페이서 상대 모델 `state/o_dev/p000_pacer.py`(base19+pace 기본 on)로 검증: **base19(글럿) vs 페이서 106.1k vs 105.0k, 마진 +1.0k, 승 23/32**; 페이스 vs 페이서 108.5k 동률(거울). 즉 페이싱은 양쪽 현금을 올리지만 정면 승부에선 덤핑이 이김(선착) → 마진 우선 규칙과 일치, 현행 매도 정책 유지. 페이서 상대 기준 우리 106k vs Majkel 110k(같은 상대급) → 실제 격차 ≈4k(수량: 밀·초기 축군).
- 09-18 11:29 기각 후보를 페이서 상대(base19p 라벨)로 재스크린(sel): EC2 −0.2k, rf_deep −0.2k, land4@14 +0.1k(o227 상대 −3.7k였으나 페이서 상대도 이득 없음), 실행 번들 +0.8k(se 0.8), fert_h0 0, sheep_plus 2 −0.1k → 기각은 o227 특이성이 아님. 상태: base19 확정, 신규 스위치 전부 off, 스냅샷 동기.
- 09-18 12:18 **Majkel d0–9 인과 분해**(도구 `o_tools/cash_trace.py`: 리플레이 시간별 현금·주문 vs 우리, `--agg 60` 집계; `o_tools/cash_shadow.py`: 시점별 +$X 주입 → 최종 자체/마진 델타). 최초 차이 3개: (1) d0 밀 씨앗 11 vs 4(멜론 6 vs 7, ≈$70 스왑) → 그의 밀 9타일이 d2–6 사료를 자급(d1–5 사료 지출 $405 vs 우리 $636, 밀 매도 +$122) → d5 현금 758 vs 478; (2) 그 현금으로 d2–3 딸기 9.5 vs 6; (3) d6 가축 6.1+딸기 9.7 vs 3.6+6.9, 당일 배치 98% vs 63%(우리 구매→배치 지연 평균 9.8스텝, 다음날 21%; h16+ 구매 65~95% 다음날). **현금 그림자 가치(+$100, sel 32경기)**: d0–1 ≈0/음(−0.1~−0.3k: 한계 달러가 사료 재고로 감), **d2–4 ×6~8(d3 +$781, 17/0 세계 개선)**, d5–8 ×3~5, **d9 ×9**, d10 ×1.8, d12+ ×1.0; 일중 시각은 무관(d3 h2=h20). 즉 병목은 d2–4·d9 현금이고 Majkel의 사료 자급($350)이 그 창에 정확히 들어감(≈+1.7~2.5k 상당).
- 09-18 12:20 최소 counterfactual(모두 sel, 마진): 밀 씨앗 9~11개(멜론 6/사료 0~1/딸기 4/nwf_lo 0 조합) 자체 −1.0~+1.0k·마진 −0.7~−3.2k(NW 25타일 제약: 밀 타일 1개 = 새벽 러시 멜론 1개(≈$1.4k) 또는 선착 딸기 1개를 밀어냄; 멜론 6+밀 11 원형은 d2 밀 시비가 비료 5개를 먹어 현금 0 → 고용 실패 → −12.8k 붕괴); 생산 전 격일 급식(feed_alt, 케어 보너스 상한 이용: 소 2일) +0.1k/0; d0–8 밀 시비 금지(nwf_lo 0) 자체 +0.7k·마진 +0.2k(n.s.); 배치 최우선(place_pr −1) −0.75k; 경로 지속(vrp_persist) −18k(파손). 결론: Majkel의 d0–9 우위는 '밀 자급 + 러시 없는 멜론'에 의존하며 o227 상대 우리 타일 배분(러시용 d0 멜론 7 + 선착 딸기 8)이 우세 → d0–9에 구조적 slack 없음. 다음 축(테이프 타이밍 exploit)으로 이동.
- 09-18 12:33 **테이프 타이밍 exploit 탐색**(`o_tools/sell_hist.py`: 엔진 `_commit_unit` 훅으로 양측 실제 단위 매도를 (품목·시각·가격)으로 기록, sel 32경기). 테이프의 대량 덤프는 멜론(d10 h9–13: 6/24/12/6/6)뿐이고 우유·양털·달걀·비료는 시간당 1~3u의 연속 흐름(타이밍 차익 없음). 딸기: 테이프는 수확 당일 오후(h13–23, 170/246u)에 매도, 우리는 주머니에 들고 있다가 일말 드롭 후 다음날 h0–5(4u/시간 배치)에 매도 → 매일 테이프 뒤에서 팜(이론 슬랙 ≈ +$0.8k 자체, 마진 ≈ +1.6k). 멜론 러시: 36u 중 24u가 h9–10에 테이프 덤프와 겹침(이론 자체 +$0.47k, 상대 −$1.1k). 실험: (a) 아침 딸기 수확 우선 + 정오 전 은행화(sw_bank_am, 3변형) 자체 −0.5~−3.2k·마진 +0.4~−2.2k — 수확이 여전히 오후에 이뤄져 매도 시각이 거의 안 움직이고 아침 노동만 잃음; (b) 멜론 2차 물결: 급수 생략(melon_water10 0) −0.5k, rush_all 3세트 +0.3k(hold −0.2k), 링 배치(rush_ring 2/3 ± 배치 최우선) −2.7~−12.8k(원인: 축군이 d≥3에 놓이면 d0 배치 지연 → d1–2 급식 누락 → 양 이탈; 러시 자체는 h2–h8에 36u 완판으로 이상적이었음). 결론: 멜론 러시 외 비대칭 타이밍 창은 딸기 하루 선매도(≈+1.6k 마진)뿐이며 현 디스패처로는 아침 수확·은행화 비용이 더 큼 → 보류.
- 09-18 12:33 **dumper/pacer 적응 oracle**: 상대 유형을 완전히 안다고 가정해도 최적은 양쪽 모두 '덤핑'(base19): vs 페이서 sel/hold/fresh 마진 +1.0/+2.8/+0.6k(승 23/27/20 of 32), 페이스 정책은 거울 0; vs o227 페이스 −2.7k. **oracle 가치 = 0 < +1.5k → 적응형 정책·탐지기 중단.**
- 09-18 12:35 근접/중간 패배 세계 장부(7005 −6.9k, 7014 −7.2k, 7026 −6.0k): 공통으로 **사료 매수 $7.7~12.1k vs 테이프 $4.4~5.0k**(우리 밀 생산 ≈330u vs 테이프 ≈640u: 40딸기+밀 회전이 사료 자급, 우리는 당근/토마토가 밀을 밀어냄) — 당근+토마토 수입(+$10k)이 사료(+$7k)·밀 매도(−$6k)와 상쇄되고 우유 단가(7014 $84 vs $110: 글럿 시장에서 당일 오후 매도자가 다음날 아침 매도자보다 ≈k·(n−c/2) ≈ $17/u 유리)로 진다. 배분 노브는 평탄(기존 결론)이라 여기서도 slack 없음. 오늘 추가된 스위치(feed_alt, place_pr, bank_am, t0war, fert_h23, anim3_y2/anim3_cows)는 전부 off, 파일 = base19 비트동일.
- 09-18 13:20 **Top-5 재정찰**: `o_tools/fetch_current_elite.py`(공개 API, 팀별 최신 50경기: MG 3200·Majkel 3189·Boey 3147·SpaTaro 3145·DSM 3082·Orbital·ymg_aq·Otter) → `o_replays/elite_current/`; `o_tools/elite_profile.py`(체크포인트·3구간 schema) → `reports/o-elite-profile-2026-09-18.ko.md` 표. 핵심: Top-5 = 정제된 공개 포크 골격(멜론 12/밀 7/2C2S 또는 멜론 6/밀 9.5/2C3S) + **수요 비례 스케일링**(딸기 19→44/베리상점, 젖소 4.6→12/우유상점, 양 3→13/얀, 후반 당근 19~28) + 시비 밀(4.8~5.0u) + 낮 매도. base19와 격차 ≈10k(세계 유형 무관). **라이브(base17 55경기 1283, base19 15경기 1525)**: 포크 계보 상대 43/70경기에 60%(+3.5k)만 — 플래너는 포크를 억제(o227의 거울 미세구조, v37 −53k)도 생산 우위도 못 함 → 래더 천장 낮음. 동결 elite pool 도구 `o_tools/elite_pool.py`(paired 전용; Boey/SpaTaro/DSM 동결은 분산 큼). 후보 스크린(o227 sel + 동결 MG/Majkel + 반응형 포크 v37/V46/K0006): α/β 개막(w0seed 9~11, melons0 6/12, sheep0 2, cow5), 밀 보유 패키지(당근 축소+즉시 재파종+nwf_d 10), 축군(rf_deep/sheep_plus/herd_min/room_f), 스텝0 왕복 확대(13+30/30+30) — 전부 0 또는 음(양2 개막은 포크가 +3.6~5.4k). 결론: 부분 이식 불가 → 포크 골격 기반 새 플래너(base20-F) 설계로 전환.
- 09-18 13:32 하이브리드 실험(base19 농장 + o227의 d0–1 시장 주문 스트림 녹음 재생, `state/o_dev/p000_hybrid_t01.py`): vs v37 **+43.6k·32/32(v37 87k로 붕괴, 우리 130.7k)**이지만 vs o227 −19.6k(3/32), V46 −17k, K0006 −18k, 페이서 −18k, base19 −18.6k(0/32), 동결 MG −32k → 녹음 스트림은 v37·seed 7000 조건에만 맞고 일반화 불가(형제 계보의 적응형 시장층이 필요). 포크 붕괴는 테이프 계보 고유 자산으로 확정. 전략 갈림길: (i) 플래너에 포크 골격+수요 비례 스케일링 경제를 별도 모드(base20-F)로 구현해 반응형 포크 상대 승률 ≥85%를 노림, (ii) 공개 포크 소스(v37/V46, 편집 가능) 기반 새 테이프형 봇에 우리 실행 개선을 이식. 라이브: base19 15경기 1525(포크 상대 60%).
- 09-18 14:30 **base20-F 구현·1차 스크린(기각)**: `sw_fmode`(기본 off, base19 동일성 ident20 +0 확인) — F1 = 별도 `fmode_pri`(2C2S·멜론12·밀 잔여, d1–5 소4·거위2, 딸기 d3+, 수요비례 목표 cows 4.6+1.7·milk/sheep 3+4.5·yarn/geese 1+1.5·egg + 층(6/3/2), 밀 하한 7/8/15/22, 당근·토마토 하한 안): 포크 풀 own **−10.7k**, 마진 −17k(v37 2/32·V46 0·K0006 0). 원인(7010·7007 trace): 딸기 지연(d6 5, d9 10 vs base19 12/22) → 선착 파이를 포크가 가져감(v37 딸기 +8k), 우유상점 없는 세계의 소 6마리(우유 3.5k=base19와 동일), 당근 상한 −3k, 밀 '엔진'은 base19도 이미 540u(가난한 세계).
- 09-18 14:50 F2(base19 흐름 안의 플래그: 골격 d0 + d1–5 소4 + d6–14 축군 층 + 밀 필러 d6 + 당근 타일 상한 + 밀 시비 d10+ + 입고 규칙 fm_bank + seed_ahead/replant + 일손5): own −12.3k → 층 제거·필러 제한(F2d) −6.6k → 딸기 프로그램 base19 그대로(F3) −4.8k. 발견: d6 첫 양털 12u가 플랜터 주머니에서 일말 드롭까지 대기 → d7 매도(하루 지연) → `fm_bank`(주머니 $v 이상·창고 5칸 이내면 먼저 입고) 추가; v=400은 −1.5k(과잉 왕복), v=1000 +0.3k.
- 09-18 15:00 **F 성분 ablation(v37 32경기, base19 대비 own/opp)**: 12멜론·2C2S 개막 = own +1.4k / **상대 +6.0k**(양 1마리 적음 → 상대 양털 +3.2k·비료 +1.4k·우유 +1.35k·딸기 +1.3k, 멜론 −1.2k; 7000: d9 현금 $4 → d10 일손 3 → 러시 실패 → 상대 +14.6k). 1C3S+12M own −0.8k/opp +1.9k; 소4 d1–5 −2.3k; hire_res(d9) own +0.0k/opp +4.9k; 당근 상한 −0.6k(마진 −1.0k); 밀 시비 d10+ own 0/상대 +1.5k(비료 매도 감소 = 상대 비료가격 상승); replant 0; 일손5 0; base19 d0 위 F 나머지 −2.8k(그중 d1–5 블록의 멜론 보충 부재 −2.0k).
- 09-18 15:03 **축군 층(MG형 d9 6C5S2G·d12 7/6/3) 단독**: v37 own **−9.1k**, 동결 MG/Majkel own **−5.9k**(66/80 악화) — 상대(포크 17마리·동결 MG 17.5마리)가 이미 우유·양털 시장을 채워 추가 공급은 사료·구입비만 소모. cow5 −1.7k, anim3 −0.2k, bank1000 단독 −0.8k. F3c(12M+bank1000) 동결 풀 own −1.0k/마진 −4.8k. **결론: base20-F 폐기(게이트1 실패, 게이트2도 음).** 동결 MG 16세계 분해(fkpi2)에서 본 MG +18k(밀 후반 +6.9k·축군 +10k·멜론 +2.4k)는 *우리가 작은 공급자일 때* MG가 가져가는 몫이지 우리가 공급을 늘려 얻을 몫이 아님(시장 흡수량 고정·선착순). 유효 신호는 첫 양털 입고 지연(fm_bank v1000 +0.3k own)뿐.
- 09-18 15:18 **소비 틱 이후 매도(`sell_h`, `sell_h_items`, 새 노브)**: 엔진은 스텝 순서 행동→시장→소비(step%4==0, 상점당 1~2u)라 h9 매도는 h1보다 소비 2틱(딸기 3상점 = 6u ≈ +$11/u, 우유 +$8/u, 양털 sq +$10~14/u)을 더 본 뒤 팔린다. sell_h=9 S/M/W/E: own **+1.05/+0.53/+1.15k**(o227 sel/hold/fresh, 마진 +0.18/−0.48/+0.01k, 승 44→42), 포크 own +1.3/+1.0/+1.5k·마진 +0.7/+0.0/+1.25k(승 동일), 동결 MG/Majkel own +1.65k·마진 +0.76k(5.6se, 10/80 악화). 상대도 +0.5~1k(비운 아침을 상대 단위가 차지). h13은 own +1.5k지만 상대 +1.6~1.9k; h17 마진 −2.3k; 아침 소량 트랜치(sell_am_n 4/8) own 감소. 딸기만: own +0.5k(se 0.07). **판단: 실재하지만 +1k own·승수 무변 → 후보 보류(base20 묶음 재료), 단독 승격 아님.**
- 09-18 15:48 **개막 미러(derail) 재발견 — 메커니즘 확정**: o227 스트림의 d0 h0 [B13,B10,S30]+h1 [S13,B5]를 플래너 h0/h1 주문 앞에 붙이면(`sw_t0war` + 새 노브 `t0_s1=S13/B5`) vs v37 **own +32.5k·마진 +46k·32/32**(hold/fresh도 96/96). 원인(`t01trace.py`): v37 = [B13,B30,S30]/[S13,B5] 예산정확 테이프. 락스텝 동일 인덱스에서 같은 품목을 같이 사면(B13↔B13, B10↔B30) 상대 매입가 +$1/u, 같이 팔면(S30↔S30) 상대 매도가 하락, h1 B5↔B5 +$2 → v37의 d0 말 현금 $15→$0 → d1 h0 HIRE($1) 실패 → 인부 0·가축 탈출·붕괴. [B23,S30]는 인덱스가 어긋나 붕괴 없음(+3k), h1만·S27(사료 3 보유)도 불충분 — 달러 단위로 취약.
- 09-18 15:48 미러의 자기 비용: 왕복 스프레드 $12(v37)~$60(o227 동일 스크립트)로 d0 사료비가 사라져 우리 가축이 d0–1 굶음 → vs o227 own −7.6k(0/32). `d0_res=60`(밀 씨앗 4개가 h1로 밀림)로 해결: **tA_m6r** = vs v37 +32.8k(96/96), o227 own +0.04/−1.07/−0.35k·마진 pooled −0.9k(승 44→42), V46 own −0.4/−0.8/−0.1k·마진 −2.4k(승 0/0/−2), K0006 own −0.1/−1.0/−0.05k·마진 −1.5k, 동결 MG own −0.1k/마진 +0.8k, 동결 Majkel own +4.2k(승 1→8, 녹음 재생 취약성). 세금의 대부분은 d0 예비금(res60 단독: own −1.0k, V46 +1.5k: d0 미급식 가축의 케어 보너스 손실).
- 09-18 15:48 **라이브 상대 분포(테이프 제출 371경기, `o_replays/live_all`)**: 개막 스크립트별 — exact0 [B13,B30,S30]/[S13,B5] **21%(79)·평점 2400·d0 말 현금 0**(테이프가 90%·마진 +39.7k로 이미 붕괴시킴); V46계 [B5,B10,S60]/[S13,B5] **35%(130)·평점 2650·현금 29(고정)** → 미러 면역(우리 테이프 69%); 기타 44%(평점 2091, 엘리트 포함; 테이프 86%). 엘리트 개막: MG [B13,B5,S13]/[S5,B5] 현금 25~33, Majkel [B5]/[S1] 5~16, DSM [B5]/[S1] 0~8, Boey/SpaTaro 탐색형. 플래너(base19)는 exact0 프록시(v37)에 50%뿐 → 미러로 100%.
- 09-18 15:48 조합(미러+res60+sell_h9): v37 +33.8k, V46 own +0.6k/마진 −2.5k(승 −2), K0006 +1.0k/−0.5k, o227 own +0.7k/마진 −0.9k **승 44→38** → sell_h는 묶지 않음. blind 7240–7255 미사용(미러의 가치는 o227이 아닌 exact0 상대에 있음).
- 09-18 15:58 **미러 다양성 풀 검증**(`$TEMP/dpool.sh`: `o_tools/diverse_pool.json` 49개 상대 × 4시드 × 2좌석, base19 paired): own **+5.8k·마진 +8.3k**, 승 276→320/392, 우리에게 불리한 flip 0. 완전 붕괴 10개(ahmedberatozer v35~v40, aurax7 v4, municef1, yhay81-0911-simple: own +24~43k, 8/8), 개선 7개(flexonafft +5.6k, prvsiyan +3.6k…), 마진 −1k 이하 8개(xuantianfengwu 계열 −1.4~−7.2k, bruceqdu −3.1k, v21-r1 −2.5k, kaitofukami −2.2k, llccqq624 −1.6k; 모두 우리가 8/8 이기는 약한 상대, 상대 현금 36~87k). `sw_mirror=1` 편의 스위치 추가(= sw_t0war,t0_q1 13,t0_q2 10,w0feed −7,t0_s1 S13/B5,d0_res 60; 기본 off, base19 동일성 ident21 +0). **base20 후보 = base19 + sw_mirror; 승격은 소유자 판단(달러 단위 취약, 상대 패치 시 −1~−2.4k 세금만 남음). blind 7240–7255 미사용.**
- 09-18 16:20 **소유자 지시(신규 국면)**: base20-F 폐기 유지, base20-mirror는 전술 exploit 후보로 보존(default-on 금지), 공식 챔피언 base19 유지, 새 구조 후보는 p001 계열 실험체. 축 1 = Adaptive Market Executor V2(딸기/우유/양털 상품별 독립 adaptive tranche seller; 고정 sell_h·price_hold 재시험 금지; ablation wool→milk→strawberry→milk+straw→all; 기록: our/opp revenue, paired margin, win flips, 상품별 $/u; 목표 강한 상대 paired margin +3k). 축 2 = Late Wheat Volume Engine(d18+ 유휴 인부·진짜 빈 타일만; 토마토·조기 딸기·멜론 러시·d0–9 현금 보호; wheat6/land4/축군/F/조기 재배분 금지; KPI 후반 밀 +100/+150/+200u의 마진 효과). 두 축 독립 검증 후에만 결합. cheap screen = V46·K0006·v48·동결 MG·Majkel; 한 상대만 좋아지면 중단; live_weighted_arena 전까지 승격·blind 금지; +1k ceiling이면 폐기.
- 09-18 16:23 준비: `base19_vs_v48_sel` 기준 생성(base19 own 107.1k vs v48 82.1k, 32/32 — v48은 로컬에서 약함, 강한 상대 지표로는 부적합) + forks.sh에 v48 추가. Ultracode 워크플로 wf_036460fd 시작: MX2/LWE 각 3설계자→2심판→합성 + `o_tools/mx_eval.py`(상품별 매출·$/u·paired margin·flip 측정 도구, base19 기준선) 제작.
- 09-18 16:55 **MX2 v0 (`sw_mx2`, p001 축1) 구현·스크린**: 상품별 시간대 계획 — 상대의 시간대별 매도 프로필(`opp_hour` EMA, track_market의 스텝별 rival 추정) + 대칭 생산 prior(우리 아침 재고, 오후 1.5배)로 남은 매도 시각(1/5/9/13/17/21 = 소비 틱 직후 + 지금)의 기대 재고를 만들고 재고를 water-filling(단위마다 기대 재고+계획량 최소 시각)으로 배분, 현재 시각분만 매도; h21·러시데이 전량, 창고 여유(shed만 100−8) 확보분은 즉시. 첫 버그: 여유 계산에 주머니 포함 → 매일 h0 청산(효과 0) → shed만으로 수정. 결과(own/상대/마진): 양털만 −0.04..+0.5k, 우유만 +0.3..+0.9k, 딸기만 +0.5..+0.8k, 우유+딸기 +0.8..+1.7k, **셋 다: o227 own +1.24/+1.31/+1.76k·마진 +0.29/+0.16/+0.56k(pooled +0.34k, 3.0se, 승 +2/96); V46 own +1.1/+1.4/+1.8k·마진 +0.2/+0.5/+0.6k; K0006 own +2.5/+2.5/+3.3k·마진 +2.8/+2.4/+3.6k(승 +2/+4/0); 동결 MG/Majkel own +2.27k·마진 +1.07k(9.2se, 0/80 악화)**. 상품별 $/u(vs K0006): 딸기 142→146, 우유 125→131, 양털 137→141(상대 불변); vs V46/o227/v37은 상대도 +0.7~1.2k(비운 아침을 상대 단위가 차지) → 마진 +0.3~0.6k. 연속 매도자 상대 마진 상한이 구조적(총 소비 고정, 타이밍은 분배 이동).
- 09-18 17:16 워크플로 wf_036460fd 완료(13 에이전트): MX2/LWE 설계 패널 합성 스펙 + **`o_tools/mx_eval.py`**(V46/K0006/v48 32경기 + 동결 MG/Majkel 40경기 = 176경기 67초; 엔진 `_commit_unit` 훅으로 양측 상품별 매출·단위·$/u, feed_spend, `--compare` = paired 마진·flip·상품표; 현금 정산 달러 단위 일치). 기준선 `o_results/mx/eval_base19.json`.
- 09-18 17:26 **MX2 최종(v0d = 현재 기본: mx2_decouple 0)** ablation(mx_eval, base19 paired 176경기, our rev/opp rev/마진/flip): 양털 +0.46/+0.11/**+0.36k**/0 · 우유 +0.70/+0.27/**+0.44k**/0 · 딸기 +0.67/+0.25/**+0.43k**/0 · 우유+딸기 +1.32/+0.59/**+0.75k**/0 · **셋 다 +1.93/+0.73/+1.21k(11.2se)/+2(K0006 7012 a/b)**; 상대별 마진 V46 +0.13, K0006 +2.56, v48 +1.36, MG +0.94, Majkel +1.16k. $/u: 딸기 144→147.5, 우유 126→128~131, 양털 139→140~149; 상대도 +1~3$/u. 변형: 마진 가중 mx2_w=2(own ↓ 상대 ↓, 마진 비슷), mx2_last=13(own ↓), 보유분 상한 분리 mx2_decouple=1(own −0.2~−0.7k: 보유분이 축군·딸기 상한을 우연히 줄이는 게 이득), 현금 하한 무영향. 설계 패널(AMX-2)도 같은 구조(틱 앵커·h0 선행·마진 가중 2·보유분 분리)를 제안 — 마진 가중/분리는 측정상 개선 없음. **판정: p001-MX2 = 강한 상대 paired 마진 +1.2k(K0006만 +2.6k) → +3k 기준 미달, +1k급 ceiling → 승격 없음, 스위치 off 보존.**
- 09-18 17:23 **LWE(p001 축2) 결과 — 폐기**: (1) 빈 타일 분해(`late_tiles.py`/`empty_trace.py`, d18–26): 평균 9~10 빈 타일 중 대부분은 1시간 내 재파종, 3~5개 구석 타일((9,0)(0,9)(1,9)…거리 9)이 며칠씩 방치 = VRP 최근접 정렬의 구조적 기아; 씨앗은 h2에 확보됨. 구석 우선 파종(lwe_pr 0/−0.5, stale 정렬)은 빈 타일-일 180→164지만 밀 441→398~425u(급수 밀려 수확량↓) → 실패. 왕복 90스텝/사이클 구석 타일은 PASS 30~50/일로 못 받침. (2) **엔진 사실**: 밀 창 age 2–4, 급수당 +1(시비 +2); base19의 age-2 시비(pr 3)는 같은 타일 must-급수(pr 0/1) 뒤에 실행돼 age-2 급수가 +1에 그치고, 시비된 밀은 age 3에서 3u(=wheat_units 3)로 조기 수확 → 후반 73회 시비가 거의 무의미. 시비를 급수 앞(pr 0)+age-3 컷 해제: 수확당 3.0~4.0→**5.0u**, 밀 441→500u(+59), 그러나 mx_eval: 밀 매출 +0.8k·사료 −0.4k 절약·비료 매출 −0.4k·**토마토 −6u(−0.5k)·당근 −12u(−0.5k)** → own −0.4k·마진 −0.4k(상대 비료가 +$1/u). 시비 pr 1.5(토마토 뒤)로 낮추면 시비 실행률 붕괴(밀 +0), age-3 컷 해제 단독 −0.7k(1일 더 점유·급수 누락 위험). lwe_d0=14 −2.0k. 기존 노브(seed_last 27·nwf_d 18·seed_ahead+replant)는 ±0.5k. **결론: 후반 밀은 노동·타일·비료에서 토마토/당근과 경쟁 — 유휴 자원만으로 +100u는 없음(상한 ~+60u ≈ own +0.9k, 마진 ≤0).** 스위치 `sw_lwe` off 보존.
- 09-18 17:30 추가 프로브(mx_eval 144경기): `sw_vrp_2opt` 마진 −0.02k(0); 2opt+land4@12 매출 +1.6~2.1k지만 마진 **−3.0k**(land4 재확인: V46의 4사분면·밀 37타일은 경제 전체가 스케일된 결과). 세션 결론: 로컬 풀에서 실행·타이밍 레버는 전부 ≤ +1k; 남은 라이브 레버는 전술(미러) 또는 live_weighted_arena가 보여줄 2650 V46계 상대의 패배 구조.
- 09-18 18:38 이틀(09-17~18) 작업 정리 문서 `reports/o-recap-2026-09-17-18.ko.md`(흐름·날짜별 표·base 이력·기각 목록·파일 지도·현재 상태). worklog 237~282행의 `09-18 00:20`~`09-19` 라벨은 시계 드리프트(실제 09-17 00~14시)임을 명기.
- 09-18 18:52 **제출물·실행환경·replay 일치 감사(보고서 1순위)**: 새 도구 `o_tools/live_replay_audit.py`(우리 라이브 리플레이에서 상대를 동결·우리 자리엔 로컬 파일을 넣고 매 스텝 행동을 서버 기록과 비교; `--fetch`로 리플레이 수집). **base19(56319267) 62경기 62/62 스텝 단위 동일**(시장·농부·일손 주문 전부, 최종 현금 양측 일치) → 타임아웃(actTimeout 1s)·예외·버전 드리프트 없음, 로컬 평가 = 라이브 행동.
- 09-18 18:55 **역사적 강자 비교(보고서 3순위)**: 같은 핀 고정 세계에서 테이프 o227/o239_50 vs V46 **12/32(마진 +0.9k)**, vs K0006 **10/32(0)**, vs v37 32/32(+53k 붕괴). base19는 14/32·14/32·16/32. → 테이프의 라이브 우위는 exact0 붕괴(전술)뿐, 반응형 포크에 대한 경제 우위는 없음. "테이프의 초반 경제를 플래너에 이식"할 대상이 존재하지 않음(이식 가능한 것은 `sw_mirror`뿐).
- 09-18 18:58 **현재 라이브 인구 동결 풀**(`o_replays/live_frozen/live_b19/` = base17/base19 라이브 117경기의 상대 녹음, `elite_pool.py --us Taeyang` 옵션 추가): 상대 최종 91.7k(녹음 91.9k) → 이 인구는 거의 비반응 테이프형 빌드(주류 "B13/S8·S9" 30경기: d12 축군17·딸기33·밀20, d24 밀37). base19 76/117(65%, 라이브 실측 72/119=60%). **MX2 80/117·own +2.45k·마진 +2.04k(14se, 악화 5/117)**; 미러 85/117·own +0.8k·마진 +1.4k(se 0.9, 붕괴 14경기 +20~29k vs B5/S1·B4B4 계열 −13~−21k 5경기: 동결 재생 혼돈 포함); 둘 다 89/117(76%)·own +3.2k. 패턴별 표는 세션 출력(B13/S8: MX2 +1.6k, 미러 0; B30/S25: 미러 +19.9k 5/6).
- 09-18 19:11 **MX2 독립 후보 동결**: `agent/p001_mx2.py` = `agent/p000_planner.py`(base19 본체, sha 7804e77b…) + `_SW_DEFAULT_ON`에 `'mx2'`만 추가(헤더 1줄 외 diff 없음), sha 448d6115…46331, 동일 사본 `state/o_dev/p001_mx2.py`, manifest `state/o_dev/p001_mx2.manifest.json`(부모·sha·diff·활성 스위치 23·MX2 파라미터 16·평가 출처). champion은 base19 유지, 동결 후 변경은 새 후보(p002~).
- 09-18 19:15 **MX2 승격 검토 문서**(새 시뮬 없음, 기존 결과만 집계) `reports/o-p001-mx2-evidence-2026-09-18.ko.md` ← `o_tools/p001_evidence.py`: 반응형 핀 고정 세트(o227/V46/K0006 각 3세트 96경기: 마진 +337/+427/+2,929, 승 36→38/32→34/32→38, W→L 0 전부), mx_eval 176 패널(품목별 $/u), 동결 MG/Majkel, 동결 라이브 풀 117(+2,039 se 146, 76→80승, W→L 0, 상대 제출물 117개 전부 서로 다름, 포함 매핑 117/119). 결론 범위(§E): 감사=base19 62경기만, 테이프 비교=V46/K0006 한정, frozen≈live 평균은 비반응 증명 아님, 축군 상관은 단서. 미러·MX2+미러는 부록 F만.
- 09-18 19:24 **arena 준비(실행 안 함)**: `configs/validation/live_weighted_arena_v1_p001mx2.json`(v1에서 models/comparison만 교체: p001-mx2 vs base19-planner; 상대 10·가중치·단계 seed·엔진 1.32.7 그대로, blind 7240–7255 미포함) → `prepare` 검증 통과, `state/agent_experiments/arena_p001mx2_screen/` 320경기 확정·실행 0. 판독기 `o_tools/arena_report.py`(클러스터 표+규칙 R1–R5, 합성 데이터로 스모크). 규칙·명령·한계는 `reports/o-p001-mx2-arena-plan-2026-09-18.ko.md`에 실행 전 고정.
- 09-18 19:27 로그 통일: 사용자 지시로 `reports/o-worklog.md` → `reports/o-working.md`(git mv, 이력 유지); AGENTS/HANDOFF/handoff/recap/memory 포인터 갱신. 이후 세션 로그는 이 파일에만 기록.
- 09-18 19:45 소유자 규칙 기록(AGENTS.md 경쟁 워크플로 절 + 메모리): 조금이라도 긴 작업은 기본 8워커, 긴 작업 12워커(canonical runner는 schema상 1..8 고정·contract 해시에 포함 → arena는 8 유지, 상향은 소유자 승인 후).
- 09-18 19:54 **라이브 주류 빌드 출처 추적(항목 5)** `reports/o-live-source-trace-2026-09-18.ko.md`, 도구 `o_tools/rival_source_trace.py`(첫 6턴 지문 대조 + 라이브 에피소드 재생 검증). "B13/S8·S9" = **공개 노트북 테이프 라우터**: Thomas Tschinkel router v5(93.8%) 7경기 — Sybery_AI ep 110295006 **720스텝 완전 동일 재현**(sha b87a27ed…, `donor_agents/agents/tschinkel-router-v5.py`); 74.5% v3.1 계보 8경기(d6/d25부터 분기); fieldbook(yhay81→flexonafft) 코어 + B13/S8 왕복 13경기(정확 판 미확보, 동결형 표기 유지); 왕복 N 변형 17; V46 1경기(neibyr) 720스텝 동일. 고정 턴(144/226/360/433)에 상점·가격 트리거로 꼬리 테이프 선택 → 반응형 강자 아님, 단 가격 트리거는 우리 판매에 영향받을 수 있음(동결 풀 한계). 그룹별: base19가 지는 곳 = router v5 3/7·왕복N 7/17·V4x계 2/7; MX2는 전 그룹 마진 +0.7~3.5k, 승 뒤집기 소수; arena v1엔 router v5·fieldbook 계보(34%)가 없음 → v2 후보. 공개 노트북 2개 추가 pull(`state/o_dev/public_pull_4/`).
- 09-18 20:10 **처리량 분석(항목 6)** `reports/o-throughput-2026-09-18.ko.md`, 새 도구 `o_tools/throughput_audit.py`(라이브 117경기 양쪽 동결 재생 + 엔진 훅: 행동 시도/실행/무효/유휴·이동·수확·빈 땅·미급수/미급식·잡초화/탈출·품목별 원장; 117/117 최종 현금 재현). 우리 유휴 1,433 vs 상대 557(d1–d9 집중)이나 일손은 매일 재고용(fib, 7명 $25/일) → 노동 병목 아님; 이동/수확 6.2 vs 6.8 우세, 무효 5 vs 53. 라우터 53경기 대비: 우유 −6.2k·비료 −6.9k·밀 순 −5.1k·멜론 −1.9k vs 토마토 +7.9k·당근 +4.7k·계란 +3.1k → −0.1k; 원인 = 축군(소 8.1 vs 6.3, 동물 16.6 vs 13.7, d2–d10 1마리/일). land4 −3k = 땅값 4,000 vs 저활용(밀 +68u·당근 +24u·비료 −40u, 고용 0, 상대별 −2.6~−3.4k 일정).
- 09-18 20:10 **구조 후보 1건(항목 7)**: p002 "cash-gated herd ramp"(현금 예비·market_room·빈 목장 타일 게이트, 1일 1마리, 비료 선판매; F 고정 하한과 구분; 정지 규칙 +1k). 구현·시뮬은 소유자 판단 후. 이번 작업 새 시뮬 0(재생·지문 프로브만), blind 7240–7255 미사용.
- 09-18 20:50 **소유자 7항 지시 처리**. (7) AGENTS.md Method: "강자=순수 planner" 전제 철회, 정책은 행동(반응 정보·결정 시점·반복 운영 안정성·이기는 상대)으로 분류, 계획+조건부 분기 구조 인정. (1) `o_tools/arena_hashcheck.py`(실행 전후 후보·상대·엔진·설정 해시 기록) + arena plan 갱신(조정 금지, v1 통과≠최종 승격). (2) 보완 패널 `configs/validation/live_lineage_panel_v1.json`: router v5(재현)·v3.1·boatlee v29·prvsiyan q45·v48·V46, 4모델(base19/p001-mx2/p002-cow1/p002-cow1-mx2), primary 2개, 새 seed, prepare 384경기(실행 0); fieldbook은 frozen 진단(`o_tools/lineage_report.py`)으로 분리; 규칙 L1–L4 고정 `reports/o-p002-panel-plan-2026-09-18.ko.md`.
- 09-18 20:50 **(3·4) p002 구현**: 본체 `sw_cow1`(default-off, `Proxy.cow1_offer`): 소 1마리, 창 d6–16, 같은 스텝 계획 구매 후 잔여 현금, 조건 현금예비/미충족 계획 없음/빈 타일/상대 공급 반영 우유가격≥100/보수적 회수≥200, telemetry `agent.telemetry`(canonical runner가 기록)·P002_DEBUG. 동일성: off==base19 4/4, 본체+mx2==p001 4/4. 동결 `agent/p002_cow1.py` f1ca4735…, `agent/p002_cow1_mx2.py` 88991c8e…, manifest `state/o_dev/p002_cow1.manifest.json`. 스모크 2경기만(7000 d8 h17 구매 own −1.9k, 7001 d6 h16 구매 own −1.8k; 결론 없음). 같은 날짜 비교(같은 경기 우리 vs 라우터, `o-throughput` §6): 라우터 소 구매 d2/d3/d6/d7/d8, 우리 현금 d6–9 425~1,600, 아침 여유 d8부터 4~9 유닛-시간.
- 09-18 20:50 **(5) 평가 설계**: `o_tools/p002_report.py`(발동률·구매일·차단 사유·추가 우유/비료 수입·소/사료/고용·밀려난 생산·상대 수입·마진·flip·구매/미구매 분리; mx_eval·canonical 둘 다), mx_eval 별칭 router_v5/router_v31/boatlee_v29/prvsiyan_q45/fieldbook + 후보 telemetry 기록, `arena_report.py --rules panel`. (6) 12워커 보류, 전부 8워커. 실행은 소유자: A arena v1 → B mx_eval 4라벨 → C frozen 2라벨 → D 패널 384.
- 09-18 20:56 **p002 스모크 원장 감사(소유자 3·4항)** `reports/o-p002-smoke-audit-2026-09-18.ko.md`(도구 `o_tools/p002_smoke_trace.py`, 출력 `o_results/p002_smoke_trace.txt`; 같은 2경기를 결정적으로 재실행해 원장 추출, 새 평가 게임 없음; 후보·설정 불변). **정정**: 7001 부모는 74,541(V46) → own −651(앞서 −1.8k는 o227 동일성 수치 오인). 7000: BUY d8 h17 성공, 배치 d8 h23, 첫 급식 d9 h12, 첫 수확 d16 h14(계산과 일치), 새 소 22u이나 축군 합 +8u(다른 소 급식 −1회·미급식↑ = 아침 급식 여력 한계), 우유 매출 −963(+8u, 시점/가격), 사료 −2,163, 딸기 −1,330/밀 +1,319, own −1,904·상대 −2,135·margin +231; 7001: 새 소 27u, 우유 +30u에 +475($16/u, d13부터 가격 붕괴), 사료 −984, own −651·상대 −2,270·margin +1,619. +1 소는 끝까지 유지(앞당김 아님). 원장 잔차 0. 조건 점검: 타일 위치·급식 시간대 미확인(설계 한계, 실제 작용), 생산 시점 정확하나 케어 보너스 무시(단위 3배 과소)·가격은 공급 후 추정이지만 d6–8 상대 이력 0으로 낙관·비료 내부 소비 미구분(2배 과대), BUY 성공 미확인(잠재 결함, 이번엔 미발생). 수정은 p003+.
- 09-18 21:02 소유자 지시(추가 구현 중지, A→B 대기): 후보·파라미터·기준 유지, p003 보류. 스모크 2세계(v46/7000/s0, v46/7001/s1)는 개발 사례로 표시(manifest `development_cases`; `p002_report`가 플래그하고 제외 합계도 출력). p002 판정은 own·margin·승률 각각(세트 평균 gate, 개별 손실은 맥락), 구매 시도/확인/실패 분리 집계(`cow1_done` 한계는 동결 후보의 알려진 한계로 기록), 미구매 경기의 부모 대비 차이 확인, 사료/비료 Δ는 농장 전체 원장 변화로 서술(직접 비용 단정 금지), 잔차 0 ≠ 원인 규명. `o_tools/p002_report.py` 확장(시도/확인/무시도 분리, 개발 사례 제외 합계, 최대 손실 사례, 미구매 차이 목록). p003 방향은 B 이후 하나만(급식 경쟁/가격 예측/예정 지출/시장 경쟁 효과/종료).
- 09-18 21:12 **실행 주체 변경**: 사용자 지시("소유자는 이제부터 너야")로 시뮬레이션 실행·판정을 Claude가 수행(8워커, 비중첩, 기존 결과 보존). Kaggle 제출은 명시 지시 전까지 하지 않음.
- 09-18 21:13 **A(arena v1) 1차 실행 실패 → 실행 오류만 수정**: `arena_p001mx2_screen` 0/320, 상대 `dmitrii-lb2700`(donor 디렉터리 main.py = policy.py/router.py/actions.json 로더)이 runner의 단일 파일 스냅샷에서 step 0 FileNotFoundError(4 job invalid). 다른 18개 model/opponent(두 config)는 스냅샷 조건 프로브 통과. 수정: 무손실 단일 파일 번들 `state/o_dev/opponents/dmitrii_lb2700_bundle.py`(router.py 원문 + actions.json lzma/base85 인라인 + sale_horizon 3 + 마지막 callable 래퍼 `bundled_agent` — 'agent' 재정의는 dict 순서상 `_SALE_PARENT`가 선택돼 step 310부터 갈라짐을 확인하고 새 이름으로 해결). 디렉터리판과 7000/7001×양좌석 4경기 행동 스트림·최종 동일(`…bundle.check.json`). 실패 캠페인 디렉터리는 보존.
- 09-18 21:21 **A 재실행**: `configs/validation/live_weighted_arena_v1b_p001mx2.json`(v1과 동일, dmitrii만 번들로 교체; 가중치·seed·규칙 불변) → `state/agent_experiments/arena_p001mx2_screen_v1b` prepare 320, 실행 전 hashcheck PASS(contract ca08fb0e…), 8워커로 실행 시작.
- 09-18 21:28 **A screen 결과(arena v1b, 320/320, 실패 0, 타임아웃 0, 해시 전후 PASS, 최대 결정 0.23s)**: MX2 vs base19 family 가중 point delta **+0.037 CI [0.00, 0.15] → inconclusive**(음수 아님); pooled 마진 +402, own **+2,234**, W→L 1(dmitrii), L→W 5(v48 1·shop-router 2·c129 2·o227 2); 승 48→54/160. 클러스터: elite +2(dmitrii −1,375 / nagata +1,379), forks +1,295(V46 +1,625·K0006 +966), climbers +385, tapes **−190**(v37 −508), anchors +518; 가중 마진 +480. **R1–R4 PASS** → confirm 단계 진행. 최악 상대군 = cluster4(v37 −508), 최악 상대 = dmitrii(−1,375, W→L 1).
- 09-18 21:40 **A confirm 결과(v1b, 320/320, 실패 0, 해시 PASS)**: MX2 vs base19 point delta +0.006 CI [0, 0.025] inconclusive(음수 아님); pooled 마진 **+1,166**, own +2,021, **W→L 0**, L→W 1(dmitrii); 상대 10종 전부 마진 +(+87 c129 ~ +3,398 K0006); 클러스터 elite +936·forks +2,011·climbers +1,456·tapes +624·anchors +803, 가중 마진 +1,292. **R1–R4 PASS** → final(16 seeds) 진행 예정. 승률은 여전히 거의 불변(승 +1/160).
- 09-18 21:45 **B 결과(mx_eval 208경기 × 4조합: v46/k0006/v48/router_v5 반응형 + 동결 MG/Majkel, 같은 seed·좌석)**: **MX2−base19 own +1,953(se 85)·마진 +1,367(se 102)·승 80→84(W→L 0, L→W 4: K0006 2·router_v5 2)**, 상대별 마진 전부 +(router_v5 +2,208, K0006 +2,560, Majkel +1,162, MG +942, v48 +1,363, V46 +126). **p002−base19 own −1,487(se 145)·상대 −1,372·마진 −115·승 80→78(W→L 2 router_v5)**; 6개 상대군 전부 own 음수(−834~−2,129), 151/208 경기 own<−500. **(MX2+p002)−MX2 own −1,529·마진 −144·승 84→82(W→L 2 K0006)**; 상호작용 마진 −29·own −42(≈0, 가산적). 조합−base19 own +424·마진 +1,224·승 82 < MX2 단독 → 조합 불채택. p002 진단: 시도 199/208(96%), 확인 196, 미확인 3, 무시도 9(부모와 완전 동일 ✓); 구매일 d6 29·d8 109·d10 52; 차단 사유 cash 85%·room 5%·tile 4%·queue 4%. 원장(경기당): 우유 +18.4u인데 **+$48**(축군 전체 단가 129→117: 한계 수입 ≈ $3/u), 비료 +15u에 +$352($23/u; 가정 60), 소 +383, 사료 전체 +1,047, 다른 품목 −534(당근·토마토·밀), 상대 수입 −1,360 → 시장 경쟁 개입(own↓ rival↓)이며 순수익·승률 개선 아님.
- 09-18 21:45 **판정**: 진행 = MX2(p001, arena final·C·D 계속); 폐기 = p002 단독·MX2+p002(own·마진·승률 3기준 모두 미달, 상대군 전반 일관 손실). 주원인 = 가격 예측 실패(우유 한계 수입이 inframarginal 단가 하락에 상쇄: 구조적)+비료 과대+식재 대체; 급식 여력은 부차. 일관된 개선 가능성 없음 → **p003 미착수, 축군 증설 실험 종료**(소유자 규칙 "어느 쪽에서도 일관된 이득이 없으면 종료"). 상세 `reports/o-p002-B-verdict-2026-09-18.ko.md`.
- 09-18 22:03 **A final(v1b) 437/640에서 중단 → 실행 오류만 수정 후 v1c로 재실행**: base19 vs o227 seed 1382149642 좌석0에서 o227 telemetry `overflow_contract_errors`(R148 창고 예측 자기점검 카운터, 예외 아님)가 1 → runner health 규칙(양성 `*error*` 키 = 오작동)으로 게임 invalid → 단계 중단. 수정: `state/o_dev/opponents/o227_stealth_arena.py`(o227 원문 + 래퍼: 그 키만 `overflow_contract_mismatch`로 개명, 예외 카운터는 그대로) — 4경기 행동 스트림·최종 동일 검증. `live_weighted_arena_v1c_p001mx2.json`(v1b + o227 래퍼만) prepare 640, hashcheck PASS, 실행 시작. 중단된 v1b final 디렉터리(437 결과)는 보존(미완성이라 판정에 사용 안 함). 관찰: 다른 상대(V4x 계열·shop-router·c129)도 caught-exception 카운터를 가짐 — 실제 예외면 무효가 맞으므로 건드리지 않음.
- 09-18 22:07 **A final 결과(v1c, 640/640, 실패 0, 해시 PASS)**: point delta +0.034 CI [−0.047, +0.103] inconclusive; pooled 마진 **+992**, own +1,389, W→L 7 / L→W 18; 상대별 마진 9/10 +(V46 **−352**, 2 W→L / 0 L→W; shop-router-v5 +1,984이지만 W→L 2 / L→W 1; K0006 +1,966 2/3; v48 +517 1/1); 클러스터 elite +1,483·forks +807·climbers +1,250·tapes +542·anchors +878, 가중 마진 +1,091. **R2 FAIL**(c2+c3 상대별 W→L ≤ L→W 위반: V46·shop-router-v5), R1·R3·R4 PASS → **arena gate 최종 불통과**. 사전 규칙대로 가중치·상대·seed 변경 없음. MX2 = own·마진은 전 단계에서 +, 승률은 반응형 포크에서 개선 없음(V46 0.34→0.28).
- 09-18 22:15 **D 결과(라이브 계보 패널 384/384, 실패 0, 해시 PASS; router v5·v3.1, boatlee v29, prvsiyan q45, v48, V46 × 4모델)**: **MX2 vs base19(descriptive) pooled 마진 +2,085·own +1,129·W→L 0·L→W 8**; router_tschinkel 클러스터 마진 +3,240/own +2,809, WR .25→.375(v3.1 L→W 4), router_v5 +2,841(WR .25 유지), roundtrip_n +2,360, v48 +1,495(own −1,037), V46 −184(WR 0/16 전 모델). **p002 vs base19 own −2,281·마진 −1,294·W→L 11/L→W 9**(boatlee v29 −6,310, W→L 5); **p002+MX2 vs MX2 own −1,152·마진 −1,132·W→L 10/9** → L2·L3 FAIL(발동률 94%). p002 폐기 재확인.
- 09-18 22:16 **C 결과(frozen 117, 개발 자료)**: MX2 +2,039(se 146, W→L 0), p002 **−114**(se 245, W→L 2, 56경기 악화), 조합 +2,006(≈MX2 단독). fieldbook A/F: MX2 +724/+1,530, p002 −316/−761.
- 09-18 22:17 **최종 판정** `reports/o-final-verdict-2026-09-18.ko.md`: **제출 권고 없음, base19 유지**. MX2 = 보류(arena final R2 불통과; own·마진은 전 세트 +, 승률 불변), p002·조합 = 폐기, p003 미착수(축군 라인 종료), blind 7240–7255 미사용 유지. 다음 개발 대상 후보: V46형 하드 포크 패배 메커니즘(base19 arena −3.9k, 패널 0/16); MX2 재도전 시 seed 44142014 원장부터.
- 09-18 22:52 **V46 손실 분석 → p003(feedrot) 구현·개발 평가 → 기각** `reports/o-p003-hypothesis-2026-09-18.ko.md`. 분석 도구 `o_tools/pair_trace.py`(같은 경기 양쪽 일별 원장·시간별 판매·상대 telemetry; `--knobs`). base19 vs V46 exact 64경기 마진 −2,247·승 24/64(양봉: 베리/우유 세계 큰 패배 26, 피자/펫/야른 세계 승 24). 큰 패배 원장: 밀 −11.4k(순생산 −230u)·우유 −6.8k·비료 −5.9k·양털 −2.9k·멜론 −1.7k vs 토마토 +5.2k·당근 +2.8k; 운영 순서: V46 소 d2·d3(4마리)·d6–7(7.5), Q3 d11, 딸기 33(d11), 밀 24–38; 우리는 3번째 양·딸기 8(d2–5)·Q2 d6 저축·Q3 d9 저축, 소 d6–10, d2–d8 밀 타일 0 → 매일 사료 구매($2.3k d0–9). 가설(사료 자급 회전 d3–11)을 `sw_feedrot`로 구현(off 동일성 4/4) → 64경기 **own −195·상대 +3,564·마진 −3,759·W→L 4**: 회전 밀이 딸기 타일을 선점(d6 13.9→8.4), 소는 안 빨라짐(초반 축군 제약 = Q1 타일 예산 + Q2 시점), V46 딸기 +3.0k → 기각(스위치 휴면 보존). 멜론 −1.7k = d1–2 보충 5멜론이 d11–12 $133에 팔리는 것(d0분은 h6 $270로 V46보다 먼저). 결론: 새 메커니즘 없음 → base19 유지.
- 09-18 22:59 인접 점검: `land3=10`(Q3를 멜론 현금 뒤로) V46 64경기 own −419·마진 −1,349(d9 현금 3,259가 미사용: 제약은 Q2 타일 만석) 기각; `sw_mx2c0`(소비 상점 없는 품목 분산 금지) 44142014에서 발동 6회·효과 0(양털은 FARMERS가 소비) — 휴면 보존. 44142014의 MX2 실패 메커니즘 = 상대 재고가 큰 품목의 h1 덤핑(시장 거부)을 MX2 분산이 풀어 V46 양털 +5.5k. **V46 라인 결론: 유효한 개입 없음, base19 유지**(`reports/o-p003-hypothesis-2026-09-18.ko.md` §6–7).
- 09-19 04:35 **V46 exact 결정 지점 추출**(소스 전 층 + 64경기 추적): 가격 조건 분기 = d9 소 전환(MILK≥WOOL, 9/32), d12 남동 양 6(WOOL≥220·WHEAT≤45, 2/32), d18 토마토 투자(TOMATO≥70, 9/32), 급식 생략(국소 최적), 투입 계획(비료 가격); 거울·클론·유사도·현금 탐침은 정체성 의존(진단 전용); tape 구매는 밀·비료만 가격 의존, 실패 주문 재시도 없음, 지연 1스텝.
- 09-19 04:38 **도달 가능성·절제 상한**(pair_trace, 절제 래퍼 `state/o_dev/opponents/v46_ablate_{v233,v219,v231,r51}.py`, 104경기): D2 양털 32–68u 필요 vs 보유 12(상한 마진 +3.9~+9.3k; 7030은 V46에게도 손해인 투자가 우리 −12~−16k), D1 우유 8–44u vs 6–12(2/9 세계만; 상한 +1.9k, 우유 가격 경유), D3 토마토 29–155u vs 0(상한 +0.6k, 6/18만 +), D5 비료 ~60u(상한 +0.36k).
- 09-19 04:41 **판정: 관측 가능한 정보로 실행할 유효 개입 없음(구현 없이 종료)** `reports/o-v46-decision-points-2026-09-19.ko.md`; p004 미사용, base19 유지, blind 미사용. handoff·AGENTS.md 갱신.
- 09-19 04:53 **정책 3종 공통 패널 비교 계획 고정** `reports/o-policy-compare-plan-2026-09-19.ko.md`: base19·V46 exact·router v5(라이브 720/720 재현 파일)를 우리 좌석 후보로, 후보 소스를 뺀 reacting 12상대·8 family 동일 가중 패널(arena v1c+lineage panel 재사용), 새 시드 RNG 20260919(screen 8/confirm 8/final 16, 기존 전부와 불겹침), 규칙 P1–P5·결정 (a)(b)(c)·조건부 선택 절차·Macro Oracle 차이 명시. 설정 `configs/validation/policy_compare_v1.json`(576/단계), 자기·교차 대전 진단 `policy_h2h_v1.json`(144, 별도). 어댑터 불필요(두 정책 모두 단일 파일, 러너 상대 좌석 실행 이력).
- 09-19 04:54 screen 실행 시작(`state/agent_experiments/policy_compare_screen`, prepare 576, hashcheck PASS contract ab90c0a9…, 8워커). `o_tools/arena_report.py --rules policy` 판독 절 추가(P1–P5·세계 구성·큰 손실·복제 감지 표시).
- 09-19 05:04 **screen 결과(576/576, 무효 0, 해시 전후 PASS, 최대 결정 0.21s)**: 승점률 base19 .422(81-111) / **V46 exact .906(174-18)** / router v5 .401(77-115). V46 vs base19: family 가중 승점 차 **+0.473 CI [.17,.67] positive**, 8/8 family ≥0(최소 +0.000 nagata: 둘 다 1.00), L→W 97 / W→L 4, 두 좌석 +.45/+.52, own +17.3k·마진 +9.4k, 큰 손실(<−10k) 41→0 → **P1–P4 통과 → confirm 실행**. router v5 vs base19: −0.023 inconclusive, 3/8 family, W→L 32, 큰 손실 69 → 불통과. 세계 지표 전부에서 V46 우세(pet2 1세계만 −.04). 복제·유사도 감지: V46의 race/probe 키가 tape 계보 8상대(dmitrii·K0006·c129·o227·v37·v38·shop-router·prvsiyan) 전 경기에서 발동(표시만, 제외 안 함).
- 09-19 05:15 **confirm 결과(576/576, 무효 0, 해시 PASS, 새 시드 8)**: 승점률 base19 .490(94-98) / **V46 exact .943(181-11)** / router v5 .438(84-108). V46 vs base19 family 가중 **+0.495 CI [.22,.71] positive**(alpha .0075), 8/8 family ≥0, L→W 92 / W→L 5, 두 좌석 +.45/+.46, own +10.2k·마진 +9.3k, 큰 손실 0(base19 27) → **P1·P2·P4 재통과 = "대체 부모의 우세가 별도 확인에서도 유지됨"**. router v5 재불통과(W→L 35). 사후 best-of-3 oracle = V46 단독 +0.021(임계 +0.05 미만) → 정책 라우터 없음. 다음: h2h 진단 → p004 동결(V46 exact 원본 그대로) → final(넓은 검증).
- 09-19 05:18 h2h 진단(144, 무효 0): V46 vs base19 12-4(+4,944), V46 vs router 15-1(+13,784), base19 vs router 7-9(−2,158); 자기 대전 V46 2-2-12(거울 게이트), router 3-3-10, base19 8-8(좌석 비대칭 ±1.5~4.8k). 설명용.
- 09-19 05:19 **p004 동결** = V46 exact 원본 동일 바이트(`agent/p004_v46_exact.py` = `state/o_dev/p004_v46_exact.py`, 735c3703…) + `state/o_dev/p004_v46_exact.manifest.json`(출처·라이브 재현·규칙·결과·표시 사항). 계획서 §3에 final은 과제 밖으로 적었으나 8항의 "통과 후보 → 넓은 검증" 연결로 같은 설정 final을 이어서 실행(판정 규칙 불변, 시드 사전 고정).
- 09-19 05:40 **final(넓은 검증, 1,152/1,152, 무효 0, 해시 PASS)**: 승점률 base19 .492 / **V46 .919(353-31)** / router .401. V46 vs base19 **+0.417 CI [.19,.62] positive**(α .0125), 8/8 family, L→W 179 / W→L 15, 두 좌석 +.42/+.43, 큰 손실 0(base19 53). router 불통과(−0.091, W→L 81). **최종: 대체 부모의 우세가 별도 확인에서도 유지됨** → 개발 부모 후보 = `state/o_dev/v46_public.py`; 남은 단계 blind(보호, 소유자 결정) → QA → 소유자 제출. `reports/o-policy-compare-results-2026-09-19.ko.md`.
- 09-19 05:50 **라이브 이전 확인(공개 ListEpisodes 읽기)**: V46 exact 동일 바이트(neibyr 56314383) 162경기 84/58/20 **≈2,430 하락 중**(2400–2599 대역 42/49/15); o239_50(우리 tape) ≈2,660(최고 2,754); **base19(56319267) 75경기 38/37 ≈1,400**; router v5 ≈1,440. → 패널은 순서(V46 > base19 ≈ router)만 맞고 절대 수준은 대표 못 함(2400–2850 대역 실행 상대 0). **p004는 제출 후보 아님**(동결 기록으로만), 다음 우선순위 = 패널 대표성 수리(상위 대역 리플레이 지문 대조). 결과 보고서 §6.
- 09-19 06:20 **라이브 상위 대역 지문 대조**(2400+ 상대 제출당 1경기: V46 105·o239 171 리플레이 8.5GB `o_replays/live_band2400/`, 공개 소스 60종 지문): V46의 정체 원인 = **같은 개막(V46 계보) 상대에게 2승 23패 16무**, 그 외 40/28. 2600–2850은 라운드트립 tape 변형(B70/S70 30, B5/S5 11 …)+공개 라우터 30+B50/S50 16(우리와 동일 개막)+V46 계보 15+K0006 9. 저자 공개 노트북: **V47 공개 점수 2,686**(V46 2,439, V48 미표시). 다음 = V47 소스 확보(소유자 허가 대기: 파일 다운로드) → 패널 상대 + 정책 후보. 보고서 §7.
- 09-19 06:23 **V47·V48 소스 확보(소유자 허가, `kaggle kernels pull` 읽기 전용)**: 노트북 내장 바이트를 pinned digest로 복원 → `state/o_dev/v47_public.py`(f4ecd487…, 공개 점수 2,686) · `state/o_dev/v48_clearqueue_public.py`(4b540288…). 러너 로더 양 좌석 정상(오류 키 0, 최대 0.1s). 라이브 검증(V46 계보 41상대 720스텝 재생): 정확 V46 16(V46 exact와 0/1/15 = 거울), **정확 V47 3(0/3), 정확 V48 6(0/6), 그 외 변형 16(2/13/1)** — V46의 정체는 후속 버전에 지는 것. V47/V48 사본 평점 2435–2600 상승 중; 우리 tape 2,660~2,754.
- 09-19 06:29 v2 실행 시작: `policy_compare_v2`(base19·V46·V47·V48 × 같은 12상대·같은 screen 시드, 768경기; 주 비교 V47 vs V46, V48 vs V47; hashcheck PASS contract 1e848052…) → 이어서 `policy_h2h_v2`(5정책 상호 대전 400경기, 우리 tape o239_50 포함, 진단). 계획 부록 A.
- 09-19 06:44 **v2 screen(768/768, 무효 0, 해시 PASS)**: 승점률 base19 .422 / V46 .906 / **V47 .938 / V48 .938**(V48 = V47 완전 동일 결과). V47 vs V46 +0.035 CI [0,.086] inconclusive, V48 vs V47 0 → **패널 포화**: 상위 버전 차이를 못 가름(라이브에선 V47/V48이 V46에 9/9). base19·V46 셀은 v1과 동일 재현.
- 09-19 06:52 **5정책 상호 대전(400, 무효 0)**: 타 정책 상대 승점 **V48 .797(51-13) > V47 .609(39-25) > o239_50 .469(30-34) > V46 .375(24-40) > base19 .250(16-48)**. V48 vs V47 14-2(마진 +394: 판매 슬롯 경쟁), V47/V48 vs V46 14-2, V47/V48 vs o239_50 11-5(마진 ≈0), o239_50 vs V46 8-8, base19 4-12 전부. 라이브 사본(9제출) 대역별: V47 사본 2500–2650(2600–2749 55/61/17, 2750+ 4/18/4), **V48 사본 2560–2760**(2600–2749 91/76/62, 2750+ 9/27/9); 우리 o239_50 2600–2749 62/44, 2750+ 11/16. → V48이 로컬 최강이나 라이브 수준은 우리 tape와 같은 2,650~2,750대, 2750+ 군에는 둘 다 30–40%. confirm 시드 h2h 실행 중(순서 별도 확인).
- 09-19 07:02 **5정책 h2h confirm(새 시드 400, 무효 0)**: V48 .906(58-6; V47 16-0, V46 16-0, o239_50 12-4 +2,942, base19 14-2) > V47 .656 > o239_50 .438 > V46 .375 > base19 .125 — screen과 같은 순서. 라운드트립 대리(o238 B70/o239_60 B60, 160경기): V47/V48 11-5, V46 8-8, base19 4-12, o239_50 16-0(o239_50 상대와 동일; 2750+ 사적 변형은 대리 불가).
- 09-19 07:07 **결정 갱신**: 개발 부모 후보 = **V48 파일**(`state/o_dev/v48_clearqueue_public.py` 4b540288…; 부모 기록 `p005_v48_exact` + manifest, p004는 대체됨). 근거 = 상호 대전 두 시드 집합 전승 + 라이브 사본 6개 2,560–2,760. 한계 = 라이브 수준이 우리 tape와 같고 2750+ 군 30% → #1은 별도 과제. 제출 후보 아님, blind 미사용. 보고서 §8.
- 09-19 07:20 **문서 최신화(소유자 요청: 처음 보는 사람·AI의 입구 정리)**: `HANDOFF.md` 맨 위에 **START HERE**(한 줄 상태·상태판·절대 규칙·평가 방법의 현재 이해·소유자 결정 대기·정해지면 할 일; 옛 c-시리즈 내용은 "(보관)" 아래로), `reports/o-index-2026-09-19.ko.md`(보고서·정책 파일·도구·캠페인·자료의 현행/참고/종료 색인) 신설, `AGENTS.md` 맨 위 STATUS 블록 + 낡은 지시문에 날짜 주석(실행 위임·checkpoint 보관 표시), `docs/o-handoff-2026-09-16.ko.md` 맨 위 최신 요약 + 낡은 절 제목에 날짜, `CLAUDE.md` 입구·실행 위임 갱신, 이 로그 머리의 09-15 상태표를 보관 표시.
- 09-19 07:36 **C/O 실험 이력 정리(소유자 요청, Codex)**: `reports/c-worklog.md`(c-working 파일 없음)·이 원장·관련 보고서/일부 구현을 대조해 `docs/experiment-history-and-lessons.ko.md` 작성. 테이프 복구·o209 정책표·o214 투자 규모·o004/o233 인계·개막 혼합·base20-F·플래너 개선/기각·평가 오류를 실패/무동작/파손/미실행으로 구분하고 재시도 조건 기록; AGENTS/HANDOFF/색인/양 원장에 연결. 기록 정리이며 수치 독립 재검증 아님. 새 시뮬·전략 코드/후보/계약 변경·제출 없음, blind 7240–7255 미사용 유지.
- 09-20 00:30 **g000_apex_frontier 정식 감사·canonical 재검증·제출 확인 (Codex)**:
  - 선행 시도 감사: `state/agent_experiments/g000_apex_confirm` 폴더의 결과가 소 전환 완화(`V9_HERD_MIN_MILK_SHOPS = 2`)된 초기 프로토타입(`f177b767`)으로 실행되어 `promotion: false`, `win_to_loss: 6`로 실패했던 결과임을 확인. 정식 후보(`1ac340d0`)는 정식 validation_v2를 거치지 않고 보고서 수치가 기재되었던 결함을 적발.
  - 정식 canonical 재검증 완료 (`state/agent_experiments/g000_apex_confirm_v2`, 12 CPU 워커, 256경기 전수 격리 하위프로세스): 126승 2패 0무 (98.44% point rate), 평균 마진 +$3,105.7 vs v9 $2,952.2 (+153.5 delta), win_to_loss: 0 (회귀 0), tie_to_loss: 2 (시드 729160656 거울 대전), bootstrap 98.5% CI [+0.0625, +0.125] (전구간 양수, signal: "positive"). vs v9 30승 2패 (마진 +$551.9), vs k0006/o240/v49 각 32승 0패.
  - Kaggle 제출 확인: Ref ID `56363144` (`submission.tar.gz`) 상태 `SubmissionStatus.COMPLETE`, 초기 점수 688.9로 래더 진입 완료.
  - g001 메커니즘 탐색: `agent/g001_clean_advance.py` (SHA-256 `5753cb98...`)로 `protected` 주문 스킵 제거 실험. vs v9 마진 +$411로 급상승하나 일부 시드(1822423521)에서 조기 매도로 인한 가격 자기잠식 확인. 차기 g001은 잔여 호가 기반 동적 매도 스케줄러로 전개 예정.
- 09-20 01:05 **g001_dynamic_liquidation 정식 검증·제출 완료 (Codex)**:
  - 후보 파일: `agent/g001_dynamic_liquidation.py` (SHA-256 `6f5961356b750ec0ca74bcd917ca2e7bdb5fd64e3ca76dacdfe4ab92b0ed0eea`).
  - 기전: 가격 충격 인지 동적 조기 청산(Price-Impact-Aware Dynamic Liquidation). 작물(딸기·양털·달걀·멜론·당근·토마토)은 일괄 수확/상대 덤핑 가격 급락($1) 전 창고 실물 재고를 1~2스텝 선제 매도하여 고단가 선점. 우유(MILK)는 4스텝 소비 주기 직후 가격 반등($169)을 보존하기 위해 조기 전진 대상에서 제외.
  - 정식 canonical 검증 완료 (12 CPU 워커, validation_v2, 총 512경기 전수 격리):
    - screen (16 개발 시드, 256경기): 124승 4패 0무 (96.88%), 패밀리 가중 승점 델타 `+0.1016` (+10.16%p), bootstrap 98.5% CI `[+0.0391, +0.1719]` (positive), vs v9 28승 4패 (마진 +$287.6).
    - confirm (16 미공개 독립 시드, 256경기): 122승 4패 2무 (96.09%), 패밀리 가중 승점 델타 `+0.0859` (+8.59%p), bootstrap 98.5% CI `[+0.03125, +0.125]` (positive), 회귀 0건 (win-to-loss 0), 평균 마진 +$3,127.8 (vs v9 마진 델타 +$616.3, own cash 델타 +$435.1). 엘리트 상대 전적: vs k0006/o240/v49 전승 (각 32승 0패).
    - 512경기 합산 런타임 오류 0건, 타임아웃 0건, 해시 계약 100% 일치.
  - Kaggle 제출: Ref ID `56364496` (`submission.tar.gz`), `SubmissionStatus.COMPLETE` 확인, 레이팅 2483.2로 상승 중 (g000 2430.4 상회).
  - 차기 과제 (g002): 1위 Majkel(3278.5)의 d20+ 타일 재활용(밀 73.3회·당근 39.9회 재파종) 및 수확 후 토마토/당근 적응형 전환 연구·개발.

</details>
