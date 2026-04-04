# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-04-04
**현재 지원 버전**: v2.1.63+ (SKILL.md v2.12.0)

---

## 자동화 설정

### GitHub Actions (권장)

`.github/workflows/auto-version-sync.yml` 워크플로우가 매일 자동 실행됩니다:

- **스케줄**: 매일 오전 9시 (UTC) = 한국시간 오후 6시
- **동작**: 새 버전 감지 시 SKILL 백업 → 버전 업데이트 → Claude Code Action 콘텐츠 분석 → PR 자동 생성
- **수동 트리거**: Actions 탭에서 "Run workflow" 가능 (force 옵션)

### 알림 받기

1. GitHub Issue 알림 활성화
2. (선택) Slack 웹훅 설정 (워크플로우 파일 참조)

---

## 주간 업데이트 체크리스트

### 1. 공식 소스 확인

- [ ] [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [ ] [Skills 문서](https://code.claude.com/docs/en/skills)
- [ ] [Hooks 문서](https://code.claude.com/docs/en/hooks)
- [ ] [Subagents 문서](https://code.claude.com/docs/en/sub-agents)
- [ ] [Slash Commands 문서](https://code.claude.com/docs/en/slash-commands)
- [ ] [MCP 문서](https://code.claude.com/docs/en/mcp)
- [ ] [Memory 문서](https://code.claude.com/docs/en/memory)

### 2. 변경 사항 분석

| 확인 항목 | 체크 |
|----------|------|
| 새로운 Hook 이벤트 | [ ] |
| 새로운 frontmatter 필드 | [ ] |
| Deprecated 기능 | [ ] |
| 새로운 내장 Subagent | [ ] |
| 새로운 도구/명령어 | [ ] |
| 버그 수정 영향 | [ ] |

### 3. 업데이트 적용

```bash
# 1. 버전 백업 생성
cp SKILL.md releases/v$(date +%Y%m%d)_SKILL.md

# 2. SKILL.md 버전 헤더 업데이트
# **Claude Code Version**: vX.X.X+

# 3. 관련 참조 문서 업데이트
# - references/skills-guide.md
# - references/hooks-guide.md
# - references/subagents-guide.md

# 4. CHANGELOG.md 기록

# 5. 테스트
```

### 4. 검증

- [ ] SKILL.md < 500줄 유지
- [ ] 모든 링크 유효성 확인
- [ ] 예시 코드 검증
- [ ] frontmatter 옵션 테스트

---

## 버전별 주요 변경 사항 추적

### v2.1.92 (2026-04-04 동기화)

**새로운 기능:**
- `forceRemoteSettingsRefresh` policy 설정 — 원격 관리 설정 강제 갱신, 취득 실패 시 CLI 종료 (fail-closed)
- 인터랙티브 Bedrock 설정 마법사 — 로그인 화면 "3rd-party platform" 선택 시 AWS 인증·리전·모델 핀 단계별 안내
- 구독 사용자 `/cost` 모델별·캐시 히트 분할 분석
- `/release-notes` 인터랙티브 버전 피커로 개선
- Remote Control 세션 이름 hostname 기본 프리픽스, `--remote-control-session-name-prefix`로 오버라이드 가능
- Pro 사용자 프롬프트 캐시 만료 후 세션 복귀 시 미캐시 토큰 수 힌트 표시

**Breaking Changes:**
- `/tag` 명령 제거
- `/vim` 명령 제거 → `/config` → Editor mode에서 vim 모드 토글

**주요 버그 수정:**
- 서브에이전트 스폰 — tmux 창 종료·번호 재할당 후 "Could not determine pane count" 영구 실패 수정
- Stop Hook — 소형 모델 `ok:false` 반환 시 잘못 실패 + 비Stop 훅 `preventContinuation:true` 시맨틱 복원
- 스트리밍 배열/객체 필드 JSON 인코딩 문자열 전송 시 도구 입력 검증 실패 수정
- 확장 사고 공백 텍스트 블록 생성 시 API 400 오류 수정
- Write 도구 대용량 파일 diff 계산 60% 성능 개선 (탭·`&`·`$` 포함 파일)
- Linux 샌드박스 `apply-seccomp` 헬퍼 npm·native 빌드 모두 포함 (unix-socket 차단 복원)

### v2.1.91 (2026-04-04 동기화)

**새로운 기능:**
- MCP 도구 결과 크기 오버라이드 — `_meta["anthropic/maxResultSizeChars"]` 어노테이션, 최대 500K (DB 스키마 등 대용량 결과)
- `disableSkillShellExecution` 설정 — 스킬/슬래시 명령/플러그인 인라인 셸 실행 비활성화
- 플러그인 `bin/` 실행 파일 지원 — Bash 도구에서 bare 명령으로 직접 실행 가능
- `claude-cli://open?q=` 딥 링크 멀티라인 프롬프트 지원 (`%0A` 인코딩 허용)

**주요 버그 수정:**
- `--resume` 트랜스크립트 체인 끊김 — 비동기 쓰기 실패 시 대화 이력 유실 수정
- 다양한 터미널(iTerm2, kitty 등)에서 `cmd+delete` 줄 시작까지 삭제 미작동 수정
- Remote 세션에서 플랜 모드 컨테이너 재시작 후 플랜 파일 추적 실패 수정
- `permissions.defaultMode: "auto"` JSON 스키마 검증 오류 수정
- Edit 도구 단축 `old_string` 앵커 사용으로 출력 토큰 감소

### v2.1.90 (2026-04-02 동기화)

**새로운 기능:**
- `/powerup` 명령 — 애니메이션 데모와 함께 Claude Code 기능 인터랙티브 학습
- `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` env var — git pull 실패 시 마켓플레이스 캐시 유지 (오프라인 환경용)
- `.husky` 디렉토리를 acceptEdits 모드 보호 디렉토리에 추가

**Breaking Changes:**
- `--resume` picker에서 `claude -p`/SDK 세션 제외 — 인터랙티브 세션만 표시
- `Get-DnsClientCache`·`ipconfig /displaydns` 자동 허용 목록 제거 — DNS 캐시 프라이버시 보호

**주요 버그 수정:**
- Rate-limit 옵션 다이얼로그 무한 반복 자동 재오픈 → 세션 크래시 수정
- `--resume` deferred tools/MCP/커스텀 에이전트 포함 세션 첫 요청 프롬프트 캐시 미스 수정 (v2.1.69 회귀)
- PostToolUse format-on-save Hook이 연속 편집 사이에 파일 재작성 시 Edit/Write 실패 수정
- `PreToolUse` Hook JSON 출력 + exit code 2 도구 호출 차단 미작동 수정
- Auto mode 명시적 사용자 경계 무시 수정 ("don't push", "wait for X before Y")
- PowerShell 도구 권한 검사 강화 (trailing `&`, `-ErrorAction Break`, TOCTOU 등)
- SSE transport 대용량 프레임 처리 성능 개선 (이차 → 선형 시간)
- SDK 롱 세션 트랜스크립트 쓰기 성능 개선 (이차 시간 저하 수정)
- MCP 도구 스키마 캐시 키 조회 시 매 턴 JSON.stringify 제거 (성능 개선)

### v2.1.89 (2026-04-01 동기화)

**새로운 기능:**
- `"defer"` 권한 결정 — `PreToolUse` Hook에서 헤드리스 세션의 도구 호출 일시 중지, `-p --resume`으로 Hook 재평가
- `MCP_CONNECTION_NONBLOCKING=true` — `-p` 모드에서 MCP 연결 대기 완전 생략; `--mcp-config` 서버 연결 최대 5s 제한
- Auto mode 거부 명령 UX 개선 — 알림 표시 + `/permissions` → Recent 탭에서 `r`로 재시도
- Hook 출력 50K 초과 시 디스크 저장 — 파일 경로 + 미리보기를 컨텍스트에 주입
- `TaskCreated` Hook 이벤트 차단 동작(blocking behavior) 공식 문서화
- `Edit` 도구가 `Bash`에서 `sed -n`/`cat`으로 확인한 파일에 별도 `Read` 없이 동작

**Breaking Changes:**
- `cleanupPeriodDays: 0` 설정 시 검증 오류 발생 — 이전에는 트랜스크립트 영속 비활성화, 이제 명시적 오류

**주요 버그 수정:**
- Edit/Write 도구 Windows CRLF 이중 변환 및 Markdown 하드 라인 브레이크 제거 수정
- `-p --resume` 64KB 초과 입력 또는 deferred 마커 없을 때 행어 수정
- `autocompact` 쓰레싱 루프 3회 반복 시 명확한 오류로 중단
- 롱 세션 중첩 CLAUDE.md 수십 번 재주입 버그 수정
- 프롬프트 히스토리 CJK/이모지 4KB 경계 유실 수정 (`~/.claude/history.jsonl`)
- `/stats` 서브에이전트 토큰 미집계 및 30일 이력 손실 수정
- "Rate limit reached" 오해 메시지 → 실제 entitlement 오류 + actionable 힌트

---

### v2.1.88 (2026-03-31 동기화)

**새로운 기능:**
- `PermissionDenied` Hook 이벤트 — auto mode 분류기 거부 후 발동, `{retry: true}` 반환 시 모델 재시도 가능
- `CLAUDE_CODE_NO_FLICKER=1` env var — 플리커 없는 alt-screen 렌더링 (가상 스크롤백 포함)
- Named subagents — `@` 멘션 타입어헤드에 Named Subagent 이름 포함
- v2.1.86: `X-Claude-Code-Session-Id` 헤더 — API 요청 세션 ID 포함, 프록시 집계 지원
- v2.1.86: `.jj`(Jujutsu), `.sl`(Sapling) VCS 메타데이터 디렉토리 Grep/자동완성 제외

**Breaking Changes:**
- `showThinkingSummaries` 기본값 false로 변경 — 복원: `"showThinkingSummaries": true` in settings.json

**주요 버그 수정:**
- Hook `if` 조건 필터링 — 복합 명령(`ls && git push`) 및 env-var 접두사 명령(`FOO=bar git push`) 매칭 수정
- `PreToolUse`/`PostToolUse` Hook에서 Write/Edit/Read `file_path`가 절대 경로로 반환되지 않던 버그 수정
- 프롬프트 캐시 미스 — 롱 세션 중 도구 스키마 바이트 변경으로 캐시 미스 발생하던 버그 수정
- `StructuredOutput` 스키마 캐시 버그 — 다중 스키마 워크플로우 ~50% 실패율 수정
- `--resume` 크래시 — 이전 버전 tool result 포함 트랜스크립트 처리 수정
- LSP 서버 좀비 상태 — 크래시 후 다음 요청 시 자동 재시작 (세션 재시작 불필요)
- 메모리 누수 — 대형 JSON 입력 LRU 캐시 키 유지 수정
- v2.1.87: Cowork Dispatch 메시지 미전달 수정
- v2.1.86: `--resume` "tool_use ids without tool_result blocks" 오류 수정

---

### v2.1.85 (2026-03-27 동기화)

**새로운 기능:**
- Hook `if` 필드 — permission rule syntax (`Bash(git *)`)로 훅 조건부 실행 필터링, 프로세스 스폰 오버헤드 감소
- `PreToolUse` hook `updatedInput` + `permissionDecision: "allow"` 반환으로 `AskUserQuestion` 충족 — 헤드리스 통합에서 custom UI로 대화형 질문 처리
- `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL` env vars — MCP `headersHelper` 스크립트에서 서버 이름·URL 접근 (하나의 헬퍼로 다중 MCP 서버 처리)
- MCP OAuth RFC 9728 Protected Resource Metadata discovery — 인증 서버 자동 탐색
- 조직 정책(`managed-settings.json`) 차단 플러그인 설치·활성화 불가 및 마켓플레이스 숨김
- Deep link `claude-cli://open?q=…` 최대 5,000자 지원 (긴 프롬프트 시 "scroll to review" 경고)
- 트랜스크립트에 `/loop`, `CronCreate` 스케줄 작업 실행 시 타임스탬프 마커 추가
- `tool_parameters` OpenTelemetry tool_result 이벤트 `OTEL_LOG_TOOL_DETAILS=1` 플래그로 게이팅

**주요 버그 수정:**
- `/compact` "context exceeded" 오류 — 대화가 compact 요청보다 클 때 실패하던 버그 수정
- `deniedMcpServers` 설정이 claude.ai MCP 서버를 차단하지 못하던 버그 수정
- MCP step-up 재인증 — 리프레시 토큰 존재 시 `403 insufficient_scope`로 재인증 흐름 미트리거 수정
- Python Agent SDK `--mcp-config`의 `type:'sdk'` MCP 서버 시작 시 누락 수정
- Remote Control 권한 해결 후 "Requires Action" 상태 고착 수정
- Kitty 키보드 프로토콜 지원 터미널(Ghostty·Kitty·WezTerm 등) 종료 후 enhanced keyboard mode 잔류 수정
- 원격 세션 스트리밍 중단 시 메모리 누수 수정
- 대형 트랜스크립트 스크롤 성능 개선 (WASM yoga-layout → pure TypeScript)

---

### v2.1.84 (2026-03-26 동기화)

**새로운 기능:**
- PowerShell 도구 — Windows 옵트인 프리뷰
- `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL_SUPPORTS` env vars — Bedrock/Vertex/Foundry 고정 모델 capability 오버라이드; `_MODEL_NAME`/`_DESCRIPTION`으로 `/model` 픽커 레이블 커스텀
- `CLAUDE_STREAM_IDLE_TIMEOUT_MS` env var — 스트리밍 유휴 워치독 타임아웃 (기본 90초)
- `TaskCreated` Hook 이벤트 — `TaskCreate` 호출 시 발동
- `WorktreeCreate` Hook `type: "http"` 지원 — `hookSpecificOutput.worktreePath`로 경로 반환
- `allowedChannelPlugins` 관리형 설정 — 팀/Enterprise 채널 플러그인 허용 목록
- Rules/Skills `paths:` frontmatter YAML 리스트 glob 지원
- MCP 도구 설명·서버 지시문 2KB 상한 (OpenAPI 서버 컨텍스트 팽창 방지)
- 로컬과 claude.ai 커넥터 중복 MCP 서버 제거 (로컬 설정 우선)
- 75분+ 유휴 복귀 시 `/clear` 넛지 프롬프트
- Global system-prompt 캐싱이 `ToolSearch` 활성화 시에도 작동 (MCP 도구 포함)
- [VSCode] rate limit 경고 배너 (사용량 % + 리셋 시간)
- 토큰 수 ≥1M을 "1.5m" 형식으로 표시
- issue/PR 참조 링크: `owner/repo#123` 형식만 클릭 가능 (bare `#123` 비활성화)

**주요 버그 수정:**
- voice push-to-talk 입력 누출 및 트랜스크립트 삽입 위치 수정
- `Ctrl+U` 멀티라인 입력에서 줄 경계 작동 수정
- 워크플로우 서브에이전트가 `--json-schema`와 함께 API 400 오류 발생하는 버그 수정
- partial clone 레포(Scalar/GVFS) 시작 시 mass blob 다운로드 트리거 성능 문제 수정
- CJK IME 인라인 렌더링 및 스크린 리더 입력 추적 수정
- macOS transient 키체인 읽기 실패로 "Not logged in" 오류 수정

---

### v2.1.83 (2026-03-26 동기화)

**새로운 기능:**
- `managed-settings.d/` 드롭인 디렉토리 — 팀별 독립 정책 파편 알파벳순 병합
- `CwdChanged`, `FileChanged` Hook 이벤트 — 반응형 환경 관리 (direnv 등)
- `sandbox.failIfUnavailable` 설정 — 샌드박스 미시작 시 에러로 종료
- `disableDeepLinkRegistration` 설정 — `claude-cli://` 프로토콜 핸들러 등록 방지
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` — Bash 도구·훅·MCP stdio 서버의 Anthropic/클라우드 자격증명 제거
- 트랜스크립트 검색 — `Ctrl+O` 모드에서 `/` 입력, `n`/`N`으로 매치 이동
- `Ctrl+X Ctrl+E` 외부 에디터 alias (readline 네이티브, `Ctrl+G` 유지)
- Agent frontmatter `initialPrompt` — 에이전트 첫 턴 자동 제출
- `chat:killAgents`, `chat:fastMode` keybindings.json으로 리바인딩 가능
- `Ctrl+L` 화면 강제 전체 재드로우 (Cmd+K 후 UI 복구)
- MEMORY.md 25KB 트런케이션 추가 (기존 200줄 제한에 추가)
- Plugin MCP 서버가 org 관리형 커넥터와 중복 시 억제
- `--bare -p` SDK 패턴 API 요청까지 ~14% 빠름

**Breaking Changes:**
- `TaskOutput` 도구 deprecated → 백그라운드 태스크 출력 파일 경로에 `Read` 사용
- "stop all background agents" 키바인딩: `Ctrl+F` → `Ctrl+X Ctrl+K` (readline forward-char 충돌 해소)

**주요 버그 수정:**
- `--mcp-config` CLI 플래그가 `allowedMcpServers`/`deniedMcpServers` 정책 우회하던 버그 수정
- 백그라운드 서브에이전트가 컨텍스트 컴팩션 후 보이지 않아 중복 생성되던 버그 수정
- 백그라운드 에이전트 태스크가 git/API 호출 hang 시 "running" 상태 고착 수정
- 미설치 플러그인 훅이 다음 세션까지 계속 발동하는 버그 수정
- SDK 세션 히스토리 손실 (훅 progress/attachment 메시지의 parentUuid 체인 분기) 수정
- 대형 파일 diff hang — 5초 타임아웃 후 graceful fallback
- macOS caffeinate 프로세스 종료 미완료로 Mac 수면 방지 버그 수정

---

### v2.1.81 (2026-03-23 동기화)

**새로운 기능:**
- `--bare` 플래그 — 스크립트형 `-p` 호출 경량 모드: 훅·LSP·플러그인·스킬 디렉토리 워크 비활성화, Auto-memory 완전 비활성화; API key 또는 `apiKeyHelper`(`--settings`) 필수
- `--channels` 권한 릴레이 — 채널 서버가 도구 승인 프롬프트를 폰으로 포워드 (v2.1.80 리서치 프리뷰 → v2.1.81 확장)
- MCP OAuth CIMD/SEP-991 지원 — Dynamic Client Registration 없는 서버에 Client ID Metadata Document 지원
- MCP read/search 도구 호출 "Queried {server}" 단일 라인 축소 (Ctrl+O 확장)
- `rate_limits` statusline 필드 — Claude.ai 5시간/7일 rate limit 사용량(`used_percentage`, `resets_at`) 표시 (v2.1.80)
- `source: 'settings'` 플러그인 마켓플레이스 소스 — settings.json에 플러그인 항목 인라인 선언 (v2.1.80)
- Skills·슬래시 명령 `effort` frontmatter — 호출 시 모델 effort 레벨 오버라이드 (v2.1.80)
- ref-tracked 플러그인 매 로드 시 재클론으로 upstream 최신화
- Remote Control 세션 타이틀 세 번째 메시지 이후 갱신

**Breaking Changes:**
- plan mode 컨텍스트 초기화 옵션 기본 숨김 (`"showClearContextOnPlanAccept": true`로 복원)
- Windows(WSL 포함) 줄 단위 응답 스트리밍 비활성화 (렌더링 문제)

**주요 버그 수정:**
- 동시 다중 세션 OAuth 토큰 갱신 시 재인증 반복 요청 수정
- voice mode WebSocket 무음 연결 종료 시 오디오 미복구 + retry 실패 묵살 수정
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 미적용으로 structured-outputs beta 헤더 전송 → Vertex/Bedrock 프록시 400 오류 수정
- Node.js 18 크래시 수정
- worktree 내 세션 재개 시 해당 worktree 자동 전환
- 백그라운드 에이전트 태스크 출력 무한 hang race condition 수정
- `--resume` 병렬 도구 결과 누락 수정 (v2.1.80)
- 시작 메모리 ~80 MB 절감 (250k 파일 레포, v2.1.80)

---

### v2.1.79 (2026-03-19 동기화)

**새로운 기능:**
- `--console` 플래그 — `claude auth login --console` Anthropic Console(API 결제) 인증
- `/config` 메뉴 "Show turn duration" 토글
- `CLAUDE_CODE_PLUGIN_SEED_DIR` 다중 시드 디렉토리 지원 (`:` Unix, `;` Windows)
- `StopFailure` Hook 이벤트 — rate limit·인증 실패 등 API 오류로 턴 종료 시 발동 (v2.1.78)
- `${CLAUDE_PLUGIN_DATA}` 변수 — 플러그인 영속 상태 저장소, 업데이트 후에도 유지 (v2.1.78)
- 플러그인 배포 에이전트 frontmatter에 `effort`, `maxTurns`, `disallowedTools` 지원 (v2.1.78)
- tmux `set -g allow-passthrough on` 시 터미널 알림이 외부 터미널에 도달 (v2.1.78)
- [VSCode] `/remote-control` — claude.ai/code에서 세션 이어받기
- [VSCode] 첫 메시지 기반 세션 탭 AI 제목 자동 생성

**주요 버그 수정:**
- `claude -p` subprocess hang 수정 (Python `subprocess.run` 등), Ctrl+C `-p` 모드 수정
- `SessionEnd` 훅이 대화형 `/resume` 시 미발동 수정
- 비스트리밍 API 폴백 2분 per-attempt 타임아웃 (무한 hang 방지)
- **Security (v2.1.78)**: `sandbox.enabled: true`이지만 의존성 없을 때 묵시적 비활성화 → 시작 경고로 수정
- `.git`, `.claude` 보호 디렉토리 `bypassPermissions`에서 프롬프트 없이 쓰기 가능하던 버그 수정 (v2.1.78)
- `deny: ["mcp__servername"]` 규칙이 모델에 차단 도구를 노출하던 버그 수정 (v2.1.78)
- 시작 메모리 사용량 ~18MB 개선

---

### v2.1.77 (2026-03-17 동기화)

**새로운 기능:**
- 토큰 한도 확대: Opus 4.6 기본 출력 64k, Opus 4.6/Sonnet 4.6 상한 128k
- `allowRead` sandbox filesystem 설정 — `denyRead` 영역 내 읽기 재허용
- `/copy N` — N번째 최근 응답 복사
- MCP Elicitation 지원 — MCP 서버가 세션 중 구조화된 입력 요청 (v2.1.76)
- 신규 Hook 이벤트: `PostCompact` (압축 완료 후), `Elicitation`, `ElicitationResult` (v2.1.76)
- `/effort` 슬래시 명령 — 모델 effort 레벨 설정 (v2.1.76)
- `-n`/`--name` CLI 플래그 — 세션 시작 시 표시 이름 지정 (v2.1.76)
- `worktree.sparsePaths` — `--worktree` 필요 디렉토리만 checkout (v2.1.76)
- 메모리 파일 최종 수정 타임스탬프 자동 기록 — Claude가 신선도 판단 가능 (v2.1.75)
- `/color` 명령 — 세션 프롬프트 바 색상 설정 (v2.1.75)
- Opus 4.6 1M context 기본 지원 (Max/Team/Enterprise, v2.1.75)
- `/branch` 명령 (기존 `/fork` 리네이밍, `/fork` alias 유지)
- `SendMessage` — 중단된 에이전트 자동 백그라운드 재개

**주요 버그 수정:**
- PreToolUse hook `"allow"` 반환 시 `deny` 규칙 및 enterprise managed settings 우회 보안 수정
- Write tool CRLF 파일 덮어쓰기 시 줄 끝 무음 변환 수정
- `--resume` 대화 히스토리 무음 truncation (메모리 추출 race condition) 수정
- 장시간 세션 메모리 누수 (progress message compaction 후 생존) 수정
- 컨텍스트 압축 후 deferred tool 스키마 손실 수정 (v2.1.76)
- 슬래시 명령 "Unknown skill" 수정 (v2.1.76)
- 토큰 추정 과잉 계산 (thinking/tool_use 블록) 수정 (v2.1.75)

**Breaking Changes:**
- Agent tool `resume` 파라미터 제거 → `SendMessage({to: agentId})` 사용
- Windows managed settings 레거시 경로 제거 (`C:\ProgramData\...` → `C:\Program Files\...`) (v2.1.75)

---

### v2.1.74 (2026-03-13 동기화)

**새로운 기능:**
- `/context` 명령 개선 — 컨텍스트 과다 도구·메모리 팽창·용량 경고에 실행 가능한 최적화 제안
- `autoMemoryDirectory` 설정 — Auto Memory 저장 디렉토리 커스텀 경로 지정
- `modelOverrides` 설정 (v2.1.73) — 모델 픽커 항목을 커스텀 provider 모델 ID로 매핑 (Bedrock ARN 등)
- `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` — SessionEnd 훅 타임아웃 가변 설정 (기존 1.5초 고정)
- Agent frontmatter `model:` 및 `--agents` JSON에서 전체 모델 ID 수용 (`--model`과 동일한 값)
- `--plugin-dir` 변경 — 로컬 개발 사본이 동명 마켓플레이스 플러그인 오버라이드

**주요 버그 수정:**
- 스트리밍 API 응답 버퍼 미해제 메모리 누수 (Node.js/npm RSS 무한 증가)
- Managed policy `ask` 규칙이 user `allow` 또는 skill `allowed-tools`에 우회되던 버그
- MCP OAuth: 콜백 포트 충돌 hang, HTTP 200 오류 시 리프레시 토큰 만료 후 재인증 미프롬프트
- macOS 네이티브 바이너리 voice mode 마이크 권한 silent fail (`audio-input` 엔타이틀먼트)
- 복잡한 bash 권한 프롬프트에서 100% CPU 루프·freeze (v2.1.73)
- `.claude/skills/` 대량 변경 시 데드락 freeze (v2.1.73)
- 다중 세션 동시 실행 시 Bash 출력 유실 (v2.1.73)
- `model: opus`/`sonnet`/`haiku` 서브에이전트 Bedrock/Vertex/Foundry 다운그레이드 (v2.1.73)
- `SessionStart` 훅 `--resume`/`--continue` 시 두 번 실행 (v2.1.73)
- Windows RTL 텍스트 렌더링, LSP 서버 malformed URI

**Deprecated:**
- `/output-style` 명령 → `/config` 사용 (출력 스타일 세션 시작 시 고정)

---

### v2.1.72 (2026-03-10 동기화)

**새로운 기능:**
- `ExitWorktree` 도구 — `EnterWorktree` 세션 종료
- `model` 파라미터 Agent 도구에 복원 (per-invocation 모델 오버라이드)
- `/plan <description>` — 플랜 모드 즉시 진입 + 실행
- `/copy` `w` 키 — 파일로 직접 쓰기 (SSH 환경)
- `CLAUDE_CODE_DISABLE_CRON` 환경변수 — 크론 작업 즉시 중지
- Bash 자동 허용 추가: `lsof`, `pgrep`, `tput`, `ss`, `fd`, `fdfind`
- Effort 간소화: low/medium/high (max 제거), 심볼 ○ ◐ ●, `/effort auto`
- CLAUDE.md HTML 주석(`<!-- -->`) 자동 주입 시 Claude에게 숨김 (Read 도구로는 표시)
- 팀 에이전트 리더 모델 자동 상속
- VSCode `vscode://anthropic.claude-code/open` URI 핸들러
- 마켓플레이스 `.git` 없는 git URL 지원 (Azure DevOps, AWS CodeCommit)
- SDK `query()` 프롬프트 캐시 수정 — 입력 토큰 최대 12x 절감
- Bash 파싱 native 모듈 전환 — 빠른 초기화, 메모리 누수 제거, 번들 ~510KB 감소

**주요 버그 수정:**
- 워크트리: Task 재개 시 cwd 미복원, 백그라운드 태스크 알림 worktreePath/worktreeBranch 누락
- 훅: `transcript_path` 잘못된 디렉토리, agent `prompt` 매 settings 쓰기마다 삭제, async 훅 stdin 미수신, validation 예시 오류
- 플러그인: Windows OneDrive EEXIST 오류, project-scope user-scope 설치 차단, `CLAUDE_CODE_PLUGIN_CACHE_DIR` 리터럴 `~`
- `/clear` 백그라운드 에이전트 종료 방지 (포그라운드만)
- 샌드박스 권한 오류, 병렬 도구 실패 시 형제 취소 → Bash만 연쇄
- VSCode: Shift+Enter 신규 줄 대신 제출, 통합 터미널 스크롤 속도

---

### v2.1.71 (2026-03-07 동기화)

**새로운 기능:**
- `/loop <interval> <prompt>` 명령 — 반복 인터벌 실행 (v2.1.71)
- `InstructionsLoaded` Hook 이벤트 — CLAUDE.md / `.claude/rules/*.md` 로드 시 트리거 (v2.1.69)
- Hook 이벤트 신규 필드: `agent_id` (서브에이전트), `agent_type`, `worktree` (v2.1.69)
- `TeammateIdle`, `TaskCompleted` Hook에서 `{"continue": false}` 지원 (v2.1.71)
- `${CLAUDE_SKILL_DIR}` Skill 변수 (v2.1.69)
- `/reload-plugins` 명령 (v2.1.69)
- MCP `oauth.authServerMetadataUrl` 설정 옵션 (v2.1.69)
- Plugin source type `git-subdir` (v2.1.69)
- Plugin MCP 서버 중복 제거 (v2.1.71)
- `includeGitInstructions` 설정 + `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` (v2.1.69)
- Bash 자동 허용: `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, `pr` (v2.1.71)
- Opus 4.6 기본 medium effort (Max/Team), "ultrathink" 키워드 high effort 재도입 (v2.1.68)
- `/claude-api` 내장 스킬 (v2.1.69)

**주요 버그 수정:**
- 중첩 Skill 발견 시 gitignore 디렉토리(`node_modules` 등) 로드 보안 수정 (v2.1.69)
- `.mcp.json` 서버 최초 실행 시 자동 전체 활성화 버그 수정 (v2.1.69)
- `/fork` 대화가 같은 plan 파일 공유하는 버그 수정 (v2.1.71)
- `WorktreeCreate`, `WorktreeRemove` 플러그인 Hook 무시 버그 수정 (v2.1.71)
- `--print` 모드에서 팀 에이전트 설정 시 무한 대기 수정 (v2.1.71)

**Breaking Changes:**
- Opus 4, Opus 4.1 Claude Code 1st-party API에서 제거 (v2.1.68)
- `/plugin uninstall`이 `.claude/settings.local.json` 수정으로 변경 (v2.1.71)

---

### v2.1.66 (2026-03-04 동기화)

**주요 버그 수정:**
- 불필요한 오류 로그 감소 (spurious error logging 제거)

---

### v2.1.63 (2026-03-01 동기화)

**새로운 기능:**
- HTTP Hooks: `type: "http"` — shell 없이 URL로 JSON POST/수신 (v2.1.63)
- `/simplify`, `/batch` 번들 슬래시 명령 추가 (v2.1.63)
- `/copy` 명령 (코드 블록 선택 또는 전체 응답 복사) (v2.1.59)
- Auto Memory 자동 저장 + `/memory` 명령으로 관리 (v2.1.59)
- Project config & Auto memory를 같은 레포의 git worktree 간 공유 (v2.1.63)
- `/copy` "Always copy full response" 옵션 (v2.1.63)
- VSCode: 세션 이름 변경/삭제 액션 (v2.1.63)

**환경변수 추가:**
- `ENABLE_CLAUDEAI_MCP_SERVERS=false` — claude.ai MCP 서버 비활성화 (v2.1.63)

**주요 버그 수정:**
- 메모리 누수 다수 수정: git root cache, JSON parsing cache, MCP server fetch cache, bash prefix cache 등 (v2.1.63)
- `/clear` 후 캐시된 skill 초기화 수정 (v2.1.63)
- Windows 설정 파일 동시 쓰기 손상 수정 (v2.1.61)
- REPL bridge 메시지 순서 경쟁 조건 수정 (v2.1.63)

### v2.1.53 (2026-02-25 동기화)

**새로운 기능:**
- `claude remote-control` 원격 제어 서브커맨드 (v2.1.51)
- 커스텀 npm 레지스트리 + 버전 핀 Plugin 설치 (v2.1.51)
- macOS plist / Windows Registry managed settings (v2.1.51)
- `WorktreeCreate`, `WorktreeRemove` Hook 이벤트 (v2.1.50)
- `claude agents` CLI 명령 (v2.1.50)
- `isolation: worktree` Agent 정의 필드 (v2.1.50)
- Opus 4.6 fast mode 1M context (v2.1.50)
- `--worktree (-w)` 격리 세션 플래그 (v2.1.49)
- `background: true` Agent 정의 필드 (v2.1.49)
- Plugin `settings.json` 동봉 (v2.1.49)
- Ctrl+F 백그라운드 에이전트 종료 (v2.1.49)
- claude.ai MCP connectors 지원 (v2.1.46)
- Claude Sonnet 4.6 모델 지원 (v2.1.45)
- `claude auth login/status/logout` CLI (v2.1.41)
- Windows ARM64 지원 (v2.1.41)

**환경변수 추가:**
- `CLAUDE_CODE_ACCOUNT_UUID`, `CLAUDE_CODE_USER_EMAIL`, `CLAUDE_CODE_ORGANIZATION_UUID`
- `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`, `CLAUDE_CODE_DISABLE_1M_CONTEXT`

**주요 버그 수정:**
- Agent Teams 메모리 누수 다수 수정 (v2.1.50)
- `CLAUDE_CODE_SIMPLE` 모드 강화 (v2.1.49-50)
- Windows 안정성 대폭 개선 (v2.1.47-53)

### v2.1.39 (2026-02-11 동기화)

**새로운 기능:**
- PDF 페이지 파라미터 지원
- `/debug` 명령어
- PR 리뷰 상태 표시기
- 68% 메모리 감소 (`--resume`)
- Task 의존성 관리 시스템
- 커스텀 키보드 단축키

**Skills 변경:**
- `disable-model-invocation` 필드 추가
- Skill scopes 계층 (Enterprise > Personal > Project > Plugin)

**Hooks 변경:**
- Setup 이벤트 상세 스키마
- Hook output의 `decision` 필드

### v2.1.30 (이전)

- SubagentStart, PostToolUseFailure 이벤트
- prompt, agent Hook 타입
- async Hook 지원

---

## v2.9.0 변경 사항 (2026-02-11)

### Breaking Changes

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

### 신규 기능

- **Agent Teams**: TeamCreate, SendMessage, TeamDelete
- **Task Management**: TaskCreate, TaskUpdate, TaskList, TaskGet
- **Memory & Modular Rules**: Auto Memory, `.claude/rules/*.md`
- **Hook 이벤트 추가**: TeammateIdle, Setup (init/init-only/maintenance)
- **Hook 타입 추가**: prompt, agent, async
- **Agent Frontmatter**: disallowedTools, permissionMode, skills

---

## 긴급 업데이트 절차

Breaking Change 감지 시:

1. **즉시 Issue 생성**
   ```bash
   gh issue create --title "[URGENT] Claude Code Breaking Change" \
     --body "Breaking change detected in vX.X.X" \
     --label "urgent,breaking-change"
   ```

2. **SKILL.md 경고 추가**
   ```markdown
   > ⚠️ **주의**: v2.X.X에서 XXX가 deprecated되었습니다.
   ```

3. **마이그레이션 가이드 작성**
   - `references/migration-vX.md` 생성

---

## 자동화 스크립트

### 로컬 버전 체크

```bash
# scripts/check-updates.sh 실행
scripts/check-updates.sh
```

### 수동 동기화

```bash
# 공식 CHANGELOG 다운로드
curl -s https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md \
  -o references/official-docs/CHANGELOG.md

# 버전 비교
LATEST=$(grep -m1 "^## [0-9]" references/official-docs/CHANGELOG.md | sed 's/## //')
CURRENT=$(grep "Claude Code Version" SKILL.md | grep -oE "v[0-9]+\.[0-9]+\.[0-9]+")
echo "Latest: $LATEST, Current: $CURRENT"
```

---

## 관련 파일

| 파일 | 용도 |
|------|------|
| `SKILL.md` | 메인 스킬 파일 |
| `CHANGELOG.md` | 스킬 변경 이력 |
| `scripts/check-updates.sh` | 로컬 버전 체크 |
| `.github/workflows/sync-claude-code-docs.yml` | 자동 동기화 |
| `references/official-docs/` | 공식 문서 백업 |

---

*이 가이드는 스킬 유지보수의 핵심 문서입니다.*
