# Changelog - Claude Code Extension Builder

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.22.0] - 2026-03-27

### Added
- **Claude Code v2.1.85 sync**
  - Hook `if` 필드 — permission rule syntax (`Bash(git *)`)로 훅 조건부 실행 필터링 (프로세스 스폰 오버헤드 감소)
  - `PreToolUse` hook `updatedInput` + `permissionDecision: "allow"` 반환으로 `AskUserQuestion` 충족 — 헤드리스 통합(custom UI)에서 대화형 질문 처리 지원
  - `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL` env vars — MCP `headersHelper` 스크립트에서 서버 정보 접근, 하나의 헬퍼로 다중 서버 처리
  - MCP OAuth RFC 9728 Protected Resource Metadata discovery — 인증 서버 자동 탐색
  - 조직 정책(`managed-settings.json`) 차단 플러그인 설치·활성화 불가 및 마켓플레이스 숨김
  - Deep link `claude-cli://open?q=…` 최대 5,000자 지원 (긴 사전 입력 프롬프트 시 "scroll to review" 경고)
  - 트랜스크립트에 `/loop`, `CronCreate` 스케줄 작업 실행 시 타임스탬프 마커 추가

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.84 → v2.1.85 업데이트
  - MCP 테이블: `CLAUDE_CODE_MCP_SERVER_NAME/URL` 행 추가, `MCP OAuth`에 RFC 9728 반영
  - Hook 노트: `if` 필드 조건부 실행, `PreToolUse` `AskUserQuestion` 충족 기능 추가
  - CLI/env: Deep link 5,000자, 트랜스크립트 타임스탬프 마커, `CLAUDE_CODE_MCP_SERVER_NAME/URL` 추가
  - Plugin: 조직 정책 차단 플러그인 마켓플레이스 숨김 반영
- `references/version-sync.md`: v2.1.85 변경사항 추적 추가

### Fixed (Claude Code v2.1.85)
- `/compact` "context exceeded" 오류 수정 (대화가 compact 요청 자체보다 클 때)
- `deniedMcpServers` 설정이 claude.ai MCP 서버를 차단하지 못하던 버그 수정
- MCP step-up 재인증 — 리프레시 토큰 존재 시 `403 insufficient_scope` 재인증 흐름 미트리거 수정
- Python Agent SDK `--mcp-config`의 `type:'sdk'` MCP 서버가 시작 시 누락되던 버그 수정
- Remote Control 세션 권한 해결 후 "Requires Action" 상태 고착 수정
- Ghostty·Kitty·WezTerm 등 Kitty 키보드 프로토콜 지원 터미널에서 종료 후 Ctrl+C·Ctrl+D 미작동 수정
- 원격 세션 스트리밍 중단 시 메모리 누수 수정
- 대형 트랜스크립트 스크롤 성능 개선 (WASM yoga-layout → pure TypeScript)

---

## [2.21.0] - 2026-03-26

### Added
- **Claude Code v2.1.84 sync**
  - PowerShell 도구 — Windows 옵트인 프리뷰 (`tools-reference#powershell-tool`)
  - `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL_SUPPORTS` env vars — Bedrock/Vertex/Foundry 고정 모델의 effort/thinking capability 오버라이드
  - `CLAUDE_STREAM_IDLE_TIMEOUT_MS` env var — 스트리밍 유휴 워치독 타임아웃 설정 (기본 90초)
  - `TaskCreated` Hook 이벤트 — `TaskCreate` 호출로 태스크 생성 시 발동
  - `WorktreeCreate` Hook `type: "http"` 지원 — `hookSpecificOutput.worktreePath`로 생성된 worktree 경로 반환
  - `allowedChannelPlugins` 관리형 설정 — 팀/Enterprise 관리자용 채널 플러그인 허용 목록 정의
  - Rules/Skills `paths:` frontmatter YAML 리스트 glob 지원
  - MCP 도구 설명·서버 지시문 2KB 상한 — OpenAPI 서버의 컨텍스트 팽창 방지
  - 로컬과 claude.ai 커넥터 중복 MCP 서버 제거 — 로컬 설정 우선
  - 75분+ 유휴 복귀 시 `/clear` 넛지 프롬프트 (오래된 세션 토큰 재캐싱 방지)
  - `x-client-request-id` 헤더 — API 요청 타임아웃 디버깅용
  - [VSCode] rate limit 경고 배너 (사용량 % + 리셋 시간)
  - issue/PR 참조 링크: `owner/repo#123` 형식만 클릭 가능 (bare `#123` 비활성화)
- **Claude Code v2.1.83 sync**
  - `managed-settings.d/` 드롭인 디렉토리 — 팀별 독립 정책 파편 알파벳순 병합
  - `CwdChanged`, `FileChanged` Hook 이벤트 — 반응형 환경 관리 (direnv 등)
  - `sandbox.failIfUnavailable` 설정 — 샌드박스 미시작 시 에러로 종료 (묵시적 비활성화 방지)
  - `disableDeepLinkRegistration` 설정 — `claude-cli://` 프로토콜 핸들러 등록 방지
  - `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` — Bash 도구·훅·MCP stdio 서버 서브프로세스에서 자격증명 제거
  - 트랜스크립트 검색 — `Ctrl+O` 모드에서 `/` 입력, `n`/`N`으로 매치 이동
  - `Ctrl+X Ctrl+E` 외부 에디터 alias (readline 네이티브 바인딩; `Ctrl+G` 유지)
  - Agent frontmatter `initialPrompt` — 에이전트 첫 턴 자동 제출
  - `Ctrl+L` 화면 강제 전체 재드로우 — `Cmd+K` 후 UI 부분 공백 복구용
  - MEMORY.md 25KB 트런케이션 추가 (기존 200줄 제한에 추가)
  - `TaskOutput` 도구 deprecated → 백그라운드 태스크 출력 파일 경로에 `Read` 사용

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.81 → v2.1.84 업데이트
  - MCP 테이블: `MCP 컨텍스트 제한` 행 추가, `Managed MCP`에 `allowedChannelPlugins`, `claude.ai MCP connectors`에 로컬 우선 중복 제거 반영
  - Memory 테이블: `Managed Policy`에 `managed-settings.d/` 드롭인, `MEMORY.md` 25KB 한도, `Modular Rules` YAML paths 리스트 추가
  - Hook 이벤트: 노트 라인에 `CwdChanged`, `FileChanged` (v2.1.83), `TaskCreated` (v2.1.84) 추가; `WorktreeCreate` HTTP type 지원 주석 추가; 주요 이벤트 카운트 21→24개 업데이트
  - Agent/CLI: `initialPrompt`, `CLAUDE_STREAM_IDLE_TIMEOUT_MS`, `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`, PowerShell 도구 추가
  - Deprecated: `TaskOutput` → `Read` 항목 추가; `Sonnet 4.5` 항목 제거 (stale)
