# 트러블슈팅 가이드

> Claude Code 확장 기능 개발 시 자주 발생하는 문제와 해결 방법

**Version**: 2.9.0
**Last Updated**: 2026-02-11

---

## API Error 400: Tool Use Concurrency Issues

### 에러 메시지

```
API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.
```

### 즉시 해결

```bash
# 1. 이전 상태로 복구
/rewind

# 2. 컨텍스트 정리 (Context low 상태일 때)
/compact

# 3. 세션 재시작 (에러 지속 시)
# Ctrl+C 후 다시 claude 실행
```

### 재발 방지 - Hybrid 규칙

**읽기는 병렬, 쓰기는 순차**:

```typescript
// ✅ 병렬 허용 (읽기 전용)
Read("file1.ts")
Read("file2.ts")
Grep("pattern", "src/")
Glob("**/*.ts")

// ✅ 순차 필수 (쓰기 작업)
Bash("cmd1 && cmd2 && cmd3")  // 체이닝
Write("file1.ts", content)     // 완료 후
Write("file2.ts", content)     // 다음 쓰기
```

---

## Hook 실행 실패

### 문제: Hook이 실행되지 않음

**원인 확인**:
```bash
# 1. 실행 권한 확인
ls -la .claude/hooks/

# 2. 권한 부여
chmod +x .claude/hooks/*.sh
chmod +x .claude/hooks/*.ts
```

**settings.json 확인**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "./hooks/my-hook.sh"  // 경로 확인
          }
        ]
      }
    ]
  }
}
```

### 문제: Hook에서 JSON 파싱 오류

**원인**: Hook 출력이 JSON 형식이 아님

```bash
# ❌ 잘못된 방법
echo "Block this action"

# ✅ 올바른 방법
echo '{"decision": "block", "reason": "Block this action"}'
```

### 문제: TeammateIdle Hook이 트리거되지 않음

**확인 사항**:
1. Agent Teams 활성화 여부 (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`)
2. settings.json에 TeammateIdle 이벤트 등록 확인:
```json
{
  "hooks": {
    "TeammateIdle": [{
      "type": "command",
      "command": "./hooks/teammate-idle.sh"
    }]
  }
}
```

---

## Skill 자동 활성화 안됨

### 문제: 키워드 언급해도 스킬 로드 안됨

**확인 사항**:

1. **description에 키워드 포함 확인**:
```yaml
---
name: my-skill
description: |
  스킬 설명.
  Use when: 키워드1, 키워드2, 키워드3
  Keywords: 핵심키워드, 관련단어
---
```

2. **파일 위치 확인**:
```bash
# 프로젝트 스킬
ls .claude/skills/my-skill/SKILL.md

# 전역 스킬
ls ~/.claude/skills/my-skill/SKILL.md
```

3. **Hot Reload 트리거**:
```bash
# 파일 수정으로 재로드 트리거
touch .claude/skills/my-skill/SKILL.md
```

---

## Subagent Task 실패

### 문제: Task가 응답 없이 중단됨

**원인**: 컨텍스트 한도 초과 또는 무한 루프

**해결**:
```typescript
// max_turns 설정으로 제한
Task({
  prompt: "...",
  subagent_type: "Explore",
  max_turns: 10  // 최대 턴 수 제한
})
```

### 문제: 커스텀 에이전트를 찾을 수 없음

**확인**:
```bash
# 에이전트 파일 존재 확인
ls .claude/agents/

# 파일명과 subagent_type 일치 확인
# frontend-developer.md → subagent_type: "frontend-developer"
```

---

## 500줄 규칙 위반

### 문제: SKILL.md가 너무 길다는 경고

**해결**: Progressive Disclosure 적용

```
# Before (500줄 초과)
my-skill/
└── SKILL.md (800줄)

# After (분리)
my-skill/
├── SKILL.md (< 500줄, 개요만)
└── references/
    ├── detailed-guide.md
    └── examples.md
```

---

## MCP 도구 연결 실패

### 문제: MCP 서버 연결 안됨

**확인 사항**:

