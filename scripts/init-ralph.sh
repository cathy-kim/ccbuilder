#!/bin/bash

# Claude Code Ralph Loop 초기화 스크립트
# Usage: ./init-ralph.sh <project-name> [method]
# Methods: simple (default), hook, full

set -e

PROJECT_NAME="$1"
METHOD="${2:-simple}"

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: $0 <project-name> [method]"
  echo ""
  echo "Methods:"
  echo "  simple  - Bash loop + TASK.md + PROGRESS.md (default)"
  echo "  hook    - Stop Hook 기반 자동 루프"
  echo "  full    - Simple + Hook + .ralphrc 전체 설정"
  echo ""
  echo "Examples:"
  echo "  $0 my-api"
  echo "  $0 my-api hook"
  echo "  $0 my-api full"
  exit 1
fi

# 방법 검증
if [[ ! "$METHOD" =~ ^(simple|hook|full)$ ]]; then
  echo "Error: Invalid method '$METHOD'. Must be: simple, hook, or full"
  exit 1
fi

echo "═══════════════════════════════════════"
echo "  Ralph Loop Setup: $PROJECT_NAME"
echo "  Method: $METHOD"
echo "═══════════════════════════════════════"
echo ""

# ──────────────────────────────────────
# TASK.md 생성
# ──────────────────────────────────────

if [ -f "TASK.md" ]; then
  echo "⚠️  TASK.md already exists, skipping"
else
  cat > TASK.md << EOF
# Task: $PROJECT_NAME

## 목표

[TODO: 프로젝트 목표를 명확하게 작성하세요]

## 요구사항

1. [TODO: 요구사항 1]
2. [TODO: 요구사항 2]
3. [TODO: 요구사항 3]

## 완료 조건

- [ ] [TODO: 테스트 통과 조건]
- [ ] [TODO: 구현 완료 조건]
- [ ] PROGRESS.md에 LOOP_COMPLETE 마커 기록

## 제약사항

- 한 번에 하나의 작업만 수행
- 각 반복 후 테스트/빌드로 검증
- TASK.md는 수정하지 않음
EOF
  echo "✅ Created TASK.md"
fi

# ──────────────────────────────────────
# PROGRESS.md 생성
# ──────────────────────────────────────

if [ -f "PROGRESS.md" ]; then
  echo "⚠️  PROGRESS.md already exists, skipping"
else
  cat > PROGRESS.md << 'EOF'
# Progress

<!-- 형식: ## Iteration N - YYYY-MM-DD HH:MM -->
<!-- ✅ 완료 / ❌ 실패 / ⚠️ 부분완료 / **Next**: 다음 작업 -->
<!-- 모든 작업 완료 시 마지막 줄에 완료 마커를 추가합니다 -->
EOF
  echo "✅ Created PROGRESS.md"
fi

# ──────────────────────────────────────
# loop.sh 생성 (simple, full)
# ──────────────────────────────────────

if [[ "$METHOD" == "simple" || "$METHOD" == "full" ]]; then
  if [ -f "loop.sh" ]; then
    echo "⚠️  loop.sh already exists, skipping"
  else
    cat > loop.sh << 'SCRIPT'
#!/bin/bash
set -e

# ═══════════════════════════════════════
# Ralph Loop - Simple Bash Implementation
# ═══════════════════════════════════════

MAX_ITERATIONS=${1:-10}
TASK_FILE=${2:-TASK.md}
PROGRESS_FILE=${3:-PROGRESS.md}

# 색상
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 사전 검증
if [[ ! -f "$TASK_FILE" ]]; then
  echo -e "${RED}Error: $TASK_FILE not found${NC}"
  exit 1
fi

if ! command -v claude &> /dev/null; then
  echo -e "${RED}Error: claude CLI not found. Install: https://code.claude.com${NC}"
  exit 1
fi

if [[ ! -f "$PROGRESS_FILE" ]]; then
  echo "# Progress" > "$PROGRESS_FILE"
fi

echo -e "${GREEN}Starting Ralph Loop${NC}"
echo "  Max iterations: $MAX_ITERATIONS"
echo "  Task file: $TASK_FILE"
echo "  Progress file: $PROGRESS_FILE"
echo ""

