# Claude Code Built-in Tools Reference

> Skill/Agent 개발 시 `allowed-tools`, `disallowedTools` 설정에 참고.
> Source: [claude-code-system-prompts](../github/repos/claude-code-system-prompts/)

**Last Synced**: 2026-03-26 (Claude Code v2.1.84+)

---

## Tool 전체 목록

### Core Tools (파일 + 검색)

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `Read` | 476 | 파일 읽기 (이미지, PDF, ipynb 포함) | 낮음 |
| `Write` | 127 | 파일 생성/덮어쓰기 | **높음** |
| `Edit` | 246 | 파일 내 문자열 치환 | **중간** |
| `Glob` | 122 | 파일명 패턴 매칭 (`**/*.ts`) | 낮음 |
| `Grep` | 300 | 파일 내용 검색 (ripgrep) | 낮음 |
| `NotebookEdit` | 121 | Jupyter 노트북 셀 편집 | 중간 |

### Execution Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `Bash` | 1,067 | Shell 명령 실행 | **높음** |
| `PowerShell` | - | PowerShell 명령 실행 (Windows 옵트인 프리뷰, v2.1.84) | **높음** |
| `Task` | 1,214 | 서브에이전트 실행 | 중간 |
| `Skill` | 326 | Skill 호출 | 낮음 |

### Communication Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `AskUserQuestion` | 194 | 사용자에게 질문 | 낮음 |
| `SendMessage` | 1,241 | 팀메이트 메시지 (Agent Teams) | 낮음 |
| `EndConversation` | - | 학대적 사용자·탈옥 시도 세션 종료 (v2.1.214 신규) | 낮음 |

### Planning Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `EnterPlanMode` | 878 | Plan 모드 진입 | 낮음 |
| `ExitPlanMode` | 417 | Plan 모드 종료/승인 요청 | 낮음 |
| `EnterWorktree` | - | 격리된 git worktree 세션 진입; `path` 파라미터로 기존 worktree 재사용 가능 (v2.1.105); Claude 관리 worktree 간 mid-session 전환 지원 (v2.1.157) | 낮음 |
| `ExitWorktree` | - | EnterWorktree 세션 종료 (v2.1.72) | 낮음 |

### Task Management Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `TaskCreate` | 558 | 작업 생성 | 낮음 |
| `TaskUpdate` | - | 작업 상태 변경 | 낮음 |
| `TaskList` | 133+ | 작업 목록 조회 | 낮음 |
| `TaskGet` | - | 작업 상세 조회 | 낮음 |
| `TaskOutput` | - | 백그라운드 태스크 출력 — **Deprecated** (v2.1.83): `Read`로 출력 파일 경로 직접 읽기 | 낮음 |
| `TodoWrite` | 2,167 | 체크리스트 관리 (레거시) | 낮음 |

### Team Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `TeamCreate` | 1,642 | 팀 생성 | 중간 |
| `TeamDelete` | 154 | 팀 삭제 | 중간 |

### Web Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `WebFetch` | 297 | URL 내용 가져오기 | 낮음 |
| `WebSearch` | 331 | 웹 검색 | 낮음 |

### Special Tools

| Tool | Tokens | 용도 | 위험도 |
|------|--------|------|--------|
| `Computer` | 161 | Chrome 브라우저 자동화 | **높음** |
| `LSP` | 255 | Language Server Protocol | 낮음 |
| `ToolSearch` | 144+690 | MCP 도구 검색/로드 | 낮음 |
| `Sleep` | 154 | 대기 (사용자 입력 시 깨어남) | 낮음 |

---

## Skill/Agent별 권장 Tool 조합

### 읽기 전용 (리서치, 분석)

```yaml
allowed-tools: [Read, Glob, Grep, WebFetch, WebSearch]
```

### 코드 수정 (개발)

```yaml
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
```

### 최소 권한 (안전)

```yaml
allowed-tools: [Read, Glob, Grep]
```

### 팀 협업 (Agent Teams)

```yaml
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet]
```

### 위험 도구 차단 (disallowedTools)

```yaml
disallowedTools: [Bash, Write, Computer]
```

---

## Tool 선택 가이드

```
Q: Agent가 파일을 수정해야 하나?
├─ Yes → Edit, Write 포함
│  Q: Shell 명령도 필요한가?
│  ├─ Yes → Bash 포함 (주의: 가장 높은 위험도)
│  └─ No → Edit, Write만
└─ No → Read, Glob, Grep만 (읽기 전용)

Q: 웹 접근이 필요한가?
├─ Yes → WebFetch, WebSearch 포함
└─ No → 제외

Q: 서브에이전트를 생성해야 하나?
├─ Yes → Task 포함
│  Q: Agent Teams 사용?
│  ├─ Yes → SendMessage, TeamCreate, Task* 도구 추가
│  └─ No → Task만
└─ No → 제외
```

---

## 권한 규칙 주의사항 (v2.1.210)

`Write(path)`, `NotebookEdit(path)`, `Glob(path)` 형태의 permission 규칙은 시작 시 경고를 표시합니다 — 이 도구들은 경로 인자를 규칙 매칭에 사용하지 않으므로 의도한 대로 동작하지 않습니다. 대신 `Edit(path)`(쓰기 제어), `Read(path)`(읽기 제어)를 사용하세요.

## 버그 수정 (v2.1.208-217)

- `Read`가 빈 파일을 "shorter than offset"로 잘못 보고하던 버그 수정 (v2.1.208)
- `Grep`이 잘못된 정규식 패턴에 "No matches found"를 반환하던 버그, count 모드 페이지네이션 시 총계 과소 집계 버그 수정 (v2.1.208)
- `Glob`이 패턴/경로/작업 디렉토리에 null byte 포함 시 불명확한 오류로 크래시하던 버그 수정 (v2.1.208)
- `Edit`이 Read 이후 파일이 수정되어도 대상 텍스트가 여전히 고유하게 일치하면 실패하던 버그 수정 (v2.1.208)
- 매우 긴 단일 라인 파일을 offset/limit으로 읽을 때 발생하던 메모리 블로우업 수정 — 이제 깔끔한 오류 반환 (v2.1.208)
- Bash/PowerShell 타임아웃 메시지가 자동 백그라운드 전환과 명시적 백그라운드 요청을 구분하도록 개선 (v2.1.210)

## 상세 참조

각 Tool의 전체 시스템 프롬프트(파라미터, 사용 규칙)는 로컬 submodule에서 직접 확인:

```
Read refs/github/repos/claude-code-system-prompts/system-prompts/tool-description-bash.md
Read refs/github/repos/claude-code-system-prompts/system-prompts/tool-description-edit.md
Read refs/github/repos/claude-code-system-prompts/system-prompts/tool-description-task.md
```

전체 Tool 목록: `Glob "tool-description-*.md" in refs/github/repos/claude-code-system-prompts/system-prompts/`
