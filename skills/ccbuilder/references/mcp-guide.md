# MCP (Model Context Protocol) 상세 가이드

> Claude Code에서 MCP 서버를 설정하고 활용하는 완전 가이드

**Version**: 2.18.0
**Last Updated**: 2026-03-17
**Claude Code Version**: v2.1.77+

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
