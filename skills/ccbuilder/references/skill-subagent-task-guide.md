# Skill / Subagent / Task 사용 가이드 (v2.1+)

> **최종 업데이트**: 2026-02-11
> **Claude Code 버전**: v2.1.39+

---

## Deprecated 기능 안내

### 2025-12 ~ 2026-01 변경 사항

| Deprecated | 대체 방법 | 비고 |
|------------|-----------|------|
| `output styles` | `--system-prompt-file` 또는 `plugins` | CLI 출력 스타일 |
| `legacy SDK entrypoint` | `@anthropic-ai/claude-agent-sdk` | SDK 마이그레이션 필수 |
| `includeCoAuthoredBy` 설정 | `attribution` 설정 | 커밋/PR 바이라인 |
| Windows `C:\ProgramData\ClaudeCode\` | `C:\Program Files\ClaudeCode\` | 관리 설정 경로 |
| `$ARGUMENTS.0` 문법 | `$ARGUMENTS[0]` 사용 | v2.7 Breaking Change |

### Slash Commands & Skills 통합

- **변경**: Slash commands와 Skills가 통합됨
- **영향**: `commands/` 폴더는 계속 지원되지만, 새 구현은 `skills/` 권장
- **네이밍**: `.claude/commands/frontend/component.md` → `/frontend:component`
- **Skills**: `userInvocable: true` 시 `/skill-name`으로 호출 가능

---

## 핵심 개념 비교

| 구분 | Skill | Subagent | Task Tool |
|------|-------|----------|-----------|
| **역할** | 지식/가이드 제공 | 독립 실행 에이전트 정의 | 에이전트 실행 도구 |
| **컨텍스트** | 현재 대화 (fork 시 별도) | 별도 200k 컨텍스트 | 별도 200k 컨텍스트 |
| **지속성** | 세션 간 유지 | 정의 파일로 유지 | 일회성 실행 |
| **도구 제한** | allowed-tools (CLI만) | 정의에서 제한 | subagent 정의 따름 |
| **용도** | "이렇게 해라" 지침 | "이 에이전트는 이렇다" | "지금 실행해라" |
| **Agent Team** | 멀티 에이전트 팀 협업 | 각 Teammate 별도 컨텍스트 | TeamCreate로 생성 |

---

## ⭐ Skill ↔ Subagent 양방향 통합 아키텍처 (v2.1.19)

Claude Code에서 Skills와 Subagents는 **양방향으로 통합**됩니다:

| 접근 방식 | System Prompt | Task (작업) | 추가 로드 |
|-----------|---------------|-------------|-----------|
| **Skill + `context: fork`** | agent 타입에서 (Explore, Plan 등) | SKILL.md 내용 | CLAUDE.md |
| **Subagent + `skills` 필드** | Subagent markdown body | Claude 위임 메시지 | Preloaded skills + CLAUDE.md |

### 방향 1: Skill에서 Subagent 호출 (`context: fork`)

Skill 내용이 **작업(Task)**이 되고, 지정된 agent가 **실행 환경**을 제공합니다.

```yaml
---
name: deep-research
description: 주제를 철저히 조사
context: fork          # 별도 컨텍스트에서 실행
agent: Explore         # Explore 에이전트 사용
---

$ARGUMENTS를 철저히 조사:

1. Glob, Grep으로 관련 파일 찾기
2. 코드 분석
3. 파일 참조와 함께 결과 요약
```

**실행 흐름**:
1. 새로운 격리된 컨텍스트 생성
2. Subagent가 SKILL.md 내용을 프롬프트로 받음
3. `agent` 필드가 실행 환경(모델, 도구, 권한) 결정
4. 결과가 요약되어 메인 대화로 반환

### 방향 2: Subagent에서 Skills 프리로드 (`skills` 필드)

Subagent의 markdown body가 **system prompt**가 되고, skills가 **참조 자료**로 주입됩니다.

```yaml
---
name: api-developer
description: 팀 컨벤션에 따라 API 엔드포인트 구현
skills:
  - api-conventions
  - error-handling-patterns
---

API 엔드포인트를 구현합니다. 프리로드된 스킬의 컨벤션과 패턴을 따르세요.
```

**핵심 차이점**:
- Subagent는 부모 대화의 스킬을 **상속하지 않음**
- `skills` 필드에 명시적으로 나열해야 함
- 전체 스킬 내용이 시작 시 주입됨 (호출 가능 상태가 아닌 컨텍스트에 존재)

### 통합 패턴 선택 가이드

```
Q: 누가 실행을 제어하나?
├─ Skill 내용이 작업을 정의 → context: fork + agent 사용
│   예: "/deep-research 인증 모듈" → Skill이 작업, Explore가 실행
│
└─ Subagent가 실행을 제어 → skills 필드로 지식 주입
    예: "api-developer로 엔드포인트 구현" → Subagent가 작업, skills가 참조

