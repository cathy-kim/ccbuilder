# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-03-06
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

### v2.1.70 (2026-03-06 동기화)

**새로운 기능:**
- `InstructionsLoaded` Hook 이벤트: CLAUDE.md 또는 `.claude/rules/*.md` 로드 시 발생 (v2.1.69) — Hook 이벤트 총 17개
- `${CLAUDE_SKILL_DIR}` 변수: Skill이 SKILL.md 내에서 자신의 디렉토리를 참조 (v2.1.69)
- Hook 이벤트에 `agent_id`, `agent_type` 필드 추가 (v2.1.69)
- Status line hook 커맨드에 `worktree` 필드 추가 (name, path, branch, original repo directory) (v2.1.69)
- `oauth.authServerMetadataUrl`: MCP OAuth 메타데이터 발견 URL 커스텀 설정 (v2.1.69)
- `includeGitInstructions` 설정 + `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 환경변수 (v2.1.69)
- `/reload-plugins` 커맨드: 재시작 없이 플러그인 활성화 (v2.1.69)
- `sandbox.enableWeakerNetworkIsolation` 설정 (macOS, Go 프로그램 TLS 인증 지원) (v2.1.69)
- Opus 4.6 Medium Effort 기본값 (Max/Team 구독자) (v2.1.68)
- "ultrathink" 키워드 복원 → 다음 턴 high effort (v2.1.68)
- VSCode: 네이티브 MCP 서버 관리 다이얼로그 (`/mcp`) (v2.1.70)
- VSCode: 스파크 아이콘 activity bar에 모든 Claude Code 세션 표시 (v2.1.70)

**Breaking Changes (v2.1.68):**
- Opus 4 및 Opus 4.1 Claude Code 1차 API에서 제거 → Opus 4.6으로 자동 전환

**주요 버그 수정:**
- `ANTHROPIC_BASE_URL` 프록시 사용 시 API 400 오류 수정 (tool_reference 블록 감지) (v2.1.70)
- ToolSearch 직후 빈 모델 응답 수정 (v2.1.70)
- `/resume` 시 skill listing 재주입 수정 (~600 토큰 절약) (v2.1.70)
- 조건부 `.claude/rules/*.md` 파일이 print 모드에서 로드되지 않는 문제 수정 (v2.1.69)
- Skill 설명에 콜론 포함 시 SKILL.md frontmatter 로드 실패 수정 (v2.1.69)
- `description:` frontmatter 없는 프로젝트 스킬이 목록에 표시 안 되는 문제 수정 (v2.1.69)
- TeammateIdle/TaskCompleted hook에서 `{"continue": false, "stopReason": "..."}` 지원 (v2.1.69)
- macOS 키체인 손상 (다중 OAuth MCP 서버) 수정 (v2.1.69)

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
