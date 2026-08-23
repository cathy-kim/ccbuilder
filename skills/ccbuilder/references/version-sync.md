# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-08-23
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

### v2.1.220 (2026-07-26 동기화)

**새로운 기능:**
- (v2.1.219) **Claude Opus 5** (`claude-opus-5`) 출시 — 신규 기본 Opus 모델, 1M 컨텍스트, Fast Mode $10/$50 per Mtok
- (v2.1.219) **서브에이전트 중첩 파견 기본값 재변경** — depth 3까지 기본 허용 (v2.1.217의 "기본 비허용"을 대체), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`로 비활성화 가능
- (v2.1.219) `sandbox.network.strictAllowlist` 설정 — 샌드박스 명령에서 미허용 호스트를 프롬프트 없이 거부
- (v2.1.219) `DirectoryAdded` Hook 신규 — `/add-dir` 또는 SDK `register_repo_root` control request로 세션 중 새 작업 디렉토리 등록 시 발동
- (v2.1.219) 헤드리스 stream-json init 이벤트에 `mcp_server_errors` 추가 — `--mcp-config` 검증 실패로 스킵된 서버 목록; 터미널 실행 시 시작 경고
- (v2.1.219) `workflowSizeGuideline` 설정 키 — Dynamic workflow 권장 크기를 모든 settings 파일에서 지정 가능 (설정 시 `/config` 행 숨김)
- (v2.1.219) stream-json에 depth-2+ 중첩 서브에이전트 전달 — `--forward-subagent-text` 설정 시 파견한 Agent `tool_use` id로 키 지정되어 표시
- (v2.1.219) `claude mcp list`/`/mcp` 서버 연결 실패 시 HTTP 상태·오류 텍스트 표시; MCP 설정 값 숨은 공백 경고
- (v2.1.219) `workflowSizeGuideline` 관련 — Dynamic workflow 기본 크기 가이드라인 medium(15개 미만 에이전트 권장)으로 변경; 실행 중 workflow 상태줄에 현재 기본 크기 + `/config` 안내 표시
- (v2.1.219) managed MCP allowlist/denylist `${VAR}` 항목이 settings 파일 env 대신 시작 환경변수·managed-settings env에서 해석되도록 변경
- (v2.1.219) `/model` 피커 신규 모델명만 하이라이트 — 새 릴리스를 명확히 표시
- (v2.1.219) `claude --teleport` 현재 체크아웃이 세션 레포와 다를 때 어떤 레포를 가리키는지 표시
- (v2.1.219) Remote Control 오류 메시지 개선 — "api.anthropic.com에서만 사용 가능" 오류에 원인 설정 이름 명시
- (v2.1.219) claude-api 스킬 기본 모델 Opus 5로 전환 (Opus 4.8 마이그레이션 경로 포함)
- (v2.1.220) 버그 수정 및 안정성 개선 (세부 사항 미공개)

**Breaking Changes:**
- 서브에이전트 중첩 파견 기본값이 depth 3 허용으로 복원 — v2.1.217의 "기본 비허용"을 대체 (v2.1.219)
- Fast Mode에서 Opus 4.7 제거 — `/fast`는 Opus 5·Opus 4.8에만 적용 (v2.1.219)

**주요 버그 수정:**
- `claude -p` 중간 스트림 API 오류 발생 시 이미 생성된 텍스트 응답이 유실되던 버그 수정 (v2.1.219)
- Fable 모델 행이 stale 캐시로 인해 "Requires usage credits"로 잘못 표시되던 버그 수정 (v2.1.219)
- `/model` 피커에서 병합된 Opus 행이 "Opus"로만 표시되던 버그 수정 — "Opus (1M context)"로 복원 (v2.1.219)
- GNU screen 내 copy-on-select가 선택 영역 대신 base64를 터미널에 출력하던 버그 수정 (v2.1.219)
- Remote Control 클라이언트가 모델 전환·재연결·조직 확인 실패 후 stale fast-mode 상태를 유지하던 버그 수정 (v2.1.219)
- Windows `CLAUDE_CODE_GIT_BASH_PATH`가 bash/sh 바이너리가 아닌 경로일 때 종료되거나 그대로 사용되던 버그 수정 — 이제 경고와 함께 무시 (v2.1.219)
- vim NORMAL 모드에서 빈 프롬프트 상태 ← 키가 에이전트 뷰로 복귀하지 않던 버그 수정 (INSERT 모드에서만 동작하던 것 수정) (v2.1.219)
- 화면낭독기 모드가 매 키 입력마다 전체 입력 줄을 재작성하던 버그 수정 — 타이핑한 문자만 에코 (v2.1.219)

---

### v2.1.218 (2026-07-23 동기화)

**새로운 기능:**
- (v2.1.218) `/code-review`가 백그라운드 서브에이전트로 실행 — 대화 컨텍스트 미점유, 스택된 슬래시 명령을 리뷰 대상 유지
- (v2.1.218) `/deep-research`는 수동 호출 시에만 시작 — Claude 자율 실행 안 함
- (v2.1.218) Skill·플러그인 frontmatter boolean에 `yes`/`no`/`on`/`off`/`1`/`0`(대소문자 무관) 허용
- (v2.1.218) agent frontmatter 이름에 `:` 포함 시 거부 — 플러그인 네임스페이싱 예약 문자
- (v2.1.218) auto mode 개선 — dangerous-rm·background-`&`·suspicious-Windows-path 검사가 권한 다이얼로그 대신 auto-mode 분류기가 판단
- (v2.1.217) 동시 실행 서브에이전트 상한 (기본 20, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`)
- (v2.1.217) **서브에이전트 기본 중첩 파견 비활성화** — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로만 허용
- (v2.1.217) emoji shortcode 자동완성 (`:heart:` → ❤️, `emojiCompletionEnabled` 설정으로 비활성화)
- (v2.1.217) `--max-budget-usd` 한도 도달 시 신규 백그라운드 서브에이전트 스폰 거부 + 실행 중 에이전트 중단
- (v2.1.216) `sandbox.filesystem.disabled` 설정 — 네트워크 egress 제어 유지하며 파일시스템 격리만 스킵
- (v2.1.215) Claude가 `/verify`·`/code-review`를 더 이상 자율적으로 실행하지 않음 — 명시적 호출 필요
- (v2.1.214) **`EndConversation` 도구 추가** — 심각한 악용·탈옥 시도 세션 자체 종료 (claude.ai와 동일)
- (v2.1.214) 장시간 도구 호출 진행 heartbeat, `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH`, docker 데몬 리다이렉트 플래그 권한 프롬프트, 메모리 frontmatter ISO `modified` 타임스탬프
- (v2.1.212) **`/fork`가 백그라운드 세션 생성으로 변경** — 기존 인라인 서브에이전트 launch는 `/subtask`로 분리
- (v2.1.212) `claude auto-mode reset`, WebSearch 세션 한도(기본 200, `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`), 서브에이전트 파견 세션 한도(기본 200, `CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`, `/clear`로 리셋)
- (v2.1.212) MCP 도구 호출 2분 초과 시 자동 백그라운드 전환 (`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`)
- (v2.1.212) Task tool `mode` 파라미터 제거(deprecated) — 서브에이전트는 부모 세션 permission mode 상속
- (v2.1.211) `--forward-subagent-text`/`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`, "always allow" 권한 규칙 레포 루트 저장(worktree 간 공유), vim `s`/`S` NORMAL mode
- (v2.1.210) 도구 호출 실시간 경과 시간 카운터, `Write(path)`/`NotebookEdit(path)`/`Glob(path)` 권한 규칙 시작 경고
- (v2.1.208) 스크린리더 모드(`--ax-screen-reader`, `CLAUDE_AX_SCREEN_READER=1`), `vimInsertModeRemaps` 설정, `CLAUDE_CODE_PROCESS_WRAPPER`
- (v2.1.207) Auto mode Bedrock·Vertex·Foundry opt-in 불필요(`disableAutoMode`로 비활성화); 해당 플랫폼 기본 모델 Opus 4.8 전환
- (v2.1.206) `/cd` 디렉토리 경로 자동완성, `/doctor` CLAUDE.md 트리밍 제안, `/commit-push-pr` push remote 자동 허용 확장, `EnterWorktree` `.claude/worktrees/` 외부 진입 확인

