---
name: ccbuilder
description: "Build and deploy Claude Code extensions (skills, hooks, agents, agent teams, ralph loops, graph workflows, slash commands) and answer questions about Claude Code functionality. Use when (1) creating new Claude Code functionality, setting up .claude infrastructure, creating custom hooks (SessionStart, PreToolUse, PermissionRequest, SubagentStart, SubagentStop, PostToolUseFailure, TeammateIdle, Stop), developing specialized agents, implementing skills, coordinating agent teams, setting up Ralph Loops, or designing graph workflows, OR (2) asking questions about Claude Code features, agent teams, hook patterns, skill development, memory system, modular rules, MCP integration, ralph loop, graph workflow, agentic loop, fresh context pattern, .claude directory structure, progressive disclosure, 500-line rule, OR (3) building programmatic LLM systems with Agent SDK. Includes P1 official documentation references and implementation guides."
userInvocable: true
argument-hint: "[skill|hook|agent|team|ralph|graph|question] <name or query>"
---

# Claude Code Extension Builder

**Version**: 2.33.0
**Last Updated**: 2026-04-29

## 목적

Claude Code 확장 기능(Skills, Agents, Hooks, Agent Teams) 개발 질문 답변 및 구현 가이드 제공.

---

## 인자 처리 규칙

**인자**: `$ARGUMENTS`

`$ARGUMENTS`의 첫 번째 토큰으로 행동을 결정합니다.

### (인자 없음) → Welcome

AskUserQuestion 도구로 다음 옵션을 제시하세요:
새 Skill 만들기 / 새 Hook 만들기 / 새 Agent 만들기 / Agent Team 구성 / Ralph Loop 설정 / Skill 평가/벤치마크 / 뭘 어디에 만들지 도와줘 / 질문하기 / 문서 보기

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

### `graph <name>` → Graph Workflow 설계/실행

자연어 → Graph 생성 → 실행까지 일괄 처리. 3단계 이상 + 분기/병렬/반복이 있을 때 사용.
1. Read [references/graph-workflow-guide.md](references/graph-workflow-guide.md) (스키마, 변환 패턴, **v2 설계 체크리스트**)
2. 요청 분석 → Graph JSON 생성 (v2 체크리스트 필수: state, reads/writes, artifacts, autonomy, adversarial verification)
3. Graph를 사용자에게 보여주고 확인 → `.omc/state/graph/{id}/` 초기화
4. flow 순서대로 노드 실행: reads 주입→Task()/LLM평가→writes append→artifacts 저장. `[A,B]`은 병렬, decision은 route_criteria 순서 평가
5. ralph.enabled면 SCAR 목표까지 Fresh Context 반복 + graph.json 자기 개선
6. 최종 결과 반환

**스키마**: `{id, goal, state, nodes:[{id, do, with, reads, writes, artifacts, autonomy}], flow, limits, ralph}`
**상세**: [references/graph-workflow-guide.md](references/graph-workflow-guide.md) | 템플릿: `references/graph-templates/`

### 자연어 요구사항 → 컴포넌트 추천

사용자가 "~하고 싶어", "~해줘", "~를 만들어줘" 등 요구사항을 말하면:

1. Read [references/what-goes-where-guide.md](references/what-goes-where-guide.md)
2. 결정 트리와 매핑 테이블을 참고하여 **어떤 컴포넌트**를 **어디에** 만들어야 하는지 추천
3. 해당 컴포넌트의 **작성 템플릿**을 보여주고, 사용자 요구사항에 맞게 내용 채움
4. 컴포넌트가 결정되면 해당 생성 흐름(skill/hook/agent 등)으로 이동

### `eval <skill-path>` → Skill 평가

1. Read [references/eval-guide.md](references/eval-guide.md)
2. `<skill-path>` 스킬의 eval 워크플로우 실행 (테스트 → 채점 → 리뷰)

### `improve <skill-path>` → Skill 개선

1. Read [references/eval-guide.md](references/eval-guide.md)
2. eval 피드백 기반 스킬 개선 → 재평가 루프

### `benchmark <skill-path>` → 벤치마크 집계

