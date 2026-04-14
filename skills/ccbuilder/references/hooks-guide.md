# Hooks 상세 가이드

> Claude Code Hooks 개발 완전 가이드

**Version**: 2.19.0
**Last Updated**: 2026-03-19
**Claude Code Version**: v2.1.79+

---

## Hook 이벤트 (v2.19 최신)

| Event | 트리거 시점 | Decision 제어 | 주요 입력 필드 |
|-------|------------|--------------|---------------|
| **SessionStart** | 세션 시작/재개 | No | `session_id`, `agent_type` |
| **TaskCompleted** | 태스크 완료 | No | `task_id` |
| **UserPromptSubmit** | 프롬프트 제출 전 | No | `prompt` — 출력: `hookSpecificOutput.sessionTitle`으로 세션 제목 설정 가능 (v2.1.94) |
| **PreToolUse** | 도구 호출 전 | Yes (block/modify/defer) | `tool_name`, `tool_input`, `tool_use_id` |
| **PostToolUse** | 도구 호출 후 | No | `tool_name`, `tool_result` |
| **PostToolUseFailure** | 도구 호출 실패 후 | No | `tool_name`, `error` |
| **PermissionRequest** | 권한 다이얼로그 | Yes (allow/deny) | `permission_type` |
| **Stop** | Claude 응답 완료 | Yes (block) | `stop_reason` |
| **SubagentStart** | 서브에이전트 생성 | No | `subagent_type`, `prompt` |
| **SubagentStop** | 서브에이전트 완료 | No | `subagent_result`, `agent_id`, `agent_transcript_path` |
| **TeammateIdle** | 팀메이트 유휴 상태 (v2.7 신규) | No | `teammate_name`, `agent_id` |
| **PreCompact** | 컨텍스트 압축 전 — exit code 2 또는 `{"decision":"block"}` 반환으로 압축 차단 가능 (v2.1.105) | Yes (block) | - |
| **Notification** | 알림 발생 | No | `notification` |
| **Setup** | 초기 설정 | No | `trigger` (init/init-only/maintenance) |
| **WorktreeCreate** | git worktree 생성 (v2.1.50) | No | `worktree_path`, `branch` |
| **WorktreeRemove** | git worktree 제거 (v2.1.50) | No | `worktree_path` |
| **InstructionsLoaded** | CLAUDE.md / `.claude/rules/*.md` 로드 시 (v2.1.69) | No | `file_path` |
| **PostCompact** | 컨텍스트 압축 완료 후 (v2.1.76) | No | - |
| **Elicitation** | MCP 서버 사용자 입력 요청 인터셉트 (v2.1.76) | Yes (override) | `request`, `server` |
| **ElicitationResult** | Elicitation 응답 전송 전 오버라이드 (v2.1.76) | Yes (override) | `result`, `server` |
| **StopFailure** | API 오류(rate limit·인증 실패)로 턴 종료 시 (v2.1.78) | No | `stop_reason`, `error` |
| **PermissionDenied** | auto mode 분류기 거부 후 발동 — `{retry: true}` 반환 시 모델 재시도 가능 (v2.1.88) | Yes (retry) | `tool_name`, `denial_reason` |

**신규 공통 필드 (v2.1.69)**: 모든 Hook 이벤트에 `agent_id` (서브에이전트 ID), `agent_type` (서브에이전트·`--agent`), `worktree` (worktree 세션 정보: name, path, branch, original_repo_dir) 포함

**TeammateIdle · TaskCompleted (v2.1.71)**: `{"continue": false, "stopReason": "..."}` 응답으로 팀메이트 중단 가능 (Stop Hook과 동일 방식)

**settings.json 복원력 (v2.1.101)**: 알 수 없는 훅 이벤트 이름이 있어도 전체 settings.json이 무시되지 않음 — 알 수 없는 이벤트만 건너뜀

**allowManagedHooksOnly (v2.1.101)**: managed settings로 강제 활성화된 플러그인의 훅이 이 설정 하에서도 정상 실행됨

**permissions.deny + PreToolUse (v2.1.101)**: `permissions.deny` 규칙이 `PreToolUse` hook의 `permissionDecision: "ask"` 응답을 다운그레이드로 재정의하지 않도록 수정 (이전에는 hook이 deny를 프롬프트로 약화 가능)

---

## Hook 타입 (v2.12)

### Command Hook (기본)

```json
{
  "type": "command",
  "command": "./hooks/my-hook.sh"
}
```

### HTTP Hook (신규 v2.1.63)

Shell 없이 URL로 JSON POST, JSON 응답 수신:

```json
{
  "type": "http",
  "url": "https://my-server.example.com/hooks/pre-tool",
  "timeout": 5000
}
```

입력/출력 스키마는 command hook과 동일 (decision, reason 등). 인증이 필요한 경우 `headers` 필드 사용 가능.

### Prompt Hook (신규)

```json
{
  "type": "prompt",
  "prompt": "코드 변경 전 보안 검토를 수행하세요. 민감한 정보 노출이 없는지 확인하세요."
}
```

### Agent Hook (신규)

```json
{
  "type": "agent",
  "agent": "security-reviewer"
}
```

---

## 비동기 Hook (신규)

