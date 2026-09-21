# Public League 현재 버전 `no_source` 재감사

- 최종 갱신: 2026-09-21 16:33 KST
- 감사 범위: 현재판 `no_source` 85개 전체의 pulled notebook, 선언 dataset, 정적 압축 payload, 공개 notebook Output 파일 목록, 공식 loader 및 첫 행동 QA
- 결과: 실제 누락을 복구해 현재판 `no_source`는 **24개**로 감소했다.
- `no_source`는 이제 "현재 내려받을 수 있는 notebook/dataset/output에서 공식 행동을 내는 제출 artifact를 찾지 못함"을 뜻한다. 소스를 찾았지만 실행 QA가 실패한 항목은 `quarantine`으로 분리한다.

## 이번에 고친 수집 결함

- zlib/gzip/lzma + base85/a85/base64, 분할 literal/join, raw source map, base64 tar, nested payload map을 정적으로 복원한다.
- `%%writefile`/`%%agentfile`, `/kaggle/working/main.py`, 단독 `submission.py`와 `*_agent` direct cell을 후보로 인식한다.
- 선언 dataset을 size-check 후 내려받고, C++ source bundle은 Docker에서 `agent.so`로 빌드한다.
- pinned GitHub/Kaggle output recipe와 고정 GitHub release artifact를 복원한다.
- `kernels pull`에 없는 공개 notebook Output의 `main.py`, `submission.py`, submission tar 및 런타임 sidecar를 별도로 내려받는다. Notebook cell은 실행하지 않는다.
- Windows Kaggle CLI와 Docker subprocess에 UTF-8/무창 실행을 적용했다.
- QA는 임의 직접 호출 대신 공식 `env.run([source, "starter"])` 첫 행동 경로를 사용한다.

## 새로 복구한 대표 항목

