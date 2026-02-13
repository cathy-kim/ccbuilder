# Claude Code Extension Best Practices

> Claude Code 확장 기능 개발을 위한 통합 모범 사례 가이드

**Version**: 2.9.0
**Last Updated**: 2026-02-11

---

## 1. CLAUDE.md 설정

### 파일 위치

| 위치 | 범위 |
|------|------|
| 레포지토리 루트 | 프로젝트 전체 |
| 부모 디렉토리 | 모노레포 |
| 자식 디렉토리 | 하위 모듈 |
| `~/.claude/` | 전역 (모든 프로젝트) |

### 효과적인 작성 팁

- "IMPORTANT" 또는 "YOU MUST"로 강조
- 반복 사용하는 프롬프트로 취급하고 개선
- `#` 키로 Claude가 자동 업데이트 유도

---

## 2. Skill 모범 사례

### 필수 체크리스트

```yaml
# ✅ Frontmatter 필수
- [ ] name: 스킬 이름
- [ ] description: 설명 + 자동 활성화 키워드
- [ ] userInvocable: true/false

# ✅ 500줄 규칙
- [ ] SKILL.md < 500줄
- [ ] 상세 내용은 references/에 분리
- [ ] 빈 파일 없음

# ✅ 자동 활성화 키워드
- [ ] Use when 섹션 포함
- [ ] 한글 + 영문 혼합
- [ ] 최소 5개 이상

# ✅ Memory 연동 (v2.7)
- [ ] 세션 간 학습 필요 시 memory/ 활용
- [ ] MEMORY.md 200줄 이하

# ✅ Rules 연동 (v2.7)
- [ ] 경로별 규칙은 rules/ 활용
- [ ] paths: frontmatter 설정
```

### References 구조

```
my-skill/
├── SKILL.md          # < 500줄
├── CHANGELOG.md
├── releases/
└── references/
    ├── core-concepts.md
    ├── implementation-guide.md
    └── examples.md
```

### Deprecated 패턴

```
❌ "Phase 0: Load References" 수동 지시
❌ 모듈 최상위 환경변수 접근
❌ output styles 사용
❌ legacy SDK entrypoint
❌ $ARGUMENTS.0 문법 사용

✅ context frontmatter 사용
✅ Lazy Initialization
✅ --system-prompt-file 또는 plugins
✅ @anthropic-ai/claude-agent-sdk
✅ $ARGUMENTS[0] 사용
```

---

## 3. Agent 모범 사례

### 핵심 원칙

- ✅ 명확한 단일 책임
- ✅ 자율 실행 가능한 지시사항
- ✅ 예상 출력 형식 명시
- ✅ 필요한 도구만 허용 (allowed-tools)

### Subagent 타입 선택

| 작업 유형 | subagent_type | model | 이유 |
|----------|---------------|-------|------|
| 코드베이스 탐색 | `Explore` | haiku | 빠름, 저비용 |
| 코드 변경 | `general-purpose` | sonnet | 편집 도구 |
| 구조 설계 | `Plan` | sonnet | 아키텍처 |
| 문서 검색 | `claude-code-guide` | haiku | 공식 문서 |

### 병렬 실행

```typescript
// 단일 메시지에 여러 Task = 동시 실행
Task({ subagent_type: "frontend", prompt: "UI 작성" })
Task({ subagent_type: "backend", prompt: "API 작성" })
Task({ subagent_type: "qa-expert", prompt: "테스트 작성" })

// 제약: 최대 동시 10개, 권장 5-7개씩 배치
```

---

## 4. Agent Teams 모범 사례 (v2.7 신규)

### 핵심 원칙

- ✅ DM 우선 (브로드캐스트는 비용 N배)
- ✅ Task 의존성으로 순서 보장 (addBlockedBy)
- ✅ Teammate는 이름으로 참조 (UUID 금지)
- ✅ 평문 메시지 (JSON 상태 메시지 금지)
- ✅ TeamDelete 전 모든 Teammate 종료

### 팀 구성 패턴

| 패턴 | Teammate 구성 | 적합한 경우 |
|------|-------------|------------|
| **리뷰 팀** | 보안 + 성능 + 테스트 리뷰어 | 병렬 코드 리뷰 |
| **풀스택 팀** | Frontend + Backend + QA | 기능 개발 |
| **디버깅 팀** | 여러 가설 조사자 | 복잡한 버그 조사 |

### 비용 최적화

