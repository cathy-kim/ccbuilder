# Memory & Rules 상세 가이드

> Claude Code의 Memory 시스템과 Modular Rules 완전 가이드

**Version**: 2.9.0
**Last Updated**: 2026-02-11
**Claude Code Version**: v2.1.39+

---

## Memory 계층 (우선순위)

```
1. Managed Policy (최고)  →  조직 차원 배포
2. Project Memory         →  CLAUDE.md / .claude/CLAUDE.md
3. Project Rules          →  .claude/rules/*.md
4. User Memory            →  ~/.claude/CLAUDE.md
5. Project Local          →  CLAUDE.local.md (자동 gitignore)
```

---

## 1. Managed Policy

조직 차원에서 배포하는 정책 파일. 시스템 디렉토리에 위치하며 최고 우선순위.

---

## 2. Project Memory (CLAUDE.md)

### 위치

| 위치 | 범위 |
|------|------|
| `./CLAUDE.md` | 프로젝트 루트 |
| `./.claude/CLAUDE.md` | 프로젝트 루트 (대안) |
| 부모 디렉토리 `CLAUDE.md` | 모노레포 공통 |
| 자식 디렉토리 `CLAUDE.md` | 하위 모듈별 |

### CLAUDE.md Imports

다른 파일을 `@path` 문법으로 import:

```markdown
# CLAUDE.md

@docs/coding-standards.md
@.claude/rules/security-policy.md
```

- **최대 깊이**: 5 hop (순환 참조 자동 감지)
- **승인 다이얼로그**: 새 import 발견 시 사용자에게 확인

### Memory Lookup

```
프로젝트 루트부터 상위로 재귀 탐색:
./CLAUDE.md → ../CLAUDE.md → ../../CLAUDE.md → ...

하위 디렉토리도 발견:
./src/CLAUDE.md (src/ 작업 시 자동 로드)
```

추가 디렉토리 로드:
```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1
```

---

## CLAUDE.md 작성 가이드

### 작성 템플릿

```markdown
# Project Name

## 기술 스택
- 언어: [언어]
- 프레임워크: [프레임워크 + 버전]
- DB: [데이터베이스]
- 테스트: [테스트 프레임워크]

## 주요 명령어
- `npm run dev`: 개발 서버
- `npm run test`: 테스트 실행
- `npm run build`: 빌드

## 프로젝트 구조
- `src/app/`: [설명]
- `src/lib/`: [설명]

## 코딩 규칙
- [규칙 1]
- [규칙 2]

## Git 규칙
- 커밋 메시지: [형식]
- PR: [규칙]

## 중요 규칙
- IMPORTANT: [절대 지켜야 할 규칙]
- YOU MUST: [필수 수행 사항]
```

### 작성 원칙

- **간결하게** (100줄 이하 권장) — 매 세션 자동 로드되므로 토큰 절약
- **"IMPORTANT"/"YOU MUST"** 로 중요 규칙 강조
- **스캔 가능한 구조** — 제목, 목록, 표 활용
- **반복 프롬프트로 취급** — `#` 키로 Claude가 자동 업데이트 유도

### CLAUDE.md vs Rules vs CLAUDE.local.md 선택 기준

```
이 내용을 어디에 적을지?

├─ 팀 전체가 알아야 하고, 프로젝트 전역에 항상 적용?
│   → CLAUDE.md (Git 커밋)
│
├─ 특정 파일/경로에서만 적용? (프론트엔드, 테스트 등)
│   → .claude/rules/*.md (paths: frontmatter)
│
├─ 내 로컬 환경에만 해당? (DB 주소, API 키 위치 등)
│   → CLAUDE.local.md (자동 gitignore)
│
├─ 모든 프로젝트에 공통? (선호 도구, 언어 등)
│   → ~/.claude/CLAUDE.md (User Memory)
│
└─ 상세한 가이드/패턴? (300줄+ 설명)
    → Skill로 분리 (.claude/skills/)
```

| 내용 예시 | 적합한 위치 | 이유 |
|----------|------------|------|
| "TypeScript 필수" | CLAUDE.md | 프로젝트 전역, 팀 공유 |
| "프론트엔드는 함수형 컴포넌트만" | `.claude/rules/frontend.md` | 특정 경로만 |
| "내 DB는 localhost:5432" | CLAUDE.local.md | 개인 환경 |
| "항상 bun 사용" | `~/.claude/CLAUDE.md` | 모든 프로젝트 |
| "React 패턴 가이드 300줄" | Skill | 매 세션 로드하면 토큰 낭비 |
| "커밋 메시지는 conventional commits" | CLAUDE.md | 팀 규칙 |
| "테스트 파일은 같은 폴더에" | `.claude/rules/testing.md` | `paths: "*.test.*"` |

---

## 3. Project Rules (.claude/rules/)

### 기본 사용

`.claude/rules/*.md` 파일은 매 세션 자동 로드됩니다.

```
.claude/rules/
├── coding-rules.md        # 전역 코딩 규칙
├── frontend-rules.md      # 프론트엔드 규칙
└── security-policy.md     # 보안 정책
```