1. Read [references/eval-guide.md](references/eval-guide.md)
2. 다수 eval 실행 결과 집계 → pass_rate, 토큰, 시간 통계

### `question <query>` 또는 자연어 질문 → 답변

1. `<query>`에서 키워드 추출 후 아래 매핑으로 관련 문서 Read:
   - skills, skill → [references/skills-guide.md](references/skills-guide.md) + [official/skills.md](references/official/skills.md)
   - hooks, hook, event → [references/hooks-guide.md](references/hooks-guide.md) + [official/hooks.md](references/official/hooks.md)
   - agent, subagent → [references/subagents-guide.md](references/subagents-guide.md) + [official/subagents.md](references/official/subagents.md)
   - team, teammate → [references/agent-teams-guide.md](references/agent-teams-guide.md)
   - 통합, integration, skill team → [references/skill-agent-teams-integration-guide.md](references/skill-agent-teams-integration-guide.md)
   - mcp, server, transport → [references/mcp-guide.md](references/mcp-guide.md) + [official/mcp.md](references/official/mcp.md)
   - memory, rules, CLAUDE.md → [references/memory-rules-guide.md](references/memory-rules-guide.md) + [official/memory-rules.md](references/official/memory-rules.md)
   - 어디에, 뭘, 어떻게, 선택, 분류 → [references/what-goes-where-guide.md](references/what-goes-where-guide.md)
   - tool, tools → [references/official/tools.md](references/official/tools.md)
   - orchestrator → [references/orchestrator-principles.md](references/orchestrator-principles.md)
   - ralph, loop, repl, fresh context, autonomous → [references/ralph-loop-guide.md](references/ralph-loop-guide.md)
   - eval, evaluation, 평가, 벤치마크, benchmark → [references/eval-guide.md](references/eval-guide.md)
   - graph, workflow, 그래프, DAG, 파이프라인 → [references/graph-workflow-guide.md](references/graph-workflow-guide.md)
2. 키워드가 불명확하면 `references/github/repos/`에서 Grep으로 실제 코드 검색
3. 문서 내용 기반으로 답변 (추측 금지, 근거 명시)

---

## 핵심 변경 사항 (v2.1.123)

### MCP 확장 (v2.8 강화)

| 기능 | 설명 |
|------|------|
| **HTTP Transport** | 권장 transport (`--transport http`), SSE deprecated |
| **Scope 계층** | Local > Project (.mcp.json) > User |
| **환경 변수 확장** | `${VAR}`, `${VAR:-default}` in .mcp.json |
| **claude mcp serve** | Claude Code를 MCP 서버로 노출; **`alwaysLoad`**: 서버 모든 도구 tool-search 지연 없이 항상 로드 (v2.1.121); 시작 오류 시 최대 3회 자동 재시도 (v2.1.121) |
| **Managed MCP** | 조직 차원 중앙 관리 (allowedMcpServers/deniedMcpServers/allowedChannelPlugins, v2.1.84) |
| **claude.ai MCP connectors** | claude.ai MCP 커넥터 사용 (v2.1.46); `ENABLE_CLAUDEAI_MCP_SERVERS=false` 비활성화 (v2.1.63); 로컬 설정과 중복 시 로컬 우선 (v2.1.84) |
| **--channels** | MCP 서버가 세션에 메시지 푸시 / 채널 서버가 도구 승인 프롬프트 폰으로 릴레이 (v2.1.80-81) |
| **oauth.authServerMetadataUrl** | MCP OAuth 커스텀 메타데이터 URL 지정 (v2.1.69) |
| **MCP OAuth** | 콜백 포트 충돌·재인증 수정 (v2.1.74); CIMD/SEP-991 (Client ID Metadata Document) 지원 (v2.1.81); RFC 9728 Protected Resource Metadata discovery — 인증 서버 자동 탐색 (v2.1.85) |
| **CLAUDE_CODE_MCP_SERVER_NAME/URL** | `headersHelper` 스크립트에서 서버 이름·URL 접근 — 하나의 헬퍼로 다중 서버 처리 (v2.1.85) |
| **MCP 도구 호출 축소** | read/search 호출 "Queried {server}" 단일 라인 표시, Ctrl+O 확장 (v2.1.81) |
| **MCP Elicitation** | MCP 서버가 세션 중 구조화된 입력 요청 (폼 필드·URL) (v2.1.76) |
| **MCP 컨텍스트 제한** | 도구 설명·서버 지시문 2KB 상한 — OpenAPI 서버 컨텍스트 팽창 방지 (v2.1.84) |
| **MCP 결과 크기 오버라이드** | `_meta["anthropic/maxResultSizeChars"]` 어노테이션 — 도구 결과 최대 500K 확장, DB 스키마 등 대용량 결과 처리 (v2.1.91) |
| **Hook → MCP 직접 호출** | `type: "mcp_tool"` 훅으로 MCP 도구 직접 실행 (v2.1.118); 서브에이전트·SDK 재구성 시 서버 병렬 연결 (v2.1.119) |
| **/mcp 중복 커넥터 힌트** | claude.ai 커넥터가 동일 URL 수동 서버에 의해 숨겨질 때 `/mcp`에서 중복 제거 힌트 표시 (v2.1.122) |