**Breaking Changes:**
- 서브에이전트 기본 중첩 파견 비활성화 — `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`로만 허용, 기존 5레벨 재귀 파견 기본 동작 대체 (v2.1.217)
- Task tool `mode` 파라미터 제거 — 서브에이전트는 부모 세션 permission mode 상속 (v2.1.212)
- `/fork`가 백그라운드 세션 생성으로 변경 — 기존 인라인 서브에이전트 launch는 `/subtask` (v2.1.212)
- Claude가 `/verify`·`/code-review`를 자동 실행하지 않음 — 명시적 호출 필요 (v2.1.215)
- `context: fork` 스킬 기본 백그라운드 실행 — opt out: `background: false` (v2.1.218)

**주요 버그 수정:**
- Windows 경로(`\u` 접두 세그먼트)가 도구 입력에서 CJK 문자로 손상되던 버그 수정 (v2.1.218)
- `Edit(src/**)` 등 단일 세그먼트 `dir/**` allow 규칙이 트리 전체 중첩 `dir/`에 잘못 자동 승인되던 보안 버그 수정 (v2.1.214)
- Windows PowerShell 5.1 세션 권한 검사 우회 취약점 수정 (v2.1.214)
- 10,000자 초과 Bash 명령 검사 없이 자동 실행되던 버그 수정 — 항상 프롬프트로 변경 (v2.1.214)
- MCP 대형 tool output 트런케이션 시 전체 결과가 세션 종료까지 메모리에 남던 누수 수정 (v2.1.217)
- 장기 세션 메시지 정규화 비용 이차 증가로 인한 수 초 단위 지연·재개 지연 수정 (v2.1.216)
- worktree 격리 서브에이전트가 `git -C`/`--git-dir`/`GIT_DIR`로 공유 체크아웃에 git 명령 우회하던 버그 수정 (v2.1.216)
- `ultracode` 키워드 옵트인이 웹훅 페이로드·릴레이된 PR 코멘트 등 비사용자 입력에서 발동하던 버그 수정 (v2.1.210)

---

### v2.1.181 (2026-06-18 동기화)

**새로운 기능:**
- `/config key=value` 문법 추가 — 프롬프트에서 모든 설정 즉시 변경 (interactive, `-p`, Remote Control 지원)
- `sandbox.allowAppleEvents` opt-in 설정 추가 (macOS 샌드박스 명령이 Apple Events 전송 허용)
- `CLAUDE_CLIENT_PRESENCE_FILE` 환경변수 추가 (마커 파일로 모바일 푸시 알림 억제)

**주요 버그 수정:**
- foreground subagent가 무제한 중첩 체인 생성하던 버그 수정 → background와 동일하게 5단계 깊이 제한 적용
- 커스텀 `ANTHROPIC_BASE_URL` / Foundry에서 prompt caching이 동작하지 않던 버그 수정
- `claude mcp get`/`list`가 tools/list 실패 시에도 `✓ Connected` 표시하던 버그 → `! Connected · tools fetch failed`로 수정

---

### v2.1.173 (2026-06-11 동기화)

**새로운 기능:**
- (v2.1.170) Claude Fable 5 출시 — Mythos 클래스 모델, 일반 사용 가능; v2.1.170 이상 업데이트 필요
- (v2.1.172) 서브에이전트 재귀 파견 최대 5레벨 — 서브에이전트가 자체 서브에이전트 파견 가능
- (v2.1.172) Amazon Bedrock `~/.aws` config에서 `AWS_REGION` 미설정 시 리전 자동 읽기; `/status` 리전 출처 표시
- (v2.1.172) `/plugin` 마켓플레이스 플러그인 브라우저 검색창 추가
- (v2.1.172) `claude_code.lines_of_code.count` OTEL 메트릭 `model` 속성 추가
- (v2.1.173) Fable 5 모델명 `[1m]` 접미사 자동 제거 — 1M 컨텍스트 기본 포함

**주요 버그 수정:**
- Windows sandbox 활성화 시 불필요한 "sandbox dependencies missing" 경고 수정 (v2.1.173)
- 1M 컨텍스트 사용 세션이 크레딧 없을 때 영구 중단되던 버그 수정 (v2.1.172)
- 백그라운드 에이전트가 다른 디렉토리 `.mcp.json` 승인·trust project settings 읽던 버그 수정 (v2.1.172)
- `availableModels` 제한이 서브에이전트 모델 오버라이드·에이전트 디스패치에 미적용되던 버그 수정 (v2.1.172)
- `WebFetch(domain:*.example.com)` 와일드카드 서브도메인 매칭 안 되던 버그 수정 (v2.1.172)
- 원격 세션에서 `CLAUDE_MEMORY_STORES` 마운트된 메모리 스토어 리콜 미동작 수정 (v2.1.172)
- VS Code 통합 터미널 세션 트랜스크립트 미저장 버그 수정 (v2.1.170)

---

### v2.1.169 (2026-06-09 동기화)

**새로운 기능:**
- (v2.1.169) `--safe-mode` 플래그 및 `CLAUDE_CODE_SAFE_MODE` — 모든 커스터마이제이션(CLAUDE.md·플러그인·스킬·훅·MCP) 비활성화 시작 (트러블슈팅)
- (v2.1.169) `/cd` 명령 — 프롬프트 캐시 유지하며 세션 작업 디렉토리 변경
- (v2.1.169) `disableBundledSkills` 설정 + `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` env var — 번들 스킬·워크플로우·내장 슬래시 명령 숨김
- (v2.1.169) `claude agents --json` — 차단·방금파견 세션 포함; `--all`로 완료 세션 포함; 신규 `id`·`state` 필드
- (v2.1.169) CLAUDE.md 경고 임계값 모델 컨텍스트 창 크기에 따라 자동 조정
- (v2.1.169) Vertex/Foundry 기본 5분 유휴 타임아웃 복원; `API_FORCE_IDLE_TIMEOUT=0`으로 비활성화
- (v2.1.169) 백그라운드 세션 retire→wake 후 `--ide`·`--chrome`·`--bare`·`--remote-control` 등 플래그 유지
- (v2.1.169) `TaskCreate` 안정성 개선 — 잘못된 입력 자동 수정, 미로드 도구 스키마 포함 오류 메시지
- (v2.1.166) `fallbackModel` 최대 3개 폴백 모델 순서 지정; `--fallback-model` 대화형 세션 지원
- (v2.1.166) deny rule tool-name 위치 glob 패턴 — `"*"`로 전체 도구 거부
- (v2.1.166) `MAX_THINKING_TOKENS=0`/`--thinking disabled`/모델별 토글 — Claude API 기본 thinking 모델 비활성화
- (v2.1.163) `requiredMinimumVersion`/`requiredMaximumVersion` managed settings — 버전 범위 밖 시작 거부
- (v2.1.163) `/plugin list` `--enabled`/`--disabled` 필터
- (v2.1.163) Skills `\$` 이스케이프 — 명령 본문 숫자 앞 리터럴 달러 기호
- (v2.1.163) Stop·SubagentStop Hook `hookSpecificOutput.additionalContext` 반환 지원
- (v2.1.163) stdio MCP 서버 `--resume` 시 `CLAUDE_CODE_SESSION_ID` 수신
- (v2.1.162) `claude agents --json` `waitingFor` 필드 (차단 세션 대기 이유)
- (v2.1.161) `OTEL_RESOURCE_ATTRIBUTES` 값 → 메트릭 데이터포인트 레이블
- (v2.1.161) 병렬 도구 호출: 개별 실패가 같은 배치 다른 호출 취소하지 않음
- (v2.1.160) acceptEdits 모드 빌드 도구 설정 파일 쓰기 전 프롬프트 추가