- `references/version-sync.md`: v2.1.83, v2.1.84 변경사항 추적 추가

---

## [2.20.0] - 2026-03-23

### Added
- **Claude Code v2.1.81 sync**
  - `--bare` 플래그 — 스크립트형 `-p` 호출용 경량 모드: 훅·LSP·플러그인 동기화·스킬 디렉토리 워크 비활성화, Auto-memory 완전 비활성화; `ANTHROPIC_API_KEY` 또는 `--settings`의 `apiKeyHelper` 필수 (OAuth·키체인 인증 불가)
  - `--channels` 권한 릴레이 — 권한 capability를 선언한 채널 서버가 도구 승인 프롬프트를 폰으로 포워드
  - plan mode 컨텍스트 초기화 옵션 기본 숨김 (`"showClearContextOnPlanAccept": true`로 복원 가능)
  - MCP OAuth CIMD/SEP-991 지원 — Dynamic Client Registration 없는 서버에 대한 Client ID Metadata Document 지원
  - MCP read/search 도구 호출 "Queried {server}" 단일 라인으로 축소 (Ctrl+O로 확장)
  - ref-tracked 플러그인 매 로드 시 재클론으로 최신 upstream 변경 사항 반영
  - Remote Control 세션 타이틀 세 번째 메시지 이후 갱신
- **Claude Code v2.1.80 sync**
  - `rate_limits` statusline 스크립트 필드 — Claude.ai rate limit 사용량 표시 (5시간·7일 윈도우, `used_percentage`·`resets_at`)
  - `source: 'settings'` 플러그인 마켓플레이스 소스 — settings.json에 플러그인 항목 인라인 선언
  - Skills·슬래시 명령 `effort` frontmatter — 호출 시 모델 effort 레벨 오버라이드
  - `--channels` (리서치 프리뷰) — MCP 서버가 세션에 메시지 푸시
  - 시작 시 메모리 사용량 대폭 절감 (~80 MB, 250k 파일 레포 기준)
  - 플러그인 install 팁 단순화 — `/plugin install` 단일 명령으로 통합
  - CLI 도구 사용 감지로 플러그인 팁 트리거 조건 확대 (파일 패턴 매칭 외)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.79 → v2.1.81 업데이트
  - MCP 테이블: `--channels` 추가, MCP OAuth CIMD/SEP-991 반영, MCP 도구 호출 축소 UX 추가
  - CLI 섹션: `--bare` 플래그, `rate_limits` statusline 필드 추가
  - Plugin 섹션: `source: 'settings'`, `effort` frontmatter, ref-tracked 플러그인 재클론 추가
  - Breaking Changes: plan mode 컨텍스트 초기화 숨김, Windows/WSL 스트리밍 비활성화 추가
- `references/version-sync.md`: v2.1.81 변경사항 추적 추가

