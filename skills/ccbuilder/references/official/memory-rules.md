# Memory & Rules - Official Reference

> Source: https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/settings

**Last Synced**: 2026-03-26

---

## Memory 계층 (우선순위 순)

| # | 계층 | 위치 | 설명 |
|---|------|------|------|
| 1 | **Managed Policy** | 조직 배포 | 최고 우선순위 (관리자 전용) |
| 2 | **Project Memory** | `CLAUDE.md` | 프로젝트 루트 + `@path` imports |
| 3 | **Project Rules** | `.claude/rules/*.md` | 경로별 규칙 (paths: frontmatter) |
| 4 | **User Memory** | `~/.claude/CLAUDE.md` | 전역 사용자 설정 |
| 5 | **Project Local** | `CLAUDE.local.md` | 개인 설정 (자동 gitignore) |

## CLAUDE.md @path Imports

```markdown
@path/to/other-doc.md
@../shared/guidelines.md
```

- 최대 **5hop** 재귀 참조
- 순환 참조 자동 감지

## Project Rules

```markdown
---
paths:
  - "src/api/**"
  - "*.test.ts"
---

# API 코딩 규칙
모든 API 엔드포인트에 에러 핸들링 필수...
```

- `.claude/rules/*.md` 위치
- `paths:` frontmatter로 적용 파일 지정 (glob 패턴 또는 YAML 리스트, v2.1.84)
- 서브디렉토리, symlink 지원
- paths 없으면 전체 프로젝트에 적용

## Auto Memory

| 항목 | 설명 |
|------|------|
| 위치 | `~/.claude/projects/<project>/memory/` |
| 자동 로드 | `MEMORY.md` (매 세션, **200줄/25KB 제한**, v2.1.83) |
| 별도 파일 | 토픽별 파일 생성 후 MEMORY.md에서 링크 |
| 용도 | 안정적 패턴, 아키텍처 결정, 사용자 선호, 반복 문제 해결책 |

### 저장 기준

**저장 O**: 여러 세션에서 확인된 패턴, 사용자가 명시적으로 기억 요청한 것
**저장 X**: 세션 한정 컨텍스트, 미검증 추측, CLAUDE.md와 중복되는 내용

## Settings 파일 계층

| 위치 | 범위 | 버전 관리 |
|------|------|-----------|
| `~/.claude/settings.json` | 전체 프로젝트 | X |
| `.claude/settings.json` | 프로젝트 | O |
| `.claude/settings.local.json` | 프로젝트 (개인) | X (gitignore) |
| `managed-settings.json` | 관리자 | - |
| `managed-settings.d/*.json` | 관리자 (팀별 드롭인, v2.1.83) | - |

## Settings 주요 필드

```json
{
  "env": {},
  "permissions": { "allow": [], "deny": [] },
  "hooks": {},
  "disableAllHooks": false,
  "enableAllProjectMcpServers": false,
  "defaultModel": "string",
  "tools": {},
  "memory": {}
}
```

## 핵심 환경 변수

| 변수 | 설명 |
|------|------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Agent Teams 활성화 (`"1"`) |
| `CLAUDE_CODE_SPAWN_BACKEND` | `tmux` (멀티 세션) |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 커스텀 압축 트리거 % |
| `ENABLE_TOOL_SEARCH` | MCP Tool Search 동작 제어 |
| `MAX_MCP_OUTPUT_TOKENS` | MCP 출력 제한 |
| `MCP_TIMEOUT` | MCP 서버 시작 타임아웃 |
