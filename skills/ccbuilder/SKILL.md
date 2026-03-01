---
name: ccbuilder
description: "Build and deploy Claude Code extensions (skills, hooks, agents, agent teams, ralph loops, slash commands) and answer questions about Claude Code functionality. Use when (1) creating new Claude Code functionality, setting up .claude infrastructure, creating custom hooks (SessionStart, PreToolUse, PermissionRequest, SubagentStart, SubagentStop, PostToolUseFailure, TeammateIdle, Stop), developing specialized agents, implementing skills, coordinating agent teams, or setting up Ralph Loops (autonomous development loops, fresh context pattern), OR (2) asking questions about Claude Code features, agent teams, hook patterns, skill development, memory system, modular rules, MCP integration, ralph loop, agentic loop, fresh context pattern, .claude directory structure, progressive disclosure, 500-line rule, OR (3) building programmatic LLM systems with Agent SDK. Includes P1 official documentation references and implementation guides."
userInvocable: true
argument-hint: "[skill|hook|agent|team|ralph|question] <name or query>"
---

# Claude Code Extension Builder

**Version**: 2.1.63
**Last Updated**: 2026-03-01

## 목적

Claude Code 확장 기능(Skills, Agents, Hooks, Agent Teams) 개발 질문 답변 및 구현 가이드 제공.

---

## 인자 처리 규칙

**인자**: `$ARGUMENTS`

`$ARGUMENTS`의 첫 번째 토큰으로 행동을 결정합니다.

### (인자 없음) → Welcome

AskUserQuestion 도구로 다음 옵션을 제시하세요:
새 Skill 만들기 / 새 Hook 만들기 / 새 Agent 만들기 / Agent Team 구성 / Ralph Loop 설정 / 뭘 어디에 만들지 도와줘 / 질문하기 / 문서 보기

### `skill <name>` → Skill 생성

1. Read [references/skills-guide.md](references/skills-guide.md)
2. Read [references/official/skills.md](references/official/skills.md)
3. `<name>`용 SKILL.md 스캐폴딩 + `references/` 디렉토리 생성
4. 필요 시 `references/github/repos/anthropics-skills/`에서 공식 Skill 예시 검색

### `hook <event>` → Hook 구현

1. Read [references/hooks-guide.md](references/hooks-guide.md)
2. Read [references/official/hooks.md](references/official/hooks.md)
3. `<event>`에 맞는 Hook 코드 생성 + settings.json 등록 안내
4. 필요 시 `references/github/repos/hooks-mastery/`에서 구현 예시 검색

### `agent <name>` → Agent 정의

1. Read [references/subagents-guide.md](references/subagents-guide.md)
2. Read [references/official/subagents.md](references/official/subagents.md)
3. `<name>`용 Agent 정의 파일(`.claude/agents/<name>.md`) 생성

### `team <name>` → Agent Team 구성

1. Read [references/agent-teams-guide.md](references/agent-teams-guide.md)
2. Team 아키텍처 설계 (역할 분담, 태스크 의존성)
3. TeamCreate → TaskCreate → Task 워크플로우 가이드

### `ralph <project-name>` → Ralph Loop 설정

1. Read [references/ralph-loop-guide.md](references/ralph-loop-guide.md)
2. 방식 선택 (Simple Bash Loop / Stop Hook / Ralph 프레임워크)
3. `TASK.md`, `PROGRESS.md`, `loop.sh` 스캐폴딩 생성
4. 필요 시 `.claude/hooks/ralph-stop.sh` + settings.json Stop Hook 등록

### 자연어 요구사항 → 컴포넌트 추천

사용자가 "~하고 싶어", "~해줘", "~를 만들어줘" 등 요구사항을 말하면:

1. Read [references/what-goes-where-guide.md](references/what-goes-where-guide.md)
2. 결정 트리와 매핑 테이블을 참고하여 **어떤 컴포넌트**를 **어디에** 만들어야 하는지 추천
3. 해당 컴포넌트의 **작성 템플릿**을 보여주고, 사용자 요구사항에 맞게 내용 채움
4. 컴포넌트가 결정되면 해당 생성 흐름(skill/hook/agent 등)으로 이동

### `question <query>` 또는 자연어 질문 → 답변

