# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-03-13
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
