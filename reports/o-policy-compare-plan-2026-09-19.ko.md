# 완성 운영 정책 3종 공통 패널 비교 — 실행 전 고정 계획 (2026-09-19 04:55)

목적: base19 · V46 exact · router v5를 **우리 좌석에서 실행되는 후보**로 같은 세계·같은 reacting 상대·양 좌석에서 비교하고, 다음 개발 부모를 고른다. 전략 수정 없음. 종료된 라인(V46 분기 공격, p002, p003) 재개 없음, MX2 보류, 챔피언 base19, blind 7240–7255 보호.

## 1. 정책 (원본 그대로, 어댑터 없음)

| 라벨 | 파일 | sha256 | 실행 확인 |
|---|---|---|---|
| base19-planner | `state/o_dev/p000_base19.py` | 53d80342…f31290 | 챔피언(정식 러너 후보 2,432경기) |
| v46-exact | `state/o_dev/v46_public.py` | 735c3703…acedb6 | 라이브 ep 110208980 720/720 재현; 정식 러너에서 상대로 1,024경기 실행(오류 키 0, 결정 p99 7ms) |
| tschinkel-router-v5 | `state/o_dev/datasets/donor_agents/agents/tschinkel-router-v5.py` | b87a27ed…f8522 | 라이브 ep 110295006 720/720 재현(`o_results/rival_source_trace.json` verify); 정식 러너에서 상대로 384경기 실행 |

두 대체 정책은 단일 파일이고 러너의 로더(마지막 callable = `agent`)로 상대 좌석에서 이미 실행됐으므로 **어댑터가 필요 없다** — 후보 좌석에서도 같은 스냅샷(`sources/<sha>.py`)을 같은 방식으로 로드한다. 원본 파일은 수정하지 않는다. router v5는 telemetry를 내보내지 않는다(건전성 규칙은 오류 키·1초 초과만 본다). 엔진 kaggle-environments 1.32.7, 설정·러너·contract 해시는 manifest와 `o_tools/arena_hashcheck.py`로 기록.

## 2. 공통 reacting 패널 (실행 전 고정)

기존 arena v1c·lineage panel v1의 상대 소스를 재사용한다(전부 정식 러너에서 정상 실행 이력). **세 후보의 소스 자체는 패널에서 제외**(자기 대전은 §5의 별도 진단). frozen·절제 래퍼 없음.

| 상대 | family(주통계 동일 가중 1/8) | arena 클러스터(설명용) | 후보와의 계보 관계(표시) |
|---|---|---|---|
| nagata-scheduler | nagata_scheduler | cluster1 elite | — |
| dmitrii-lb2700(단일 파일 번들, 행동 동일 확인됨) | dmitrii_market | cluster1 elite | — |
| jaxa-k0006 | jaxa_microstructure | cluster2 hard fork | — |
| v48-fast-climber | ahmed_v3x_v4x | cluster3 | **V46 동일 저자 계보** |
| v37-more-yield | ahmed_v3x_v4x | cluster4 fragile | V46 동일 저자 계보 |
| ahmed-v38 | ahmed_v3x_v4x | cluster4 fragile | V46 동일 저자 계보 |
| shop-router-v5(yhay81) | yhay81_shop_router | cluster3 | — |
| tschinkel-state-router-v31 | router_tschinkel | 라이브 계보 | **router v5 동일 저자 계보(다른 버전)** |
| boatlee-v29-roundtrip | roundtrip_n | 라이브 계보 | — |
| prvsiyan-wheat-q45 | roundtrip_n | 라이브 계보 | — |
| c129-benchmark | historical_anchor | cluster5 | (우리 과거 tape) |
| o227-stealth(telemetry 키 개명 래퍼, 행동 동일 확인됨) | historical_anchor | cluster5 | (우리 과거 tape) |

가중: 주통계는 러너 규칙대로 **family 동일 가중**(8 family × 12.5%; 같은 저자 계보의 여러 버전은 한 family로 묶어 합계 12.5%). arena 클러스터 가중(0.35/0.30/0.15/0.10/0.10)은 설명용으로 병기. 후보의 동일 저자 계보 상대가 포함된 셀은 결과표에 표시하고, 그 family를 뺀 민감도도 병기한다(제외하지 않음).

## 3. 캠페인 구조