**상세**: [references/mcp-guide.md](references/mcp-guide.md)

### Memory 계층 확장 (v2.8 강화)

| 계층 | 설명 |
|------|------|
| **Managed Policy** | 조직 배포 (최고 우선순위); `managed-settings.d/` 드롭인 디렉토리 지원 (v2.1.83) |
| **Project Memory** | CLAUDE.md + `@path` imports (5hop 재귀) |
| **Project Rules** | `.claude/rules/*.md` + paths: + subdirs + symlinks |
| **User Memory** | `~/.claude/CLAUDE.md` + `~/.claude/rules/` |
| **Project Local** | `CLAUDE.local.md` (자동 gitignore) |
| **HTML 주석** | `<!-- -->` 자동 주입 시 Claude에게 숨김, Read 도구로는 표시 (v2.1.72) |
| **autoMemoryDirectory** | Auto Memory 저장 디렉토리 커스텀 경로 지정 (v2.1.74) |
| **메모리 타임스탬프** | 메모리 파일 최종 수정 시각 자동 기록 — 신선도 판단 지원 (v2.1.75) |

**상세**: [references/memory-rules-guide.md](references/memory-rules-guide.md)

### Agent Teams (실험적)

멀티 에이전트 팀 협업 시스템. Team Lead가 Teammate들을 조율하여 병렬 작업 수행. **v2.1.72**: 팀 에이전트 리더 모델 자동 상속. **v2.1.114**: 팀메이트 도구 권한 요청 시 권한 다이얼로그 크래시 수정.

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
| **MEMORY.md** | 매 세션 자동 로드 (200줄/25KB 제한, v2.1.83) |
| **Modular Rules** | `.claude/rules/*.md` + `paths:` frontmatter로 경로별 규칙 (YAML 리스트 지원, v2.1.84) |
| **Worktree 공유** | 같은 레포의 git worktree 간 Project config/Auto memory 공유 (v2.1.63) |

### 신규 Hook 이벤트

