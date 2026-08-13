# Subagents 상세 가이드

> Claude Code Subagents 및 Plugin System 개발 완전 가이드

**Version**: 2.14.0
**Last Updated**: 2026-08-13
**Claude Code Version**: v2.1.231+

---

## 내장 Subagent 타입

| subagent_type | 용도 | 특징 |
|---------------|------|------|
| `Explore` | 코드베이스 탐색 | 읽기 전용, Haiku 기반, 빠름 |
| `Plan` | 구현 계획 설계 | 아키텍처 분석 |
| `general-purpose` | 복잡한 멀티스텝 작업 | 모든 도구 접근 |
| `Bash` | 명령어 실행 전문 | Bash 도구만 |
| `claude-code-guide` | Claude Code 문서 조회 | 공식 문서 검색 |

> **v2.1.140+**: `subagent_type`은 대소문자·구분자 무관 매칭 — `"Code Reviewer"`, `"code_reviewer"`, `"code-reviewer"` 모두 동일하게 해석됨

> **v2.1.172+**: 서브에이전트 재귀 파견 지원 — 서브에이전트가 자체 서브에이전트를 파견 가능, 최대 5레벨 깊이
>
> **v2.1.217 Breaking Change**: 서브에이전트는 **기본적으로 중첩 서브에이전트를 파견하지 않음** — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 환경변수를 설정해야 더 깊은 중첩 허용. 동시 실행 서브에이전트 수도 기본 20개로 제한 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`로 오버라이드).
>
> **v2.1.219 기본값 재변경**: 서브에이전트는 다시 기본적으로 depth 3까지 중첩 서브에이전트를 파견 가능 (v2.1.217 기본값 대체) — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`로 설정하면 중첩 비활성화.

---

## 커스텀 에이전트 정의 (.claude/agents/) - v2.3

```yaml
---
name: frontend-developer
description: "React/Next.js 프론트엔드 개발 전문"
model: sonnet                     # sonnet | opus | haiku (또는 전체 모델 ID, v2.1.74+)

# 도구 허용 (allowedTools)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(npm:*)
  - Bash(npx:*)

# 도구 차단 (신규 v2.1.30+)
disallowedTools:
  - Task                          # 중첩 방지
  - mcp__dangerous__*             # 위험한 MCP 차단

# 권한 모드 (신규 v2.1.30+)
permissionMode: acceptEdits       # default | acceptEdits | dontAsk | bypassPermissions | plan

# 스킬 프리로드 (신규 v2.1.30+)
skills:
  - frontend-design-system
  - testing-patterns

# Worktree 격리 (신규 v2.1.50)
isolation: worktree              # 격리된 git worktree에서 실행

# 백그라운드 실행 (신규 v2.1.49)
background: true                 # 항상 백그라운드 Task로 실행

# 내장 Hooks
hooks:
  - type: PreToolUse
    tool: Write
    script: ./hooks/lint-check.sh
---

# Frontend Developer Agent

## 역할
React/Next.js 기반 프론트엔드 개발을 담당합니다.

## 규칙
1. TypeScript 사용 필수
2. 컴포넌트는 함수형으로 작성
3. 테스트 코드 함께 작성
```

---

## Agent Frontmatter 옵션 (v2.3)

| 옵션 | 타입 | 설명 | 기본값 |
|------|------|------|--------|
| `name` | string | 에이전트 이름 | **필수** |
| `description` | string | 설명 | **필수** |
| `model` | string | 모델 (sonnet/opus/haiku) | sonnet |
| `allowed-tools` | string[] | 허용된 도구 목록 | 모든 도구 |
| `disallowedTools` | string[] | 차단된 도구 목록 (신규) | - |
| `permissionMode` | string | 권한 모드 (신규) | default |
| `skills` | string[] | 프리로드할 스킬 (신규) | - |
| `hooks` | object[] | 내장 Hook 정의 | - |
| `mcpServers` | object | `--agent` 세션에서 로드할 MCP 서버 정의 (v2.1.117) | - |

---

## Permission Modes (신규)

| Mode | 설명 |
|------|------|
| `default` | 일반 권한 요청 |
| `acceptEdits` | 파일 편집 자동 승인 |
| `dontAsk` | 권한 요청 건너뜀 (신뢰 환경) |
| `bypassPermissions` | 모든 권한 우회 (위험) |
| `plan` | 계획 모드로 시작 |

---

## Task Tool 사용 (v2.3)

