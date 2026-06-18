# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-06-18
**현재 지원 버전**: v2.1.181+ (SKILL.md v2.25.0)

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

### v2.1.181 (2026-06-18 동기화)

**새로운 기능:**
- `/config key=value` 문법 추가 — 프롬프트에서 모든 설정 즉시 변경 (interactive, `-p`, Remote Control 지원)
- `sandbox.allowAppleEvents` opt-in 설정 추가 (macOS 샌드박스 명령이 Apple Events 전송 허용)
- `CLAUDE_CLIENT_PRESENCE_FILE` 환경변수 추가 (마커 파일로 모바일 푸시 알림 억제)

**주요 버그 수정:**
- foreground subagent가 무제한 중첩 체인 생성하던 버그 수정 → background와 동일하게 5단계 깊이 제한 적용
- 커스텀 `ANTHROPIC_BASE_URL` / Foundry에서 prompt caching이 동작하지 않던 버그 수정
- `claude mcp get`/`list`가 tools/list 실패 시에도 `✓ Connected` 표시하던 버그 → `! Connected · tools fetch failed`로 수정

### v2.1.178 (2026-06-18 동기화)

**새로운 기능:**
- 권한 규칙에 `Tool(param:value)` 문법 추가 — 도구 입력 파라미터 매칭 (`*` 와일드카드), 예: `Agent(model:opus)`로 Opus subagent 차단
- 중첩 `.claude/skills` 디렉토리 스킬 자동 로드 — 이름 충돌 시 `<dir>:<name>`로 둘 다 유지
- 중첩 `.claude/`: 작업 디렉토리에 가장 가까운 agent/workflow/output-style이 이름 충돌 시 우선

**주요 버그 수정:**
- subagent `disallowedTools`에서 MCP 서버 레벨 스펙(`mcp__server`, `mcp__*`)이 무시되던 버그 수정
- compaction이 `--fallback-model`을 무시하던 버그 수정 (overload 시 fallback 체인으로 폴백)

### v2.1.176 (2026-06-18 동기화)

**새로운 기능:**
- `footerLinksRegexes` 설정 추가 (footer에 regex 매칭 링크 배지, user/managed settings 구성 가능)
- 세션 제목이 대화 언어로 생성 (`language` 설정으로 고정 가능)

**주요 버그 수정:**
- hook `if` 조건의 Read/Edit/Write 경로 패턴(`Edit(src/**)`, `Read(.env)` 등)이 올바르게 매칭되도록 수정
- `availableModels` 우회 차단 — alias 모델 선택이 `ANTHROPIC_DEFAULT_*_MODEL`로 차단 모델로 리다이렉트되지 않도록

### v2.1.175 / v2.1.172 (2026-06-18 동기화)

**새로운 기능:**
- `enforceAvailableModels` managed 설정 추가 (v2.1.175) — `availableModels` allowlist가 Default 모델까지 제약, user/project가 managed 리스트를 확장 불가
- Sub-agent가 자체 sub-agent를 spawn 가능 (최대 5단계 깊이) (v2.1.172)
- `model` 속성이 `claude_code.lines_of_code.count` OTEL 메트릭에 추가 (v2.1.172)

**주요 버그 수정:**
- `availableModels` 제약이 subagent 모델 override / agent dispatch 모델 picker / advisor 모델에 미적용되던 버그 수정 (v2.1.172)
- `WebFetch(domain:*.example.com)` 와일드카드 규칙이 서브도메인 매칭 안 되던 버그, mid-pattern 와일드카드 파일 규칙(`Read(secrets-*/config.json)`) 거부 버그 수정 (v2.1.172)

### v2.1.169 / v2.1.166 / v2.1.163 (2026-06-18 동기화)

