# Hooks - Official Reference

> Source: https://code.claude.com/docs/en/hooks

**Last Synced**: 2026-03-01

---

## Hook Events (라이프사이클 순서)

| # | Event | 용도 | 차단 가능 |
|---|-------|------|-----------|
| 1 | `SessionStart` | 세션 시작/재개 | - |
| 2 | `UserPromptSubmit` | 프롬프트 처리 전 | exit 2 |
| 3 | `PreToolUse` | 도구 실행 전 | allow/deny/ask |
| 4 | `PermissionRequest` | 권한 대화상자 표시 | allow/deny |
| 5 | `PostToolUse` | 도구 성공 후 | block |
| 6 | `PostToolUseFailure` | 도구 실패 후 | block |
| 7 | `Notification` | 알림 발송 시 | - |
| 8 | `SubagentStart` | 서브에이전트 생성 | - |
| 9 | `SubagentStop` | 서브에이전트 완료 | block |
| 10 | `Stop` | Claude 응답 완료 | block |
| 11 | `TeammateIdle` | 팀메이트 유휴 상태 | exit 2 |
| 12 | `TaskCompleted` | 태스크 완료 | exit 2 |
| 13 | `PreCompact` | 컨텍스트 압축 전 | - |
| 14 | `Setup` | 초기 설정 (--init, --init-only, --maintenance) | - |
| 15 | `WorktreeCreate` | git worktree 생성 (v2.1.50) | - |
| 16 | `WorktreeRemove` | git worktree 제거 (v2.1.50) | - |

## Handler 타입

| 타입 | 설명 |
|------|------|
| `type: "command"` | Shell 스크립트. stdin JSON, exit code + JSON 응답 |
| `type: "http"` | URL로 JSON POST, JSON 응답 수신 (shell 불필요, v2.1.63) |
| `type: "prompt"` | 단일 LLM 호출. `{ok: true/false, reason: "..."}` |
| `type: "agent"` | 서브에이전트 (도구 접근 가능). prompt와 동일 스키마 |
| `async: true` | 백그라운드 실행 (command hook만). 차단 안 함 |

## Matcher 패턴

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash|Edit|Write",
      "hooks": [{ "type": "command", "command": "./my-hook.sh" }]
    }]
  }
}
```

- Tool events: `tool_name` 매칭 (정규식 지원)
- Session events: `startup`, `resume`, `clear`, `compact` 매칭
- MCP 도구: `mcp__<server>__<tool>` 패턴
- matcher 없거나 `*`이면 전체 매칭

## 설정 위치

| 위치 | 범위 |
|------|------|
| `~/.claude/settings.json` | 전체 프로젝트 |
| `.claude/settings.json` | 프로젝트 (버전 관리) |
| `.claude/settings.local.json` | 프로젝트 (gitignore) |
| Plugin `hooks/hooks.json` | 플러그인 |
| Skill/Agent frontmatter `hooks` | Skill/Agent 스코프 |

## Decision Control

| Event | 필드 | 값 |
|-------|------|-----|
| `PreToolUse` | `hookSpecificOutput.permissionDecision` | `allow` / `deny` / `ask` |
| `PermissionRequest` | `hookSpecificOutput.decision.behavior` | `allow` / `deny` |
| `PostToolUse`, `Stop` 등 | top-level `decision` | `"block"` |

**Exit Codes**: 0 = 성공, 2 = 차단 에러, 기타 = 비차단

## 고급 기능

- **Async Hook**: 백그라운드 실행, 다음 턴에 `systemMessage` 또는 `additionalContext` 반환
- **SessionStart 환경 변수**: `$CLAUDE_ENV_FILE`에 기록하면 세션 전체에서 사용 가능
- **MCP 도구 Hook**: MCP 도구도 일반 도구와 동일하게 Hook 발동

## Deprecation

- `PreToolUse` decision: top-level `decision`/`reason` → `hookSpecificOutput.permissionDecision`/`permissionDecisionReason`으로 변경
