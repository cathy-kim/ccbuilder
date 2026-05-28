# Hooks - Official Reference

> Source: https://code.claude.com/docs/en/hooks

**Last Synced**: 2026-03-26

---

## Hook Events (라이프사이클 순서)

| # | Event | 용도 | 차단 가능 |
|---|-------|------|-----------|
| 1 | `SessionStart` | 세션 시작/재개 | - |
| 2 | `UserPromptSubmit` | 프롬프트 처리 전 | exit 2 |
| 3 | `PreToolUse` | 도구 실행 전 | allow/deny/ask/defer |
| 4 | `PermissionRequest` | 권한 대화상자 표시 | allow/deny |
| 5 | `PostToolUse` | 도구 성공 후 — `duration_ms` 포함 (v2.1.119) | block |
| 6 | `PostToolUseFailure` | 도구 실패 후 — `duration_ms` 포함 (v2.1.119) | block |
| 7 | `Notification` | 알림 발송 시 | - |
| 8 | `SubagentStart` | 서브에이전트 생성 | - |
| 9 | `SubagentStop` | 서브에이전트 완료 — `background_tasks`·`session_crons` 입력 필드 포함 (v2.1.145) | block |
| 10 | `Stop` | Claude 응답 완료 — `background_tasks`·`session_crons` 입력 필드 포함 (v2.1.145) | block |
| 11 | `TeammateIdle` | 팀메이트 유휴 상태 | exit 2 |
| 12 | `TaskCompleted` | 태스크 완료 | exit 2 |
| 13 | `PreCompact` | 컨텍스트 압축 전 — exit code 2 또는 `{"decision":"block"}` 반환으로 차단 가능 (v2.1.105) | block |
| 14 | `Setup` | 초기 설정 (--init, --init-only, --maintenance) | - |
| 15 | `WorktreeCreate` | git worktree 생성 (v2.1.50); HTTP type 지원 → `hookSpecificOutput.worktreePath` 반환 (v2.1.84) | - |
| 16 | `WorktreeRemove` | git worktree 제거 (v2.1.50) | - |
| 17 | `InstructionsLoaded` | CLAUDE.md / `.claude/rules/*.md` 로드 시 (v2.1.69) | - |
| 18 | `PostCompact` | 컨텍스트 압축 완료 후 (v2.1.76) | - |
| 19 | `Elicitation` | MCP 서버 사용자 입력 요청 인터셉트 (v2.1.76) | override |
| 20 | `ElicitationResult` | Elicitation 응답 전송 전 오버라이드 (v2.1.76) | override |
| 21 | `StopFailure` | API 오류(rate limit·인증 실패)로 턴 종료 시 (v2.1.78) | - |
| 22 | `CwdChanged` | 작업 디렉토리 변경 시 — 반응형 환경 관리 (direnv 등) (v2.1.83) | - |
| 23 | `FileChanged` | 파일 변경 감지 시 (v2.1.83) | - |
| 24 | `TaskCreated` | `TaskCreate` 호출로 태스크 생성 시 (v2.1.84) | - |
| 25 | `PermissionDenied` | auto mode 분류기 거부 후 발동 — `{retry: true}` 반환 시 모델 재시도 (v2.1.88) | retry |
| 26 | `MessageDisplay` | 어시스턴트 메시지 텍스트 표시 전 발동 — 변환·숨김 처리 가능 (v2.1.152) | transform/hide |

## Handler 타입

| 타입 | 설명 |
|------|------|
| `type: "command"` | Shell 스크립트. stdin JSON, exit code + JSON 응답 |
| `type: "http"` | URL로 JSON POST, JSON 응답 수신 (shell 불필요, v2.1.63) |
| `type: "prompt"` | 단일 LLM 호출. `{ok: true/false, reason: "..."}` |
| `type: "agent"` | 서브에이전트 (도구 접근 가능). prompt와 동일 스키마 |
| `type: "mcp_tool"` | MCP 도구 직접 호출 — `server`, `tool`, `arguments` 필드 지정 (v2.1.118) |
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
| `PreToolUse` | `hookSpecificOutput.permissionDecision` | `allow` / `deny` / `ask` / `defer` (v2.1.89: 헤드리스 세션 일시 중지 후 `-p --resume` 재평가) |
| `PermissionRequest` | `hookSpecificOutput.decision.behavior` | `allow` / `deny` |
| `PostToolUse`, `Stop` 등 | top-level `decision` | `"block"` |

**Exit Codes**: 0 = 성공, 2 = 차단 에러, 기타 = 비차단

## 고급 기능

- **Async Hook**: 백그라운드 실행, 다음 턴에 `systemMessage` 또는 `additionalContext` 반환
- **SessionStart 환경 변수**: `$CLAUDE_ENV_FILE`에 기록하면 세션 전체에서 사용 가능
- **MCP 도구 Hook**: MCP 도구도 일반 도구와 동일하게 Hook 발동
- **`terminalSequence`** (v2.1.141): Hook JSON 출력에 추가 가능 — 제어 터미널 없이 데스크탑 알림·창 제목·벨 신호 발송 (예: tmux 알림, 터미널 벨)

## Deprecation

- `PreToolUse` decision: top-level `decision`/`reason` → `hookSpecificOutput.permissionDecision`/`permissionDecisionReason`으로 변경
