# ccbuilder: Claude Code 확장을 몇 초 만에 만드는 플러그인의 모든 것

> Skills, Hooks, Agents, Agent Teams, Ralph Loops — 하나의 플러그인으로 Claude Code 확장 생태계를 완전 정복하다

**Published**: 2026-02-13
**Author**: Cathy Kim
**Version**: ccbuilder v2.10.0

---

## Claude Code 확장 개발, 왜 이렇게 어려울까?

Claude Code는 강력하다. 하지만 확장을 직접 만들려면 현실은 다르다.

- **20개 이상의 공식 문서** 페이지를 넘나들며 정보를 조합해야 하고
- **정확한 파일 구조와 YAML frontmatter** 형식을 매번 기억해야 하며
- **커뮤니티에서 이미 만들어진 수백 개의 패턴**을 몰라서 바퀴를 다시 발명하고
- 결국 "이건 Skill로 만들어야 하나? Hook으로? Agent로?" 라는 **근본적인 질문**에서 막힌다

이 모든 문제를 해결하기 위해 **ccbuilder**를 만들었다.

```bash
claude plugin install github:cathy-kim/ccbuilder
```

한 줄이면 설치 끝. 그 다음부터는 `/ccbuilder skill my-skill` 한 번으로 완성된 스캐폴딩이 생성된다.

---

## ccbuilder가 뭔가요?

ccbuilder는 **Claude Code Extension Builder Plugin**이다. 단순한 템플릿 생성기가 아니라, Claude Code 확장 개발에 필요한 **지식 체계 전체**를 하나의 플러그인에 담았다.

### 핵심 수치

| 항목 | 수치 |
|------|------|
| 지원 확장 유형 | 7종 (Skill, Hook, Agent, Agent Team, Ralph Loop, Memory, Rules) |
| 내장 레퍼런스 | 33개 가이드 |
| 공식 문서 요약 | 6개 파일 |
| 커뮤니티 레포 | 11개 Git Submodule (339+ skills, 126+ subagents, 112 agents) |
| 릴리즈 히스토리 | 13개 버전 (v1.0.0 ~ v2.10.0) |

### 사용법

슬래시 명령으로 직접 호출하거나:

```
/ccbuilder skill react-patterns      # Skill 스캐폴딩
/ccbuilder hook PreToolUse           # Hook 구현
/ccbuilder agent code-reviewer       # Agent 정의
/ccbuilder team feature-dev          # Agent Team 구성
/ccbuilder ralph my-project          # Ralph Loop (자율 개발 루프) 설정
```

또는 자연어로 대화하면 **자동 활성화**된다:

> "React 패턴 가이드를 만들어줘" → Skill 생성 흐름 자동 진입
> "민감 파일 수정을 차단해줘" → Hook 생성 흐름 자동 진입
> "야간에 자율 개발시켜줘" → Ralph Loop 설정 흐름 자동 진입

---

## 파일은 어디에 배치해야 할까? — "What Goes Where" 결정 트리

Claude Code 확장 개발에서 가장 흔한 실수는 **"어디에 뭘 적어야 하는지 모르는 것"**이다. ccbuilder에는 이 문제를 해결하는 전용 가이드가 내장되어 있다.

### 핵심 결정 트리

```
사용자가 원하는 것이 무엇인가?

├─ "프로젝트 전체에 항상 적용될 규칙"
│   ├─ 팀 공유 필요? → CLAUDE.md (Git 커밋)
│   ├─ 내 로컬만? → CLAUDE.local.md
│   └─ 특정 경로에서만? → .claude/rules/*.md
│
├─ "반복적으로 사용할 지침/가이드"
│   └─ Skill (.claude/skills/<name>/SKILL.md)
│
├─ "특정 역할의 독립 에이전트"
│   └─ Agent (.claude/agents/<name>.md)
│
├─ "이벤트에 자동 반응"
│   └─ Hook (settings.json + 스크립트)
│
├─ "여러 에이전트가 협업"
│   └─ Agent Team (TeamCreate → Task → SendMessage)
│
├─ "장시간 자율 개발 (30분+)"
│   └─ Ralph Loop (TASK.md + loop.sh)
│
└─ "외부 서비스/API 연동"
    └─ MCP Server (.mcp.json)
```