iteration=1
while [[ $iteration -le $MAX_ITERATIONS ]]; do
  echo "═══════════════════════════════════════"
  echo -e "  ${YELLOW}Iteration $iteration/$MAX_ITERATIONS${NC}"
  echo "  $(date '+%Y-%m-%d %H:%M:%S')"
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
    echo "1. PROGRESS에서 다음 미완료 작업을 확인하세요"
    echo "2. 해당 작업 1개만 수행하세요 (한 번에 하나씩)"
    echo "3. 테스트/빌드로 변경사항을 검증하세요"
    echo "4. PROGRESS.md를 업데이트하세요:"
    echo "   - ## Iteration $iteration - $(date '+%Y-%m-%d %H:%M')"
    echo "   - 완료/실패/부분완료 상태"
    echo "   - 발견된 문제"
    echo "   - **Next**: 다음에 할 작업"
    echo "5. TASK.md의 모든 작업이 완료되고 검증되면 PROGRESS.md 마지막에 이 줄을 추가하세요:"
    echo "   LOOP_COMPLETE"
  } > "$PROMPT_FILE"

  # 새 세션 생성 + 상태 주입
  claude -p \
    --allowedTools 'Read,Write,Edit,Bash,Glob,Grep' \
    < "$PROMPT_FILE" || true

  rm -f "$PROMPT_FILE"

  # 자동 커밋 (변경사항 있으면)
  if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
    git add -A
    git commit -m "ralph: iteration $iteration" --no-verify 2>/dev/null || true
  fi

  # 완료 마커 확인 (줄 시작이 LOOP_COMPLETE인 경우만 매칭)
  if grep -q "^LOOP_COMPLETE" "$PROGRESS_FILE" 2>/dev/null; then
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ All tasks completed!${NC}"
    echo -e "${GREEN}  Iterations: $iteration${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    exit 0
  fi

  ((iteration++))

  # 반복 간 짧은 대기 (API rate limit 방지)
  sleep 2
done

echo ""
echo -e "${YELLOW}⏱️ Max iterations ($MAX_ITERATIONS) reached without completion${NC}"
echo "Check PROGRESS.md for current status."
exit 1
SCRIPT
    chmod +x loop.sh
    echo "✅ Created loop.sh (executable)"
  fi
fi

# ──────────────────────────────────────
# Stop Hook 생성 (hook, full)
# ──────────────────────────────────────

if [[ "$METHOD" == "hook" || "$METHOD" == "full" ]]; then
  HOOK_DIR=".claude/hooks"
  HOOK_FILE="$HOOK_DIR/ralph-stop.sh"

  mkdir -p "$HOOK_DIR"

  if [ -f "$HOOK_FILE" ]; then
    echo "⚠️  $HOOK_FILE already exists, skipping"
  else
    cat > "$HOOK_FILE" << 'HOOK'
#!/bin/bash

# ═══════════════════════════════════════
# Ralph Loop - Stop Hook
# ═══════════════════════════════════════
# Claude가 종료하려 할 때 실행됩니다.
# exit 0 = 종료 허용
# exit 1 = 종료 차단 (stderr 메시지가 Claude에게 전달)

# Claude 출력을 stdin으로 받음
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
  echo "⏱️ 최대 반복 횟수($MAX_ITERATIONS)에 도달했습니다. 종료합니다." >&2
  exit 0
fi

# 완료되지 않았으면 종료 차단
echo "아직 TASK.md의 모든 작업이 완료되지 않았습니다. PROGRESS.md를 확인하고 다음 미완료 작업을 수행하세요. 모든 작업 완료 후 PROGRESS.md에 LOOP_COMPLETE를 추가하세요." >&2
exit 1
HOOK
    chmod +x "$HOOK_FILE"
    echo "✅ Created $HOOK_FILE (executable)"

    # settings.json 안내
    echo ""
    echo "📋 settings.json에 다음을 추가하세요:"
    echo ""
    echo '  {'
    echo '    "hooks": {'
    echo '      "Stop": [{'
    echo '        "matcher": "",'
    echo '        "hooks": [{'
    echo '          "type": "command",'
    echo "          \"command\": \"$HOOK_FILE\""
    echo '        }]'
    echo '      }]'
    echo '    }'
    echo '  }'
  fi