**새로운 기능:**
- Self-hosted runner: `post-session` 라이프사이클 hook 추가 (세션 종료 후 workspace 삭제 전 실행) (v2.1.169)
- `--safe-mode` 플래그 + `CLAUDE_CODE_SAFE_MODE` 추가 — 모든 커스터마이징(CLAUDE.md, plugins, skills, hooks, MCP) 비활성화로 troubleshooting (v2.1.169)
- `/cd` 명령 추가 — 프롬프트 캐시 깨지 않고 작업 디렉토리 이동 (v2.1.169)
- `disableBundledSkills` 설정 + `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` 환경변수 추가 — 번들 스킬/워크플로우/빌트인 슬래시 커맨드 숨김 (v2.1.169)
- `fallbackModel` 설정 추가 — 최대 3개 fallback 모델 순서대로 시도 (v2.1.166)
- deny rule 도구명 위치에 glob 패턴 지원(`"*"`로 모든 도구 차단) (v2.1.166)
- `SendMessage`로 다른 세션이 릴레이한 메시지는 user authority 미보유 (권한 요청 거부, auto mode 차단) (v2.1.166)
- `requiredMinimumVersion`/`requiredMaximumVersion` managed 설정 추가 — 버전 범위 밖이면 시작 거부 (v2.1.163)
- `/plugin list` 명령 추가 (`--enabled`/`--disabled` 필터) (v2.1.163)
- Stop/SubagentStop hook이 `hookSpecificOutput.additionalContext` 반환 가능 — hook error 없이 피드백 주며 턴 계속 (v2.1.163)
- Skills: 커맨드 본문에서 숫자 앞 리터럴 `$`를 위한 `\$` 이스케이프 문법 추가 (v2.1.163)
- stdio MCP 서버가 `--resume` 시 hooks/Bash와 동일한 `CLAUDE_CODE_SESSION_ID` 수신 (v2.1.163)

**주요 버그 수정:**
- enterprise managed MCP 정책(`allowedMcpServers`/`deniedMcpServers`)이 reconnect/IDE config/`--mcp-config`에서 미적용되던 버그 수정 (v2.1.169)
- managed-settings predicate가 `${VAR}` 참조 시 미매칭되던 버그 수정 (v2.1.166)
- hook `if: "Bash(...)"` 조건이 subshell/backtick 내 명령도 매칭되도록 수정 (v2.1.163)

### v2.1.157 / v2.1.158 (2026-06-18 동기화)

**새로운 기능:**
- `.claude/skills` 디렉토리 내 플러그인 자동 로드 (marketplace 불필요) (v2.1.157)
- `claude plugin init <name>` 추가 — `.claude/skills`에 새 플러그인 스캐폴드 (v2.1.157)
- `/plugin` 인자 자동완성 추가 (서브커맨드/설치된 플러그인/marketplace 플러그인) (v2.1.157)
- `settings.json`의 `agent` 필드가 dispatch 세션에 적용, `--agent <name>`로 override (v2.1.157)
- `EnterWorktree`가 Claude 관리 worktree 간 mid-session 전환 가능 (v2.1.157)
- `tool_decision` 텔레메트리에 `tool_parameters` 포함 (`OTEL_LOG_TOOL_DETAILS=1`) (v2.1.157)
- Auto mode가 Bedrock/Vertex/Foundry의 Opus 4.7/4.8에서 사용 가능 (`CLAUDE_CODE_ENABLE_AUTO_MODE=1`) (v2.1.158)

### v2.1.154 (2026-06-18 동기화)

**새로운 기능:**
- 동적 워크플로우(dynamic workflows) 도입 — Claude가 백그라운드에서 수십~수백 agent에 작업 오케스트레이션, `/workflows`로 조회
- 플러그인이 `plugin.json`/marketplace 엔트리에서 `defaultEnabled: false` 선언 가능 — `/plugin`/`claude plugin enable`로 활성화
- stdio MCP 서버 서브프로세스가 `CLAUDE_CODE_SESSION_ID` + `CLAUDECODE=1` 환경변수 수신
- `claude mcp list`/`get`이 미승인 `.mcp.json` 서버를 `⏸ Pending approval`로 표시 (파이프 출력 시 auto-approve 안 함)
- `lean system prompt`가 Haiku/Sonnet/Opus 4.7 이전 외 모든 모델의 기본값

**Breaking Changes:**
- `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` deprecated (06/01 제거 예정)