### 실전 매핑 테이블

| 이렇게 말하면... | 여기에 만든다 | 이유 |
|------------------|--------------|------|
| "TypeScript만 써야 해" | **CLAUDE.md** | 프로젝트 전체 규칙 |
| "프론트엔드는 함수형만" | **.claude/rules/frontend.md** | 특정 경로만 적용 |
| "내 로컬 DB는 5432야" | **CLAUDE.local.md** | 개인 환경, Git 제외 |
| "React 패턴 가이드" | **Skill** | 반복 사용 지식, 호출 시만 로드 |
| "코드 리뷰 에이전트" | **Agent** | 독립 실행 에이전트 |
| "민감 파일 수정 차단" | **Hook** | 이벤트 반응 자동화 |
| "프론트+백엔드 병렬 개발" | **Agent Team** | 멀티 에이전트 협업 |
| "야간 자율 개발" | **Ralph Loop** | Fresh Context 자율 루프 |

### 흔한 실수와 올바른 접근

```
❌ CLAUDE.md에 300줄짜리 React 패턴 가이드
   → 매 세션마다 토큰 낭비
✅ Skill로 분리 → 필요할 때만 로드

❌ Skill로 "TypeScript 필수" 1줄 규칙
   → 과도한 구조
✅ CLAUDE.md에 한 줄로 작성

❌ CLAUDE.md에 "프론트엔드만 적용" 규칙
   → 백엔드 작업 시 불필요한 노이즈
✅ .claude/rules/frontend.md + paths: "src/frontend/**"
```

---

## 복잡한 Workflow는 어떻게 설계할까?

ccbuilder가 지원하는 7가지 확장 유형은 **조합**할 때 진짜 힘을 발휘한다.

### Workflow 1: 단일 Skill — 반복 지식 주입

가장 기본적인 패턴. "React 패턴 가이드", "API 설계 표준" 같은 반복 사용 지식을 `/my-skill` 한 번으로 주입.

```
/my-skill → SKILL.md 로드 → 필요시 references/ 참조 → 대화에 반영
```

**핵심**: 500줄 규칙 (Progressive Disclosure). SKILL.md는 개요만, 상세는 `references/`에.

### Workflow 2: Hook 자동화 — 이벤트 기반 워크플로우 제어

14가지 라이프사이클 이벤트에 자동 반응:

```
SessionStart → 환경 검증
PreToolUse → 위험 명령 차단 (rm -rf, force push 등)
PostToolUse → 자동 린트, 테스트
Stop → 커밋 메시지 생성, 리포트 작성
```

### Workflow 3: Agent Team — 병렬 협업

Frontend, Backend, Test 에이전트가 동시에 작업:

```
1. TeamCreate("feature-team")
2. TaskCreate("Build API") + TaskCreate("Build UI") + TaskCreate("Write Tests")
3. Task(name: "api-dev", prompt: "API 구현") → 병렬 실행
4. Task(name: "ui-dev", prompt: "UI 구현")  → 병렬 실행
5. TaskUpdate(taskId: "3", addBlockedBy: ["1", "2"])  → 테스트는 API+UI 완료 후
6. 완료 후 TeamDelete()
```

### Workflow 4: Ralph Loop — 장시간 자율 개발

30분 이상 걸리는 대규모 작업? 컨텍스트 윈도우 열화 없이 자율 개발:

```
Session 1 → TASK.md 읽기 → 1번 작업 수행 → PROGRESS.md 업데이트 → Git commit
    ↓ (컨텍스트 0% 리셋)
Session 2 → TASK.md + PROGRESS.md 읽기 → 2번 작업 수행 → 업데이트 → commit
    ↓
Session N → LOOP_COMPLETE 감지 → 종료
```

