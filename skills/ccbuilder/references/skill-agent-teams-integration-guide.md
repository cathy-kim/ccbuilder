# Skill + Agent Teams 통합 패턴 가이드

> 기존 스킬에 Agent Teams 모드를 추가하는 실전 패턴 가이드

**Version**: 1.0.0
**Last Updated**: 2026-03-03
**Claude Code Version**: v2.1.63+

---

## 1. 언제 Agent Teams를 스킬에 추가해야 하는가?

### 결정 체크리스트

아래 조건 중 **3개 이상** 해당하면 Agent Teams 적용을 권장:

- [ ] 3개 이상 독립적으로 병렬 실행 가능한 Phase가 존재
- [ ] Phase 간 파일 소유권 경계가 명확 (디렉토리/모듈 단위)
- [ ] 단일 에이전트 실행 시 컨텍스트 누적으로 품질 저하 발생
- [ ] Evaluation Loop (CONTINUE/MODIFY/RETRY) 패턴이 이미 존재
- [ ] 현재 Task() 단독으로 병렬 위임하지만 상태 공유가 필요

### Agent Teams vs Task() 단독

| 항목 | Task() 단독 | Agent Teams |
|------|------------|-------------|
| 에이전트 수명 | 1회성 (fire-and-forget) | 지속 (팀 해산까지) |
| 상태 공유 | 없음 (결과 반환만) | 공유 TaskList |
| 통신 | 결과 반환만 | DM, broadcast, shutdown |
| 컨텍스트 | 부모 컨텍스트 누적 | 각 Teammate 독립 컨텍스트 |
| MODIFY 지시 | 불가 (재생성 필요) | SendMessage로 즉시 가능 |
| 비용 | Task 건당 | Teammate 활성 시간 기준 |
| 적합 시나리오 | 독립적 단순 병렬 | 복잡한 협업, 긴 워크플로우 |

### 적용하지 말아야 하는 경우

- Phase가 2개 이하인 단순 스킬
- 모든 Phase가 순차적이고 컨텍스트 누적이 문제되지 않는 경우
- Task() 결과만으로 충분한 독립 병렬 작업 (예: 번역, 포맷 변환)

---

## 2. SKILL.md 수정 패턴

### Step 1: frontmatter allowed-tools 추가

```yaml
allowed-tools:
  # ... 기존 도구들 유지 ...
  - TeamCreate      # 팀 생성
  - TeamDelete      # 팀 해산
  - SendMessage     # 팀 내 통신
  - TaskCreate      # 작업 생성
  - TaskUpdate      # 작업 상태/소유자/의존성 관리
  - TaskList        # 전체 작업 목록 조회
  - TaskGet         # 개별 작업 상세 조회
```

### Step 2: 모드 선택 섹션 추가 (15줄 이내)

Core Principles 바로 아래에 추가. **반드시 상세는 references/로 분리**:

```markdown
### Agent Team Mode (NEW - vX.Y.0)

[스킬 특화 설명 1줄]:

| 모드 | 적합한 경우 | 상세 |
|------|------------|------|
| **default** | [기본 시나리오] | Task() 병렬 (기존 방식) |
| **agent-team** | [팀 시나리오] | [references/agent-team-mode.md](references/agent-team-mode.md) |

**키워드**: `--mode=team`, `팀 모드로`
```

### Step 3: references/agent-team-mode.md 생성

[autonomous-service-builder/references/agent-team-mode.md](../../../autonomous-service-builder/references/agent-team-mode.md)를 canonical 템플릿으로 사용. 필수 섹션:

```
# Agent Team Mode - [스킬명]
## 개요           ← 팀 구성 ASCII 다이어그램
## 사전 요구사항   ← settings.json 설정
## 실행 흐름       ← Phase별 TeamCreate/TaskCreate/Agent 코드
## 의존성 그래프   ← ASCII 그래프 + 최대 병렬 수
## Evaluation     ← 시점별 검증 테이블
## 비용 최적화     ← Teammate별 모델 선택 (sonnet/haiku)
## Cleanup        ← shutdown_request 루프 + TeamDelete
```

### Step 4: 버전 업데이트

- SKILL.md Version 헤더: MINOR 버전 증가 (새 기능)
- CHANGELOG.md에 `[vX.Y.0]` 엔트리 추가
- releases/에 이전 SKILL.md 백업

---

## 3. 스킬 유형별 팀 구성 템플릿

### Archetype A: Phase-wave (설계-구현-검증)

