# MCP (Model Context Protocol) 상세 가이드

> Claude Code에서 MCP 서버를 설정하고 활용하는 완전 가이드

**Version**: 2.20.0
**Last Updated**: 2026-07-26
**Claude Code Version**: v2.1.220+

---

## 개요

MCP를 통해 Claude Code에 외부 도구, 데이터 소스, 서비스를 연결할 수 있습니다.

---

## Transport 타입

| Transport | 설명 | 상태 |
|-----------|------|------|
| **HTTP** | HTTP 기반 (streamable-http) | **권장** |
| **SSE** | Server-Sent Events | Deprecated |
| **Stdio** | 로컬 프로세스 (stdin/stdout) | 지원 |

---

## 설치 방법

### HTTP 서버 (권장)

```bash
claude mcp add --transport http <name> <url>

# 예시
claude mcp add --transport http stripe https://mcp.stripe.com
```

### Stdio 서버

```bash
claude mcp add <name> -- <command> [args...]

# 예시
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

### SSE 서버 (Deprecated)

```bash
claude mcp add --transport sse <name> <url>
```

---

## 설치 Scope

```
Local (기본) > Project > User
```

| Scope | 저장 위치 | 설명 |
|-------|-----------|------|
| **Local** | `~/.claude.json` (프로젝트별) | 개인 개발용 (기본값) |
| **Project** | `.mcp.json` (프로젝트 루트) | 팀 공유, Git 커밋 |
| **User** | `~/.claude.json` (전역) | 모든 프로젝트에 적용 |

```bash
# Scope 지정
claude mcp add --scope project <name> -- <command>
claude mcp add --scope user <name> -- <command>
```

---

## .mcp.json 설정

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp@latest"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_KEY:-default_value}"
      }
    },
    "stripe": {
      "type": "http",
      "url": "https://mcp.stripe.com"
    }
  }
}
```

### 환경 변수 확장

```json
{
  "env": {
    "VAR": "${VAR}",              // 환경 변수 참조
    "VAR": "${VAR:-default}"      // 기본값 설정
  }
}
```

### CLAUDE_PROJECT_DIR (v2.1.139+)

Stdio MCP 서버는 `CLAUDE_PROJECT_DIR` 환경변수를 자동으로 수신합니다. Plugin config에서도 `${CLAUDE_PROJECT_DIR}`로 참조 가능:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PROJECT_DIR}/.mcp/server.js"]
    }
  }
}
```

> **주의**: `workspace`는 MCP 예약 서버 이름 (v2.1.128+) — 해당 이름으로 서버 등록 시 경고 후 스킵됨

### 추가 stdio 서버 자동 환경변수 (v2.1.154+)

Stdio MCP 서버 서브프로세스는 다음 환경변수도 자동으로 수신합니다:

| 환경변수 | 값 | 용도 |
|---------|-----|------|
| `CLAUDE_CODE_SESSION_ID` | 현재 세션 ID | 세션별 상태 추적 (`--resume` 시에도 전달, v2.1.163+) |
| `CLAUDECODE` | `1` | Claude Code 실행 환경 감지 |
| `CLAUDE_PROJECT_DIR` | 프로젝트 루트 경로 | 프로젝트 파일 접근 (v2.1.139+) |

---

## OAuth 인증

### 자동 등록 (Dynamic Client Registration)

```bash
claude mcp add --transport http my-server https://mcp.example.com
# OAuth 흐름이 자동으로 시작됨
```

### 수동 등록 (Pre-configured Credentials)

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com",
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "authorizationUrl": "https://auth.example.com/authorize",
        "tokenUrl": "https://auth.example.com/token",
        "scopes": ["read", "write"],
        "authServerMetadataUrl": "https://auth.example.com/.well-known/oauth-authorization-server"
      }
    }
  }
}
```

> **v2.1.74 수정**: OAuth 콜백 포트가 이미 사용 중일 때 인증이 hang되는 버그 수정. 리프레시 토큰 만료 후 HTTP 200으로 오류를 반환하는 OAuth 서버(예: Slack)에서 재인증 프롬프트가 나타나지 않던 버그 수정.

> **v2.1.81 신규**: **CIMD/SEP-991 지원** — Dynamic Client Registration을 지원하지 않는 서버에 대해 Client ID Metadata Document (CIMD) 방식으로 OAuth 등록 가능. 서버가 `/.well-known/oauth-client` 엔드포인트를 노출하면 자동 처리됨.

> **v2.1.85 신규**: **RFC 9728 Protected Resource Metadata discovery** — MCP OAuth가 RFC 9728 표준에 따라 리소스 서버의 `/.well-known/oauth-protected-resource` 메타데이터를 조회해 인증 서버를 자동으로 탐색합니다. `authServerMetadataUrl` 수동 지정 없이도 인증 서버를 찾을 수 있습니다.

> **v2.1.225 수정**: macOS에서 MCP OAuth 서버가 keychain 읽기 타임아웃 후 마치 한 번도 인증되지 않은 것처럼 401 오류가 연쇄적으로 발생하며 간헐적으로 실패하던 버그 수정.

