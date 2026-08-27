# MCP (Model Context Protocol) - Official Reference

> Source: https://code.claude.com/docs/en/mcp

**Last Synced**: 2026-08-27 (v2.1.247)

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
| **자동 백그라운드 전환** | 도구 호출 2분 초과 시 자동 백그라운드 이동 — `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`로 임계값 조정/비활성화 (v2.1.212) |

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
- **v2.1.219**: `${VAR}` 항목은 settings 파일 자체의 `env` 대신 시작 시 환경변수·managed-settings env에서 해석
- **v2.1.243**: `/mcp`·`/plugins`에서 조직이 인증을 관리하는 claude.ai 커넥터에 `managed` 마커 표시

## Headless 진단 (v2.1.219)

- stream-json init 이벤트 `mcp_server_errors` — `--mcp-config` 검증 실패로 스킵된 서버 목록 (터미널 실행 시 시작 경고로도 표시)
- `claude mcp list`/`/mcp` — 연결 실패 시 HTTP 상태·오류 텍스트 표시; 값에 숨은 공백 경고
- **v2.1.247**: Bedrock·Vertex·Foundry(텔레메트리 비활성화 세션 포함) — MCP 서버 연결 실패를 Claude에게 명시적으로 전달, 도구 부재로 오판하지 않도록 개선

## headersHelper 신뢰·격리 (v2.1.238)

- 프로젝트 `.mcp.json`·플러그인·agent 파일 인라인 서버의 `headersHelper`는 해당 폴더 신뢰 다이얼로그 수락 후에만 실행 (`claude -p` 포함)
- 프로젝트 `.mcp.json`·플러그인·agent 파일의 `headersHelper`는 상속 자격증명 env var 없이 실행; user/managed/claude.ai-scope 헬퍼는 Claude 설정 디렉토리에서 실행
- 플러그인 마켓플레이스 `headersHelper` — 설치·업데이트 시에만 실행되어 카탈로그·동일 출처 아카이브용 단기 토큰 발급, 실행 전 명령 표시 + `[y/N]` 확인

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
