# Agent Teams 상세 가이드

> Claude Code Agent Teams 개발 완전 가이드

**Version**: 2.7.0
**Last Updated**: 2026-02-11
**Claude Code Version**: v2.1.39+
**Status**: Experimental (Research Preview)

---

## 개요

Agent Teams는 여러 Claude Code 인스턴스가 팀으로 협업하는 시스템입니다.
Team Lead가 Teammate들을 생성하고, 공유 Task List로 작업을 조율합니다.

```
Team Lead (Main Session)
├── Teammate A (독립 컨텍스트)
├── Teammate B (독립 컨텍스트)
└── Teammate C (독립 컨텍스트)
    └── 공유 Task List (~/.claude/tasks/{team-name}/)
```

---

## 활성화

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 핵심 도구

### TeamCreate - 팀 생성

```typescript
TeamCreate({
  team_name: "feature-team",
  description: "User auth feature 개발"
})
```

생성되는 리소스:
- `~/.claude/teams/{team-name}/config.json` - 팀 설정
- `~/.claude/tasks/{team-name}/` - 공유 Task List

### TaskCreate - 작업 생성

```typescript
TaskCreate({
  subject: "Build REST API",
  description: "인증 관련 REST API 엔드포인트 구현",
  activeForm: "Building REST API"  // 진행 중 표시 텍스트
})
```

### TaskUpdate - 작업 관리

```typescript
// 작업 시작
TaskUpdate({ taskId: "1", status: "in_progress" })

// 소유자 지정
TaskUpdate({ taskId: "1", owner: "api-developer" })

// 의존성 설정
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })

// 작업 완료
TaskUpdate({ taskId: "1", status: "completed" })
```

### Task - Teammate 생성

```typescript
Task({
  description: "Build API endpoints",
  prompt: "REST API 엔드포인트를 구현하세요",
  subagent_type: "backend",       // 에이전트 타입
  team_name: "feature-team",      // 팀 이름
  name: "api-developer",          // Teammate 이름
  mode: "bypassPermissions"       // 권한 모드
})
```

### SendMessage - 커뮤니케이션

```typescript
// DM 전송
SendMessage({
  type: "message",
  recipient: "api-developer",
  content: "DB 스키마 먼저 정의해주세요",
  summary: "DB 스키마 요청"
})

// 전체 브로드캐스트 (비용 주의)
SendMessage({
  type: "broadcast",
  content: "테스트 서버가 다운됐습니다",
  summary: "서버 다운 알림"
})

// 종료 요청
SendMessage({
  type: "shutdown_request",
  recipient: "api-developer",
  content: "작업 완료, 종료해주세요"
})
```

### TeamDelete - 팀 정리

```typescript
TeamDelete()  // 현재 팀 리소스 제거
```

---

## 전체 워크플로우

```
1. TeamCreate({ team_name: "my-team" })
2. TaskCreate({ subject: "Task A", ... })
3. TaskCreate({ subject: "Task B", ... })
4. TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })  // B는 A 완료 후
5. Task({ team_name: "my-team", name: "worker-a", ... })  // Teammate 생성
6. Task({ team_name: "my-team", name: "worker-b", ... })  // Teammate 생성
7. TaskUpdate({ taskId: "1", owner: "worker-a" })  // 작업 할당
8. // Teammate들이 작업 수행...
9. SendMessage({ type: "shutdown_request", ... })  // 종료 요청
10. TeamDelete()  // 정리
```

---

## Teammate 상태

| 상태 | 의미 |
|------|------|
| **Active** | 작업 수행 중 |
| **Idle** | 작업 대기 (정상 - 메시지로 깨울 수 있음) |
| **Shutdown** | 종료됨 |

**주의**: Idle은 에러가 아닙니다. Teammate가 메시지 전송 후 Idle 상태가 되는 것은 정상 흐름입니다.

---

## 표시 모드

| 모드 | 설정 | 설명 |
|------|------|------|
| **in-process** | 기본값 | 모든 Teammate가 하나의 터미널에 표시 |
| **tmux** | `teammateMode: "tmux"` | 각 Teammate가 별도 tmux 패널 |

```json
// settings.json
{
  "teammateMode": "tmux"
}
```

---

## 팀 구성 읽기

```typescript
// ~/.claude/teams/{team-name}/config.json
{
  "members": [
    {
      "name": "team-lead",      // 항상 이름으로 참조
      "agentId": "abc-123",     // 참조용 (통신에 사용 안 함)
      "agentType": "general-purpose"
    },
    {
      "name": "api-developer",
      "agentId": "def-456",
      "agentType": "backend"
    }
  ]
}
```

---

## Task 의존성

```
Task A (pending)
  └── blocks → Task B (blocked)
                └── blocks → Task C (blocked)
```

- `addBlocks`: 이 Task가 완료되어야 시작할 수 있는 Task들
- `addBlockedBy`: 이 Task 시작 전 완료되어야 하는 Task들
- blockedBy가 모두 완료되면 자동으로 unblock

---

## 적합한 사용 사례

| 사용 사례 | 왜 Agent Teams? |
|----------|----------------|
| **병렬 코드 리뷰** | 보안, 성능, 테스트 리뷰어가 동시 진행 |
| **Full-stack 기능 개발** | Frontend, Backend, Tests 동시 작업 |
| **경쟁 가설 디버깅** | 여러 원인을 동시에 조사 |
| **리서치 + 구현** | 조사와 코딩을 분리하여 병렬 진행 |

---

## 비용 고려

- 각 Teammate는 별도 Claude 인스턴스 (토큰 사용량 N배)
- 브로드캐스트는 N명에게 개별 전송 (비용 선형 증가)
- DM이 브로드캐스트보다 효율적 - 기본적으로 DM 사용
- 가장 효율적인 ROI: 리서치, 리뷰, 탐색적 작업

---

## 주의사항

- **실험적 기능**: 향후 API 변경 가능
- **TeamDelete 전 종료 필수**: 활성 Teammate가 있으면 삭제 실패
- **이름으로 참조**: Teammate는 항상 `name`으로 참조 (UUID 사용 금지)
- **평문 메시지**: JSON 상태 메시지 전송 금지, 자연어로 소통
- **TaskUpdate로 완료 표시**: 자동 idle 알림은 시스템이 처리

---

## Hook 연동

### TeammateIdle Hook

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

## 공식 문서

- **Agent Teams**: https://code.claude.com/docs/en/agent-teams

---

*이 문서는 v2.7.0에서 신규 생성되었습니다 (2026-02-11)*
