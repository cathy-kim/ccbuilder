# Sub-agents - Official Reference

> Source: https://code.claude.com/docs/en/sub-agents

**Last Synced**: 2026-08-29 (v2.1.251)

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
| `experimental.cacheTtl` | `"5m"` \| `"1h"` — 에이전트별 프롬프트 캐시 TTL, 서브에이전트 TTL 미설정 시 적용 (v2.1.248) |

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

- **재귀 파견 (v2.1.172+)**: 서브에이전트가 자체 서브에이전트 파견 가능 — 최대 5레벨 깊이. **v2.1.217부터 기본 비활성화**로 변경 — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` 설정 시에만 중첩 허용. **v2.1.219부터 다시 기본 depth 3 허용**으로 변경 — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`로 비활성화
- **동시 실행 상한 (v2.1.217+)**: 기본 20개 동시 서브에이전트 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); 세션당 파견 총량 기본 200개 (`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`, `/clear`로 리셋, v2.1.212+); `--max-budget-usd` 한도 도달 시 신규 스폰 거부 + 실행 중 백그라운드 에이전트 중단
- **Persistent Memory**: `memory` 필드로 세션 간 지식 영속
- **Task Spawning 제한**: `Task(agent-name)`으로 호출 가능한 agent 제한
- **Task tool `mode` 파라미터 제거 (v2.1.212)**: 서브에이전트는 부모 세션 permission mode 기본 상속
- **Tool Search**: MCP 도구가 컨텍스트 10% 초과 시 자동 활성화
- **Skill 프리로드**: `skills` 필드로 Skill 전체 내용을 agent에 주입
- **Resume (v2.1.77 제거)**: Agent tool `resume` 파라미터 제거됨 → `SendMessage({to: agentId})` 로 대체
- **병렬 실행**: 독립적인 리서치는 여러 agent 동시 실행
- **`/fork` vs `/subtask` (v2.1.212 Breaking Change)**: `/fork`는 이제 대화를 새 백그라운드 세션으로 복제(`claude agents` 자체 행); 기존 인라인 서브에이전트 launch 방식은 `/subtask`로 분리
- **EnterWorktree / ExitWorktree**: 격리된 worktree 세션 진입/종료 (v2.1.72); Claude 관리 worktree 간 mid-session 전환 지원 (v2.1.157)
- **팀 에이전트 모델 상속**: Agent Team에서 팀메이트가 리더 모델 자동 상속 (v2.1.72)
- **SendMessage 자동 재개**: 중단된 에이전트에 SendMessage 시 자동으로 백그라운드 재개 (v2.1.77)
- **`settings.json` `agent` 필드**: dispatched 세션 기본 에이전트 지정; `--agent <name>`으로 오버라이드 (v2.1.157)
- **agent 이름 제약 (v2.1.218+)**: agent frontmatter `name`에 `:` 포함 시 거부 — 플러그인 네임스페이싱 예약 문자
- **reasoning effort (v2.1.215+)**: `subagentStatusLine` payload에 effort 레벨 포함 — 커스텀 상태줄에서 모델·effort 렌더링 가능
- **`CLAUDE_CODE_SUBAGENT_MODEL` 동작 변경 (v2.1.251)**: 모든 서브에이전트를 강제 오버라이드하던 방식에서 **기본 서브에이전트 모델 지정**으로 변경 — agent 정의의 `model:` frontmatter와 파견 시 명시적 모델 지정이 이 값보다 우선함
- **Remote Control 실시간 스트리밍 (v2.1.251)**: foreground 서브에이전트의 도구 호출·결과가 Remote Control 클라이언트에 실시간 스트리밍됨 (백그라운드 서브에이전트는 기존처럼 상태만 표시)
- **모델 404 자동 폴백 (v2.1.247)**: 서브에이전트가 첫 호출에서 모델 404를 받으면 세션의 fallback 모델 체인을 사용; 부모에게 반환되는 오류에 오류 타입·상태·request id·모델명 포함
- **부모/형제 에이전트 메시지 응답 (v2.1.251 수정)**: 백그라운드 서브에이전트가 이름 없는 형제·부모 에이전트가 보낸 메시지에도 응답 가능 (이전에는 `from`이 agent type이라 주소 지정 불가)
