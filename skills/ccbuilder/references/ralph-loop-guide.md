# Ralph Loop (Fresh Context Pattern) Guide

**Version**: 1.0.0
**Last Updated**: 2026-02-13

---

## 개요

Ralph Loop(Fresh Context Pattern)은 Claude Code의 컨텍스트 윈도우 열화 문제를 해결하는 자율 개발 루프 패턴입니다. 매 반복마다 새로운 Claude Code 세션을 생성하면서, 파일 시스템과 Git을 통해 상태를 유지합니다.

**핵심 원리**: 컨텍스트 윈도우를 0%로 리셋하면서 모든 상태를 영구 파일에 보존

```
Session 1 → Read TASK.md + PROGRESS.md → Execute task → Git commit
    ↓
Session 2 → Read TASK.md + PROGRESS.md (updated) → Execute next → Git commit
    ↓
Session N → LOOP_COMPLETE marker 감지 → Exit
```

---

## 핵심 개념

### 컨텍스트 윈도우 열화 (Context Degradation)

| 컨텍스트 사용량 | 성능 수준 |
|-----------------|-----------|
| 0-50% | Baseline (정상) |
| 50-80% | 점진적 저하 |
| 80-92% | 심각한 저하 |
| 92%+ | 자동 compaction 발생 |

Ralph Loop는 매 반복에서 컨텍스트를 0%로 리셋하여 항상 최적 성능을 유지합니다.

### 패턴 비교

| 항목 | Ralph Loop | Tasks API | /compact |
|------|-----------|-----------|----------|
| 컨텍스트 리셋 | 완전 (0%) | 부분 (~50%) | 부분 (50%) |
| 상태 저장 | 파일 + Git | 디스크 | 세션 메모리 |
| 멀티세션 | Yes | Yes | No |
| 적합 사례 | 대규모 리팩토링, 자율 개발 | 기능 개발 | 세션 중간 정리 |

---

## 디렉토리 구조

### 기본 구조 (Simple)

```
project-root/
├── TASK.md              # 목표 정의 (불변)
├── PROGRESS.md          # 진행 상태 (반복마다 업데이트)
├── loop.sh              # 루프 스크립트
└── src/                 # 프로젝트 소스
```

### Ralph 프레임워크 구조 (Advanced)

```
project-root/
├── .ralph/
│   ├── PROMPT.md        # 고수준 개발 목표
│   ├── fix_plan.md      # 우선순위 작업 목록
│   ├── AGENT.md         # 빌드/테스트 명령어 (자동 관리)
│   ├── specs/           # 상세 요구사항
│   │   └── stdlib/      # 재사용 패턴
│   └── logs/            # 세션 로그
├── .ralphrc             # 프로젝트 설정
└── src/                 # 프로젝트 소스
```

---

## 핵심 파일

### TASK.md (불변 - Claude가 읽기만 함)

```markdown
# Task: REST API 구현

## 목표
Express.js 기반 REST API 구현 (CRUD + 테스트 + 문서)

## 요구사항
1. User, Post 엔드포인트 구현
2. JWT 인증 적용
3. Jest 테스트 커버리지 80% 이상
4. Swagger 문서 자동 생성

## 완료 조건
- 모든 테스트 통과
- API 문서 생성 완료
- PROGRESS.md에 LOOP_COMPLETE 마커 기록
```

### PROGRESS.md (반복마다 업데이트)

```markdown
# Progress

## Iteration 1 - 2026-02-13 10:00
- ✅ Express 프로젝트 초기화
- ✅ User 모델 + CRUD 엔드포인트
- ⚠️ JWT 미적용 (다음 반복에서 처리)
- **Next**: JWT 인증 미들웨어 구현

## Iteration 2 - 2026-02-13 10:15
- ✅ JWT 인증 미들웨어
- ✅ Post 모델 + CRUD 엔드포인트
- **Next**: 테스트 작성

## Iteration 3 - 2026-02-13 10:30
- ✅ Jest 테스트 (커버리지 85%)
- ✅ Swagger 문서 생성
- ✅ 모든 요구사항 충족

LOOP_COMPLETE
```

---

## 구현

### 방법 1: Simple Bash Loop (권장 시작점)