설정 `configs/validation/policy_compare_v1.json`(정식 러너 v1, 8워커, timeout 240s). 시드는 `random.Random(20260919)`로 새로 뽑아 기존 모든 설정·개발(7000–7031)·blind와 겹치지 않음을 확인.

| 단계 | 시드 8/8/16 | 경기 수(3정책 × 12상대 × 2좌석) | 용도 |
|---|---|---|---|
| screen | 1360408755, 211221630, 1731695924, 753666044, 299387588, 1692877162, 1406320235, 1607321654 | 576 | **개발 평가**(이 단계로 §4 판정) |
| confirm | 2123141811, 1750783264, 1645646950, 727065759, 863774942, 1546655756, 1203423100, 601752748 | 576 | 우세 정책 또는 조건부 규칙의 **별도 확인** |
| final | 16개(설정 파일) | 1,152 | p004가 생길 때의 넓은 검증(이번 과제에서 실행하지 않음) |

주 비교(primary 2개, Bonferroni): v46-exact vs base19, tschinkel-router-v5 vs base19. 한 번에 한 캠페인만 실행, 정식 러너 8워커 고정.

## 4. 판정 규칙 (결과 보기 전 고정)

각 primary 비교 P(정책) vs base19에 대해 screen에서:

- **P1 주신호**: 러너 family 가중 승점 차이의 bootstrap CI가 0을 넘음(`positive`; alpha .01/2).
- **P2 폭(계보 붕괴 은폐 금지)**: 8 family 중 ≥6에서 paired 승점 차이 ≥ 0 이고, 어떤 family에서도 승점 차이 ≤ −0.25 가 없음.
- **P3 전환**: 합산 L→W − W→L > 0.
- **P4 건전성**: 무효·timeout·오류 키·1초 초과 0, 두 좌석 모두 승점 차이 ≥ 0.
- **P5 현금 비기준**: own cash 차이는 보고만 한다. 승률이 오르지 않으면 현금이 높아도 우세가 아니다. 세계가 다른 경기의 평균 현금은 비교하지 않는다.

결정:
- (a) 어느 P가 **P1–P4 전부 통과** → "폭넓게 우세(개발)". confirm(새 시드 8개)에서 P1(alpha .015/2)·P2·P4 재통과 시 **"대체 부모의 우세가 별도 확인에서도 유지됨"** → 그 정책이 새 개발 부모 후보. p004 = 그 정책의 실행 가능 동결 후보(원본 그대로 + manifest) → final(넓은 검증) → blind → QA → 소유자 제출. base19에 기능 이식 없음. 둘 다 통과하면 family 가중 승점 차이가 큰 쪽.
- (b) 통과 정책이 없고 **강한 조건이 갈릴 때**(어떤 family 또는 세계 구성에서 P의 승점 차이 ≥ +0.25 이면서 다른 family/세계 구성에서 ≤ −0.25): §6 절차로 조건부 선택을 조사. 조사에서 회수 여지가 확인되지 않으면 라우터를 만들지 않는다.
- (c) 그 외 → **base19 유지**, 대체 정책 채택 근거 없음으로 기록.

"planner가 낫다/tape가 낫다"로 결론 내리지 않는다. 결론은 정책 파일 단위.

## 5. 별도 진단 (주평가 밖, 설명용)

- **자기 대전·상호 대전** `configs/validation/policy_h2h_v1.json`: 같은 세 정책을 상대 좌석에도 두어 3×3 셀(자기 대전 3 + 교차 6) × 2좌석 × screen 시드 8 = 144경기. 주평가와 겹치지 않게 screen 종료 후 실행. 주 지표에 넣지 않는다.
- **복제·유사도 감지 발동 표시**: 후보/상대 telemetry의 `race_mirror`, `race_clone_turns`, `race_horizon_turns`, `race_lost_races`, `probe_matches`, `three_turn_calls`, `probe_four_turn_calls`(V46·v48 계열), o227 래퍼의 race 키 > 0 인 경기는 결과표에 표시한다(제외하지 않음).
- 기존 관측(7000–7031 고정 상점 세계, 절제 상한)은 개발 자료로만 인용.

## 6. 조건부 선택 조사 절차 (결정 (b)일 때만)

