# p001_mx2 arena 검증 계획 (2026-09-18, 실행 전 고정)

목적: 동결 후보 `agent/p001_mx2.py`(= base19 + `mx2` default-on)를 소유자 arena(`configs/validation/live_weighted_arena_v1.json` 체계)에서 base19와 **같은 seed·같은 상대·양쪽 좌석**으로 비교한다. 이 문서의 규칙은 결과를 보기 전에 고정하며, 결과를 본 뒤 가중치·통과 기준을 바꾸지 않는다.

## 1. 설정
- 설정 파일: `configs/validation/live_weighted_arena_v1_p001mx2.json` — v1에서 **models·comparisons만** 교체(상대 10종·클러스터 가중치·단계 seed·엔진 핀 그대로).
  - models: `base19-planner` = `state/o_dev/p000_base19.py` (sha256 53d80342…f31290), `p001-mx2` = `state/o_dev/p001_mx2.py` (sha256 448d6115…46331). 후보 manifest: `state/o_dev/p001_mx2.manifest.json`.
  - comparison: `p001-mx2` vs `base19-planner` (primary).
- 상대(전부 실제 코드가 매 턴 반응하는 **reacting** 에이전트; 동결 replay 없음), 클러스터·가중치(v1 그대로):
  | cluster | weight | opponents |
  |---|---|---|
  | 1 elite planners | 0.35 | nagata-scheduler, dmitrii-lb2700 |
  | 2 hard reacting forks | 0.30 | v46-reacting, jaxa-k0006 |
  | 3 modern fast climbers | 0.15 | v48-fast-climber, shop-router-v5 |
  | 4 fragile exact tapes | 0.10 | v37-more-yield, ahmed-v38 |
  | 5 historical anchors | 0.10 | c129-benchmark, o227-stealth |
- 단계: screen 8 seeds(alpha .010) → confirm 8 seeds(.015) → final 16 seeds(.025); 서로 겹치지 않는 seed, 720스텝, workers 8, 게임당 timeout 240s. **blind 7240–7255는 이 arena 어디에도 쓰지 않는다.**
- 호환성 점검(게임 실행 없이): `prepare`가 엔진 identity(1.32.7, 파일 해시)·12개 소스 sha·컴파일을 검증하고 `state/agent_experiments/arena_p001mx2_screen/manifest.json`에 **320 게임**(8 seed × 10 상대 × 2 좌석 × 2 모델)을 확정했다 — 실행된 게임 0.
- 산출: runner의 `results.json`(모델별 상대/패밀리/좌석 승률, 페어드 마진·own·W→L, 패밀리 가중 point delta의 부트스트랩 CI) + `o_tools/arena_report.py`(클러스터별 표, 클러스터 가중 점수, 아래 규칙 판정).

## 2. 적용 규칙 (실행 전 고정)
runner의 통계 계약(패밀리 동일 가중, seed 클러스터 부트스트랩)을 1차 신호로 쓰고, 소유자의 승격 조건을 다음 R1–R4로 옮긴다. R5는 기록만 한다.
- **R1** primary signal(`p001-mx2_vs_base19-planner`, 패밀리 가중 point delta CI)이 `negative`가 아닐 것. `positive`면 통과, `inconclusive`면 다음 단계로 진행은 가능하되 승격 근거로 쓰지 않음.
- **R2 (V46/K0006 승률 악화 없음)** cluster 2+3의 상대별로 W→L ≤ L→W, 그리고 cluster 2+3 합산 페어드 마진 ≥ 0.
- **R3 (elite 회귀 없음)** cluster 1 합산 페어드 마진 ≥ 0 이고 own cash delta ≥ 0.
- **R4 (anchor 안전)** cluster 5(c129, o227) 합산 페어드 마진 ≥ −1,000.
- **R5** cluster 4(v37, ahmed-v38)는 MX2 본체에 대해 기록만 한다(v1의 stage1 "WR ≥ 0.95 vs cluster 4"는 미러 오버레이용 게이트이며 본체에 적용하지 않음).
- 클러스터 가중 점수(arena_meta weights)는 **설명용**으로만 보고한다. 이 단계에서 어떤 결과도 champion/base20 승격을 자동으로 결정하지 않는다(승격은 소유자).
- 단계 진행: screen R1–R4 통과 → confirm(같은 규칙) → final → (통과 시) 미러 오버레이 재검증 → blind 7240–7255(핀 고정 도구) → 제출 준비. arena v1 통과만으로 최종 승격을 결정하지 않는다: 라이브 34%(router·fieldbook 계보)는 보완 패널·frozen 진단(`reports/o-p002-panel-plan-2026-09-18.ko.md`)으로 따로 본다.
- MX2 파라미터·통과 기준은 결과를 본 뒤 조정하지 않는다. 수정이 필요하면 p003 이후의 별도 후보로 분리한다.

