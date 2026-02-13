# Skills - Official Reference

> Source: https://code.claude.com/docs/en/skills

**Last Synced**: 2026-02-11

---

## 개요

Skills는 `.md` 파일로 정의하는 Claude Code 확장 기능. 지식 주입(reference) 또는 작업 지시(task) 두 가지 유형.

## 파일 위치 & 우선순위

```
Enterprise (최고) > Personal (~/.claude/skills/) > Project (.claude/skills/) > Plugin
```

- 자동 탐색: 중첩된 `.claude/skills/` 디렉토리도 인식 (모노레포 지원)
- Plugin Skills: `plugin-name:skill-name` 네임스페이스

## Frontmatter 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | O | 소문자, max 64자 |
| `description` | 권장 | Claude 자동 호출 조건 설명 |
| `userInvocable` | - | `false`면 사용자 메뉴에서 숨김 (Claude 전용) |
| `disable-model-invocation` | - | `true`면 자동 호출 비활성화 (수동 `/` 명령만) |
| `allowed-tools` | - | Skill 내 사용 가능 도구 제한 |
| `context` | - | `fork`면 별도 subagent에서 실행 |
| `model` | - | Skill 전용 모델 오버라이드 |
| `argument-hint` | - | `/` 자동완성 시 힌트 표시 |
| `hooks` | - | Skill 스코프 라이프사이클 훅 |

## 문자열 치환

| 변수 | 설명 |
|------|------|
| `$ARGUMENTS` | 전체 인자 문자열 |
| `$ARGUMENTS[N]` | N번째 인자 (0-indexed) |
| `$N` | N번째 인자 단축형 |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID |

## 동적 컨텍스트 주입

`` !`command` `` 문법으로 실행 시점에 명령어 결과를 주입:

```markdown
현재 브랜치: !`git branch --show-current`
```

## 핵심 규칙

- SKILL.md 최대 **500줄** 권장 (progressive disclosure)
- 메타데이터는 항상 로드, 본문은 활성화 시 로드, resources는 필요 시 로드
- `.claude/commands/` 파일도 여전히 동작하지만 `skills/` 권장

## Breaking Change

- Custom slash commands가 Skills 시스템으로 통합됨
- `$ARGUMENTS.0` → `$ARGUMENTS[0]` 문법 변경
