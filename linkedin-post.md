# LinkedIn Post — ccbuilder v2.10.0

---

## Post (한국어)

---

**Claude Code 확장을 만들고 싶은데, 뭘 어디에 만들어야 할지 모르겠다면?**

ccbuilder v2.10.0을 공개합니다 — Claude Code Extension Builder Plugin.

Skills, Hooks, Agents, Agent Teams, Ralph Loops.
하나의 플러그인으로 Claude Code 확장 생태계 전체를 커버합니다.

설치: `claude plugin install github:cathy-kim/ccbuilder`

---

### 1. 파일 배치: "뭘 어디에 만들지?" 결정 트리

Claude Code 확장 개발에서 가장 흔한 실수가 "잘못된 곳에 만드는 것"입니다.

300줄짜리 React 가이드를 CLAUDE.md에 넣으면? 매 세션마다 토큰 낭비.
1줄짜리 규칙을 Skill로 만들면? 과도한 구조.

ccbuilder에는 이런 실수를 방지하는 **What-Goes-Where 결정 트리**가 내장되어 있습니다:

```
"프로젝트 전체 규칙"        → CLAUDE.md
"특정 경로에서만 적용"      → .claude/rules/ (paths: frontmatter)
"반복 사용할 상세 가이드"   → Skill (.claude/skills/)
"독립 에이전트"            → Agent (.claude/agents/)
"이벤트 자동 반응"         → Hook (settings.json)
"여러 에이전트 협업"       → Agent Team (TeamCreate)
"장시간 자율 개발"         → Ralph Loop (TASK.md + loop.sh)
"외부 API 연동"           → MCP Server (.mcp.json)
```

핵심 원칙: **항상 적용 = CLAUDE.md, 호출 시만 = Skill, 이벤트 반응 = Hook.**

---

### 2. 복잡한 Workflow 설계: 5가지 패턴

ccbuilder의 7가지 확장은 조합할 때 진짜 힘을 발휘합니다.

**패턴 A — Skill + Hook 조합**
Skill로 코딩 가이드를 주입하고, Hook(PreToolUse)으로 규칙 위반을 자동 차단.

**패턴 B — Agent Team (병렬 협업)**
Frontend, Backend, Test 에이전트가 동시 작업. 의존성(blockedBy)으로 순서 제어.

```
TeamCreate → TaskCreate(3개) → Task(3명 병렬) → SendMessage → TeamDelete
```

**패턴 C — Ralph Loop (자율 개발)**
30분+ 대규모 작업을 컨텍스트 열화 없이 자율 실행.

```
Session 1 → 작업 수행 → PROGRESS.md 업데이트 → Git commit
    ↓ (컨텍스트 0% 리셋 — 항상 최적 성능!)
Session 2 → PROGRESS.md 읽기 → 다음 작업 → commit
    ↓
Session N → LOOP_COMPLETE → 종료
```

3가지 구현 방법:
- Simple Bash Loop (5분 세팅)
- Stop Hook 기반 (Claude Code 내장)
- Ralph 프레임워크 (tmux + 서킷 브레이커)

**패턴 D — Agent Team + Ralph (하이브리드)**
큰 프로젝트를 서브태스크로 분해 → 각각 Ralph Loop로 Fresh Context 실행.

**패턴 E — 전체 통합**
CLAUDE.md(규칙) + Rules(경로별) + Skill(가이드) + Hook(자동화) + Agent(전문가) + Team(협업) + Ralph(자율)
— 7개 레이어를 모두 활용한 엔터프라이즈급 워크플로우.

---

### 3. 플러그인 상세 구성: 33개 레퍼런스의 체계

ccbuilder는 단순한 템플릿이 아닙니다. **체계적으로 구조화된 지식 베이스**입니다.

**SKILL.md (490줄) — 라우터 역할**
인자의 첫 토큰을 보고 적절한 레퍼런스를 로드합니다:
- `/ccbuilder skill` → skills-guide.md + official/skills.md
- `/ccbuilder hook` → hooks-guide.md + official/hooks.md
- `/ccbuilder ralph` → ralph-loop-guide.md
- 자연어 → 키워드 추출 → 매칭 문서 자동 로드

**references/ (33개 가이드)**

| 카테고리 | 내용 |
|----------|------|
| **기능별 가이드** (7개) | Skills, Hooks, Agents, Teams, Ralph, MCP, Memory |
| **설계 가이드** (5개) | What-Goes-Where, Orchestrator 원칙, Skill/Agent/Task 비교, 구현 패턴, 모범 사례 |
| **품질 가이드** (3개) | 리뷰 시스템, 트러블슈팅, 버전 동기화 |
| **공식 문서 요약** (6개) | Skills, Hooks, Sub-agents, MCP, Memory, Tools (28+ 도구) |
| **GitHub 생태계** (5개 + 11 레포) | Tier별 레포 분석, 검증 패턴 10가지 |

**11개 Git Submodule — 실제 코드 레퍼런스**

```
anthropics-skills     → 공식 Skill 구현 (Anthropic)
obra-superpowers      → TDD, 디버깅 워크플로우
everything-claude-code → 15 agents, 30+ skills
wshobson-agents       → 112 agents, 16 orchestrators
awesome-subagents     → 126+ subagent 패턴
awesome-agent-skills  → 339+ 멀티에이전트 호환 skills
hooks-mastery         → 13 hook event 구현 예시
```