**Breaking Changes:**
- Dynamic Workflow 트리거 `workflow` → `ultracode` 리네임 (v2.1.160)
- `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE` 제거 → no-op (v2.1.160)
- acceptEdits 빌드 도구 설정 파일(`.npmrc`, `.yarnrc*`, `bunfig.toml`, `.bazelrc`, `.pre-commit-config.yaml`, `.devcontainer/`) 쓰기 전 프롬프트 (v2.1.160)

**주요 버그 수정:**
- MCP `allowedMcpServers`/`deniedMcpServers` 재연결·IDE·`--mcp-config`·원격 설정 로드 전 미적용 수정 (v2.1.169)
- macOS claude.ai 자격증명 로그인 시 매 턴 ~30-50ms UI 스톨 수정 (v2.1.169)
- Windows `claude -p` 슬래시 명령/스킬 스캔 행어 수정 (v2.1.169, v2.1.161 회귀)
- Remote Control OAuth 토큰 갱신 동시 발생 시 "reconnecting" 고착 수정 (v2.1.169)
- 신뢰되지 않은 project settings의 OTEL 클라이언트 인증서 경로 신뢰 확인 없이 설정 가능하던 보안 수정 (v2.1.169)
- 백그라운드 세션 project-level settings `env` 값 무시 수정 (v2.1.169)

---

### v2.1.158 (2026-05-30 동기화)