---

## 1. Skill (스킬)

### 용도
- 반복되는 지침, 도메인 전문 지식, 코딩 패턴 제공
- 현재 대화 컨텍스트에 지식 주입
- 슬래시 명령으로 직접 호출 (`/skill-name`)

### 위치
- `~/.claude/skills/` (전역)
- `.claude/skills/` (프로젝트)

### 최신 SKILL.md Frontmatter (v2.1+)

```yaml
---
name: my-skill                        # 필수
description: "스킬 설명 + 자동 활성화 키워드"  # 필수
userInvocable: true                   # /my-skill 로 직접 호출 가능

# 도구 제한 (CLI에서만 작동, SDK는 별도 설정 필요)
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit

# 실행 컨텍스트 (선택)
context: fork                         # 별도 컨텍스트에서 실행

# 에이전트 타입 지정 (선택)
agent: backend                        # 특정 에이전트로 실행

# 다른 스킬 함께 로드 (선택)
skills:
  - design-system
  - testing-patterns

# 내장 Hooks (선택)
hooks:
  - type: PreToolUse
    tool: Bash
    script: ./hooks/validate.sh
  - type: Stop
    script: ./hooks/cleanup.sh
    once: true                        # 세션당 1회만 실행

# 추가 옵션
version: "1.0.0"                      # 버전 추적용 메타데이터
disable-model-invocation: false       # true면 자동 호출 방지, 수동만 가능
mode: false                           # true면 "Mode Commands" 섹션에 표시
---

# My Skill

## 목적
이 스킬의 목적 설명

## 지침
1. 첫 번째 단계
2. 두 번째 단계

## 참조
상세 내용은 `references/` 폴더 참조
```

### Frontmatter 옵션 정리 (v2.1.19 공식 문서 기준)

| 옵션 | 타입 | 설명 | 기본값 |
|------|------|------|--------|
| `name` | string | 스킬 이름 (소문자, 숫자, 하이픈만, 최대 64자) | 디렉토리 이름 |
| `description` | string | 설명 + 자동 활성화 키워드 | **권장** |
| `argument-hint` | string | 자동완성 시 표시될 인자 힌트 (예: `[issue-number]`) | - |
| `disable-model-invocation` | boolean | `true`면 Claude 자동 호출 방지, 수동만 가능 | `false` |
| `user-invocable` | boolean | `false`면 `/` 메뉴에서 숨김 (배경 지식용) | `true` |
| `allowed-tools` | string[] | 허용된 도구 목록 (CLI만) | 모든 도구 |
| `model` | string | 스킬 활성화 시 사용할 모델 | - |
| `context` | "fork" | 별도 forked subagent 컨텍스트에서 실행 | - |
| `agent` | string | `context: fork` 시 사용할 subagent 타입 | `general-purpose` |
| `hooks` | object | 스킬 생명주기 스코프 Hooks | - |

### 호출 제어 조합표

| Frontmatter | 사용자 호출 | Claude 호출 | 컨텍스트 로드 시점 |
|-------------|------------|-------------|-------------------|
| (기본값) | ✅ | ✅ | description 항상, 전체는 호출 시 |
| `disable-model-invocation: true` | ✅ | ❌ | description 미포함, 사용자 호출 시만 |
| `user-invocable: false` | ❌ | ✅ | description 항상, 호출 시 전체 |

### 문자열 치환 변수

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | 스킬 호출 시 전달된 모든 인자 |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID (로깅, 세션별 파일 생성용) |

### 동적 컨텍스트 주입 (`!`command``)

Shell 명령을 실행하고 결과를 스킬 내용에 주입:

```yaml
---
name: pr-summary
context: fork
agent: Explore
---

## PR 컨텍스트
- PR diff: !`gh pr diff`
- 변경된 파일: !`gh pr diff --name-only`

## 작업
이 PR을 요약하세요...
```

### Hot Reload (v2.1+)

```bash
# 스킬 수정 시 자동 반영 - 재시작 불필요!
echo "수정" >> .claude/skills/my-skill/SKILL.md
# 즉시 활성화됨
```

### SDK 제한 사항