### Fixed (Claude Code v2.1.81)
- 동시 다중 세션에서 OAuth 토큰 갱신 시 재인증 반복 요청 수정
- voice mode 재시도 실패 묵살 및 오해 "check your network" 메시지 → 실제 오류 표시로 수정
- voice mode 서버 WebSocket 무음 연결 종료 시 오디오 미복구 수정
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` 미적용으로 structured-outputs beta 헤더 전송 → Vertex/Bedrock 프록시 400 오류 수정
- `--channels` Team/Enterprise 조직에서 managed settings 미구성 시 bypass 수정
- Node.js 18 크래시 수정
- 문자열 내 대시 포함 Bash 명령에 불필요한 권한 프롬프트 수정
- 세션 중 플러그인 디렉토리 삭제 시 플러그인 훅이 프롬프트 제출 차단하는 버그 수정
- 백그라운드 에이전트 태스크 출력이 태스크 완료 직후 폴링 시 무한 hang하는 race condition 수정
- worktree 내 세션 재개 시 해당 worktree로 자동 전환
- `/btw` 활성 응답 중 사용 시 붙여넣기 텍스트 미포함 수정
- tmux에서 빠른 Cmd+Tab 후 붙여넣기가 클립보드 복사보다 앞서는 race condition 수정
- 자동 생성 세션 설명으로 터미널 탭 제목 미업데이트 수정
- 보이지 않는 훅 첨부가 transcript 모드 메시지 수 부풀리는 버그 수정
- Remote Control 세션 범용 제목 → 첫 프롬프트 기반 제목으로 수정
- `/rename` Remote Control 세션 타이틀 미동기화 수정
- Remote Control `/exit` 세션 아카이빙 불안정 수정
- [VSCode] Git Bash 사용 시 Windows PATH 상속 누락 수정 (v2.1.78 회귀)

### Fixed (Claude Code v2.1.80)
- `--resume` 병렬 도구 결과 누락 — 병렬 tool_use/tool_result 쌍 모두 복원
- voice mode WebSocket 실패 (Cloudflare bot detection TLS 지문 문제) 수정
- API 프록시·Bedrock·Vertex에서 fine-grained 도구 스트리밍 400 오류 수정
- `/remote-control` 게이트웨이·서드파티 프로바이더 배포에서도 표시되던 버그 수정
- `/sandbox` 탭 전환 Tab·방향키 미응답 수정
- 원격 설정(`remote-settings.json`) 캐시로 managed settings 미적용 수정

---

## [2.19.0] - 2026-03-19

### Added
- **Claude Code v2.1.79 sync**
  - `--console` 플래그 — `claude auth login --console` Anthropic Console(API 결제) 인증
  - `/config` 메뉴에 "Show turn duration" 토글 추가
  - `CLAUDE_CODE_PLUGIN_SEED_DIR` 다중 시드 디렉토리 지원 (`:` Unix, `;` Windows)
  - [VSCode] `/remote-control` — 브라우저/폰(claude.ai/code)에서 세션 이어받기
  - [VSCode] 첫 메시지 기반 세션 탭 AI 제목 자동 생성
- **Claude Code v2.1.78 sync**
  - `StopFailure` Hook 이벤트 — rate limit·인증 실패 등 API 오류로 턴 종료 시 발동
  - `${CLAUDE_PLUGIN_DATA}` 변수 — 플러그인 업데이트 후에도 유지되는 영속 상태 저장소
  - 플러그인 배포 에이전트 frontmatter에 `effort`, `maxTurns`, `disallowedTools` 지원
  - tmux `set -g allow-passthrough on` 시 터미널 알림(iTerm2/Kitty/Ghostty)이 외부 터미널에 도달
  - 응답 텍스트 생성 중 줄 단위 스트리밍

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.77 → v2.1.79 업데이트
  - 신규 Hook 이벤트: `StopFailure` 추가 (20→21개)
  - CLI 섹션: `--console` 플래그 반영
  - Plugin 섹션: `${CLAUDE_PLUGIN_DATA}`, `CLAUDE_CODE_PLUGIN_SEED_DIR` 추가
- `references/hooks-guide.md`: `StopFailure` 이벤트 추가 (21번째)
- `references/official/hooks.md`: `StopFailure` 이벤트 추가 (21번째)
- `references/official/subagents.md`: 플러그인 에이전트 frontmatter `effort` 필드 추가
- `references/version-sync.md`: v2.1.79 변경사항 추적 추가

### Fixed (Claude Code v2.1.79)
- `claude -p` 명시적 stdin 없이 subprocess로 실행 시 hang 수정 (Python `subprocess.run` 등)
- `-p` (print) 모드에서 Ctrl+C 동작 않는 버그 수정
- `/btw` 스트리밍 중 트리거 시 메인 에이전트 출력 반환 문제 수정
- `voiceEnabled: true` 설정 시 음성 모드 시작 활성화 오류 수정
- `SessionEnd` 훅이 대화형 `/resume`으로 세션 전환 시 미발동 수정
- 비스트리밍 API 폴백에 2분 per-attempt 타임아웃 추가 (무한 hang 방지)
- 시작 시 메모리 사용량 ~18MB 개선

### Fixed (Claude Code v2.1.78)
- **Security**: `sandbox.enabled: true`이지만 의존성 없을 때 샌드박스 묵시적 비활성화 → 시작 시 경고 표시로 수정
- `deny: ["mcp__servername"]` 권한 규칙이 모델에 차단 도구를 노출하던 버그 수정
- `sandbox.filesystem.allowWrite` 절대 경로 미작동 수정
- `.git`, `.claude` 등 보호 디렉토리가 `bypassPermissions` 모드에서 프롬프트 없이 쓰기 가능하던 버그 수정
- `cc log`, `--resume` 대형 세션(>5MB) 대화 히스토리 무음 truncation 수정

---

## [2.18.0] - 2026-03-17

### Added
- **Claude Code v2.1.77 sync**
  - 토큰 한도 확대: Opus 4.6 기본 출력 64k, Opus 4.6/Sonnet 4.6 상한 128k
  - `allowRead` sandbox filesystem 설정 — `denyRead` 영역 내 읽기 재허용
  - `/copy N` — N번째 최근 응답 복사 (인덱스 선택)
  - `SendMessage` — 중단된 에이전트 자동 백그라운드 재개 (에러 대신)
  - `/branch` 명령 (기존 `/fork` 리네이밍, `/fork` alias 유지)
  - Background bash 작업 출력 5GB 초과 시 자동 종료 (디스크 보호)
  - 플랜 수락 시 플랜 내용으로 세션 자동 이름 지정
  - `claude plugin validate` 개선 — skill/agent/command frontmatter + `hooks/hooks.json` 검증
  - `apiKeyHelper` 10초 이상 소요 시 경고 알림 (메인 루프 블로킹 방지)
- **Claude Code v2.1.76 sync**
  - MCP Elicitation 지원 — MCP 서버가 세션 중 구조화된 입력 요청 (폼 필드·URL)
  - `Elicitation`, `ElicitationResult` Hook 이벤트 — MCP 요청 인터셉트/오버라이드
  - `PostCompact` Hook 이벤트 — 컨텍스트 압축 완료 후 실행
  - `/effort` 슬래시 명령 — 모델 effort 레벨 세션 내 설정
  - `-n`/`--name <name>` CLI 플래그 — 세션 시작 시 표시 이름 설정
  - `worktree.sparsePaths` — `--worktree` 시 필요한 디렉토리만 sparse checkout
  - `feedbackSurveyRate` 설정 — 세션 품질 설문 샘플링 비율 (enterprise)
- **Claude Code v2.1.75 sync**
  - Opus 4.6 1M context window 기본 지원 (Max, Team, Enterprise plans)
  - 메모리 파일 최종 수정 타임스탬프 자동 기록 — Claude가 신선도 판단 가능
  - `/color` 명령 — 세션 프롬프트 바 색상 설정
  - Hook source 표시 (settings/plugin/skill) — 권한 프롬프트에서 출처 확인
  - 세션 이름 프롬프트 바 표시 (`/rename` 사용 시)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.74 → v2.1.77 업데이트
  - MCP 테이블: MCP Elicitation 항목 추가
  - Memory 테이블: 메모리 타임스탬프 항목 추가
  - 신규 Hook 이벤트: PostCompact, Elicitation, ElicitationResult 추가 (17→20개)
  - Agent/CLI: /branch, /effort, /copy N, allowRead, 토큰 한도, SendMessage 변경 반영
  - Breaking Changes: Agent tool resume 파라미터 제거, Windows managed settings 경로 추가
- `references/hooks-guide.md`: PostCompact, Elicitation, ElicitationResult 이벤트 추가
- `references/official/hooks.md`: 신규 Hook 이벤트 3개 추가 (17→20개)
- `references/mcp-guide.md`: MCP Elicitation 지원 추가
- `references/official/mcp.md`: MCP Elicitation 기능 추가
- `references/subagents-guide.md`: Agent tool resume 파라미터 제거 안내 추가
- `references/official/subagents.md`: Agent tool 변경 사항 업데이트
- `references/version-sync.md`: v2.1.77 변경사항 추적 추가

### Breaking Changes
- Agent tool `resume` 파라미터 제거 → `SendMessage({to: agentId})` 사용 (v2.1.77)
- Windows managed settings 레거시 경로 제거: `C:\ProgramData\ClaudeCode\managed-settings.json` → `C:\Program Files\ClaudeCode\managed-settings.json` (v2.1.75)

### Fixed (Claude Code v2.1.77)
- PreToolUse hook `"allow"` 반환 시 `deny` 권한 규칙 및 enterprise managed settings 우회 보안 버그 수정
- Write tool CRLF 파일/디렉토리 덮어쓰기 시 줄 끝 무음 변환 수정
- `--resume` 메모리 추출 쓰기와 주 트랜스크립트 간 race condition으로 인한 대화 히스토리 무음 truncation 수정
- 장시간 세션 메모리 누수 (progress message가 compaction 후 생존) 수정
- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` beta tool-schema 필드 미제거로 프록시 게이트웨이 요청 거부 수정
- Bash 도구: 시스템 temp 경로에 공백 포함 시 성공 명령에 오류 보고 수정
- API 비스트리밍 폴백 시 비용·토큰 미집계 수정
- Claude Desktop 세션이 terminal CLI API 키 사용 (OAuth 대신) 수정
- `git-subdir` 플러그인 동일 모노레포 서브디렉토리 간 플러그인 캐시 충돌 수정
- stale worktree 정리가 직전 재개된 에이전트 worktree 삭제 race condition 수정