fi

# ──────────────────────────────────────
# .ralphrc 생성 (full만)
# ──────────────────────────────────────

if [[ "$METHOD" == "full" ]]; then
  if [ -f ".ralphrc" ]; then
    echo "⚠️  .ralphrc already exists, skipping"
  else
    # 프로젝트 타입 자동 감지
    PROJECT_TYPE="unknown"
    if [ -f "package.json" ]; then
      PROJECT_TYPE="javascript"
      if grep -q '"typescript"' package.json 2>/dev/null || [ -f "tsconfig.json" ]; then
        PROJECT_TYPE="typescript"
      fi
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
      PROJECT_TYPE="python"
    elif [ -f "Cargo.toml" ]; then
      PROJECT_TYPE="rust"
    elif [ -f "go.mod" ]; then
      PROJECT_TYPE="go"
    fi

    cat > .ralphrc << EOF
# Ralph Loop Configuration
# Project: $PROJECT_NAME

PROJECT_NAME="$PROJECT_NAME"
PROJECT_TYPE="$PROJECT_TYPE"

# Loop settings
MAX_ITERATIONS=10
CLAUDE_TIMEOUT_MINUTES=15

# Tool permissions (comma-separated)
ALLOWED_TOOLS="Write,Read,Edit,Bash,Glob,Grep"

# Circuit breaker (safety)
CB_NO_PROGRESS_THRESHOLD=3    # Stop after N iterations without progress
CB_SAME_ERROR_THRESHOLD=5     # Stop after N identical errors
CB_COOLDOWN_MINUTES=30        # Cooldown before auto-retry
EOF
    echo "✅ Created .ralphrc (detected: $PROJECT_TYPE)"
  fi

  # .gitignore에 추가
  if [ -f ".gitignore" ]; then
    if ! grep -q ".ralphrc" ".gitignore" 2>/dev/null; then
      echo "" >> .gitignore
      echo "# Ralph Loop" >> .gitignore
      echo ".ralphrc" >> .gitignore
      echo "✅ Added .ralphrc to .gitignore"
    fi
  fi
fi

# ──────────────────────────────────────
# 완료 메시지
# ──────────────────────────────────────

echo ""
echo "═══════════════════════════════════════"
echo "  ✅ Ralph Loop setup complete!"
echo "═══════════════════════════════════════"
echo ""
echo "Created files:"
[ -f "TASK.md" ] && echo "  📄 TASK.md          - 목표 정의 (편집 필수)"
[ -f "PROGRESS.md" ] && echo "  📄 PROGRESS.md      - 진행 추적"
[ -f "loop.sh" ] && echo "  🔄 loop.sh          - 루프 실행 스크립트"
[ -f ".claude/hooks/ralph-stop.sh" ] && echo "  🪝 .claude/hooks/ralph-stop.sh - Stop Hook"
[ -f ".ralphrc" ] && echo "  ⚙️  .ralphrc          - 프로젝트 설정"
echo ""
echo "Next steps:"
echo "  1. TASK.md를 편집하여 목표와 요구사항을 작성하세요"

if [[ "$METHOD" == "simple" || "$METHOD" == "full" ]]; then
  echo "  2. 실행: ./loop.sh [max-iterations]"
  echo "     예: ./loop.sh 10"
fi

if [[ "$METHOD" == "hook" ]]; then
  echo "  2. settings.json에 Stop Hook을 등록하세요 (위 안내 참고)"
  echo "  3. claude 실행 후 TASK.md의 작업을 지시하세요"
  echo "     Claude가 완료될 때까지 자동으로 루프합니다"
fi

if [[ "$METHOD" == "full" ]]; then
  echo "  3. .ralphrc에서 설정을 조정하세요"
  echo "  4. settings.json에 Stop Hook을 등록하세요 (위 안내 참고)"
fi