```
⚠️ allowed-tools frontmatter는 CLI에서만 작동
   SDK 사용 시 query 설정의 allowedTools 옵션 사용
```

---

## 2. Subagent (서브에이전트)

### 용도
- 특정 역할의 독립 에이전트 정의
- 도구 제한, 스킬 연결, 커스텀 지침
- 별도 200k 컨텍스트에서 독립 실행

### 위치 및 우선순위

| 위치 | 스코프 | 우선순위 |
|------|--------|----------|
| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |
| `.claude/agents/` | 현재 프로젝트 | 2 |
| `~/.claude/agents/` | 모든 프로젝트 | 3 |
| Plugin의 `agents/` | 플러그인 활성화된 곳 | 4 (최저) |

### Frontmatter 옵션 (v2.1.19)

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | ✅ | 고유 식별자 (소문자, 하이픈) |
| `description` | ✅ | Claude가 언제 위임할지 결정하는 설명 |
| `tools` | - | 허용 도구 목록 (생략 시 전체 상속) |
| `disallowedTools` | - | 거부할 도구 목록 (상속/지정 목록에서 제거) |
| `model` | - | `sonnet`, `opus`, `haiku`, `inherit` (기본: inherit) |
| `permissionMode` | - | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `skills` | - | 시작 시 컨텍스트에 주입할 스킬 목록 |
| `hooks` | - | 이 subagent 스코프의 생명주기 훅 |

### 에이전트 정의 파일 예시

```yaml
---
name: frontend-developer
description: "React/Next.js 프론트엔드 개발 전문. 코드 변경 후 적극적으로 사용."
model: sonnet

# 도구 제한
tools: Read, Write, Edit, Glob, Grep, Bash

# 스킬 프리로드 (전체 내용이 컨텍스트에 주입됨)
skills:
  - frontend-design-system
  - testing-patterns

# 생명주기 Hooks
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint-check.sh"
---

# Frontend Developer Agent

## 역할
React/Next.js 기반 프론트엔드 개발을 담당합니다.

## 규칙
1. TypeScript 사용 필수
2. 컴포넌트는 함수형으로 작성
3. 테스트 코드 함께 작성
```

### 내장 Subagent 타입

| subagent_type | 용도 | 모델 | 특징 |
|---------------|------|------|------|
| `Explore` | 코드베이스 탐색 | Haiku | 읽기 전용, 빠름, 저비용 |
| `Plan` | 구현 계획 설계 | 상속 | Plan mode에서 리서치 |
| `general-purpose` | 복잡한 멀티스텝 작업 | 상속 | 모든 도구 접근 |
| `claude-code-guide` | Claude Code 문서 조회 | Haiku | 공식 문서 검색 |
| `Bash` | 터미널 명령 실행 | 상속 | 별도 컨텍스트에서 명령 실행 |
| `statusline-setup` | 상태 표시줄 설정 | Sonnet | /statusline 실행 시 |

### Explore 세부 옵션

```typescript
// Claude가 thoroughness level 자동 결정:
// - quick: 타겟 검색
// - medium: 균형 잡힌 탐색
// - very thorough: 포괄적 분석
Task({
  description: "Quick search",
  prompt: "로그인 핸들러 찾기",
  subagent_type: "Explore"
})
```

### Permission Modes

| 모드 | 동작 |
|------|------|
| `default` | 표준 권한 확인 (프롬프트 표시) |
| `acceptEdits` | 파일 편집 자동 승인 |
| `dontAsk` | 권한 프롬프트 자동 거부 (명시적 허용 도구는 작동) |
| `bypassPermissions` | 모든 권한 체크 스킵 ⚠️ |
| `plan` | Plan mode (읽기 전용 탐색) |

---

## 3. Task Tool (태스크 도구)

### 용도
- Subagent를 실제로 실행하는 도구
- 별도 200k 컨텍스트에서 독립 실행

### 기본 스키마

```typescript
Task({
  description: string,        // 5단어 이내 설명 (필수)
  prompt: string,             // 수행할 작업 상세 설명 (필수)
  subagent_type: string,      // 에이전트 타입 (필수)
  model?: "sonnet" | "opus" | "haiku",  // 선택
  run_in_background?: boolean,          // 백그라운드 실행
  resume?: string             // 이전 에이전트 ID로 재개
})
```

### 사용 예시