### Fixed (Claude Code v2.1.76)
- 컨텍스트 압축 후 deferred tool 입력 스키마 손실로 array/number 파라미터 타입 오류 수정
- 슬래시 명령 "Unknown skill" 표시 수정
- 자동 압축 연속 실패 시 무한 재시도 (circuit breaker: 3회 후 중단)

### Fixed (Claude Code v2.1.75)
- 토큰 추정 과잉 계산 (thinking/tool_use 블록) — 조기 컨텍스트 압축 방지
- 음성 모드 신규 설치 시 `/voice` 두 번 토글 없이 정상 활성화

---

## [2.17.0] - 2026-03-14

### Added
- **Graph Schema v2** — Shared State + Node Autonomy + Multi-route Decision 지원
  - `state` (workspace + raw_vault): 노드 간 context 단절 해결, 누적 문서 + 원본 보존
  - `reads/writes`: 노드→공유 상태 접근 선언
  - `artifacts`: 원본 데이터 파일 보존 (lossy compression 방지)
  - `autonomy`: subagent 자율 탐색 허용 (Skill 수준의 유연성)
  - `route_criteria`: multi-route decision (이진→다중 분기)
- **Ralph-Graph Loop** — Graph를 Ralph Loop로 반복 실행하여 SCAR 목표 달성까지 자율 개선
  - `ralph` 필드: `{enabled, target, max_iterations, evolve, feedback_file}`
  - Fresh Context 매 반복 + `evolve: true`로 graph.json 자체 개선 가능
  - 실행 프로토콜, 피드백 파일 구조, SCAR 현실 가이드 포함
- **Research Team v3 템플릿** (`references/graph-templates/research-team-v3.json`)
  - 4개 병렬 검색 전략 + adversarial verification + triangulation
  - Multi-route quality gate (complete/has_gaps/low_quality)
- **Claude Code v2.1.74 동기화**
  - `/context` 명령 개선 — 컨텍스트 과다 도구, 메모리 팽창, 용량 경고에 대한 실행 가능한 최적화 제안
  - `autoMemoryDirectory` 설정 — Auto Memory 저장 디렉토리 커스텀 경로 지정
  - `modelOverrides` 설정 (v2.1.73) — 모델 픽커 항목을 커스텀 provider 모델 ID로 매핑 (Bedrock inference profile ARN 등)
  - `--plugin-dir` 동작 변경 — 로컬 개발 사본이 마켓플레이스 동명 플러그인 오버라이드 (managed settings 강제 활성화 제외)
  - `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 환경변수 — `SessionEnd` 훅 타임아웃 설정 (기존 1.5초 고정 → 가변, v2.1.74)
  - Agent frontmatter `model:` 필드에서 전체 모델 ID (`claude-opus-4-5` 등) 수용 — `--model` 과 동일한 값 허용 (v2.1.74)
  - SSL 인증서 오류 시 (기업 프록시, `NODE_EXTRA_CA_CERTS`) 실행 가능한 안내 메시지 (v2.1.73)

### Changed
- `graph-schema.json`: v1→v2 업그레이드 (state, reads/writes, artifacts, autonomy, ralph 추가)
- `graph-workflow-guide.md`: v2.0.0 전면 개정 (Shared State 원칙, v2 노드 필드, Ralph-Graph Loop Phase 2.5)
- SKILL.md graph 섹션: v2 스키마 + Ralph Loop 반영 (500줄 유지)
- `SKILL.md`: 핵심 변경 사항 섹션 v2.1.72 → v2.1.74 업데이트
- `references/version-sync.md`: v2.1.74 변경사항 추적 추가

### Fixed (Claude Code v2.1.74)
- 스트리밍 API 응답 버퍼 미해제로 인한 메모리 누수 (Node.js/npm 경로 RSS 무한 증가) 수정
- Managed policy `ask` 규칙이 user `allow` 규칙 또는 skill `allowed-tools`에 의해 우회되던 버그 수정
- MCP OAuth 콜백 포트 충돌 시 hang 수정
- MCP OAuth 리프레시 토큰 만료 후 HTTP 200 오류 응답 시 재인증 미프롬프트 수정
- macOS 네이티브 바이너리 voice mode 마이크 권한 silent fail 수정 (`audio-input` 엔타이틀먼트 추가)
- `SessionEnd` 훅이 `hook.timeout` 무시하고 1.5초 후 강제 종료되던 버그 수정
- `/plugin install` REPL 내부 실행 실패 수정
- 마켓플레이스 업데이트 시 git 서브모듈 미동기화 수정
- Windows Terminal / conhost / VS Code에서 히브리어·아랍어 등 RTL 텍스트 렌더링 수정
- Windows LSP 서버 malformed file URI 수정

### Fixed (Claude Code v2.1.73)
- 복잡한 bash 명령 권한 프롬프트에서 100% CPU 루프 및 freeze 수정
- `.claude/skills/` 디렉토리 대량 변경 시 (e.g. `git pull`) 데드락 freeze 수정
- 같은 프로젝트 디렉토리에서 다중 세션 실행 시 Bash 도구 출력 유실 수정
- `model: opus`/`sonnet`/`haiku` 서브에이전트가 Bedrock/Vertex/Foundry에서 구형 버전으로 다운그레이드되던 버그 수정
- 서브에이전트 종료 시 백그라운드 bash 프로세스 미정리 수정
- `SessionStart` 훅이 `--resume`/`--continue` 재개 시 두 번 실행되던 버그 수정

### Deprecated
- `/output-style` 명령 → `/config` 사용 권장 (출력 스타일 세션 시작 시 고정으로 변경, v2.1.74)

---

## [2.16.0] - 2026-03-12

### Added
- **Graph Workflow System** — 자연어 → 구조화된 실행 계획(Graph) 변환 시스템
  - `references/graph-workflow-guide.md` — 메인 가이드 (스키마, NL→Graph 변환 패턴, 실행 프로토콜, 로깅, 개선 루프)
  - `references/graph-schema.json` — JSON Schema draft-07 Graph 정의 검증 (12개 테스트 통과)
  - `references/graph-templates/` — 3개 템플릿 (eval-pipeline, team-implementation, autonomous-loop)
- SKILL.md에 `graph <name>` 인자 처리 규칙 추가
- 키워드 자동 활성화: graph, workflow, 그래프, DAG, 파이프라인
- 시나리오 결정 가이드에 "복잡한 멀티스텝 워크플로우" 분기 추가
- 확장 기능 유형에 Graph Workflow 추가 (총 8개)

### Changed
- SKILL.md description에 graph workflow 키워드 추가
- `argument-hint`에 `graph` 옵션 추가
- Breaking Changes / Deprecated 섹션 압축 (500줄 제한 준수)

---

## [2.15.0] - 2026-03-10

### Added
- **Claude Code v2.1.72 동기화**
  - `ExitWorktree` 도구 — `EnterWorktree` 세션을 종료하는 새 도구
  - `model` 파라미터 Agent 도구에 복원 — per-invocation 모델 오버라이드
  - `/plan <description>` 인자 지원 — 플랜 모드 진입과 동시에 즉시 실행 (e.g. `/plan fix the auth bug`)
  - `/copy` 에서 `w` 키 — 파일로 직접 쓰기 (SSH 환경에서 클립보드 우회)
  - `CLAUDE_CODE_DISABLE_CRON` 환경변수 — 세션 중 예약된 cron 작업 즉시 중지
  - Bash 자동 허용 목록 추가: `lsof`, `pgrep`, `tput`, `ss`, `fd`, `fdfind`
  - Effort 레벨 간소화 — low/medium/high (max 제거), 새 심볼 ○ ◐ ●, `/effort auto` 로 초기화
  - CLAUDE.md HTML 주석(`<!-- -->`) 자동 주입 시 Claude에게 숨김 처리 (Read 도구로는 표시)
  - 팀 에이전트가 리더 모델 자동 상속
  - VSCode `vscode://anthropic.claude-code/open` URI 핸들러 — 새 탭 프로그래밍 방식 열기
  - 마켓플레이스 `.git` 접미사 없는 git URL 지원 (Azure DevOps, AWS CodeCommit)
  - SDK `query()` 프롬프트 캐시 수정 — 입력 토큰 비용 최대 12x 절감
  - Bash 명령 파싱 native 모듈 전환 — 초기화 속도 향상, 메모리 누수 제거, 번들 크기 ~510KB 감소

