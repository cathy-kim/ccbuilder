#!/bin/bash

# Claude Code Hook 테스트 스크립트
# Usage: ./test-hook.sh <hook-file> <hook-type> [test-case]

set -e

HOOK_FILE="$1"
HOOK_TYPE="$2"
TEST_CASE="$3"

if [ -z "$HOOK_FILE" ] || [ -z "$HOOK_TYPE" ]; then
  echo "Usage: $0 <hook-file> <hook-type> [test-case]"
  echo "Hook types: UserPromptSubmit, PreToolUse, Stop"
  echo "Test cases: default, custom"
  echo ""
  echo "Examples:"
  echo "  $0 .claude/hooks/my-hook.ts UserPromptSubmit"
  echo "  $0 .claude/hooks/my-hook.ts PreToolUse custom"
  exit 1
fi

if [ ! -f "$HOOK_FILE" ]; then
  echo "Error: Hook file not found: $HOOK_FILE"
  exit 1
fi

echo "Testing hook: $HOOK_FILE"
echo "Type: $HOOK_TYPE"
echo "---"

# 테스트 입력 생성
generate_test_input() {
  case "$HOOK_TYPE" in
    UserPromptSubmit)
      if [ "$TEST_CASE" == "custom" ]; then
        read -p "Enter test prompt: " PROMPT
        echo "{\"session_id\":\"test-$(date +%s)\",\"prompt\":\"$PROMPT\"}"
      else
        echo "{\"session_id\":\"test-$(date +%s)\",\"prompt\":\"create a new skill for testing\"}"
      fi
      ;;

    PreToolUse)
      if [ "$TEST_CASE" == "custom" ]; then
        read -p "Enter tool name (Edit/Write/Bash): " TOOL_NAME
        read -p "Enter file path: " FILE_PATH
        echo "{\"session_id\":\"test-$(date +%s)\",\"tool_name\":\"$TOOL_NAME\",\"tool_input\":{\"file_path\":\"$FILE_PATH\"}}"
      else
        echo "{\"session_id\":\"test-$(date +%s)\",\"tool_name\":\"Edit\",\"tool_input\":{\"file_path\":\"test.ts\"}}"
      fi
      ;;

    Stop)
      if [ "$TEST_CASE" == "custom" ]; then
        echo "{\"session_id\":\"test-$(date +%s)\"}"
      else
        echo "{\"session_id\":\"test-$(date +%s)\"}"
      fi
      ;;

    *)
      echo "Error: Invalid hook type"
      exit 1
      ;;
  esac
}

# 테스트 실행
TEST_INPUT=$(generate_test_input)

echo "Test input:"
echo "$TEST_INPUT" | jq . 2>/dev/null || echo "$TEST_INPUT"
echo ""
echo "Running hook..."
echo "---"

# Hook 실행 및 결과 캡처
set +e
STDOUT=$(echo "$TEST_INPUT" | npx tsx "$HOOK_FILE" 2>/dev/null)
EXIT_CODE=$?
STDERR=$(echo "$TEST_INPUT" | npx tsx "$HOOK_FILE" 2>&1 >/dev/null)
set -e

# 결과 출력
echo "Exit code: $EXIT_CODE"
echo ""

if [ -n "$STDOUT" ]; then
  echo "Stdout (sent to Claude):"
  echo "$STDOUT"
  echo ""
fi

if [ -n "$STDERR" ]; then
  echo "Stderr (blocking message):"
  echo "$STDERR"
  echo ""
fi

# 종료 코드 해석
echo "Interpretation:"
case "$HOOK_TYPE" in
  UserPromptSubmit)
    case $EXIT_CODE in
      0)
        echo "✅ Hook executed successfully"
        if [ -n "$STDOUT" ]; then
          echo "   Message will be injected before Claude sees the prompt"
        else
          echo "   No message injected"
        fi
        ;;
      1)
        echo "⚠️  Hook sent stderr message to Claude"
        ;;
      *)
        echo "❌ Unexpected exit code: $EXIT_CODE"
        ;;
    esac
    ;;

  PreToolUse)
    case $EXIT_CODE in
      0)
        echo "✅ Tool execution allowed"
        ;;
      2)
        echo "🚫 Tool execution BLOCKED"
        if [ -n "$STDERR" ]; then
          echo "   Blocking message sent to Claude"
        fi
        ;;
      *)
        echo "❌ Unexpected exit code: $EXIT_CODE"
        ;;
    esac
    ;;

  Stop)
    case $EXIT_CODE in
      0)
        echo "✅ Hook executed successfully"
        if [ -n "$STDOUT" ]; then
          echo "   Reminder sent to Claude"
        else
          echo "   No reminder"
        fi
        ;;
      *)
        echo "❌ Unexpected exit code: $EXIT_CODE"
        ;;
    esac
    ;;
esac

echo ""
echo "Test completed!"