```typescript
// 1. 코드베이스 탐색 (빠름, 저비용)
Task({
  description: "Find auth handlers",
  prompt: "인증 관련 핸들러 파일들을 찾고 구조를 분석해줘",
  subagent_type: "Explore",
  model: "haiku"
})

// 2. 복잡한 구현 작업
Task({
  description: "Implement login feature",
  prompt: "JWT 기반 로그인 기능을 구현해줘. 기존 auth/ 폴더 패턴을 따라서.",
  subagent_type: "backend"
})

// 3. 병렬 실행 (단일 메시지에 여러 Task = 동시 실행)
Task({ subagent_type: "frontend", prompt: "UI 컴포넌트 작성" })
Task({ subagent_type: "backend", prompt: "API 엔드포인트 작성" })
Task({ subagent_type: "qa-expert", prompt: "테스트 케이스 작성" })

// 4. 백그라운드 실행
Task({
  description: "Run long analysis",
  prompt: "전체 코드베이스 분석",
  subagent_type: "Explore",
  run_in_background: true  // Ctrl+B로도 전환 가능
})

// 5. 커스텀 에이전트 호출
Task({
  description: "Build React component",
  prompt: "대시보드 컴포넌트를 만들어줘",
  subagent_type: "frontend-developer"  // .claude/agents/frontend-developer.md
})

// 6. 에이전트 재개
Task({
  description: "Continue previous work",
  prompt: "이전 작업 계속",
  subagent_type: "frontend-developer",
  resume: "agent-123-abc"  // 이전 agent_id
})
```

### Foreground vs Background 실행

| 실행 모드 | 특징 |
|-----------|------|
| **Foreground** | 메인 대화 블록, 권한 프롬프트 전달, 질문 가능 |
| **Background** | 동시 실행, 부모 권한 상속, 미승인 권한/질문 시 실패 후 계속, MCP 도구 불가 |

```bash
# Background 전환
- Ctrl+B: 실행 중인 작업을 백그라운드로
- CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1: 비활성화

# Background 실패 시 Foreground에서 resume 가능
```

---

## 4. Agent Teams (v2.7 신규)

### 용도
- 여러 에이전트가 팀으로 협업
- 공유 Task List로 작업 조율
- Team Lead가 Teammate 생성/관리

### 핵심 도구

| 도구 | 용도 |
|------|------|
| `TeamCreate` | 팀 생성 (team_name, description) |
| `TaskCreate` | 작업 생성 (subject, description, activeForm) |
| `TaskUpdate` | 상태 변경, 소유자 할당, 의존성 설정 |
| `TaskList` | 전체 작업 목록 조회 |
| `TaskGet` | 개별 작업 상세 조회 |
| `SendMessage` | DM, 브로드캐스트, 종료 요청 |
| `TeamDelete` | 팀 리소스 정리 |

### 워크플로우

```typescript
// 1. 팀 생성
TeamCreate({ team_name: "feature-team" })

// 2. 작업 생성 및 의존성 설정
TaskCreate({ subject: "Build API", description: "..." })
TaskCreate({ subject: "Build UI", description: "..." })
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })

// 3. Teammate 생성
Task({ subagent_type: "backend", team_name: "feature-team", name: "api-dev", prompt: "..." })
Task({ subagent_type: "frontend", team_name: "feature-team", name: "ui-dev", prompt: "..." })

// 4. 작업 할당
TaskUpdate({ taskId: "1", owner: "api-dev" })

// 5. 완료 후 정리
SendMessage({ type: "shutdown_request", recipient: "api-dev" })
TeamDelete()
```

### Agent Teams vs Task Tool 단독

| 기능 | Task Tool (단독) | Agent Teams |
|------|-----------------|-------------|
| 에이전트 수명 | 단발성 | 지속적 |
| 상태 공유 | 없음 | 공유 Task List |
| 커뮤니케이션 | 결과만 반환 | DM, 브로드캐스트 |
| 비용 | 작업당 | 활성 시간 내내 |
| 적합한 경우 | 단순 병렬 작업 | 복잡한 협업 |

**상세**: [agent-teams-guide.md](agent-teams-guide.md)

---

## 사용 시나리오 결정 가이드