## 3. 사용자 실행 명령 (PowerShell, 저장소 루트)
```powershell
# 0) 실행 전 해시 기록(후보·상대·엔진·설정 = config == 저장소 파일 == 캠페인 스냅샷; hashcheck-<utc>.json 저장). 실행 후 같은 명령을 한 번 더 실행해 일치를 확인한다.
.venv\Scripts\python.exe o_tools\arena_hashcheck.py configs\validation\live_weighted_arena_v1_p001mx2.json state\agent_experiments\arena_p001mx2_screen
```
```powershell
# 1) 준비 확인(게임 실행 없음; manifest/소스 스냅샷 검증)
.\tools\run-validation.ps1 -Config configs\validation\live_weighted_arena_v1_p001mx2.json -Out state\agent_experiments\arena_p001mx2_screen -Stage screen -Action Check
```
```powershell
# 2) screen 실행(320게임, 8 워커). 진행률/완료 수/cached/실패/경과/ETA는 Write-Progress로 표시되고 console-*.log에 PROGRESS 행으로 남는다. 종료 시 트레이 알림+사운드(성공/실패 구분).
.\tools\run-validation.ps1 -Config configs\validation\live_weighted_arena_v1_p001mx2.json -Out state\agent_experiments\arena_p001mx2_screen -Stage screen -Action Run
```
```powershell
# 3) 클러스터 판독 + 규칙 R1–R5
.venv\Scripts\python.exe o_tools\arena_report.py state\agent_experiments\arena_p001mx2_screen configs\validation\live_weighted_arena_v1_p001mx2.json
```
- confirm/final은 `-Stage confirm -Out state\agent_experiments\arena_p001mx2_confirm`, `-Stage final -Out ...\arena_p001mx2_final`로 같은 순서(Check → Run → report).
- 실행 조건: 다른 캠페인/`o_tools` 파이썬 프로세스가 돌고 있으면 runner가 시작을 거부한다(전역 launch lock). 중단·실패 시 결과는 `jobs/<match_id>/result.json`에 보존되고 재실행 시 cached로 건너뛴다.
- 예상 시간: 게임당 30–60초(Kaggle 로더 서브프로세스, 16코어) × 320 / 8 워커 ≈ 20–40분. 정확한 ETA는 runner 표시를 따른다.

## 4. 주의와 한계
- runner는 상점 시퀀스를 핀 고정하지 않는다(엔진 RNG가 행동에 따라 다르게 소비됨) → 같은 seed라도 두 모델의 세계가 갈릴 수 있어 페어드 분산이 핀 고정 도구보다 크다. 그래서 단계별 seed 수와 CI를 그대로 따르고, 핀 고정 결과(`reports/o-p001-mx2-evidence-2026-09-18.ko.md`)는 별도 근거로 둔다.
- arena 상대 10종은 현재 라이브 인구의 주류 빌드("B13/S8·S9" = 공개 노트북 테이프 라우터, `reports/o-live-source-trace-2026-09-18.ko.md`)를 포함하지 않는다: Tschinkel router v5(라이브 720스텝 재현 검증, `state/o_dev/datasets/donor_agents/agents/tschinkel-router-v5.py`)와 fieldbook 계보(합 34%)가 v1에 없음 → arena 통과가 곧 라이브 인구 승률을 뜻하지 않는다. v1 설정은 이번 arena가 끝날 때까지 바꾸지 않고, 추가는 v2 설정 파일로 한다.
- 실행 전 남은 확인 2건(이번 작업에서는 시뮬레이션을 돌리지 않아 미실행): (a) `agent/p001_mx2.py` vs `agent/p000_planner.py`+`PROXY_KNOBS=sw_mx2=1` 1경기 비트 동일성, (b) 동결 파라미터(tc 1/same .5)로 o227·V46·K0006 hold/fresh 재측정(약 2분). 둘 다 arena 실행 전에 하는 것을 권장하되 결과 해석 규칙은 위 R1–R5 그대로다.