```json
{
  "type": "command",
  "command": "./hooks/slow-analysis.sh",
  "async": true
}
```

---

## Decision 제어

### PreToolUse Decision

```json
// stdout으로 JSON 출력
{
  "decision": "block",
  "reason": "이 작업은 허용되지 않습니다"
}

// 또는 도구 입력 수정
{
  "decision": "modify",
  "tool_input": { "modified": "input" }
}

// v2.1.85: AskUserQuestion 충족 (헤드리스 통합용)
// permissionDecision: "allow" + updatedInput 반환 시
// Claude의 AskUserQuestion을 훅이 직접 처리
{
  "permissionDecision": "allow",
  "updatedInput": { "answer": "사용자 응답 내용" }
}

// v2.1.89: "defer" — 헤드리스 세션에서 도구 호출 일시 중지
// -p --resume 으로 재개 시 훅이 재평가됨
{
  "permissionDecision": "defer"
}
```

### PermissionRequest Decision

```json
{
  "decision": "allow"
}
// 또는
{
  "decision": "deny",
  "reason": "보안 정책 위반"
}
```

### Stop Decision

```json
{
  "decision": "block",
  "reason": "작업이 완료되지 않았습니다. 계속 진행하세요."
}
```

---

## Exit Codes

| Exit Code | 효과 |
|-----------|------|
| **0** | 정상 진행 (stdout → Claude에 표시 또는 decision 처리) |
| **1** | 에러 (stderr → 사용자에게 표시) |
| **2** | 액션 차단 (레거시, decision 방식 권장) |

---

## settings.json 설정 (v2.7)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "echo 'Session started'"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/validate.sh"
          }
        ]
      },
      {
        "matcher": "mcp__*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "MCP 도구 사용 시 주의하세요"
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "type": "command",
        "command": "./hooks/on-error.sh"
      }
    ],
    "SubagentStart": [
      {
        "type": "command",
        "command": "./hooks/subagent-init.sh"
      }
    ],
    "Stop": [
      {
        "type": "command",
        "command": "./hooks/on-stop.sh"
      }
    ],
    "SubagentStop": [
      {
        "type": "command",
        "command": "./hooks/subagent-complete.sh"
      }
    ],
    "TeammateIdle": [
      {
        "type": "command",
        "command": "./hooks/teammate-idle.sh"
      }
    ],
    "Setup": [
      {
        "type": "command",
        "command": "./hooks/setup.sh"
      }
    ]
  }
}
```

---

## Matcher 패턴 (v2.7)

| 패턴 | 매칭 대상 |
|------|----------|
| `"Bash"` | Bash 도구만 |
| `"Edit\|Write"` | Edit 또는 Write |
| `"*"` | 모든 도구 |
| `"mcp__*"` | 모든 MCP 도구 (신규) |
| `"mcp__supabase__*"` | Supabase MCP 도구만 (신규) |

---

## 조건부 실행 — `if` 필드 (v2.1.85)

훅에 `if` 필드를 추가하면 permission rule syntax로 실행 조건을 필터링합니다. 조건에 맞지 않으면 훅 프로세스 자체를 스폰하지 않아 오버헤드를 줄입니다.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/check-git.sh",
            "if": "Bash(git *)"
          }
        ]
      }
    ]
  }
}
```

`if` 값은 `Bash(git *)`, `Write(src/*)` 처럼 permission rule syntax를 사용합니다.

---

## 주의사항

- **SessionStart/SessionEnd/Notification**: TypeScript SDK에서만 지원 (Python SDK 미지원)
- **Stop hook**: `block` decision 반환 시 Claude가 계속 작업 (reason 필수)
- **SubagentStop**: `agent_transcript_path`로 전체 transcript 접근 가능
- **async hooks**: 백그라운드에서 실행, 결과 대기 안함
- **SessionEnd 타임아웃** (v2.1.74): 기존 1.5초 강제 종료 → `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 환경변수로 가변 설정 가능

---

## Hook 예제

### 파일 백업 Hook

```bash
#!/bin/bash
# hooks/backup-on-edit.sh

TOOL_NAME=$(echo "$CLAUDE_TOOL_USE_INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$CLAUDE_TOOL_USE_INPUT" | jq -r '.tool_input.file_path')

if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
  if [[ -f "$FILE_PATH" ]]; then
    cp "$FILE_PATH" "${FILE_PATH}.backup"
  fi
fi

exit 0
```

### 보안 검토 Hook

```bash
#!/bin/bash
# hooks/security-check.sh

CONTENT=$(echo "$CLAUDE_TOOL_USE_INPUT" | jq -r '.tool_input.content // .tool_input.command')

# 민감한 정보 패턴 검사
if echo "$CONTENT" | grep -qE '(password|secret|api_key|token)'; then
  echo '{"decision": "block", "reason": "민감한 정보가 포함되어 있습니다"}'
  exit 0
fi

exit 0
```

---

## Breaking Changes (v2.8-2.9)

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

---

## 공식 문서

- **Hooks Reference**: https://code.claude.com/docs/en/hooks

---

*이 문서는 SKILL.md에서 분리되었습니다 (2026-02-04, v2.9.0 업데이트 2026-02-11)*