- Teammate 수 최소화 (3-5개 권장)
- 짧은 작업은 Task Tool 단독 사용
- 브로드캐스트 대신 DM 기본 사용

---

## 5. Memory & Rules 모범 사례 (v2.7 신규)

### Memory 작성 원칙

- ✅ MEMORY.md 200줄 이하 유지
- ✅ 토픽별 별도 파일 분리 (debugging.md, patterns.md)
- ✅ 검증된 패턴만 저장 (추측 금지)
- ✅ CLAUDE.md와 중복 방지

### Rules 작성 원칙

- ✅ `paths:` frontmatter로 범위 제한
- ✅ 핵심 규칙만 포함 (상세는 docs/reference/)
- ✅ 전체 rules/ 합계 200줄 이하 권장

---

## 6. Hook 모범 사례

### 핵심 원칙

- ✅ 실행 시간 < 100ms
- ✅ Graceful degradation (실패 시 전체 중단 금지)
- ✅ 세션 반복 알림 방지
- ✅ JSON 형식 출력

### Exit Code 규칙

| Hook | 0 | 1 | 2 |
|------|---|---|---|
| UserPromptSubmit | 계속 | stderr 표시 | - |
| PreToolUse | 허용 | - | 차단 |
| Stop | 정상 | - | - |

---

## 7. 검증된 워크플로우

### Explore → Plan → Code → Commit

1. 코딩 없이 관련 파일 읽기
2. 구현 계획 요청 ("think hard" 사용)
3. 솔루션 구현
4. 커밋 및 PR 생성

### TDD (테스트 주도 개발)

1. 예상 동작에 대한 테스트 작성
2. 구현 전 테스트 실패 확인
3. 테스트 커밋
4. 모든 테스트 통과할 때까지 반복
5. 최종 구현 커밋

### 비주얼 반복

1. 스크린샷 또는 목업 제공
2. 디자인에 따른 구현 요청
3. 비주얼 피드백 기반 반복

---

## 8. 최적화 전략

### 명확한 지침

```
❌ "add tests for foo.py"
✅ "write test case covering logged-out user edge case; avoid mocks"
```

### 컨텍스트 관리

- `/clear` 명령으로 컨텍스트 재설정
- 비주얼 컨텍스트 활용 (스크린샷, 다이어그램)
- 탭 완성으로 파일 참조

### Multi-Claude 워크플로우

- 병렬 검증: 코드 작성 + 리뷰 분리
- Git Worktrees로 병렬 작업
- Headless fanning & pipelining

---

## 9. 품질 등급

### A등급 (완전 준수)

- Frontmatter 100%
- SKILL.md < 400줄
- references/ 5개+ 문서
- 키워드 10개+
- Deprecated 패턴 0개
- Agent Teams 리뷰 체크리스트 통과 (해당 시)

### B등급 (대부분 준수)

- Frontmatter 70%+
- SKILL.md < 500줄
- references/ 3개+ 문서
- 키워드 5개+
- Deprecated 패턴 1-2개

### C등급 (개선 필요)

- Frontmatter 50% 미만
- SKILL.md > 500줄
- references/ 미흡
- Deprecated 패턴 3개+

---

## 10. 품질 메트릭

```yaml
skills:
  trigger_accuracy: "> 85%"
  response_quality: "> 80%"
  lines: "< 500"

agents:
  completion_rate: "> 90%"
  accuracy: "> 85%"
  duration: "< 60s"

hooks:
  latency_p99: "< 100ms"
  error_rate: "< 1%"
```

---

## 11. 자동화 스크립트

### 500줄 초과 스킬 찾기

```bash
for f in skills/*/SKILL.md; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 500 ]; then
    echo "$f: $lines lines (OVER)"
  fi
done
```

### Frontmatter 검증

```bash
for f in skills/*/SKILL.md; do
  echo "=== $f ==="
  head -30 "$f" | grep -E "^(name|description|userInvocable|model|allowed-tools):"
done
```

---

## 참고 문서

- [Skills Guide](skills-guide.md)
- [Hooks Guide](hooks-guide.md)
- [Subagents Guide](subagents-guide.md)
- [Agent Teams Guide](agent-teams-guide.md)
- [Evaluation Framework](../evaluations/evaluation-framework.md)
- [Review System](review-system.md)

---

*통합 문서: best-practices-qa-guide.md + claude-code-best-practices.md + skill-review-guidelines.md (2026-02-04, v2.9.0 업데이트 2026-02-11)*