3가지 구현 방법 제공:
1. **Simple Bash Loop** (권장 시작점) — `loop.sh` 하나로 시작
2. **Stop Hook 기반** — Claude Code 내장 Stop Hook 활용
3. **Ralph 프레임워크** — tmux 대시보드, 서킷 브레이커 포함 풀 프레임워크

### Workflow 5: 하이브리드 — Agent Team + Ralph Loop

궁극의 조합. 큰 프로젝트를 서브태스크로 분해하고, 각각을 Ralph Loop로 실행:

```
Agent Team (고수준 분해)
  └─ Ralph Loop (서브태스크별, 각각 Fresh Context)
      ├─ Subtask 1 → 5 iterations → COMPLETE
      ├─ Subtask 2 → 3 iterations → COMPLETE
      └─ Subtask 3 → 7 iterations → COMPLETE
```

---

## 플러그인 내부 구조 — 33개 레퍼런스의 체계

ccbuilder는 단순한 템플릿이 아니다. **체계적으로 구조화된 지식 베이스**다.

### 디렉토리 구조

```
ccbuilder/
├── .claude-plugin/
│   ├── plugin.json           # 플러그인 매니페스트
│   └── marketplace.json      # 마켓플레이스 등록
│
├── skills/ccbuilder/
│   ├── SKILL.md              # 메인 스킬 (490줄, 라우팅 + Quick Reference)
│   └── references/           # 33개 레퍼런스 가이드
│       ├── skills-guide.md           # Skill 개발 완전 가이드
│       ├── hooks-guide.md            # Hook 14 이벤트 가이드
│       ├── subagents-guide.md        # Agent 정의 가이드
│       ├── agent-teams-guide.md      # 멀티 에이전트 팀 가이드
│       ├── ralph-loop-guide.md       # 자율 개발 루프 가이드
│       ├── mcp-guide.md              # MCP 연동 가이드
│       ├── memory-rules-guide.md     # 메모리 & 규칙 가이드
│       ├── what-goes-where-guide.md  # 파일 배치 결정 가이드
│       ├── best-practices.md         # 모범 사례
│       ├── implementation-guide.md   # 구현 패턴
│       ├── orchestrator-principles.md        # 오케스트레이터 원칙
│       ├── orchestrator-skill-creation-guide.md
│       ├── skill-subagent-task-guide.md      # Skill/Agent/Task 비교
│       ├── review-system.md          # 스킬 검증 시스템
│       ├── troubleshooting.md        # 트러블슈팅
│       ├── version-sync.md           # 버전 동기화
│       ├── external-resources.md     # 커뮤니티 리소스
│       │
│       ├── official/                 # 공식 문서 요약 (6개)
│       │   ├── skills.md
│       │   ├── hooks.md
│       │   ├── subagents.md
│       │   ├── mcp.md
│       │   ├── memory-rules.md
│       │   └── tools.md             # 28+ 빌트인 도구 레퍼런스
│       │
│       └── github/                   # 커뮤니티 생태계
│           ├── README.md             # Tier별 레포 인덱스
│           ├── official-repos.md     # T1: Anthropic 공식
│           ├── ecosystem-collections.md  # T2: 10k+ 스타
│           ├── specialized-tools.md  # T3/T4: 특화 도구
│           ├── patterns.md           # 크로스 레포 검증 패턴 10가지
│           └── repos/                # 11개 Git Submodule
│               ├── anthropics-skills/        # 공식 Skill
│               ├── obra-superpowers/         # TDD, 디버깅
│               ├── everything-claude-code/   # 15 agents, 30+ skills
│               ├── wshobson-agents/          # 112 agents
│               ├── awesome-subagents/        # 126+ subagents
│               ├── awesome-agent-skills/     # 339+ skills
│               └── ...
│
├── scripts/                  # 스캐폴딩 스크립트
│   ├── init-skill.sh
│   ├── init-agent.sh
│   ├── init-hook.sh
│   ├── init-ralph.sh         # Ralph Loop 초기화
│   ├── test-hook.sh
│   └── check-updates.sh      # 공식 문서 업데이트 체크
│
├── evaluations/              # 품질 평가 프레임워크
│   ├── test-cases.json       # 5개 테스트 시나리오
│   ├── run_evaluation.py     # 자동 평가 러너
│   └── golden-outputs/       # 기대 출력 레퍼런스
│
└── releases/                 # 13개 버전 스냅샷
```