| 이벤트 | 용도 |
|--------|------|
| `TeammateIdle` | 팀메이트 유휴 상태 (Agent Teams) |
| `SubagentStart` | 서브에이전트 생성 시점 |
| `PostToolUseFailure` | 도구 호출 실패 후 — `duration_ms` 포함 (v2.1.119) |
| `Setup` | 초기 설정 (--init, --init-only, --maintenance) |
| `WorktreeCreate`/`WorktreeRemove` | git worktree 생성/제거 시 (v2.1.50); Create: HTTP hook 지원 → `hookSpecificOutput.worktreePath` 반환 (v2.1.84) |
| `InstructionsLoaded` | CLAUDE.md / `.claude/rules/*.md` 로드 시 (v2.1.69) |
| `PostCompact` | 컨텍스트 압축 완료 후 (v2.1.76) |
| `Elicitation` | MCP 서버 사용자 입력 요청 인터셉트 (v2.1.76) |
| `ElicitationResult` | Elicitation 응답 전송 전 오버라이드 (v2.1.76) |
| `StopFailure` | API 오류(rate limit·인증 실패)로 턴 종료 시 (v2.1.78) |
**신규 필드 (v2.1.69)**: `agent_id`, `agent_type`, `worktree` (모든 이벤트에 추가) | **HTTP Hook (v2.1.63)**: `type: "http"` — URL로 JSON POST | **v2.1.83+**: `CwdChanged`, `FileChanged` (v2.1.83), `TaskCreated` (v2.1.84) | **v2.1.85+**: Hook `if` 필드 — permission rule syntax (`Bash(git *)`)로 조건부 실행 필터링 (프로세스 스폰 오버헤드 감소); `PreToolUse` hook `updatedInput` + `permissionDecision: "allow"` 반환으로 `AskUserQuestion` 충족 (헤드리스 통합 지원) | **v2.1.88+**: `PermissionDenied` Hook — auto mode 분류기 거부 후 발동, `{retry: true}` 반환 시 모델 재시도; Hook `if` 복합 명령(`ls && git push`) 및 env-var 접두사 매칭 수정 | **v2.1.89+**: `PreToolUse` `"defer"` 권한 결정 — 헤드리스 세션 도구 호출 일시 중지 후 `-p --resume`으로 훅 재평가; Hook 출력 50K 초과 시 디스크 저장 (파일 경로+미리보기 컨텍스트 주입) | **v2.1.92**: Stop 타입 Hook에서 소형 빠른 모델이 `ok:false` 반환 시 잘못 실패하던 버그 수정; `preventContinuation:true` 시맨틱 복원 | **v2.1.94**: `hookSpecificOutput.sessionTitle` — `UserPromptSubmit` Hook에서 세션 제목 설정 지원; managed settings 강제 플러그인 훅이 `allowManagedHooksOnly` 설정 시에도 실행 | **v2.1.101**: settings.json의 알 수 없는 훅 이벤트 이름이 전체 파일 무시를 유발하지 않도록 복원; `permissions.deny` 규칙이 `PreToolUse` hook의 `permissionDecision: "ask"` 다운그레이드를 방지하도록 수정 | **v2.1.105**: `PreCompact` Hook — 컨텍스트 압축 차단 지원 (exit code 2 또는 `{"decision":"block"}` 반환) | **v2.1.118**: Hooks → MCP 도구 직접 호출 (`type: "mcp_tool"` 타입 추가) | **v2.1.119**: PostToolUse·PostToolUseFailure에 `duration_ms` (도구 실행 시간, 권한 프롬프트·PreToolUse 제외) 필드 추가 | **v2.1.121**: PostToolUse `hookSpecificOutput.updatedToolOutput` — 이제 모든 도구에서 tool output 교체 지원 (기존 MCP 전용→전체 확장)

### Agent/CLI/Plugin 강화