### Changed
- `SKILL.md`: 핵심 변경 사항 섹션 v2.1.71 → v2.1.72 업데이트
  - Agent/CLI 섹션에 `ExitWorktree`, `model` param, `/plan <description>`, `CLAUDE_CODE_DISABLE_CRON`, Bash 허용 추가 반영
  - Memory 계층 테이블에 CLAUDE.md HTML 주석 항목 추가
  - Breaking Changes에 Effort 레벨 max 제거 항목 추가
  - Agent Teams 설명에 리더 모델 상속 추가
- `references/version-sync.md`: v2.1.72 변경사항 추적 추가
- 버전: 2.14.0 → 2.15.0

### Fixed (Claude Code v2.1.72)
- 워크트리 격리 이슈: Task 도구 재개 시 cwd 미복원, 백그라운드 태스크 알림에 `worktreePath`/`worktreeBranch` 누락
- 훅 이슈: `transcript_path` 잘못된 디렉토리, agent `prompt` settings.json 매 쓰기마다 삭제, async 훅 bash `read -r` stdin 미수신
- 플러그인 이슈: Windows EEXIST 오류, project-scope가 user-scope 설치 차단, `CLAUDE_CODE_PLUGIN_CACHE_DIR` 리터럴 `~` 디렉토리 생성
- `/clear` 시 백그라운드 에이전트/태스크 종료 방지 (포그라운드 태스크만 정리)
- 샌드박스 권한 이슈: 파일 쓰기 오류 허용, `/tmp/claude/` 리디렉션 불필요 프롬프트
- 병렬 도구 호출에서 실패한 Read/WebFetch/Glob이 형제 취소 — Bash 오류만 연쇄

---

## [2.14.0] - 2026-03-07

