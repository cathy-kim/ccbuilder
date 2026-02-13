# Orchestrator & Multi-Agent Principles

> 병렬 Agent 운영 및 Orchestrator 설계 원칙 (AB Test 검증 포함)

**최종 업데이트**: 2026-01-23
**버전**: 1.1.0

---

## 목차

1. [Core Principles](#1-core-principles)
2. [Context Injection System](#2-context-injection-system)
3. [Mission Reminder System](#3-mission-reminder-system)
4. [Delegation Format](#4-delegation-format)
5. [Evaluation Loop](#5-evaluation-loop)
6. [Checklist-Driven Evaluation](#6-checklist-driven-evaluation) ⭐ NEW
7. [Agent Council & Codex 활용 전략](#7-agent-council--codex-활용-전략) ⭐ NEW
8. [Parallel Execution Patterns](#8-parallel-execution-patterns)
9. [AB Test Results](#9-ab-test-results)

---

## 1. Core Principles

### 1.1 YOU ORCHESTRATE, YOU DO NOT EXECUTE

```
Orchestrator의 역할:
✅ 계획 수립 및 분해
✅ SubAgent에게 위임
✅ 결과 검증 및 통합
✅ 실패 시 재위임

❌ 직접 코드 작성
❌ 직접 파일 수정
❌ SubAgent 역할 대체
```

**이유**: Orchestrator가 직접 실행하면 컨텍스트가 빠르게 소진되고, 병렬 처리가 불가능해짐.

### 1.2 SUBAGENTS LIE. VERIFY EVERYTHING.

```typescript
// SubAgent 완료 보고를 신뢰하지 않음
async function verifySubagentWork(result: SubagentResult): Promise<boolean> {
  // 1. 파일 실제 생성 확인
  const filesExist = await checkFilesExist(result.claimedFiles);

  // 2. 빌드 성공 확인
  const buildSuccess = await runBuild();

  // 3. 테스트 통과 확인
  const testsPass = await runTests();

  // 4. 타입 에러 확인
  const noTypeErrors = await checkTypeScript();

  return filesExist && buildSuccess && testsPass && noTypeErrors;
}
```

### 1.3 BACKWARD COMPATIBILITY IS NON-NEGOTIABLE

```
하위호환 체크리스트:
□ 기존 API 엔드포인트 - 동일한 요청/응답 형식
□ 기존 DB 스키마 - 컬럼 삭제/타입 변경 금지
□ 기존 컴포넌트 - Props 인터페이스 유지
□ 기존 라우트 - URL 구조 유지
□ 기존 타입 - 기존 타입 정의 수정 금지

⚠️ 하위호환 깨짐 = 즉시 RETRY (점수 무관)
```

---

## 2. Context Injection System

> **AB Test 검증 완료** (2026-01-21)
> - Goal Retention: 0% → 100%
> - Boundary Compliance: 측정 불가 → 100%

### 2.1 개요

병렬로 실행되는 Agent들이 동일한 목적(Goal)을 공유하고, 파일 경계(Boundary)를 존중하도록 하는 시스템.

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                             │
│  1. Shared Context 생성                                     │
│  2. 병렬 Agent 실행 (각각 Individual Context 포함)           │
│  3. Result Reports 수집 및 검증                              │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────┐
│              SHARED CONTEXT                        │
│  - Original Goal                                   │
│  - Success Criteria                                │
│  - Tech Stack                                      │
│  - Agent List & Boundaries                         │
│  - Coordination Rules                              │
└───────────────────────────────────────────────────┘
        │
        ├──────────────┬──────────────┐
        ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Agent A    │ │  Agent B    │ │  Agent C    │
│  - Read     │ │  - Read     │ │  - Read     │
│    Shared   │ │    Shared   │ │    Shared   │
│  - Execute  │ │  - Execute  │ │  - Execute  │
│  - Report   │ │  - Report   │ │  - Report   │
└─────────────┘ └─────────────┘ └─────────────┘
```

### 2.2 구성 요소

#### Shared Context (공유 컨텍스트)

모든 병렬 Agent가 읽어야 하는 공통 정보:

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
- Framework: Next.js 14
- Database: Supabase

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

#### Individual Context (개별 컨텍스트)

각 Agent에게 전달되는 개별 지시:

```markdown
## STEP 0: READ SHARED CONTEXT
먼저 다음 파일을 읽으세요:
`{shared-context-path}`

---

## 0. MISSION REMINDER
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
```

#### Result Report (결과 보고서)

표준화된 완료 보고서:

```markdown
# Agent {name} Result Report

## Session Info
| Key | Value |
|-----|-------|
| Session ID | {session-id} |
| Agent Name | agent-{name} |
| Task | {task} ({n}/{total}) |
| Status | ✅ COMPLETED |

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

### 2.3 적용 시점

```yaml
triggers:
  - 2개 이상의 Agent가 병렬 실행될 때
  - Phase 3-5 (Schema, Implementation, UI) 동시 진행 시
  - 여러 파일을 동시에 생성/수정할 때

not_needed:
  - 단일 Agent 순차 실행
  - 간단한 단일 파일 수정
```

---

## 3. Mission Reminder System

### 3.1 문제점

긴 작업 중 Agent가 원래 목적을 잊어버리는 현상:
- Context window 후반부에서 목적 망각
- 범위를 벗어나는 작업 수행
- 불필요한 리팩토링/개선 시도

### 3.2 해결책: Mission Reminder Box

```
╔══════════════════════════════════════════════════════════════╗
║  MISSION REMINDER - DO NOT FORGET                            ║
╠══════════════════════════════════════════════════════════════╣
║  Original Goal: {목표}                                        ║
║  Your Task: {현재 태스크}                                     ║
║  Session: {세션 ID}                                          ║
╚══════════════════════════════════════════════════════════════╝
```

**특징**:
- 시각적으로 눈에 띄는 박스 형태
- 모든 Delegation prompt 상단에 배치
- 작업 중간에 참조하도록 유도

### 3.3 효과

| Before | After |
|--------|-------|
| 목적 망각 빈번 | 목적 유지율 100% |
| 범위 초과 작업 | 범위 내 작업만 수행 |
| 불필요한 리팩토링 | 요청된 작업만 수행 |

---

## 4. Delegation Format

### 4.1 9-Section Format (v3.1)

```markdown
## STEP 0: READ SHARED CONTEXT (v3.1)
먼저 Shared Context 파일을 읽으세요.

---

## 0. MISSION REMINDER (⚠️ DO NOT FORGET)
[Mission Reminder Box]
### Boundaries
- ALLOWED: ...
- FORBIDDEN: ...

## 1. TASK
구체적인 작업 내용

## 2. EXPECTED OUTCOME
- [ ] 예상 결과물 1
- [ ] 예상 결과물 2

## 3. REQUIRED SKILLS
필요한 기술 스택

## 4. REQUIRED TOOLS
Allowed: Read, Write, Edit, Bash, Glob, Grep
NOT Allowed: Task, Bash(rm *), Bash(git *)

## 5. MUST DO
- 필수 수행 사항 1
- 필수 수행 사항 2

## 6. MUST NOT DO
- 금지 사항 1
- 금지 사항 2

## 7. CONTEXT
### 7.1 Inherited Knowledge
### 7.2 Previous Task Learnings
### 7.3 Dependencies

## 8. VERIFICATION
```bash
npx tsc --noEmit && npm run build && npm test
```

## 9. RESULT REPORT (v3.1)
완료 후 Result Report 생성
```

---

## 5. Evaluation Loop

### 5.1 흐름

```
TASK COMPLETION
      │
      ▼
QUALITY EVALUATION
      │
      ▼
   SCORE?
   /  |  \
  /   |   \
 ▼    ▼    ▼
≥90  60-89  <60
 │    │     │
 ▼    ▼     ▼
CONTINUE MODIFY RETRY
```

### 5.2 Quality Score (100점 만점)

| 항목 | 점수 | 기준 |
|------|------|------|
| TypeScript 에러 | 20점 | 0개=20, 1-3개=10, 4+개=0 |
| 빌드 성공 | 15점 | 성공=15, 실패=0 |
| 테스트 통과 | 15점 | 전체=15, 일부=8, 실패=0 |
| 하위호환 | 25점 | 100%=25, 깨짐=0 |
| Scope 준수 | 10점 | 범위 내=10, 초과=0 |
| Result Report | 15점 | 형식+Goal=15, 형식만=8, 없음=0 |

### 5.3 Decision Rules

```typescript
function decide(score: number, backwardCompatible: boolean): Action {
  // 하위호환 최우선
  if (!backwardCompatible) return "RETRY";

  if (score >= 90) return "CONTINUE";
  if (score >= 60) return "MODIFY";
  return "RETRY";
}
```

### 5.4 SubagentStop Hook 활용

SubagentStop Hook으로 모든 Agent 완료 시 자동 검증:

```json
// settings.json
{
  "hooks": {
    "SubagentStop": [
      {
        "type": "command",
        "command": "./hooks/validate-subagent-result.sh"
      }
    ]
  }
}
```

```bash
#!/bin/bash
# hooks/validate-subagent-result.sh

# stdin으로 subagent 결과 받음
RESULT=$(cat)

# 1. Result Report 존재 확인
if ! echo "$RESULT" | grep -q "## Result Report"; then
  echo "ERROR: Missing Result Report" >&2
  exit 1
fi

# 2. Completed Items 확인
COMPLETED=$(echo "$RESULT" | grep -c "\[x\]")
if [ "$COMPLETED" -lt 1 ]; then
  echo "WARNING: No completed items found"
fi

# 3. Verification 결과 확인
if echo "$RESULT" | grep -q "Build: ❌\|TypeScript: ❌\|Tests: ❌"; then
  echo "ERROR: Verification failed" >&2
  exit 1
fi

echo "✅ Validation passed: $COMPLETED items completed"
```

---

## 6. Checklist-Driven Evaluation

> **핵심 원칙**: Agent Council/Codex를 매 Phase마다 호출하는 것보다, **명시적 Checklist + 자동 검증**이 더 효율적이고 확실하다.

### 6.1 Phase별 Completion Checklist

각 Phase의 예상 산출물을 **명시적으로 정의**:

```typescript
// orchestrator-config.ts
const PHASE_CHECKLISTS = {
  research: {
    required: [
      'existing_patterns.md',      // 기존 패턴 분석
      'dependencies.json',          // 의존성 목록
      'target_files.txt'            // 수정 대상 파일
    ],
    minToolCalls: 5,
    validation: (files) => files.every(f =>
      existsSync(f) && readFileSync(f).length > 100
    )
  },

  design: {
    required: [
      'design-doc.md',             // 설계 문서
      'api-spec.yaml',             // API 명세 (해당 시)
      'component-tree.md'          // 컴포넌트 구조 (해당 시)
    ],
    minToolCalls: 10,
    validation: (files) => files.some(f => existsSync(f))
  },

  implementation: {
    required: [
      'modified_files[]',          // 수정된 파일들
      'new_files[]',               // 새로 생성된 파일들
    ],
    minToolCalls: 15,
    validation: async (result) => {
      const buildPassed = await execAsync('npm run build');
      const typesPassed = await execAsync('npx tsc --noEmit');
      return buildPassed.status === 0 && typesPassed.status === 0;
    }
  },

  testing: {
    required: [
      'test_files[]',              // 테스트 파일
      'coverage_report'            // 커버리지 (선택)
    ],
    minToolCalls: 8,
    validation: async () => {
      const testResult = await execAsync('npm test');
      return testResult.status === 0;
    }
  }
};
```

### 6.2 Result Report 강제화

모든 Subagent는 **구조화된 Result Report**를 반환해야 함:

```markdown
## Result Report

### Session Info
| Key | Value |
|-----|-------|
| Session ID | {session-id} |
| Agent Name | {agent-name} |
| Task | {task} ({n}/{total}) |
| Status | ✅ COMPLETED / ⚠️ PARTIAL / ❌ FAILED |

### Completed Items
- [x] UserProfile 컴포넌트 생성 (src/components/UserProfile.tsx)
- [x] API route 추가 (app/api/users/route.ts)
- [x] 테스트 작성 (tests/UserProfile.test.tsx)
- [ ] 스토리북 스토리 (미완료 시 명시)

### Verification Results
| Check | Status | Details |
|-------|--------|---------|
| Build | ✅ passed | 0 errors |
| TypeScript | ✅ passed | 0 errors |
| Tests | ✅ passed | 3/3 passed |
| Lint | ⚠️ warning | 2 warnings |

### Files Modified
| File | Action | Lines | Description |
|------|--------|-------|-------------|
| src/components/UserProfile.tsx | created | 45 | 프로필 컴포넌트 |
| app/api/users/route.ts | created | 32 | API 엔드포인트 |

### Shared Context Verification
✅ **Original Goal**: {goal 명시}
✅ **Boundaries Respected**: 다른 Agent 파일 미수정

### Missing/Blocked (if any)
- (none) 또는
- ⚠️ 스토리북 설정 없어서 스토리 생성 불가
```

### 6.3 Orchestrator 자동 검증 로직

```
Phase N 완료
    │
    ▼
1. Result Report 파싱
    │
    ▼
2. Checklist 대조 (누락 항목 식별)
    │
    ├─ 필수 항목 누락? ──────────────────┐
    │                                     │
    ▼                                     ▼
3. 파일 실제 존재 확인 (Read tool)    RETRY with missing items
    │
    ├─ 파일 없음/빈 파일? ───────────────┐
    │                                     │
    ▼                                     ▼
4. 빌드/테스트 실행 (Bash)            RETRY with fix request
    │
    ├─ 실패? ────────────────────────────┐
    │                                     │
    ▼                                     ▼
5. Quality Score 계산              MODIFY or RETRY
    │
    ├─ < 90점? ──────────────────────────┘
    │
    ▼
✅ 다음 Phase로 CONTINUE
```

### 6.4 누락 방지를 위한 추가 검증

```typescript
async function verifyPhaseCompletion(
  phase: string,
  result: SubagentResult
): Promise<VerificationResult> {
  const checklist = PHASE_CHECKLISTS[phase];
  const issues: string[] = [];

  // 1. Result Report 존재 확인
  if (!result.includes('## Result Report')) {
    issues.push('Missing Result Report');
  }

  // 2. Completed Items 파싱
  const completedItems = parseCompletedItems(result);
  const expectedItems = checklist.required.length;

  if (completedItems.length < expectedItems * 0.8) {
    issues.push(`Only ${completedItems.length}/${expectedItems} items completed`);
  }

  // 3. 파일 실제 존재 확인
  for (const file of extractMentionedFiles(result)) {
    if (!await fileExists(file)) {
      issues.push(`File not found: ${file}`);
    }
  }

  // 4. 빌드/테스트 검증
  if (phase === 'implementation') {
    const buildResult = await runBuild();
    if (!buildResult.success) {
      issues.push(`Build failed: ${buildResult.error}`);
    }
  }

  // 5. 최소 도구 호출 수 확인
  const toolCallCount = countToolCalls(result);
  if (toolCallCount < checklist.minToolCalls) {
    issues.push(`Insufficient tool calls: ${toolCallCount} < ${checklist.minToolCalls}`);
  }

  return {
    passed: issues.length === 0,
    issues,
    score: calculateScore(issues)
  };
}
```

---

## 7. Agent Council & Codex 활용 전략

> **핵심**: Council과 Codex는 **평가(Evaluation)보다 기준 수립(Standard Setting)에 활용**하는 것이 효과적

### 7.1 효율적 활용 시점

| 시점 | 도구 | 용도 | 비용 |
|------|------|------|------|
| **Phase 0 (1회만)** | Codex | 프로젝트별 Quality Gate 조회/저장 | 낮음 |
| **2회 연속 실패 시** | Council | 실패 원인 분석 및 대안 제안 | 높음 (선택적) |
| **새 패턴 발견 시** | Codex | 베스트 프랙티스 저장 | 낮음 |

### 7.2 Phase 0: 기준 수립 (Codex)

작업 시작 전 **1회만** Codex로 Best Practice 조회:

```typescript
// Phase 0에서 1회만 실행
async function establishQualityGate(featureName: string) {
  const codexResult = await Task({
    subagent_type: "general-purpose",
    prompt: `
      mcp__codex__codex를 사용해서 다음을 조회해:

      1. "${featureName}" 구현 시 필요한 체크리스트
      2. 이전에 비슷한 작업에서 빠뜨렸던 항목
      3. 프로젝트 코딩 규칙 (coding-rules.md)

      결과를 JSON 형식으로 반환해.
    `
  });

  // 결과를 PHASE_CHECKLISTS에 병합
  return mergeWithDefaultChecklist(codexResult);
}
```

**Codex에 Quality Gate 저장 예시**:

```typescript
// 프로젝트별 Quality Gate를 Codex에 저장
await mcp__codex__codex({
  query: "branding-design-system feature 추가 체크리스트 저장",
  content: `
    ## Feature Addition Checklist (branding-design-system)

    ### 필수 항목
    - [ ] TypeScript 타입 정의 (.d.ts 또는 인라인)
    - [ ] 컴포넌트 Props 인터페이스
    - [ ] 단위 테스트 (최소 1개)
    - [ ] 빌드 통과 (npm run build)
    - [ ] 린트 통과 (npm run lint)

    ### 권장 항목
    - [ ] 스토리북 스토리
    - [ ] E2E 테스트 (UI 컴포넌트인 경우)
    - [ ] JSDoc 주석

    ### 이전 실패 패턴
    - 빌드 시 환경 변수 누락 (Lazy Initialization 필수)
    - 타입 정의 누락으로 tsc 실패
  `
});
```

### 7.3 실패 시에만 Council 소집

```typescript
// 2회 연속 RETRY 시에만 Council 호출 (비용 최적화)
async function handleRepeatedFailure(
  failedItems: string[],
  retryCount: number
) {
  if (retryCount < 2) {
    // 일반 RETRY
    return { action: 'RETRY', items: failedItems };
  }

  // Council 소집
  const councilResult = await Task({
    subagent_type: "agent-council",
    prompt: `
      ## 상황
      ${featureName} 구현 중 다음 항목이 ${retryCount}회 연속 실패:
      - ${failedItems.join('\n- ')}

      ## 이전 시도
      ${previousAttempts.map(a => `- ${a.approach}: ${a.result}`).join('\n')}

      ## 질문
      1. 왜 계속 실패하는지 원인 분석
      2. 근본적으로 다른 접근법 제안
      3. 이 실패 패턴을 Codex에 저장해야 하는지
    `
  });

  // Council 결과에 따라 접근법 변경
  return {
    action: 'MODIFY',
    newApproach: councilResult.recommendation
  };
}
```

### 7.4 활용 전략 요약

```
┌─────────────────────────────────────────────────────────────┐
│                    EVALUATION STRATEGY                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Phase 0 (1회)                                              │
│   ┌─────────────┐                                           │
│   │   Codex     │ → Quality Gate 조회/생성                   │
│   └─────────────┘                                           │
│         │                                                    │
│         ▼                                                    │
│   Phase 1~N (매번)                                           │
│   ┌─────────────┐                                           │
│   │  Checklist  │ → 명시적 항목 검증                         │
│   │  + 자동검증  │ → Build/Test/TypeScript                   │
│   └─────────────┘                                           │
│         │                                                    │
│         ├─ 통과 ─────────────────────────▶ 다음 Phase       │
│         │                                                    │
│         └─ 실패 (1회) ───────────────────▶ RETRY            │
│               │                                              │
│               └─ 실패 (2회+) ────────────▶ Council 소집     │
│                     │                                        │
│                     ▼                                        │
│               ┌─────────────┐                               │
│               │  Council    │ → 원인 분석, 대안 제안         │
│               └─────────────┘                               │
│                     │                                        │
│                     ▼                                        │
│               ┌─────────────┐                               │
│               │   Codex     │ → 새 패턴 저장 (선택)          │
│               └─────────────┘                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.5 비용 비교

| 방식 | Phase당 MCP 호출 | 총 호출 (5 Phase) | 효과 |
|------|------------------|-------------------|------|
| 매 Phase Council+Codex | 2회 | 10회 | Context 분산, 지연 |
| **Checklist + 선택적 호출** | 0~0.4회 | 1~2회 | 빠름, 일관성 |

---

## 8. Parallel Execution Patterns

### 8.1 독립 태스크 병렬화

```typescript
// 의존성 없는 태스크들은 병렬 실행
await Promise.all([
  Task({ subagent_type: "backend", prompt: schemaPrompt }),
  Task({ subagent_type: "frontend", prompt: uiPrompt }),
]);
```

### 8.2 의존성 있는 태스크 순차화

```typescript
// Schema → API → UI 순서 (의존성 있음)
const schemaResult = await Task({ prompt: schemaPrompt });
const apiResult = await Task({ prompt: apiPrompt, context: schemaResult });
const uiResult = await Task({ prompt: uiPrompt, context: apiResult });
```

### 8.3 Boundary 정의

```yaml
# 병렬 실행 시 파일 경계 명확히 정의
parallel_agents:
  - name: agent-schema
    allowed: ["supabase/migrations/", "types/database.ts"]
    forbidden: ["app/", "components/"]

  - name: agent-api
    allowed: ["app/api/", "lib/"]
    forbidden: ["components/", "supabase/"]

  - name: agent-ui
    allowed: ["components/", "app/(pages)/"]
    forbidden: ["app/api/", "supabase/"]
```

---

## 9. AB Test Results

### 9.1 테스트 설계

**테스트 일시**: 2026-01-21
**테스트 태스크**: 문자열 유틸리티 함수 3개 병렬 생성

| 버전 | 설명 |
|------|------|
| A (Control) | 단순 prompt만 제공 |
| B (Treatment) | Context Injection System 적용 |

### 9.2 결과

| 지표 | Version A | Version B | 개선 |
|------|-----------|-----------|------|
| Goal Retention | 0% | 100% | +100% |
| Boundary Compliance | 측정 불가 | 100% | 측정 가능 |
| Code Quality | 동등 | 동등 | - |
| Completion Rate | 100% | 100% | - |

### 9.3 정성적 발견

**Version A (기존 방식)**:
- Agent 완료 메시지: "Done. The file has been created..."
- Original Goal 언급 없음
- 다른 Agent 존재 인식 없음

**Version B (Context Injection)**:
- Agent 완료 메시지: "Original Goal (문자열 유틸리티 라이브러리)..."
- Shared Context Alignment 명시
- Boundaries Respected 확인

### 9.4 결론

> **Context Injection System은 Goal Retention과 Boundary Compliance를 유의미하게 개선한다.**

적용 권장 대상:
- autonomous-feature-builder (v3.1 적용 완료)
- autonomous-service-builder
- infinite-orchestrator
- 모든 병렬 Agent 실행 시나리오

---

## 참고 문서

- [autonomous-feature-builder SKILL.md](../../skills/autonomous-feature-builder/SKILL.md)
- [autonomous-feature-builder CHANGELOG.md](../../skills/autonomous-feature-builder/CHANGELOG.md)
- [Context Injection Templates](../../templates/context-injection/)
- [AB Test Results](../../ab-test/context-injection-test/results/comparison.md)

---

**문서 관리**:
- 이 문서는 새로운 원칙이 추가되거나 AB Test가 완료될 때 업데이트됩니다.
- 변경 시 버전 번호와 날짜를 갱신하세요.