**새로운 기능:**
- (v2.1.158) Auto mode Bedrock·Vertex·Foundry 지원 — Opus 4.7·4.8 대상; `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 옵트인
- (v2.1.157) `.claude/skills` 디렉토리 플러그인 자동 로드 — 마켓플레이스 설치 불필요
- (v2.1.157) `claude plugin init <name>` — `.claude/skills`에 새 플러그인 스캐폴딩
- (v2.1.157) `/plugin` 인자 자동완성 — 서브커맨드·설치된 플러그인·알려진 마켓플레이스 목록 서브스트링 매칭
- (v2.1.157) `settings.json` `agent` 필드 — dispatched 세션 기본 에이전트 지정; `--agent <name>` 오버라이드
- (v2.1.157) `EnterWorktree` Claude 관리 worktree 간 mid-session 전환 지원
- (v2.1.157) `OTEL_LOG_TOOL_DETAILS=1` — `tool_decision` 이벤트에 `tool_parameters` 포함 (bash commands, MCP/skill names)
- (v2.1.157) Workflow keyword trigger 설정 (`/config`) — "workflow" 단어 Dynamic Workflow 자동 트리거 비활성화
- (v2.1.157) Claude 관리 worktree 작업 완료 후 잠금 해제 → `git worktree remove`/`prune` 가능

**주요 버그 수정:**
- 처리 불가 이미지(zero-byte, 손상) 요청 크래시 → 텍스트 플레이스홀더 처리 (v2.1.157)
- auto/bypass-permissions 모드 sandbox 네트워크 권한 프롬프트 불필요 표시 수정 (v2.1.157)
- `claude agents` 완료 세션 유휴 서브에이전트 남아 정리 안 되던 버그 수정 (v2.1.157)
- 백그라운드 에이전트 worktree 30일 정리 시 고아로 남는 버그 수정 (v2.1.157)
- sleep/wake 재연결 후 모델 잘못된 날짜 사용 버그 수정 (v2.1.157)
- VS Code/Cursor/Windsurf 통합 터미널 우클릭 붙여넣기 중복 수정 (v2.1.157)
- WSL 이미지 붙여넣기·Windows 11 스크린샷·Windows Explorer 이미지 드래그 지원 (v2.1.157)

---

### v2.1.156 (2026-05-29 동기화)

**새로운 기능:**
- (v2.1.154) Opus 4.8 모델 출시 — xhigh effort 기본값, Fast Mode 2x 비용·2.5x 속도
- (v2.1.154) Dynamic Workflows (`/workflows`) — 수십~수백 에이전트 백그라운드 오케스트레이션
- (v2.1.154) `claude agents` `! <command>` — 셸 명령 백그라운드 세션 실행
- (v2.1.154) Plugin `defaultEnabled: false` — 기본 비활성화 선언 지원
- (v2.1.154) Stdio MCP 서버 서브프로세스에 `CLAUDE_CODE_SESSION_ID`·`CLAUDECODE=1` env 자동 제공
- (v2.1.154) `claude mcp list`/`get` — 미승인 서버 `⏸ Pending approval` 표시
- (v2.1.152) `MessageDisplay` Hook 이벤트 — 어시스턴트 메시지 텍스트 변환·숨김
- (v2.1.152) Skills/슬래시 명령 `disallowed-tools` frontmatter 지원
- (v2.1.152) `/reload-skills` 명령; `SessionStart` Hook `reloadSkills: true` + `sessionTitle` 지원
- (v2.1.152) Auto mode 옵트인 동의 불필요
- (v2.1.153) `skipLfs` — github/git 플러그인 소스 LFS 건너뛰기
- (v2.1.153) `/model` 선택 기본값 저장; `s`로 현재 세션만 전환

**주요 버그 수정:**
- Opus 4.8 thinking block 수정으로 API 400 오류 수정 (v2.1.156)
- 백그라운드 세션 subagent worktree isolation 우회 버그 수정 (v2.1.154)
- `worktree.baseRef: "head"` linked worktree에서 잘못된 HEAD 반환 수정 (v2.1.154)
- managed settings 단일 잘못된 항목으로 전체 정책 무시되던 버그 수정 (v2.1.154)
- Agent tool frontmatter MCP 서버 `--strict-mcp-config`·managed 정책 무시 수정 (v2.1.153)

---

### v2.1.150 (2026-05-23 동기화)

**새로운 기능:**
- (v2.1.150) 내부 인프라 개선 (사용자 가시 변경 없음)
- (v2.1.149) `/usage` 카테고리별 사용량 분석 — skills·subagents·plugins·MCP 서버별 비용 표시
- (v2.1.149) `/diff` 상세 뷰 키보드 스크롤 지원 (arrows·j/k·PgUp/PgDn·Space·Home/End)
- (v2.1.149) 마크다운 GFM task list 체크박스 렌더링 — `- [ ] todo` / `- [x] done` 기본 불릿 대신 체크박스 표시
- (v2.1.149) Enterprise: `allowAllClaudeAiMcps` managed 설정 — `managed-mcp.json`과 함께 claude.ai cloud MCP 커넥터 동시 로드
- (v2.1.147) 핀된 백그라운드 세션 (`Ctrl+T` in `claude agents`) 유휴 시 유지·업데이트 in-place 재시작·메모리 압박 시에만 비핀 세션 후 제거
- (v2.1.147) 자동 업데이트 개선 — 네트워크 실패 재시도, 상세 오류 카테고리·OS 에러 코드 보고

**주요 버그 수정:**
- PowerShell 권한 우회 — 내장 `cd` 함수(`cd..`, `cd\`, `cd~`, `X:`)가 감지 없이 워크스페이스 외부 디렉토리 접근 허용하던 버그 수정 (v2.1.149)
- git worktree 내 sandbox 쓰기 허용 리스트가 공유 `.git` 디렉토리 대신 전체 메인 레포 루트를 커버하던 버그 수정 (v2.1.149)
- `find` 명령이 macOS 시스템 파일/vnode 테이블 고갈·호스트 크래시 유발하던 버그 수정 (v2.1.149)
- `/ultraplan` 및 원격 세션 생성 시 변경 없는 워킹 트리에서 "Could not capture uncommitted changes" 실패 수정 (v2.1.149)
- Bash 도구 exit code 127 회귀 수정 (v2.1.147 회귀 → v2.1.148 핫픽스)
- managed-settings 승인 다이얼로그 수락 후 터미널 프리즈 수정 (v2.1.149)

---

### v2.1.146 (2026-05-21 동기화)

**새로운 기능:**
- (v2.1.146) `/code-review [effort]` 명령 — `/simplify` 리네임, 선택적 effort 레벨 지원 (e.g. `/code-review high`)
- (v2.1.146) auto mode에서 사용자·스킬이 `AskUserQuestion` 명시 의존 시 억제하지 않음
- (v2.1.145) `claude agents --json` — 실행 중 세션 JSON 목록 출력 (스크립팅·tmux-resurrect·status bar)
- (v2.1.145) `agent_id`·`parent_agent_id` 속성 — `claude_code.tool` OTEL span에 추가; 백그라운드 서브에이전트 trace parenting 수정
- (v2.1.145) `/plugin` Discover·Browse 화면에서 설치 전 명령·에이전트·스킬·훅·MCP/LSP 서버 상세 미리 보기
- (v2.1.145) status line JSON 입력에 GitHub 레포·PR 정보 포함 (감지 시)
- (v2.1.145) Stop·SubagentStop Hook 입력에 `background_tasks`·`session_crons` 필드 추가
- (v2.1.145) 슬래시 명령·@-멘션 제안 목록 풀스크린 모드 마우스 호버·클릭 지원
- (v2.1.144) `/resume` 백그라운드 세션 지원 — `bg` 마커로 구분 표시
- (v2.1.144) 백그라운드 서브에이전트 완료 알림에 elapsed duration 표시 (예: "Agent completed · 3h 2m 5s")
- (v2.1.144) `/model` 현재 세션만 변경 — 신규 세션 기본값 설정은 모델 피커 `d` 키
- (v2.1.144) `/extra-usage` → `/usage-credits` 리네임 (구 명령 유지)
- (v2.1.144) `/plugin` browse·discover 패널 플러그인 마지막 업데이트 일시 표시
- (v2.1.143) `worktree.bgIsolation: "none"` 설정 — 백그라운드 세션 worktree 격리 없이 직접 편집
- (v2.1.143) `claude plugin disable` 의존성 강제 — 의존 플러그인 존재 시 거부 + disable-chain 힌트
- (v2.1.143) `claude plugin enable` 전이적 의존성 자동 강제 활성화
- (v2.1.143) `/plugin` 마켓플레이스 브라우즈 패널 예상 컨텍스트 비용 표시
- (v2.1.143) `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` env var — stop hook 블록 반복 상한 오버라이드 (기본 8회)
- (v2.1.143) PowerShell 도구 `-ExecutionPolicy Bypass` 기본 전달

**Breaking Changes:**
- `/simplify` → `/code-review [effort]` 리네임 (v2.1.146)
- PowerShell 도구 `-ExecutionPolicy Bypass` 기본 전달 — 옵트아웃: `CLAUDE_CODE_POWERSHELL_RESPECT_EXECUTION_POLICY=1` (v2.1.143)

**주요 버그 수정:**
- MCP `resources/list`, `resources/templates/list`, `prompts/list` 페이지네이션 서버에서 2페이지 이후 항목 누락 수정 (v2.1.146)
- Windows PowerShell 도구 winget/Microsoft Store 설치 시 "command line is invalid" 오류 수정 (v2.1.146)
- Read 도구 전체 파일 토큰 한도 초과 시 "PARTIAL view" 노티스와 함께 첫 페이지 트런케이션 반환 (v2.1.145)
- Agent Teams 비ASCII 이름 팀메이트 API 호출 실패 (유효하지 않은 헤더 인코딩) 수정 (v2.1.145)
- `/review` deprecated `projectCards` GraphQL 쿼리 수정 (v2.1.145)
- `claude plugin validate` `skills:` 항목 파일 가리킬 때 미검출 수정 (v2.1.145)
- 시작 시 `api.anthropic.com` 미달 시 최대 75초 hang 현상 수정 — 15초 타임아웃 (v2.1.144)
- Stop Hook 반복 블록 무한 루프 — 8회 연속 블록 후 경고와 함께 턴 종료 (v2.1.143)

---

### v2.1.142 (2026-05-15 동기화)

**새로운 기능:**
- (v2.1.142) `claude agents` 신규 플래그 — `--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions` 백그라운드 세션 상세 설정
- (v2.1.142) Fast Mode Opus 4.7 기본 전환 (이전: Opus 4.6); `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`로 Opus 4.6 고정 가능
- (v2.1.142) 루트 레벨 `SKILL.md` 보유 플러그인 (`skills/` 서브디렉토리 없음) 스킬로 자동 노출
- (v2.1.142) `/plugin` 상세 패널 및 `claude plugin details`에서 제공 LSP 서버 목록 표시
- (v2.1.142) `/web-setup` 기존 GitHub App 연결 교체 전 경고 추가

**주요 버그 수정:**
- `MCP_TOOL_TIMEOUT` 설정이 원격 HTTP/SSE MCP 서버 per-request fetch timeout에 미반영되던 버그 수정 (60초 상한 → 설정값 반영) (v2.1.142)
- 백그라운드 세션 기존 git worktree 미인식 → Edit 차단·`EnterWorktree` 중복 거부 버그 수정 (v2.1.142)
- macOS 수면/재개 후 백그라운드 세션 소실 및 daemon 재연결 실패 수정 (v2.1.142)
- 바이너리 업그레이드 후 데몬 미정상 종료로 파견 에이전트 크래시 루프 수정 (v2.1.142)
- 플러그인 `skills: ["./"]` "path escapes plugin directory" 거짓 오류 수정 (v2.1.142)
- Reactive compaction 첫 시도 시 원본 요청 overflow 크기에서 시드 — 낭비 재시도 방지 (v2.1.142)

---

### v2.1.141 (2026-05-14 동기화)

**새로운 기능:**
- (v2.1.141) Hook JSON 출력 `terminalSequence` 필드 — 제어 터미널 없이 데스크탑 알림·창 제목·벨 신호 발송 가능
- (v2.1.141) `CLAUDE_CODE_PLUGIN_PREFER_HTTPS` env var — SSH 키 없는 환경에서 GitHub 플러그인 소스 HTTPS 클론 (기본: SSH)
- (v2.1.141) `ANTHROPIC_WORKSPACE_ID` env var — workload identity federation 토큰 특정 워크스페이스 범위 지정
- (v2.1.141) `claude agents --cwd <path>` — 세션 목록을 특정 디렉토리 범위로 필터링
- (v2.1.141) `/feedback` 최근 세션 포함 지원 (24시간·7일) — 현재 세션 범위를 넘는 이슈 제보 가능
- (v2.1.141) Rewind 메뉴 "Summarize up to here" — 최근 대화 유지하며 이전 컨텍스트 압축
- (v2.1.141) auto mode permission dialog: `permissions.ask` 규칙 원인 설명 추가
- (v2.1.141) 파일 편집 권한 프롬프트 "view diff in your IDE" 옵션 복원 (IDE 연결 시)
- (v2.1.141) 백그라운드 에이전트(`/bg`·`←←`) 현재 permission mode 유지 — 기본값 revert 방지
- (v2.1.141) `claude agents`: 완료 후 백그라운드 쉘이 남은 에이전트 → Completed 상태 이동
- (v2.1.141) thinking 스피너 10초 후 황색 전환 표시

**주요 버그 수정:**
- Bedrock/Vertex/Foundry/gateway background side-queries에 unavailable Haiku 모델 ID 전송 수정 (v2.1.141)
- hooks에서 `EnterWorktree` 이후 non-existent `transcript_path` 수신 버그 수정 (v2.1.141)
- 마크다운 테이블 셀 줄바꿈 시 세로 key-value 레이아웃 폴백 회귀 수정 (v2.1.141, v2.1.136 회귀)
- MCP HTTP/SSE 서버 403 반환 시 "needs auth" 표시 수정 (v2.1.141)
- MCP 서버 config POSIX shell parameter expansion 누락 env var로 오판 수정 (v2.1.141)
- `claude plugin install` upstream `ref` 없을 때 `sha` pinned 시 실패 수정 (v2.1.141)
- Bedrock `awsCredentialExport` ambient 자격증명 시에도 항상 실행 (cross-account 인증, v2.1.141)
- Remote MCP 서버 optional server-events 스트림 실패 시 불필요한 연결 해제 수정 (v2.1.141)

---

### v2.1.140 (2026-05-13 동기화)

**새로운 기능:**
- (v2.1.140) Agent tool `subagent_type` 대소문자·구분자 무관 매칭 — `"Code Reviewer"` → `code-reviewer` 자동 해석
- (v2.1.139) agent view (Research Preview) — `claude agents` 실행 중·대기·완료 세션 단일 목록
- (v2.1.139) `/goal <condition>` 명령 — 완료 조건 설정, 조건 충족 시까지 자율 실행 (interactive·`-p`·Remote Control)
- (v2.1.139) Hook `args: string[]` (exec form) — 셸 없이 직접 실행, 경로 플레이스홀더 인용 불필요
- (v2.1.139) Hook `continueOnBlock` PostToolUse 옵션 — 거부 사유 모델 피드백 후 턴 계속
- (v2.1.139) MCP stdio 서버에 `CLAUDE_PROJECT_DIR` 환경변수 자동 제공; plugin config `${CLAUDE_PROJECT_DIR}` 참조 가능
- (v2.1.139) 서브에이전트 API 요청에 `x-claude-code-agent-id`/`x-claude-code-parent-agent-id` 헤더 + OTEL span 속성 추가
- (v2.1.136) `settings.autoMode.hard_deny` — auto mode 무조건 차단 규칙
- (v2.1.133) Hook `effort.level` JSON 입력 필드 + `$CLAUDE_EFFORT` env var (Bash 서브프로세스 포함)
- (v2.1.133) `worktree.baseRef` 설정 (`fresh` | `head`) — worktree 브랜치 기준점 선택
- (v2.1.133) `sandbox.bwrapPath` / `sandbox.socatPath` 관리형 설정 — 커스텀 bubblewrap·socat 경로
- (v2.1.133) `parentSettingsBehavior` admin-tier 키 (`'first-wins' | 'merge'`)
- (v2.1.132) `CLAUDE_CODE_SESSION_ID` — Bash 서브프로세스 환경에 세션 ID 자동 제공
- (v2.1.132) `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` — 풀스크린 렌더러 비활성화, 네이티브 스크롤백 유지
- (v2.1.129) `--plugin-url <url>` — 세션 전용 플러그인 .zip URL 즉시 로드
- (v2.1.129) `skillOverrides` 설정 정상 동작 — `off` / `user-invocable-only` / `name-only`
- (v2.1.129) `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` / `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` 신규 env var
- (v2.1.128) `workspace`는 MCP 예약 서버 이름 — 기존 서버 경고 후 스킵

**Breaking Changes:**
- `worktree.baseRef` 기본값 `"fresh"` — `EnterWorktree` 기준점 `origin/<default>` (v2.1.133); 미푸시 커밋 유지 시 `"head"` 설정

**주요 버그 수정:**
- `/goal` `disableAllHooks`/`allowManagedHooksOnly` 설정 시 무한 대기 수정 (v2.1.140)
- settings hot-reload 심볼릭 링크 파일 변경 이벤트 오귀속 수정 (v2.1.140)
- `claude --bg` 유휴 종료 직전 연결 오류 수정 (v2.1.140)
- Remote managed settings 401 force-refresh 재시도 (v2.1.140)
- `/loop` 중복 wakeup 폴링 수정 (v2.1.140)
- `Read` 도구 `offset` 공백/`+` 접두사 허용 (v2.1.140)
- `/clear` 후 MCP 서버(`.mcp.json`·플러그인·claude.ai 커넥터) 사라지는 버그 수정 (v2.1.136)
- Plan mode `Edit(...)` allow 규칙 시 파일 쓰기 차단 수정 (v2.1.136)

---

### v2.1.126 (2026-05-03 동기화)

**새로운 기능:**
- (v2.1.126) `claude project purge [path]` — 프로젝트 전체 상태(트랜스크립트·태스크·파일 이력·설정 엔트리) 삭제; `--dry-run`, `-y/--yes`, `-i/--interactive`, `--all` 지원
- (v2.1.126) `/model` 피커에서 `ANTHROPIC_BASE_URL` Anthropic 호환 게이트웨이의 `/v1/models` 엔드포인트 모델 목록 표시
- (v2.1.126) `claude auth login` OAuth 코드 터미널 직접 붙여넣기 — WSL2·SSH·컨테이너 환경 브라우저 콜백 불가 시 대응
- (v2.1.126) `claude_code.skill_activated` OTel 이벤트 신규 `invocation_trigger` 속성 (`"user-slash"`, `"claude-proactive"`, `"nested-skill"`)
- (v2.1.126) Auto mode 스피너 — 권한 확인 지연 시 빨간색으로 전환 (도구 실행 중 오인 방지)
- (v2.1.126) `--dangerously-skip-permissions` 확장 — `.claude/`, `.git/`, `.vscode/`, 셸 설정 파일 쓰기 프롬프트 생략 (재앙적 명령은 계속 프롬프트)
- (v2.1.126) Windows: Microsoft Store·PATH 미등록 MSI·`.NET global tool` 경로 PowerShell 7 자동 탐지; PowerShell 도구 활성화 시 기본 셸로 사용
- (v2.1.122) `ANTHROPIC_BEDROCK_SERVICE_TIER` env var — Bedrock 서비스 티어 선택 (`default`, `flex`, `priority`); `X-Amzn-Bedrock-Service-Tier` 헤더로 전송
- (v2.1.122) `/resume` 검색창 PR URL 붙여넣기로 해당 PR 생성 세션 탐색 (GitHub·GitHub Enterprise·GitLab·Bitbucket)
- (v2.1.122) OpenTelemetry `claude_code.at_mention` 로그 이벤트 — `@`-멘션 해결 추적
- (v2.1.122) `/mcp` — 중복 URL 수동 서버로 숨겨진 claude.ai 커넥터 표시 + 중복 제거 힌트

**보안 수정:**
- `allowManagedDomainsOnly`·`allowManagedReadPathsOnly` — 상위 관리형 설정 소스에 `sandbox` 블록 없을 때 무시되던 버그 수정 (v2.1.126)

**주요 버그 수정:**
- 2000px 초과 이미지 붙여넣기 시 세션 중단 → 자동 다운스케일·히스토리 과대 이미지 자동 제거·재시도 (v2.1.126)
- `context: fork` 스킬·서브에이전트 첫 턴에 지연 로드 도구(WebSearch·WebFetch 등) 누락 수정 (v2.1.126)
- Windows CJK 텍스트 no-flicker 모드에서 깨진 문자 수정 (v2.1.126)
- `Ctrl+L` 프롬프트 입력 클리어 → 화면 강제 재드로우만 수행 (readline 동작 일치, v2.1.126)
- Mac 수면 해제 후 "Stream idle timeout" 수정; 백그라운드·원격 세션 긴 thinking 중 잘못된 타임아웃 수정 (v2.1.126)
- OAuth 로그인 타임아웃 — slow·proxy·IPv6-only devcontainer·WSL2 브라우저 콜백 실패 수정 (v2.1.126)
- Agent SDK 병렬 도구 호출 배치에서 잘못된 도구 이름 방출 시 hang 수정 (v2.1.126)
- ToolSearch — nonblocking 모드 세션 시작 후 연결 MCP 도구 누락 수정 (v2.1.122)
- settings.json 잘못된 훅 항목 시 전체 파일 무효화 수정 (v2.1.122)
- OAuth 인증 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` 설정 시 401 루프 수정 (v2.1.123)