1. **.mcp.json 설정 확인**:
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp@latest"]
    }
  }
}
```

2. **환경 변수 확인**:
```bash
# 필요한 환경 변수 설정
export SUPABASE_URL="..."
export SUPABASE_KEY="..."
```

3. **MCP 서버 직접 테스트**:
```bash
npx -y @supabase/mcp@latest
```

---

## Agent Teams 문제 (v2.7 신규)

### 문제: TeamCreate 실패

**확인 사항**:
1. **환경 변수 확인**:
```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

2. **팀 이름 유효성**: kebab-case, 특수문자 금지

### 문제: Teammate가 응답하지 않음

**원인**: Idle 상태는 정상. 메시지 전송으로 깨울 수 있음.

```typescript
// Teammate에 메시지 전송
SendMessage({
  type: "message",
  recipient: "teammate-name",  // 항상 이름으로 참조
  content: "작업을 계속해주세요",
  summary: "작업 계속 요청"
})
```

### 문제: TeamDelete 실패

**원인**: 활성 Teammate가 남아있음

**해결**:
```typescript
// 1. 모든 Teammate에 종료 요청
SendMessage({
  type: "shutdown_request",
  recipient: "teammate-name",
  content: "작업 완료, 종료해주세요"
})

// 2. 모든 Teammate 종료 후 삭제
TeamDelete()
```

### 문제: Task 의존성이 해제되지 않음

**확인**:
```typescript
// blockedBy 목록 확인
TaskGet({ taskId: "blocked-task-id" })

// 선행 Task가 completed인지 확인
TaskList()
```

---

## Memory 시스템 문제 (v2.7 신규)

### 문제: MEMORY.md가 로드되지 않음

**확인 사항**:
1. 파일 위치: `~/.claude/projects/<project-hash>/memory/MEMORY.md`
2. 파일 크기: 200줄 초과 시 잘림
3. 프로젝트 해시가 올바른지 확인

### 문제: Memory가 세션 간 유지되지 않음

**원인**: memory/ 디렉토리 외부에 저장하는 경우

**해결**:
```bash
# 올바른 위치에 저장
~/.claude/projects/<project>/memory/MEMORY.md   # ✅
~/.claude/projects/<project>/notes.md           # ❌ 로드 안됨
```

---

## Context Low 경고

### 문제: "Context is getting low" 경고

**즉시 조치**:
```bash
# compact 실행
/compact
```

**예방**:
- 불필요한 파일 읽기 최소화
- 큰 파일은 부분 읽기 사용
- 주기적으로 /compact 실행

---

## 일반적인 디버깅 팁

### 1. 로그 확인

```bash
# 세션 로그 위치
ls ~/.claude/logs/sessions/
```

### 2. 설정 검증

```bash
# settings.json 문법 검사
cat .claude/settings.json | jq .
```

### 3. 스킬 검증

```bash
# SKILL.md frontmatter 검사
head -20 .claude/skills/my-skill/SKILL.md
```

### 4. 권한 문제

```bash
# 실행 권한 일괄 부여
chmod +x .claude/hooks/*.sh
chmod +x .claude/hooks/*.ts
```

---

## Breaking Changes 문제 (v2.8-2.9)

### `$ARGUMENTS.0` → `$ARGUMENTS[0]` 마이그레이션

**증상**: 스킬에서 인자 접근 시 undefined 반환
**원인**: v2.8부터 `$ARGUMENTS.0` 문법 deprecated
**해결**: `$ARGUMENTS[0]` 또는 `$0` 사용

### `npm install` → `claude install` 변경

**증상**: MCP 서버 설치 실패
**원인**: v2.8부터 `npm install` deprecated
**해결**: `claude install` 사용

### SSE → HTTP Transport 전환

**증상**: MCP 서버 연결 불안정
**원인**: SSE transport deprecated
**해결**: `--transport http` (streamable-http) 사용

---

## 도움 받기

- **공식 문서**: https://code.claude.com/docs/en/
- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Discord**: https://discord.gg/anthropic

---

*이 문서는 SKILL.md에서 분리되었습니다 (2026-02-04, v2.9.0 업데이트 2026-02-11)*
