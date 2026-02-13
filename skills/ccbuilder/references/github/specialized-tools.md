# T3/T4 - Specialized Tools & Use Cases

> 특화 도구들. 특정 문제 해결에 탁월.

**Last Updated**: 2026-02-11

---

## T3 - Specialized (1k-10k Stars)

### 1. VoltAgent/awesome-agent-skills (~6.7k Stars)

- **URL**: https://github.com/VoltAgent/awesome-agent-skills
- **제공**: 339+ 멀티 에이전트 호환 Skills (공식 팀 + 커뮤니티)

#### 공식 팀 Skills

| 팀 | Skills |
|-----|--------|
| Vercel | React, Next.js |
| Cloudflare | Workers, D1, KV |
| Stripe | 결제 연동 |
| Hugging Face | 모델 트레이닝 |
| Microsoft | Azure SDK (.NET/Java/Python) |
| HashiCorp | Terraform |
| Expo | React Native |
| Sentry | 에러 트래킹 |

#### 유즈 케이스

- **"Vercel 배포 Skill 참고"** → Vercel 팀 공식 Skill
- **"멀티 에이전트 호환 Skill 포맷"** → Claude Code + Codex + Gemini CLI + Cursor 모두 동작
- **"특정 서비스 Skill 검색"** → 조직별 카테고리 탐색

---

### 2. travisvn/awesome-claude-skills (~6.9k Stars)

- **URL**: https://github.com/travisvn/awesome-claude-skills
- **제공**: Skills 비교표 + 튜토리얼

#### 핵심 가치

- **결정 매트릭스**: Skills vs MCP vs Subagents vs Projects 선택 기준
- **Skill 생성 튜토리얼**: skill-creator 도구 + 수동 가이드
- **보안 고려사항**: 엔터프라이즈 Skill 심사 기준
- **커뮤니티 하이라이트**: obra/superpowers, iOS Simulator, FFUF Web Fuzzing, Playwright 등

---

### 3. ChrisWiles/claude-code-showcase (~5.3k Stars)

- **URL**: https://github.com/ChrisWiles/claude-code-showcase
- **제공**: 완전한 프로젝트 설정 예시 + GitHub Actions 자동화

#### 핵심 유즈 케이스

| 패턴 | 설명 |
|------|------|
| **Ticket-to-Code** | JIRA 티켓 → 코드 구현 → PR + 상태 업데이트 |
| **Scheduled Agents** | GitHub Actions cron으로 Claude 정기 실행 |
| **Skill Matching Hook** | 프롬프트 키워드 기반 Skill 자동 제안 |
| **Quality Gates** | Linting, Testing, Formatting을 PreToolUse Hook으로 |

#### 구성 요소

| 유형 | 예시 |
|------|------|
| `.mcp.json` | JIRA, GitHub, Slack, DB 연동 |
| Agents | Code Reviewer, Ticket Handler, Quality Improvement |
| Commands | `/ticket`, `/onboard`, `/pr-review` |
| Hooks | Main 브랜치 편집 차단, Auto-format, Auto-test, TSC 체크 |
| GitHub Actions | 월별 문서 동기화, 주별 품질 리뷰, 격주 의존성 감사 |

---

### 4. zilliztech/claude-context (~5.3k Stars)

- **URL**: https://github.com/zilliztech/claude-context
- **제공**: 벡터 임베딩 기반 코드 검색 MCP 서버

#### 유즈 케이스

- **대규모 코드베이스 검색**: 수백만 줄을 자연어로 검색
- **토큰 절약**: 디렉토리 전체 로딩 대비 ~40% 감소
- **Tools**: `index_codebase`, `search_code`, `clear_index`, `get_indexing_status`
- **호환**: Claude Code, VS Code, Cursor, Windsurf

#### 기술

- Hybrid 검색: BM25 키워드 + Dense Vector 유사도
- Zilliz Cloud 매니지드 벡터 저장소

---

### 5. Piebald-AI/claude-code-system-prompts (~4.4k Stars)

- **URL**: https://github.com/Piebald-AI/claude-code-system-prompts
- **제공**: Claude Code 시스템 프롬프트 추출/분석 (110+ 문자열)

#### 유즈 케이스

- **내부 동작 이해**: Plan/Explore/Task agent가 어떤 프롬프트로 동작하는지
- **토큰 예산 참고**: 28+ 내장 도구 설명의 정확한 토큰 수
- **버전 추적**: 95+ 버전 CHANGELOG (릴리스 수 분 내 업데이트)
- **커스터마이징**: `tweakcc` 도구로 개별 프롬프트 조각 수정

