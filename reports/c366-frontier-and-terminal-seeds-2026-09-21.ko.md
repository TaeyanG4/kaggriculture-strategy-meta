# c366 이후 — 공개 부모 비교·실전 감사·시즌말 씨앗 예비

현재 부모는 c365다. 확실한 개선 후보가 독립 검증을 통과할 때만 제출한다. 아래의 표본은 현재 공개 정책 패널에 대한 증거이며 비공개 상위권이나 미래 리더보드 순위를 보증하지 않는다. 작업 상태는 HANDOFF.md가 기준이다.

## c366: 공개 부모 교체 screen — 기각

Public League의 상위20 부분 순위는 공통 상대·동일 세계 비교가 아니므로 그 순서만으로 부모를 바꾸지 않았다. c365, Moon147, Wheat142를 8개 실행 소스·새 8세계·양 좌석에서 비교했다. 소스별 동일 가중이며 계보가 겹쳐 8개 독립 전략군이라고 해석하지 않는다.

- 12-worker v1은 상대 Local Best 한 결정 1.048초로 실행 계약 중단. 공식 DONE/오류0였으나 고정한 로컬 health gate를 완화하지 않았다. 중단 기록 보존 후 같은 정책·시드의 별도 8-worker v1b로 재실행했다.
- v1b 384/384 완료, hash PASS, health 오류0, 최대 결정 0.982초.
- c365 99승27패2무/128.
- Moon147: 승점 +3.906%p, 마진 −400.5, own +568.4. c358 상대 −37.5%p, Local Best 상대 −50%p. screen 기준 실패.
- Wheat142: 승점 −1.563%p, 마진 −428.3, own +486.4. screen 기준 실패.
- 예약 confirm/final 미사용. 공개 후보는 기존 League에 남기고 제출하지 않았다.

계약: `configs/validation/c366_public_parent_challenge_v1{,b}.json`. 검증 판독: `state/c366/parent-screen-readout.json`.

## c365 실전: 실행 문제와 상대층을 분리

공개 episode 목록 당시 세 제출은 각각 56417606=47승13패, 56417592=52승3패, 56407947=75승1패였다. 뒤 두 제출의 상대 initial score는 모두2400 미만이었고 첫 제출만2400–2600에서22승12패를 기록했다. c358(56402500)은 더 높은 상대층의 경기가 많았다. 현재 표시 평점이나 세 사본의 전체 승률을 동일 모집단의 실력 비교로 합산하지 않는다.

최신 두 c365 제출의 최근 패배를 각각3개씩, 기존 `fetch_current_elite.py`에 선택적 `--public-only --outcome loss` 필터만 추가해 받았다. 정확한 공개 type은 `EPISODE_TYPE_PUBLIC`이다. 처음 임시 판독의 `PUBLIC` 필터는 빈 결과를 냈으며 해당 개별 scratch JSON은 증거에서 제외했다. 올바른 집계는 `state/c366/live-public-summary.json`이다.

- 기존 live replay audit: 6/6 모든 행동·양측 최종 현금 일치.
- 기존 replay accounting: 6/6 관측 재현, 현금 원장 잔차0.
- 네 작은 패배는 주로 판매 단가·시점 차이, 두 큰 패배는 생산 품목 구성 차이가 컸다.
- 마지막 창고는 모두 비어 있었다. 마지막 고용 일손이 하루 내내 생산 효과가 없는 경우도 없었다. 종료 재고 미판매나 공짜 고용 감축이 원인이라는 주장은 하지 않는다.

원자료: `o_replays/c366_live/`, `state/c366/live_accounting/`, `o_results/live_audit_{56417606,56417592}.json`.

## c367: adaptive_market 최종 자기판매 관측 — 정상 음수

가까운 선행 c327은 옛 v9 RACE 관측을 고쳤지만 실제 마진이 음수였다. 이번 것은 최종층 이전의 판매량을 쓰는 별도의 adaptive_market 소비자다. 공개 sale-advance 층이 이후 추가한 자기판매가 상대 압력으로 오인되는지를 감사했다.

정확 live 6경기의 12,942 품목·턴에서 기존 물리 투영 `_ov_fields`/`_r97_market_stock`은 엔진 판매량과 모두 일치했다. 중간층 자기판매 기록과 982건 차이가 있었으며 같은 관측의 그림자 계산에서3턴의 주문이 달라졌다. 수량 정확성은 순시장유입·정책 수익성의 증명이 아니다.

후보 `agent/c367_adaptive_observer.py`는 c365 본체·임계값·생산을 보존하고 최종 자기판매 기록만 덮어썼다. OFF 양좌석 전체 행동/최종상태 동일, ON native QA 정상.