---

### v2.1.121 (2026-04-28 동기화)

**새로운 기능:**
- (v2.1.121) `alwaysLoad` MCP 서버 설정 옵션 — `true` 시 해당 서버 모든 도구 tool-search 지연 없이 항상 로드
- (v2.1.121) MCP 서버 시작 일시 오류 시 최대 3회 자동 재시도 (이전: 연결 끊긴 채 유지)
- (v2.1.121) `claude plugin prune` — 고아 자동 설치 플러그인 의존성 제거; `plugin uninstall --prune` 연쇄 삭제
- (v2.1.121) `/skills` 필터 검색박스 — 긴 스킬 목록에서 타이핑으로 검색, 스크롤 불필요
- (v2.1.121) PostToolUse hooks `hookSpecificOutput.updatedToolOutput` — 모든 도구에서 tool output 교체 지원 (기존 MCP 전용→전체 확장)
- (v2.1.121) `--dangerously-skip-permissions` — `.claude/skills/`, `.claude/agents/`, `.claude/commands/` 쓰기 프롬프트 스킵
- (v2.1.121) SDK `mcp_authenticate` `redirectUri` 파라미터 — 커스텀 스킴 완료 및 claude.ai 커넥터 지원
- (v2.1.121) OpenTelemetry: `stop_reason`, `gen_ai.response.finish_reasons`, `user_system_prompt` (`OTEL_LOG_USER_PROMPTS` 게이팅) LLM span 필드 추가
- (v2.1.121) Vertex AI: X.509 인증서 기반 Workload Identity Federation (mTLS ADC) 지원
- (v2.1.120) Windows: Git Bash 불필요 — 미설치 시 PowerShell을 셸 도구로 자동 사용
- (v2.1.120) `claude ultrareview [target]` CLI 서브커맨드 — CI/스크립트 비대화형 실행; `--json` raw output; exit 0/1
- (v2.1.120) `${CLAUDE_EFFORT}` — Skill 콘텐츠에서 현재 effort 레벨 동적 참조 가능
- (v2.1.120) `AI_AGENT` 환경변수 서브프로세스 자동 설정 — `gh` 등이 Claude Code 트래픽 귀속
- (v2.1.120) `claude plugin validate` — `marketplace.json` 최상위 `$schema`·`version`·`description`, `plugin.json` `$schema` 허용

