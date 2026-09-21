# c365 — CARROT2 사료 예비기간 2일→1일

판정: **일관된 양수 효과를 확인했지만 사전 final 통계 기준은 미달했다. 사용자가 이 한계를 확인한 뒤 live validation 제출을 명시해 제출했다.** c365는 Public League 후보로도 계속 비교한다. 보호 blind 7240–7255는 사용하지 않았다.

## 이력과 재시도 근거

- c320의 후기 당근 부품은 own +166, margin +199, 승점 변화0이었다. 전체 선행 전환이 음수라 승격되지 않았다.
- c321의 고정 생산 프로필 5종은 기회비용을 포함한 native 평가에서 모두 음수였다.
- c359의 임시 밀 1u 추가 성숙은 승점 +1.5625%p, own +21, margin +22였으나 신뢰구간이 0을 포함했다.
- c361의 V54 본체 전체 이식은 fresh confirm에서 own/margin이 음수이고 W→L 20건이라 기각됐다.

`tools/crop_lane_trace.py`로 c358과 One More Wheat를 같은 8세계·양좌석에서 추적했다. c358의 깊은 CARROT2 본체는 `_CA_FEED_DAYS=2`, One More Wheat·Metav4·V54·Pipe16은 1이었다. seed 1056137939에서 c358은 `ca_feed_block=10`, One More Wheat는 0이었고, seed 1177892056에서는 9 대 4였다. 같은 step의 보유 밀과 가격이 같아도 c358만 2일 예비 조건 때문에 밀을 다시 심었다. c359의 추가 밀 1u는 차단 수를 줄이지 못했다.

c365는 c358의 개막·시장 스택·경로를 그대로 보존하고 이 상수만 1로 바꾼다. 새 생산 프로필, 전체 V54 이식, 가격 임계값 재튜닝이 아니다. 후보 SHA-256은 `d48e66c3c5aec21a55be8101d7544278d5303fc6a1b1a487d9a2df055c82e72f`다.

## QA와 원장

- 비활성 래퍼는 c358과 4/4 양측 행동·현금 동일.
- 이미 원인 분석에 쓴 두 세계에서 활성 c365는 `ca_feed_block`을 9→0, 8→4로 줄이고 성공한 당근 식재를 각 4칸 늘렸다.
- 동일 세계 원장 평균: 당근 수확 +16u, 밀 수확 −20u, 당근 씨앗비 +100, 밀 씨앗비 −50, 사료 구매비 변화0, 일말 미급식 동물 수 변화0.
- 한 세계에서 성공한 FEED 2회·CARE 1회가 줄었으나 일말 미급식 수는 늘지 않았다. 두 세계 own/margin은 모두 양수였다. 이는 개발 사례라 승격 증거로 세지 않았다.

## 동결 검증

현재 강한 공개/우리 8개 source family, 양좌석, native reacting, 8워커로 실행했다. 후보·상대·엔진·설정 해시는 각 캠페인에서 고정됐다.

- screen 256/256 valid: 승점 +1.5625%p, own +177.2, margin +89.6, W→L 0, 99% seed CI `[0,+6.25]%p`.
- confirm 256/256 valid: 승점 +10.15625%p, own +61.0, margin +850.6, W→L 0, CI `[0,+28.125]%p`. 효과는 8 seed 중 2개에 집중됐다.
- final 512/512 valid: 승점 +3.125%p, own +182.2, margin +143.0, W→L 0, CI `[0,+12.5]%p`.
- 세 단계 합산 1,024경기: seed 32개, 승점 +4.4921875%p, own +150.6, margin +306.6, L→W 23, W→L 0. 행동 변경 160/512 paired 조건. 승점 개선 seed 4, 악화 seed 0, 무변화 seed 28. 사전 고정 99% 군집 bootstrap 구간은 `[0,+11.9140625]%p`.
- 모든 완료 캠페인은 invalid 0, 내부 오류0. 최대 후보 결정 0.835초, 최대 상대 결정 0.998초.

첫 screen 폴더 `c365_feed_reserve_screen_v1`은 전략 판정 전에 c358 기준선 한 결정이 1.124초를 기록해 중단됐다. 같은 계약의 새 폴더 v1b에서는 256/256 valid, c358 최대0.803초였다. 실패 폴더와 invalid 결과는 보존했다. 이 실행 오류를 성능 결과로 세지 않았다.

## 결론

세 단계 모두 point/own/margin이 양수이고 W→L가 한 건도 없어 유망하다. 그러나 작동 세계가 드물고, 사전 final 기준은 **세 단계 합산 99% seed-cluster CI 하한 >0**이었다. 실제 하한은 0이므로 통계 gate 자체는 FAIL로 보존한다. 이후 사용자가 결과를 검토하고 live validation 제출을 명시해 c365를 제출했다. 이는 사전 gate 통과로 재해석하지 않는다.

## 제출 기록

- 후보 원본: `agent/c365_feed_reserve.py`, SHA-256 `d48e66c3c5aec21a55be8101d7544278d5303fc6a1b1a487d9a2df055c82e72f`, 821,363 bytes.
- 제출 패키지: `state/c365/c365_feed_reserve_submission.tar.gz`, SHA-256 `752d5d1bdb983ca69643c6943f7232895ed2ca5660962dc72e37b34b83ad4cb0`, 663,952 bytes.
- 패키지 재읽기: 멤버는 `main.py` 하나이며 SHA-256이 후보 원본과 일치한다.
- Kaggle submission ID: `56407947`. `SubmissionStatus.COMPLETE`를 확인했으며 초기 표시 점수는 `1156.7`이다. 초기 대진 수가 적은 시점 값이므로 강도 판정에는 사용하지 않는다.
- 제출 설명: `c365 CARROT2 feed reserve 2->1: 1024 valid vs c358, +4.49pp, +307 margin, L->W23/W->L0; exact d48e66c3`.

산출물: `agent/c365_feed_reserve.py`, `tools/build_c365_feed_reserve.py`, `tools/crop_lane_trace.py`, `configs/validation/c365_feed_reserve_{qa,public_v1}.json`, `state/c365/`, `state/agent_experiments/c365_feed_reserve_*`.
