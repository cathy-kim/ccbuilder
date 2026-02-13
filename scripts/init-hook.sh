#!/bin/bash

# Claude Code Hook 초기화 스크립트
# Usage: ./init-hook.sh <hook-name> <hook-type>
# Hook types: UserPromptSubmit, PreToolUse, Stop

set -e

HOOK_NAME="$1"
HOOK_TYPE="$2"

if [ -z "$HOOK_NAME" ] || [ -z "$HOOK_TYPE" ]; then
  echo "Usage: $0 <hook-name> <hook-type>"
  echo "Hook types: UserPromptSubmit, PreToolUse, Stop"
  echo "Example: $0 my-hook UserPromptSubmit"
  exit 1
fi

# Hook 타입 검증
if [[ ! "$HOOK_TYPE" =~ ^(UserPromptSubmit|PreToolUse|Stop)$ ]]; then
  echo "Error: Invalid hook type. Must be: UserPromptSubmit, PreToolUse, or Stop"
  exit 1
fi

# Hook 파일 생성
HOOK_FILE=".claude/hooks/$HOOK_NAME.ts"

if [ -f "$HOOK_FILE" ]; then
  echo "Error: Hook file already exists: $HOOK_FILE"
  exit 1
fi

# .claude/hooks 디렉토리 생성
mkdir -p ".claude/hooks"

echo "Creating $HOOK_TYPE hook: $HOOK_NAME"
echo "File: $HOOK_FILE"

# Hook 타입별 템플릿 생성
case "$HOOK_TYPE" in
  UserPromptSubmit)
    cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env npx tsx

/**
 * UserPromptSubmit Hook
 *
 * Triggered: Before Claude sees the user prompt
 * Purpose: Suggest relevant skills or inject context
 * Exit codes:
 *   0 - Continue normally
 *   1 - Show stderr message to Claude, then continue
 */

interface HookInput {
  session_id: string;
  prompt: string;
}

async function main() {
  const input: HookInput = JSON.parse(await readStdin());

  // TODO: Implement your logic here
  const shouldTrigger = checkConditions(input);

  if (shouldTrigger) {
    // Send message to Claude via stdout
    console.log(`📌 Reminder: [TODO: Your message here]`);
  }

  process.exit(0);
}

function checkConditions(input: HookInput): boolean {
  // TODO: Implement your trigger conditions
  const { prompt } = input;

  // Example: Check for keywords
  const keywords = ['example', 'test'];
  return keywords.some(keyword => prompt.toLowerCase().includes(keyword));
}

function readStdin(): Promise<string> {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });
}

main().catch(err => {
  console.error('Hook error:', err);
  process.exit(0); // Don't block workflow on errors
});
EOF
    ;;

  PreToolUse)
    cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env npx tsx

/**
 * PreToolUse Hook
 *
 * Triggered: Before tool execution
 * Purpose: Validate, block, or suggest before tool use
 * Exit codes:
 *   0 - Allow tool execution
 *   2 - Block tool execution and show stderr message
 */

interface HookInput {
  session_id: string;
  tool_name: string;
  tool_input: any;
}

async function main() {
  const input: HookInput = JSON.parse(await readStdin());

  // Only intercept Edit/Write tools for file modifications
  if (!['Edit', 'Write'].includes(input.tool_name)) {
    process.exit(0);
  }

  // TODO: Implement your validation logic
  const shouldBlock = checkValidation(input);

  if (shouldBlock) {
    // Block and send error message via stderr
    console.error(`❌ Blocked: [TODO: Your blocking message here]`);
    process.exit(2);
  }

  process.exit(0);
}

function checkValidation(input: HookInput): boolean {
  // TODO: Implement your validation logic
  const { tool_input } = input;
  const filePath = tool_input.file_path;

  // Example: Block editing certain files
  const blockedPatterns = ['.env', 'credentials'];
  return blockedPatterns.some(pattern => filePath?.includes(pattern));
}

function readStdin(): Promise<string> {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });
}

main().catch(err => {
  console.error('Hook error:', err);
  process.exit(0); // Don't block on errors
});
EOF
    ;;

  Stop)
    cat > "$HOOK_FILE" << 'EOF'
#!/usr/bin/env npx tsx

/**
 * Stop Hook
 *
 * Triggered: After Claude completes response
 * Purpose: Provide gentle reminders or post-response analysis
 * Exit codes:
 *   0 - Normal completion
 */

interface HookInput {
  session_id: string;
  // Additional context may be available
}

async function main() {
  const input: HookInput = JSON.parse(await readStdin());

  // TODO: Implement your post-response logic
  const shouldRemind = checkConditions(input);

  if (shouldRemind) {
    // Send gentle reminder via stdout
    console.log(`💡 Reminder: [TODO: Your reminder message here]`);
  }

  process.exit(0);
}

function checkConditions(input: HookInput): boolean {
  // TODO: Implement your reminder conditions

  // Example: Random reminder (10% chance)
  return Math.random() < 0.1;
}

function readStdin(): Promise<string> {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });
}

main().catch(err => {
  console.error('Hook error:', err);
  process.exit(0);
});
EOF
    ;;
esac

# 실행 권한 부여
chmod +x "$HOOK_FILE"

# settings.json 업데이트 안내
echo ""
echo "✅ Hook created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $HOOK_FILE"
echo "2. Complete all [TODO] sections"
echo "3. Test with: cat test-input.json | npx tsx $HOOK_FILE"
echo "4. Register in .claude/settings.json:"
echo ""
echo "   {"
echo "     \"hooks\": {"
echo "       \"$HOOK_TYPE\": \"$HOOK_FILE\""
echo "     }"
echo "   }"