**주요 버그 수정:**
- 다수 이미지 세션 멀티-GB RSS 무제한 메모리 증가 수정 (v2.1.121)
- `/usage` 대용량 트랜스크립트 히스토리 ~2GB 메모리 누수 수정 (v2.1.121)
- Bash 도구 — 시작 디렉토리 삭제·이동 시 영구 비활성화 버그 수정 (v2.1.121)
- `--resume` 비정상 종료로 손상된 트랜스크립트 라인 건너뛰기 (v2.1.121)
- Microsoft 365 MCP OAuth `prompt` 파라미터 중복·미지원 오류 수정 (v2.1.121)
- Esc 중 stdio MCP 도구 호출 시 전체 서버 연결 종료 버그 수정 (v2.1.120)

---

### v2.1.119 (2026-04-26 동기화)

**새로운 기능:**
- (v2.1.119) `/config` 설정 `~/.claude/settings.json` 영속화 — 프로젝트/로컬/정책 우선순위 계층 참여
- (v2.1.119) `prUrlTemplate` 설정 — PR 배지 푸터 커스텀 URL 지정
- (v2.1.119) `CLAUDE_CODE_HIDE_CWD` env var — 시작 로고 작업 디렉토리 숨김
- (v2.1.119) `--from-pr` GitLab MR·Bitbucket PR·GitHub Enterprise URL 지원
- (v2.1.119) `--print` 모드 agent `tools:`/`disallowedTools:` frontmatter 준수
- (v2.1.119) `--agent <name>` built-in agent `permissionMode` 준수
- (v2.1.119) PowerShell 도구 자동 승인 — Bash와 동일 권한 모드
- (v2.1.119) Hooks: PostToolUse·PostToolUseFailure에 `duration_ms` 필드 추가
- (v2.1.119) 서브에이전트·SDK MCP 서버 재구성 시 병렬 연결
- (v2.1.119) Status line stdin JSON에 `effort.level`·`thinking.enabled` 추가
- (v2.1.119) Security: `blockedMarketplaces` hostPattern/pathPattern 적용 수정
- (v2.1.118) vim visual mode `v`/visual-line mode `V`
- (v2.1.118) `/usage` — `/cost`+`/stats` 통합
- (v2.1.118) Custom themes (`/theme`, `~/.claude/themes/`, plugin `themes/`)
- (v2.1.118) Hooks → MCP 도구 직접 실행 (`type: "mcp_tool"` 타입)
- (v2.1.118) `DISABLE_UPDATES` env var — 전체 업데이트 경로 차단
- (v2.1.118) `wslInheritsWindowsSettings` 정책
- (v2.1.118) `claude plugin tag` 명령
- (v2.1.117) Agent frontmatter `mcpServers` — `--agent` 세션 MCP 서버 로드
- (v2.1.117) `CLAUDE_CODE_FORK_SUBAGENT=1` — 외부 빌드 forked subagents 활성화
- (v2.1.117) Pro/Max Opus 4.6·Sonnet 4.6 기본 effort `high`

