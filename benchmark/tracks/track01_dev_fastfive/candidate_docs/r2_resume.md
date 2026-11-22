# 김도현 이력서 — 패스트파이브 Backend Engineer 지원

## 요약
5년간 실사용 B2B 공간 예약·정산 플랫폼을 운영하며, CS·지점 운영팀 문의를 로그와 데이터로 파고들어 문제 정의부터 백엔드·어드민 화면 구현, 배포·장애 재발 방지까지 끝까지 책임진 백엔드 엔지니어입니다.

## 경력 (총 5년)
### 주식회사 스페이스링크 (2021.03 ~ 현재, 플랫폼 백엔드 개발자)
- **예약·정산·출입 플랫폼 End-to-End 운영:** 월 18만 건 예약·정산 트래픽을 처리하는 TypeScript/Node.js/NestJS/TypeORM REST API 및 PostgreSQL 트랜잭션 설계·운영
- **운영팀 반복 문의 해결 및 어드민 React 화면 직접 구현:** 지점 운영팀의 수동 환불/출입권한 오류 문의(주 40건+)를 Datadog·Grafana 로그 분석으로 규명하고, 백엔드 API + React 기반 정산·출입 어드민 화면을 직접 구현·배포하여 관련 CS 문의 74% 감소(주 42건 → 11건)
- **결제·출입 외부 시스템 연동 및 RabbitMQ 비동기 전환:** 결제 PG 및 출입 게이트 외부 API 장애 시 예약이 롤백되던 문제를 RabbitMQ 기반 비동기 메시징 + 멱등키·재시도 큐로 재설계해 결제 실패율 3.2% → 0.18% 개선
- **장애 대응 및 재발 방지:** 정산 배치 데드락 사고 당시 PostgreSQL lock 로그를 분석해 인덱스·격리수준 조정 및 모니터링 알림·자동 복구 런북 반영(재발 0건)
- **AI 코딩 도구 활용:** Claude Code를 레거시 코드 분석·회귀 테스트 작성·어드민 UI 프로토타이핑에 적극 활용해 기능 리드타임 약 35% 단축

## 기술 스택
TypeScript, Node.js, NestJS, TypeORM, React, PostgreSQL, Redis, RabbitMQ, AWS, Docker, Datadog, Grafana, Claude Code