```bash
#!/bin/bash
set -e

MAX_ITERATIONS=${1:-10}
TASK_FILE=${2:-TASK.md}
PROGRESS_FILE=${3:-PROGRESS.md}

# 사전 검증
if [[ ! -f "$TASK_FILE" ]]; then
  echo "Error: $TASK_FILE not found"
  exit 1
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
  echo "# Progress" > "$PROGRESS_FILE"
fi

iteration=1
while [[ $iteration -le $MAX_ITERATIONS ]]; do
  echo "═══════════════════════════════════════"
  echo "  Iteration $iteration/$MAX_ITERATIONS"
  echo "═══════════════════════════════════════"

  # 프롬프트를 임시 파일로 생성 (heredoc 중첩 문제 방지)
  PROMPT_FILE=$(mktemp)
  {
    echo "다음 TASK와 PROGRESS를 읽고 작업을 수행하세요."
    echo ""
    echo "## TASK"
    cat "$TASK_FILE"
    echo ""
    echo "## PROGRESS"
    cat "$PROGRESS_FILE"
    echo ""
    echo "## 지침"
    echo "1. 다음 미완료 작업 1개만 수행하세요"
    echo "2. 테스트/빌드로 변경사항 검증하세요"
    echo "3. PROGRESS.md를 업데이트하세요 (✅/❌/⚠️ + **Next**)"
    echo "4. 모든 작업 완료 시 PROGRESS.md 마지막 줄에 추가:"
    echo "   LOOP_COMPLETE"
  } > "$PROMPT_FILE"

  # 새 세션 생성 + 상태 주입
  claude -p --allowedTools 'Read,Write,Edit,Bash,Glob,Grep' \
    < "$PROMPT_FILE" || true
  rm -f "$PROMPT_FILE"

  # 자동 커밋 (변경사항 있으면)
  if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    git add -A
    git commit -m "ralph: iteration $iteration" --no-verify 2>/dev/null || true
  fi

  # 완료 마커 확인 (줄 시작이 LOOP_COMPLETE인 경우만)
  if grep -q "^LOOP_COMPLETE" "$PROGRESS_FILE" 2>/dev/null; then
    echo "✅ All tasks completed in $iteration iterations"
    exit 0
  fi

  ((iteration++))
  sleep 2  # API rate limit 방지
done

echo "⏱️ Max iterations ($MAX_ITERATIONS) reached"
exit 1
```

### 방법 2: Stop Hook 기반 (Claude Code 내장)

Claude Code의 Stop Hook을 활용하여 루프를 구현합니다.

**settings.json**:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "./.claude/hooks/ralph-stop.sh"
          }
        ]
      }
    ]
  }
}
```

**`.claude/hooks/ralph-stop.sh`**:
```bash
#!/bin/bash

# Stop 시점에 Claude의 출력을 stdin으로 받음
RESULT=$(cat)

# 1. Claude 출력에서 완료 마커 확인
if echo "$RESULT" | grep -q "^LOOP_COMPLETE"; then
  exit 0
fi

# 2. PROGRESS.md에서 완료 마커 확인
if [[ -f "PROGRESS.md" ]] && grep -q "^LOOP_COMPLETE" "PROGRESS.md"; then
  exit 0
fi

# 3. 최대 반복 체크 (안전장치)
ITERATION_COUNT=$(grep -c "^## Iteration" "PROGRESS.md" 2>/dev/null || echo "0")
MAX_ITERATIONS=${RALPH_MAX_ITERATIONS:-20}
if [[ "$ITERATION_COUNT" -ge "$MAX_ITERATIONS" ]]; then
  echo "최대 반복 횟수($MAX_ITERATIONS)에 도달. 종료합니다." >&2
  exit 0
fi

# 완료되지 않았으면 종료 차단 + 계속 지시
echo "아직 TASK.md의 모든 작업이 완료되지 않았습니다. 다음 미완료 작업을 수행하세요." >&2
exit 1
```

### 방법 3: Ralph 프레임워크 사용 (Full-featured)

```bash
# Ralph 설치
git clone https://github.com/frankbria/ralph-claude-code.git
cd ralph-claude-code && ./install.sh

# 기존 프로젝트에 적용
cd my-project
ralph-enable          # 대화형 위자드

# 실행
ralph --monitor       # tmux 대시보드 포함
ralph --live          # 실시간 출력
```

---

## 설정 (.ralphrc)

```bash
# 프로젝트 기본
PROJECT_NAME="my-project"
PROJECT_TYPE="typescript"      # typescript, python, rust, go 등

# 루프 설정
MAX_CALLS_PER_HOUR=100         # API 호출 제한
CLAUDE_TIMEOUT_MINUTES=15      # 세션 타임아웃
CLAUDE_OUTPUT_FORMAT="json"    # json 또는 text

# 도구 권한
ALLOWED_TOOLS="Write,Read,Edit,Bash(git *),Bash(npm *),Bash(pytest)"

# 세션 관리
SESSION_CONTINUITY=true        # --resume 지원
SESSION_EXPIRY_HOURS=24        # 세션 만료

