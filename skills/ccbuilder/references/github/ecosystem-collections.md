# T2 - Ecosystem Collections (10k+ Stars)

> 생태계 핵심 컬렉션. 아이디어와 패턴의 보고.

**Last Updated**: 2026-02-11

---

## 1. obra/superpowers (~49.6k Stars)

- **URL**: https://github.com/obra/superpowers
- **제공**: 에이전트 워크플로우 방법론 (Skills 프레임워크)

### 핵심 유즈 케이스

| 워크플로우 | 설명 |
|------------|------|
| **TDD** | RED-GREEN-REFACTOR 엄격 적용 (테스트 먼저 강제) |
| **Systematic Debugging** | 4단계 근본 원인 분석 |
| **Brainstorming** | 소크라테스식 설계 (코딩 전 질문) |
| **Subagent-driven Dev** | Agent 파견 → 작업 → 리뷰 2단계 |
| **Parallel Dispatching** | git worktree 기반 병렬 워크플로우 |

### 학습 포인트

- **방법론 우선 접근**: Skill이 "기능"이 아닌 "워크플로우"를 인코딩
- **자동 트리거**: 컨텍스트 기반 자동 활성화 (수동 호출 불필요)
- **YAGNI 원칙**: 모든 Skill에 증거 기반 검증 내장
- **생태계**: `superpowers-skills` (커뮤니티), `superpowers-lab` (실험), `superpowers-marketplace` (큐레이션)

---

## 2. affaan-m/everything-claude-code (~44.0k Stars)

- **URL**: https://github.com/affaan-m/everything-claude-code
- **제공**: 올인원 설정 (Anthropic 해커톤 우승작, 10개월+ 실전 사용)

### 핵심 유즈 케이스

| 카테고리 | 내용 |
|----------|------|
| **Agents (15)** | Planner, Architect, TDD Guide, Security Reviewer, Build Error Resolver 등 |
| **Skills (30+)** | TypeScript, Python, Go, Django, Spring Boot 패턴 |
| **Commands (30+)** | `/plan`, `/tdd`, `/code-review`, `/build-fix`, `/multi-plan`, `/multi-execute` |
| **MCP 설정** | GitHub, Supabase, Vercel, Railway 연동 |
| **Memory Hook** | 세션 라이프사이클 자동 저장/로드 |

### 학습 포인트

- **Continuous Learning v2**: 패턴을 "instincts"로 추출 + 신뢰도 점수 부여
- **토큰 최적화**: 모델 선택, 시스템 프롬프트 슬리밍, 백그라운드 프로세스
- **검증 루프**: Checkpoint vs Continuous evaluation (pass@k 메트릭)
- **멀티 언어 규칙**: `rules/common/` + `rules/typescript/` 등 언어별 오버라이드

---

## 3. wshobson/agents (~28.4k Stars)

- **URL**: https://github.com/wshobson/agents
- **제공**: 112 agents + 16 orchestrators + 146 skills + 79 tools (73 plugins)

### 핵심 유즈 케이스

| Orchestrator | 용도 |
|-------------|------|
| Full-Stack Feature Development | 기능 개발 전체 파이프라인 |
| Security Hardening | 보안 강화 자동화 |
| Kubernetes Operations | K8s 운영 워크플로우 |
| ML Pipeline | ML 파이프라인 오케스트레이션 |
| Incident Response | 인시던트 대응 자동화 |
| CI/CD Pipeline Setup | CI/CD 구성 |

### 학습 포인트

- **3-Tier 모델 전략**: Opus (핵심 결정) / Sonnet (개발) / Haiku (운영)
- **Progressive Disclosure**: 메타데이터 항상 → 본문 활성화 시 → 리소스 필요 시
- **Composable Plugin**: 평균 3.4 컴포넌트/플러그인, 23 카테고리
- **세분화된 전문화**: 각 Plugin이 자체 agents/commands/skills만 로드

---

## 4. hesreallyhim/awesome-claude-code (~23.4k Stars)

- **URL**: https://github.com/hesreallyhim/awesome-claude-code
- **제공**: 큐레이션된 생태계 디렉토리

### 핵심 유즈 케이스

| 카테고리 | 예시 |
|----------|------|
| **Hook SDK** | cchooks (Python), claude-hooks (TS), beyondcode SDK (PHP) |
| **Orchestrators** | Claude Squad, Claude Swarm, Happy Coder, TSK |
| **Usage Monitors** | ccflare, CCUsage, Claudex |
| **IDE 통합** | Claudix (VSCode), claude-code.nvim (Neovim), claude-code.el (Emacs) |
| **Status Lines** | CCometixLine, ccstatusline, claudia-statusline |
| **CLAUDE.md 모음** | 언어별, 도메인별 프로젝트 메모리 |

### 학습 포인트

- **생태계 전체 인덱스**: 새 도구/라이브러리 발견의 출발점
- **카테고리별 Commands**: git, testing, CI/deployment, task management
- **트렌드 파악**: 커뮤니티에서 어떤 패턴이 인기인지 확인

---

## 5. VoltAgent/awesome-claude-code-subagents (~10.2k Stars)

- **URL**: https://github.com/VoltAgent/awesome-claude-code-subagents
- **제공**: 126+ 전문 서브에이전트 (10 카테고리)

### 카테고리별 Agent 수

| 카테고리 | 수 | 예시 |
|----------|-----|------|
| Core Development | 10 | API Designer, Frontend/Backend Dev |
| Language Specialists | 26 | TS, Python, Go, Rust, Java, PHP, Ruby |
| Infrastructure | 15 | DevOps, K8s, Terraform, Platform Eng |
| Quality & Security | 14 | Testing, Code Review, Pen Testing |
| Data & AI | 12 | ML Engineer, Data Scientist, LLM Architect |
| Meta & Orchestration | 11 | Multi-agent Coordinator |
| Business & Product | 10 | PM, Project Coordinator |

### 학습 포인트

- **단일 책임 Agent 설계**: 한 Agent = 한 전문 분야
- **카테고리 기반 조직**: 쉬운 탐색과 선택
- **4가지 설치 방법**: marketplace, 수동 복사, installer script, curl