### Progressive Disclosure 아키텍처

ccbuilder의 핵심 설계 원칙은 **Progressive Disclosure (점진적 노출)**이다.

```
Level 0: 슬래시 명령 → 즉시 스캐폴딩 (사용자 입력 1줄)
Level 1: SKILL.md → 490줄 라우팅 + Quick Reference (기본 지식)
Level 2: references/*.md → 17개 상세 가이드 (심화 지식)
Level 3: references/official/*.md → 6개 공식 문서 요약 (정확한 스펙)
Level 4: references/github/repos/ → 11개 실제 코드 레포 (실전 예시)
```

필요한 만큼만 로드하므로 **토큰 효율이 극대화**된다.

### SKILL.md의 인자 라우팅

SKILL.md는 490줄짜리 "라우터"다. 인자의 첫 번째 토큰을 보고 적절한 레퍼런스를 Read한 후 작업을 수행한다:

```
/ccbuilder skill → skills-guide.md + official/skills.md 읽기 → 스캐폴딩
/ccbuilder hook  → hooks-guide.md + official/hooks.md 읽기 → Hook 생성
/ccbuilder agent → subagents-guide.md + official/subagents.md 읽기 → Agent 정의
/ccbuilder team  → agent-teams-guide.md 읽기 → Team 구성
/ccbuilder ralph → ralph-loop-guide.md 읽기 → Ralph Loop 설정
자연어 질문    → 키워드 추출 → 매칭 문서 읽기 → 답변
```

---

## 버전 히스토리 — 2개월간의 진화

| 버전 | 날짜 | 핵심 변경 |
|------|------|-----------|
| v1.0.0 | 2025-12-23 | 최초 릴리즈 (Skills, Hooks, Agents) |
| v2.0.0 | 2026-01-15 | Agent SDK, 최신 Hook 이벤트 |
| v2.2.0 | 2026-01-24 | Skill ↔ Subagent 양방향 통합 |
| v2.4.0 | 2026-02-04 | 대규모 리팩토링 (14MB → 1.6MB) |
| v2.7.0 | 2026-02-11 | Agent Teams, Memory, Modular Rules |
| v2.9.0 | 2026-02-11 | 공식 문서 요약 + GitHub 생태계 |
| v2.10.0 | 2026-02-13 | Ralph Loop, What-Goes-Where 가이드 |

---

## 시작하기

```bash
# 설치
claude plugin install github:cathy-kim/ccbuilder

# 바로 사용
/ccbuilder skill my-first-skill
/ccbuilder hook PreToolUse
/ccbuilder ralph my-project

# 또는 자연어로
"Hook 이벤트가 뭐가 있어?"
"Skill이랑 Agent 차이가 뭐야?"
"프론트+백엔드 병렬로 개발하고 싶어"
```

---

## 마무리

ccbuilder는 "Claude Code 확장을 어떻게 만들지?"라는 질문에 대한 **원스톱 답변**이다.

- **33개 레퍼런스** — 흩어진 문서를 하나로
- **7가지 확장 유형** — Skill부터 Ralph Loop까지 전부 지원
- **11개 커뮤니티 레포** — 수백 개의 실전 패턴 내장
- **자동 활성화** — 슬래시 명령 없이도 자연어로 동작

Claude Code 확장 개발의 진입 장벽을 몇 시간에서 **몇 초**로 줄이는 것. 그게 ccbuilder의 목표다.

---

*ccbuilder는 MIT 라이센스 오픈소스입니다.*
*GitHub: github.com/cathy-kim/ccbuilder*