**주요 버그 수정:**
- managed settings의 단일 잘못된 `allowedMcpServers`/`deniedMcpServers` 엔트리가 전체 정책을 폐기하던 버그 수정 (bad 엔트리만 drop + doctor 경고)
- background 세션 subagent가 worktree-isolation 가드 우회해 shared checkout에 쓰던 버그 수정

### v2.1.153 (2026-06-18 동기화)

**새로운 기능:**
- `github`/`git` 플러그인 marketplace 소스에 `skipLfs` 옵션 추가 (Git LFS 다운로드 건너뜀)
- 상태줄 명령이 `COLUMNS`/`LINES` 환경변수 수신

**주요 버그 수정:**
- subagent(Agent tool) frontmatter MCP 서버가 `--strict-mcp-config`/`--bare`/remote/enterprise managed MCP/allow-deny 정책 무시하던 버그 수정
- `--strict-mcp-config`가 명시 전달된 agent 정의(`--agents`/SDK)의 inline `mcpServers`를 strip하던 버그 수정 (차단된 subagent MCP는 경고 표시)

**Breaking Changes:**
- `/model`이 선택을 새 세션 기본값으로 저장 (IDE와 일치). 현재 세션만 변경하려면 picker에서 `s`. `keybindings.json`에서 `modelPicker:setAsDefault`를 `modelPicker:thisSessionOnly`로 rename 필요

### v2.1.152 (2026-06-18 동기화)

**새로운 기능:**
- Skills/슬래시 커맨드가 frontmatter에 `disallowed-tools` 설정 가능 — 스킬 활성 동안 모델에서 도구 제거
- `/reload-skills` 명령 추가 — 재시작 없이 스킬 디렉토리 재스캔
- `SessionStart` hook이 `reloadSkills: true` 반환 가능 (hook이 설치한 스킬을 같은 세션에서 사용), `hookSpecificOutput.sessionTitle`로 세션 제목 설정 가능
- `MessageDisplay` hook 이벤트 추가 — 표시되는 assistant 메시지 텍스트를 변환/숨김
- `pluginSuggestionMarketplaces` managed 설정 추가 (admin이 제안 가능 org marketplace allowlist)
- `claude plugin marketplace remove`가 `--scope user|project|local` 수용

**주요 버그 수정:**
- plugin MCP 서버가 동일 command·다른 환경변수일 때 잘못 dedup되던 버그 수정
- `CLAUDE_CODE_SUBAGENT_MODEL`이 agent team teammate 프로세스에 미적용되던 버그 수정 (v2.1.147)

### v2.1.149 / v2.1.147 / v2.1.145 (2026-06-18 동기화)

**새로운 기능:**
- `/usage`가 skills/subagents/plugins/MCP 서버별 limit 사용량 분해 표시 (v2.1.149)
- `claude agents --json`으로 라이브 세션을 JSON 나열 (v2.1.145)
- `claude_code.tool` OTEL span에 `agent_id`/`parent_agent_id` 속성 추가, background subagent span이 dispatching Agent span 하위로 nest (v2.1.145)
- Stop/SubagentStop hook 입력에 `background_tasks` + `session_crons` 필드 추가 (v2.1.145)
- `/plugin` Discover/Browse가 설치 전 commands/agents/skills/hooks/MCP·LSP 서버 표시 (v2.1.145)

**Breaking Changes:**
- `/simplify` → `/code-review`로 rename (correctness 버그 보고, `--comment`로 PR inline 코멘트). 기존 cleanup-and-fix 동작 제거 (v2.1.147)

**주요 버그 수정:**
- 플러그인 agent가 `tools:` frontmatter에 여러 `Agent(...)` 타입 선언 시 마지막 외 전부 drop되던 버그 수정 (v2.1.147)
- hook `if` 조건 `PowerShell(git push*)`가 매칭 안 되던 버그 수정 (v2.1.147)
- `context: fork` 스킬이 자기 자신을 무한 재호출하던 버그 수정 (v2.1.145)
- `claude plugin validate`가 파일을 가리키는 `skills:` 엔트리를 미검출하던 버그 수정 (v2.1.145)
- Agent Teams teammate가 non-ASCII 이름일 때 헤더 인코딩 오류로 모든 API 호출 실패하던 버그 수정 (v2.1.145)