**주요 버그 수정:**
- vim INSERT Esc — 대기 메시지 입력창으로 당기지 않음; 다시 Esc로 중단 (v2.1.119)
- 비활성화된 MCP 서버가 `/status`에서 "failed"로 표시되는 버그 수정 (v2.1.119)
- async PostToolUse hooks 응답 없을 때 빈 트랜스크립트 항목 작성 버그 수정 (v2.1.119)
- `/skills` Enter 키가 다이얼로그를 닫는 버그 수정 (v2.1.119)
- `TaskList` 파일시스템 순서 대신 ID 정렬 반환 (v2.1.119)
- MCP OAuth `expires_in` 누락 시 매 시간 재인증 필요 버그 수정 (v2.1.118)
- credential 저장 크래시로 `~/.claude/.credentials.json` 손상 수정 (v2.1.118)

---

### v2.1.114 (2026-04-18 동기화)

**새로운 기능:**
- (v2.1.113) CLI 네이티브 바이너리 스폰으로 전환 — 번들 JS 대신 플랫폼별 optional dependency 실행
- (v2.1.113) `sandbox.network.deniedDomains` 설정 — 광역 허용 도메인 와일드카드 내 특정 도메인 차단
- (v2.1.113) Esc로 `/loop` 대기 wakeup 취소; wakeup 표시 메시지 개선
- (v2.1.113) 서브에이전트 스트림 정지 시 10분 후 명확한 오류 반환 — 무한 행 방지
- (v2.1.111) Claude Opus 4.7 `xhigh` effort 레벨 — high~max 사이
- (v2.1.111) Auto mode — Max 구독자 Opus 4.7 지원; `--enable-auto-mode` 플래그 불필요
- (v2.1.111) `/effort` 인터랙티브 슬라이더 (인자 없이 호출 시 화살표 키 탐색)
- (v2.1.111) "Auto (match terminal)" 테마 옵션
- (v2.1.111) `/ultrareview` — 클라우드 병렬 멀티에이전트 코드리뷰
- (v2.1.111) `/less-permission-prompts` — 읽기 전용 Bash·MCP 허용 리스트 자동 제안
- (v2.1.111) `OTEL_LOG_RAW_API_BODIES` env var — API 요청·응답 전체 OTEL 로그
- (v2.1.111) `CLAUDE_CODE_USE_POWERSHELL_TOOL` — PowerShell 도구 옵트인
- (v2.1.111) plan 파일 프롬프트 기반 이름 자동 생성
- (v2.1.110) `/tui` 명령 및 `tui` 설정 — 플리커 없는 풀스크린 렌더링
- (v2.1.110) Push notification tool
- (v2.1.110) `/focus` 명령 — 포커스 뷰 토글 (`Ctrl+O`는 verbose 전용 분리)
- (v2.1.110) `autoScrollEnabled` 설정

**보안 강화 (v2.1.113):**
- Bash deny 규칙 — env/sudo/watch/ionice/setsid 래퍼 명령 매칭
- `Bash(find:*)` allow 규칙이 `find -exec`/`-delete` 자동 승인 불가
- macOS `/private/{etc,var,tmp,home}` 경로 `Bash(rm:*)` 위험 경로 처리
- Bash 멀티라인 첫 줄 주석 시 전체 명령 표시 — UI 스푸핑 차단

**주요 버그 수정:**
- Agent Teams 팀메이트 도구 권한 요청 시 권한 다이얼로그 크래시 수정 (v2.1.114)
- MCP 동시 호출 타임아웃 핸들링 — 한 도구 응답이 다른 호출 watchdog 해제 버그 수정 (v2.1.113)
- claude-opus-4-7 auto mode 사용 불가 수정 (v2.1.112)
- `Cmd-backspace`/`Ctrl+U` 커서 앞 텍스트 삭제 복원 (v2.1.113)

---

### v2.1.109 (2026-04-15 동기화)

**새로운 기능:**
- (v2.1.109) extended-thinking 표시기 로테이팅 진행 힌트 개선
- (v2.1.108) `ENABLE_PROMPT_CACHING_1H` env var — API key·Bedrock·Vertex·Foundry 1시간 프롬프트 캐시 TTL 옵트인 (`ENABLE_PROMPT_CACHING_1H_BEDROCK` deprecated·honored); `FORCE_PROMPT_CACHING_5M` — 5분 TTL 강제
- (v2.1.108) `/recap` 명령 — 세션 복귀 시 컨텍스트 요약; `/config`에서 설정, `CLAUDE_CODE_ENABLE_AWAY_SUMMARY`로 강제
- (v2.1.108) Skill tool로 내장 슬래시 명령 자동 탐색·실행 (`/init`, `/review`, `/security-review`)
- (v2.1.108) `/undo` — `/rewind` 별칭
- (v2.1.108) `/model` 전환 전 미캐시 경고 — 전체 히스토리 미캐시 안내
- (v2.1.108) `/resume` 피커 현재 디렉토리 기본 표시; `Ctrl+A` 전체 표시
- (v2.1.108) 오류 메시지 개선 — rate limit vs plan limit 구분, 5xx/529 → status.claude.com 링크, 미지원 명령 유사어 제안
- (v2.1.108) 언어 문법 온디맨드 로드 — 파일 읽기·편집·구문 강조 메모리 절약
- (v2.1.108) 상세 트랜스크립트(`Ctrl+O`) "verbose" 표시기
- (v2.1.108) `DISABLE_PROMPT_CACHING*` 설정 시 시작 경고

**주요 버그 수정:**
- `/login` 코드 입력 붙여넣기 미작동 수정 (v2.1.108, 2.1.105 회귀)
- `DISABLE_TELEMETRY` 설정 구독자 캐시 TTL 폴백 오류 수정 (v2.1.108)
- `CLAUDE_ENV_FILE` `#` 주석 줄 종료 시 Bash 도구 출력 없음 수정 (v2.1.108)
- `--resume <id>` 세션 커스텀 이름·색상 유실 수정 (v2.1.108)
- `/feedback` Enter 재제출 미작동 수정 (v2.1.108)
- 응답 중 다이어크리틱 문자(악센트·움라우트 등) 누락 수정 (v2.1.108, `language` 설정 시)
- 정책 관리 플러그인 다른 프로젝트 설치 시 자동 업데이트 안 됨 수정 (v2.1.108)

---

### v2.1.107 (2026-04-14 동기화)

**새로운 기능:**
- (v2.1.107) 긴 작업 중 thinking 힌트 더 빨리 표시
- (v2.1.105) `PreCompact` Hook 차단 지원 — exit code 2 또는 `{"decision":"block"}` 반환으로 컨텍스트 압축 차단 가능
- (v2.1.105) 플러그인 `monitors` 매니페스트 최상위 키 — 세션 시작/스킬 invoke 시 백그라운드 모니터 자동 실행
- (v2.1.105) `EnterWorktree` `path` 파라미터 — 현재 레포의 기존 worktree로 전환
- (v2.1.105) `/proactive` — `/loop` 별칭
- (v2.1.105) 스킬 설명 최대 길이 250 → 1,536자; 초과 시 시작 경고
- (v2.1.105) `WebFetch` `<style>`·`<script>` 태그 내용 제거 — CSS/JS 헤비 페이지 컨텍스트 예산 보호
- (v2.1.105) MCP 대용량 출력 truncation 프롬프트 — JSON(`jq`), 텍스트(청크 계산) 등 포맷별 처리 레시피
- (v2.1.105) 스트림 5분 무응답 시 자동 중단 후 non-streaming 재시도
- (v2.1.105) `/doctor` 레이아웃 개선: 상태 아이콘 + `f` 키로 자동 수정

