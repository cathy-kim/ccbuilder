# Changelog - Claude Code Extension Builder

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.16.0] - 2026-03-13

### Added
- **Claude Code v2.1.74 동기화**
  - `/context` 명령 개선 — 컨텍스트 과다 도구, 메모리 팽창, 용량 경고에 대한 실행 가능한 최적화 제안
  - `autoMemoryDirectory` 설정 — Auto Memory 저장 디렉토리 커스텀 경로 지정
  - `modelOverrides` 설정 (v2.1.73) — 모델 픽커 항목을 커스텀 provider 모델 ID로 매핑 (Bedrock inference profile ARN 등)
  - `--plugin-dir` 동작 변경 — 로컬 개발 사본이 마켓플레이스 동명 플러그인 오버라이드 (managed settings 강제 활성화 제외)
  - `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 환경변수 — `SessionEnd` 훅 타임아웃 설정 (기존 1.5초 고정 → 가변, v2.1.74)
  - Agent frontmatter `model:` 필드에서 전체 모델 ID (`claude-opus-4-5` 등) 수용 — `--model` 과 동일한 값 허용 (v2.1.74)
  - SSL 인증서 오류 시 (기업 프록시, `NODE_EXTRA_CA_CERTS`) 실행 가능한 안내 메시지 (v2.1.73)

### Changed
- `SKILL.md`: 핵심 변경 사항 섹션 v2.1.72 → v2.1.74 업데이트
  - MCP 테이블: OAuth 콜백 포트 충돌 + 리프레시 토큰 만료 수정 추가
  - Memory 테이블: `autoMemoryDirectory` 설정 항목 추가
  - Agent/CLI 섹션: 전체 모델 ID 지원, `modelOverrides`, `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`, `--plugin-dir` 변경 반영
  - Deprecated 테이블: `/output-style` → `/config` 추가
- `references/version-sync.md`: v2.1.74 변경사항 추적 추가
- 버전: 2.15.0 → 2.16.0

### Fixed (Claude Code v2.1.74)
- 스트리밍 API 응답 버퍼 미해제로 인한 메모리 누수 (Node.js/npm 경로 RSS 무한 증가) 수정
- Managed policy `ask` 규칙이 user `allow` 규칙 또는 skill `allowed-tools`에 의해 우회되던 버그 수정
- MCP OAuth 콜백 포트 충돌 시 hang 수정
- MCP OAuth 리프레시 토큰 만료 후 HTTP 200 오류 응답 시 재인증 미프롬프트 수정
- macOS 네이티브 바이너리 voice mode 마이크 권한 silent fail 수정 (`audio-input` 엔타이틀먼트 추가)
- `SessionEnd` 훅이 `hook.timeout` 무시하고 1.5초 후 강제 종료되던 버그 수정
- `/plugin install` REPL 내부 실행 실패 수정
- 마켓플레이스 업데이트 시 git 서브모듈 미동기화 수정
- 알 수 없는 슬래시 명령에 인자 포함 시 입력 묵살 → 경고 메시지 표시로 변경
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