```
Team Lead
├── "planner" (Phase 1)
│   └── 완료 → designer-1, designer-2, designer-3 unblock
├── "designer-1" (Phase 2)     ← 병렬
├── "designer-2" (Phase 3)     ← 병렬
├── "designer-3" (Phase 4)     ← 병렬
│   └── 모두 완료 → implementer unblock
├── "implementer" (Phase 5)
│   └── 완료 → tester unblock
└── "tester" (Phase 6)
```

**예시**: autonomous-service-builder (DB + API + UI 병렬 설계)
**최대 병렬**: 3-4, **총 Teammate**: 5-7

### Archetype B: Batch-parallel (대량 병렬 생성)

```
Team Lead
├── "planner" (Phase 1)
│   └── 완료 → Batch 1 전체 unblock
├── Batch 1 (병렬 N개):
│   ├── "writer-1" ... "writer-N"
│   └── Batch 1 완료 → Batch 2 unblock
├── Batch 2 (병렬 M개):
│   ├── "producer-1" ... "producer-M"
│   └── Batch 2 완료 → Reviewers unblock
└── Reviewers (병렬 K개):
    └── "reviewer-1" ... "reviewer-K"
```

**예시**: content-marketing-orchestrator (5 writers → 4 producers → 3 reviewers)
**최대 병렬**: N (Batch 크기), **총 Teammate**: N+M+K+1

### Archetype C: Sequential-chain (컨텍스트 격리)

```
Team Lead
├── "step-1" (Phase 1)
│   └── 완료 → step-2 unblock
├── "step-2" (Phase 2)
│   └── 완료 → step-3 unblock
├── "step-3" (Phase 3)
│   └── 완료 → reviewer unblock
└── "reviewer" (Phase 4)
```

**예시**: video-editing-orchestrator (Director → Editor → Assembly → Review)
**핵심 가치**: 병렬이 아닌 **컨텍스트 격리** — 60분+ 영상 등 대용량 처리 시 각 Phase 독립 컨텍스트
**최대 병렬**: 1-2, **총 Teammate**: 3-5

---

## 4. 태스크 분해 패턴

### Phase-based 의존성

```typescript
// Phase 2, 3, 4는 Phase 1 완료 후 병렬 실행
TaskCreate({ subject: "Phase 1: Planning", ... })        // id: "1"
TaskCreate({ subject: "Phase 2: DB Design", ... })       // id: "2"
TaskCreate({ subject: "Phase 3: API Design", ... })      // id: "3"
TaskCreate({ subject: "Phase 4: UI Design", ... })       // id: "4"

TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "3", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "4", addBlockedBy: ["1"] })
```

```
[1] Planning
 ├──→ [2] DB Design   ← 병렬
 ├──→ [3] API Design  ← 병렬
 └──→ [4] UI Design   ← 병렬
```

### Batch-based 의존성

```typescript
// Batch 1: 5개 병렬, 모두 planner 완료 후
for (const id of ["2","3","4","5","6"]) {
  TaskUpdate({ taskId: id, addBlockedBy: ["1"] })
}
// Batch 2: Batch 1 전체 완료 후
for (const id of ["7","8","9","10"]) {
  TaskUpdate({ taskId: id, addBlockedBy: ["2","3","4","5","6"] })
}
```

```
[1] Planner
 ├──→ [2][3][4][5][6] Batch 1 (병렬 5개)
 │         모두 완료
 └──→ [7][8][9][10] Batch 2 (병렬 4개)
```

### Sequential Chain 의존성

```typescript
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })
TaskUpdate({ taskId: "3", addBlockedBy: ["2"] })
TaskUpdate({ taskId: "4", addBlockedBy: ["3"] })
```

```
[1] → [2] → [3] → [4]  (순차, 각 독립 컨텍스트)
```

---

## 5. Context Injection 템플릿

### Shared Context (팀 전체 공유)

Agent 프롬프트에 포함하는 공통 정보:

```typescript
const sharedContext = `
## Shared Context
- 프로젝트: ${projectName}
- 브랜드: ${brandName}
- 기술 스택: ${techStack}
- 품질 기준: ${qualityCriteria}
- 팀 이름: ${teamName}
`;
```

### Individual Context (역할별)