- V14 Clone Preemption, Adaptive Shop Guard, Yummers, A Wonderful Life, Story of Seasons, Six-Day Fieldbook, Shop Router 0908, Shape the Shop, best version, Fieldbook Commit, V23 Adaptive Routes, Route Replay Agent, Kaggriculture 2820
- [No Cow Left Behind](https://www.kaggle.com/code/nathanjacob/no-cow-left-behind-v40-autopsy-fix): 공개 Output의 `submission.tar.gz`
- [FlyFarmer](https://www.kaggle.com/code/takamichitoda/flyfarmer-connectome-plays-kaggriculture): 공개 Output의 `main.py + brain_weights.npz`
- [Sovereign Swarm Kinematics](https://www.kaggle.com/code/taylorclark637/sovereign-swarm-kinematics-the): 공개 Output의 `submission.py`
- [Building a Kaggriculture AI Agent](https://www.kaggle.com/code/jek1wantaufik/building-a-kaggriculture-ai-agent): 공개 Output의 `submission.py`
- [Kaggriculture v66 Public Agent](https://www.kaggle.com/code/mohui666/kaggriculture-v66-public-agent): 고정 GitHub release의 13파일 artifact
- [Kaggriculture: Getting Started](https://www.kaggle.com/code/bovard/kaggriculture-getting-started): 단독 `submission.py`
- [Interactive P&L Analyzer & Arena](https://www.kaggle.com/code/haideptry/kaggriculture-interactive-p-l-analyzer-arena): `greedy_farmer_agent` direct cell

`pavloivanin/kaggriculture-baseline`은 `submission.py`를 찾았지만 공식 첫 행동이 `None`이어서 `no_source`가 아니라 `quarantine`이다.

## 최종 `no_source` — 점수 있는 항목부터

1. [Kaggriculture | What 2600+ Farms Do Differently](https://www.kaggle.com/code/georgymamarin/kaggriculture-what-2600-farms-do-differently) — 현재 표시 45.0 — replay 분석 notebook, 실행 agent/output 없음
2. [X-ray your agent](https://www.kaggle.com/code/destbreso/x-ray-your-agent) — 현재 표시 44.0 — live replay 분석 도구, 실행 agent/output 없음
3. [top10-replay-dataset-archive](https://www.kaggle.com/code/ashok205/top10-replay-dataset-archive) — 현재 표시 14.0 — replay dataset publisher; Output도 parquet/manifest뿐
4. [Kaggriculture: Can Specialists Beat One Agent?](https://www.kaggle.com/code/mansiaggarwal88/kaggriculture-can-specialists-beat-one-agent) — 현재 표시 14.0 — 분석 notebook, 제출 artifact 없음
5. [Every community agent, one arena](https://www.kaggle.com/code/destbreso/every-community-agent-one-arena) — 현재 표시 2.0 — 여러 donor를 소비하는 arena; 자체 단일 제출 agent 없음
6. [How Many Twins - Strategy Clustering Kaggriculture](https://www.kaggle.com/code/nathanjacob/how-many-twins-strategy-clustering-kaggriculture) — 현재 표시 2.0 — replay clustering 분석, Output은 그림뿐
7. [Agent telemetry | Catch what you lose](https://www.kaggle.com/code/destbreso/agent-telemetry-catch-what-you-lose) — 현재 표시 1.0 — 분석/진단 도구, Output은 `silent_leaks.py`뿐

## 최종 `no_source` — Kaggle 제출 점수 없음

8. [4000x environment speedup | Kaggriculture](https://www.kaggle.com/code/nikital7/4000x-environment-speedup-kaggriculture) — simulator/benchmark source만 있음
9. [A Macroeconomic X-Ray of the Kaggriculture Meta](https://www.kaggle.com/code/destbreso/a-macroeconomic-x-ray-of-the-kaggriculture-meta) — 분석 notebook
10. [Kagg Team Decisions](https://www.kaggle.com/code/anandkumar369o/kagg-team-decisions) — replay/team 분석 및 parquet Output
11. [Kaggriculture Dawn Ledger: Pareto Action Cards](https://www.kaggle.com/code/prvsiyan/kaggriculture-dawn-ledger-pareto-action-cards) — 진단/의사결정 문서
12. [Kaggriculture Market Ledger | Seasonal Counterplay](https://www.kaggle.com/code/prvsiyan/kaggriculture-market-ledger-seasonal-counterplay) — Output policy가 스스로 "competition action을 제출하지 않는다"고 명시
13. [Kaggriculture MetaCounter R1](https://www.kaggle.com/code/alperen5252525/kaggriculture-metacounter-r1) — pulled notebook에 실행 agent 없음; Kaggle Output API는 현재 403이라 **외부 Output 유무는 확인 불가**
14. [Kaggriculture Route Ab Timing Lab 20260921](https://www.kaggle.com/code/prvsiyan/kaggriculture-route-ab-timing-lab-20260921) — 실험/분석 notebook
15. [Kaggriculture Unlocked: A Beginner's Guide](https://www.kaggle.com/code/mhmda81/kaggriculture-unlocked-a-beginner-s-guide) — replay 교육 notebook
16. [Kaggriculture Visible-Price Switch Lab](https://www.kaggle.com/code/prvsiyan/kaggriculture-visible-price-switch-lab) — 실험/분석 notebook
17. [Kaggriculture Weatherboard: Route Regime Switches](https://www.kaggle.com/code/prvsiyan/kaggriculture-weatherboard-route-regime-switches) — 실험/분석 notebook
18. [Kaggriculture: The Win-Rate Illusion](https://www.kaggle.com/code/prvsiyan/kaggriculture-the-win-rate-illusion) — 평가 방법 설명; 예시 문자열만 있고 제출 artifact 없음
19. [Kaggriculture: What the Top Farms Do — a Live Meta](https://www.kaggle.com/code/cjlcjlcjl/kaggriculture-what-the-top-farms-do-a-live-meta) — replay/live meta 분석
20. [The Farm Day as a Routing Problem](https://www.kaggle.com/code/destbreso/the-farm-day-as-a-routing-problem) — routing 분석 notebook
21. [notebook868efb1104](https://www.kaggle.com/code/hanialsh/notebook868efb1104) — Kaggle 기본 template, 실행 agent 없음
22. [Kaggriculture Trajectory Engine](https://www.kaggle.com/code/datascikhan/kaggriculture-trajectory-engine) — replay feature/trajectory 분석
23. [Kaggriculture Data Quality Check](https://www.kaggle.com/code/mhmda81/kaggriculture-data-quality-check) — replay dataset 품질 검사
24. [AgriSim Deep Dive](https://www.kaggle.com/code/datascikhan/agrisim-deep-dive) — replay 분석; `parse_agent_actions`는 parser이고 제출 agent가 아님

## 증거 한계

- 24개 중 23개는 pulled code, 선언 dataset, 공개 Output까지 확인했고 제출 가능한 agent가 없었다.
- MetaCounter R1 한 개는 로컬에 받은 notebook 자체에는 agent가 없지만 공개 Output API가 403이므로, 작성자가 별도 Output을 공개했는지는 확정할 수 없다. 접근이 가능해지면 자동 수집기가 다시 확인할 수 있다.
- `no_source`는 전략 아이디어가 없다는 뜻이 아니다. 리그에서 실행할 정확한 제출 artifact가 없다는 뜻이다.
