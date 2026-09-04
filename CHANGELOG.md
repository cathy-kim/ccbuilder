# Changelog - Claude Code Extension Builder

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---


## [2.55.0] - 2026-09-04

### Added
- **Claude Code v2.1.260 sync** (v2.1.220 → v2.1.260 콘텐츠 반영)
  - (v2.1.260) **`/diff` 패널** — 풀스크린 모드에서 대화 옆에 미커밋 변경사항 diff 패널 표시, `/diff`로 토글
  - (v2.1.260) **`/advisor` 텍스트 폼** — desktop 앱·Remote Control·headless(-p/SDK)에서 `/advisor`, `/advisor <model>`, `/advisor off`
  - (v2.1.260) `/cost`·상태줄 `prompt_cache` 필드에 캐시 미스 가능 원인(도구 정의·시스템 프롬프트 변경, TTL 경과 등) 표시
  - (v2.1.260) `/reload-plugins` 헤드리스 세션 지원; `/ultrareview` 클라우드 리뷰 대기시간 30→45분; 서브에이전트 백그라운드 명령 1시간 제한 제거
  - (v2.1.260) **`Read()` deny 규칙의 Bash 인자 적용을 2.1.259에서 롤백** — `npm run build`가 `Read(./**/build/**)` 규칙에 걸려 auto mode에서도 차단되던 회귀 수정
  - (v2.1.259) **`managedMcpServers`** 관리형 설정 신규 — 조직이 모든 사용자에게 HTTP/SSE MCP 서버 제공(`.mcp.json`과 동일 형식)
  - (v2.1.259) `--permission-prompts none` — 무인 헤드리스 호스트에서 프롬프트 대상 명령 자동 거부(active mode는 계속 판단)
  - (v2.1.259) `glab mr create/merge/close/reopen/note/update` 인식 → GitLab MR을 `MR !N`으로 표시, 풋터 MR 배지 갱신
  - (v2.1.259) `claude plugin validate --json` — 머신 판독 가능 검증 리포트
  - (v2.1.259) **Breaking**: `allowedMcpServers`가 이제 사용자가 직접 추가한 서버만 대상 — `managed-mcp.json`의 리터럴 서버는 더 이상 자동 필터링되지 않음(차단은 `deniedMcpServers`)
  - (v2.1.259) **관리형 설정 파싱 실패 시 시작 거부로 변경** — 이전엔 조용히 미적용되던 것이 이제 소스 이름과 함께 시작 거부
  - (v2.1.257) **Claude Fable 5.1**(`claude-fable-5-1`) 출시 — 신규 기본 Fable 모델, 1M 컨텍스트, $10/$50 per Mtok($0.25/Mtok 캐시읽기)
  - (v2.1.257) `timeFormat`/`timeZone` 설정 — 12시간·24시간·24시간 UTC·strftime 패턴
  - (v2.1.257) auto mode **Containment Escape 룰** 추가 — 클라우드 메타데이터 크리덴셜 페치·egress 회피·크로스테넌트 접근 자동승인 차단
  - (v2.1.257) `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`, agent frontmatter `experimental.cacheTtl`(`5m`|`1h`), `/effort s`(세션 한정), `permissions.blockReadsOutsideWorkingDirectories`
  - (v2.1.251) **`PreModelSwitch`·`PostModelSwitch` Hook 이벤트 신규** — 모델 전환을 차단·확인·주석 처리(block/confirm/annotate)
  - (v2.1.251) Remote Control에 포그라운드 서브에이전트 도구 호출·결과 실시간 스트리밍; `/usage` Spend limit bar; `/cost` 프롬프트 캐시 히트율 라인 + `prompt_cache` 상태줄 필드
  - (v2.1.248) **`--restricted`**(`CLAUDE_CODE_RESTRICTED=1`) — 명령 실행 도구·`WebFetch` 제거, 파일 도구 작업 디렉토리 내 제한, `bypassPermissions` 거부
  - (v2.1.248) 크로스세션 메시징(SendMessage/ListAgents)이 Bedrock·Vertex·Foundry·텔레메트리 비활성 세션에서도 지원
  - (v2.1.247) **`SendFeedback` 도구 신규** — 세션 중 문제 발생 시 피드백 초안 작성 후 `/feedback`에서 검토·전송(`feedbackDrafts` 설정으로 끄기)
  - (v2.1.247) `spinnerTipsOverride`에 `{id,text,cooldownSessions,priority}`·`tipsFile`·`label`; `/claude-api cost-optimize` 신규

### Changed
- SKILL.md: 핵심 변경 사항 섹션 헤딩 v2.1.220 → v2.1.260; MCP·Hook·CLI/Plugin/Agent·Breaking Changes 섹션에 위 항목 반영, Hook 이벤트 목록에 `PreModelSwitch`·`PostModelSwitch` 추가(29개)
- `references/version-sync.md`: v2.1.260 변경사항 추적 엔트리 추가
- `references/hooks-guide.md`, `references/official/hooks.md`: `PreModelSwitch`·`PostModelSwitch` Hook 이벤트 추가
- `references/mcp-guide.md`, `references/official/mcp.md`: `managedMcpServers` 관리형 설정 추가, `allowedMcpServers` 동작 변경(Breaking) 반영
- `references/official/tools.md`: `SendFeedback` 도구 추가

### Breaking Changes (Claude Code v2.1.259)
- `allowedMcpServers`가 사용자 추가 서버만 govern — `managed-mcp.json` 리터럴 서버는 더 이상 자동 필터링 안 됨
- 관리형 설정(managed-settings.json 등) 파싱 실패 시 조용히 미적용되는 대신 시작을 거부

### Fixed (Claude Code v2.1.221~260 주요 수정)
- `Edit`/`Write`/`Read` 권한 규칙에 괄호가 포함될 때 Bash 샌드박스가 무효로 처리해 "read-only" 폴더가 쓰기 가능해지던 버그 수정 (v2.1.260)
- 컴파일 불가능한 패턴(닫히지 않은 `[` 등)을 가진 파일 권한 규칙 하나가 모든 파일 편집을 "Invalid regular expression" 오류로 실패시키던 버그 수정 (v2.1.260)
- zsh `REPORTTIME`/`REPORTMEMORY`/`DIRSTACKSIZE` 할당에 숨은 명령 치환이 Bash 권한 검사에서 자동 승인되던 버그 수정 (v2.1.260)
- `/rewind`·`--rewind-files`가 체크포인트 백업 파일이 없는데도 복원 성공으로 보고하던 버그 수정 (v2.1.260)
- 서브에이전트가 SendMessage로 재개한 다른 에이전트의 완료 알림을 받지 못하던 버그 수정 (v2.1.260)
- 동시 세션이 서로의 `~/.claude.json` 변경을 되돌리던 버그 수정 — workspace trust·MCP/프로젝트 상태 유실 방지 (v2.1.259)
- managed-settings 파일·드롭인·MDM plist·HKLM 값 파싱 실패 시 조용히 무시되던 버그 수정 (v2.1.259)
- Stop이 remote-control 세션의 백그라운드 에이전트·워크플로우를 실제로 멈추지 못하던 버그 수정 (v2.1.259)


## [2.54.0] - 2026-07-26

### Added
- **Claude Code v2.1.220 sync** (v2.1.218 → v2.1.220 콘텐츠 반영)
  - (v2.1.219) **Claude Opus 5** (`claude-opus-5`) 출시 — 신규 기본 Opus 모델, 1M 컨텍스트, Fast Mode $10/$50 per Mtok
  - (v2.1.219) **서브에이전트 중첩 파견 기본값 재변경** — depth 3까지 기본 허용 (v2.1.217 "기본 비허용" 대체), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`로 비활성화 가능
  - (v2.1.219) `sandbox.network.strictAllowlist` 설정 — 샌드박스 명령 미허용 호스트를 프롬프트 없이 거부
  - (v2.1.219) **`DirectoryAdded` Hook 신규** — `/add-dir` 또는 SDK `register_repo_root`로 세션 중 새 작업 디렉토리 등록 시 발동
  - (v2.1.219) 헤드리스 stream-json init 이벤트 `mcp_server_errors` — `--mcp-config` 검증 실패 스킵 서버 목록, 터미널 시작 경고
  - (v2.1.219) `workflowSizeGuideline` 설정 키 — Dynamic workflow 권장 크기 지정; 기본값 medium(15개 미만 에이전트)으로 변경, 상태줄에 현재 크기 표시
  - (v2.1.219) stream-json depth-2+ 중첩 서브에이전트 전달 — `--forward-subagent-text` 설정 시 파견 Agent `tool_use` id로 키 지정
  - (v2.1.219) `claude mcp list`/`/mcp` HTTP 상태·오류 텍스트 표시, MCP 설정 값 숨은 공백 경고
  - (v2.1.219) managed MCP allowlist/denylist `${VAR}` — 시작 환경변수·managed-settings env에서 해석 (설정 파일 env 대신)
  - (v2.1.219) `/model` 피커 신규 모델명만 하이라이트, `claude --teleport` 레포 불일치 표시, Remote Control 오류 메시지에 원인 설정명 명시
  - (v2.1.219) claude-api 스킬 기본 모델 Opus 5 전환 (Opus 4.8 마이그레이션 경로 포함)
  - (v2.1.220) 버그 수정 및 안정성 개선

### Changed
- SKILL.md: 핵심 변경 사항 섹션 헤딩 v2.1.218 → v2.1.220; MCP·Hook·Agent/CLI·Breaking Changes 섹션에 위 항목 반영, Hook 이벤트 목록에 `DirectoryAdded` 추가(27개)
- `references/version-sync.md`: v2.1.220 변경사항 추적 엔트리 추가
- `references/subagents-guide.md`, `references/official/subagents.md`: 서브에이전트 중첩 파견 기본값 재변경(depth 3 복원), Fast Mode 대상 모델 변경 반영
- `references/mcp-guide.md`, `references/official/mcp.md`: managed MCP `${VAR}` 해석 변경, headless `mcp_server_errors` 진단 필드 반영
- `references/hooks-guide.md`, `references/official/hooks.md`: `DirectoryAdded` Hook 이벤트 추가

### Breaking Changes (Claude Code v2.1.219)
- 서브에이전트 중첩 파견 기본값이 depth 3 허용으로 복원 — v2.1.217의 "기본 비허용"을 대체
- Fast Mode에서 Opus 4.7 제거 — Opus 5·Opus 4.8에만 적용

### Fixed (Claude Code v2.1.219 주요 수정)
- `claude -p` 중간 스트림 API 오류 시 이미 생성된 텍스트 응답 유실 수정
- Fable 모델 행 stale 캐시로 인한 "Requires usage credits" 오표시 수정
- `/model` 피커 병합 Opus 행 "Opus (1M context)" 표시 복원
- GNU screen copy-on-select가 base64를 터미널에 출력하던 버그 수정
- Remote Control 클라이언트 stale fast-mode 상태 표시 수정
- Windows `CLAUDE_CODE_GIT_BASH_PATH` 비-bash 바이너리 지정 시 경고 후 무시로 변경
- vim NORMAL 모드 빈 프롬프트 ← 키 에이전트 뷰 복귀 버그 수정
- 화면낭독기 모드 매 키 입력마다 전체 줄 재작성하던 버그 수정









## [2.53.0] - 2026-07-23

### Added
- **Claude Code v2.1.218 sync** (v2.1.181 → v2.1.218 콘텐츠 반영; v2.1.205 이후 실제 변경사항 정리)
  - (v2.1.218) `/code-review`가 백그라운드 서브에이전트로 실행 — 대화 컨텍스트를 점유하지 않고 스택된 슬래시 명령을 리뷰 대상으로 유지
  - (v2.1.218) `/deep-research`는 수동 호출 시에만 시작 — Claude가 더 이상 자율적으로 실행하지 않음
  - (v2.1.218) Skill·플러그인 frontmatter boolean에 `yes`/`no`/`on`/`off`/`1`/`0`(대소문자 무관) 허용
  - (v2.1.218) agent frontmatter 이름에 `:` 포함 시 거부 — 플러그인 네임스페이싱 예약 문자
  - (v2.1.217) 동시 실행 서브에이전트 상한 추가 (기본 20, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`)
  - (v2.1.217) **서브에이전트 기본 중첩 파견 비활성화** — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로만 허용 (기존 5레벨 재귀 파견 기본 동작 대체)
  - (v2.1.217) emoji shortcode 자동완성 (`:heart:` → ❤️, `emojiCompletionEnabled` 설정)
  - (v2.1.217) `--max-budget-usd` 한도 도달 시 신규 백그라운드 서브에이전트 스폰 거부 + 실행 중 에이전트 중단
  - (v2.1.216) `sandbox.filesystem.disabled` 설정 — 네트워크 egress 제어 유지하며 파일시스템 격리만 스킵
  - (v2.1.215) Claude가 `/verify`·`/code-review`를 더 이상 자율적으로 실행하지 않음 — 명시적 호출 필요
  - (v2.1.214) **`EndConversation` 도구 추가** — 심각한 악용·탈옥 시도 세션 자체 종료
  - (v2.1.214) 장시간 도구 호출 진행 heartbeat, `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`, docker 데몬 리다이렉트 플래그 권한 프롬프트
  - (v2.1.212) **`/fork`가 백그라운드 세션 생성으로 변경** — 기존 인라인 서브에이전트 launch는 `/subtask`로 분리
  - (v2.1.212) `claude auto-mode reset`, WebSearch 세션 한도(기본 200, `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`), 서브에이전트 파견 세션 한도(기본 200, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`)
  - (v2.1.212) MCP 도구 호출 2분 초과 시 자동 백그라운드 전환 (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`)
  - (v2.1.212) Task tool `mode` 파라미터 제거(deprecated) — 서브에이전트는 부모 세션 permission mode 상속
  - (v2.1.211) `--forward-subagent-text`/`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`, "always allow" 권한 규칙 레포 루트 저장(worktree 간 공유)
  - (v2.1.210) 도구 호출 실시간 경과 시간 카운터, `Write(path)`/`NotebookEdit(path)`/`Glob(path)` 권한 규칙 시작 경고
  - (v2.1.208) 스크린리더 모드(`--ax-screen-reader`), `vimInsertModeRemaps` 설정, `CLAUDE_CODE_PROCESS_WRAPPER`
  - (v2.1.207) Auto mode Bedrock·Vertex·Foundry opt-in 불필요; 해당 플랫폼 기본 모델 Opus 4.8 전환
  - (v2.1.206) `/cd` 경로 자동완성, `/doctor` CLAUDE.md 트리밍 제안, `/commit-push-pr` push remote 자동 허용 확장, `EnterWorktree` 외부 진입 확인