```
Q: 반복적으로 같은 지침이 필요한가?
├─ Yes → Skill 생성
│  Q: 슬래시 명령으로 호출하고 싶은가?
│  ├─ Yes → userInvocable: true
│  └─ No → userInvocable: false (자동 활성화만)
└─ No
   Q: 여러 에이전트가 병렬로 협업해야 하나?
   ├─ Yes → Agent Team (TeamCreate + Task + SendMessage)
   └─ No
      Q: 독립적인 작업 실행이 필요한가?
      ├─ Yes → Task Tool 사용
      │  Q: 커스텀 에이전트가 필요한가?
      │  ├─ Yes → .claude/agents/ 에 정의 후 Task에서 호출
      │  └─ No → 내장 subagent_type 사용
      │     Q: 읽기 전용 탐색인가?
      │     ├─ Yes → Explore (haiku, 빠름)
      │     └─ No
      │        Q: 계획 수립인가?
      │        ├─ Yes → Plan
      │        └─ No → general-purpose
      └─ No → 직접 대화에서 처리
```

---

## 조합 예시

### 프로젝트 구조

```
.claude/
├── skills/
│   └── react-patterns/
│       ├── SKILL.md          # React 코딩 패턴 지침
│       └── references/
│           └── hooks.md
├── agents/
│   └── react-developer.md    # skills: [react-patterns] 포함
├── rules/
│   └── coding-rules.md       # 자동 로드되는 규칙
└── settings.json
```

### 호출

```typescript
// react-developer 에이전트가 react-patterns 스킬을 자동 로드
Task({
  description: "Build dashboard component",
  prompt: "대시보드 컴포넌트를 만들어줘",
  subagent_type: "react-developer"
})
```

---

## 제약 사항

| 제약 | 값 | 비고 |
|------|-----|------|
| 최대 동시 Task | 10개 | 초과 시 큐잉 |
| Task 컨텍스트 | 200k 토큰 | 메인과 분리 |
| 중첩 금지 | - | Subagent 중첩 불가 (Agent Teams의 Teammate는 별도) |
| Hook 스코프 | Skill/Agent 생명주기 | 해당 컴포넌트 실행 중에만 |
| allowed-tools | CLI만 지원 | SDK는 별도 설정 |
| Background MCP | 불가 | Background subagent에서 MCP 도구 사용 불가 |
| Skills 상속 | 불가 | Subagent는 부모 스킬 자동 상속 안됨, 명시적 나열 필요 |
| Skill char budget | 15,000 | 스킬 description 총합 제한 (`SLASH_COMMAND_TOOL_CHAR_BUDGET`로 조정) |

### Auto-Compaction

Subagent는 약 95% 용량에서 자동 compaction 실행:
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`: 더 낮은 비율로 조기 compaction 가능
- Transcript 파일: `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`

---

## 베스트 프랙티스

### Skill 작성 시

1. **Progressive Disclosure**: SKILL.md < 500줄, 상세는 `references/`
2. **키워드 포함**: description에 자동 활성화 키워드
3. **도구 제한**: 필요한 도구만 allowed-tools에 (CLI 사용 시)
4. **Hot Reload 활용**: 수정 후 재시작 불필요
5. **YAML 문법 주의**: frontmatter는 `---`로 시작/종료, 탭 대신 스페이스

### Subagent 정의 시

1. **역할 명확화**: 하나의 도메인에 집중
2. **스킬 연결**: 관련 스킬을 skills 필드에
3. **도구 최소화**: 필요한 도구만 허용
4. **모델 선택**: 복잡도에 따라 haiku/sonnet/opus

### Task 호출 시

1. **Explore 우선**: 탐색 작업은 Explore + haiku
2. **병렬 활용**: 독립 작업은 동시 호출 (단일 메시지에 여러 Task)
3. **백그라운드**: 긴 작업은 run_in_background
4. **프롬프트 명확화**: 구체적인 지시 제공
5. **에이전트 재개**: resume 옵션으로 이전 작업 계속

---

## 참고 문서

### 공식 문서 (Primary)
- [Skills Documentation](https://code.claude.com/docs/en/skills) - Skill 생성, frontmatter, context:fork
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents) - Subagent 정의, skills 프리로드
- [Hooks Documentation](https://code.claude.com/docs/en/hooks) - Hook 이벤트, 입력/출력 스키마
- [Plugins Documentation](https://code.claude.com/docs/en/plugins) - 플러그인 배포
- [Documentation Index](https://code.claude.com/docs/llms.txt) - 전체 문서 인덱스

### 추가 리소스
- [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Agent Skills Open Standard](https://agentskills.io) - 크로스 플랫폼 스킬 표준

---

## 변경 이력

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-02-11 | v2.1.39+ | Agent Teams, Task Management, Memory, Breaking Changes 추가 |
| 2026-01-24 | v2.1.19 | Skill↔Subagent 양방향 통합 문서화, frontmatter 옵션 업데이트 |
| 2026-01-15 | v2.1.x | 초기 가이드 작성 |