#### 주요 프롬프트 토큰 수

| 프롬프트 | 토큰 |
|----------|-------|
| Explore agent | 516 |
| Plan mode | 633 |
| Task tool | 294 |
| `/pr-comments`, `/review-pr`, `/security-review` | 2,610 |
| Agent creation architect | 1,110 |

---

### 6. disler/claude-code-hooks-mastery (~2.9k Stars)

- **URL**: https://github.com/disler/claude-code-hooks-mastery
- **제공**: 전체 13개 Hook 이벤트 구현 + TTS + 보안

#### 유즈 케이스

| 기능 | 설명 |
|------|------|
| **All 13 Events** | 모든 Hook 이벤트의 레퍼런스 구현 |
| **TTS 통합** | ElevenLabs > OpenAI > pyttsx3 우선순위 |
| **감사 로그** | JSON 기반 전체 이벤트 추적 |
| **터미널 상태** | 9가지 터미널 디스플레이 변형 |

#### 기술

- **UV 단일 파일 스크립트**: 각 Hook이 독립적 Python (의존성 내장)
- **보안 우선**: Pre-execution 검증으로 위험 작업 사전 차단

---

### 7. alirezarezvani/claude-skills (~1.7k Stars)

- **URL**: https://github.com/alirezarezvani/claude-skills
- **제공**: 53개 프로덕션 Skills (비기술 도메인 포함)

#### 비기술 도메인 Skills

| 도메인 | Skills |
|--------|--------|
| 마케팅 | Content Creator, Campaign Analytics, ASO, Social Media Analyzer |
| C-Level | CEO Advisor, CTO Advisor |
| 제품 | PM Toolkit, Agile Product Owner, UX Researcher |
| 프로젝트 관리 | Scrum Master, Jira Expert, Confluence Expert |
| 규제/품질 | 12개 컴플라이언스/QA 프레임워크 |

---

### 8. disler/claude-code-hooks-multi-agent-observability (~1.1k Stars)

- **URL**: https://github.com/disler/claude-code-hooks-multi-agent-observability
- **제공**: 멀티 에이전트 실시간 모니터링 대시보드

#### 유즈 케이스

- 복수 Agent 동시 작업 감시
- 태스크 핸드오프 추적
- 12개 라이프사이클 이벤트 캡처
- 실시간 Pulse Chart (세션별 컬러 코딩)

#### 아키텍처

```
Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite (WAL) → WebSocket → Vue 3
```

---

### 9. steipete/claude-code-mcp (~1.1k Stars)

- **URL**: https://github.com/steipete/claude-code-mcp
- **제공**: Claude Code를 MCP 서버로 활용 (Agent-in-Agent)

#### 유즈 케이스

- **Cursor/Windsurf에서 Claude Code 호출**: MCP 클라이언트로 연결
- **권한 없이 자동화**: `--dangerously-skip-permissions` 파이프라인용
- **복잡한 멀티 스텝 워크플로우**: 단일 호출로 처리

---

## T4 - Emerging (<1k Stars)

### 10. johnlindquist/claude-hooks (~292 Stars)

- **URL**: https://github.com/johnlindquist/claude-hooks
- **제공**: TypeScript 타입 안전 Hook 시스템

#### 유즈 케이스

- **IntelliSense 지원 Hook 개발**: PreToolUse, PostToolUse 등 타입 정의
- **Zero-config 셋업**: `npx claude-hooks`
- **Bun 런타임**: 빠른 Hook 실행

---

### 11. karanb192/claude-code-hooks (~136 Stars)

- **URL**: https://github.com/karanb192/claude-code-hooks
- **제공**: 복사-붙여넣기 Ready Hook 모음 (안전 + 자동화)

#### 유즈 케이스

| Hook | 기능 |
|------|------|
| `block-dangerous-commands` | 위험한 Shell 명령 차단 |
| `protect-secrets` | 민감 파일 보호 |
| `auto-stage` | 편집 후 자동 git stage |
| `notify-permission` | 권한 요청 시 Slack 알림 |
| `event-logger` | Hook 이벤트 디버깅 |

---

### 12. daymade/claude-code-skills (~569 Stars)

- **URL**: https://github.com/daymade/claude-code-skills
- **제공**: 36개 프로덕션 Skills 마켓플레이스

#### 주목할 Skills

- `deep-research`: 심층 리서치
- `prompt-optimizer`: 프롬프트 최적화
- `cli-demo-generator`: CLI 데모 자동 생성
- `teams-channel-post-writer`: Teams 채널 포스팅
- `youtube-downloader`: YouTube 다운로드
