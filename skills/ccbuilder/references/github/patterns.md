# Cross-Repository Patterns & Learning Points

> 여러 레포에서 반복적으로 나타나는 검증된 패턴 정리.

**Last Updated**: 2026-02-11

---

## 1. Progressive Disclosure (점진적 공개)

**출처**: anthropics/skills, wshobson/agents

```
Level 1: 메타데이터 (항상 로드) → name, description만
Level 2: 본문 (활성화 시) → SKILL.md 지시사항
Level 3: 리소스 (필요 시) → references/, resources/, scripts/
```

**핵심**: SKILL.md 500줄 이하 유지. 상세 내용은 references/로 분리.

---

## 2. 3-Tier Model Strategy (모델 계층화)

**출처**: wshobson/agents

| Tier | 모델 | 용도 |
|------|------|------|
| Critical | Opus | 아키텍처 결정, 보안 리뷰 |
| Development | Sonnet | 코드 작성, 리팩토링 |
| Operational | Haiku | 파일 탐색, 간단한 검증 |

**핵심**: 모든 작업에 같은 모델 쓰지 말기. 비용과 속도 최적화.

---

## 3. Subagent-Driven Development (에이전트 위임 개발)

**출처**: obra/superpowers

```
1. Agent 파견 (Dispatch): 명확한 작업 지시 + 독립 컨텍스트
2. 리뷰 (Review): 결과물을 별도 Agent가 검증
```

**핵심**: 한 Agent가 모든 것을 하지 않음. 파견 → 리뷰 분리.

---

## 4. Continuous Learning (지속적 학습)

**출처**: affaan-m/everything-claude-code

```
세션 중 발견한 패턴 → "Instinct"로 추출 → 신뢰도 점수 부여 → Memory에 저장
```

**핵심**: 세션 간 학습이 누적되어 갈수록 정확한 코드 생성.

---

## 5. Ticket-to-Code Workflow (티켓 기반 개발)

**출처**: ChrisWiles/claude-code-showcase

```
JIRA 티켓 읽기 → 코드 구현 → PR 생성 → JIRA 상태 업데이트
```

**필요 구성**:
- `.mcp.json`: JIRA, GitHub MCP 서버
- Agent: Ticket Handler
- Command: `/ticket`
- Hook: Main 브랜치 보호

---

## 6. Scheduled Agent Workflows (예약 실행)

**출처**: ChrisWiles/claude-code-showcase

```yaml
# GitHub Actions
schedule:
  - cron: '0 9 * * 1'  # 매주 월요일 9시
jobs:
  quality-review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
```

| 스케줄 | 작업 |
|--------|------|
| 월별 | 문서 동기화 |
| 주별 | 코드 품질 리뷰 |
| 격주 | 의존성 감사 |

---

## 7. Safety-First Hooks (안전 우선 Hook)

**출처**: disler/claude-code-hooks-mastery, karanb192/claude-code-hooks

| Hook | 패턴 |
|------|------|
| `PreToolUse(Bash)` | 위험 명령 사전 차단 (`rm -rf`, `DROP TABLE`) |
| `PreToolUse(Read/Edit)` | `.env`, 자격 증명 파일 접근 차단 |
| `PostToolUse(Edit)` | 편집 후 자동 git stage |
| `Notification` | 권한 요청 시 Slack/Discord 알림 |

---

## 8. Agent-in-Agent Pattern (에이전트 중첩)

**출처**: steipete/claude-code-mcp

```
외부 AI Tool (Cursor, Windsurf) → MCP 호출 → Claude Code → 작업 수행
```

**핵심**: Claude Code를 MCP 서버로 노출하여 다른 도구에서 호출.

---

## 9. Multi-Agent Observability (멀티 에이전트 관측)

**출처**: disler/claude-code-hooks-multi-agent-observability

```
Claude Agents → Hook 스크립트 → HTTP POST → 서버 → SQLite → WebSocket → 대시보드
```

**핵심**: 여러 Agent가 병렬로 작업할 때 실시간 모니터링 + 이벤트 추적.

---

## 10. Non-Technical Skills (비기술 Skill)

**출처**: alirezarezvani/claude-skills

**기존 인식**: Skill = 코드 생성/개발 도구
**확장**: 마케팅, PM, 경영 자문, 규제 준수도 Skill로 구현 가능

| 도메인 | 예시 |
|--------|------|
| 마케팅 | Content Creator, Campaign Analytics |
| 경영 | CEO Advisor, CTO Advisor |
| 프로젝트 | Scrum Master, Jira Expert |
| 규제 | Compliance Framework (12종) |

---

## 패턴 적용 우선순위

```
새 Skill 만들 때:
1. Progressive Disclosure 적용 (500줄 규칙)
2. Model Strategy 설정 (Opus/Sonnet/Haiku)
3. Safety Hooks 추가 (최소한 위험 명령 차단)
4. Memory 연동 (패턴 축적)

팀 워크플로우 구축 시:
1. Ticket-to-Code 패턴 참조
2. Scheduled Agents 설정
3. Multi-Agent Observability 추가
4. Subagent-Driven Development 적용
```