### v2.1.144 / v2.1.143 / v2.1.142 (2026-06-18 동기화)

**새로운 기능:**
- 플러그인 의존성 강제: `claude plugin disable`이 의존 플러그인 있으면 거부, `enable`은 전이 의존성 force-enable (v2.1.143)
- `worktree.bgIsolation: "none"` 설정 추가 — background 세션이 `EnterWorktree` 없이 working copy 직접 편집 (v2.1.143)
- PowerShell 도구가 `-ExecutionPolicy Bypass` 전달 (opt-out: `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1`) (v2.1.143)
- `claude agents`가 `--add-dir`/`--settings`/`--mcp-config`/`--plugin-dir`/`--permission-mode`/`--model`/`--effort`/`--dangerously-skip-permissions` 수용 (v2.1.143/142)
- 루트 레벨 `SKILL.md`만 있고 `skills/` 서브디렉토리 없는 플러그인이 skill로 노출 (v2.1.142)

**주요 버그 수정:**
- stop hook이 반복 차단 시 영원히 루프하던 버그 수정 — 8회 연속 차단 후 경고와 함께 턴 종료 (`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`로 override) (v2.1.143)
- `--agent <name>`가 `plugin:` prefix 없이 plugin agent를 못 찾던 버그 수정 (v2.1.143)
- prompt-/agent-type hook을 `SessionStart`/`Setup`/`SubagentStart`에 구성 시 "command-type hook 사용" 명확한 에러 표시 (v2.1.142)
- `MCP_TOOL_TIMEOUT`이 remote HTTP/SSE 서버 fetch timeout을 못 올리던 버그(60초 cap) 수정 (v2.1.142)

### v2.1.141 / v2.1.140 (2026-06-18 동기화)

**새로운 기능:**
- hook JSON 출력에 `terminalSequence` 필드 추가 — controlling terminal 없이 desktop 알림/window 제목/벨 emit (v2.1.141)
- `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` 추가 — GitHub plugin 소스를 HTTPS로 clone (v2.1.141)
- `ANTHROPIC_WORKSPACE_ID` 환경변수 추가 (workload identity federation) (v2.1.141)
- Agent tool `subagent_type` 매칭이 대소문자·구분자 무시 (`"Code Reviewer"` → `code-reviewer`) (v2.1.140)

**주요 버그 수정:**
- settings hot-reload에서 symlink 설정 파일이 spurious `ConfigChange` hook 유발하던 회귀 수정 (v2.1.140)
- `/goal`이 `disableAllHooks`/`allowManagedHooksOnly` 설정 시 무한 hang하던 버그 수정 (v2.1.140)
- managed `extraKnownMarketplaces` auto-update 정책이 `known_marketplaces.json`에 미저장되던 버그 수정 (v2.1.140)

### v2.1.139 (2026-06-18 동기화)

**새로운 기능:**
- `claude agents` agent view (Research Preview) 추가
- `/goal` 명령 추가 — 완료 조건 설정 후 충족까지 턴 넘어 계속 작업 (interactive, `-p`, Remote Control)
- hook `args: string[]` 필드(exec form) 추가 — shell 없이 직접 spawn, path placeholder 따옴표 불필요
- `PostToolUse` hook `continueOnBlock` config 옵션 추가 — `true`로 hook 거부 사유를 Claude에 피드백하고 턴 계속
- MCP stdio 서버가 `CLAUDE_PROJECT_DIR` 환경변수 수신 (hooks와 일치), plugin config에서 `${CLAUDE_PROJECT_DIR}` 참조 가능
- subagent API 요청이 `x-claude-code-agent-id`/`x-claude-code-parent-agent-id` 헤더 carry, OTEL span에 동일 속성

**주요 버그 수정:**
- hook이 terminal에 쓸 때 on-screen 프롬프트를 손상시키던 버그 수정 (hook은 이제 terminal access 없이 실행)
- `Skill(name *)` 권한 규칙의 와일드카드가 prefix 매칭하도록 수정
- settings hot-reload가 symlink `~/.claude/settings.json` 편집을 미감지하던 버그 수정
- skill argument 이름에 regex 메타문자 포함 시 argument 치환 깨지던 버그 수정