1. `<query>`에서 키워드 추출 후 아래 매핑으로 관련 문서 Read:
   - skills, skill → [references/skills-guide.md](references/skills-guide.md) + [official/skills.md](references/official/skills.md)
   - hooks, hook, event → [references/hooks-guide.md](references/hooks-guide.md) + [official/hooks.md](references/official/hooks.md)
   - agent, subagent → [references/subagents-guide.md](references/subagents-guide.md) + [official/subagents.md](references/official/subagents.md)
   - team, teammate → [references/agent-teams-guide.md](references/agent-teams-guide.md)
   - mcp, server, transport → [references/mcp-guide.md](references/mcp-guide.md) + [official/mcp.md](references/official/mcp.md)
   - memory, rules, CLAUDE.md → [references/memory-rules-guide.md](references/memory-rules-guide.md) + [official/memory-rules.md](references/official/memory-rules.md)
   - 어디에, 뭘, 어떻게, 선택, 분류 → [references/what-goes-where-guide.md](references/what-goes-where-guide.md)
   - tool, tools → [references/official/tools.md](references/official/tools.md)
   - orchestrator → [references/orchestrator-principles.md](references/orchestrator-principles.md)
   - ralph, loop, repl, fresh context, autonomous → [references/ralph-loop-guide.md](references/ralph-loop-guide.md)
2. 키워드가 불명확하면 `references/github/repos/`에서 Grep으로 실제 코드 검색
3. 문서 내용 기반으로 답변 (추측 금지, 근거 명시)

---

## 핵심 변경 사항 (v2.1.63)

### MCP 확장 (v2.8 강화)

| 기능 | 설명 |
|------|------|
| **HTTP Transport** | 권장 transport (`--transport http`), SSE deprecated |
| **Scope 계층** | Local > Project (.mcp.json) > User |
| **환경 변수 확장** | `${VAR}`, `${VAR:-default}` in .mcp.json |
| **claude mcp serve** | Claude Code를 MCP 서버로 노출 |
| **Managed MCP** | 조직 차원 중앙 관리 (allowedMcpServers/deniedMcpServers) |
| **claude.ai MCP connectors** | claude.ai의 MCP 커넥터를 Claude Code에서 사용 (v2.1.46) |

**상세**: [references/mcp-guide.md](references/mcp-guide.md)

### Memory 계층 확장 (v2.8 강화)

| 계층 | 설명 |
|------|------|
| **Managed Policy** | 조직 배포 (최고 우선순위) |
| **Project Memory** | CLAUDE.md + `@path` imports (5hop 재귀) |
| **Project Rules** | `.claude/rules/*.md` + paths: + subdirs + symlinks |
| **User Memory** | `~/.claude/CLAUDE.md` + `~/.claude/rules/` |
| **Project Local** | `CLAUDE.local.md` (자동 gitignore) |

**상세**: [references/memory-rules-guide.md](references/memory-rules-guide.md)

### Agent Teams (실험적)

멀티 에이전트 팀 협업 시스템. Team Lead가 Teammate들을 조율하여 병렬 작업 수행.

```
TeamCreate → TaskCreate → Task(teammate) → SendMessage → TeamDelete
```

**활성화**: `settings.json` → `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`

**상세**: [references/agent-teams-guide.md](references/agent-teams-guide.md)

### Task Management (신규)

| 도구 | 용도 |
|------|------|
| `TaskCreate` | 작업 생성 (subject, description, activeForm) |
| `TaskUpdate` | 상태 변경, 소유자 할당, 의존성 설정 |
| `TaskList` | 전체 작업 목록 조회 |
| `TaskGet` | 개별 작업 상세 조회 |

### Memory & Modular Rules (신규)

| 기능 | 설명 |
|------|------|
| **Auto Memory** | `~/.claude/projects/<project>/memory/` 영구 저장 |
| **MEMORY.md** | 매 세션 자동 로드 (200줄 제한) |
| **Modular Rules** | `.claude/rules/*.md` + `paths:` frontmatter로 경로별 규칙 |

### 신규 Hook 이벤트

| 이벤트 | 용도 |
|--------|------|
| `TeammateIdle` | 팀메이트 유휴 상태 (Agent Teams) |
| `SubagentStart` | 서브에이전트 생성 시점 |
| `PostToolUseFailure` | 도구 호출 실패 후 |
| `Setup` | 초기 설정 (--init, --init-only, --maintenance) |
| `WorktreeCreate` | git worktree 생성 시 (v2.1.50) |
| `WorktreeRemove` | git worktree 제거 시 (v2.1.50) |

### Agent/CLI/Plugin 강화 (v2.1.41-51)