- **Agent 필드**: `isolation: worktree` (격리 실행), `background: true` (백그라운드), `model` (per-invocation 오버라이드 복원, v2.1.72); 전체 모델 ID (`claude-opus-4-5` 등) agent frontmatter에서 수용 (v2.1.74); `initialPrompt` — 에이전트 첫 턴 자동 제출 (v2.1.83)
- **CLI**: `claude agents`, `claude auth login [--console]`, `claude auth status/logout`, `claude remote-control`, `--worktree (-w)`, Ctrl+F (에이전트 종료), `--bare` (-p 경량화: 훅/LSP/플러그인 비활성화·Auto-memory 끔, API key 필수, v2.1.81), `rate_limits` statusline 필드 (5시간/7일 rate limit 표시, v2.1.80); auto mode 거부 명령 알림 + `/permissions` Recent 탭에서 `r`로 재시도 (v2.1.89); Skill tool로 내장 슬래시 명령(`/init`, `/review`, `/security-review`) 자동 탐색·실행 (v2.1.108); `/model` 전환 전 미캐시 경고 (v2.1.108); `/resume` 피커 현재 디렉토리 기본 표시·Ctrl+A 전체 표시 (v2.1.108); `/resume` 검색창에 PR URL 붙여넣기로 해당 PR 생성 세션 자동 검색 (GitHub/GHE/GitLab/Bitbucket, v2.1.122); 오류 메시지 개선 — rate limit vs plan limit 구분·5xx/529 → status.claude.com·미지원 명령 유사어 제안 (v2.1.108); thinking 표시기 로테이팅 힌트 개선 (v2.1.109); CLI 네이티브 바이너리 스폰으로 전환 (v2.1.113); `xhigh` effort — Opus 4.7 전용 (v2.1.111); auto mode `--enable-auto-mode` 플래그 불필요·Max 구독자 Opus 4.7 지원 (v2.1.111); `/tui fullscreen` 플리커 없는 풀스크린 (v2.1.110); `/focus` 포커스 뷰 토글 (`Ctrl+O`는 verbose 전용 분리, v2.1.110); `/ultrareview` 클라우드 병렬 코드리뷰 (v2.1.111); `/less-permission-prompts` 읽기 전용 허용 리스트 자동 제안 (v2.1.111); `/effort` 인터랙티브 슬라이더 (v2.1.111); plan 파일 프롬프트 기반 이름 (v2.1.111); Esc로 `/loop` wakeup 취소 (v2.1.113); 서브에이전트 스트림 정지 10분 타임아웃 (v2.1.113); `Ctrl+U` 전체 버퍼 클리어·`Ctrl+Y` 복원 (v2.1.111); Windows Git Bash 불필요 — 미설치 시 PowerShell 자동 사용 (v2.1.120); `claude ultrareview [target]` CI/스크립트 비대화형 실행 (`--json` raw output, exit 0/1, v2.1.120); `AI_AGENT` env var 서브프로세스 자동 설정 — `gh` 트래픽 Claude Code 귀속 (v2.1.120)
- **Plugin**: `settings.json` 동봉, 커스텀 npm 레지스트리, macOS plist / Windows Registry managed settings; `--plugin-dir` 로컬 개발 사본이 마켓플레이스 동명 플러그인 오버라이드 (v2.1.74); `${CLAUDE_PLUGIN_DATA}` 플러그인 영속 상태 변수 — 업데이트 후에도 유지 (v2.1.78); `CLAUDE_CODE_PLUGIN_SEED_DIR` 다중 시드 디렉토리 지원 (`:` Unix, `;` Windows, v2.1.79); `source: 'settings'` 마켓플레이스 소스 — settings.json 내 플러그인 인라인 선언 (v2.1.80); ref-tracked 플러그인 매 로드 시 재클론으로 최신화 (v2.1.81); Skills/슬래시 명령 `effort` frontmatter — 모델 effort 레벨 오버라이드 (v2.1.80); 조직 정책(`managed-settings.json`) 차단 플러그인 설치·활성화 불가 및 마켓플레이스 숨김 (v2.1.85); 플러그인 `bin/` 디렉토리 실행 파일 배포 — Bash 도구에서 bare command로 실행 가능 (v2.1.91); `disableSkillShellExecution` 설정 — Skills/슬래시 명령/플러그인 명령 인라인 셸 실행 비활성화 (v2.1.91); `keep-coding-instructions` frontmatter 필드 — 플러그인 output style 유지 (v2.1.94); `"skills": ["./"]` 선언 시 frontmatter `name` 필드로 호출명 결정 (v2.1.94); 플러그인 `monitors` 매니페스트 키 — 세션 시작/스킬 invoke 시 백그라운드 모니터 자동 실행 (v2.1.105); 스킬 설명 최대 길이 250 → 1,536자, 초과 시 시작 경고 (v2.1.105); `claude plugin prune` 고아 의존성 제거·`uninstall --prune` 연쇄 삭제 (v2.1.121); `claude plugin validate` `$schema`·`version`·`description` 최상위 허용 (v2.1.120); `${CLAUDE_EFFORT}` Skill 콘텐츠에서 현재 effort 레벨 참조 (v2.1.120); `/skills` 필터 검색박스 (v2.1.121)
- **신규 명령**: `/loop <interval> <prompt>` (v2.1.71), `/reload-plugins` (v2.1.69), `/plan <description>` 즉시 플랜 모드 (v2.1.72), `/branch` (v2.1.77, `/fork` alias 유지), `/effort` 레벨 설정 (v2.1.76), `/copy N` N번째 최근 응답 복사 (v2.1.77), `/powerup` 애니메이션 데모와 함께 Claude Code 기능 인터랙티브 학습 (v2.1.90), `/team-onboarding` 로컬 Claude Code 사용 이력 기반 팀원 온보딩 가이드 자동 생성 (v2.1.101), `/proactive` `/loop` 별칭 (v2.1.105), `/recap` 세션 복귀 시 컨텍스트 요약 (`/config` 설정·`CLAUDE_CODE_ENABLE_AWAY_SUMMARY` 강제, v2.1.108), `/undo` `/rewind` 별칭 (v2.1.108), `/tui` 풀스크린 렌더링 (v2.1.110), `/focus` 포커스 뷰 (v2.1.110), `/ultrareview` 클라우드 병렬 코드리뷰 (v2.1.111), `/less-permission-prompts` 허용 리스트 제안 (v2.1.111)
- **신규 도구 · env**: `ANTHROPIC_BEDROCK_SERVICE_TIER` env var — Bedrock 서비스 티어 선택 (`default`·`flex`·`priority`), `X-Amzn-Bedrock-Service-Tier` 헤더로 전송 (v2.1.122); `ExitWorktree` (v2.1.72), `CLAUDE_CODE_DISABLE_CRON` (v2.1.72), `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` (v2.1.74), `modelOverrides` (v2.1.73), `allowRead` sandbox 설정 (v2.1.77), 토큰 한도 확대 (Opus 4.6 기본 64k·상한 128k, v2.1.77), `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` (서브프로세스 자격증명 제거, v2.1.83), `CLAUDE_STREAM_IDLE_TIMEOUT_MS` (스트리밍 유휴 타임아웃, 기본 90s, v2.1.84), PowerShell 도구 (Windows 옵트인 프리뷰, v2.1.84), `CLAUDE_CODE_MCP_SERVER_NAME`/`CLAUDE_CODE_MCP_SERVER_URL` (headersHelper 다중 서버 구분, v2.1.85), Deep link `claude-cli://open?q=…` 최대 5,000자 지원 (v2.1.85), 트랜스크립트 `/loop`·`CronCreate` 실행 시 타임스탬프 마커 추가 (v2.1.85), `CLAUDE_CODE_NO_FLICKER=1` (플리커 없는 alt-screen 렌더링, v2.1.88), `MCP_CONNECTION_NONBLOCKING=true` (`-p` 모드 MCP 연결 대기 생략; `--mcp-config` 서버 5s 제한, v2.1.89), `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` (git pull 실패 시 기존 마켓플레이스 캐시 유지 — 오프라인 환경용, v2.1.90), `forceRemoteSettingsRefresh` 정책 — CLI 시작 시 원격 managed settings 최신화 강제 (실패 시 종료, v2.1.92), `--remote-control-session-name-prefix` (Remote Control 세션 이름 호스트명 기반 기본값, v2.1.92), `Monitor` 도구 — 백그라운드 스크립트 이벤트 스트리밍 (v2.1.98), `CLAUDE_CODE_PERFORCE_MODE` — 읽기 전용 파일 편집 시 `p4 edit` 힌트 (v2.1.98), `CLAUDE_CODE_USE_MANTLE=1` — Amazon Bedrock Mantle 지원 (v2.1.94), `refreshInterval` status line 재실행 주기 설정 (초 단위, v2.1.97), `workspace.git_worktree` status line JSON 필드 (linked worktree 시 설정, v2.1.97), `--exclude-dynamic-system-prompt-sections` print mode 플래그 (크로스유저 프롬프트 캐시 개선, v2.1.98), `CLAUDE_CODE_CERT_STORE=bundled` — OS CA 인증서 저장소 신뢰 비활성화 (기본: OS CA 신뢰, v2.1.101), `EnterWorktree` `path` 파라미터 — 기존 worktree로 전환 (v2.1.105), `WebFetch` `<style>`·`<script>` 콘텐츠 제거 — CSS 헤비 페이지 컨텍스트 예산 보호 (v2.1.105), `ENABLE_PROMPT_CACHING_1H` — API key·Bedrock·Vertex·Foundry 1시간 캐시 TTL 옵트인 (`ENABLE_PROMPT_CACHING_1H_BEDROCK` deprecated·honored, v2.1.108), `FORCE_PROMPT_CACHING_5M` — 5분 TTL 강제 (v2.1.108), `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` — 텔레메트리 비활성화 시 recap 강제 (v2.1.108), `sandbox.network.deniedDomains` — 광역 허용 도메인 내 특정 도메인 차단 (v2.1.113), `autoScrollEnabled` — 풀스크린 자동 스크롤 비활성화 (v2.1.110), `OTEL_LOG_RAW_API_BODIES` — API 요청·응답 전체 OTEL 로그 (v2.1.111), `CLAUDE_CODE_USE_POWERSHELL_TOOL` — PowerShell 도구 옵트인 Linux/macOS (v2.1.111); **`/usage`** `/cost`+`/stats` 통합 (v2.1.118); custom themes — `/theme` 명령·`~/.claude/themes/`·플러그인 `themes/` 디렉토리 (v2.1.118); `--from-pr` GitLab MR·Bitbucket PR·GitHub Enterprise URL 지원 (v2.1.119); `prUrlTemplate` 설정 — PR 배지 커스텀 URL (v2.1.119); `CLAUDE_CODE_HIDE_CWD` env var — 시작 로고 cwd 숨김 (v2.1.119); `DISABLE_UPDATES` env var — 수동 포함 전체 업데이트 차단 (v2.1.118); `wslInheritsWindowsSettings` 정책 — WSL Windows managed settings 상속 (v2.1.118); `claude plugin tag` — 버전 검증 포함 릴리스 git 태그 생성 (v2.1.118); status line stdin JSON에 `effort.level`·`thinking.enabled` 추가 (v2.1.119); PowerShell 도구 자동 승인 — Bash와 동일 권한 모드 (v2.1.119); vim visual mode `v`/`V` (선택·시각적 피드백, v2.1.118)
- **인증**: OAuth 인증 실패 시 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 설정 환경에서 발생하던 401 재시도 루프 수정 (v2.1.123)
- **Agent**: `SendMessage` — 중단 에이전트 자동 백그라운드 재개 (v2.1.77); Agent tool `resume` 파라미터 제거 → `SendMessage({to: agentId})` 사용 (v2.1.77); `--agent <name>` built-in agent `permissionMode` 준수 (v2.1.119); agent frontmatter `mcpServers` — `--agent` 세션 MCP 서버 로드 (v2.1.117); 외부 빌드 forked subagents `CLAUDE_CODE_FORK_SUBAGENT=1` (v2.1.117)