### Changed
- SKILL.md: 핵심 변경 사항 섹션 헤딩 v2.1.181 → v2.1.218; MCP·Agent/CLI·Breaking Changes 섹션에 위 항목 반영
- `references/version-sync.md`: v2.1.218 변경사항 추적 엔트리 추가
- `references/subagents-guide.md`, `references/official/subagents.md`: 서브에이전트 중첩 파견 기본값 변경, 동시 실행 상한, `/fork`→백그라운드 세션 변경 반영
- `references/mcp-guide.md`, `references/official/mcp.md`: MCP 도구 호출 자동 백그라운드 전환 반영
- `references/official/tools.md`: `EndConversation` 도구 추가

### Fixed (Claude Code v2.1.205~218 주요 수정)
- Windows 경로(`C:\Users\unicorn` 등 `\u` 접두 세그먼트)가 도구 입력에서 CJK 문자로 손상되던 버그 수정 (v2.1.218)
- `Edit(src/**)` 등 단일 세그먼트 `dir/**` allow 규칙이 트리 전체 중첩 `dir/`에 잘못 자동 승인되던 보안 버그 수정 (v2.1.214)
- Windows PowerShell 5.1 세션 권한 검사 우회 취약점 수정 (v2.1.214)
- 10,000자 초과 Bash 명령이 검사 없이 자동 실행되던 버그 수정 — 이제 항상 프롬프트 (v2.1.214)
- MCP 대형 tool output 트런케이션 시 전체 결과가 세션 종료까지 메모리에 남던 누수 수정 (v2.1.217)
- 장기 세션에서 메시지 정규화 비용이 턴 수에 이차적으로 증가해 발생하던 수 초 단위 지연·재개 지연 수정 (v2.1.216)

## [2.52.0] - 2026-07-08

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.204
- Note: AI content analysis was skipped — manual review recommended

## [2.51.0] - 2026-07-06

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.201
- Note: AI content analysis was skipped — manual review recommended

## [2.50.0] - 2026-06-28

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.195
- Note: AI content analysis was skipped — manual review recommended

## [2.49.0] - 2026-06-27

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.195
- Note: AI content analysis was skipped — manual review recommended

## [2.48.0] - 2026-06-26

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.193
- Note: AI content analysis was skipped — manual review recommended

## [2.47.0] - 2026-06-24

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.187
- Note: AI content analysis was skipped — manual review recommended

## [2.46.0] - 2026-06-21

### Changed
- Claude Code compatibility updated: v2.1.181 -> v2.1.185
- Note: AI content analysis was skipped — manual review recommended

## [2.45.0] - 2026-06-18

### Added
- **Claude Code v2.1.181 sync** (v2.1.179 → v2.1.181; v2.1.180 미발행)
  - `/config key=value` — 프롬프트에서 모든 설정 즉시 변경 (interactive·`-p`·Remote Control)
  - `sandbox.allowAppleEvents` opt-in 설정 (macOS 샌드박스 명령 Apple Events 전송 허용)
  - `CLAUDE_CLIENT_PRESENCE_FILE` 환경변수 (마커 파일로 모바일 푸시 알림 억제)

### Changed
- SKILL.md: 핵심 변경 섹션 v2.1.173 → v2.1.181, footer v2.1.179+ → v2.1.181+, 신규 명령(`/config`)·env(`sandbox.allowAppleEvents`/`CLAUDE_CLIENT_PRESENCE_FILE`) 추가
- version-sync.md: v2.1.181 엔트리 추가
- plugin.json/marketplace.json/README → v2.45.0 / Claude Code v2.1.181+

### Fixed (Claude Code v2.1.181 주요 수정)
- foreground subagent 무제한 중첩 체인 → background와 동일 5단계 깊이 제한
- 커스텀 `ANTHROPIC_BASE_URL`/Foundry prompt caching 미동작 수정
- `claude mcp get`/`list`가 tools/list 실패 시에도 `✓ Connected` 표시 → `! Connected · tools fetch failed`

---

## [2.44.0] - 2026-06-17

### Changed
- Claude Code compatibility updated: v2.1.173 -> v2.1.179
- Note: AI content analysis was skipped — manual review recommended

## [2.43.0] - 2026-06-16

### Changed
- Claude Code compatibility updated: v2.1.173 -> v2.1.178
- Note: AI content analysis was skipped — manual review recommended

## [Unreleased]

### Added
- `seongsu-kang/tycono` 서브모듈 추가 — tycono.ai 플랫폼 레퍼런스 (`references/github/repos/`)
- `yeachan-heo/oh-my-claudecode` 서브모듈 추가 — OMC orchestration layer 레퍼런스 (`references/github/repos/`)

---

## [2.42.0] - 2026-06-11

### Added
- **Claude Code v2.1.173 sync**
  - (v2.1.170) **Claude Fable 5** 출시 — Mythos 클래스 모델, 일반 사용 가능; v2.1.170 이상 업데이트 필요
  - (v2.1.172) **서브에이전트 재귀 파견 최대 5레벨** — 서브에이전트가 자체 서브에이전트 파견 가능 (최대 5단계 깊이)
  - (v2.1.172) Amazon Bedrock `~/.aws` config에서 `AWS_REGION` 미설정 시 리전 자동 읽기; `/status`에 리전 출처 표시
  - (v2.1.172) `/plugin` 마켓플레이스 플러그인 브라우저 검색창 추가
  - (v2.1.172) `claude_code.lines_of_code.count` OTEL 메트릭에 `model` 속성 추가
  - (v2.1.173) Fable 5 모델명 `[1m]` 접미사 자동 제거 — Fable 5는 1M 컨텍스트 기본 포함

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.169 → v2.1.173 업데이트
  - 섹션 제목 v2.1.173으로 변경
  - Agent 섹션: 서브에이전트 재귀 파견 최대 5레벨 추가
  - CLI 섹션: Claude Fable 5, Bedrock `~/.aws` 리전 읽기, Fable 5 `[1m]` 접미사 정규화 추가
  - Plugin 섹션: `/plugin` 마켓플레이스 검색창 추가
- `references/version-sync.md`: v2.1.173 변경사항 추적 엔트리 추가
- `references/subagents-guide.md`: 서브에이전트 재귀 파견 5레벨 추가
- `references/official/subagents.md`: 서브에이전트 최대 중첩 깊이 추가

### Fixed
- Windows에서 sandbox 활성화 시 불필요한 "sandbox dependencies missing" 경고 수정 (v2.1.173)
- Fable 5 모델명 `[1m]` 접미사 중복 표기 정규화 (v2.1.173)
- 1M 컨텍스트 사용 세션이 사용 크레딧 없을 때 영구 중단되던 버그 수정 (v2.1.172)
- 백그라운드 에이전트가 다른 디렉토리 project settings (`.mcp.json` 승인·trust) 읽던 버그 수정 (v2.1.172)
- `availableModels` 제한이 서브에이전트 모델 오버라이드·에이전트 디스패치 모델 피커에 미적용되던 버그 수정 (v2.1.172)
- `WebFetch(domain:*.example.com)` 와일드카드 도메인 규칙이 서브도메인과 매칭되지 않던 버그 수정 (v2.1.172)
- 원격 세션에서 마운트된 팀 메모리 스토어 (`CLAUDE_MEMORY_STORES`) 메모리 리콜 미동작 수정 (v2.1.172)
- VS Code 통합 터미널에서 실행된 세션 트랜스크립트 미저장 버그 수정 (v2.1.170)

---

## [2.41.0] - 2026-06-09