### 경로별 조건부 Rules

`paths:` frontmatter로 특정 경로에서만 활성화:

```yaml
---
paths:
  - "src/frontend/**"
  - "*.tsx"
  - "*.{ts,tsx}"
---

# Frontend Rules
- TypeScript 필수
- 함수형 컴포넌트만
```

### Glob 패턴 지원

```yaml
paths:
  - "src/**/*.ts"                    # 재귀 매칭
  - "*.{ts,tsx}"                     # 확장자 그룹
  - "{src,lib}/**/*.ts"              # 디렉토리 그룹 (Brace expansion)
```

### 서브디렉토리 구성

```
.claude/rules/
├── coding-rules.md
├── frontend/
│   ├── react-rules.md
│   └── styling-rules.md
└── backend/
    └── api-rules.md
```

### Rules 본문 작성 가이드

**작성 원칙**:
- 규칙은 **명령형** ("사용", "금지", "필수")
- 대안 제시 ("X 대신 Y 사용")
- 파일당 **하나의 도메인** (프론트엔드, 백엔드, 테스트 등)
- 전체 rules/ 합계 **200줄 이하** 권장

**예시: 보안 정책 규칙**

```yaml
---
paths:
  - "src/api/**"
  - "src/middleware/**"
---

# Security Rules

## 인증
- 모든 API 엔드포인트에 인증 미들웨어 적용 필수
- JWT 토큰 검증은 middleware에서만 수행
- 토큰 만료 시간: access 15분, refresh 7일

## 입력 검증
- 사용자 입력은 zod 스키마로 반드시 검증
- SQL 쿼리에 raw string 직접 삽입 금지 → Prisma parameterized query 사용
- 파일 업로드: 확장자 화이트리스트 + MIME 타입 검증

## 민감 정보
- .env 파일 절대 커밋 금지
- API 키, 비밀번호는 환경변수에서만 참조
- 로그에 사용자 개인정보 출력 금지
```

**예시: 테스트 규칙**

```yaml
---
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "tests/**"
---

# Testing Rules

- 테스트 파일은 소스 파일과 같은 디렉토리에 위치
- 테스트 프레임워크: Vitest (Jest 금지)
- mock 최소화 → 실제 구현 우선, 외부 의존성만 mock
- 테스트 이름: "should [expected behavior] when [condition]"
- 커버리지 80% 이상 유지
```

### Symlink로 규칙 공유

```bash
# 공통 규칙을 여러 프로젝트에서 공유
ln -s /shared/rules/common.md .claude/rules/common.md
```

---

## 4. User Memory (~/.claude/CLAUDE.md)

모든 프로젝트에 적용되는 전역 설정:

```markdown
# ~/.claude/CLAUDE.md

## 선호사항
- 항상 TypeScript 사용
- 커밋 메시지는 한국어로
- bun 대신 npm 사용
```

### User-level Rules

```
~/.claude/rules/
└── global-rules.md    # 모든 프로젝트에 적용
```

---

## 5. Project Local (CLAUDE.local.md)

Git에 커밋하지 않을 개인 설정:

```markdown
# CLAUDE.local.md (자동 .gitignore)

## 로컬 환경
- DB: localhost:5432
- API_KEY는 .env 참조
```

---

## Auto Memory

세션 간 학습 내용을 자동으로 영속 저장:

```
~/.claude/projects/<project-path>/memory/
├── MEMORY.md        # 매 세션 자동 로드 (처음 200줄)
├── debugging.md     # 토픽별 상세 노트
├── patterns.md      # 코딩 패턴
└── api-conventions.md
```

### MEMORY.md 작성 원칙

**저장할 내용:**
- 여러 세션에서 확인된 안정적 패턴
- 주요 아키텍처 결정, 파일 경로
- 사용자의 워크플로우/도구 선호도
- 반복 문제의 해결책

**저장하지 않을 내용:**
- 세션별 임시 상태 (현재 작업, 진행 중 상태)
- 단일 파일에서 읽은 미검증 결론
- CLAUDE.md와 중복되는 내용

### 토픽 파일

MEMORY.md에서 링크하고, 필요할 때 온디맨드 로드:

```markdown
# MEMORY.md (200줄 이하)

## 주요 패턴
- 상세: [patterns.md](patterns.md)

## 디버깅 노트
- 상세: [debugging.md](debugging.md)
```

---

## /memory 명령

세션 내에서 메모리 파일을 관리:

```bash
/memory    # 메모리 파일 선택기 열기
```

---

## Breaking Changes (v2.8-2.9)

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

---

## 관련 문서

- [Skills Guide](skills-guide.md) - Skill에서 Memory/Rules 활용
- [Best Practices](best-practices.md) - Memory/Rules 모범 사례
- [Troubleshooting](troubleshooting.md) - Memory 문제 해결

## 공식 문서

- **Memory Reference**: https://code.claude.com/docs/en/memory

---

*이 문서는 v2.9.0 업데이트 (2026-02-11)*