### Added
- **Claude Code v2.1.71 동기화** (v2.1.67–v2.1.71 반영)
  - `/loop <interval> <prompt>` 명령 — 반복 인터벌 실행 (e.g. `/loop 5m check the deploy`) (v2.1.71)
  - 세션 내 반복 프롬프트용 cron 스케줄링 도구 (v2.1.71)
  - `InstructionsLoaded` Hook 이벤트 — CLAUDE.md / `.claude/rules/*.md` 로드 시 트리거 (v2.1.69)
  - Hook 이벤트에 `agent_id`, `agent_type`, `worktree` 필드 추가 (v2.1.69)
  - `TeammateIdle`, `TaskCompleted` Hook: `{"continue": false, "stopReason": "..."}` 지원 (v2.1.71)
  - `${CLAUDE_SKILL_DIR}` Skill 변수 — Skill이 자신의 디렉토리 참조 (v2.1.69)
  - `/reload-plugins` 명령 — 재시작 없이 플러그인 변경 사항 활성화 (v2.1.69)
  - MCP OAuth `oauth.authServerMetadataUrl` 설정 옵션 (v2.1.69)
  - Plugin source type `git-subdir` — git 레포 서브디렉토리 지원 (v2.1.69)
  - Plugin MCP 서버 중복 제거 — 동일 command/URL 서버 자동 스킵 (v2.1.71)
  - `includeGitInstructions` 설정 + `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 환경변수 (v2.1.69)
  - `sandbox.enableWeakerNetworkIsolation` 설정 (macOS, MITM 프록시 환경) (v2.1.69)
  - Voice STT 10개 언어 추가 (총 20개: Russian, Polish, Turkish, Dutch, Ukrainian 등) (v2.1.69)
  - `voice:pushToTalk` 키바인딩 재설정 가능 (기본: space, v2.1.71)
  - Bash 자동 허용 목록에 `fmt`, `comm`, `cmp`, `numfmt`, `expr`, `test`, `printf`, `getconf`, `seq`, `tsort`, `pr` 추가 (v2.1.71)
  - Opus 4.6 Max/Team 기본 노력 수준: medium effort (v2.1.68)
  - "ultrathink" 키워드로 high effort 활성화 (v2.1.68)
  - `/claude-api` 내장 스킬 추가 (v2.1.69)

### Changed
- `SKILL.md`: 핵심 변경 사항 섹션 v2.1.66 → v2.1.71 업데이트
  - 신규 Hook 이벤트 `InstructionsLoaded` 추가 (총 17개)
  - Hook 이벤트 신규 필드 (`agent_id`, `agent_type`, `worktree`) 명시
  - MCP 테이블에 `oauth.authServerMetadataUrl`, 플러그인 MCP 중복 제거 추가
  - 신규 슬래시 명령 (`/loop`, `/reload-plugins`) 추가
  - Skill 변수 `${CLAUDE_SKILL_DIR}` 추가
  - Breaking Change에 Opus 4/4.1 제거 추가
- `references/hooks-guide.md`: `InstructionsLoaded` 이벤트, 신규 Hook 필드 추가
- `references/official/hooks.md`: `InstructionsLoaded` 이벤트 (17번째) 추가
- `references/mcp-guide.md`: `oauth.authServerMetadataUrl` 옵션 추가
- `references/version-sync.md`: v2.1.71 변경사항 추적 추가
- 버전: 2.13.0 → 2.14.0

### Breaking Changes
- Opus 4, Opus 4.1 Claude Code 1st-party API에서 제거 — Opus 4.6으로 자동 이전 (v2.1.68)
- `/plugin uninstall`이 `.claude/settings.local.json` 수정으로 변경 (`.claude/settings.json` 비수정, v2.1.71)

---

## [2.13.0] - 2026-03-04

### Added
- **Claude Code v2.1.66 동기화**
  - 불필요한 오류 로그 감소 (spurious error logging 제거)

### Changed
- `SKILL.md`: 핵심 변경 사항 섹션 v2.1.63 → v2.1.66 업데이트
- `references/version-sync.md`: v2.1.66 변경사항 추적 추가
- 버전: 2.12.1 → 2.13.0

---

## [2.12.1] - 2026-03-03

### Added
- **Skill + Agent Teams 통합 패턴 가이드** (`references/skill-agent-teams-integration-guide.md`)
  - 기존 스킬에 Agent Teams 모드를 추가하는 실전 패턴 가이드
  - 3가지 Archetype: Phase-wave, Batch-parallel, Sequential-chain
  - 태스크 분해 패턴, Context Injection 템플릿, Evaluation + Shutdown 워크플로우
  - Before/After 예시 (CMO, VEO)
- SKILL.md 키워드 매핑: `통합, integration, skill team` → 통합 패턴 가이드

---

## [2.12.0] - 2026-03-01

### Added
- **Claude Code v2.1.63 동기화** (v2.1.54 → v2.1.63 반영)
  - **HTTP Hooks**: `type: "http"` — URL로 JSON POST/수신 (shell 불필요, v2.1.63)
  - **`/simplify`, `/batch`** 번들 슬래시 명령 추가 (v2.1.63)
  - **`/copy`, `/memory`** 명령 추가 (v2.1.59)
  - **Auto Memory 자동 저장**: Claude가 유용한 컨텍스트를 자동 저장, `/memory`로 관리 (v2.1.59)
  - Project config & Auto memory를 같은 레포의 git worktree 간 공유 (v2.1.63)
  - `ENABLE_CLAUDEAI_MCP_SERVERS=false` 환경변수로 claude.ai MCP 서버 비활성화 (v2.1.63)
  - 다수 메모리 누수 수정 (git root cache, JSON parsing cache, MCP server cache 등) (v2.1.63)

### Changed
- `SKILL.md`: 핵심 변경 사항 섹션 v2.11.0 → v2.1.63 업데이트
  - MCP 테이블: `ENABLE_CLAUDEAI_MCP_SERVERS=false` 추가
  - Memory 테이블: Worktree 간 공유 항목 추가
  - 신규 Hook 타입 (`type: "http"`) 명시
- `references/hooks-guide.md`: HTTP hook 타입 추가, 버전 v2.12.0 업데이트
- `references/official/hooks.md`: Handler 타입 테이블에 http 추가
- `references/mcp-guide.md`: `ENABLE_CLAUDEAI_MCP_SERVERS=false` 환경변수 추가
- `references/memory-rules-guide.md`: Auto Memory worktree 공유 내용 추가
- `references/version-sync.md`: v2.1.63 변경사항 추적 추가
- 버전: 2.11.0 → 2.12.0

---

## [2.11.0] - 2026-02-25

### Added
- **Claude Code v2.1.53 동기화** (v2.1.39 → v2.1.53, 14개 버전 반영)
  - Hook 이벤트 2개 추가: `WorktreeCreate`, `WorktreeRemove` (총 16개)
  - Agent 정의 필드 추가: `isolation: worktree`, `background: true`
  - CLI 명령어 추가: `claude agents`, `claude auth`, `claude remote-control`, `--worktree (-w)`
  - Plugin 시스템 강화: `settings.json` 동봉, npm 레지스트리, managed settings (plist/Registry)
  - MCP: claude.ai MCP connectors 지원
  - 환경변수 5개 추가 (`CLAUDE_CODE_ACCOUNT_UUID` 등)
- **GitHub Actions 버전 동기화 워크플로우 안정화**
  - Claude Code Action → shell script 기반으로 전환 (SDK 크래시 해결)

### Changed
- 모델 변경: Sonnet 4.5 → Sonnet 4.6 (Max plan), Opus 4.6 1M context
- `references/hooks-guide.md`: 이벤트 테이블 16개로 확장
- `references/subagents-guide.md`: Agent frontmatter에 isolation/background 추가
- `references/official/hooks.md`: 이벤트 목록 16개로 확장
- `references/version-sync.md`: v2.1.53 변경사항 추적 추가
- 버전: 2.10.0 → 2.11.0

---

## [2.10.0] - 2026-02-13

### Added
- **Ralph Loop (자율 개발 루프) 지원**
  - `references/ralph-loop-guide.md` - Fresh Context Pattern 상세 가이드 (3가지 구현 방법, 종료 감지, 서킷 브레이커, 모범 사례)
  - `scripts/init-ralph.sh` - Ralph Loop 초기화 스크립트 (simple/hook/full 3가지 방식)
  - SKILL.md에 `ralph <project-name>` 인자 처리 규칙 추가
  - 키워드 자동 활성화: ralph, loop, repl, fresh context, autonomous
  - 시나리오 결정 가이드에 "장시간 자율 개발" 분기 추가
- **마켓플레이스 매니페스트** (`.claude-plugin/marketplace.json` 신규 생성)
  - `claude plugin marketplace add` 및 `claude plugin install` 지원

### Fixed
- `plugin.json`의 skills 경로에 `./` 접두사 누락 → `claude plugin validate` 실패 수정
- Ralph Loop `loop.sh`의 heredoc 중첩 프롬프트 전달 오류 → 임시파일(mktemp) 방식으로 수정
- PROGRESS.md 템플릿의 HTML 주석에 `LOOP_COMPLETE` 텍스트 포함 → grep 오탐 수정 (`^LOOP_COMPLETE` 패턴으로 변경)

### Changed
- 확장 기능 유형: 6개 → 7개 (Ralph Loop 추가)
- 참조 문서: 32개 → 33개
- 버전: 2.9.0 → 2.10.0

---

## [2.9.0] - 2026-02-11

### Added
- **공식 문서 레퍼런스** (`references/official/` 신규 생성)
  - `official/skills.md` - Skills 공식 문서 요약 (Frontmatter, 문자열 치환, 동적 컨텍스트)
  - `official/hooks.md` - Hooks 공식 문서 요약 (14 events, Handler 타입, Decision Control)
  - `official/subagents.md` - Sub-agents 공식 문서 요약 (내장 Agent, Frontmatter, Memory)
  - `official/mcp.md` - MCP 공식 문서 요약 (Transport, Scope, Managed MCP)
  - `official/memory-rules.md` - Memory & Rules 공식 문서 요약 (5단계 계층, Auto Memory)
  - `official/tools.md` - Built-in Tools 레퍼런스 (28+ 도구, 토큰 수, 위험도, 권장 조합)
- **GitHub 레포 레퍼런스** (`references/github/` 신규 생성)
  - `github/README.md` - Tier별 레포 인덱스 (Top 11 Quick Reference)
  - `github/official-repos.md` - T1 Anthropic 공식 레포 (skills, claude-code, plugins-official 등)
  - `github/ecosystem-collections.md` - T2 종합 컬렉션 (obra/superpowers, everything-claude-code 등)
  - `github/specialized-tools.md` - T3/T4 특화 도구 12개 (유즈 케이스 포함)
  - `github/patterns.md` - 크로스 레포 검증 패턴 10가지 (Progressive Disclosure, 3-Tier Model 등)
- **Git Submodule** `Piebald-AI/claude-code-system-prompts` 추가 (`repos/claude-code-system-prompts`)
  - Claude Code 시스템 프롬프트 원문 (버전별 추적)
  - Tool Description 스펙 (파라미터, 사용 규칙)
- SKILL.md 참조 문서 섹션에 official/, github/ 카테고리 추가

### Changed
- SKILL.md 참조 문서 구조 재편 (기존 external-resources.md → official/ + github/ 보완)
- 공식 문서 URL에 Settings 추가

---

## [2.8.0] - 2026-02-11

### Added
- **MCP 상세 가이드** (`references/mcp-guide.md` 신규 생성)
  - HTTP Transport (권장), SSE deprecated, Stdio 지원
  - Scope 계층 (Local > Project > User)
  - .mcp.json 설정 및 환경 변수 확장 (`${VAR}`, `${VAR:-default}`)
  - OAuth 인증 (자동/수동 등록)
  - Tool Search, Resources, Prompts as Commands
  - `claude mcp serve` (Claude Code를 MCP 서버로 노출)
  - Managed MCP (조직 차원 중앙 관리, allowedMcpServers/deniedMcpServers)
  - MCP CLI 명령어 및 Hook 매칭 패턴
- **Memory & Rules 상세 가이드** (`references/memory-rules-guide.md` 신규 생성)
  - 5단계 Memory 계층 (Managed Policy > Project Memory > Project Rules > User Memory > Project Local)
  - CLAUDE.md `@path` imports (5hop 재귀, 순환 참조 감지)
  - Project Rules `paths:` frontmatter, glob 패턴, 서브디렉토리, symlink
  - Auto Memory 시스템 상세
  - CLAUDE.local.md (자동 gitignore)
- SKILL.md "시스템 가이드" 섹션에 mcp-guide.md, memory-rules-guide.md 링크 추가
- 공식 문서 섹션에 MCP, Memory URL 추가

### Changed
- MCP Transport Breaking Change 추가 (SSE → HTTP streamable-http)
- Deprecated 목록에 SSE MCP transport 추가

### Removed
- `references/cookbooks/` → `deprecated/20260211_deprecated-references/` 이동
- `references/infrastructure-showcase/` → `deprecated/20260211_deprecated-references/` 이동
- review-system.md에서 infrastructure-showcase 참조 제거

---

## [2.7.0] - 2026-02-11

### Added
- **Agent Teams 지원** (실험적 기능)
  - `references/agent-teams-guide.md` 신규 생성
  - TeamCreate, SendMessage, TeamDelete 도구 문서화
  - Task Management (TaskCreate, TaskUpdate, TaskList, TaskGet) 문서화
  - Team 워크플로우, 표시 모드, 의존성 추적 가이드
  - SKILL.md에 Agent Teams Quick Reference 섹션 추가
- **Memory & Modular Rules 시스템**
  - Auto Memory (`~/.claude/projects/<project>/memory/`)
  - MEMORY.md 자동 로드 (200줄 제한)
  - Modular Rules (`paths:` frontmatter, 경로별 규칙)
- **MCP 강화 기능**
  - Tool Search (자동 활성화)
  - Prompts as Commands (`/mcp__server__prompt`)
  - Resources (`@server:protocol://path`)
  - OAuth 지원, 설치 Scopes (local > project > user)