**주요 버그 수정:**
- 대기열 메시지에 첨부된 이미지 유실 수정 (v2.1.105)
- 긴 대화에서 프롬프트 입력 줄바꿈 시 화면 공백 수정 (v2.1.105)
- 멀티라인 응답 선택 시 선행 공백 복사 수정 (v2.1.105)
- ASCII 아트·들여쓰기 다이어그램 선행 공백 삭제 수정 (v2.1.105)
- one-shot 예약 작업 반복 재실행 수정 (v2.1.105)
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 전체 프로젝트 지표 비활성화 수정 (v2.1.105)
- MCP tools가 headless/remote-trigger 세션 첫 턴에 누락되는 버그 수정 (v2.1.105)
- AWS Bedrock 비US 리전 `/model` 피커에서 잘못된 `us.*` 모델 ID 저장 수정 (v2.1.105)
- 429 rate-limit 오류에서 raw JSON 덤프 대신 깔끔한 메시지 표시 (v2.1.105)

---

### v2.1.101 (2026-04-12 동기화)

**새로운 기능:**
- `/team-onboarding` 명령 — 로컬 Claude Code 사용 이력 기반 팀원 온보딩 가이드 자동 생성
- OS CA 인증서 저장소 기본 신뢰 — 엔터프라이즈 TLS 프록시 별도 설정 불필요 (`CLAUDE_CODE_CERT_STORE=bundled`로 비활성화)
- `/ultraplan` 및 원격 세션 기능: 웹 설정 없이 기본 클라우드 환경 자동 생성
- settings.json 복원력 — 알 수 없는 훅 이벤트 이름이 전체 파일 무시를 유발하지 않도록 개선
- `claude -p --resume <name>` — `/rename`·`--name`으로 설정한 세션 제목으로 재개 지원
- beta 추적 `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT` 환경변수 지원
- SDK `query()` — `for await` break 또는 `await using` 시 서브프로세스·임시 파일 자동 정리
- (v2.1.98) Google Vertex AI 인터랙티브 설정 마법사 (로그인 화면 "3rd-party platform")
- (v2.1.98) `CLAUDE_CODE_PERFORCE_MODE` — 읽기 전용 파일 편집 시 `p4 edit` 힌트
- (v2.1.98) `Monitor` 도구 — 백그라운드 스크립트 이벤트 스트리밍
- (v2.1.98) `workspace.git_worktree` status line JSON 입력 필드
- (v2.1.98) `--exclude-dynamic-system-prompt-sections` print mode 플래그
- (v2.1.97) focus view 토글 (`Ctrl+O`, `NO_FLICKER` 모드)
- (v2.1.97) `refreshInterval` status line 재실행 주기 설정
- (v2.1.94) `CLAUDE_CODE_USE_MANTLE=1` — Amazon Bedrock Mantle 지원
- (v2.1.94) `keep-coding-instructions` frontmatter 필드
- (v2.1.94) `hookSpecificOutput.sessionTitle` — `UserPromptSubmit` Hook에서 세션 제목 설정
- (v2.1.94) `"skills": ["./"]` 선언 시 frontmatter `name`으로 호출명 결정

**Breaking Changes:**
- 기본 effort 레벨 medium → **high** 전환 (API키·Bedrock·Vertex·Foundry·Team·Enterprise 사용자, v2.1.94)

**주요 버그 수정:**
- LSP binary 탐지 POSIX `which` 폴백 명령 인젝션 취약점 수정 (보안)
- 장기 세션 메모리 누수 (가상 스크롤러 메시지 목록 중복 저장) 수정
- `--resume`/`--continue` 대용량 세션 대화 컨텍스트 유실 수정
- 서브에이전트가 동적 주입 MCP 서버 도구를 상속받지 못하던 버그 수정
- 격리된 worktree 서브에이전트의 자신 worktree 파일 Read/Edit 거부 수정
- 하드코딩된 5분 요청 타임아웃 수정 (`API_TIMEOUT_MS` 적용)
- `permissions.deny` 규칙이 `PreToolUse` hook의 `permissionDecision: "ask"` 다운그레이드를 방지
- Grep 도구 내장 ripgrep 바이너리 stale 시 시스템 `rg` 폴백 + 자동 복구
- (v2.1.98) Bash 도구 백슬래시 이스케이프 플래그 권한 우회·복합 명령 강제 프롬프트 우회 수정
- (v2.1.98) 429 재시도 지수 백오프 최솟값 적용 (소형 `Retry-After` 시 시도 소진 방지)

---

### v2.1.92 (2026-04-07 동기화)

**새로운 기능:**
- `forceRemoteSettingsRefresh` 정책 — CLI 시작 시 원격 managed settings 최신화 강제, 실패 시 종료 (fail-closed)
- Bedrock 인터랙티브 설정 마법사 — 로그인 화면 "3rd-party platform" 선택 시 AWS 인증·리전·자격증명·모델 핀닝 단계별 안내
- `/cost` 구독 사용자 대상 모델별·캐시 히트 별 비용 세부 내역 표시
- `/release-notes` 인터랙티브 버전 피커로 전환
- Remote Control 세션 이름 호스트명 기반 기본 접두사; `--remote-control-session-name-prefix`로 오버라이드
- Pro 사용자: 프롬프트 캐시 만료 후 세션 복귀 시 미캐시 토큰 수 푸터 힌트
- (v2.1.91) MCP `_meta["anthropic/maxResultSizeChars"]` — 도구 결과 최대 500K 허용 (DB 스키마 등 대용량)
- (v2.1.91) `disableSkillShellExecution` 설정 — Skills/슬래시 명령/플러그인 인라인 셸 실행 비활성화
- (v2.1.91) 플러그인 `bin/` 실행 파일 지원 — Bash 도구에서 bare command 실행
- (v2.1.91) `claude-cli://open?q=` 딥 링크 멀티라인 프롬프트 지원

**Breaking Changes:**
- `/tag` 명령 제거 (v2.1.92)
- `/vim` 명령 제거 — vim 모드 토글은 `/config` → Editor mode 사용 (v2.1.92)

**주요 버그 수정:**
- 서브에이전트 생성 시 tmux 창 재번호 후 "Could not determine pane count" 영구 실패 수정
- prompt-type Stop Hook에서 소형 빠른 모델 `ok:false` 반환 시 잘못 실패하던 버그; `preventContinuation:true` 시맨틱 복원
- Write 도구 대용량 파일 diff 계산 60% 속도 향상 (탭/`&`/`$` 포함 파일)
- Linux sandbox `apply-seccomp` 헬퍼 npm·네이티브 빌드 모두 포함
- (v2.1.91) `--resume` 비동기 트랜스크립트 쓰기 실패로 대화 이력 유실 수정
- (v2.1.91) Edit 도구 `old_string` 앵커 단축으로 출력 토큰 절감

---

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