### Breaking Changes

`$ARGUMENTS.0` → `$ARGUMENTS[0]`, `npm install` → `claude install`, SSE → HTTP, Sonnet 4.5 → 4.6, Opus 4/4.1 → 4.6, Effort max 제거 (○ ◐ ●), **Agent tool `resume` 파라미터 제거** → `SendMessage({to: agentId})` 사용 (v2.1.77), Windows managed settings 레거시 경로 제거 (v2.1.75), plan mode 컨텍스트 초기화 기본 숨김 (`"showClearContextOnPlanAccept": true`로 복원 가능, v2.1.81), Windows/WSL 응답 줄 단위 스트리밍 비활성화 (v2.1.81), **`showThinkingSummaries` 기본값 비활성화** — 설정 복원: `"showThinkingSummaries": true` (v2.1.88), **`cleanupPeriodDays: 0` 검증 오류** — 이전에는 트랜스크립트 영속 비활성화, 이제 명시적 오류 발생 (v2.1.89), **`--resume` picker에서 `claude -p`/SDK 세션 제외** (v2.1.90), **`Get-DnsClientCache`·`ipconfig /displaydns` 자동 허용 제거** — DNS 캐시 프라이버시 보호 (v2.1.90), **`/tag` 명령 제거** (v2.1.92), **`/vim` 명령 제거** → `/config` → Editor mode (v2.1.92), **기본 effort 레벨 medium → high 전환** — API키·Bedrock·Vertex·Foundry·Team·Enterprise 사용자 대상 (v2.1.94); `/effort`로 조정 가능, **Bash deny 규칙 강화** — env/sudo/watch/ionice/setsid 래퍼 명령 매칭 (v2.1.113); `Bash(find:*)` allow 규칙이 `find -exec`/`-delete` 자동 승인 불가 (v2.1.113); macOS `/private/{etc,var,tmp,home}` 경로 `Bash(rm:*)` 위험 경로 처리 (v2.1.113); `Ctrl+U` — 전체 입력 버퍼 클리어로 변경 (`Ctrl+Y`로 복원, v2.1.111); **`--print` 모드 agent frontmatter 준수** — `tools:`/`disallowedTools:` 인터랙티브 모드와 동일 동작 (v2.1.119); **vim INSERT Esc 동작 변경** — 대기 메시지를 입력창으로 당기지 않음, 다시 Esc로 중단 가능 (v2.1.119)