```typescript
Agent({
  subagent_type: "backend",
  team_name: teamName,
  name: "api-designer",
  prompt: `
    ${sharedContext}

    ## Your Mission
    API 엔드포인트 설계. REST 패턴 준수.

    ## Owned Files
    - app/api/**
    - types/api.ts

    ## Interface Contract (읽기 전용)
    - types/database.ts (db-architect 소유)

    ## 완료 시
    1. TaskUpdate({ taskId: "3", status: "completed" })
    2. SendMessage to Lead: 결과 요약
  `
})
```

### Teammate 간 직접 통신

```typescript
// api-designer가 db-architect에게 스키마 확인 요청
SendMessage({
  type: "message",
  recipient: "db-architect",
  content: "users 테이블에 role 컬럼 추가 가능한가요?",
  summary: "Schema change request"
})
```

---

## 6. Evaluation + Shutdown 워크플로우

### Teammate 완료 시 (Teammate가 실행)

```typescript
// 1. Task 완료 표시
TaskUpdate({ taskId: myTaskId, status: "completed" })

// 2. Lead에게 결과 보고
SendMessage({
  type: "message",
  recipient: "team-lead",  // 또는 Lead 이름
  content: "Phase 2 완료. 결과: ...",
  summary: "Phase 2 DB design completed"
})
```

### Lead의 검증 판단

| 점수 | 판단 | 액션 |
|------|------|------|
| ≥ 90 | CONTINUE | 다음 Phase unblock |
| 60-89 | MODIFY | SendMessage로 수정 지시 |
| < 60 | RETRY | 새 Teammate 생성 또는 재지시 |

```typescript
// MODIFY 예시
SendMessage({
  type: "message",
  recipient: "api-designer",
  content: "인증 미들웨어 누락. auth-middleware.ts 추가 필요.",
  summary: "MODIFY: add auth middleware"
})
```

### Shutdown 워크플로우

```typescript
// 모든 Task 완료 확인 후
const teammates = ["planner", "designer", "implementer", "tester"];

for (const name of teammates) {
  SendMessage({
    type: "shutdown_request",
    recipient: name,
    content: "모든 작업 완료. 팀 해산합니다."
  })
}

// 모든 shutdown_response 수신 후
TeamDelete()
```

---

## 7. Before/After 예시

### 예시 A: Batch-parallel (Content Marketing Orchestrator)

**Before (Task() 단독)**:
```typescript
// 5개 Task 동시 호출 — 결과만 받고 끝
Task({ subagent_type: "cmo-newsletter-writer", prompt: "..." })
Task({ subagent_type: "cmo-blog-writer", prompt: "..." })
Task({ subagent_type: "cmo-linkedin-writer", prompt: "..." })
// 품질 미달 시 전체 재생성 필요
```

**After (Agent Teams)**:
```typescript
TeamCreate({ team_name: "cmo-content" })

// 5개 Teammate 병렬 생성 — 독립 컨텍스트, 공유 TaskList
Agent({ subagent_type: "cmo-newsletter-writer", team_name: "cmo-content", name: "newsletter-writer", ... })
// ...

// 품질 미달 시 해당 writer에게만 MODIFY 지시
SendMessage({ type: "message", recipient: "blog-writer", content: "CTA 추가 필요", summary: "MODIFY blog" })
```

### 예시 B: Sequential-chain (Video Editing Orchestrator)

**Before (Task() 체인)**:
```typescript
const plan = await Task({ subagent_type: "general-purpose", prompt: "Story plan..." })
// plan 결과가 부모 컨텍스트에 누적
const edits = await Task({ subagent_type: "general-purpose", prompt: `${plan}\nEdit decisions...` })
// 60분 영상 분석 결과 + 편집 결과 = 컨텍스트 폭발
```

**After (Agent Teams)**:
```typescript
TeamCreate({ team_name: "veo-edit" })
// 각 Teammate가 독립 컨텍스트에서 작업
Agent({ team_name: "veo-edit", name: "video-director", prompt: "Story plan..." })
// director 완료 → editor에게 결과 파일 경로만 전달 (컨텍스트 격리)
Agent({ team_name: "veo-edit", name: "video-editor", prompt: "Read plan from file, make edit decisions..." })
```

---

## 참고

- Agent Teams 기본 개념: [agent-teams-guide.md](agent-teams-guide.md)
- 오케스트레이터 원칙: [orchestrator-principles.md](orchestrator-principles.md)
- Best Practices: [best-practices.md](best-practices.md) Section 4
- Canonical 템플릿: `autonomous-service-builder/references/agent-team-mode.md`

---

*Skill + Agent Teams Integration Guide v1.0.0 | 2026-03-03*