1. **상한 먼저**: screen 자료에서 (시드, 좌석, 상대)별 세 정책 중 사후 최선을 고른 승점 − 최선 단일 정책 승점 = oracle 이득. 이득 < +0.05 승점(5%p)이면 조사 종료(회수 여지 없음).
2. **관측 정보만**: 규칙 입력은 결정 시점에 보이는 것만 — 경기 시작(step 0: 아무 정보 없음) 또는 step 1(상대의 step‑0 시장 서명 = 상대 현금·시장 재고 변화)까지. 상점(d3 이후 공개)·미래 가격·seed·상대 이름·submission ID 사용 금지. 중간 교체(내부 상태 이식) 금지.
3. **분리**: 규칙은 screen 시드(양 좌석 포함)에서만 만들고 confirm 시드에서 평가. 같은 세계가 양쪽에 들어가지 않는다.
4. 규칙이 confirm에서 oracle 이득의 유의미한 부분을 회수하고 P2·P4를 만족할 때만 "관측 가능한 조건부 선택이 별도 확인에서도 개선됨".

**Macro Oracle(09-17)과의 차이**: 그때는 한 정책(planner) 내부의 d6+ 분기(축군·딸기·토지 시점 등)를 사후 선택했고 순수 전략 여지 ≈ +0.6k(n.s.)였다. 이번은 서로 다른 완성 정책 전체를 같은 세계·상대에서 비교하며, 선택 시점은 경기 시작(또는 step 1의 상대 서명)뿐이고, 회수 가능성은 oracle 상한과 관측 규칙의 confirm 성적으로 판단한다.

## 7. 보고 항목

정책별 승률과 CI(러너 bootstrap), 상대별·family별 승패, base19 대비 paired 마진·own·승점 차이와 W→L/L→W, 큰 손실(마진 < −10k) 목록과 family 회귀, 세계 구성별(최종 상점열 지표: YARN≥2 / 우유상점≥3 / 딸기상점≥3 / 피자·농산물≥3 / PET≥2) 결과, 실행 오류·timeout·결정 시간·행동 건전성. 도구: `tools/validation_stats_v1.py`(러너 내장), `o_tools/arena_report.py`(P 규칙 판독·세계 구성 절 추가), `o_tools/arena_hashcheck.py`.

## 부록 A (06:30, 실행 전 고정) — v2: V47·V48 추가 비교와 5정책 상호 대전

- 근거: 라이브 대조(결과 보고서 §6–7)에서 V46 exact의 정체 원인이 같은 저자 계보의 후속 버전(V47 공개 점수 2,686; V48 정확 사본 6개가 2435–2600에서 상승 중)임이 확인됨. 두 소스는 공개 노트북(Apache-2.0)에서 노트북 내장 digest로 복원(`state/o_dev/v47_public.py` f4ecd487…, `state/o_dev/v48_clearqueue_public.py` 4b540288…), 러너 로더에서 양 좌석 정상 실행(오류 키 0, 최대 결정 0.1s).
- `configs/validation/policy_compare_v2.json`: 같은 12상대 패널·같은 단계 시드(base19/V46 셀은 v1과 동일 재현). 후보 base19 · V46 · V47 · V48(router v5 제외). 주 비교 **V47 vs V46, V48 vs V47**(규칙 P1–P5 동일, α .01/2); base19 대비는 설명용. 질문: 패널이 상위에서 여전히 갈리는가(V48 > V47 > V46), 아니면 포화(.9대 동률)인가.
- `configs/validation/policy_h2h_v2.json`(진단, 주 지표 아님): base19 · V46 · V47 · V48 · **우리 tape 라인 o239_50**(단일 파일, 라이브 2,660~2,754)을 후보이자 상대로 5×5×2좌석×8시드 = 400경기. 자기 대전 셀은 거울. 목적: 라이브에서 검증된 강한 정책들 사이의 로컬 순서와 우리 tape 라인의 위치.
- 판정 활용: (i) 패널이 포화면 "패널로는 상위 부모를 못 고른다"고 기록하고 다음은 패널 v2(라이브 강자 실행 상대 추가) 설계. (ii) 패널이 갈리고 V48이 P1–P4를 통과하면 V48이 개발 부모 후보(V46 대체), 단 라이브 순위(우리 tape ≥ V47/V48)와 함께 소유자에게 보고. 어느 경우도 제출 후보로 승격하지 않음(blind 미사용).
