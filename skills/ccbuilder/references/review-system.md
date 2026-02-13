# Claude Code Extension Review System

## 목적

Claude Code 확장 기능의 품질을 보장하기 위한 체계적인 리뷰 프로세스와 체크리스트를 제공합니다.

**Version**: 2.7.0
**Last Updated**: 2026-02-11

---

## 목차

1. [리뷰 프로세스](#1-리뷰-프로세스)
2. [Skill 리뷰](#2-skill-리뷰)
3. [Agent 리뷰](#3-agent-리뷰)
4. [Hook 리뷰](#4-hook-리뷰)
5. [Command 리뷰](#5-command-리뷰)
6. [Agent Teams 리뷰](#6-agent-teams-리뷰)
7. [Memory & Rules 리뷰](#7-memory--rules-리뷰)
8. [보안 리뷰](#8-보안-리뷰)
9. [성능 리뷰](#9-성능-리뷰)
10. [PR 리뷰 템플릿](#10-pr-리뷰-템플릿)

---

## 1. 리뷰 프로세스

### 리뷰 단계

```
1. 자가 리뷰 (Self-Review)
   ↓
2. 자동화 검증 (CI/CD)
   ↓
3. 피어 리뷰 (Peer Review)
   ↓
4. 최종 승인 (Approval)
   ↓
5. 배포 (Deploy)
```

### 리뷰어 역할

| 역할 | 책임 | 권한 |
|------|------|------|
| **Author** | 코드 작성, 자가 리뷰 | PR 생성 |
| **Reviewer** | 코드 검토, 피드백 | Comment, Request Changes |
| **Approver** | 최종 승인 | Approve, Merge |

### 리뷰 우선순위

```yaml
priority_levels:
  P0_Critical:
    description: "보안 취약점, 데이터 손실 위험"
    response_time: "즉시"
    requires: "시니어 리뷰"

  P1_High:
    description: "핵심 기능 버그, 성능 문제"
    response_time: "24시간 이내"
    requires: "팀원 리뷰"

  P2_Medium:
    description: "일반 기능 개선, 새 기능"
    response_time: "48시간 이내"
    requires: "팀원 리뷰"

  P3_Low:
    description: "문서화, 코드 스타일"
    response_time: "1주일 이내"
    requires: "자가 리뷰"
```

---

## 2. Skill 리뷰

### 2.1 Skill 리뷰 체크리스트

```markdown
## Skill Review Checklist

### 구조 (Structure)
- [ ] SKILL.md 파일이 올바른 위치에 있음 (.claude/skills/{name}/)
- [ ] Frontmatter에 name, description 포함
- [ ] description이 1024자 이하
- [ ] SKILL.md가 500줄 이하

### 내용 (Content)
- [ ] 목적 섹션이 명확함
- [ ] 사용 시점이 구체적으로 정의됨
- [ ] 핵심 가이드가 실행 가능함
- [ ] 예제가 포함됨
- [ ] 참조 문서가 올바르게 링크됨

### 트리거 (Trigger)
- [ ] description에 관련 키워드 포함
- [ ] skill-rules.json에 등록됨 (필요한 경우)
- [ ] 트리거 테스트 통과 (최소 3개)
- [ ] 오탐 테스트 통과 (최소 2개)

### 품질 (Quality)
- [ ] 맞춤법/문법 오류 없음
- [ ] 일관된 마크다운 형식
- [ ] 코드 블록에 언어 지정됨
- [ ] 링크가 유효함

### Progressive Disclosure
- [ ] SKILL.md에 핵심 내용만 포함
- [ ] 상세 내용은 references/에 위치
- [ ] 100줄+ 참조 파일에 목차 포함
```

### 2.2 Skill 품질 기준

```yaml
skill_quality_standards:
  basic:
    description: "최소 요구사항 충족"
    criteria:
      - SKILL.md 존재
      - Frontmatter 완전
      - 기본 섹션 존재

  standard:
    description: "표준 품질"
    criteria:
      - 모든 basic 요구사항
      - 3개 이상 트리거 테스트 통과
      - 예제 포함
      - 에러 케이스 처리

  production:
    description: "프로덕션 레디"
    criteria:
      - 모든 standard 요구사항
      - 500줄 이하
      - Progressive disclosure 적용
      - 10개 이상 테스트 통과
      - 성능 기준 충족

  excellent:
    description: "우수 품질"
    criteria:
      - 모든 production 요구사항
      - Self-evolution 메커니즘
      - 사용자 피드백 반영
      - 지속적 개선 이력
```

### 2.3 Skill 리뷰 피드백 예시

```markdown
### ✅ 좋은 점
- 목적이 명확하게 정의됨
- 예제가 실용적이고 이해하기 쉬움
- Progressive disclosure 패턴 잘 적용됨

### ⚠️ 개선 필요
1. **트리거 키워드 누락**
   - description에 "authentication" 키워드 추가 필요
   - 현재 "auth"만 있어 일부 프롬프트에서 트리거 안됨

2. **500줄 초과**
   - 현재 520줄 → 480줄로 축소 필요
   - "고급 패턴" 섹션을 references/로 이동 권장

### ❌ 블로킹 이슈
1. **보안 문제**
   - 예제에서 하드코딩된 API 키 발견
   - 반드시 환경변수 사용으로 변경 필요
```

---

## 3. Agent 리뷰

### 3.1 Agent 리뷰 체크리스트

```markdown
## Agent Review Checklist

### 구조 (Structure)
- [ ] .md 파일이 .claude/agents/에 위치
- [ ] 파일명이 agent 역할을 반영
- [ ] 필수 섹션 포함 (목적, 역할, 지시사항)

### 지시사항 (Instructions)
- [ ] 자율 실행 가능한 단계별 가이드
- [ ] 각 단계가 명확하고 구체적
- [ ] 완료 조건이 정의됨
- [ ] 예상 출력 형식 명시

### 도구 사용 (Tool Usage)
- [ ] 사용 가능한 도구 목록 명시
- [ ] 각 도구의 사용 목적 설명
- [ ] 불필요한 도구 제외

### 안전성 (Safety)
- [ ] 파괴적 작업에 대한 경고
- [ ] 범위 제한 명시
- [ ] 에러 처리 가이드

### 출력 품질 (Output Quality)
- [ ] 출력 형식이 일관됨
- [ ] 필요한 모든 정보 포함
- [ ] 실행 가능한 권장사항 제공
```

### 3.2 Agent 리뷰 기준

```yaml
agent_review_criteria:
  autonomy:
    weight: 30%
    questions:
      - "사용자 개입 없이 작업을 완료할 수 있는가?"
      - "에러 발생 시 자동 복구가 가능한가?"
      - "중간 결과를 적절히 저장하는가?"

  accuracy:
    weight: 25%
    questions:
      - "결과가 정확한가?"
      - "허위 정보 생성 가능성이 있는가?"
      - "일관된 결과를 제공하는가?"

  efficiency:
    weight: 20%
    questions:
      - "불필요한 도구 호출이 있는가?"
      - "실행 시간이 적절한가?"
      - "토큰 사용이 효율적인가?"

  safety:
    weight: 15%
    questions:
      - "파괴적 작업을 수행하는가?"
      - "범위를 벗어난 작업을 하는가?"
      - "민감한 정보를 다루는가?"

  reporting:
    weight: 10%
    questions:
      - "보고서가 명확한가?"
      - "필요한 모든 정보가 포함되어 있는가?"
      - "권장사항이 실행 가능한가?"
```

### 3.3 Agent 리뷰 피드백 템플릿

```markdown
## Agent Review: [agent-name]

### 요약
- **평가**: ✅ Approved / ⚠️ Needs Changes / ❌ Rejected
- **점수**: __/100
- **리뷰어**: [name]
- **날짜**: [date]

### 자율성 (Autonomy) - __/30
- [ ] 독립적 실행 가능
- [ ] 에러 복구 메커니즘
- [ ] 체크포인트 저장
**피드백**: ...

### 정확성 (Accuracy) - __/25
- [ ] 결과 정확도
- [ ] 일관성
- [ ] 허위 정보 방지
**피드백**: ...

### 효율성 (Efficiency) - __/20
- [ ] 도구 사용 최적화
- [ ] 실행 시간
- [ ] 토큰 효율성
**피드백**: ...

### 안전성 (Safety) - __/15
- [ ] 파괴적 작업 방지
- [ ] 범위 준수
- [ ] 권한 존중
**피드백**: ...

### 보고서 품질 (Reporting) - __/10
- [ ] 명확성
- [ ] 완전성
- [ ] 실행 가능성
**피드백**: ...

### 필수 수정사항
1. ...
2. ...

### 권장 개선사항
1. ...
2. ...
```

---

## 4. Hook 리뷰

### 4.1 Hook 리뷰 체크리스트

```markdown
## Hook Review Checklist

### 구조 (Structure)
- [ ] .claude/hooks/에 위치
- [ ] settings.json에 등록됨
- [ ] 적절한 Hook 타입 사용

### 구현 (Implementation)
- [ ] stdin JSON 파싱 구현
- [ ] 올바른 종료 코드 반환
- [ ] stdout/stderr 적절히 사용

### 성능 (Performance)
- [ ] 실행 시간 < 100ms
- [ ] 메모리 사용량 적절
- [ ] 동기 블로킹 없음

### 안정성 (Stability)
- [ ] 에러 처리 구현
- [ ] 실패 시 graceful degradation
- [ ] 세션 상태 관리 (필요한 경우)

### 테스트 (Testing)
- [ ] 정상 케이스 테스트
- [ ] 에러 케이스 테스트
- [ ] 경계 조건 테스트
```

### 4.2 Hook 타입별 리뷰 포인트

```yaml
UserPromptSubmit:
  purpose: "프롬프트 처리 전 실행"
  exit_codes:
    0: "계속 진행"
    1: "stderr 메시지 표시 후 계속"
  review_points:
    - "트리거 조건이 적절한가?"
    - "출력 메시지가 유용한가?"
    - "세션 반복 알림 방지가 되어 있는가?"

PreToolUse:
  purpose: "도구 실행 전 검증"
  exit_codes:
    0: "허용"
    2: "차단 + stderr 메시지"
  review_points:
    - "차단 조건이 명확한가?"
    - "오탐이 없는가?"
    - "에러 메시지가 실행 가능한가?"

Stop:
  purpose: "응답 완료 후 실행"
  exit_codes:
    0: "정상"
  review_points:
    - "리마인더가 유용한가?"
    - "너무 자주 트리거되지 않는가?"
    - "메시지가 건설적인가?"
```

### 4.3 Hook 성능 기준

```yaml
performance_requirements:
  latency:
    excellent: < 50ms
    acceptable: < 100ms
    warning: < 500ms
    unacceptable: >= 500ms

  memory:
    excellent: < 10MB
    acceptable: < 50MB
    warning: < 100MB
    unacceptable: >= 100MB

  cpu:
    excellent: < 10%
    acceptable: < 25%
    warning: < 50%
    unacceptable: >= 50%
```

---

## 5. Command 리뷰

> **참고**: Commands는 Skills로 통합되었습니다 (v2.1+). 새 구현은 Skills 권장.
> 기존 `.claude/commands/` 파일은 계속 지원됩니다.

### 5.1 Command 리뷰 체크리스트

```markdown
## Command Review Checklist

### 구조 (Structure)
- [ ] .claude/commands/에 위치
- [ ] 파일명이 명령어를 반영 ({name}.md)
- [ ] 마크다운 형식 유효

### 문서화 (Documentation)
- [ ] 목적 설명 포함
- [ ] 파라미터 문서화
- [ ] 사용 예제 포함
- [ ] 예상 동작 설명

### 기능 (Functionality)
- [ ] 명확한 단일 목적
- [ ] 합리적인 기본값
- [ ] 에러 케이스 처리
- [ ] 도움말 제공

### 사용성 (Usability)
- [ ] 직관적인 이름
- [ ] 일관된 파라미터 형식
- [ ] 명확한 피드백 메시지
```

### 5.2 Command 이름 규칙

```yaml
naming_conventions:
  format: "kebab-case"
  examples:
    good:
      - dev-docs
      - route-research-for-testing
      - create-component
    bad:
      - devDocs (camelCase 지양)
      - dev_docs (snake_case 지양)
      - DEV-DOCS (대문자 지양)

  guidelines:
    - 동사로 시작 (create, update, delete, generate, etc.)
    - 명확하고 설명적으로
    - 2-4 단어로 구성
    - 일반적인 약어만 사용
```

---

## 6. Agent Teams 리뷰 (v2.7 신규)

### 6.1 Agent Teams 리뷰 체크리스트

```markdown
## Agent Teams Review Checklist

### 팀 구성 (Team Structure)
- [ ] 팀 이름이 명확하고 kebab-case
- [ ] Teammate 수가 적절 (3-5개 권장)
- [ ] 각 Teammate의 역할이 명확
- [ ] 적절한 subagent_type 선택

### 작업 관리 (Task Management)
- [ ] Task 의존성이 올바르게 설정됨 (addBlockedBy)
- [ ] activeForm이 모든 Task에 설정됨
- [ ] Task description이 자율 실행 가능할 정도로 상세

### 커뮤니케이션 (Communication)
- [ ] DM 우선 사용 (브로드캐스트 최소화)
- [ ] Teammate를 이름으로 참조 (UUID 금지)
- [ ] 평문 메시지 사용 (JSON 상태 메시지 금지)

### 생명주기 (Lifecycle)
- [ ] 모든 Teammate 종료 후 TeamDelete 호출
- [ ] shutdown_request로 graceful 종료
- [ ] TeammateIdle Hook 설정 (필요 시)

### 비용 (Cost)
- [ ] 불필요한 브로드캐스트 없음
- [ ] Teammate 수 최적화
- [ ] 단순 작업에 Agent Teams 사용하지 않음 (Task Tool 단독 사용)
```

### 6.2 Agent Teams 리뷰 기준

```yaml
agent_teams_review_criteria:
  team_design:
    weight: 30%
    questions:
      - "팀 구성이 작업에 적합한가?"
      - "Teammate 역할이 명확히 분리되는가?"
      - "Task 의존성이 올바르게 모델링되었는가?"

  communication:
    weight: 25%
    questions:
      - "DM 위주로 소통하는가?"
      - "브로드캐스트 사용이 정당한가?"
      - "메시지가 명확하고 실행 가능한가?"

  cost_efficiency:
    weight: 25%
    questions:
      - "Agent Teams가 필요한 복잡도인가?"
      - "Teammate 수가 최적인가?"
      - "작업 시간이 적절한가?"

  lifecycle:
    weight: 20%
    questions:
      - "Graceful shutdown이 구현되었는가?"
      - "리소스 정리가 완전한가?"
      - "에러 시 복구 방안이 있는가?"
```

---

## 7. Memory & Rules 리뷰 (v2.7 신규)

### 7.1 Memory 리뷰 체크리스트

```markdown
## Memory Review Checklist

### MEMORY.md
- [ ] 200줄 이하
- [ ] 검증된 패턴만 포함
- [ ] CLAUDE.md와 중복 없음
- [ ] 토픽별로 정리됨

### 토픽 파일
- [ ] 의미있는 파일명 (debugging.md, patterns.md)
- [ ] 시간순이 아닌 토픽순 정리
- [ ] 오래된 정보 제거/업데이트

### 저장 기준
- [ ] 여러 세션에서 확인된 패턴만 저장
- [ ] 추측이나 미검증 결론 제외
- [ ] 사용자 명시적 요청은 즉시 저장
```

### 7.2 Rules 리뷰 체크리스트

```markdown
## Rules Review Checklist

### 구조
- [ ] .claude/rules/ 디렉토리에 위치
- [ ] kebab-case 파일명
- [ ] 전체 rules 합계 200줄 이하 권장

### 내용
- [ ] 핵심 규칙만 포함 (상세는 docs/reference/)
- [ ] paths: frontmatter 적절히 설정
- [ ] 규칙 간 충돌 없음
- [ ] CLAUDE.md와 일관성 유지
```

---

## 8. 보안 리뷰

### 8.1 보안 체크리스트

```markdown
## Security Review Checklist

### 인증/권한 (Authentication/Authorization)
- [ ] API 키가 하드코딩되지 않음
- [ ] 환경변수로 민감 정보 관리
- [ ] 최소 권한 원칙 준수
- [ ] 접근 제어 구현

### 입력 검증 (Input Validation)
- [ ] 모든 입력 검증됨
- [ ] 경로 순회 공격 방지
- [ ] 명령어 주입 방지
- [ ] XSS 방지 (웹 출력의 경우)

### 데이터 보호 (Data Protection)
- [ ] 민감 데이터 로깅 안함
- [ ] 임시 파일 적절히 삭제
- [ ] 암호화 적용 (필요한 경우)

### 의존성 (Dependencies)
- [ ] 알려진 취약점 없음
- [ ] 버전 고정됨
- [ ] 최신 보안 패치 적용

### 실행 환경 (Execution Environment)
- [ ] 샌드박스 경계 준수
- [ ] 파일 시스템 접근 제한
- [ ] 네트워크 접근 제한 (필요한 경우)
```

### 8.2 보안 취약점 분류

```yaml
vulnerability_severity:
  critical:
    description: "즉시 수정 필요"
    examples:
      - 원격 코드 실행 (RCE)
      - 인증 우회
      - 민감 데이터 노출
    action: "즉시 차단 및 수정"

  high:
    description: "24시간 내 수정"
    examples:
      - 권한 상승
      - SQL 주입
      - 명령어 주입
    action: "긴급 수정"

  medium:
    description: "1주일 내 수정"
    examples:
      - XSS
      - CSRF
      - 정보 누출
    action: "계획된 수정"

  low:
    description: "다음 릴리스에 수정"
    examples:
      - 정보 노출 (비민감)
      - 서비스 거부 (제한적)
    action: "백로그 추가"
```

### 8.3 보안 리뷰 템플릿

```markdown
## Security Review: [extension-name]

### 요약
- **위험 수준**: Critical / High / Medium / Low
- **발견된 취약점**: __개
- **리뷰어**: [name]
- **날짜**: [date]

### 발견된 취약점

#### 취약점 1: [제목]
- **심각도**: Critical / High / Medium / Low
- **유형**: [RCE / SQLi / XSS / etc.]
- **위치**: [파일:라인]
- **설명**: ...
- **재현 방법**: ...
- **수정 방안**: ...

### 보안 체크리스트 결과
- [ ] 인증/권한 - ✅/❌
- [ ] 입력 검증 - ✅/❌
- [ ] 데이터 보호 - ✅/❌
- [ ] 의존성 - ✅/❌
- [ ] 실행 환경 - ✅/❌

### 권장사항
1. ...
2. ...

### 결론
- **승인**: ✅ Approved / ❌ Rejected
- **조건**: ...
```

---

## 9. 성능 리뷰

### 9.1 성능 체크리스트

```markdown
## Performance Review Checklist

### 실행 시간 (Execution Time)
- [ ] Hook < 100ms
- [ ] Agent < 60s (기본 작업)
- [ ] Command < 5s (기본 실행)

### 리소스 사용 (Resource Usage)
- [ ] 메모리 누수 없음
- [ ] CPU 사용량 적절
- [ ] 디스크 I/O 최적화

### 확장성 (Scalability)
- [ ] 대용량 입력 처리 가능
- [ ] 동시 실행 지원
- [ ] 타임아웃 처리

### 효율성 (Efficiency)
- [ ] 불필요한 API 호출 없음
- [ ] 캐싱 적용 (적절한 경우)
- [ ] 배치 처리 (가능한 경우)
```

### 9.2 성능 벤치마크 기준

```yaml
benchmark_standards:
  hooks:
    p50: 30ms
    p90: 50ms
    p99: 100ms
    max: 500ms

  agents:
    simple_task:
      p50: 15s
      p90: 30s
      p99: 60s
    complex_task:
      p50: 45s
      p90: 90s
      p99: 180s

  commands:
    p50: 1s
    p90: 3s
    p99: 5s
    max: 30s
```

### 9.3 성능 최적화 권장사항

```yaml
optimization_recommendations:
  hooks:
    - "JSON 파싱 최적화 (streaming parser 사용)"
    - "세션 상태 캐싱"
    - "불필요한 파일 I/O 제거"
    - "비동기 처리 활용"

  agents:
    - "병렬 도구 호출 활용"
    - "체크포인트 저장으로 재시작 지원"
    - "불필요한 파일 읽기 최소화"
    - "결과 캐싱 (중복 분석 방지)"

  commands:
    - "지연 로딩 적용"
    - "결과 스트리밍"
    - "백그라운드 처리 (긴 작업)"
```

---

## 10. PR 리뷰 템플릿

### 10.1 PR 생성 템플릿

```markdown
## PR: [확장 기능 유형] [이름] - [변경 사항 요약]

### 변경 유형
- [ ] 새 기능 (Skill/Agent/Hook/Command)
- [ ] 기능 개선
- [ ] 버그 수정
- [ ] 문서화
- [ ] 성능 개선
- [ ] 리팩토링

### 변경 내용
[변경 사항에 대한 상세 설명]

### 테스트
- [ ] 자동화 테스트 추가/수정
- [ ] 수동 테스트 완료
- [ ] 모든 기존 테스트 통과

### 체크리스트
- [ ] 500-line rule 준수 (Skill)
- [ ] 성능 기준 충족
- [ ] 보안 검토 완료
- [ ] 문서화 업데이트

### 스크린샷/데모
[해당되는 경우 추가]

### 관련 이슈
Fixes #[issue-number]
```

### 10.2 PR 리뷰 템플릿

```markdown
## PR Review: #[number]

### 요약
- **결정**: ✅ Approve / 🔄 Request Changes / ❌ Reject
- **리뷰어**: [name]
- **날짜**: [date]

### 검토 항목

#### 코드 품질
- [ ] 코드가 명확하고 이해하기 쉬움
- [ ] 일관된 코딩 스타일
- [ ] 적절한 에러 처리
- [ ] 중복 코드 없음

#### 기능
- [ ] 요구사항 충족
- [ ] 엣지 케이스 처리
- [ ] 기존 기능과의 호환성

#### 성능
- [ ] 성능 기준 충족
- [ ] 리소스 사용 적절
- [ ] 확장성 고려됨

#### 보안
- [ ] 보안 취약점 없음
- [ ] 민감 정보 보호됨
- [ ] 입력 검증 구현됨

#### 문서화
- [ ] 코드 주석 적절
- [ ] README/문서 업데이트됨
- [ ] 변경 이력 기록됨

### 피드백

#### ✅ 좋은 점
1. ...

#### ⚠️ 개선 필요
1. [파일:라인] - [설명]
   ```suggestion
   // 제안 코드
   ```

#### ❌ 블로킹 이슈
1. [파일:라인] - [설명]
   - 이유: ...
   - 수정 방안: ...

### 추가 의견
...
```

### 10.3 리뷰 결정 기준

```yaml
review_decision_criteria:
  approve:
    conditions:
      - "모든 체크리스트 통과"
      - "블로킹 이슈 없음"
      - "테스트 통과"
    action: "Merge 진행"

  request_changes:
    conditions:
      - "수정 가능한 이슈 존재"
      - "테스트 실패"
      - "문서화 누락"
    action: "수정 후 재리뷰"

  reject:
    conditions:
      - "심각한 보안 취약점"
      - "설계 결함"
      - "요구사항 불충족"
    action: "재설계 필요"
```

---

## 부록

### A. 리뷰 도구

```bash
# Skill 구조 검증
node .claude/scripts/validate-skills.js

# Hook 성능 벤치마크
.claude/scripts/hook-benchmark.sh

# 보안 스캔
npm audit
snyk test

# 코드 품질 검사
eslint .claude/hooks/
```

### B. 리뷰 자동화

```yaml
# .github/workflows/extension-review.yml
name: Extension Review

on:
  pull_request:
    paths:
      - '.claude/**'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Structure validation
        run: node .claude/scripts/validate-structure.js

      - name: Security scan
        run: npm audit --audit-level=high

      - name: Performance check
        run: .claude/scripts/check-performance.sh

      - name: Generate review report
        run: node .claude/scripts/generate-review.js

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const report = require('./review-report.json');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report.summary
            });
```

### C. 참고 문서

- [Evaluation Framework](../evaluations/evaluation-framework.md)
- [Best Practices](./best-practices.md)

---

**문서 상태**: PRODUCTION-READY ✅
**마지막 업데이트**: 2026-02-11 (v2.7.0)
