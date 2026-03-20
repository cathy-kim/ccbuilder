# MCP (Model Context Protocol) - Official Reference

> Source: https://code.claude.com/docs/en/mcp

**Last Synced**: 2026-03-17

---

## Transport 방식

| Transport | 명령어 | 상태 |
|-----------|--------|------|
| **HTTP** | `claude mcp add --transport http <name> <url>` | 권장 (streamable-http) |
| **SSE** | `claude mcp add --transport sse <name> <url>` | **Deprecated** |
| **Stdio** | `claude mcp add --transport stdio <name> -- <cmd>` | 로컬 서버 |

## 설정 Scope

| Scope | 저장 위치 | 적용 범위 |
|-------|-----------|-----------|
| `local` (기본) | `~/.claude.json` | 현재 프로젝트만 |
| `project` | `.mcp.json` | 팀 공유 (버전 관리) |
| `user` | `~/.claude.json` | 모든 프로젝트 |
| `managed` | `managed-mcp.json` | 관리자 제어 |

## .mcp.json 예시

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {
        "API_KEY": "${API_KEY}",
        "TIMEOUT": "${TIMEOUT:-30}"
      }
    }
  }
}
```

- 환경 변수 확장: `${VAR}`, `${VAR:-default}`

## 주요 기능

| 기능 | 설명 |
|------|------|
| **Resources** | `@server:protocol://path`로 참조 |
| **Prompts as Commands** | `/mcp__server__prompt`로 실행 |
| **Tool Search** | MCP 도구 10%+ 컨텍스트 초과 시 자동 활성화 |
| **OAuth 2.0** | `/mcp` 명령으로 인증 (자동/수동 등록) |
| **Dynamic Updates** | 서버가 `list_changed` 발송 시 도구 목록 갱신 |
| **claude mcp serve** | Claude Code를 MCP 서버로 노출 |
| **Elicitation** | MCP 서버가 세션 중 사용자 입력 요청 (폼·URL); `Elicitation`/`ElicitationResult` Hook으로 인터셉트 (v2.1.76) |
| **--channels** | MCP 서버가 세션에 메시지 직접 푸시 (research preview, v2.1.80) |

## Managed MCP (조직 관리)

**방법 1**: `managed-mcp.json` - 관리자 전용 제어 (사용자 커스터마이징 불가)

**방법 2**: 허용/차단 목록
```json
{
  "allowedMcpServers": [{ "serverName": "approved-*" }],
  "deniedMcpServers": [{ "serverUrl": "*.untrusted.com" }]
}
```
- 필터: `serverName`, `serverCommand`, `serverUrl` (와일드카드 지원)
- **차단 목록이 항상 우선**

## 출력 제한

| 설정 | 기본값 |
|------|--------|
| Warning threshold | 10,000 tokens |
| Max output | 25,000 tokens |
| Override | `MAX_MCP_OUTPUT_TOKENS` 환경 변수 |

## CLI 명령어

```bash
claude mcp add <name> -- <command>     # 서버 추가
claude mcp remove <name>               # 서버 제거
claude mcp list                        # 서버 목록
claude mcp serve                       # Claude Code를 MCP 서버로
claude mcp add-from-claude-desktop     # Claude Desktop에서 가져오기
```