### v2.1.136 / v2.1.133 / v2.1.132 (2026-06-18 동기화)

**새로운 기능:**
- `settings.autoMode.hard_deny` 추가 — user intent/allow 예외 무관하게 무조건 차단하는 auto mode classifier 규칙 (v2.1.136)
- `allowAllClaudeAiMcps` managed 설정 추가 (claude.ai cloud MCP connector를 managed-mcp.json과 함께 로드) (v2.1.136)
- `worktree.baseRef` 설정(`fresh`|`head`) 추가 — worktree branch 기준 선택 (v2.1.133)
- `sandbox.bwrapPath`/`sandbox.socatPath` managed 설정 추가 (Linux/WSL) (v2.1.133)
- `parentSettingsBehavior` admin-tier 키(`'first-wins'|'merge'`) 추가 (v2.1.133)
- hook이 effort level을 `effort.level` JSON 입력 필드 + `$CLAUDE_EFFORT` 환경변수로 수신, Bash 도구도 `$CLAUDE_EFFORT` 읽기 가능 (v2.1.133)
- `CLAUDE_CODE_SESSION_ID` 환경변수가 Bash 도구 서브프로세스 환경에 추가 (hooks와 일치) (v2.1.132)

**Breaking Changes:**
- `worktree.baseRef` 기본값 `fresh`가 `EnterWorktree`의 base를 `origin/<default>`로 되돌림 (2.1.128부터 local HEAD였음) — unpushed 커밋 유지하려면 `head` 설정 (v2.1.133)

**주요 버그 수정:**
- MCP 서버(`.mcp.json`/plugins/connector)가 `/clear` 후 VS Code/JetBrains/SDK에서 사라지던 버그 수정 (v2.1.136)
- plan 모드가 매칭 `Edit(...)` allow 규칙 있을 때 파일 쓰기를 미차단하던 버그 수정 (v2.1.136)
- subagent가 project/user/plugin skills를 Skill 도구로 발견 못 하던 버그 수정 (v2.1.133)
- `plugin.json`의 `skills` 엔트리가 default `skills/` 디렉토리를 숨기던 버그, `CLAUDE_ENV_FILE` SessionStart hook env가 `/resume`·`/clear` 후 stale되던 버그 수정 (v2.1.136)

### v2.1.129 / v2.1.128 / v2.1.126 (2026-06-18 동기화)

**새로운 기능:**
- `--plugin-url <url>` 플래그 추가 — URL에서 plugin `.zip` 가져옴 (v2.1.129)
- `skillOverrides` 설정 동작(`off`/`user-invocable-only`/`name-only`) (v2.1.129)
- `claude_code.skill_activated` OTEL 이벤트에 `invocation_trigger` 속성 추가 (v2.1.126)
- `--plugin-dir`가 `.zip` plugin 아카이브 수용 (v2.1.128)
- SDK 호스트가 Bash 권한 프롬프트에 persistent `localSettings` 제안 → "Always allow"가 `.claude/settings.local.json`에 기록 (v2.1.128)
- `claude project purge [path]` 추가 — 프로젝트의 모든 Claude Code state 삭제 (v2.1.126)

**Breaking Changes:**
- Plugin manifest: `themes`/`monitors`는 `"experimental": { ... }` 하위로 선언해야 함 (top-level은 동작하나 validate 경고) (v2.1.129)
- MCP: `workspace`가 예약된 서버명 — 동일 이름 기존 서버는 경고와 함께 skip (v2.1.128)
- `EnterWorktree`가 local HEAD에서 브랜치 생성하도록 변경 (이전 `origin/<default-branch>`) (v2.1.128)

**주요 버그 수정:**
- deferred tools(WebSearch/WebFetch 등)가 `context: fork` 스킬·subagent의 첫 턴에서 미사용되던 버그 수정 (v2.1.126)

### v2.1.122 / v2.1.121 / v2.1.119 / v2.1.118 (2026-06-18 동기화)