- 새8세계×10source×양좌석×2모델=320/320, hash PASS, health0, 최대0.963초.
- c365137승7패16무 → c367135승19패6무.
- 승점 −4.375%p, 마진 −7.2, own −2.3, W→L2/T→L10.
- 사전 screen 실패. 확인·최종 미실행, 제출 안 함. 같은 압력 임계값 재튜닝 안 함.

별도 OR2 재고층 그림자 감사에서도 자기판매만 교정하면6경기 전체 재고 오차가 줄지 않았다. 이 변형은 후보를 만들지 않았다. 같은 턴 수확을 사료 예비로 인정하는 별도 진단도 실행 가능한 전체 정책으로 승격하지 않았다.

계약·판독: `configs/validation/c367_adaptive_observer_v1.json`, `state/c366/c367-screen-readout.json`, `adaptive-audit.json`, `or2-audit.json`.

## c368: terminal route의 씨앗 예비 상한 — 제출 완료

정확 live6경기 중4경기가 CARROT 씨앗8개($160)를 남기고 끝났다. CARROT2는 d27까지 보유 씨앗을8개로 계속 채우지만 step648 이후 chassis는 terminal route2를 사용하고 남은 WHEAT/CARROT PLANT 수가0으로 줄어든다.

가까운 선행 c307은 base19의 초기 구매 부족량 이중 차감을 고쳐 경제적으로 실패했고, c365는 급식 예비 일수를 줄였다. c368은 둘과 다른 범위로, **종료 구간의 남은 식재 명령 전체보다 큰 씨앗 예비**만 줄인다. 미래 상점·상대 행동·실현 가격을 쓰지 않는다.

- 부모 c365 그대로, c367 수정 포함 안 함.
- step648 이후 `_CA_BUFFER=min(8, 현재 턴 다음부터 남은 WHEAT+CARROT PLANT 수)`.
- 두 작물을 모두 세어 보수적인 상한으로 쓰며 식재/수확 명령을 직접 바꾸지 않는다. 실행 중 생산 보존은 별도 확인한다.
- OFF 양좌석 행동/최종상태 일치. 기존 개발세계의 ON native QA는 양좌석 모두 own+160, 상대 현금 불변.
- 계약 `configs/validation/c368_terminal_seed_budget_v1.json`: 독립8/16/32세계, 동일10source, 양좌석,8workers. screen/confirm은 양수 및 상대 회귀 제한; 독립 final은 CI하한>0·승점≥3%p·마진>0·상대별−12.5%p 미만 회귀 없음. 실패한 final을 pooled 결과로 구제하지 않는다.

후보 SHA `fed4a96fafe96a80a37ec480fcf12de8ded716517fd4226d2b0ed4bcaeeab1b0`. 검증용 단일 main.py tar.gz와 readback manifest는 `state/c368/`에 있다. Kaggle 제출 56432202 COMPLETE. blind7240–7255 미사용.

### c368 screen·confirm 완료

- screen320/320: 승점+15.625%p, 99%seed CI[+3.75,+41.25]%p, own/margin 전160조건+160, W→L0/T→L0.
- confirm640/640: 승점+7.50%p, 98.5%seed CI[+1.5625,+19.0625]%p, 평균own/margin+93, W→L0/T→L0, 최대결정0.989초.
- confirm 첫 실행은 재개 시 일반League가 켜져 CPU중복으로 결정1.002초·고정health실패, 부분성능미판독. API로리그중지·worker0 확인한 뒤 같은config/source/seeds의별도v1b로완주했다. 실패폴더보존,gate완화없음.
- 기존 crop_lane_trace를 재사용한 개발세계양좌석대조(부모/후보4실행): 양쪽1953개field event 전체동일, 기록된일손명령동일, own+160/rival0.
- 사용자 명시 지시로 final32세계1280게임을 중단·생략했다. 부분 결과는 확인하거나 성능 판정에 사용하지 않았다. 이는 final gate 통과가 아니며, 완료된 screen·confirm 결과로 제출했다. 중단 marker는 `state/agent_experiments/c368_final_v1/owner-cancellation.json`.
- 제출 56432202 COMPLETE, 후보 source/member SHA `fed4a96fafe96a80a37ec480fcf12de8ded716517fd4226d2b0ed4bcaeeab1b0`, archive SHA `762b41922410f728972725bba6f24f168c030f13c3b891481bf39b067ff7e9f3`. 파일은 `state/c368/c368_terminal_seed_budget_submission.tar.gz`, 접수·상태 기록은 `state/c368/submission-receipt.json`. 연구는 지시대로 잠시 중지한다.
- 판독 주의: research_ops의 `excluding_named_parent_descriptive`는 라벨만 비교하므로 `c365_direct`를 제외하지 못했다. 이 필드는 부모 제외 통계로 인용하지 않는다. 본문 전체 panel 통계 및 고정 gate에는 영향이 없다.
