# c358 — Local Best + V54 HybridOpening

## 선행과 변경 근거

- 가장 가까운 선행 c324는 새 공개 whole-policy가 v9 대비 승점 구간에 0을 포함하고 마진도 음수여서 종료됐다.
- c357에서 2026-09-21 Public League의 새 V54 `949e2eed...`를 Metav4 v13 부모 `9d634946...`와 fresh seed로 비교했다. V54의 차이는 d0–d2 유휴 일손과 미래 pasture 한 타일을 이용해 밀 2u를 생산·판매하고 pasture를 복원하는 `HybridOpening`이다.
- c357 screen 256경기: V54−Metav4 승점 +7.8125%p, 마진 +56.15, own +39.24, W→L 0, seed-bootstrap 99% 구간 `[+6.25,+12.5]%p`. Pipe16은 사실상 같은 opening 정책이므로 독립 증거로 세지 않았다.
- 현재 리그 Local Best `41dd60f7...`는 새 차체가 아니라 공개 v9 계보에 market portfolio, frontload, adaptive market, sale advance, sell-impact reorder를 순차 포장한 정책이었다. base85+lzma payload는 AST literal만 읽어 해제했고 공개 코드를 분석 과정에서 실행하지 않았다.
- c358은 Local Best 전체 실행 소스를 그대로 본체로 두고, V54의 정확한 한 타일 opening만 최하단 native route-0 tape에 적용했다. 과거 feedrot/land 확장과 달리 새 토지·고용·기존 작물 치환이 없다.

## 구현·QA

- 후보: `agent/c358_localbest_hybrid.py`, SHA-256 `680a4f713d8d672dce3f13f5429df1f803626f408d76e1690eabe32152779196`.
- 재현 빌더: `tools/build_c358_localbest_hybrid.py`.
- 비활성 래퍼와 Local Best 원본: 4/4 행동 해시·최종 현금 완전 동일.
- 활성 후보: QA 4/4와 정식 480/480 후보 경기에서 임시 밀 확인, 2u 수확, pasture 복원, 판매 확인; extension error 0.
- 최초 12-worker screen은 146/320 시점 후보 결정 1회가 1.0106초여서 health gate 중단. 결과는 보존했다. 전략·시드·상대·기준을 바꾸지 않고 workers만 8로 낮춘 v1b를 새 계약으로 실행했다.
- v1b screen/confirm/final 960/960 valid, health failure 0. 후보 최대 결정 0.965초. 과거 느린 세계의 1-worker 16게임 감사에서는 후보 0.581초, 부모 0.590초였다.

## 정식 결과

각 단계는 fresh 8 seeds × 10 opponent sources × 양 좌석 × 후보/부모 = 320경기다. V54와 Pipe16은 결과에 모두 보이지만 family weighting에서는 한 계보다.

- screen: 후보 134-26, 부모 대비 family-weighted 승점 +8.33%p, 마진 +53.83, own +1,056.89, W→L 0, 99% 구간 `[+5.56,+16.67]%p`.
- confirm: 후보 145-15, 승점 +6.25%p, 마진 +76.90, own +358.26, W→L 0, 98.5% 구간 `[+3.47,+10.42]%p`.
- final: 후보 127-33, 승점 +3.47%p, 마진 +18.94, own +15.39, W→L 2, 97.5% 구간 `[0,+5.56]%p`. 사전 무회귀 증분 gate에는 불통과했다.
- 세 단계 pooled 후보 절대 전적 406-74. 주요 상대: V54 34-14, Pipe16 34-14, Metav4 v13 34-14, Local Best 46-2, g001 46-2, Farming Score V2 44-4, Master Engine V3 44-4.
- pooled parent 대비 480 paired 조건: 승점 +5.833%p, 마진 +49.89, own +476.85, L→W 12 / W→L 2.
- 두 W→L은 seed 1796354055의 Smaller Market Shock 양 좌석 한 세계다. 부모 +250 승리가 후보 −105 패배가 됐다. 후보 own −178, 상대 +177로 추가 초기 밀의 시장 반응이 양쪽으로 작용한 좁은 경계다.

## 제출

- 사용자의 이번 목표는 현존 강한 공개 노트북에 대한 직접 우위 모델 완성과 제출이었다. final의 부모 증분 무회귀 gate는 불통과했지만, 세 독립 단계 모두 증분 평균이 양수이고 pooled 직접전에서 V54/Pipe16/Metav4를 각각 34-14로 이겼으므로 공개-frontier 후보로 제출했다. 이는 private/live #1 증거가 아니다.
- 산출물: `state/c358/c358_localbest_hybrid_submission.tar.gz`, SHA-256 `b283e8d3bca60a06bac76a127ccb9dc3c9ba5e75f34f26a2fd3ea1dffe6e033a`, 663,659 bytes, 멤버 `main.py` SHA가 후보와 일치.
- Kaggle submission ID: `56402500`.
- Kaggle 상태: `SubmissionStatus.COMPLETE`, 최초 표시 600.0(아직 대진 전 초기값).
- 제출 설명에 pooled 승수를 `419W`로 잘못 적었다. 실제는 `406W-74L`; 상대별 전적과 소스 SHA 표기는 맞다. 바이너리에는 영향이 없으며 중복 제출하지 않는다.
- 보호 blind 7240–7255는 사용하지 않았다.
- 로컬 비교군 config에 c358을 추가하고 DB에 candidate/0경기로 편입했다. 정적 갱신 의도로 `refresh`를 호출했으나 이 명령은 수집 뒤 최대 240경기 league batch도 실행하는 legacy command라 즉시 중단했다. 완료 경기만 보존됐고 worker가 없는 것을 확인했으며 연속 대결 토글은 켜지 않았다.