### Added
- **Claude Code v2.1.169 sync**
  - (v2.1.169) `--safe-mode` 플래그 및 `CLAUDE_CODE_SAFE_MODE` env var — CLAUDE.md·플러그인·스킬·훅·MCP 서버 모두 비활성화하여 시작 (트러블슈팅용)
  - (v2.1.169) `/cd` 명령 — 프롬프트 캐시를 유지하면서 세션 작업 디렉토리 변경
  - (v2.1.169) `disableBundledSkills` 설정 및 `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` env var — 번들 스킬·워크플로우·내장 슬래시 명령 숨김
  - (v2.1.169) `claude agents --json` — 차단된 세션 및 방금 파견된 세션 포함; `--all`로 완료 세션 포함; 신규 `id`·`state` 필드
  - (v2.1.169) CLAUDE.md 너무 길다는 경고 임계값이 모델 컨텍스트 창 크기에 따라 자동 조정
  - (v2.1.169) Vertex/Foundry 5분 기본 유휴 타임아웃 복원 — 스톨 스트림 자동 중단; `API_FORCE_IDLE_TIMEOUT=0`으로 비활성화
  - (v2.1.169) 백그라운드 세션이 retire→wake 후 `--ide`, `--chrome`, `--bare`, `--remote-control` 등 플래그 유지
  - (v2.1.169) `TaskCreate` 안정성 개선 — 잘못된 입력 자동 수정, 미로드 도구 검증 오류 시 스키마 포함
  - (v2.1.166) `fallbackModel` 설정 — 기본 모델 과부하/불가 시 순서대로 시도할 최대 3개 폴백 모델; `--fallback-model` 대화형 세션 지원
  - (v2.1.166) deny 규칙 tool-name 위치 glob 패턴 지원 — `"*"`로 전체 도구 거부; allow 규칙은 MCP 외 glob 거부
  - (v2.1.166) `MAX_THINKING_TOKENS=0`, `--thinking disabled`, 모델별 thinking 토글 — Claude API 기본 thinking 모델 비활성화 (3rd-party 제공자 미변경)
  - (v2.1.166) 예기치 않은 non-retryable 오류 시 폴백 모델로 1회 재시도
  - (v2.1.163) `requiredMinimumVersion` 및 `requiredMaximumVersion` managed settings — 허용 버전 범위 밖 Claude Code 시작 거부
  - (v2.1.163) `/plugin list` 명령 — 설치된 플러그인 목록; `--enabled`/`--disabled` 필터 지원
  - (v2.1.163) Skills `\$` 이스케이프 문법 — 명령 본문에서 숫자 앞 리터럴 달러 기호 표기
  - (v2.1.163) Stop·SubagentStop Hook `hookSpecificOutput.additionalContext` 반환 — hook error 레이블 없이 Claude에 피드백 전달하며 턴 계속
  - (v2.1.163) stdio MCP 서버가 `--resume` 시에도 `CLAUDE_CODE_SESSION_ID` 수신
  - (v2.1.162) `claude agents --json` `waitingFor` 필드 — 대기 세션이 블록된 이유(e.g. 권한 프롬프트) 표시
  - (v2.1.161) `OTEL_RESOURCE_ATTRIBUTES` 값을 메트릭 데이터포인트 레이블로 포함 — 팀·레포 등 커스텀 차원으로 사용량 메트릭 슬라이싱
  - (v2.1.161) 병렬 도구 호출: Bash 명령 실패가 같은 배치의 다른 호출 취소하지 않음

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.158 → v2.1.169 업데이트
  - 섹션 제목 v2.1.169로 변경
  - MCP 섹션: `--resume` 시 stdio MCP 서버 `CLAUDE_CODE_SESSION_ID` 전달 추가
  - Hook 섹션: Stop·SubagentStop `hookSpecificOutput.additionalContext` 반환 추가
  - CLI 섹션: `--safe-mode`, `/cd`, `disableBundledSkills`, `fallbackModel`, deny rule glob, thinking disable, `requiredMinimumVersion`/`requiredMaximumVersion`, `/plugin list`, Skills `\$` 이스케이프, Dynamic Workflow 트리거 `ultracode` 리네임, `claude agents --json` `--all` 추가
  - Breaking Changes: Dynamic Workflow 트리거 리네임, `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 제거, acceptEdits 빌드 도구 파일 프롬프트 추가
- `references/version-sync.md`: v2.1.169 변경사항 추적 엔트리 추가
- `references/hooks-guide.md`: Stop·SubagentStop `hookSpecificOutput.additionalContext` 반환 기능 추가
- `references/official/hooks.md`: Stop·SubagentStop `hookSpecificOutput.additionalContext` 추가
- `references/mcp-guide.md`: `--resume` 시 stdio MCP 서버 `CLAUDE_CODE_SESSION_ID` 전달 추가

### Fixed
- MCP `allowedMcpServers`/`deniedMcpServers` 정책이 재연결·IDE 설정·`--mcp-config` 서버·원격 설정 로드 전 세션에서 미적용되던 버그 수정 (v2.1.169)
- macOS claude.ai 자격증명 로그인 시 매 턴 시작 시 ~30-50ms UI 스톨 수정 (v2.1.169)
- Windows에서 `claude -p` 슬래시 명령/스킬 스캔 대기로 느리거나 행어 현상 수정 (v2.1.169, v2.1.161 회귀)
- Remote Control 세션 재개 중 OAuth 토큰 갱신 동시 발생 시 "reconnecting" 고착 수정 (v2.1.169)
- Windows Git Credential Manager의 "Connect to GitHub" 팝업이 시작 시 표시되던 버그 수정 (v2.1.169)
- 커스텀 statusline 사용 시 footer 힌트(예: "esc to interrupt") 미표시 수정 (v2.1.169)
- 백그라운드 세션이 project-level settings `env` 값(예: `ANTHROPIC_MODEL`) 무시하던 버그 수정 (v2.1.169)
- MCPB 플러그인 캐시 Windows에서 불필요하게 무효화·재추출되던 버그 수정 (v2.1.169)
- 신뢰되지 않은 project settings에서 신뢰 확인 없이 OTEL 클라이언트 인증서 경로 설정 가능하던 보안 수정 (v2.1.169)

### Breaking Changes
- **Dynamic Workflow 트리거 `workflow` → `ultracode`** — "workflow" 단어는 더 이상 트리거하지 않음; 직접 요청은 계속 작동 (v2.1.160)
- **`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 제거** — no-op 환경변수로 변경; 대안: `/model claude-opus-4-6[1m]` 후 `/fast on` (v2.1.160)
- **acceptEdits 모드** — 코드 실행을 허용하는 빌드 도구 설정 파일(`.npmrc`, `.yarnrc*`, `bunfig.toml`, `.bazelrc`, `.pre-commit-config.yaml`, `.devcontainer/` 등) 쓰기 전 프롬프트 (v2.1.160)

---

## [2.40.0] - 2026-05-30

### Added
- **Claude Code v2.1.158 sync**
  - (v2.1.158) Auto mode Bedrock·Vertex·Foundry 지원 — Opus 4.7·4.8 대상; `CLAUDE_CODE_ENABLE_AUTO_MODE=1`로 옵트인
  - (v2.1.157) `.claude/skills` 디렉토리 플러그인 자동 로드 — 마켓플레이스 설치 불필요
  - (v2.1.157) `claude plugin init <name>` — `.claude/skills`에 새 플러그인 스캐폴딩
  - (v2.1.157) `/plugin` 인자 자동완성 — 서브커맨드·설치된 플러그인·마켓플레이스 목록 서브스트링 매칭
  - (v2.1.157) `settings.json` `agent` 필드 — dispatched 세션 기본 에이전트 지정; `--agent <name>` 오버라이드
  - (v2.1.157) `EnterWorktree` Claude 관리 worktree 간 mid-session 전환 지원
  - (v2.1.157) `OTEL_LOG_TOOL_DETAILS=1` — `tool_decision` 이벤트에 `tool_parameters` 포함 (bash commands, MCP/skill names)
  - (v2.1.157) Workflow keyword trigger 설정 (`/config`) — "workflow" 단어로 Dynamic Workflow 자동 트리거 비활성화 가능
  - (v2.1.157) Claude 관리 worktree 작업 완료 후 잠금 해제 → `git worktree remove`/`prune` 직접 정리 가능
  - (v2.1.157) `claude agents` dispatch 입력 슬래시 명령 자동완성 서브스트링 매칭
  - (v2.1.157) `/terminal-setup` — VS Code/Cursor/Windsurf 통합 터미널 GPU 가속 비활성화 (텍스트 깨짐 방지)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.156 → v2.1.158 업데이트
  - Plugin 섹션: `.claude/skills` 자동 로드, `claude plugin init`, `/plugin` 자동완성 추가
  - CLI 섹션: Auto mode Bedrock/Vertex/Foundry, Workflow keyword trigger, `OTEL_LOG_TOOL_DETAILS` 추가
  - Agent 섹션: `settings.json` `agent` 필드, `EnterWorktree` worktree 전환 추가
- `references/version-sync.md`: v2.1.158 변경사항 추적 엔트리 추가
- `references/official/subagents.md`: `agent` 필드 settings.json, EnterWorktree worktree 전환 추가
- `references/official/tools.md`: `EnterWorktree` Claude 관리 worktree 전환 설명 추가

### Fixed
- 처리 불가 이미지(zero-byte, 손상) 첨부 시 요청 크래시 → 텍스트 플레이스홀더 처리 (v2.1.157)
- auto·bypass-permissions 모드에서 sandbox 네트워크 권한 프롬프트 불필요하게 표시되던 버그 수정 (v2.1.157)
- `claude agents` 완료 세션이 유휴 서브에이전트 남아 있을 때 정리되지 않던 버그 수정 (v2.1.157)
- 백그라운드 에이전트 worktree가 30일 정리 시 고아로 남는 버그 수정 (v2.1.157)
- sleep/wake 후 재연결된 백그라운드 세션에서 모델이 잘못된 날짜를 사용하던 버그 수정 (v2.1.157)
- `--resume` 이전 프로세스 종료 시 실행 중이던 백그라운드 서브에이전트 미보고 수정 (v2.1.157)
- VS Code/Cursor/Windsurf 통합 터미널에서 우클릭 붙여넣기 중복 버그 수정 (v2.1.157)
- WSL 이미지 붙여넣기(`alt+v`), Windows 11 스크린샷 붙여넣기, Windows Explorer 이미지 드래그 지원 (v2.1.157)

---

## [2.39.0] - 2026-05-29

### Added
- **Claude Code v2.1.156 sync**
  - (v2.1.154) **Opus 4.8** 모델 출시 — xhigh effort 기본값, Fast Mode 2x 비용·2.5x 속도
  - (v2.1.154) **Dynamic Workflows** — `/workflows` 명령으로 수십~수백 에이전트 백그라운드 오케스트레이션
  - (v2.1.154) Lean system prompt 기본값 전환 (Haiku·Sonnet·Opus 4.7 이하 제외)
  - (v2.1.154) `claude agents` `! <command>` — 셸 명령을 백그라운드 세션으로 실행 (`claude --bg --exec '<command>'` 동등)
  - (v2.1.154) Plugin `defaultEnabled: false` 선언 지원 — `/plugin` 또는 `claude plugin enable`로 명시 활성화; 의존 플러그인은 자동 활성화
  - (v2.1.154) `/plugin` Discover 탭 현재 디렉토리 연관 플러그인 고정 표시 (`suggested for this directory` 어노테이션)
  - (v2.1.154) Stdio MCP 서버 서브프로세스에 `CLAUDE_CODE_SESSION_ID`·`CLAUDECODE=1` env 자동 제공
  - (v2.1.154) `claude mcp list`/`get` — 미승인 `.mcp.json` 서버 `⏸ Pending approval` 표시 (파이프 출력 시 자동 승인 방지)
  - (v2.1.152) `MessageDisplay` Hook 이벤트 — 어시스턴트 메시지 텍스트 변환·숨김 가능
  - (v2.1.152) Skills/슬래시 명령 `disallowed-tools` frontmatter — 스킬 활성 중 모델에서 특정 도구 제거
  - (v2.1.152) `/reload-skills` 명령 — 세션 재시작 없이 스킬 디렉토리 재스캔
  - (v2.1.152) `SessionStart` Hook `reloadSkills: true` 반환 — 훅이 설치한 스킬 동일 세션 내 즉시 사용 가능
  - (v2.1.152) `SessionStart` Hook `hookSpecificOutput.sessionTitle` — 시작·재개 시 세션 제목 설정 지원
  - (v2.1.152) Auto mode 옵트인 동의 불필요
  - (v2.1.152) `pluginSuggestionMarketplaces` managed 설정 — 관리자용 조직 마켓플레이스 컨텍스트 팁 허용 리스트
  - (v2.1.153) `skipLfs` 옵션 — `github`/`git` 플러그인 마켓플레이스 소스 Git LFS 다운로드 건너뛰기
  - (v2.1.153) `/model` 선택 신규 세션 기본값으로 저장; `s` 키로 현재 세션만 변경

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.150 → v2.1.156 업데이트
  - 신규 Hook 이벤트 테이블: `MessageDisplay` 추가 (총 26개)
  - Hook 인라인 노트: v2.1.152 `MessageDisplay`, `SessionStart` `reloadSkills`/`sessionTitle` 추가
  - MCP 섹션: Stdio 서버 `CLAUDE_CODE_SESSION_ID`·`CLAUDECODE=1` env, Pending approval 표시 추가
  - CLI 섹션: Opus 4.8, Dynamic Workflows, `/reload-skills`, `disallowed-tools`, `! <command>`, Lean system prompt 전환, `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` deprecated 추가
  - Plugin 섹션: `defaultEnabled: false`, `pluginSuggestionMarketplaces`, Discover 탭 디렉토리 고정 추가
  - Breaking Changes: `modelPicker:setAsDefault` → `modelPicker:thisSessionOnly` 리네임, Lean system prompt 기본값 추가
  - 주요 이벤트 카운트 25 → 26개 업데이트