---

## headersHelper 다중 서버 지원 (v2.1.85 신규)

`headersHelper` 스크립트에서 `CLAUDE_CODE_MCP_SERVER_NAME`과 `CLAUDE_CODE_MCP_SERVER_URL` 환경변수를 사용하면 하나의 헬퍼 스크립트로 여러 MCP 서버의 인증 헤더를 처리할 수 있습니다.

```bash
#!/bin/bash
# ~/.claude/mcp-headers.sh — 다중 서버 공용 headersHelper

case "$CLAUDE_CODE_MCP_SERVER_NAME" in
  "github-server")
    echo '{"Authorization": "Bearer '"$GITHUB_TOKEN"'"}'
    ;;
  "jira-server")
    echo '{"Authorization": "Basic '"$JIRA_ENCODED"'"}'
    ;;
  *)
    echo '{}'
    ;;
esac
```

```json
{
  "mcpServers": {
    "github-server": {
      "type": "http",
      "url": "https://mcp.github.example.com",
      "headersHelper": "~/.claude/mcp-headers.sh"
    },
    "jira-server": {
      "type": "http",
      "url": "https://mcp.jira.example.com",
      "headersHelper": "~/.claude/mcp-headers.sh"
    }
  }
}
```

---

## `-p` 모드 MCP 연결 최적화 (v2.1.89 신규)

헤드리스(`-p`) 실행 시 MCP 연결 대기를 건너뛸 수 있습니다.

```bash
# MCP 연결 대기 완전 생략 (-p 모드 전용)
MCP_CONNECTION_NONBLOCKING=true claude -p "prompt"

# --mcp-config 서버 연결은 최대 5s로 자동 제한 (v2.1.89 기본 동작)
```

> **주의**: `MCP_CONNECTION_NONBLOCKING=true` 사용 시 MCP 서버가 완전히 연결되기 전에 첫 요청이 전송됩니다. 빠른 응답이 필요한 자동화 파이프라인에서 사용하세요.

---

## MCP 도구 결과 크기 오버라이드 (v2.1.91 신규)

기본적으로 MCP 도구 결과는 크기 제한이 적용되어 잘릴 수 있습니다. `_meta` 필드의 `anthropic/maxResultSizeChars` 어노테이션으로 최대 500,000자까지 확장할 수 있습니다.

```json
{
  "content": [{ "type": "text", "text": "<large schema or data>" }],
  "_meta": {
    "anthropic/maxResultSizeChars": 500000
  }
}
```

> **용도**: DB 스키마, 대용량 파일 목록 등 기본 제한을 초과하는 도구 결과 전달. MCP 서버 구현 시 응답에 `_meta` 필드를 추가하세요.

---

## MCP Elicitation (v2.1.76 신규)

MCP 서버가 세션 실행 중 사용자에게 구조화된 입력을 요청할 수 있습니다. 대화형 폼 필드 또는 브라우저 URL로 표시됩니다.

Hook으로 인터셉트 가능:
- `Elicitation`: 요청이 표시되기 전에 인터셉트 (응답 오버라이드)
- `ElicitationResult`: 응답이 서버로 전송되기 전에 오버라이드

```json
{
  "hooks": {
    "Elicitation": [{
      "matcher": "my-server",
      "hooks": [{ "type": "command", "command": "./hooks/handle-elicitation.sh" }]
    }]
  }
}
```

---

## alwaysLoad — Tool Search 지연 비활성화 (v2.1.121 신규)

MCP 서버 설정에 `alwaysLoad: true`를 추가하면, 해당 서버의 모든 도구가 tool-search 지연 없이 항상 로드됩니다.

```json
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com",
      "alwaysLoad": true
    }
  }
}
```

> **용도**: 자주 사용하는 MCP 서버의 도구를 tool-search 없이 즉시 접근할 때 사용하세요. Tool Search가 활성화된 환경에서도 해당 서버 도구는 항상 사용 가능합니다.

---

## MCP_TOOL_TIMEOUT — 원격 서버 도구 호출 타임아웃 (v2.1.142 수정)

`MCP_TOOL_TIMEOUT` 환경변수가 원격 HTTP/SSE MCP 서버의 per-request fetch timeout에 이제 올바르게 반영됩니다. 이전에는 설정값과 무관하게 도구 호출이 60초에 상한되었으나, v2.1.142부터 설정값대로 적용됩니다.

```bash
# 도구 호출 타임아웃 설정 (ms)
MCP_TOOL_TIMEOUT=120000  # 120초
```

---

## MCP 서버 시작 자동 재시도 (v2.1.121 신규)

MCP 서버가 시작 시 일시적 오류를 만나면 연결 끊긴 채로 유지되지 않고, 최대 3회 자동 재시도합니다.

---

## MCP 도구 호출 자동 백그라운드 전환 (v2.1.212 신규)