# 서킷 브레이커 (안전장치)
CB_NO_PROGRESS_THRESHOLD=3    # 진행 없음 N회 후 중단
CB_SAME_ERROR_THRESHOLD=5     # 동일 에러 N회 후 중단
CB_COOLDOWN_MINUTES=30        # 쿨다운 시간
CB_AUTO_RESET=false           # 자동 리셋 여부
```

---

## 종료 감지 (Exit Detection)

### 이중 조건 게이트 (Dual-Condition Exit)

Ralph는 **두 가지 조건 모두** 충족해야 종료합니다:

| 조건 | 설명 | 예시 |
|------|------|------|
| `completion_indicators >= 2` | 자연어 완료 패턴 감지 | "Complete", "Done", "✅ All tasks" |
| `EXIT_SIGNAL: true` | 명시적 종료 신호 | RALPH_STATUS 블록 내 |

```markdown
## RALPH_STATUS
STATUS: COMPLETE
EXIT_SIGNAL: true
completion_count: 2
```

이 이중 게이트는 **조기 종료를 방지**합니다. Claude가 "Phase complete"라 출력해도 `EXIT_SIGNAL: false`면 루프가 계속됩니다.

### 서킷 브레이커 (Safety)

| 트리거 | 기본값 | 동작 |
|--------|--------|------|
| 진행 없음 | 3회 | 루프 중단 |
| 동일 에러 반복 | 5회 | 루프 중단 |
| API 한도 초과 | 5시간 | 자동 대기 |

---

## 사용 시나리오

### 적합한 경우

- **대규모 리팩토링**: 30-90분 규모의 코드 변경
- **자율 기능 개발**: 야간 자동 개발
- **반복 테스트/수정**: TDD 루프
- **배치 처리**: 여러 파일 일괄 변환
- **CI/CD 통합**: 자동화 파이프라인

### 부적합한 경우

- **5분 이내 작업**: 세션 오버헤드(5-10초)가 비효율적
- **대화형 작업**: 실시간 피드백이 필요한 경우
- **탐색/질문**: 단일 세션이 더 효율적

### 작업 크기 가이드

| 작업 규모 | 권장 방식 |
|-----------|-----------|
| < 5분 | 단일 세션 (직접 `claude` 사용) |
| 5-30분 | Simple Loop (방법 1) |
| 30-90분 | Ralph 프레임워크 (방법 3) |
| 90분+ | Agent Team + Ralph 하이브리드 |

---

## 모범 사례

### TASK.md 작성

1. **명확한 완료 조건** 정의 (테스트 통과, 파일 생성 등)
2. **작업 단위** 하나당 3-10 반복 분량으로 설계
3. **불변 유지** - Claude가 수정하지 않도록 지시

### PROGRESS.md 관리

1. **간결하게** - 10K 줄 이하 유지
2. **구조화** - 반복 번호, 상태 아이콘, 다음 작업 명시
3. **블로커 기록** - 문제 발생 시 컨텍스트와 함께 기록

### 안전 운영

1. **항상 반복 상한** 설정 (`MAX_ITERATIONS` 또는 `--calls`)
2. **Git 커밋** 활용 - 롤백 가능성 확보
3. **서킷 브레이커** 활성화 - 무한 루프 방지
4. **도구 권한** 최소화 - `ALLOWED_TOOLS`로 필요한 것만 허용

### 하이브리드 워크플로우

```
Tasks API (고수준 분해)
  └─ Ralph Loop (서브태스크별 실행, 각각 Fresh Context)
      ├─ Subtask 1 → 5 iterations → COMPLETE
      ├─ Subtask 2 → 3 iterations → COMPLETE
      └─ Subtask 3 → 7 iterations → COMPLETE
```

---

## Slash Command 연동

ccbuilder에서 Ralph Loop를 스캐폴딩하려면:

```
/ccbuilder ralph <project-name>
```

생성되는 파일:
- `TASK.md` - 목표 정의 템플릿
- `PROGRESS.md` - 빈 진행 파일
- `loop.sh` - 루프 실행 스크립트
- `.claude/hooks/ralph-stop.sh` - Stop Hook (선택)
- `.ralphrc` - 프로젝트 설정 (선택)

---

## 참고 자료

- [frankbria/ralph-claude-code](https://github.com/frankbria/ralph-claude-code) - Ralph 프레임워크
- [disler/infinite-agentic-loop](https://github.com/disler/infinite-agentic-loop) - 무한 에이전틱 루프
- [AnandChowdhary/continuous-claude](https://github.com/AnandChowdhary/continuous-claude) - Continuous Claude
- [Fresh Context Pattern (DeepWiki)](https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/9.5-fresh-context-pattern-(ralph-loop))
- [Ralph Loop: Defining AI Development in 2026](https://namiru.ai/blog/the-ralph-loop-why-this-claude-code-plugin-is-defining-ai-development-in-2026)

---

**Status**: NEW (2026-02-13)