- **Agent 필드**: `isolation: worktree` (격리 실행), `background: true` (백그라운드)
- **CLI**: `claude agents`, `claude auth login/status/logout`, `claude remote-control`, `--worktree (-w)`, Ctrl+F (에이전트 종료)
- **Plugin**: `settings.json` 동봉, 커스텀 npm 레지스트리, macOS plist / Windows Registry managed settings

### Breaking Changes

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |
| 기본 모델 | Sonnet 4.5 | Sonnet 4.6 (Max plan) |

---

## Deprecated (사용 중지)

| Deprecated | 대체 방법 |
|------------|-----------|
| `output styles` | `--system-prompt-file` 또는 `plugins` 사용 |
| `legacy SDK entrypoint` | `@anthropic-ai/claude-agent-sdk`로 마이그레이션 |
| `includeCoAuthoredBy` 설정 | 새 `attribution` 설정 사용 |
| `$ARGUMENTS.0` 문법 | `$ARGUMENTS[0]` 사용 |
| SSE MCP transport | HTTP (streamable-http) 사용 |
| Sonnet 4.5 (1M context) | Sonnet 4.6 사용 (Max plan) |

---

## 확장 기능 유형 요약

| 유형 | 용도 | 컨텍스트 | 위치 |
|------|------|----------|------|
| **Skill** | 지식/가이드 주입 + 슬래시 명령 | 현재 대화 (fork 시 별도) | `.claude/skills/` |
| **Subagent** | 독립 에이전트 정의 | 별도 200k | `.claude/agents/` |
| **Agent Team** | 멀티 에이전트 팀 협업 (신규) | 각 Teammate 별도 | `~/.claude/teams/` |
| **Hook** | 워크플로우 제어 | - | `settings.json` |
| **Memory** | 세션 간 지식 영속 (신규) | 자동 로드 | `~/.claude/projects/*/memory/` |
| **Rules** | 경로별 규칙 적용 (신규) | 자동 로드 | `.claude/rules/` |
| **Ralph Loop** | 자율 개발 루프 (신규) | 매 반복 Fresh | `TASK.md` + `loop.sh` |

---

## Quick Reference

### Skills 핵심

```yaml
---
name: my-skill
description: "설명 + 자동 활성화 키워드"
userInvocable: true
argument-hint: "<topic>"
allowed-tools: [Read, Grep, Glob]
---

# My Skill

## 목적
스킬의 목적

## 지침
상세 내용은 references/ 참조
```

**상세**: [references/skills-guide.md](references/skills-guide.md)

---

### Hooks 핵심

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash|Write",
      "hooks": [{
        "type": "command",
        "command": "./hooks/validate.sh"
      }]
    }],
    "Stop": [{
      "type": "command",
      "command": "./hooks/on-stop.sh"
    }]
  }
}
```

**주요 이벤트**: SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, TeammateIdle

**상세**: [references/hooks-guide.md](references/hooks-guide.md)

---

### Agent Teams 핵심 (신규)

```
1. TeamCreate({ team_name: "my-team" })
2. TaskCreate({ subject: "Build API", description: "..." })
3. Task({ subagent_type: "backend", team_name: "my-team", name: "api-dev", prompt: "..." })
4. SendMessage({ type: "message", recipient: "api-dev", content: "..." })
5. TeamDelete()  // 작업 완료 후
```

**활성화**: `settings.json` → `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`

**상세**: [references/agent-teams-guide.md](references/agent-teams-guide.md)

---

### Subagents 핵심

```yaml
---
name: frontend-developer
description: "React/Next.js 개발 전문"
model: sonnet
allowed-tools: [Read, Write, Edit, Bash(npm:*)]
permissionMode: acceptEdits
isolation: worktree            # 격리된 worktree 실행 (v2.1.50)
background: true               # 항상 백그라운드 실행 (v2.1.49)
---