---

## Deprecated (사용 중지)

| Deprecated | 대체 방법 |
|------------|-----------|
| `/output-style` 명령 | `/config` 사용 (v2.1.74); 또는 `--system-prompt-file` / `plugins` |
| `legacy SDK entrypoint` | `@anthropic-ai/claude-agent-sdk`로 마이그레이션 |
| `includeCoAuthoredBy` 설정 | 새 `attribution` 설정 사용 |
| SSE MCP transport | HTTP (streamable-http) 사용 |
| `TaskOutput` 도구 | 백그라운드 태스크 출력 파일 경로에 `Read` 사용 (v2.1.83) |

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
| **Ralph Loop** | 자율 개발 루프 | 매 반복 Fresh | `TASK.md` + `loop.sh` |
| **Graph Workflow** | 구조화된 실행 계획 (신규) | 파일 기반 | `.omc/state/graph/` |

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

**주요 이벤트**: SessionStart, PreToolUse, PostToolUse, Stop, StopFailure, SubagentStop, TeammateIdle, InstructionsLoaded, PostCompact, Elicitation, ElicitationResult, CwdChanged, FileChanged, TaskCreated, PermissionDenied (25개)
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
cat TASK.md PROGRESS.md | claude -p "다음 미완료 작업 수행 후 PROGRESS.md 업데이트. 완료 시 LOOP_COMPLETE 추가"
```

**핵심**: 매 반복 Fresh Context(0%) + 파일/Git으로 상태 유지 + 이중 종료 조건

**상세**: [references/ralph-loop-guide.md](references/ralph-loop-guide.md)

---

## 시나리오 결정 가이드

| 조건 | 선택 |
|------|------|
| 장시간 자율 개발 (30분+, 컨텍스트 열화 방지) | **Ralph Loop** |
| 복잡한 멀티스텝 워크플로우 (조건 분기, 병렬, 반복) | **Graph Workflow** |
| 반복적으로 같은 지침 필요 | **Skill** |
| 여러 에이전트 병렬 협업 | **Agent Team** |
| 독립적 작업 실행 + 커스텀 에이전트 | **Subagent** → Task |
| 독립적 작업 실행 + 내장 타입 | **Task** (Explore, Plan 등) |
| 그 외 | 직접 대화에서 처리 |

---

## 프로젝트 구조 예시

```
.claude/
├── skills/<name>/ ─ SKILL.md (<500줄) + CHANGELOG.md + releases/ + references/
├── agents/<name>.md
├── rules/*.md
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
| [references/eval-guide.md](references/eval-guide.md) | Skill 평가, 벤치마크, 개선 루프 가이드 |
| [references/graph-workflow-guide.md](references/graph-workflow-guide.md) | Graph Workflow 설계, 변환 패턴, 실행 프로토콜 |

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
| [references/official/hooks.md](references/official/hooks.md) | Hooks 공식 문서 요약 (16 events) |
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

시맨틱 코드 검색 설치 (선택): `claude mcp add claude-context` (Gemini+Zilliz 또는 Ollama+Milvus)

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
**Status**: 2026-03-27 | **Claude Code**: v2.1.123+ | **Sync**: [version-sync.md](references/version-sync.md) | [check-updates.sh](../../scripts/check-updates.sh)