- **TeammateIdle Hook 이벤트** (Agent Teams 연동)
- **확장 기능 유형 요약 테이블** 확장 (Agent Team, Memory, Rules 추가)
- **사용 시나리오 결정 가이드** Agent Teams 분기 추가

### Changed
- Claude Code Version v2.1.39+ 지원으로 업데이트
- SKILL.md description에 Agent Teams, Memory, MCP 키워드 추가
- `argument-hint`에 `team` 옵션 추가
- hooks-guide.md v2.7.0으로 업데이트 (TeammateIdle 이벤트, settings.json 예시)
- subagents-guide.md v2.7.0으로 업데이트 (Agent Teams vs Task Tool 비교표)
- skills-guide.md v2.7.0으로 업데이트 (Memory & Modular Rules, $ARGUMENTS[0], 관련 문서 링크)
- best-practices.md v2.7.0으로 업데이트 (Agent Teams/Memory/Rules 모범 사례 추가)
- troubleshooting.md v2.7.0으로 업데이트 (Agent Teams/Memory/TeammateIdle 트러블슈팅)
- skill-subagent-task-guide.md v2.7.0으로 업데이트 (Agent Teams 섹션, 결정 가이드 확장)
- review-system.md v2.7.0으로 업데이트 (Agent Teams/Memory/Rules 리뷰 체크리스트)
- implementation-guide.md v2.7.0으로 업데이트 (Agent Teams/Memory 구현 패턴, 모델 ID 수정)
- Deprecated 목록에 `$ARGUMENTS.0` 문법 추가

### Breaking Changes
- `$ARGUMENTS.0` → `$ARGUMENTS[0]` 문법 변경 (Claude Code 전체)
- NPM 설치 → `claude install` 변경

---

## [2.6.0] - 2026-02-05

### Fixed
- **Dynamic Context 파싱 에러 수정**
  - 문서화 예시 `` !`command` `` 패턴이 실제 명령으로 파싱되는 버그 수정
  - "redirection with no command" 에러 해결
  - 모든 releases/ 버전에도 동일 수정 적용

### Added
- **No Arguments Handler** (인자 없이 호출 시 응답 가이드)
  - AskUserQuestion 도구를 활용한 대화형 메뉴 표시
  - 새 Skill/Hook/Agent 만들기, 질문하기, 문서 보기 옵션