**새로운 기능:**
- MCP 서버 config에 `alwaysLoad` 옵션 추가 — `true`면 해당 서버 모든 도구가 tool-search deferral 건너뛰고 항상 사용 가능 (v2.1.121)
- `claude plugin prune` 추가 (orphaned auto-installed 의존성 제거), `plugin uninstall --prune` cascade (v2.1.121)
- PostToolUse hook이 `hookSpecificOutput.updatedToolOutput`로 모든 도구 출력 교체 가능 (이전 MCP 전용) (v2.1.121)
- `--print` 모드가 agent `tools:`/`disallowedTools:` frontmatter 존중, `--agent`가 빌트인 agent의 `permissionMode` 존중 (v2.1.119)
- PostToolUse/PostToolUseFailure hook 입력에 `duration_ms` 추가 (v2.1.119)
- 상태줄 stdin JSON에 `effort.level`/`thinking.enabled` 추가 (v2.1.119)
- Hook이 `type: "mcp_tool"`로 MCP 도구 직접 호출 가능 (v2.1.118)
- `DISABLE_UPDATES` env var 추가 (수동 `claude update`까지 차단), `wslInheritsWindowsSettings` 정책 키 추가 (v2.1.118)
- auto mode `autoMode.allow`/`soft_deny`/`environment`에 `"$defaults"` 포함해 빌트인에 커스텀 규칙 추가, `claude plugin tag` 추가 (v2.1.118)
- `ANTHROPIC_BEDROCK_SERVICE_TIER` 환경변수 추가 (v2.1.122)

**주요 버그 수정:**
- `ToolSearch`가 nonblocking 모드에서 세션 시작 후 연결된 MCP 도구를 놓치던 버그, 잘못된 hooks 엔트리가 전체 `settings.json`을 무효화하던 버그 수정 (v2.1.122)
- agent-type hook이 `Stop`/`SubagentStop` 외 이벤트에 구성 시 "Messages are required" 실패, `prompt` hook이 verifier subagent 도구 호출에 재발화하던 버그 수정 (v2.1.118)

### v2.1.113 / v2.1.110 (2026-06-18 동기화)

**새로운 기능:**
- `sandbox.network.deniedDomains` 설정 추가 — `allowedDomains` 와일드카드가 허용해도 특정 도메인 차단 (v2.1.113)
- `/tui` 명령 + `tui` 설정 추가 (v2.1.110)
- push notification 도구 추가 — Remote Control + config 활성 시 Claude가 모바일 푸시 전송 (v2.1.110)
- `autoScrollEnabled` config 추가, SDK/headless가 환경에서 `TRACEPARENT`/`TRACESTATE` 읽어 분산 trace 연결 (v2.1.110)

**Breaking Changes:**
- CLI가 번들 JavaScript 대신 네이티브 바이너리(플랫폼별 optional dependency) spawn (v2.1.113)

**주요 버그 수정:**
- `Bash` `dangerouslyDisableSandbox`가 권한 프롬프트 없이 샌드박스 밖 실행하던 버그 수정 (v2.1.113)
- `PermissionRequest` hook의 `updatedInput`이 `permissions.deny` 규칙에 재검사 안 되던 버그 수정; `setMode:'bypassPermissions'`가 `disableBypassPermissionsMode` 존중 (v2.1.110)
- `PreToolUse` hook `additionalContext`가 도구 호출 실패 시 drop되던 버그, skills `disable-model-invocation: true`가 `/<skill>`로 호출 시 실패하던 버그 수정 (v2.1.110)

### v2.1.108 / v2.1.105 (2026-06-18 동기화)

**새로운 기능:**
- `ENABLE_PROMPT_CACHING_1H` env var 추가 (API/Bedrock/Vertex/Foundry 1시간 캐시 TTL), `FORCE_PROMPT_CACHING_5M` 추가 (v2.1.108)
- 모델이 빌트인 슬래시 커맨드(`/init`, `/review`, `/security-review`)를 Skill 도구로 발견·호출 가능 (v2.1.108)
- `EnterWorktree` 도구에 `path` 파라미터 추가 (기존 worktree로 전환) (v2.1.105)
- PreCompact hook 지원 추가 — exit code 2 또는 `{"decision":"block"}`으로 compaction 차단 (v2.1.105)
- 플러그인 background monitor 지원 — top-level `monitors` manifest 키 (세션 시작/스킬 호출 시 auto-arm) (v2.1.105)
- skill description 리스팅 cap 250→1,536자로 상향 (v2.1.105)