# Frontend Developer Agent
```

**내장 타입**: Explore, Plan, general-purpose, Bash, claude-code-guide

**CLI**: `claude agents` — 설정된 에이전트 목록 조회

**상세**: [references/subagents-guide.md](references/subagents-guide.md)

---

### Ralph Loop 핵심 (신규)

```bash
# Simple: TASK.md + PROGRESS.md + loop.sh
cat TASK.md PROGRESS.md | claude -p "다음 미완료 작업 수행 후 PROGRESS.md 업데이트. 완료 시 LOOP_COMPLETE 추가"
# Stop Hook: 종료 차단으로 자동 루프
# Ralph Framework: ralph --monitor (풀 프레임워크)
```

**핵심**: 매 반복 Fresh Context(0%) + 파일/Git으로 상태 유지 + 이중 종료 조건

**상세**: [references/ralph-loop-guide.md](references/ralph-loop-guide.md)

---

## 사용 시나리오 결정 가이드

```
Q: 장시간 자율 개발이 필요한가? (30분+, 컨텍스트 열화 방지)
├─ Yes → Ralph Loop (TASK.md + loop.sh)
└─ No
   Q: 반복적으로 같은 지침이 필요한가?
   ├─ Yes → Skill 생성
   └─ No
      Q: 여러 에이전트가 병렬로 협업해야 하나?
      ├─ Yes → Agent Team (TeamCreate + Task + SendMessage)
      └─ No
         Q: 독립적인 작업 실행이 필요한가?
         ├─ Yes → Task Tool 사용
         │  Q: 커스텀 에이전트가 필요한가?
         │  ├─ Yes → Subagent 정의 후 Task에서 호출
         │  └─ No → 내장 subagent_type 사용 (Explore, Plan, general-purpose)
         └─ No → 직접 대화에서 처리
```

---

## 프로젝트 구조 예시

```
.claude/
├── skills/
│   └── react-patterns/
│       ├── SKILL.md              # < 500줄
│       ├── CHANGELOG.md
│       ├── releases/
│       └── references/
│           ├── hooks.md
│           └── state-management.md
├── agents/
│   └── react-developer.md
├── rules/
│   └── coding-rules.md
└── settings.json
```

---

## Progressive Disclosure (500줄 규칙)

SKILL.md는 500줄 이하로 유지합니다:

```
my-skill/
├── SKILL.md          # < 500줄 (개요만)
├── CHANGELOG.md      # 변경 이력
├── releases/         # 버전별 스냅샷
└── references/       # 상세 가이드
    ├── topic-1.md
    └── topic-2.md
