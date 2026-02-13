# 요청사항 → 어디에 뭘 적을지 가이드

> 사용자의 요구사항을 듣고, 어떤 컴포넌트를 어디에 만들어야 하는지 안내하는 가이드

**Version**: 2.10.0
**Last Updated**: 2026-02-13

---

## 핵심 결정 트리

```
사용자가 원하는 것이 무엇인가?

├─ "프로젝트 전체에 항상 적용될 규칙/컨벤션"
│   ├─ 팀 공유 필요? → CLAUDE.md (Git 커밋)
│   ├─ 내 로컬만? → CLAUDE.local.md
│   └─ 특정 경로에서만? → .claude/rules/*.md (paths: frontmatter)
│
├─ "반복적으로 사용할 지침/가이드/패턴"
│   └─ Skill (.claude/skills/<name>/SKILL.md)
│
├─ "특정 역할의 독립 에이전트"
│   └─ Agent (.claude/agents/<name>.md)
│
├─ "이벤트에 자동 반응 (파일 수정 차단, 커밋 전 검사 등)"
│   └─ Hook (settings.json + 스크립트)
│
├─ "여러 에이전트가 협업해서 큰 작업 수행"
│   └─ Agent Team (TeamCreate → Task → SendMessage)
│
├─ "장시간 자율 개발 (30분+, 컨텍스트 열화 방지)"
│   └─ Ralph Loop (TASK.md + loop.sh)
│
└─ "외부 서비스/API 연동"
    └─ MCP Server (.mcp.json)
```

---

## 요구사항 → 컴포넌트 매핑 테이블

| 사용자 요구사항 예시 | 컴포넌트 | 위치 | 이유 |
|---------------------|----------|------|------|
| "TypeScript만 써야 해" | **CLAUDE.md** | `./CLAUDE.md` | 프로젝트 전체 규칙 |
| "프론트엔드는 함수형 컴포넌트만" | **Rules** | `.claude/rules/frontend.md` | 특정 경로에만 적용 |
| "내 로컬 DB 주소는 localhost:5432야" | **CLAUDE.local.md** | `./CLAUDE.local.md` | 개인 환경, Git 제외 |
| "React 패턴 가이드를 만들어줘" | **Skill** | `.claude/skills/react-patterns/` | 반복 사용 지식 |
| "코드 리뷰 전문 에이전트를 만들어줘" | **Agent** | `.claude/agents/code-reviewer.md` | 독립 실행 에이전트 |
| "민감 파일 수정을 차단해줘" | **Hook** | `.claude/hooks/` + `settings.json` | 이벤트 반응 |
| "프론트+백엔드 병렬로 개발해줘" | **Agent Team** | `TeamCreate` | 멀티 에이전트 협업 |
| "항상 bun 사용해줘" (전역) | **User CLAUDE.md** | `~/.claude/CLAUDE.md` | 모든 프로젝트 적용 |
| "커밋 메시지는 conventional commits로" | **CLAUDE.md** | `./CLAUDE.md` | 팀 공유 규칙 |
| "테스트 파일은 반드시 같은 폴더에" | **Rules** | `.claude/rules/testing.md` | `paths: "*.test.*"` |
| "Supabase 연동해줘" | **MCP** | `.mcp.json` | 외부 서비스 |

---

## CLAUDE.md vs Rules vs Skill — 언제 어디에?

### 판단 기준

```
이 내용이...
├─ 프로젝트 전체에 항상 적용? → CLAUDE.md
├─ 특정 파일/경로에서만 적용? → .claude/rules/ (paths: frontmatter)
├─ 호출 시에만 필요한 상세 가이드? → Skill
└─ 여러 프로젝트에 공통? → ~/.claude/CLAUDE.md (전역)
```

### 비교표

| 기준 | CLAUDE.md | .claude/rules/ | Skill |
|------|-----------|----------------|-------|
| **로드 시점** | 매 세션 자동 | 매 세션 자동 (paths 매칭 시) | 키워드/슬래시 호출 시 |
| **범위** | 프로젝트 전체 | 지정 경로만 | 호출된 대화 |
| **크기** | 짧고 핵심만 | 짧고 핵심만 | 500줄 + references/ |
| **적합한 내용** | 스택, 명령어, Git 규칙 | 코딩 스타일, 린트 규칙 | 상세 가이드, 패턴, 튜토리얼 |
| **Git 공유** | O | O | O |

### 예시별 배치

```
❌ CLAUDE.md에 300줄짜리 React 패턴 가이드 → 매 세션 토큰 낭비
✅ Skill로 분리 → 필요할 때만 로드

❌ Skill로 "TypeScript 필수" 1줄 규칙 → 과도한 구조
✅ CLAUDE.md에 한 줄로 작성

❌ CLAUDE.md에 "프론트엔드만 적용" 규칙 → 백엔드 작업 시 불필요한 노이즈
✅ .claude/rules/frontend.md + paths: "src/frontend/**"
```

---

## 컴포넌트별 작성 템플릿

### 1. CLAUDE.md 작성 템플릿