**주요 버그 수정:**
- stdio MCP 서버가 stray non-JSON 출력 시 첫 줄에서 disconnect되던 버그 수정 (v2.1.105)

### v2.1.101 / v2.1.98 / v2.1.97 (2026-06-18 동기화)

**새로운 기능:**
- `/team-onboarding` 명령 추가 (로컬 사용 기반 teammate 램프업 가이드 생성) (v2.1.101)
- Monitor 도구 추가 (background 스크립트 이벤트 스트리밍) (v2.1.98)
- `workspace.git_worktree`를 상태줄 JSON 입력에 추가 (linked worktree 내일 때) (v2.1.98/97)
- `CLAUDE_CODE_PERFORCE_MODE` env var 추가 (read-only 파일에서 Edit/Write 실패 + `p4 edit` 힌트) (v2.1.98)
- `--exclude-dynamic-system-prompt-sections` print 모드 플래그 추가 (cross-user 캐싱) (v2.1.98)
- `refreshInterval` 상태줄 설정 추가 (N초마다 재실행) (v2.1.97)

**주요 버그 수정:**
- `permissions.deny` 규칙이 PreToolUse hook의 `permissionDecision: "ask"`를 override 못 하던 버그 수정 (hook이 deny를 prompt로 다운그레이드 가능했음) (v2.1.101)
- 컴파운드 Bash 명령이 auto/bypass 모드에서 강제 권한 프롬프트를 우회하던 버그 수정 (보안) (v2.1.98)
- subagent가 dynamically-injected 서버의 MCP 도구를 미상속하던 버그, prompt-type Stop/SubagentStop hook이 긴 세션에서 실패하던 버그 수정 (v2.1.101/98/97)

### v2.1.94 / v2.1.92 / v2.1.91 / v2.1.90 (2026-06-18 동기화)

**새로운 기능:**
- `hookSpecificOutput.sessionTitle`을 `UserPromptSubmit` hook에 추가 (세션 제목 설정) (v2.1.94)
- `keep-coding-instructions` frontmatter 필드 지원 (plugin output styles) (v2.1.94)
- 플러그인 스킬 `"skills": ["./"]`이 directory basename 대신 frontmatter `name`을 invocation 이름으로 사용 (v2.1.94)
- `forceRemoteSettingsRefresh` 정책 설정 추가 (remote managed settings 신선 fetch까지 시작 차단, fail-closed) (v2.1.92)
- MCP `_meta["anthropic/maxResultSizeChars"]` 어노테이션으로 결과 persistence override(최대 500K) (v2.1.91)
- `disableSkillShellExecution` 설정 추가 (skills/슬래시 커맨드/plugin 커맨드의 inline shell 실행 비활성화) (v2.1.91)
- 플러그인이 `bin/` 하위 실행파일을 bare 명령으로 Bash 도구에서 호출 가능 (v2.1.91)
- `.husky`를 protected 디렉토리에 추가 (acceptEdits) (v2.1.90)

**Breaking Changes:**
- `/tag` 명령 제거, `/vim` 명령 제거(`/config` → Editor mode로 토글) (v2.1.92)

**주요 버그 수정:**
- 플러그인 스킬 hook이 YAML frontmatter에 정의 시 무시되던 버그, `CLAUDE_PLUGIN_ROOT` 미설정 시 "No such file" 실패, `${CLAUDE_PLUGIN_ROOT}`가 marketplace source로 resolve되던 버그 수정 (v2.1.94)
- `PreToolUse` hook이 JSON을 stdout에 emit하고 exit code 2일 때 도구 호출을 올바로 차단하도록 수정 (v2.1.90)
- prompt-type Stop hook이 small fast 모델이 `ok:false` 반환 시 잘못 실패하던 버그, `preventContinuation:true` 의미 복원 (v2.1.92)
- `permissions.defaultMode: "auto"`의 JSON 스키마 검증 수정 (v2.1.91)

---

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