```

---

## 상세 참조 문서

### 기능별 가이드

| 문서 | 설명 |
|------|------|
| [references/skills-guide.md](references/skills-guide.md) | Skills 상세 가이드 |
| [references/hooks-guide.md](references/hooks-guide.md) | Hooks 상세 가이드 |
| [references/subagents-guide.md](references/subagents-guide.md) | Subagents + Plugin 가이드 |
| [references/agent-teams-guide.md](references/agent-teams-guide.md) | Agent Teams 상세 가이드 |
| [references/ralph-loop-guide.md](references/ralph-loop-guide.md) | Ralph Loop (자율 개발 루프) 가이드 |
| [references/troubleshooting.md](references/troubleshooting.md) | 트러블슈팅 |

### Orchestrator Skill 개발

| 문서 | 설명 |
|------|------|
| [references/orchestrator-principles.md](references/orchestrator-principles.md) | 핵심 원칙, Context Injection |
| [references/orchestrator-skill-creation-guide.md](references/orchestrator-skill-creation-guide.md) | 생성 가이드, 체크리스트 |

### 구현 및 품질

| 문서 | 설명 |
|------|------|
| [references/implementation-guide.md](references/implementation-guide.md) | 구현 단계별 가이드 |
| [references/review-system.md](references/review-system.md) | 스킬 리뷰/검증 시스템 |
| [references/skill-subagent-task-guide.md](references/skill-subagent-task-guide.md) | Skill/Subagent/Task 상세 비교 |
| [references/best-practices.md](references/best-practices.md) | 모범 사례 |

### 시스템 가이드

| 문서 | 설명 |
|------|------|
| [references/mcp-guide.md](references/mcp-guide.md) | MCP 설정 및 활용 가이드 |
| [references/what-goes-where-guide.md](references/what-goes-where-guide.md) | 요청사항 → 어디에 뭘 적을지 가이드 |
| [references/memory-rules-guide.md](references/memory-rules-guide.md) | Memory & Rules 상세 가이드 |

### 공식 문서 레퍼런스 (official/)

| 문서 | 설명 |
|------|------|
| [references/official/skills.md](references/official/skills.md) | Skills 공식 문서 요약 |
| [references/official/hooks.md](references/official/hooks.md) | Hooks 공식 문서 요약 (14 events) |
| [references/official/subagents.md](references/official/subagents.md) | Sub-agents 공식 문서 요약 |
| [references/official/mcp.md](references/official/mcp.md) | MCP 공식 문서 요약 |
| [references/official/memory-rules.md](references/official/memory-rules.md) | Memory & Rules 공식 문서 요약 |
| [references/official/tools.md](references/official/tools.md) | Built-in Tools 레퍼런스 (토큰, 위험도, 권장 조합) |

### GitHub 레포 & 유즈 케이스 (github/)

| 문서 | 설명 |
|------|------|
| [references/github/README.md](references/github/README.md) | Tier별 레포 인덱스 (Top 10) |
| [references/github/official-repos.md](references/github/official-repos.md) | Anthropic 공식 레포 (T1) |
| [references/github/ecosystem-collections.md](references/github/ecosystem-collections.md) | 종합 컬렉션 10k+ (T2) |
| [references/github/specialized-tools.md](references/github/specialized-tools.md) | 특화 도구 & 유즈 케이스 (T3/T4) |
| [references/github/patterns.md](references/github/patterns.md) | 크로스 레포 검증 패턴 10가지 |

### 로컬 Submodule 레포 (github/repos/)

Skill, Subagent, Hook 구현 시 아래 로컬 레포에서 **실제 코드를 검색**하여 참고합니다:

| 레포 | 로컬 경로 | 검색 대상 |
|------|-----------|-----------|
| anthropics/skills | `references/github/repos/anthropics-skills` | 공식 Skill 구현 (DOCX, PDF 등) |
| obra/superpowers | `references/github/repos/obra-superpowers` | TDD, 디버깅, Subagent 워크플로우 |
| everything-claude-code | `references/github/repos/everything-claude-code` | 15 agents, 30+ skills, hooks |
| wshobson/agents | `references/github/repos/wshobson-agents` | 112 agents, 16 orchestrators |
| awesome-claude-code | `references/github/repos/awesome-claude-code` | 생태계 디렉토리 |
| awesome-subagents | `references/github/repos/awesome-subagents` | 126+ 서브에이전트 |
| awesome-claude-skills | `references/github/repos/awesome-claude-skills` | Skills 비교표, 튜토리얼 |
| awesome-agent-skills | `references/github/repos/awesome-agent-skills` | 339+ 멀티에이전트 호환 Skills |
| hooks-mastery | `references/github/repos/hooks-mastery` | 13 Hook events 구현 |
| claude-code-showcase | `references/github/repos/claude-code-showcase` | GitHub Actions, JIRA 워크플로우 |
| claude-code-system-prompts | `references/github/repos/claude-code-system-prompts` | 시스템 프롬프트 원문, Tool 스펙 |

**검색 방법**:

| 방법 | 도구 | 용도 |
|------|------|------|
| 키워드 검색 | `Grep` | 정확한 패턴/문자열 매칭 |
| 파일 탐색 | `Glob` | 파일명/경로 패턴 매칭 |
| 깊은 분석 | `Task(Explore)` | 멀티 라운드 탐색 + 관계 파악 |
| 시맨틱 검색 | `claude-context MCP` | 자연어 코드 검색 (설치 필요) |

```
# Grep: 키워드 검색
Grep "PreToolUse" in references/github/repos/hooks-mastery/

# Glob: Skill 파일 찾기
Glob "**/SKILL.md" in references/github/repos/anthropics-skills/

# Task(Explore): 깊은 분석
Task(Explore, "repos/obra-superpowers에서 TDD 워크플로우 구조 분석해줘")

# claude-context MCP: 시맨틱 검색 (설치 후)
"Hook에서 보안 필터링하는 패턴 찾아줘"
```

#### claude-context MCP 설치 (선택)

시맨틱 코드 검색 — 설정: `claude mcp add claude-context` (Gemini+Zilliz 또는 Ollama+Milvus)

### 기타 참조

| 문서 | 설명 |
|------|------|
| [references/external-resources.md](references/external-resources.md) | 커뮤니티, 포럼, 블로그 링크 |

---

## 공식 문서 URL (P1 참조)

- **Skills**: https://code.claude.com/docs/en/skills
- **Hooks**: https://code.claude.com/docs/en/hooks
- **Subagents**: https://code.claude.com/docs/en/sub-agents
- **Slash Commands**: https://code.claude.com/docs/en/slash-commands
- **MCP**: https://code.claude.com/docs/en/mcp
- **Memory**: https://code.claude.com/docs/en/memory
- **Settings**: https://code.claude.com/docs/en/settings

---

**Status**: UPDATED (2026-02-25) | **Claude Code**: v2.1.63+ | **Sync**: [version-sync.md](references/version-sync.md) | [check-updates.sh](../../scripts/check-updates.sh)