- `references/version-sync.md`: v2.1.156 변경사항 추적 엔트리 추가
- `references/official/hooks.md`: `MessageDisplay` Hook 이벤트 (#26) 추가
- `references/hooks-guide.md`: `MessageDisplay` Hook 이벤트 + `SessionStart` 신규 필드 추가
- `references/mcp-guide.md`: Stdio 서버 `CLAUDE_CODE_SESSION_ID`·`CLAUDECODE=1` env 섹션 추가

### Fixed
- Opus 4.8 thinking block 수정으로 API 400 오류 발생하던 버그 수정 (v2.1.156)
- 백그라운드 세션 subagent가 worktree isolation 우회하여 shared checkout에 직접 쓰던 버그 수정 (v2.1.154)
- `worktree.baseRef: "head"` linked worktree 내부에서 current worktree HEAD 대신 main checkout HEAD 반환하던 버그 수정 (v2.1.154)
- 핀된 백그라운드 세션이 Claude Code 업데이트 후 매분 respawn으로 알림·프로세스 낭비하던 버그 수정 (v2.1.154)
- managed settings에서 단일 잘못된 `allowedMcpServers`/`deniedMcpServers` 항목이 전체 정책을 무시하던 버그 수정 (v2.1.154)
- stateful MCP 서버 optional GET SSE stream 없을 때 `tools/list` 재연결 루프 버그 수정 (v2.1.153 회귀)
- Agent tool frontmatter MCP 서버가 `--strict-mcp-config`·`--bare`·managed 정책 무시하던 버그 수정 (v2.1.153)

### Breaking Changes
- `modelPicker:setAsDefault` keybinding → `modelPicker:thisSessionOnly` 리네임 (v2.1.153); `/model` 선택 기본값 저장, `s`로 현재 세션만 전환
- `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` deprecated — 2026-06-01 제거 예정; `/model claude-opus-4-6[1m]` 후 `/fast on` 사용 (v2.1.154)

---

## [2.38.0] - 2026-05-23

### Added
- **Claude Code v2.1.150 sync**
  - (v2.1.149) `/usage` 카테고리별 사용량 분석 — skills·subagents·plugins·MCP 서버별 비용 표시로 사용량 원인 파악 가능
  - (v2.1.149) `/diff` 상세 뷰 키보드 스크롤 지원 (arrows·j/k·PgUp/PgDn·Space·Home/End)
  - (v2.1.149) 마크다운 GFM task list 체크박스 렌더링 — `- [ ] todo` / `- [x] done`을 기본 불릿 대신 체크박스로 표시
  - (v2.1.149) Enterprise: `allowAllClaudeAiMcps` managed 설정 — `managed-mcp.json`과 함께 claude.ai cloud MCP 커넥터 동시 로드
  - (v2.1.147) 핀된 백그라운드 세션 (`Ctrl+T` in `claude agents`) 유휴 시에도 유지, Claude Code 업데이트 시 in-place 재시작, 메모리 압박 시에만 비핀 세션 후 제거
  - (v2.1.147) 자동 업데이트 개선 — 네트워크 실패 재시도, 상세 오류 카테고리·OS 에러 코드 보고, 업데이트 실패 시 현재 버전 표시
  - (v2.1.150) 내부 인프라 개선 (사용자 가시 변경 없음)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.146 → v2.1.150 업데이트
  - MCP 섹션: `allowAllClaudeAiMcps` managed 설정 추가 (claude.ai MCP connectors 행)
  - CLI 섹션: `/usage` 카테고리별 분석, `/diff` 키보드 스크롤, GFM 체크박스 렌더링, 핀된 백그라운드 세션 개선 추가
- `references/version-sync.md`: v2.1.150 변경사항 추적 엔트리 추가

### Fixed
- PowerShell 권한 우회 수정 — 내장 `cd` 함수(`cd..`, `cd\`, `cd~`, `X:`)가 감지 없이 워크스페이스 외부 디렉토리 접근 허용하던 버그 (v2.1.149)
- git worktree 내 sandbox 쓰기 허용 리스트가 공유 `.git` 디렉토리 대신 전체 메인 레포 루트를 커버하던 버그 수정 (v2.1.149)
- `find` 명령이 macOS 시스템 파일/vnode 테이블 고갈·호스트 크래시 유발하던 버그 수정 (v2.1.149)
- `/ultraplan` 및 원격 세션 생성 시 변경 없는 워킹 트리에서 "Could not capture uncommitted changes" 실패 수정 (v2.1.149)
- Bash 도구 exit code 127 회귀 수정 (v2.1.147 회귀 → v2.1.148 핫픽스)
- managed-settings 승인 다이얼로그 수락 후 터미널 프리즈 수정 (v2.1.149)

---

## [2.37.0] - 2026-05-21

### Added
- **Claude Code v2.1.146 sync**
  - `/code-review [effort]` 명령 — `/simplify` 리네임, 선택적 effort 레벨 지원 (e.g. `/code-review high`) (v2.1.146)
  - `claude agents --json` — 실행 중 세션 JSON 목록 출력 (스크립팅·tmux-resurrect·status bar 지원) (v2.1.145)
  - `/resume` 백그라운드 세션 지원 — `bg` 마커로 구분 표시 (v2.1.144)
  - `/model` 현재 세션만 변경 — 모델 피커 `d` 키로 신규 세션 기본값 설정 (v2.1.144)
  - `/extra-usage` → `/usage-credits` 리네임 (구 명령 유지) (v2.1.144)
  - `worktree.bgIsolation: "none"` 설정 — 백그라운드 세션 EnterWorktree 없이 작업 디렉토리 직접 편집 (v2.1.143)
  - `claude plugin disable` 의존성 강제 — 다른 플러그인 의존 시 거부 + copy-pasteable disable-chain 힌트 (v2.1.143)
  - `claude plugin enable` 전이적 의존성 자동 강제 활성화 (v2.1.143)
  - `/plugin` 마켓플레이스 브라우즈 패널 예상 컨텍스트 비용(per-turn·per-invocation 토큰) 표시 (v2.1.143)
  - `/plugin` Discover·Browse 화면에서 설치 전 명령·에이전트·스킬·훅·MCP/LSP 서버 상세 미리 보기 (v2.1.145)
  - Stop·SubagentStop Hook 입력에 `background_tasks`·`session_crons` 필드 추가 (v2.1.145)
  - status line JSON 입력에 GitHub 레포·PR 정보 포함 (감지 시) (v2.1.145)
  - auto mode에서 사용자·스킬이 `AskUserQuestion` 명시 의존 시 억제하지 않도록 수정 (v2.1.146)
  - `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` env var — stop hook 블록 반복 상한 오버라이드 (기본 8회) (v2.1.143)
  - 백그라운드 서브에이전트 완료 알림에 elapsed duration 추가 (v2.1.144)
  - PowerShell 도구 `-ExecutionPolicy Bypass` 기본 전달 (v2.1.143)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.142 → v2.1.146 업데이트
  - CLI 섹션: `/code-review`, `claude agents --json`, `/resume` bg 지원, `/model` 세션 전용, `/usage-credits`, `worktree.bgIsolation`, `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` 추가
  - Plugin 섹션: 플러그인 의존성 강제, `/plugin` 상세 미리 보기, 컨텍스트 비용 표시 추가
  - Hook 섹션: Stop·SubagentStop `background_tasks`/`session_crons` 필드 추가
  - Breaking Changes: `/simplify` → `/code-review` 리네임, PowerShell `-ExecutionPolicy Bypass` 기본 전달 추가
- `references/version-sync.md`: v2.1.146 변경사항 추적 엔트리 추가
- `references/hooks-guide.md`: Stop·SubagentStop `background_tasks`/`session_crons` 필드 업데이트
- `references/official/hooks.md`: Stop·SubagentStop `background_tasks`/`session_crons` 필드 업데이트

### Fixed
- MCP `resources/list`, `resources/templates/list`, `prompts/list` 페이지네이션 서버에서 2페이지 이후 항목 누락 버그 수정 (v2.1.146)
- Read 도구 전체 파일 토큰 한도 초과 시 하드 에러 대신 "PARTIAL view" 노티스와 함께 첫 페이지 트런케이션 반환 (v2.1.145)
- 시작 시 `api.anthropic.com` 미달 시 최대 75초 hang 현상 수정 — 사이드 채널 API 호출 15초 타임아웃 (v2.1.144)
- Agent Teams 비ASCII 이름 팀메이트 API 호출 실패 (유효하지 않은 헤더 인코딩) 수정 (v2.1.145)
- Windows PowerShell 도구 winget/Microsoft Store 경유 설치 시 "command line is invalid" 오류 수정 (v2.1.146)
- `/review` deprecated `projectCards` GraphQL 쿼리로 Classic Projects 보유 레포 오류 수정 (v2.1.145)
- `claude plugin validate` `skills:` 항목이 디렉토리 대신 파일 가리킬 때 미검출 수정 (v2.1.145)
- Stop Hook 반복 블록 무한 루프 수정 — 8회 연속 블록 후 경고와 함께 턴 종료 (v2.1.143)

### Breaking Changes
- `/simplify` → `/code-review [effort]` 리네임 (v2.1.146)
- PowerShell 도구 `-ExecutionPolicy Bypass` 기본 전달 — 옵트아웃: `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1` (v2.1.143)

---

## [2.36.0] - 2026-05-15

### Added
- **Claude Code v2.1.142 sync**
  - `claude agents` 신규 플래그 — `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions`으로 백그라운드 세션 상세 설정 가능
  - Fast Mode Opus 4.7 기본 전환 (이전: Opus 4.6); `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`로 Opus 4.6 고정 가능
  - 루트 레벨 `SKILL.md` 보유 플러그인 (`skills/` 서브디렉토리 없음) 스킬로 자동 노출
  - `/plugin` 상세 패널 및 `claude plugin details`에서 플러그인이 제공하는 LSP 서버 목록 표시
  - `/web-setup` 기존 GitHub App 연결 교체 전 경고 추가

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.141 → v2.1.142 업데이트
  - CLI 섹션: `claude agents` 신규 플래그, Fast Mode Opus 4.7 전환 추가
  - Plugin 섹션: 루트 레벨 SKILL.md 플러그인 자동 노출, LSP 서버 표시 추가
- `references/version-sync.md`: v2.1.142 변경사항 추적 엔트리 추가

### Fixed
- `MCP_TOOL_TIMEOUT` 설정이 원격 HTTP/SSE MCP 서버의 per-request fetch timeout에 미반영되던 버그 수정 (도구 호출 60초 상한 → 설정값 적용)
- 백그라운드 세션이 기존 git worktree 미인식으로 Edit 차단 및 `EnterWorktree` 중복 생성 거부하던 버그 수정
- macOS 수면/재개 후 백그라운드 세션 소실 및 daemon 재연결 실패 수정 (클록 점프를 경과 유휴로 잘못 처리하던 문제)
- 바이너리 업그레이드(`brew upgrade` 등) 후 데몬 미정상 종료로 파견 에이전트가 삭제된 경로에서 크래시 루프하던 버그 수정
- `claude --bg --dangerously-skip-permissions` 플래그가 retire/wake 후 유지되지 않던 버그 수정
- 플러그인 `skills: ["./"]` 사용 시 "path escapes plugin directory" 거짓 오류 수정
- Reactive compaction 첫 시도 시 원본 요청 overflow 크기에서 시드 — 낭비 재시도 방지

---

## [2.35.0] - 2026-05-14

### Added
- **Claude Code v2.1.141 sync**
  - Hook JSON 출력 `terminalSequence` 필드 — 제어 터미널 없이 데스크탑 알림·창 제목·벨 신호 발송 가능
  - `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` env var — SSH 키 없는 환경에서 GitHub 플러그인 소스 HTTPS 클론
  - `ANTHROPIC_WORKSPACE_ID` env var — workload identity federation 토큰 특정 워크스페이스 범위 지정
  - `claude agents --cwd <path>` — 세션 목록을 특정 디렉토리 범위로 필터링
  - `/feedback` 최근 세션 포함 지원 (최근 24시간·7일) — 현재 세션 범위를 넘는 이슈 제보 가능
  - Rewind 메뉴 "Summarize up to here" — 최근 대화 유지하며 이전 컨텍스트 압축
  - auto mode permission dialog: `permissions.ask` 규칙이 프롬프트를 발생시킨 경우 원인 설명 추가
  - 파일 편집 권한 프롬프트에서 "view diff in your IDE" 옵션 복원 (IDE 연결 시)
  - 백그라운드 에이전트(`/bg`·`←←`) 현재 permission mode 유지 — 기본값으로 revert 방지
  - `claude agents`: 작업 완료 후 백그라운드 쉘이 남아있는 에이전트를 Completed 상태로 이동
  - thinking 스피너 10초 후 황색 전환 — 장시간 thinking 중 작업 진행 중임을 시각적으로 표시
  - 플러그인 메뉴 탐색 개선: `→`/Tab 탭 전환, `↑` 탭 스트립 이동, 풀스크린 모드 탭 헤더·검색박스 클릭 가능

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.140 → v2.1.141 업데이트
  - Hook 섹션: `terminalSequence` 필드, `EnterWorktree` transcript_path 버그 수정 추가
  - CLI 섹션: `claude agents --cwd`, 백그라운드 에이전트 permission mode 유지, `/feedback` 세션 포함, Rewind "Summarize" 추가
  - 신규 도구·env 섹션: `ANTHROPIC_WORKSPACE_ID`, `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` 추가
- `references/version-sync.md`: v2.1.141 변경사항 추적 엔트리 추가

### Fixed
- Bedrock/Vertex/Foundry/gateway에서 background side-queries에 unavailable Haiku 모델 ID 전송 수정
- `claude daemon status` 및 `/doctor` Windows에서 daemon pipe key file 잠김·읽기 불가 시 불명확 오류 수정
- `claude agents` 크래시된 세션 열 때 작업 디렉토리 삭제 시 중복 dispatch 수정
- hooks에서 `EnterWorktree` 이후 non-existent `transcript_path` 수신 버그 수정
- 마크다운 테이블 셀 줄바꿈 시 세로 key-value 레이아웃으로 폴백하던 회귀 수정 (v2.1.136 회귀)
- `/model` 명령이 한 세션에서 다른 동시 세션의 autocompact 임계값을 변경하던 버그 수정
- MCP HTTP/SSE 서버 연결 시 403 반환 시 "failed" 대신 "needs auth" 표시 수정
- Remote MCP 서버 optional server-events 스트림 재연결 실패 시 불필요한 연결 해제 수정
- MCP 서버 config의 POSIX shell parameter expansion(`${var%pattern}` 등)을 누락 환경변수로 잘못 플래그하던 버그 수정
- `claude plugin install` marketplace `ref`가 upstream에 없을 때 `sha`가 pinned되어도 실패하던 버그 수정
- Bedrock: `awsCredentialExport` — ambient AWS 자격증명 확인 시에도 항상 실행 (cross-account 인증 수정)

---

## [2.34.0] - 2026-05-13

### Added
- **Claude Code v2.1.140 sync**
  - Agent tool `subagent_type` 대소문자·구분자 무관 매칭 — `"Code Reviewer"` → `code-reviewer` 자동 해석 (v2.1.140)
  - agent view (Research Preview): `claude agents` — 실행 중·대기·완료 모든 세션 단일 목록 (v2.1.139)
  - `/goal <condition>` 명령 — 완료 조건 설정, 조건 충족 시까지 자율 실행 (interactive·`-p`·Remote Control, v2.1.139)
  - `/scroll-speed` 명령 — 마우스 휠 속도 라이브 프리뷰 조정 (v2.1.139)
  - Hook `args: string[]` (exec form) — 셸 없이 직접 실행, 경로 플레이스홀더 인용 불필요 (v2.1.139)
  - Hook `continueOnBlock` PostToolUse 옵션 — 거부 사유 모델 피드백 후 턴 계속 (v2.1.139)
  - MCP stdio 서버에 `CLAUDE_PROJECT_DIR` 환경변수 자동 제공; plugin config `${CLAUDE_PROJECT_DIR}` 참조 가능 (v2.1.139)
  - Hook `effort.level` JSON 입력 필드 + `$CLAUDE_EFFORT` env var — 현재 effort 레벨 Bash 서브프로세스 포함 전달 (v2.1.133)
  - `worktree.baseRef` 설정 (`fresh` | `head`) — worktree 브랜치 기준점 선택 (v2.1.133)
  - `sandbox.bwrapPath` / `sandbox.socatPath` 관리형 설정 — Linux/WSL 커스텀 bubblewrap·socat 경로 (v2.1.133)
  - `parentSettingsBehavior` admin-tier 키 (`'first-wins' | 'merge'`) (v2.1.133)
  - `CLAUDE_CODE_SESSION_ID` — Bash 서브프로세스 환경에 세션 ID 자동 제공 (v2.1.132)
  - `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` — 풀스크린 렌더러 비활성화, 네이티브 스크롤백 유지 (v2.1.132)
  - `settings.autoMode.hard_deny` — auto mode 무조건 차단 규칙 (v2.1.136)
  - `--plugin-url <url>` — 세션 전용 플러그인 .zip URL 즉시 로드 (v2.1.129)
  - `skillOverrides` 설정 정상 동작 수정 — `off` / `user-invocable-only` / `name-only` 지원 (v2.1.129)
  - `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` / `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` 신규 env var (v2.1.129)
  - 서브에이전트 API 요청에 `x-claude-code-agent-id` / `x-claude-code-parent-agent-id` 헤더 추가 (v2.1.139)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.126 → v2.1.140 업데이트
  - Agent 섹션: `subagent_type` 대소문자 무관 매칭, agent view, `/goal`, agent 헤더 추가
  - Hook 섹션: `args` exec form, `continueOnBlock`, `effort.level`/`$CLAUDE_EFFORT` 추가
  - MCP 섹션: `CLAUDE_PROJECT_DIR`, `workspace` 예약명 추가
  - CLI 섹션: `/goal`, `/scroll-speed`, `CLAUDE_CODE_SESSION_ID`, `worktree.baseRef`, `skillOverrides` 등 추가
- `references/version-sync.md`: v2.1.140 변경사항 추적 엔트리 추가

### Fixed
- `/goal` 명령 `disableAllHooks`/`allowManagedHooksOnly` 설정 시 무한 대기 → 명확한 메시지 표시 (v2.1.140)
- settings hot-reload 심볼릭 링크 설정 파일 변경 이벤트 오귀속·스퓨리어스 `ConfigChange` 훅 수정 (v2.1.140)
- `claude --bg` 백그라운드 서비스 유휴 종료 직전 "connection dropped mid-request" 오류 수정 (v2.1.140)
- Remote managed settings 401 시 force-refresh 토큰으로 1회 재시도 (v2.1.140)
- `/loop` 백그라운드 태스크 완료 알림 후 중복 wakeup 폴링 수정 (v2.1.140)
- `Read` 도구 `offset` 파라미터 공백 패딩·`+` 접두사 문자열 허용 (v2.1.140)
- `/clear` 후 MCP 서버(`.mcp.json`·플러그인·claude.ai 커넥터) 사라지는 버그 수정 (v2.1.136)
- Plan mode에서 매칭 `Edit(...)` allow 규칙 존재 시 파일 쓰기 차단 수정 (v2.1.136)

### Breaking Changes
- `worktree.baseRef` 기본값 `"fresh"` — `EnterWorktree`·`--worktree` 브랜치 기준이 `origin/<default>` (v2.1.133); 미푸시 커밋 유지 시 `"head"` 설정 필요

---

## [2.33.0] - 2026-05-03

### Added
- **Claude Code v2.1.126 sync**
  - `claude project purge [path]` — 프로젝트 전체 상태(트랜스크립트·태스크·파일 이력·설정 엔트리) 삭제; `--dry-run`, `-y/--yes`, `-i/--interactive`, `--all` 지원 (v2.1.126)
  - `/model` 피커에서 `ANTHROPIC_BASE_URL`이 Anthropic 호환 게이트웨이를 가리킬 때 `/v1/models` 엔드포인트 모델 목록 표시 (v2.1.126)
  - `claude auth login` OAuth 코드 터미널 직접 붙여넣기 지원 — 브라우저 콜백이 localhost에 도달 불가한 WSL2·SSH·컨테이너 환경 대응 (v2.1.126)
  - `claude_code.skill_activated` OpenTelemetry 이벤트 — 사용자 슬래시 명령 실행 시 발동; 신규 `invocation_trigger` 속성(`"user-slash"`, `"claude-proactive"`, `"nested-skill"`) 추가 (v2.1.126)
  - Auto mode: 권한 확인이 멈출 때 스피너가 빨간색으로 전환 — 도구 실행 중으로 오인 방지 (v2.1.126)
  - `--dangerously-skip-permissions` 확장 — `.claude/`, `.git/`, `.vscode/`, 셸 설정 파일 쓰기 프롬프트 생략 (재앙적 명령은 계속 프롬프트, v2.1.126)
  - Windows: Microsoft Store·PATH 미등록 MSI·`.NET global tool` 경로의 PowerShell 7 자동 탐지; PowerShell 도구 활성화 시 기본 셸로 사용 (v2.1.126)
  - `ANTHROPIC_BEDROCK_SERVICE_TIER` 환경변수 — Bedrock 서비스 티어 선택(`default`·`flex`·`priority`); `X-Amzn-Bedrock-Service-Tier` 헤더로 전송 (v2.1.122)
  - `/resume` 검색창에 PR URL 붙여넣기 시 해당 PR을 생성한 세션 자동 탐색 (GitHub·GitHub Enterprise·GitLab·Bitbucket, v2.1.122)
  - OpenTelemetry `claude_code.at_mention` 로그 이벤트 — `@`-멘션 해결 추적 (v2.1.122)
  - `/mcp` — 중복 URL 수동 서버로 숨겨진 claude.ai 커넥터 표시 + 중복 제거 힌트 (v2.1.122)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.121 → v2.1.126 업데이트
  - CLI 섹션: `claude project purge`, `/model` 게이트웨이 모델 목록, `claude auth login` OAuth 코드 붙여넣기, Windows PowerShell 기본 셸 추가
  - env 섹션: `ANTHROPIC_BEDROCK_SERVICE_TIER` 추가
  - Hooks 섹션: `claude_code.skill_activated` `invocation_trigger` 속성 및 보안 수정 추가
- `references/version-sync.md`: v2.1.126 변경사항 추적 엔트리 추가

### Fixed
- **Security**: `allowManagedDomainsOnly`·`allowManagedReadPathsOnly` — 상위 우선순위 관리형 설정 소스에 `sandbox` 블록 없을 때 무시되던 버그 수정 (v2.1.126)
- 2000px 초과 이미지 붙여넣기 시 세션 중단 → 자동 다운스케일·히스토리 과대 이미지 자동 제거·재시도 (v2.1.126)
- `context: fork` 스킬·서브에이전트 첫 턴에 지연 로드 도구(WebSearch·WebFetch 등) 누락 수정 (v2.1.126)
- Windows CJK(일본어·한국어·중국어) 텍스트 no-flicker 모드에서 깨진 문자 표시 수정 (v2.1.126)
- `Ctrl+L` 프롬프트 입력 클리어 → 화면 강제 재드로우만 수행 (readline 동작 일치, v2.1.126)
- Mac 수면 해제 후 "Stream idle timeout" 오류; 백그라운드·원격 세션 긴 모델 thinking 중 잘못된 타임아웃 중단 수정 (v2.1.126)
- OAuth 로그인 타임아웃 — slow·proxy 연결·IPv6-only devcontainer·WSL2 브라우저 콜백 실패 환경 수정 (v2.1.126)
- Agent SDK — 병렬 도구 호출 배치에서 잘못된 도구 이름 방출 시 hang 수정 (v2.1.126)
- `/plan` 모드 도구 — `--channels` 옵션 인터랙티브 세션에서 사용 불가 수정 (v2.1.126)
- ToolSearch — 비차단(nonblocking) 모드에서 세션 시작 후 연결된 MCP 도구 누락 수정 (v2.1.122)
- settings.json 잘못된 훅 항목 시 전체 파일 무효화되던 버그 수정 (v2.1.122)
- OAuth 인증 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 설정 시 401 루프 수정 (v2.1.123)

---

## [2.32.0] - 2026-04-28

### Added
- **Claude Code v2.1.121 sync**
  - `alwaysLoad` MCP 서버 옵션 — 해당 서버 모든 도구의 tool-search 지연 비활성화; 항상 사용 가능 상태 유지 (v2.1.121)
  - MCP 서버 시작 일시 오류 시 최대 3회 자동 재시도 (이전: 연결 끊긴 채 유지, v2.1.121)
  - `claude plugin prune` 서브커맨드 — 고아 자동 설치 플러그인 의존성 제거; `plugin uninstall --prune` 연쇄 삭제 (v2.1.121)
  - `/skills` 필터 검색박스 — 긴 스킬 목록에서 타이핑으로 검색, 스크롤 불필요 (v2.1.121)
  - PostToolUse hooks `hookSpecificOutput.updatedToolOutput` — 이제 모든 도구에서 tool output 교체 지원 (기존 MCP 전용→전체 확장, v2.1.121)
  - `--dangerously-skip-permissions` 모드에서 `.claude/skills/`, `.claude/agents/`, `.claude/commands/` 쓰기 프롬프트 생략 (v2.1.121)
  - SDK `mcp_authenticate`에 `redirectUri` 파라미터 추가 — 커스텀 스킴 완료 및 claude.ai 커넥터 지원 (v2.1.121)
  - Vertex AI: X.509 인증서 기반 Workload Identity Federation (mTLS ADC) 지원 (v2.1.121)
  - OpenTelemetry: LLM request span에 `stop_reason`, `gen_ai.response.finish_reasons`, `user_system_prompt`(`OTEL_LOG_USER_PROMPTS` 게이팅) 필드 추가 (v2.1.121)
  - Windows: Git Bash 불필요 — 미설치 시 Claude Code가 PowerShell을 셸 도구로 자동 사용 (v2.1.120)
  - `claude ultrareview [target]` CLI 서브커맨드 — CI·스크립트에서 `/ultrareview` 비대화형 실행; `--json` raw output; exit 0/1 (v2.1.120)
  - `${CLAUDE_EFFORT}` — Skill 콘텐츠에서 현재 effort 레벨 동적 참조 (v2.1.120)
  - `AI_AGENT` 환경변수 서브프로세스 자동 설정 — `gh` CLI 등이 Claude Code 트래픽 자동 귀속 (v2.1.120)
  - `claude plugin validate` — `marketplace.json` 최상위 `$schema`·`version`·`description`, `plugin.json` `$schema` 키 허용 (v2.1.120)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.119 → v2.1.121 업데이트
  - MCP 섹션: `alwaysLoad` 옵션, 시작 자동 재시도 추가
  - Hooks 섹션: PostToolUse `updatedToolOutput` 전체 도구 확장 추가
  - CLI 섹션: Windows Git Bash 불필요, `claude ultrareview` CLI, `AI_AGENT` env var 추가
  - Plugin 섹션: `plugin prune`, `plugin validate` 개선, `${CLAUDE_EFFORT}`, `/skills` 검색박스 추가
- `references/version-sync.md`: v2.1.121 변경사항 추적 엔트리 추가
- `references/hooks-guide.md`: PostToolUse `updatedToolOutput` 전체 도구 지원 업데이트
- `references/mcp-guide.md`: `alwaysLoad` 옵션, MCP 서버 자동 재시도 추가

### Fixed
- 다수 이미지 세션 멀티-GB 메모리 무제한 증가 수정 (v2.1.121)
- `/usage` 대용량 트랜스크립트 시스템 ~2GB 메모리 누수 수정 (v2.1.121)
- Bash 도구 시작 디렉토리 삭제·이동 시 영구 비활성화 버그 수정 (v2.1.121)
- `--resume` 비정상 종료로 손상된 트랜스크립트 라인 건너뛰기 (v2.1.121)
- Esc 중 stdio MCP 도구 호출 시 서버 연결 전체 종료 버그 수정 (v2.1.120)

---

## [2.31.0] - 2026-04-26

### Added
- **Claude Code v2.1.119 sync**
  - `/config` 설정(테마, 에디터 모드 등)이 `~/.claude/settings.json`에 영속 저장되며 프로젝트/로컬/정책 우선순위 계층 참여 (v2.1.119)
  - `prUrlTemplate` 설정 — PR 배지 푸터를 커스텀 코드리뷰 URL로 지정 (v2.1.119)
  - `CLAUDE_CODE_HIDE_CWD` 환경변수 — 시작 로고에서 작업 디렉토리 숨김 (v2.1.119)
  - `--from-pr` GitLab MR·Bitbucket PR·GitHub Enterprise URL 지원 (v2.1.119)
  - `--print` 모드에서 agent `tools:`/`disallowedTools:` frontmatter 준수 — 인터랙티브 모드와 동일 동작 (v2.1.119)
  - `--agent <name>` built-in agent의 `permissionMode` frontmatter 준수 (v2.1.119)
  - PowerShell 도구 명령 자동 승인 — Bash와 동일 권한 모드 동작 (v2.1.119)
  - Hooks: `PostToolUse`·`PostToolUseFailure` 입력에 `duration_ms`(도구 실행 시간, 권한 프롬프트·PreToolUse 제외) 필드 추가 (v2.1.119)
  - 서브에이전트·SDK MCP 서버 재구성 시 병렬 연결 — 직렬 연결 대비 기동 속도 개선 (v2.1.119)
  - Plugins: 다른 플러그인 버전 제약으로 핀된 플러그인 만족하는 최고 git 태그로 자동 업데이트 (v2.1.119)
  - Status line stdin JSON에 `effort.level`·`thinking.enabled` 필드 추가 (v2.1.119)
  - vim visual mode `v`/visual-line mode `V` — 선택·연산자·시각적 피드백 지원 (v2.1.118)
  - `/usage` 신규 — `/cost`와 `/stats` 통합 (v2.1.118)
  - Custom themes — `/theme` 명령으로 생성·전환; `~/.claude/themes/` JSON 파일 편집; 플러그인 `themes/` 디렉토리 배포 지원 (v2.1.118)
  - Hooks → MCP 도구 직접 실행 (`type: "mcp_tool"` 훅 타입 추가) (v2.1.118)
  - `DISABLE_UPDATES` 환경변수 — 수동 `claude update` 포함 전체 업데이트 경로 차단 (v2.1.118)
  - `wslInheritsWindowsSettings` 정책 키 — WSL에서 Windows 측 managed settings 상속 (v2.1.118)
  - Auto mode `"$defaults"` — `autoMode.allow`·`soft_deny`·`environment`에 내장 목록 유지하며 커스텀 규칙 추가 (v2.1.118)
  - `claude plugin tag` 명령 — 버전 검증 포함 플러그인 릴리스 git 태그 생성 (v2.1.118)
  - Forked subagents 외부 빌드 활성화 `CLAUDE_CODE_FORK_SUBAGENT=1` (v2.1.117)
  - Agent frontmatter `mcpServers` — `--agent` 세션에서 MCP 서버 로드 지원 (v2.1.117)
  - `/model` 선택 영속화 — 재시작 후에도 유지; 시작 헤더에 모델 출처(project/managed pin) 표시 (v2.1.117)
  - `/resume` 대용량 오래된 세션 요약 제안 (v2.1.117)
  - Native builds(macOS/Linux) Glob·Grep → 내장 `bfs`·`ugrep` 전환 (v2.1.117)
  - Pro/Max 구독자 Opus 4.6·Sonnet 4.6 기본 effort `high`으로 상향 (v2.1.117)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.114 → v2.1.119 업데이트
  - MCP 섹션: Hook → MCP 직접 호출, 서브에이전트·SDK 병렬 연결 추가
  - Hooks 섹션: `duration_ms` 필드, `mcp_tool` 타입 추가
  - Agent/CLI 섹션: `--from-pr` 멀티플랫폼, `/usage` 통합, custom themes, `DISABLE_UPDATES`, `wslInheritsWindowsSettings`, `plugin tag`, status line 필드, PowerShell 자동 승인, vim visual mode 추가
  - Breaking Changes: `--print` frontmatter 준수, vim INSERT Esc 변경 추가
- `references/version-sync.md`: v2.1.119 변경사항 추적 엔트리 추가
- `references/hooks-guide.md`: `duration_ms` 필드, `mcp_tool` 훅 타입 추가
- `references/official/hooks.md`: `mcp_tool` 훅 타입 추가

---

## [2.30.0] - 2026-04-18

### Added
- **Claude Code v2.1.114 sync**
  - CLI 네이티브 바이너리 스폰으로 전환 — 번들 JS 대신 플랫폼별 optional dependency 실행 (v2.1.113)
  - `sandbox.network.deniedDomains` 설정 — 광역 허용 도메인 와일드카드 내 특정 도메인 차단 가능 (v2.1.113)
  - Claude Opus 4.7 `xhigh` effort 레벨 — high~max 사이; `/effort`, `--effort`, 모델 피커에서 설정 가능 (v2.1.111)
  - Auto mode — Max 구독자 Opus 4.7 지원; `--enable-auto-mode` 플래그 불필요 (v2.1.111)
  - `/effort` 인터랙티브 슬라이더 — 인자 없이 호출 시 화살표 키 탐색, Enter 확인 (v2.1.111)
  - "Auto (match terminal)" 테마 옵션 — 터미널 dark/light 모드 자동 매칭 (v2.1.111)
  - `/ultrareview` 명령 — 클라우드 병렬 멀티에이전트 코드리뷰; 인자 없으면 현재 브랜치, `/ultrareview <PR#>`으로 특정 PR 리뷰 (v2.1.111)
  - `/less-permission-prompts` 스킬 — 읽기 전용 Bash·MCP 도구 트랜스크립트 스캔 후 `.claude/settings.json` 허용 리스트 자동 제안 (v2.1.111)
  - `/tui` 명령 및 `tui` 설정 — 같은 대화 내에서 플리커 없는 풀스크린 렌더링 전환 (v2.1.110)
  - `/focus` 명령 — 포커스 뷰 별도 토글 (`Ctrl+O`는 verbose transcript 전용으로 분리, v2.1.110)
  - Push notification tool — Remote Control + "Push when Claude decides" 설정 시 모바일 푸시 알림 전송 (v2.1.110)
  - `autoScrollEnabled` 설정 — 풀스크린 모드 자동 스크롤 비활성화 (v2.1.110)
  - `OTEL_LOG_RAW_API_BODIES` 환경 변수 — API 요청·응답 전체 본문 OTEL 로그 이벤트 출력 (v2.1.111)
  - `CLAUDE_CODE_USE_POWERSHELL_TOOL` — PowerShell 도구 옵트인 (Linux/macOS: `=1`, Windows 점진적 배포, v2.1.111)
  - plan 파일 프롬프트 기반 이름 자동 생성 (예: `fix-auth-race-snug-otter.md`, v2.1.111)
  - Esc로 `/loop` 대기 wakeup 취소; wakeup 메시지 "Claude resuming /loop wakeup" 표시 (v2.1.113)
  - 서브에이전트 스트림 정지 시 10분 후 명확한 오류 반환 — 무한 행 방지 (v2.1.113)
  - `/extra-usage`, Remote Control `@`-파일 자동완성 지원 (v2.1.113)
  - `--resume`/`--continue` 만료 미경과 예약 작업 복원 (v2.1.110)
  - `/context`, `/exit`, `/reload-plugins` Remote Control 지원 (v2.1.110)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.109 → v2.1.114 업데이트
  - CLI 섹션: 네이티브 바이너리, xhigh effort, auto mode 플래그 불필요, `/tui`·`/focus`·`/ultrareview`·`/less-permission-prompts`, plan 파일 이름, `/loop` Esc 취소, 서브에이전트 타임아웃, `Ctrl+U` 변경 추가
  - Agent Teams 섹션: v2.1.114 권한 다이얼로그 크래시 수정 추가
  - 신규 명령: `/tui`, `/focus`, `/ultrareview`, `/less-permission-prompts` 추가
  - 신규 도구·env: `sandbox.network.deniedDomains`, `autoScrollEnabled`, `OTEL_LOG_RAW_API_BODIES`, `CLAUDE_CODE_USE_POWERSHELL_TOOL` 추가
  - Breaking Changes: Bash deny 규칙 강화(env/sudo 래퍼), `Bash(find:*)` -exec 자동 승인 차단, macOS /private/ 위험 경로, `Ctrl+U` 변경 추가
- `references/version-sync.md`: v2.1.114 변경사항 추적 엔트리 추가

### Security
- Bash deny 규칙이 env/sudo/watch/ionice/setsid 래퍼로 감싼 명령도 매칭 (v2.1.113)
- `Bash(find:*)` allow 규칙이 `find -exec`/`-delete` 자동 승인 불가 (v2.1.113)
- macOS `/private/{etc,var,tmp,home}` 경로를 `Bash(rm:*)` 위험 경로로 처리 (v2.1.113)
- Bash 멀티라인 첫 줄 주석 시 전체 명령 트랜스크립트 표시 — UI 스푸핑 차단 (v2.1.113)

---

## [2.29.0] - 2026-04-15

### Added
- **Claude Code v2.1.109 sync**
  - extended-thinking 표시기 로테이팅 진행 힌트 개선 (v2.1.109)
  - `ENABLE_PROMPT_CACHING_1H` env var — API key·Bedrock·Vertex·Foundry 1시간 프롬프트 캐시 TTL 옵트인; `FORCE_PROMPT_CACHING_5M` — 5분 TTL 강제 (v2.1.108)
  - `/recap` 명령 — 세션 복귀 시 컨텍스트 요약 제공; `/config`에서 설정, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`로 강제 활성화 (v2.1.108)
  - Skill tool로 내장 슬래시 명령 자동 탐색·실행 지원 (`/init`, `/review`, `/security-review`, v2.1.108)
  - `/undo` — `/rewind` 별칭 추가 (v2.1.108)
  - `/model` 전환 전 미캐시 경고 — 다음 응답이 전체 히스토리 미캐시로 읽힘 안내 (v2.1.108)
  - `/resume` 피커 현재 디렉토리 세션 기본 표시; `Ctrl+A`로 전체 프로젝트 표시 (v2.1.108)
  - 오류 메시지 개선: 서버 rate limit vs plan 사용 한도 구분; 5xx/529 오류 → status.claude.com 링크; 미지원 슬래시 명령 유사어 제안 (v2.1.108)
  - 언어 문법 온디맨드 로드 — 파일 읽기·편집·구문 강조 메모리 절약 (v2.1.108)
  - 상세 트랜스크립트(`Ctrl+O`) "verbose" 표시기 추가 (v2.1.108)
  - `DISABLE_PROMPT_CACHING*` env var 설정 시 시작 경고 (v2.1.108)
  - 다수 버그 수정: `/login` 코드 입력 붙여넣기, 텔레메트리 비활성화 시 캐시 TTL 폴백, `CLAUDE_ENV_FILE` `#` 주석 줄 처리, `--resume` 세션 이름·색상 유실, `/feedback` Enter 재제출, 다이어크리틱 문자 응답 누락, 정책 플러그인 자동 업데이트 등 (v2.1.108)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.107 → v2.1.109 업데이트
  - CLI 섹션: Skill tool 내장 슬래시 명령 지원, `/model` 경고, `/resume` 피커 개선, 오류 메시지 개선, thinking 힌트 추가
  - 신규 명령: `/recap`, `/undo` 추가
  - 신규 도구·env: `ENABLE_PROMPT_CACHING_1H`, `FORCE_PROMPT_CACHING_5M`, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY` 추가
- `references/version-sync.md`: v2.1.109 변경사항 추적 엔트리 추가

---

## [2.28.0] - 2026-04-14

### Added
- **Claude Code v2.1.107 sync**
  - 긴 작업 중 thinking 힌트를 더 빨리 표시 (v2.1.107)
  - `PreCompact` Hook 차단 지원 — exit code 2 또는 `{"decision":"block"}` 반환으로 컨텍스트 압축 차단 가능 (v2.1.105)
  - 플러그인 `monitors` 매니페스트 최상위 키 — 세션 시작 또는 스킬 invoke 시 백그라운드 모니터 자동 실행 (v2.1.105)
  - `EnterWorktree` `path` 파라미터 — 현재 레포의 기존 worktree로 전환 (v2.1.105)
  - `/proactive` — `/loop` 별칭 추가 (v2.1.105)
  - 스킬 설명 최대 길이 250 → 1,536자 확대; 초과 시 시작 경고 (v2.1.105)
  - `WebFetch` `<style>`·`<script>` 태그 내용 제거 — CSS/JS 헤비 페이지 컨텍스트 예산 보호 (v2.1.105)
  - 스트림 5분 무응답 시 자동 중단 후 non-streaming 재시도 (v2.1.105)
  - 네트워크 오류 즉시 재시도 메시지 표시 (v2.1.105)
  - MCP 대용량 출력 truncation 프롬프트 — JSON(`jq`), 텍스트(청크 크기 계산) 등 포맷별 처리 레시피 제공 (v2.1.105)
  - `/doctor` 레이아웃 개선: 상태 아이콘 표시, `f` 키로 Claude 자동 수정 (v2.1.105)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.101 → v2.1.107 업데이트
  - Hook 인라인 노트: v2.1.105 `PreCompact` 차단 지원 추가
  - Plugin 섹션: `monitors` 매니페스트 키, 스킬 설명 길이 확대 추가
  - 신규 명령: `/proactive` 별칭 추가
  - 신규 도구·env: `EnterWorktree` path 파라미터, `WebFetch` 개선 추가
- `references/version-sync.md`: v2.1.107 변경사항 추적 엔트리 추가

---

## [2.27.0] - 2026-04-12

### Added
- **Claude Code v2.1.101 sync**
  - `/team-onboarding` 명령 — 로컬 Claude Code 사용 이력 기반 팀원 온보딩 가이드 자동 생성
  - OS CA 인증서 저장소 기본 신뢰 — 엔터프라이즈 TLS 프록시 별도 설정 불필요 (`CLAUDE_CODE_CERT_STORE=bundled`로 번들 CA만 사용 가능)
  - `/ultraplan` 및 원격 세션 기능: 웹 설정 없이 기본 클라우드 환경 자동 생성
  - settings.json 복원력 개선 — 알 수 없는 훅 이벤트 이름이 전체 파일 무시를 유발하지 않음
  - `permissions.deny` 규칙이 `PreToolUse` hook의 `permissionDecision: "ask"` 다운그레이드를 방지하도록 수정
  - `claude -p --resume <name>` — `/rename` 또는 `--name`으로 설정한 세션 제목으로 재개 지원
  - SDK `query()` — `for await` break 또는 `await using` 시 서브프로세스·임시 파일 자동 정리
- **Claude Code v2.1.98 sync**
  - Google Vertex AI 인터랙티브 설정 마법사 — 로그인 화면 "3rd-party platform"에서 GCP 인증·프로젝트·리전·자격증명 검증·모델 핀닝 단계별 안내
  - `CLAUDE_CODE_PERFORCE_MODE` env var — 읽기 전용 파일 편집 시 `p4 edit` 힌트 출력
  - `Monitor` 도구 — 백그라운드 스크립트 이벤트 스트리밍
  - Linux 서브프로세스 샌드박싱 PID 네임스페이스 격리 (`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 설정 시)
  - `--exclude-dynamic-system-prompt-sections` print mode 플래그 — 크로스유저 프롬프트 캐시 개선
  - `workspace.git_worktree` status line JSON 입력 필드 — linked git worktree 내부에서 설정
  - Bash 도구 서브프로세스에 W3C `TRACEPARENT` env var 주입 (OTEL 추적 활성화 시)
  - LSP: `clientInfo` 필드로 언어 서버에 Claude Code 신원 전달 (`initialize` 요청)
  - Bash 도구 권한 강화 — 백슬래시 이스케이프 플래그 우회·복합 명령·env-var 접두사·네트워크 리다이렉트 등 다수 수정
- **Claude Code v2.1.97 sync**
  - focus view 토글 (`Ctrl+O`, `NO_FLICKER` 모드) — 프롬프트·도구 요약·최종 응답만 표시
  - `refreshInterval` status line 설정 — N초마다 status line 명령 재실행
  - `/agents` 화면: 실행 중인 서브에이전트 타입별 `● N running` 표시
  - Cedar 정책 파일 (`.cedar`, `.cedarpolicy`) 구문 강조 지원
- **Claude Code v2.1.94 sync**
  - `CLAUDE_CODE_USE_MANTLE=1` — Amazon Bedrock powered by Mantle 지원
  - Slack MCP send-message 도구 호출에 `Slacked #channel` 헤더 + 클릭 링크 표시
  - `keep-coding-instructions` frontmatter 필드 — 플러그인 output style 유지
  - `hookSpecificOutput.sessionTitle` — `UserPromptSubmit` Hook에서 세션 제목 설정
  - `"skills": ["./"]` 선언 시 frontmatter `name` 필드로 호출명 결정 (설치 방식 무관 일관된 이름)
  - 기본 effort 레벨 medium → **high** 전환 (API키·Bedrock·Vertex·Foundry·Team·Enterprise 사용자)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.92 → v2.1.101 업데이트
  - CLI 명령: `/team-onboarding` 추가
  - 신규 도구·env: `Monitor`, `CLAUDE_CODE_PERFORCE_MODE`, `CLAUDE_CODE_USE_MANTLE`, `refreshInterval`, `workspace.git_worktree`, `--exclude-dynamic-system-prompt-sections`, `CLAUDE_CODE_CERT_STORE` 추가
  - Plugin 섹션: `keep-coding-instructions`, `"skills": ["./"]` name 결정 방식 추가
  - Hook 인라인 노트: v2.1.94 `hookSpecificOutput.sessionTitle`, v2.1.101 settings resilience 추가
  - Breaking Changes: 기본 effort high 전환 추가
- `references/version-sync.md`: v2.1.101 변경사항 추적 엔트리 추가

### Fixed (Claude Code v2.1.101 주요 수정)
- LSP binary 탐지 POSIX `which` 폴백 명령 인젝션 취약점 수정 (보안)
- 장기 세션 메모리 누수 — 가상 스크롤러가 수십 개의 메시지 목록 사본 유지하던 문제 수정
- `--resume`/`--continue` 대용량 세션에서 대화 컨텍스트 유실 수정
- `--resume` 체인 복구 시 서브에이전트 대화로 잘못 브리지되던 버그 수정
- 서브에이전트가 동적 주입 MCP 서버의 도구를 상속받지 못하던 버그 수정
- 격리된 worktree에서 실행 중인 서브에이전트가 자신의 worktree 내 파일 Read/Edit 거부되던 버그 수정
- 하드코딩된 5분 요청 타임아웃 수정 — `API_TIMEOUT_MS` 설정 값 적용
- Grep 도구 내장 ripgrep 바이너리 경로 stale 시 ENOENT 오류 → 시스템 `rg` 폴백 후 자동 복구
- plugin `context: fork`·`agent` frontmatter 미적용, 슬래시 명령 중복 `name:` 오해석 등 다수 수정
- Bedrock SigV4 인증 — Authorization 헤더 설정 시 403 오류 수정

---

## [2.26.0] - 2026-04-07

### Added
- **Claude Code v2.1.92 sync**
  - `forceRemoteSettingsRefresh` 정책 설정 — CLI 시작 시 원격 managed settings 최신화 강제; 가져오기 실패 시 종료 (fail-closed)
  - Bedrock 인터랙티브 설정 마법사 — 로그인 화면 "3rd-party platform"에서 AWS 인증·리전·자격증명 검증·모델 핀닝 단계별 가이드
  - `/cost` 구독 사용자 대상 모델별·캐시 히트 별 비용 세부 내역
  - `/release-notes` 인터랙티브 버전 피커로 전환
  - Remote Control 세션 이름 호스트명 기반 기본 접두사; `--remote-control-session-name-prefix`로 오버라이드 가능
  - Pro 사용자 프롬프트 캐시 만료 후 세션 복귀 시 미캐시 토큰 수 푸터 힌트 표시
- **Claude Code v2.1.91 sync**
  - MCP 도구 결과 크기 오버라이드 — `_meta["anthropic/maxResultSizeChars"]` 어노테이션으로 최대 500K 결과 전달 (DB 스키마 등 대용량 데이터)
  - `disableSkillShellExecution` 설정 — Skills/슬래시 명령/플러그인 명령 인라인 셸 실행 비활성화
  - 플러그인 `bin/` 디렉토리 실행 파일 지원 — Bash 도구에서 bare command로 직접 실행
  - `claude-cli://open?q=` 딥 링크 멀티라인 프롬프트 지원 (`%0A` 인코딩된 개행 허용)
  - Edit 도구 `old_string` 앵커 단축 — 출력 토큰 절감

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.90 → v2.1.92 업데이트
  - MCP 테이블: `_meta["anthropic/maxResultSizeChars"]` 결과 크기 오버라이드 추가
  - Plugin 섹션: `bin/` 실행 파일·`disableSkillShellExecution` 추가
  - CLI/env 섹션: `forceRemoteSettingsRefresh`·`--remote-control-session-name-prefix` 추가
  - Hook 인라인 노트: v2.1.92 Stop Hook 수정 사항 추가
  - Breaking Changes: `/tag`·`/vim` 명령 제거 추가
- `references/version-sync.md`: v2.1.92 변경사항 추적 엔트리 추가
- `references/mcp-guide.md`: MCP 도구 결과 크기 오버라이드 섹션 추가

### Fixed (Claude Code v2.1.92 주요 수정)
- 서브에이전트 생성 시 tmux 창 종료/번호 변경 후 "Could not determine pane count" 오류로 영구 실패하던 버그 수정
- prompt-type Stop Hook에서 소형 빠른 모델이 `ok:false` 반환 시 잘못 실패하던 버그; `preventContinuation:true` 시맨틱 복원
- 스트리밍 시 배열/객체 필드가 JSON 인코딩 문자열로 전달될 때 도구 입력 검증 실패 수정
- 확장 사고 중 공백 텍스트 블록 생성 시 API 400 오류 수정
- Write 도구 대용량 파일 diff 계산 속도 60% 향상 (탭/`&`/`$` 포함 파일)
- 플러그인 MCP 서버가 미인증 claude.ai 커넥터와 중복 시 "connecting" 상태로 멈추는 버그 수정
- Linux sandbox `apply-seccomp` 헬퍼 npm·네이티브 빌드 모두 포함 (유닉스 소켓 차단 복원)

### Fixed (Claude Code v2.1.91 주요 수정)
- `--resume` 시 비동기 트랜스크립트 쓰기 실패로 대화 이력 유실되던 트랜스크립트 체인 끊김 수정
- plan mode 컨테이너 재시작 후 원격 세션에서 플랜 파일 추적 상실 → 권한 프롬프트·빈 플랜 승인 모달 수정

---

## [2.25.0] - 2026-04-02

### Added
- **Claude Code v2.1.90 sync**
  - `/powerup` 명령 — 애니메이션 데모와 함께 Claude Code 기능을 인터랙티브하게 학습
  - `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` env var — git pull 실패 시 기존 마켓플레이스 캐시 유지 (오프라인 환경용)
  - `.husky` 디렉토리를 acceptEdits 모드 보호 목록에 추가

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.89 → v2.1.90 업데이트
  - 신규 명령: `/powerup` 추가
  - 신규 env: `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` 추가
  - Breaking Changes: `--resume` picker `claude -p`/SDK 세션 제외; DNS 캐시 명령 자동 허용 제거 추가
- `references/version-sync.md`: v2.1.90 변경사항 추적 엔트리 추가

### Fixed (Claude Code v2.1.90 주요 수정)
- Rate-limit 옵션 다이얼로그 무한 반복 자동 재오픈 후 세션 크래시 수정
- `--resume` 사용 시 deferred tools/MCP/커스텀 에이전트 포함 세션 첫 요청 프롬프트 캐시 미스 수정 (v2.1.69 이후 회귀)
- PostToolUse format-on-save Hook이 연속 편집 사이에 파일 재작성 시 Edit/Write "File content has changed" 오류 수정
- JSON 출력 + exit code 2로 종료하는 `PreToolUse` Hook이 도구 호출을 올바르게 차단하지 않던 버그 수정
- Auto mode가 명시적 사용자 경계("don't push", "wait for X before Y")를 무시하던 버그 수정
- PowerShell 도구 권한 검사 강화: trailing `&` 백그라운드 작업 우회, `-ErrorAction Break` 디버거 행, 아카이브 추출 TOCTOU, 파싱 실패 시 deny-rule 저하 수정
- MCP 도구 스키마 캐시 키 조회 시 매 턴 JSON.stringify 제거 (성능 개선)
- SSE transport 대용량 프레임 처리 선형 시간으로 개선 (기존 이차 시간)
- SDK 롱 세션 트랜스크립트 쓰기 이차 시간 저하 수정 (성능 개선)
- `/resume` all-projects 뷰 프로젝트 세션 병렬 로드 — 다수 프로젝트 사용자 로드 시간 개선

---

## [2.24.0] - 2026-04-01

### Added
- **Claude Code v2.1.89 sync**
  - `"defer"` 권한 결정 — `PreToolUse` Hook에서 헤드리스 세션의 도구 호출 일시 중지 후 `-p --resume`으로 Hook 재평가 가능
  - `MCP_CONNECTION_NONBLOCKING=true` — `-p` 모드에서 MCP 연결 대기 완전 생략; `--mcp-config` 서버 연결 최대 5s 제한
  - Auto mode 거부 명령 UX 개선 — 알림 표시 + `/permissions` → Recent 탭에서 `r`로 재시도 가능
  - Hook 출력 50K 초과 시 디스크 저장 — 파일 경로 + 미리보기를 컨텍스트에 주입 (컨텍스트 팽창 방지)
  - `TaskCreated` Hook 이벤트 차단 동작(blocking behavior) 공식 문서화
  - `Edit` 도구가 `Bash`에서 `sed -n`/`cat`으로 확인한 파일에도 별도 `Read` 없이 동작

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.88 → v2.1.89 업데이트
  - Hook 인라인 노트: v2.1.89 `"defer"` 권한 결정 및 Hook 출력 50K 디스크 저장 추가
  - Breaking Changes: `cleanupPeriodDays: 0` 검증 오류 추가
  - CLI: auto mode 거부 명령 알림·Recent 탭 추가
  - 신규 env: `MCP_CONNECTION_NONBLOCKING=true` 추가
- `references/hooks-guide.md`: PreToolUse `"defer"` 권한 결정 추가
- `references/official/hooks.md`: PreToolUse `"defer"` 권한 결정 추가
- `references/mcp-guide.md`: `MCP_CONNECTION_NONBLOCKING=true` 추가
- `references/version-sync.md`: v2.1.89 변경사항 추적 엔트리 추가

### Fixed (Claude Code v2.1.89 주요 수정)
- Edit/Write 도구 Windows CRLF 이중 변환 및 Markdown 하드 라인 브레이크(두 개 공백) 제거 수정
- `-p --resume` 64KB 초과 입력 또는 deferred 마커 없을 때 행어 수정
- `autocompact` 쓰레싱 루프 — 압축 후 즉시 컨텍스트 재충전 시 3회 반복 감지 후 명확한 오류로 중단
- 롱 세션에서 중첩 CLAUDE.md 파일 수십 번 재주입 버그 수정
- 프롬프트 히스토리 CJK/이모지 항목 4KB 경계에서 유실 버그 수정 (`~/.claude/history.jsonl`)
- `/stats` 서브에이전트 토큰 미집계 및 30일 초과 이력 손실 수정
- "Rate limit reached" 오해 메시지 — entitlement 오류를 실제 원인 + actionable 힌트로 표시
- 대형 세션 파일(50MB+) 메시지 삭제 시 크래시 수정
- LSP 서버 좀비 상태 — 크래시 후 다음 요청 시 자동 재시작

---

## [2.23.0] - 2026-03-31

### Added
- **Claude Code v2.1.88 sync**
  - `PermissionDenied` Hook 이벤트 — auto mode 분류기 거부 후 발동, `{retry: true}` 반환 시 모델 재시도 가능 (v2.1.88)
  - `CLAUDE_CODE_NO_FLICKER=1` env var — 플리커 없는 alt-screen 렌더링 (가상 스크롤백 포함) (v2.1.88)
  - Named subagents — `@` 멘션 타입어헤드에 Named Subagent 포함 (v2.1.88)
  - `X-Claude-Code-Session-Id` 헤더 — API 요청에 세션 ID 포함, 프록시 세션별 집계 지원 (v2.1.86)
  - `.jj`, `.sl` VCS 메타데이터 디렉토리를 Grep 및 파일 자동완성에서 제외 (v2.1.86)

### Changed
- SKILL.md: 핵심 변경 사항 섹션 v2.1.85 → v2.1.88 업데이트
  - 신규 Hook 이벤트: `PermissionDenied` 추가 (총 25개)
  - Hook 인라인 노트: v2.1.88 내용 추가 (PermissionDenied, 복합 명령 `if` 조건 수정)
  - Breaking Changes: `showThinkingSummaries` 기본값 비활성화 추가
  - CLI/env: `CLAUDE_CODE_NO_FLICKER=1` 추가
- `references/hooks-guide.md`: `PermissionDenied` Hook 이벤트 행 추가
- `references/official/hooks.md`: `PermissionDenied` Hook 이벤트 (#25) 추가
- `references/version-sync.md`: v2.1.88 변경사항 추적 엔트리 추가

### Fixed (Claude Code v2.1.88 주요 수정)
- Hook `if` 조건 필터링 — 복합 명령(`ls && git push`) 및 env-var 접두사 명령 이제 올바르게 매칭
- `PreToolUse`/`PostToolUse` Hook에서 Write/Edit/Read 도구의 `file_path`를 절대 경로로 반환
- 프롬프트 캐시 미스 — 롱 세션 중 도구 스키마 바이트 변경으로 캐시 미스 발생하던 버그 수정
- `StructuredOutput` 스키마 캐시 버그 — 다중 스키마 워크플로우 ~50% 실패율 수정
- `--resume` 크래시 — 이전 버전 tool result 포함 트랜스크립트 처리 시 크래시 수정
- LSP 서버 좀비 상태 — 크래시 후 다음 요청 시 자동 재시작 (세션 재시작 불필요)
- 메모리 누수 — 대형 JSON 입력이 LRU 캐시 키로 유지되던 문제 수정
- v2.1.87: Cowork Dispatch 메시지 미전달 수정
- v2.1.86: `--resume` "tool_use ids without tool_result blocks" 오류 수정

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