- `argument-hint` frontmatter 추가: `[skill|hook|agent|question] <name or query>`

---

## [2.5.0] - 2026-02-05

### Added
- **자동 버전 동기화 시스템**
  - GitHub Actions 워크플로우 (`.github/workflows/sync-claude-code-docs.yml`)
  - 로컬 버전 체크 스크립트 (`scripts/check-updates.sh`)
  - 버전 동기화 가이드 (`references/version-sync.md`)
- **Skills 신규 옵션 문서화**
  - `disable-model-invocation`: 모델 자동 호출 비활성화
  - `context: fork`: 별도 컨텍스트 실행

### Changed
- Claude Code Version v2.1.31+ 지원으로 업데이트
- SKILL.md에 자동 업데이트 설정 섹션 추가

### Infrastructure
- `scripts/` 폴더 신설
- 자동 업데이트 감지 및 Issue 생성 자동화

---

## [2.4.0] - 2026-02-04

### Changed
- **대규모 구조 리팩토링** (14MB → 1.6MB, 732 files → 147 files)
  - SKILL.md: 674줄 → 241줄 (Progressive Disclosure 적용)
  - 핵심 가이드 분리: skills-guide.md, hooks-guide.md, subagents-guide.md, troubleshooting.md

### Removed
- **외부 프로젝트 제거** (deprecated/20260204_external-projects/로 이동)
  - `tips/`: 외부 팁 모음 (skills/reddit-fetch 등)
  - `claude-orchestrator/`: 별도 프로젝트
  - `awesome-claude-agents/`: 외부 에이전트 모음
- **중복 문서 통합** (deprecated/20260204_consolidated-docs/로 이동)
  - best-practices-qa-guide.md + claude-code-best-practices.md + skill-review-guidelines.md → best-practices.md
  - dspy-guide.md (별도 dspy-prompt-optimizer 스킬로 이관)

### Added
- `references/best-practices.md`: 통합 모범 사례 가이드
- `references/external-resources.md`: 외부 리소스 링크 모음
- `evaluations/`: 평가 프레임워크 전용 폴더

---

## [2.3.0] - 2026-02-04

### Added
- **신규 Hook 이벤트** (v2.1.30+ 기반)
  - `SubagentStart`: 서브에이전트 생성 시점에 트리거
  - `PostToolUseFailure`: 도구 호출 실패 후 트리거
  - `Setup`: 초기 설정 (--init, --init-only, --maintenance)
- **신규 Hook 타입**
  - `type: "prompt"`: 프롬프트 기반 Hook (Claude가 처리)
  - `type: "agent"`: 에이전트 기반 Hook (전용 에이전트 실행)
  - `async: true`: 비동기 Hook (백그라운드 실행)
- **MCP 도구 Matcher 패턴**: `mcp__*`, `mcp__supabase__*` 등
- **Subagent 신규 옵션**
  - `disallowedTools`: 명시적 도구 차단 목록
  - `permissionMode`: 권한 모드 (default, acceptEdits, dontAsk, bypassPermissions, plan)
  - `skills`: 스킬 프리로드
  - `resume`: 에이전트 재개 기능
- **Plugin System** 섹션 추가 (Marketplace, MCP OAuth 통합)
- **Bash** 내장 서브에이전트 추가

### Changed
- Hook 이벤트 테이블에 Decision 제어 컬럼 추가 (block/modify, allow/deny)
- settings.json 예시에 신규 Hook 이벤트 추가
- Agent Frontmatter 옵션 테이블 확장
- 공식 문서 기반 Claude Code Version v2.1.30+으로 업데이트

### Fixed
- Exit code 2 설명을 "레거시, decision 방식 권장"으로 명확화

---

## [2.2.0] - 2026-01-24

### Added
- **Bidirectional Skill ↔ Subagent Integration Architecture** (v2.1.19 공식 문서 기반)
  - Skill + `context: fork` + `agent` → SKILL.md 내용이 Task로 전달
  - Subagent + `skills` 필드 → Subagent body가 System Prompt, Skills 사전 로드
- **Dynamic Context Injection** with `!`command`` syntax
- **String Substitution Variables**: `$ARGUMENTS`, `${CLAUDE_SESSION_ID}`
- **Permission Modes** 문서화: default, acceptEdits, dontAsk, bypassPermissions, plan
- **Foreground vs Background Execution** 패턴 정리
- 공식 Frontmatter 필드: `argument-hint`, `user-invocable`

### Changed
- `skill-subagent-task-guide.md` Claude Code v2.1.19 공식 문서 기준으로 전면 업데이트
- Frontmatter 옵션 테이블 공식 필드로 갱신
- Subagent 제약사항 업데이트 (Background MCP 제한, Skills 상속 불가, 15k char 예산)

### Fixed
- 호출 제어 조합표 정확성 개선

---

## [2.1.1] - 2026-01-23

### Added
- **orchestrator-principles.md v1.1.0** 주요 업데이트:
  - Section 5.4: SubagentStop Hook 활용 (자동 검증 스크립트 예시)
  - Section 6: Checklist-Driven Evaluation (Phase별 Completion Checklist, Result Report 강제화, 자동 검증 로직)
  - Section 7: Agent Council & Codex 활용 전략 (효율적 활용 시점, Phase 0 기준 수립, 실패 시에만 Council 소집)

### Changed
- orchestrator-principles.md 목차 및 섹션 번호 재정렬 (6→8, 7→9)

### Note
- **핵심 원칙**: Agent Council/Codex를 매 Phase마다 호출하는 것보다 **Checklist + 자동 검증**이 더 효율적이고 확실함
- Council은 2회 연속 실패 시에만 소집하여 비용 최적화

---

## [2.1.0] - 2026-01-22

### Added
- Section 4: Orchestrator Skill 가이드 추가
  - `orchestrator-principles.md` 참조 문서
  - `orchestrator-skill-creation-guide.md` 참조 문서
- Context Injection System 설명 추가

### Changed
- 참조 테이블에 Orchestrator 문서 추가

---

## [2.0.0] - 2026-01-15

### Added
- Agent SDK 섹션 추가
- 최신 Hook 이벤트 (SessionStart, SubagentStop, PreCompact, PermissionRequest) 문서화

### Changed
- deprecated features 목록 업데이트
- Slash Commands & Skills 통합 안내 추가

---

## [1.2.0] - 2025-12-23 (Draft)

### Changed
- 구조 간소화 시도 (SKILL.md.new로 저장됨)

---

## [1.1.0] - 2025-12-23

### Changed
- 내용 업데이트

---

## [1.0.0] - 2025-12-23

### Added
- Initial version
- Claude Code Extensions (Skills, Hooks, Agents) 가이드
- 공식 문서 기반 참조 체계 구축
