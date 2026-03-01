# Changelog - Claude Code Extension Builder

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.12.0] - 2026-03-01

### Added
- **Claude Code v2.1.63 동기화** (v2.1.53 → v2.1.63, 10개 버전 반영)
  - HTTP Hook 타입 추가: URL로 JSON POST/응답 수신 (shell 명령 대신 HTTP 엔드포인트 활용)
  - `ConfigChange` Hook 이벤트: 세션 중 설정 파일 변경 감지, 차단 가능 (v2.1.49에서 누락됨)
  - `/simplify`, `/batch` 번들 슬래시 명령 추가
  - `ENABLE_CLAUDEAI_MCP_SERVERS=false` 환경 변수로 claude.ai MCP 서버 비활성화
  - MCP OAuth 인증 시 수동 URL 붙여넣기 폴백 지원
  - 동일 저장소 git worktree 간 프로젝트 설정 및 auto memory 공유
  - `/copy` 명령에 "Always copy full response" 옵션 추가
  - `/model` 명령에 현재 활성 모델 표시
  - Auto memory 자동 저장 기능 강화 (`/memory`로 관리)
  - 다수 메모리 누수 수정 (MCP 서버 재연결, git root 감지, JSON 파싱 캐시 등)

### Changed
- `references/hooks-guide.md`: ConfigChange 이벤트 및 HTTP hook 타입 추가
- `references/official/hooks.md`: ConfigChange 이벤트 및 HTTP hook 타입 추가
- `references/mcp-guide.md`: ENABLE_CLAUDEAI_MCP_SERVERS 환경 변수 및 OAuth URL 폴백 추가
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
