# Skills 상세 가이드

> Claude Code Skills 개발 완전 가이드

**Version**: 2.9.0
**Last Updated**: 2026-02-11
**Claude Code Version**: v2.1.39+

---

## Skill Scopes (우선순위)

Claude Code는 다음 순서로 Skills를 로드합니다:

```
Enterprise > Personal > Project > Plugin
(높은 우선순위)        (낮은 우선순위)
```

| Scope | 위치 | 설명 |
|-------|------|------|
| **Enterprise** | 조직 설정 | 기업용 공통 스킬 |
| **Personal** | `~/.claude/skills/` | 사용자 개인 전역 스킬 |
| **Project** | `.claude/skills/` | 프로젝트별 스킬 |
| **Plugin** | 플러그인 | 마켓플레이스/플러그인 스킬 (Tool Search, OAuth 지원) |

동일 이름의 스킬은 **높은 우선순위 scope가 덮어씁니다**.

---

## 위치

- `~/.claude/skills/` (전역, Personal scope)
- `.claude/skills/` (프로젝트, Project scope)

---

## SKILL.md Frontmatter (v2.7)

```yaml
---
name: my-skill                    # 필수
description: "설명 + 자동 활성화 키워드"  # 필수
userInvocable: true               # /my-skill 로 직접 호출 가능

# 자동완성 힌트 (신규 v2.1.30+)
argument-hint: "<topic> [--verbose]"

# 도구 제한 (CLI에서만 작동, SDK는 별도 설정 필요)
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit

# 실행 컨텍스트 (선택)
context: fork                     # 별도 컨텍스트에서 실행

# 에이전트 지정 (선택)
agent: backend                    # 특정 에이전트로 실행

# 다른 스킬 함께 로드 (선택)
skills:
  - design-system
  - testing-patterns

# 내장 Hooks (선택)
hooks:
  - type: PreToolUse
    tool: Bash
    script: ./hooks/validate.sh
  - type: Stop
    script: ./hooks/cleanup.sh
    once: true                    # 세션당 1회만

# 추가 옵션
version: "1.0.0"                  # 버전 추적용
disable-model-invocation: false   # true면 자동 호출 방지, 수동만 가능
mode: false                       # true면 "Mode Commands" 섹션에 표시
---

# My Skill

## 목적
스킬의 목적 설명

## 지침
1. 첫 번째 단계
2. 두 번째 단계

## 참조
상세 내용은 `references/` 폴더 참조
```

---

## Frontmatter 옵션 정리

| 옵션 | 타입 | 설명 | 기본값 |
|------|------|------|--------|
| `name` | string | 스킬 이름 | **필수** |
| `description` | string | 설명 + 자동 활성화 키워드 | **필수** |
| `userInvocable` | boolean | `/skill-name`으로 직접 호출 | `true` |
| `argument-hint` | string | 자동완성 시 힌트 (신규) | - |
| `allowed-tools` | string[] | 허용된 도구 목록 | 모든 도구 |
| `context` | "fork" | 별도 컨텍스트에서 실행 | - |
| `agent` | string | 실행할 에이전트 타입 | - |
| `skills` | string[] | 함께 로드할 다른 스킬 | - |
| `hooks` | object[] | 내장 Hook 정의 | - |
| `version` | string | 버전 추적용 메타데이터 | - |
| `disable-model-invocation` | boolean | Claude 자동 호출 방지 (슬래시 명령만 허용) | `false` |
| `mode` | boolean | Mode Commands 섹션에 표시 | `false` |

---

## 문자열 치환 (String Substitutions)

```yaml
# SKILL.md 내에서 사용 가능한 변수
$ARGUMENTS     # 전체 인자 문자열
$1, $2, ...    # 개별 인자 (위치 기반)
$ARGUMENTS[0]  # 배열 접근 (v2.7, 이전: $ARGUMENTS.0 → deprecated)
${CLAUDE_SESSION_ID}  # 현재 세션 ID
```

---

## 동적 컨텍스트 주입 (신규)

```markdown
# SKILL.md 내에서 동적 컨텍스트 로드

현재 Git 상태:
!`git status --short`

패키지 정보:
!`cat package.json | jq '.dependencies'`
```

---

## Hot Reload

```bash
# 스킬 수정 시 자동 반영 - 재시작 불필요!
echo "수정" >> .claude/skills/my-skill/SKILL.md
# 즉시 활성화됨
```

---

## Memory & Modular Rules (v2.7 신규)

### Auto Memory

Skill이 세션 간 학습한 내용을 영속적으로 저장:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md        # 매 세션 자동 로드 (200줄 제한)
├── debugging.md     # 토픽별 상세 노트
└── patterns.md
```

### Modular Rules

`.claude/rules/*.md` 파일은 매 세션 자동 로드됩니다:

```yaml
---
paths:
  - "src/frontend/**"
  - "*.tsx"
---

# Frontend Rules
- TypeScript 필수
- 함수형 컴포넌트만
```

`paths:` frontmatter로 특정 경로에서만 활성화되는 규칙을 정의할 수 있습니다.

---

## Progressive Disclosure (500줄 규칙)

SKILL.md는 500줄 이하로 유지하고, 상세 내용은 references/에 분리합니다.

```
my-skill/
├── SKILL.md          # < 500줄 (개요만)
├── CHANGELOG.md      # 변경 이력
├── releases/         # 버전별 스냅샷
└── references/       # 상세 가이드
    ├── topic-1.md
    └── topic-2.md
```

---

## 스킬 구조 예시

### 기본 스킬 (Tier 1)

```
my-skill/
├── SKILL.md
├── CHANGELOG.md
└── releases/
```

### 중급 스킬 (Tier 2)

```
my-skill/
├── SKILL.md
├── CHANGELOG.md
├── releases/
└── references/
    ├── core-concepts.md
    └── examples.md
```

### 고급 스킬 (Tier 3)

```
my-skill/
├── SKILL.md
├── CHANGELOG.md
├── releases/
├── references/
├── agents/           # 스킬 전용 에이전트
├── hooks/            # 스킬 전용 훅
└── scripts/          # 유틸리티
```

---

## Task Management (v2.9)

| 도구 | 용도 |
|------|------|
| `TaskCreate` | 작업 생성 (subject, description, activeForm) |
| `TaskUpdate` | 상태 변경, 소유자 할당, 의존성 설정 |
| `TaskList` | 전체 작업 목록 조회 |
| `TaskGet` | 개별 작업 상세 조회 |

---

## Breaking Changes (v2.8-2.9)

| 변경 | 이전 | 이후 |
|------|------|------|
| Shell 인자 접근 | `$ARGUMENTS.0` | `$ARGUMENTS[0]` 또는 `$0` |
| NPM 설치 | `npm install` | `claude install` |
| MCP Transport | SSE | HTTP (streamable-http) |

---

## 관련 문서

- [Hooks Guide](hooks-guide.md)
- [Subagents Guide](subagents-guide.md)
- [Agent Teams Guide](agent-teams-guide.md)
- [Best Practices](best-practices.md)

## 공식 문서

- **Skills Reference**: https://code.claude.com/docs/en/skills

---

*이 문서는 SKILL.md에서 분리되었습니다 (2026-02-04, v2.9.0 업데이트 2026-02-11)*