MCP 도구 호출이 2분 이상 실행되면 자동으로 백그라운드로 이동하여 세션이 계속 사용 가능한 상태를 유지합니다.

```bash
# 임계값 변경 또는 비활성화 (ms 단위)
CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=300000  # 5분으로 변경
CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS=0       # 비활성화
```

> **용도**: 장시간 실행되는 MCP 도구(대용량 데이터 처리, 외부 배치 작업 등) 호출 중에도 세션이 멈추지 않고 다른 작업을 계속할 수 있습니다.

---

## Tool Search

MCP 도구가 전체의 10% 이상일 때 자동 활성화됩니다.

```bash
# 설정 옵션
ENABLE_TOOL_SEARCH=auto   # 기본 (10% 이상 시 자동)
ENABLE_TOOL_SEARCH=true   # 항상 활성화
ENABLE_TOOL_SEARCH=false  # 비활성화

# claude.ai MCP 서버 비활성화 (v2.1.63)
ENABLE_CLAUDEAI_MCP_SERVERS=false
```

활성화 시 모든 MCP 도구가 즉시 로드되지 않고, 필요할 때 온디맨드로 검색/로드됩니다.

---

## MCP Resources

MCP 서버가 제공하는 리소스를 `@` 멘션으로 참조:

```
@server:protocol://resource/path
```

---

## Prompts as Commands

MCP 서버의 프롬프트가 슬래시 명령으로 노출됩니다:

```bash
# 형식: /mcp__<server>__<prompt>
/mcp__supabase__query
/mcp__github__create-issue
```

---

## Claude as MCP Server

Claude Code 자체를 MCP 서버로 노출:

```bash
claude mcp serve
```

다른 앱에서 Claude Code를 MCP 서버로 연결하여 사용할 수 있습니다.

> **v2.1.101 수정**: `claude mcp serve` 도구 호출이 `outputSchema`를 검증하는 MCP 클라이언트에서 "Tool execution failed" 오류로 실패하던 버그 수정.

---

## 출력 제한

```bash
# MCP 도구 출력 토큰 제한 (기본: 25,000)
MAX_MCP_OUTPUT_TOKENS=50000
```

---

## Managed MCP (조직 관리)

### managed-mcp.json

조직 차원에서 MCP 서버를 중앙 관리:

```json
{
  "mcpServers": {
    "internal-api": {
      "command": "npx",
      "args": ["@company/mcp-internal"]
    }
  }
}
```

### 정책 기반 제한

```json
{
  "allowedMcpServers": ["supabase", "github"],
  "deniedMcpServers": ["*"]
}
```

제한 방식:
- **Command-based**: 실행 명령어 기반
- **URL-based**: 서버 URL 기반
- **Name-based**: 서버 이름 기반

> **v2.1.219**: `allowedMcpServers`/`deniedMcpServers`의 `${VAR}` 항목이 settings 파일 자체의 `env` 값 대신 **시작 시 환경변수·managed-settings env**에서 해석되도록 변경.

---

## Headless / CI 진단 (v2.1.219)

- 헤드리스 stream-json init 이벤트에 `mcp_server_errors` 필드 추가 — `--mcp-config`로 지정한 서버 중 설정 검증에 실패해 스킵된 항목 목록. 터미널(비-JSON) 실행에서는 시작 시 경고로 표시.
- `claude mcp list`/`/mcp` — 서버 연결 실패 시 HTTP 상태 코드·오류 텍스트 표시; MCP 설정 값에 숨겨진 선행/후행 공백이 있을 때 경고.

---

## MCP CLI 명령어

```bash
claude mcp add <name> -- <command>    # 서버 추가
claude mcp remove <name>              # 서버 제거
claude mcp list                       # 서버 목록
claude mcp reset                      # 모든 서버 초기화

# /mcp 슬래시 명령 (세션 내)
/mcp                                  # MCP 관리 인터페이스
```

---

## Hook에서 MCP 도구 매칭

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__*",
        "hooks": [{ "type": "command", "command": "./hooks/mcp-guard.sh" }]
      },
      {
        "matcher": "mcp__supabase__*",
        "hooks": [{ "type": "command", "command": "./hooks/supabase-guard.sh" }]
      }
    ]
  }
}
```

---

## 트러블슈팅

### 서버 연결 실패

1. `.mcp.json` 문법 검사: `cat .mcp.json | jq .`
2. 환경 변수 설정 확인
3. 서버 직접 실행 테스트: `npx -y @supabase/mcp@latest`

### OAuth 인증 실패

1. `/mcp` 명령으로 인증 상태 확인
2. 토큰 갱신 시도
3. 서버 재등록

### 도구가 너무 많아 로딩 느림

Tool Search 활성화: `ENABLE_TOOL_SEARCH=true`

---

## Breaking Changes (v2.8-2.9)

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

---

## 공식 문서

- **MCP Reference**: https://code.claude.com/docs/en/mcp

---

*이 문서는 v2.9.0 업데이트 (2026-02-11)*
