# c370–c371: 최신 메타 확인과 자원 지출 절약

최종 판정: c371이 사전 screen·confirm 기준을 통과해 Kaggle **56444327**로 제출됐다(2026-09-22 07:04 KST 업로드, 최초 확인 PENDING). Public League agent224에도 등록했다. c370은 개발 부품으로 보존하며 별도 제출하지 않았다. 신규 전략 연구는 위임 원칙대로 제출 후 잠시 중지한다.

## 재개 전 확인

2026-09-22 KST 조회 스냅샷에서 로컬은 V56(agent216) BT2693/1286경기, c369(agent210) 2659/1116, seed-leak(agent219) 2645/1302, c368(agent209) 2616/1116 순이었다. 새 수집본에는 V55/V56, Yummers 갱신, Fieldcraft, seed-leak, race-horizon 변경, Frontier 갱신 등이 있다. 제목의 공개 승률을 재현된 사실로 간주하지 않고 소스와 현재 전적을 읽었다. `state/c370/latest/`에 원자료를 저장했다.

- [V56](https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer): 남은 파종 기회에 맞춘 씨앗 예산과 불필요한 시비 생략. 씨앗 예산은 c368과 문제의식이 겹치며 별도 신규 아이디어라고 세지 않는다. 시비 생략층만 이번 조합에 사용한다.
- [Seed leak](https://www.kaggle.com/code/busyaprime/92-vs-the-best-public-farm-a-seed-leak-in-v54): 말기 씨앗·마지막 날 비료 구매 절약. 공개 92% 수치는 주로 같은 부모 상대이고 평균 마진은 작다.
- [V54 fork](https://www.kaggle.com/code/busyaprime/v54-fork-wins-72-5-head-to-head-against-v54): race horizon을 늘린 변형. 저자도 다른 상대 회귀와 더 긴 horizon에 대한 취약성을 밝힌다.
- [Clone Race Horizon](https://www.kaggle.com/code/nihilisticneuralnet/kaggriculture-clone-race-horizon): 실행 소스는 V56 대비 horizon41→48 및 주석 변경. 수집 직후 League 0경기라 강자 확정 없이 새 평가 상대에 포함한다.

실전 조회 시 c368 제출56432202는 66승22패/2734.6, 사용자가 제출한 c369 56435115는 72승16패/2454.7이었다. 평균 상대 갱신점수는2374/2098이고 공통 상대 submission은0개였다. c368은 경기 전2600–2800 상대33승17패, c369는 이 대역 표본0이며2400–2600에서19승9패다. 따라서 두 제출의 승률이나 현재 점수만으로 후보 간 강도 차이를 추정하지 않는다. 각 제출 최근 패배2개를 기존 live_replay_audit로 재생해719호출 전부와 양측 현금 일치를 확인했다. 4경기의 일치는 전체 제출의 무오류 증명이 아니다.

로컬 직접전도 c368–c369 6세계12경기 전부 무승부다. c369–V56은4세계7승1패, c368–V56은5세계4승6패이나 서로 다른 세계여서 paired 개선 증거가 아니다. c369의 이전 독립 screen 발동0/변화0 판정은 그대로 보존한다.

## 구현과 개발 QA

c370은 c368에 V54의 V219SKIP만 이식했다. d19/21/23에 기존 토마토가 모두 전날 급수되어 미급수연속0일 때 유지급수용 추가고용을 생략한다. 공식 엔진은 미급수2연속 refresh에서 고사하며 d18 식재 토마토의 첫 생산 refresh는d25 종료다. 공개 donor의 날짜와 조건은 변경하지 않았다.

3개 개발세계 양좌석 부모/OFF/ON 18경기에서 OFF6/6 행동·최종상태 동일. 발동세계1579215803에서는 토마토80u를 유지하고 고용비521 감소, 밀+12u·딸기+2u, own+573~576·마진+531~536이었다. 비료 구매는326 증가해 고용절약을 순현금 효과로 혼동하지 않는다. 나머지2세계는 무발동이다.

c371은 c369에 같은 유지급수 생략과 V56 EXP410 시비 생략을 결합했다. 이미 비료가day+2까지 유효하거나, 관측 타일과 고정 방문계획으로 계산한 수확량이 추가 시비 전후 같을 때만 시비를 생략한다. 다른 일꾼의 같은 턴 행동을 순서대로 적용하며 미확정 반응형 작업자는 계획 수확조건에서 제외한다. `_ca_visits`, `_ca_yield_path`, `_v219_native_day`는 donor와 부모의 AST가 동일하다. 역사적 base15의 날짜 일괄 시비 생략, c334 추가고용 투자와 다른 조건이며 그 결과를 취소하지 않는다.

- 부모 c369 SHA: `e3bc73c98b2ea83f7635653d43c8ed94a2aa118ce6be614a87dca5da841d2682`.
- c371 SHA: `e23cc84b4b801a40f92e209f43e5c9ad18e825e54dd6ed5527ea8f57b1cef12e`.
- donor V54 `5fbb75c9...`, V56 `a1ad0fd1...`. 출처·기존 Apache notices 보존.
- 별도 OFF6/6 행동·최종상태 동일, native QA18 정상.
- 부모/급수부품/조합3가지의 개발3세계 양좌석18원장: 조합마진 +22 / +535~539 / +228, own +12 / +569~571 / −64. 토마토 보존, 밀 불변 또는+12, 딸기+2~4; 시비생략3~4·처리오류0. 모든 세계 own 개선을 주장하지 않는다.
- c370/c371 단일main.py tar를 기존 package_agent로 생성하고 readback SHA를 확인했다. 전체 archive SHA는 각 `state/c370/manifest.json`, `state/c371/manifest.json`에 저장했다.

## 사전 검증 계약

`configs/validation/c371_resource_budget_v1.json`: 6workers, 최신8실행소스, c368/c369/c371, 새8세계 screen384경기→통과 시16세계 confirm768경기. 세계 단위 bootstrap, 양좌석을 독립표본으로 세지 않는다. 소스별 동일 가중이지만 같은 계보가 많아 독립8전략군을 의미하지 않는다.

primary c371−c369: screen 승점/own/마진>0, confirm 승점≥3%p·own/마진>0·98.5%세계CI하한>0, 두 단계 모두 각 상대 승점회귀≥−12.5%p. 추가로 c368 대비 전체승점/own/마진 비음수를 요구한다. 건강성 실패0, 원본해시 일치가 필요하다. 미달 시 로컬 보류하며 결과 합산이나 시드 추가로 구제하지 않는다. 사용자 지시대로32세계final 생략; schema의 final2예비시드는 실행하지 않는다. blind7240–7255 미사용.

기존 c300_execution_audit, pair_trace, live_episodes, fetch_current_elite, live_replay_audit, validation_v2, research_ops, package_agent를 재사용했다. 새 runner·crawler를 만들지 않았다.

## 실행 포장 보완

첫 screen v1은 Fieldcraft의 mirror_plan.py가 연구러너 단일소스 snapshot에 빠져중단됐다. 원본 agent 오류가 아니다. 모든 상대 artifact_files를 재확인했고 Fieldcraft만 실행 helper가 필요했다. 기존 c300 modular/bundle 감사형식으로 helper의 독립 namespace를 보존하고 import를연결한번들을 만들었다. 2개발세계 양좌석4/4 전체행동/최종상태가원본과동일했다. v1부분강도는미판독·원본보존, v1b는이상대포장만교정하고후보/시드/판정기준/6workers불변이다.

## 큰 실전 패배의 추가 관찰

기존 elite_profile의 리플레이 상태 읽기로 최악 패배 2건을 추가 확인했다(정확 거래 원장이나 인과 절제가 아니다). c368 ep111675950/ra5anchor는d6경제·축군이거의같고d12현금은우리+5964였지만상대딸기가d12 43대33,d18 53대33이며최종−17864였다. c369 ep111690506/redblackbst는d12우리+2723,축군동일8C9S였지만d18토마토14대10,최종−4855였다. 생산규모·운영일정차가관찰되며이번비용절약만으로해결한다고주장하지않는다. 단일상대/세계와실전녹음으로확장투자수익성을단정하지않고,후속과제라면과거추가토지/딸기투자기각과새상점/부모조건을대조해야한다. 원자료 state/c370/latest/worst-{profiles,compact}.json.

## 독립 screen 완료

v1b384/384, hashPASS·health0·max0.761초. 부모c369/c368 각62W46L20T, c37192W27L9T. primary승점+19.1406%p(99%세계bootstrap3.125~42.96875), own+171.20/margin+244.58, W→L0/T→L0. 전8상대승점비음수여서 사전screen PASS. 절대직접전은V56 12W4L, clone horizon6W9L1T로모든최신공개모델압도는아니다. 같은소스/기준으로confirm16새세계768경기진입.

첫 screen 효과범위: 128paired조건중80행동변경,5/8세계활성·세계평균마진모두비음수. 개별조건2개 own음수(최저−82),2개마진음수(최저−12). 유지급수생략96일·시비생략272회·telemetry오류0; Y축종층은이번8세계발동0. 개선을확인되지않은축종효과로귀속하지않는다.

## 독립 confirm과 제출

confirm768/768, hashPASS·health0·max0.868초. c369/c368 각143승73패40무에서 c371205승47패4무로 개선됐다. c369 대비 승점+17.1875%p,98.5%세계bootstrap[3.90625,32.8125]%p, own+192.12·마진+265.63. 승→패0,무→패8이므로 무회귀라고 부르지 않는다. 전8상대의 평균 승점변화는 비음수로 사전gate PASS; c368 대비도 같은 aggregate 개선이다.

| 독립 확인 상대 | c371 승–패–무 | 평균 마진 |
|---|---:|---:|
| c368 | 22–8–2 | +218 |
| c369 | 22–8–2 | +218 |
| V56 | 26–6–0 | +670 |
| Clone Race Horizon | 26–6–0 | +640 |
| Seed leak | 26–6–0 | +768 |
| Fieldcraft | 31–1–0 | +3760 |
| V54 | 26–6–0 | +875 |
| Yummers 새판 | 26–6–0 | +875 |

각32경기는16독립세계×양좌석이다. 화면 BT와 별개로 고정 common-panel의 paired 개선을 확인한 것이며 private 1위·현재 실전 우세의 증명은 아니다. screen에서 Clone Race Horizon에6–9–1이었던 점도 보존하며 confirm만 골라 무패/압도라고 말하지 않는다. 같은 계보·부모를 여러 실행소스로 포함한 대표성 한계도 남는다.

완료1152경기(384+768)를 판정에 사용했다. Fieldcraft 포장실패 v1부분은 제외, 32세계final은 사용자 지시대로 미실행·blind미사용. 제출전 단일main.py tar의 source/member/archive SHA를 다시 확인했다.

- 제출: [56444327](https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=56444327).
- 직접 업로드 파일: `H:\dev\kaggle-data\kaggriculture-strategy-meta\state\c371\c371_resource_budget_submission.tar.gz`.
- archive SHA: `548260def5759db53f7235f97b36d4212aa223e8629b9c84ad78d281b376f9be`.
- 접수기록: `state/c371/submission-receipt.json`; 등록기록: `state/c371/league-registration.json`; 상태복원: `state/c371/league-restored.json`.
- 자동수집3시간ON·일반연속대결8workers ON 복원. 공유 Kaggle Notebook에는 게시하지 않았다(사용자가 말한 등록대상은 로컬 Public League).
