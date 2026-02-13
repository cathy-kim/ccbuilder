# Orchestrator Skill 생성 가이드

> 병렬 Agent를 조율하는 Orchestrator Skill을 만들 때 따라야 할 체크리스트와 템플릿

**최종 업데이트**: 2026-02-11
**버전**: 2.9.0

---

## 목차

1. [Orchestrator Skill이란?](#1-orchestrator-skill이란)
2. [생성 전 체크리스트](#2-생성-전-체크리스트)
3. [필수 구성 요소](#3-필수-구성-요소)
4. [SKILL.md 템플릿](#4-skillmd-템플릿)
5. [Context Injection 구현](#5-context-injection-구현)
6. [Evaluation Loop 구현](#6-evaluation-loop-구현)
7. [테스트 및 검증](#7-테스트-및-검증)
8. [예시: autonomous-feature-builder](#8-예시-autonomous-feature-builder)

---

## 1. Orchestrator Skill이란?

### 1.1 정의

**Orchestrator Skill**은 여러 SubAgent를 조율하여 복잡한 작업을 완료하는 스킬입니다.

```
┌─────────────────────────────────────────┐
│           ORCHESTRATOR SKILL            │
│  - 계획 수립                            │
│  - SubAgent 위임                        │
│  - 결과 검증                            │
│  - 품질 평가                            │
└─────────────────────────────────────────┘
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
   [SubAgent A]   [SubAgent B]   [SubAgent C]
```

### 1.2 언제 Orchestrator를 만들어야 하는가?

| 상황 | Orchestrator 필요 여부 |
|------|----------------------|
| 2개 이상 Agent가 병렬 실행 | ✅ 필요 |
| 작업이 여러 Phase로 분리됨 | ✅ 필요 |
| 결과 품질 평가 및 재시도 필요 | ✅ 필요 |
| 단일 Agent가 순차 실행 | ❌ 불필요 |
| 간단한 단일 파일 수정 | ❌ 불필요 |

### 1.3 핵심 원칙

```
1. YOU ORCHESTRATE, YOU DO NOT EXECUTE
   - Orchestrator는 직접 코드를 작성하지 않음
   - 모든 실행은 SubAgent에게 위임

2. SUBAGENTS LIE. VERIFY EVERYTHING.
   - SubAgent 완료 보고를 신뢰하지 않음
   - 파일 생성, 빌드, 테스트 모두 검증

3. BACKWARD COMPATIBILITY IS NON-NEGOTIABLE
   - 하위호환 깨짐 = 즉시 RETRY
```

---

## 2. 생성 전 체크리스트

### 2.1 스킬 필요성 확인

- [ ] 작업이 2개 이상의 독립적인 SubAgent로 분리 가능한가?
- [ ] 병렬 실행으로 효율을 높일 수 있는가?
- [ ] 품질 검증 및 재시도 로직이 필요한가?
- [ ] 기존 스킬로는 해결이 어려운가?

### 2.2 범위 정의

- [ ] Orchestrator가 담당할 작업 범위 명확히 정의
- [ ] 각 SubAgent의 역할과 경계 정의
- [ ] 예상되는 Phase 수와 의존성 파악
- [ ] 성공 기준(Success Criteria) 정의

### 2.3 기존 패턴 확인

- [ ] `orchestrator-principles.md` 읽기
- [ ] `autonomous-feature-builder` 구조 참고
- [ ] Context Injection System 이해

---

## 3. 필수 구성 요소

### 3.1 폴더 구조

```
.claude/skills/[orchestrator-name]/
├── SKILL.md              # 스킬 정의 (필수)
├── CHANGELOG.md          # 버전 히스토리 (권장)
├── templates/            # 위임 템플릿 (선택)
│   ├── shared-context.template.md
│   ├── individual-context.template.md
│   └── result-report.template.md
├── agents/               # SubAgent 정의 (선택)
│   └── [agent-name].md
└── references/           # 참조 문서 (선택)
```

### 3.2 SKILL.md 필수 섹션

| 섹션 | 설명 | 필수 여부 |
|------|------|----------|
| 메타데이터 | 이름, 설명, 트리거, 키워드 | ✅ 필수 |
| Core Principles | 핵심 원칙 | ✅ 필수 |
| Phases | 실행 단계 | ✅ 필수 |
| Delegation Format | 위임 프롬프트 형식 | ✅ 필수 |
| Evaluation Loop | 품질 평가 기준 | ✅ 필수 |
| Context Injection | 병렬 실행 시 컨텍스트 주입 | 병렬 시 필수 |

### 3.3 필수 시스템

1. **Mission Reminder System** - 목적 망각 방지
2. **Context Injection System** - 병렬 Agent 조율
3. **Evaluation Loop** - 품질 검증 및 재시도
4. **Result Report** - 표준화된 완료 보고

---

## 4. SKILL.md 템플릿

```markdown
# [Skill Name]

> [한 줄 설명]

**Version**: 1.0.0
**Updated**: YYYY-MM-DD

---

## 트리거

- [트리거 키워드 1]
- [트리거 키워드 2]

## 핵심 원칙

### 1. YOU ORCHESTRATE, YOU DO NOT EXECUTE
[설명]

### 2. SUBAGENTS LIE. VERIFY EVERYTHING.
[설명]

### 3. [도메인 특화 원칙]
[설명]

---

## Phases

### Phase 1: [이름]
- 목적: [목적]
- 도구: [사용 도구]
- 산출물: [산출물]

### Phase 2: [이름]
...

### Phase N: [이름]
...

---

## Delegation Format (9-Section)

### STEP 0: READ SHARED CONTEXT
```
먼저 다음 파일을 읽으세요:
`{shared-context-path}`
```

### Section 0: MISSION REMINDER
```
╔══════════════════════════════════════════════════════════════╗
║  MISSION REMINDER - DO NOT FORGET                            ║
╠══════════════════════════════════════════════════════════════╣
║  Original Goal: {goal}                                       ║
║  Your Task: {task} ({n}/{total})                            ║
║  Session: {session-id}                                       ║
╚══════════════════════════════════════════════════════════════╝

### Boundaries
- ALLOWED: {허용 파일}
- FORBIDDEN: {금지 파일}
```

### Section 1-8: [표준 섹션]
[autonomous-feature-builder 참조]

### Section 9: RESULT REPORT
[표준 Result Report 형식]

---

## Evaluation Loop

### Quality Score (100점)

| 항목 | 점수 | 기준 |
|------|------|------|
| [항목 1] | [점수] | [기준] |
| [항목 2] | [점수] | [기준] |
| ... | ... | ... |
| 합계 | 100점 | |

### Decision Rules

| 점수 | 행동 | 설명 |
|------|------|------|
| ≥90 | CONTINUE | 다음 Phase 진행 |
| 60-89 | MODIFY | 이슈만 수정 |
| <60 | RETRY | 처음부터 재시도 |

⚠️ **하위호환 깨짐 = 즉시 RETRY** (점수 무관)

---

## Context Injection System

[병렬 실행이 있는 경우]

### Shared Context 생성

| 항목 | 설명 |
|------|------|
| Original Goal | 원래 목표 |
| Success Criteria | 성공 기준 |
| Tech Stack | 기술 스택 |
| Parallel Agents | Agent 목록 및 경계 |
| Coordination Rules | 조율 규칙 |

### Individual Context 포함 사항

| 항목 | 설명 |
|------|------|
| STEP 0 | Shared Context 읽기 지시 |
| Mission Reminder Box | 목적 및 경계 명시 |
| Task Details | 개별 작업 내용 |

---

## 참고 문서

- [orchestrator-principles.md](../reference/orchestrator-principles.md)
- [autonomous-feature-builder/SKILL.md](../autonomous-feature-builder/SKILL.md)
```

---

## 5. Context Injection 구현

### 5.1 Shared Context 템플릿

```markdown
# Shared Context - {Project Name}

## 0. Mission
**Original Goal**: {원래 목표}
**Project Name**: {프로젝트명}
**Session ID**: {세션 ID}

## 1. Success Criteria
- [ ] 성공 기준 1
- [ ] 성공 기준 2

## 2. Tech Stack
- Language: TypeScript
- Framework: [프레임워크]
- Database: [데이터베이스]

## 3. Constraints
- 각 Agent는 자신의 파일만 수정
- 하위호환 100% 유지

## 4. Parallel Agents
| # | Agent Name | Role | Files | Status |
|---|------------|------|-------|--------|
| 1 | agent-a | 역할 A | path/a.ts | pending |
| 2 | agent-b | 역할 B | path/b.ts | pending |

## 5. Coordination Rules
1. File Ownership: 각 Agent는 자신의 파일만 수정
2. Result Report: 완료 시 표준 형식으로 보고
```

### 5.2 Individual Context 템플릿

```markdown
## STEP 0: READ SHARED CONTEXT
먼저 다음 파일을 읽으세요:
`{shared-context-path}`

---

## 0. MISSION REMINDER (⚠️ DO NOT FORGET)

╔══════════════════════════════════════════════════════════════╗
║  MISSION REMINDER - DO NOT FORGET                            ║
╠══════════════════════════════════════════════════════════════╣
║  Original Goal: {원래 목표}                                   ║
║  Your Task: {이 Agent의 역할} ({n}/{total})                   ║
║  Session: {session-id}                                       ║
╚══════════════════════════════════════════════════════════════╝

### Boundaries
- ALLOWED: {허용된 파일 경로}
- FORBIDDEN: {금지된 파일 경로}

## 1. TASK
{구체적인 작업 내용}

...

## 9. RESULT REPORT
완료 후 다음 형식으로 보고서 작성:
{result-report-template}
```

### 5.3 Result Report 템플릿

```markdown
# Agent {name} Result Report

## Session Info
| Key | Value |
|-----|-------|
| Session ID | {session-id} |
| Agent Name | agent-{name} |
| Task | {task} ({n}/{total}) |
| Status | ✅ COMPLETED / ❌ FAILED |

## Completed Items
- [x] 항목 1
- [x] 항목 2

## Created/Modified Files
| File | Status | Description |
|------|--------|-------------|
| path/to/file.ts | ✅ Created | 설명 |

## Shared Context Verification
✅ **Original Goal**: {goal 명시}
✅ **Boundaries Respected**: 다른 Agent 파일 수정 안 함

## Validation Results
- TypeScript: ✅ 에러 0개
- Build: ✅ 성공
- Tests: ✅ 통과
```

---

## 6. Evaluation Loop 구현

### 6.1 표준 품질 점수 배분

| 항목 | 점수 | 설명 |
|------|------|------|
| TypeScript 에러 | 20점 | 0개=20, 1-3개=10, 4+개=0 |
| 빌드 성공 | 15점 | 성공=15, 실패=0 |
| 테스트 통과 | 15점 | 전체=15, 일부=8, 실패=0 |
| 하위호환 | 25점 | 100%=25, 깨짐=0 |
| Scope 준수 | 10점 | 범위 내=10, 초과=0 |
| Result Report | 15점 | 형식+Goal=15, 형식만=8, 없음=0 |
| **합계** | **100점** | |

### 6.2 Decision Matrix

```typescript
function decide(score: number, backwardCompatible: boolean): Action {
  // 하위호환 최우선
  if (!backwardCompatible) return "RETRY";

  if (score >= 90) return "CONTINUE";
  if (score >= 60) return "MODIFY";
  return "RETRY";
}
```

### 6.3 검증 명령

```bash
# 표준 검증 스크립트
npx tsc --noEmit && npm run build && npm test

# 하위호환 체크 (API 변경 시)
npm run test:e2e -- --grep "backward-compat"
```

---

## 7. 테스트 및 검증

### 7.1 AB Test 수행 (권장)

새로운 Orchestrator 패턴 적용 전:

1. **Version A (Control)**: 기존 방식 또는 단순 프롬프트
2. **Version B (Treatment)**: 새 패턴 적용

### 7.2 측정 지표

| 지표 | 측정 방법 |
|------|----------|
| Goal Retention | Agent 완료 메시지에서 Original Goal 언급 여부 |
| Boundary Compliance | 금지 파일 수정 여부 |
| Code Quality | TypeScript 에러, 빌드, 테스트 |
| Completion Rate | 작업 완료율 |

### 7.3 AB Test 폴더 구조

```
.claude/ab-test/[test-name]/
├── TEST-PLAN.md
├── version-a/
│   └── output/
├── version-b/
│   ├── output/
│   └── results/
└── results/
    └── comparison.md
```

---

## 8. 예시: autonomous-feature-builder

### 8.1 구조

```
.claude/skills/autonomous-feature-builder/
├── SKILL.md              # v3.1.0
├── CHANGELOG.md          # 버전 히스토리
└── (templates는 inline)
```

### 8.2 핵심 특징

1. **9 Phases**: Research → Design → Schema → API → UI → ...
2. **Context Injection**: Phase 2.5에서 Shared Context 생성
3. **9-Section Delegation**: STEP 0 + Section 0-9
4. **Evaluation Loop**: 90점 이상 CONTINUE

### 8.3 AB Test 검증

| 지표 | Before | After |
|------|--------|-------|
| Goal Retention | 0% | 100% |
| Boundary Compliance | 측정 불가 | 100% |

---

## Quick Reference

### Orchestrator Skill 생성 단계

1. **계획**: 범위 정의, Phase 분리, Agent 역할 정의
2. **구조 생성**: `.claude/skills/[name]/SKILL.md`
3. **원칙 적용**: 3대 원칙 + Context Injection
4. **Delegation Format**: 9-Section 형식 사용
5. **Evaluation Loop**: 품질 점수 및 Decision Rule
6. **테스트**: AB Test로 효과 검증
7. **문서화**: CHANGELOG.md 작성

### 필수 체크리스트

- [ ] `orchestrator-principles.md` 참조
- [ ] Mission Reminder Box 포함
- [ ] Context Injection System 적용 (병렬 시)
- [ ] Evaluation Loop 정의
- [ ] Result Report 형식 지정
- [ ] 하위호환 검증 로직
- [ ] AB Test 수행 (권장)

---

## 참고 문서

- [orchestrator-principles.md](./orchestrator-principles.md) - 핵심 원칙
- [autonomous-feature-builder/SKILL.md](../../skills/autonomous-feature-builder/SKILL.md) - 참조 구현
- [autonomous-feature-builder/CHANGELOG.md](../../skills/autonomous-feature-builder/CHANGELOG.md) - 버전 히스토리
- [AB Test Results](../../ab-test/context-injection-test/results/comparison.md) - 검증 결과

---

**문서 관리**:
- 새로운 패턴이 검증되면 이 가이드에 추가
- 변경 시 버전 번호와 날짜 갱신