### 1. 코드베이스 탐색 (빠름, 저비용)

```typescript
Task({
  description: "Find auth handlers",
  prompt: "인증 관련 핸들러 파일들을 찾고 구조를 분석해줘",
  subagent_type: "Explore",
  model: "haiku"
})
```

### 2. 커스텀 에이전트 호출

```typescript
Task({
  description: "Build React component",
  prompt: "대시보드 컴포넌트를 만들어줘",
  subagent_type: "frontend-developer"  // .claude/agents/frontend-developer.md
})
```

### 3. 병렬 실행 (단일 메시지에 여러 Task)

```typescript
Task({ subagent_type: "frontend", prompt: "UI 작성" })
Task({ subagent_type: "backend", prompt: "API 작성" })
Task({ subagent_type: "qa-expert", prompt: "테스트 작성" })
```

### 4. 백그라운드 실행 (신규)

```typescript
Task({
  description: "Long analysis",
  prompt: "전체 코드베이스 분석",
  subagent_type: "Explore",
  run_in_background: true  // 백그라운드에서 실행
})
// output_file로 결과 확인
```

### 5. 백그라운드 세션 분기 (`/fork`) vs 인라인 서브에이전트 (`/subtask`)

> **v2.1.212 Breaking Change**: `/fork`가 현재 대화를 **새 백그라운드 세션**(`claude agents` 자체 행)으로 복제하는 방식으로 변경되었습니다. 기존에 `/fork`가 하던 인라인 서브에이전트 launch 방식은 **`/subtask`**로 이름이 분리되었습니다.

```
/subtask   # 기존 /fork 방식 — 현재 세션 내 인라인 서브에이전트 실행
/fork      # 신규 — 대화 전체를 백그라운드 세션으로 복제, 원 세션은 계속 작업 가능
```

또한 Task tool의 `mode` 파라미터는 제거(무시)되었습니다 — 서브에이전트는 이제 부모 세션의 permission mode를 기본 상속합니다 (v2.1.212).

### 6. 에이전트 재개

> ⚠️ **v2.1.77 Breaking Change**: Agent tool의 `resume` 파라미터가 제거되었습니다.
> 이전 에이전트 재개 시 `SendMessage({to: agentId})` 를 사용하세요.
> `SendMessage`는 중단된 에이전트를 자동으로 백그라운드에서 재개합니다.

```typescript
// 기존 방식 (제거됨)
// Task({ resume: "agent-id" })

// 신규 방식 (v2.1.77+)
SendMessage({ to: "agent-id-from-previous-task", content: "이전 작업을 계속해주세요" })
```

> **v2.1.224 신규**: **크로스 세션 `SendMessage`** — 같은 머신뿐 아니라 다른 머신의 Claude Code 세션에도 메시지 전송 가능 (macOS·Linux). `ListAgents`로 다른 세션을 탐색합니다. `crossSessionInbound`/`dialogExpiry` 설정으로 bypass-permissions 세션에는 승인 대기 후 전달하도록 제어할 수 있습니다.
> **v2.1.229 신규**: `ListAgents`가 연결 끊긴 Remote Control 세션은 `offline`, 클라우드 세션은 `cloud`로 표시합니다.

---

## 제약 사항

| 제약 | 값 |
|------|-----|
| 동시 실행 서브에이전트 | 기본 20개 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, v2.1.217) |
| 세션당 서브에이전트 파견 총량 | 기본 200개, `/clear`로 리셋 (`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`, v2.1.212) |
| 세션당 WebSearch 호출 | 기본 200회 (`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`, v2.1.212) |
| Task 컨텍스트 | 200k 토큰 |
| 중첩 | **기본 depth 3 허용** — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`로 비활성화 (v2.1.219; v2.1.217 "기본 비허용" 대체) |
| Auto-compaction | 서브에이전트 자동 compact 지원 |

---

## Plugin System (신규)

### Plugin Marketplace

```bash
# 플러그인 검색
/plugins search supabase

# 플러그인 설치
/plugins install @supabase/mcp

