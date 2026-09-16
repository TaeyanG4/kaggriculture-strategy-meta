작업 경로: H:\dev\kaggle-data\kaggriculture-strategy-meta

역할: 아래 두 독립 후보의 코드 구현만 수행하라. 게임 실행·대규모 검증·제출은 하지 마라.
AGENTS.md, HANDOFF.md와 reports/c155-o160-screen-review-2026-09-15.ko.md를 먼저 읽어라.
기존 소스·결과·manifest·공통 검증기는 변경하지 마라. 버전 번호 충돌을 확인하라.

근거:
- o160은 공통 상대 288경기에서 256승/32패, o159b는 243승/45패다.
- 그러나 o160-o159b 승점 차이 구간은 0을 포함하고 승→패9건, 손실 꼬리 악화가 있다.
- 수확 추가 후 급식 생략도 증가했다. 효과의 단독 원인과 상호작용은 미확정이다.

후보 A: agent/o161_harvest_only.py
- 부모: agent/c150.py
- 부모 SHA256: 9713af1538ccc8e4e0e8a7ff72ae8a614ba9e7dcb3eb9d53c3074aabec137d6b
- agent/overlays/o160_goose_harvest.py의 행동 로직을 그대로 적용하라.
- o159/o159b 급식 오버레이는 넣지 마라. 수확 임계값 GOOSE3/COW5/SHEEP5를 유지하라.
- 기존 부모의 급식·시장·이동·고용 정책을 임의로 손대지 마라.
- 목적은 c150/급식만(o159b)/수확만(o161)/급식+수확(o160)의 2×2 효과 분리다.

후보 B: agent/o162_goose_only.py
- 부모: agent/o159b_feed_margin06.py. 원본 SHA256을 계산하고 빌드에 고정하라.
- o160 수확 오버레이의 _O160_THRESH에 해당하는 사전만 {'GOOSE': 3}으로 제한하라.
- 소·양의 CARE는 부모 그대로 반환하라. 거위 임계값과 시간창은 변경하지 마라.
- o159b의 급식 계수0.6 및 모든 급식 조건은 유지하라.
- 목적은 수확 변경의 적용 종을 줄였을 때 이득과 회귀가 어떻게 달라지는지 보는 것이다.

구현 세부:
1. 독립 오버레이 파일과 부모 해시를 확인하는 재현 가능한 빌드를 제공하라.
   기존 빌드 도구를 먼저 검색해 재사용하라. 같은 이름의 다른 파일을 덮어쓰지 마라.
2. 부모(observation, configuration)는 턴당 정확히 한 번만 호출하라.
3. observation과 부모 행동 객체를 직접 수정하지 마라. 변경할 때만 복사하라.
4. 최종 Kaggle loader가 선택할 callable은 agent여야 한다.
5. telemetry 접두어를 o161_/o162_로 명확하게 구분하고 부모 telemetry는 보존하라.
   종별 harvest_swap_requests, requested_units, errors를 기록하라.
   requested_units를 실제 수확·매출이라고 표기하지 마라.
6. 부모 행동이 FEED/HARVEST/PASS일 때는 수확 오버레이로 변경하지 마라.
   새 현금·가격·상대·시드 조건이나 중복 급식 게이트를 추가하지 마라.

짧은 비게임 검사는 수행해도 된다:
- 합성 관측으로 후보 A의 수확 동작이 기존 o160 오버레이와 같은지 확인.
- 후보 B는 거위 CARE/yield3에서 HARVEST, 거위 yield2에서는 CARE 유지,
  소·양 CARE에서는 yield가 높아도 부모 유지.
- 부모 단일 호출, 입력 객체 불변, 최종 callable, 부모 해시 확인.
실제 경기·리플레이 재실행·shadow 캠페인은 실행하지 마라.

검증 도구를 새로 만들거나 기존 실험 러너를 복제하지 마라.
공통 도구는 tools/run-validation.ps1, tools/validation_v1.py,
tools/validation_stats_v1.py이며, 검증 설정과 명령은 구현 리뷰 후 별도로 제공된다.

완료 보고:
- 후보/부모/오버레이 경로와 SHA256
- 정확한 행동 변경과 변하지 않은 조건
- 수행한 비게임 검사와 미검증 사항
- 모든 산출물의 절대 경로
- '구현 완료·성능 미검증' 표기
