# MCP (Model Context Protocol) - Official Reference

> Source: https://code.claude.com/docs/en/mcp

**Last Synced**: 2026-03-26

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
| **OAuth 2.0** | `/mcp` 명령으로 인증 (자동/수동 등록); CIMD/SEP-991 지원 — Dynamic Client Registration 없는 서버도 지원 (v2.1.81) |
| **Dynamic Updates** | 서버가 `list_changed` 발송 시 도구 목록 갱신 |
| **claude mcp serve** | Claude Code를 MCP 서버로 노출 |
| **Elicitation** | MCP 서버가 세션 중 사용자 입력 요청 (폼·URL); `Elicitation`/`ElicitationResult` Hook으로 인터셉트 (v2.1.76) |
| **--channels** | 채널 capability 선언 MCP 서버가 도구 승인 프롬프트를 폰으로 릴레이 (v2.1.80-81) |
| **도구 호출 축소** | read/search 호출 "Queried {server}" 단일 라인 표시, Ctrl+O로 확장 (v2.1.81) |
| **컨텍스트 2KB 상한** | 도구 설명·서버 지시문 2KB로 제한 — OpenAPI 서버 컨텍스트 팽창 방지 (v2.1.84) |
| **중복 서버 제거** | 로컬과 claude.ai 커넥터 동명 서버 중복 시 로컬 설정 우선 (v2.1.84) |

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

## 안정성 개선 (v2.1.203-217)

- 세션의 추가 작업 디렉토리가 `roots/list`에 포함되고 변경 시 `notifications/roots/list_changed` 전송 (v2.1.203)
- `--mcp-config`/`.mcp.json` 서버의 per-server `request_timeout_ms` 미적용 버그 수정 (v2.1.206)
- `"Claude Browser"` 서버 이름 예약 — 사용자 설정 서버 등록 불가 (v2.1.205)
- 2분 이상 걸리는 MCP 도구 호출 자동 백그라운드 전환 — `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` (v2.1.212)
- 유휴 웹 세션 각성 후 플러그인 MCP 서버 재연결 안 되던 버그 수정 (v2.1.211)
- OAuth 재인증이 신규 로그인 성공 전 기존 자격증명을 폐기하던 버그 수정 (v2.1.216)
- truncated 도구 결과 메모리 누수 수정 (v2.1.217)