# 설치된 플러그인 목록
/plugins list
```

### MCP 통합

```json
// .mcp.json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp@latest"],
      "oauth": {
        "provider": "supabase",
        "scopes": ["database", "storage"]
      }
    }
  }
}
```

---

## Orchestrator Skill (병렬 Agent 조율)

병렬 Agent를 조율하는 Orchestrator Skill 생성 시 **반드시** 참조:

| 문서 | 설명 |
|------|------|
| [orchestrator-principles.md](orchestrator-principles.md) | 핵심 원칙, Context Injection, AB Test 결과 |
| [orchestrator-skill-creation-guide.md](orchestrator-skill-creation-guide.md) | 생성 가이드, 템플릿, 체크리스트 |

### 핵심 원칙

1. **YOU ORCHESTRATE, YOU DO NOT EXECUTE** - Orchestrator는 직접 코드 작성 안함
2. **SUBAGENTS LIE. VERIFY EVERYTHING.** - 파일/빌드/테스트 모두 검증
3. **BACKWARD COMPATIBILITY IS NON-NEGOTIABLE** - 하위호환 깨짐 = 즉시 RETRY

---

## Agent Teams vs Task Tool

| 기능 | Task Tool (단독) | Agent Teams |
|------|-----------------|-------------|
| 에이전트 수명 | 단발성 (작업 끝나면 종료) | 지속적 (팀 해체까지 유지) |
| 상태 공유 | 없음 | 공유 Task List |
| 커뮤니케이션 | 결과만 반환 | DM, 브로드캐스트 |
| 조율 | 호출자가 직접 | Team Lead가 조율 |
| 비용 | 작업당 과금 | 활성 시간 내내 과금 |
| 적합한 경우 | 단순 병렬 작업 | 복잡한 협업, 장기 프로젝트 |

**Agent Teams 상세**: [agent-teams-guide.md](agent-teams-guide.md)

---

## Task Management (v2.9)

| 도구 | 용도 |
|------|------|
| `TaskCreate` | 작업 생성 (subject, description, activeForm) |
| `TaskUpdate` | 상태 변경, 소유자 할당, 의존성 설정 |
| `TaskList` | 전체 작업 목록 조회 |
| `TaskGet` | 개별 작업 상세 조회 |

---

## Breaking Changes (v2.8-2.9)

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

## Breaking Changes (v2.1.212-2.1.219)

| 변경 | 이전 | 이후 |
|------|------|------|
| 서브에이전트 중첩 파견 | 기본 허용 (최대 5레벨) | **기본 비허용** — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 설정 필요 (v2.1.217) → **다시 기본 depth 3 허용** (v2.1.219) |
| Task tool `mode` 파라미터 | 지정 가능 | **제거(무시)** — 부모 세션 permission mode 상속 (v2.1.212) |
| `/fork` | 인라인 서브에이전트 launch | **백그라운드 세션 생성**; 기존 동작은 `/subtask` (v2.1.212) |
| agent frontmatter `name` | 임의 문자열 허용 | `:` 포함 시 거부 — 플러그인 네임스페이싱 예약 (v2.1.218) |
| Fast Mode 대상 모델 | Opus 4.7·4.8 | **Opus 4.7 제거** — Opus 5·Opus 4.8만 지원 (v2.1.219) |

## claude agents 플래그 (v2.1.142 신규)

`claude agents` 서브커맨드에 백그라운드 세션 상세 설정 플래그가 추가되었습니다:

| 플래그 | 설명 |
|--------|------|
| `--add-dir <path>` | 세션에 추가 디렉토리 마운트 |
| `--settings <path>` | 커스텀 settings.json 경로 지정 |
| `--mcp-config <path>` | MCP 설정 파일 경로 지정 |
| `--plugin-dir <path>` | 플러그인 디렉토리 경로 지정 |
| `--permission-mode <mode>` | 권한 모드 설정 |
| `--model <model>` | 사용 모델 지정 |
| `--effort <level>` | effort 레벨 설정 |
| `--dangerously-skip-permissions` | 권한 프롬프트 건너뜀 |

---

## 버그 수정 (v2.1.101)

- **MCP 도구 상속**: 동적으로 주입된 MCP 서버의 도구를 서브에이전트가 상속받지 못하던 버그 수정 — 이제 동적 주입 서버 도구도 정상 상속
- **isolation: worktree 파일 접근**: 격리된 worktree에서 실행 중인 서브에이전트가 자신의 worktree 내 파일에 Read/Edit 접근이 거부되던 버그 수정 — 이제 자신의 worktree 내 파일에 정상 접근 가능

---

## 공식 문서

- **Subagents Reference**: https://code.claude.com/docs/en/sub-agents
- **Agent Teams**: https://code.claude.com/docs/en/agent-teams

---

*이 문서는 SKILL.md에서 분리되었습니다 (2026-02-04, v2.9.0 업데이트 2026-02-11)*