```markdown
# Project Name

## 기술 스택
- 언어: TypeScript
- 프레임워크: Next.js 14 (App Router)
- DB: PostgreSQL + Prisma
- 테스트: Vitest

## 주요 명령어
- `npm run dev`: 개발 서버
- `npm run test`: 테스트 실행
- `npm run build`: 빌드

## 프로젝트 구조
- `src/app/`: 페이지 및 라우팅
- `src/lib/`: 공용 유틸리티
- `src/components/`: UI 컴포넌트
- `prisma/`: DB 스키마

## 코딩 규칙
- 함수형 컴포넌트만 사용
- 커밋 메시지: conventional commits (feat:, fix:, docs:)
- PR은 반드시 테스트 포함

## 중요 규칙
- IMPORTANT: .env 파일은 절대 커밋하지 마세요
- YOU MUST: 모든 API 엔드포인트에 에러 핸들링 필수
```

**작성 원칙**:
- 간결하게 (100줄 이하 권장)
- "IMPORTANT", "YOU MUST"로 중요 규칙 강조
- 빠르게 스캔할 수 있는 구조 (목록, 표)
- 반복 프롬프트로 취급하고 점진적 개선

### 2. Rules 작성 템플릿

```yaml
---
paths:
  - "src/frontend/**"
  - "*.tsx"
---

# Frontend Rules

## 컴포넌트
- 함수형 컴포넌트만 사용 (class 금지)
- Props는 interface로 정의 (type 아닌 interface)
- 컴포넌트 파일명: PascalCase (UserProfile.tsx)

## 스타일
- Tailwind CSS 사용
- 인라인 스타일 금지
- 반응형: mobile-first (sm → md → lg)

## 상태 관리
- 서버 상태: React Query
- 클라이언트 상태: zustand
- 전역 상태 최소화
```

**작성 원칙**:
- `paths:` frontmatter로 적용 범위 명시
- 규칙은 명령형 ("사용", "금지", "필수")
- 대안 제시 ("X 대신 Y 사용")
- 파일당 하나의 도메인 (프론트엔드, 백엔드, 테스트 등)

### 3. Skill 작성 템플릿

```yaml
---
name: my-skill
description: "설명 + 자동 활성화 키워드. Use when [시나리오1], [시나리오2], [시나리오3]."
userInvocable: true
argument-hint: "<topic> [options]"
---

# My Skill

## 목적
이 스킬이 해결하는 문제를 1-2문장으로.

## 사용 시점
- 시나리오 1 설명
- 시나리오 2 설명
- 시나리오 3 설명

---

## 핵심 가이드

### 패턴 1: [이름]

[코드 예시 + 설명]

### 패턴 2: [이름]

[코드 예시 + 설명]

---

## 참조 문서
- [Advanced Guide](references/advanced-guide.md)
- [Examples](references/examples.md)
```

**작성 원칙**:
- 500줄 이하 (상세는 references/에)
- description에 자동 활성화 키워드 포함 (영문 + 한글)
- 구체적 코드 예시 포함
- "## 참조 문서"로 progressive disclosure

### 4. Agent 작성 템플릿

```yaml
---
name: my-agent
description: "[역할 설명]. 코드 변경/리뷰/분석 시 사용."
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
permissionMode: acceptEdits
---

# My Agent

## 역할
이 에이전트의 핵심 책임을 1-2문장으로.

## 지시사항
1. 첫 번째로 할 일
2. 두 번째로 할 일
3. 결과 검증 방법

## 규칙
- 반드시 지켜야 할 규칙 1
- 반드시 지켜야 할 규칙 2

## 출력 형식
[에이전트가 반환할 결과 형식 명시]
```

**작성 원칙**:
- frontmatter에 name, description 필수
- allowed-tools로 필요한 도구만 허용
- 지시사항은 순서대로 (에이전트가 자율 실행)
- 출력 형식 명시 (결과 품질 보장)

---

## 자주 하는 실수

| 실수 | 올바른 방법 |
|------|------------|
| CLAUDE.md에 500줄 가이드 작성 | Skill로 분리, CLAUDE.md는 핵심만 |
| Rules에 paths: 없이 작성 | 전체 적용이면 CLAUDE.md, 경로 한정이면 paths: 추가 |
| Agent에 frontmatter 없이 작성 | name, description 필수, allowed-tools 권장 |
| Skill description에 키워드 누락 | "Use when" + 영문/한글 키워드 혼합 |
| 모든 것을 Skill로 만듦 | 1줄 규칙은 CLAUDE.md, 이벤트 반응은 Hook |
| CLAUDE.md와 Rules에 같은 내용 중복 | 한 곳에만 작성, 다른 곳에서 @path import |

---

## 관련 문서

- [Memory & Rules Guide](memory-rules-guide.md) - CLAUDE.md, Rules 상세 스펙
- [Skills Guide](skills-guide.md) - Skill frontmatter, 구조 상세
- [Subagents Guide](subagents-guide.md) - Agent frontmatter, 호출 방법
- [Hooks Guide](hooks-guide.md) - Hook 이벤트, 스크립트 작성
- [Implementation Guide](implementation-guide.md) - 구현 패턴 예시

---

*이 문서는 v2.10.0에서 신규 추가되었습니다 (2026-02-13)*