코드 검색: `Grep "PreToolUse" in repos/hooks-mastery/` — 실제 코드에서 직접 검색 가능.

**scripts/ — 스캐폴딩 자동화**
- `init-skill.sh` / `init-agent.sh` / `init-hook.sh` / `init-ralph.sh`
- `test-hook.sh` — Hook 테스트
- `check-updates.sh` — 공식 문서 업데이트 감지

**evaluations/ — 품질 보증**
- 5개 테스트 시나리오 (P0/P1)
- Golden outputs + 자동 평가 러너
- 스킬 품질을 정량적으로 측정

**설계 원칙: Progressive Disclosure (점진적 노출)**

```
Level 0: 슬래시 명령 → 즉시 결과 (1줄 입력)
Level 1: SKILL.md → Quick Reference (기본 지식)
Level 2: references/ → 상세 가이드 (심화)
Level 3: official/ → 공식 스펙 (정확성)
Level 4: repos/ → 실전 코드 (구현 참고)
```

필요한 만큼만 로드 → 토큰 효율 극대화.

---

### v2.10.0 신규 기능 하이라이트

- **Ralph Loop**: Fresh Context Pattern 자율 개발 루프 (3가지 구현 방법)
- **What-Goes-Where 가이드**: 요구사항 → 컴포넌트 매핑 결정 트리
- **마켓플레이스 지원**: `claude plugin install`로 원클릭 설치

---

```bash
# 지금 바로 시작하세요
claude plugin install github:cathy-kim/ccbuilder

# 또는 자연어로 물어보세요
"Skill이랑 Agent 차이가 뭐야?"
"Hook 이벤트가 뭐가 있어?"
"프론트+백엔드 병렬로 개발하고 싶어"
```

MIT License | GitHub: github.com/cathy-kim/ccbuilder

#ClaudeCode #AI #AIEngineering #DeveloperTools #Anthropic #Claude #Plugin #AgentTeams #RalphLoop #AIAgents #Automation #OpenSource

---

## Post (English version)

---

**Want to build Claude Code extensions but don't know where to put what?**

Introducing ccbuilder v2.10.0 — the Claude Code Extension Builder Plugin.

Skills, Hooks, Agents, Agent Teams, Ralph Loops — one plugin covers the entire Claude Code extension ecosystem.

Install: `claude plugin install github:cathy-kim/ccbuilder`

---

### 1. File Placement: The "What Goes Where" Decision Tree

The most common mistake in Claude Code extension development: building things in the wrong place.

A 300-line React guide in CLAUDE.md? Token waste every session.
A 1-line rule as a Skill? Over-engineered.

ccbuilder includes a built-in **What-Goes-Where decision tree**:

```
"Project-wide rules"          → CLAUDE.md
"Path-specific rules"         → .claude/rules/ (with paths: frontmatter)
"Reusable detailed guides"    → Skill (.claude/skills/)
"Independent agents"          → Agent (.claude/agents/)
"Event-driven automation"     → Hook (settings.json)
"Multi-agent collaboration"   → Agent Team (TeamCreate)
"Long-running autonomous dev" → Ralph Loop (TASK.md + loop.sh)
"External API integration"    → MCP Server (.mcp.json)
```

Key principle: **Always-on = CLAUDE.md, On-demand = Skill, Event-driven = Hook.**

---

### 2. Complex Workflow Design: 5 Patterns

ccbuilder's 7 extension types shine when combined.

**Pattern A — Skill + Hook combo**: Inject coding guides via Skill, auto-block violations via Hook (PreToolUse).

**Pattern B — Agent Team (parallel collaboration)**: Frontend, Backend, Test agents work simultaneously. Dependency control via blockedBy.

**Pattern C — Ralph Loop (autonomous development)**: 30min+ tasks with zero context degradation.

```
Session 1 → Execute → Update PROGRESS.md → Git commit
    ↓ (Context reset to 0% — always peak performance!)
Session N → LOOP_COMPLETE detected → Exit
```

**Pattern D — Agent Team + Ralph (hybrid)**: Decompose into subtasks → Execute each via Ralph Loop with fresh context.

---

### 3. Inside the Plugin: 33 Reference Guides

ccbuilder isn't a simple template generator. It's a **systematically structured knowledge base**.

**SKILL.md (490 lines)** — Acts as a router. Routes arguments to the right reference docs.

**references/ (33 guides)**: Functional guides (7), Design guides (5), Quality guides (3), Official doc summaries (6), GitHub ecosystem (5 + 11 submodule repos with 339+ skills, 126+ subagents, 112 agents).

**Progressive Disclosure architecture**: Load only what you need → maximize token efficiency.

```
Level 0: Slash command → Instant scaffolding
Level 1: SKILL.md → Quick Reference
Level 2: references/ → Detailed guides
Level 3: official/ → Exact specs
Level 4: repos/ → Real-world code
```

---

### What's New in v2.10.0

- **Ralph Loop**: Fresh Context Pattern for autonomous dev (3 implementations)
- **What-Goes-Where Guide**: Requirement → component mapping decision tree
- **Marketplace support**: One-click install via `claude plugin install`

```bash
claude plugin install github:cathy-kim/ccbuilder
```

MIT License | GitHub: github.com/cathy-kim/ccbuilder

#ClaudeCode #AI #AIEngineering #DeveloperTools #Anthropic #Claude #Plugin #AgentTeams #RalphLoop #AIAgents #Automation #OpenSource
