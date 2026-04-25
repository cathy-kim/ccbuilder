# Sub-agents - Official Reference

> Source: https://code.claude.com/docs/en/sub-agents

**Last Synced**: 2026-03-26 (v2.1.84)

---

## 내장 Agent 타입

| 타입 | 모델 | 도구 | 용도 |
|------|------|------|------|
| `Explore` | Haiku | 읽기 전용 | 파일 탐색/분석 |
| `Plan` | - | 읽기 전용 | Plan 모드 리서치 |
| `general-purpose` | - | 전체 | 복잡한 멀티 스텝 작업 |
| `Bash` | - | Bash만 | 명령 실행 |
| `statusline-setup` | - | Read, Edit | 상태줄 설정 |
| `claude-code-guide` | - | 웹 검색 등 | Claude Code 질문 답변 |

## Frontmatter 필드

| 필드 | 설명 |
|------|------|
| `name` | Agent 이름 (필수) |
| `description` | Agent 설명 (필수) |
| `tools` | 허용 도구 목록 (미지정 시 전체 상속) |
| `disallowedTools` | 차단 도구 목록 |
| `model` | `sonnet`, `opus`, `haiku`, `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | 최대 에이전트 턴 수 |
| `effort` | 모델 effort 레벨 (`low`, `medium`, `high`) — 플러그인 배포 에이전트 (v2.1.78) |
| `skills` | 프리로드할 Skill (전체 내용 주입) |
| `mcpServers` | 사용 가능 MCP 서버 |
| `hooks` | Agent 스코프 라이프사이클 훅 |
| `memory` | 영속 메모리 범위 (`user`, `project`, `local`) |
| `initialPrompt` | 에이전트 첫 턴 자동 제출 내용 (v2.1.83) |

## 파일 위치 & 우선순위

```
CLI flag --agents (세션) > .claude/agents/ (프로젝트) > ~/.claude/agents/ (사용자) > Plugin agents/
```

## Task Tool로 호출

```json
{
  "subagent_type": "my-custom-agent",
  "prompt": "API 엔드포인트 구현해줘",
  "name": "api-builder",
  "team_name": "my-team",
  "run_in_background": true
}
```

- `subagent_type`: 내장 또는 커스텀 agent 이름
- `name`: 팀 내 표시 이름
- `team_name`: Agent Team 소속
- `run_in_background`: 백그라운드 실행
- `model`: per-invocation 모델 오버라이드 (v2.1.72 복원, e.g. `"claude-opus-4-6"`)

## 고급 기능

- **Persistent Memory**: `memory` 필드로 세션 간 지식 영속
- **Task Spawning 제한**: `Task(agent-name)`으로 호출 가능한 agent 제한
- **Tool Search**: MCP 도구가 컨텍스트 10% 초과 시 자동 활성화
- **Skill 프리로드**: `skills` 필드로 Skill 전체 내용을 agent에 주입
- **Resume (v2.1.77 제거)**: Agent tool `resume` 파라미터 제거됨 → `SendMessage({to: agentId})` 로 대체
- **--print frontmatter 준수 (v2.1.119)**: `--print` 모드에서 에이전트 `tools:`·`disallowedTools:` frontmatter 적용 (인터랙티브 모드와 동일)
- **--agent permissionMode 준수 (v2.1.119)**: `--agent <name>`으로 built-in 에이전트 실행 시 정의된 `permissionMode` 준수
- **병렬 실행**: 독립적인 리서치는 여러 agent 동시 실행
- **EnterWorktree / ExitWorktree**: 격리된 worktree 세션 진입/종료 (v2.1.72)
- **팀 에이전트 모델 상속**: Agent Team에서 팀메이트가 리더 모델 자동 상속 (v2.1.72)
- **SendMessage 자동 재개**: 중단된 에이전트에 SendMessage 시 자동으로 백그라운드 재개 (v2.1.77)
