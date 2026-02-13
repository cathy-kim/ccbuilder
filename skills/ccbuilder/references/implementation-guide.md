# Claude Code Extension Implementation Guide

> **Source Credibility**: P1/P2 sources combined
> **Purpose**: Step-by-step implementation patterns based on official documentation

**Version**: 2.7.0
**Last Updated**: 2026-02-11
**Claude Code Version**: v2.1.39+

---

## Quick Decision Tree

```
What do you want to build?
│
├─ "Add domain knowledge" → Skill
│   └─ Auto-triggers based on context
│
├─ "Coordinate multiple agents" → Agent Team (v2.7 신규)
│   └─ TeamCreate + TaskCreate + SendMessage
│
├─ "Run autonomous task" → Agent
│   └─ Spawned via Task tool
│
├─ "React to events" → Hook
│   └─ PreToolUse, Stop, TeammateIdle, etc.
│
├─ "Persist knowledge across sessions" → Memory (v2.7 신규)
│   └─ ~/.claude/projects/<project>/memory/
│
├─ "Reusable prompt" → Command (Skills 권장)
│   └─ Invoked with /prefix:name
│
└─ "Package for distribution" → Plugin
    └─ Contains any/all of above
```

---

## Implementation Patterns

### Pattern 1: Create a Domain Skill

**Use Case**: Provide guidance for specific tech stack or workflow

```bash
# 1. Create skill directory
mkdir -p .claude/skills/nextjs-patterns

# 2. Create SKILL.md
cat > .claude/skills/nextjs-patterns/SKILL.md << 'EOF'
---
name: nextjs-patterns
description: Next.js App Router patterns and best practices. Use when creating pages, API routes, server components, or working with Next.js 14+ features.
---

# Next.js Patterns

## Server Components (Default)

\`\`\`typescript
// app/users/page.tsx
export default async function UsersPage() {
  const users = await db.users.findMany();
  return <UserList users={users} />;
}
\`\`\`

## Client Components

\`\`\`typescript
'use client';
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
\`\`\`

## API Routes

\`\`\`typescript
// app/api/users/route.ts
export async function GET(request: NextRequest) {
  const users = await db.users.findMany();
  return NextResponse.json(users);
}
\`\`\`

## See Also
- [Server Components Guide](references/server-components.md)
- [Data Fetching Patterns](references/data-fetching.md)
EOF

# 3. Test by mentioning keywords
# "Create a new Next.js page for user profiles"
```

### Pattern 2: Create a Review Agent

**Use Case**: Autonomous code review with specific focus

```bash
# 1. Create agent file
cat > .claude/agents/security-reviewer.md << 'EOF'
---
name: security-reviewer
description: Reviews code for security vulnerabilities
model: opus
tools: Read, Grep, Glob
---

# Security Reviewer Agent

## Purpose
Identify security vulnerabilities in code.

## Checklist
- [ ] SQL Injection
- [ ] XSS (Cross-Site Scripting)
- [ ] Command Injection
- [ ] Insecure Dependencies
- [ ] Hardcoded Secrets
- [ ] Authentication Flaws

## Instructions
1. Find relevant files: `Glob("**/*.{ts,js,py}")`
2. Search for patterns:
   - `Grep("eval\(|exec\(|os\.system")`
   - `Grep("innerHTML|dangerouslySetInnerHTML")`
   - `Grep("password|secret|api_key")`
3. Analyze findings
4. Generate report

## Output Format
### Security Review Report

#### Critical Issues
- [file:line] Description

#### Warnings
- [file:line] Description

#### Recommendations
- Suggestion 1
- Suggestion 2
EOF

# 2. Invoke via Task tool
# "Use Task tool with subagent_type='security-reviewer'"
```

### Pattern 3: Create a Blocking Hook

**Use Case**: Prevent modifications to sensitive files

```bash
# 1. Create hook directory
mkdir -p .claude/hooks

# 2. Create TypeScript hook
cat > .claude/hooks/protect-sensitive.ts << 'EOF'
#!/usr/bin/env npx tsx

interface HookInput {
  session_id: string;
  tool_name: string;
  tool_input: {
    file_path?: string;
    command?: string;
  };
}

const PROTECTED_PATTERNS = [
  '.env',
  'package-lock.json',
  '.git/',
  'credentials',
  'secrets'
];

async function main() {
  const input: HookInput = JSON.parse(await readStdin());

  const content = JSON.stringify(input.tool_input);

  for (const pattern of PROTECTED_PATTERNS) {
    if (content.includes(pattern)) {
      console.error(`BLOCKED: Cannot modify protected file: ${pattern}`);
      process.exit(2);
    }
  }

  process.exit(0);
}

function readStdin(): Promise<string> {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
EOF

# 3. Make executable
chmod +x .claude/hooks/protect-sensitive.ts

# 4. Register in settings.json
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "npx tsx .claude/hooks/protect-sensitive.ts"
          }
        ]
      }
    ]
  }
}
EOF

# 5. Test
echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | \
  npx tsx .claude/hooks/protect-sensitive.ts
```

### Pattern 4: Create a Workflow Command

**Use Case**: Multi-step guided workflow

```bash
# 1. Create command file
cat > .claude/commands/feature.md << 'EOF'
Guide me through implementing a new feature with proper planning.

## Phase 1: Research
1. Understand the requirement: $ARGUMENTS
2. Search for similar implementations in codebase
3. Identify affected files

## Phase 2: Plan
1. List files to create/modify
2. Define interfaces/types first
3. Plan test cases

## Phase 3: Implement
1. Create types/interfaces
2. Implement core logic
3. Add error handling
4. Write tests

## Phase 4: Review
1. Self-review changes
2. Run tests
3. Check for edge cases

## Requirements
$ARGUMENTS
EOF

# 2. Use the command
# /project:feature "Add user authentication with JWT"
```

### Pattern 5: Create an Agent Team (v2.7 신규)

**Use Case**: 여러 에이전트가 병렬로 협업하여 기능 개발

```typescript
// 1. 팀 생성
TeamCreate({ team_name: "feature-team", description: "User auth 개발" })

// 2. 작업 생성
TaskCreate({ subject: "Build REST API", description: "인증 API 구현", activeForm: "Building REST API" })
TaskCreate({ subject: "Build Login UI", description: "로그인 화면 구현", activeForm: "Building Login UI" })
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })  // UI는 API 완료 후

// 3. Teammate 생성 및 할당
Task({
  subagent_type: "backend",
  team_name: "feature-team",
  name: "api-dev",
  prompt: "인증 REST API를 구현하세요",
  mode: "bypassPermissions"
})
TaskUpdate({ taskId: "1", owner: "api-dev" })

// 4. 커뮤니케이션
SendMessage({
  type: "message",
  recipient: "api-dev",
  content: "JWT 방식으로 구현해주세요",
  summary: "JWT 인증 방식 요청"
})

// 5. 완료 후 정리
SendMessage({ type: "shutdown_request", recipient: "api-dev", content: "작업 완료" })
TeamDelete()
```

**활성화 필수**: `settings.json` → `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"`

### Pattern 6: Setup Memory System (v2.7 신규)

**Use Case**: 세션 간 학습 내용 영속 저장

```bash
# Memory 디렉토리 구조
~/.claude/projects/<project>/memory/
├── MEMORY.md        # 매 세션 자동 로드 (200줄 제한)
├── debugging.md     # 디버깅 패턴
└── patterns.md      # 코딩 패턴
```

MEMORY.md에 저장할 내용:
- 확인된 아키텍처 패턴과 컨벤션
- 주요 파일 경로와 프로젝트 구조
- 사용자의 워크플로우/도구 선호도
- 반복 문제의 해결책

저장하지 않을 내용:
- 세션별 임시 상태
- CLAUDE.md와 중복되는 내용
- 미검증된 추측
```

---

## Combining Extensions

### Complete Dev Workflow Plugin

```
my-dev-workflow/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── feature.md        # /my-dev-workflow:feature
│   ├── review.md         # /my-dev-workflow:review
│   └── deploy.md         # /my-dev-workflow:deploy
├── agents/
│   ├── code-reviewer.md  # Review specialist
│   └── test-writer.md    # Test generation
├── skills/
│   └── project-conventions/
│       └── SKILL.md      # Auto-applied guidance
├── hooks/
│   └── pre-commit.ts     # Validation before commits
└── README.md
```

### plugin.json

```json
{
  "name": "my-dev-workflow",
  "version": "1.0.0",
  "description": "Complete development workflow",
  "commands": [
    "commands/feature.md",
    "commands/review.md",
    "commands/deploy.md"
  ],
  "agents": [
    "agents/code-reviewer.md",
    "agents/test-writer.md"
  ],
  "skills": [
    "skills/project-conventions"
  ],
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "npx tsx ${CLAUDE_PLUGIN_ROOT}/hooks/pre-commit.ts"
          }
        ]
      }
    ]
  }
}
```

---

## Testing Extensions

### Test a Hook

```bash
# Simulate PreToolUse input
echo '{
  "session_id": "test-123",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm install",
    "description": "Install dependencies"
  }
}' | npx tsx .claude/hooks/my-hook.ts

# Check exit code
echo "Exit code: $?"
```

### Test a Skill

1. Start Claude Code
2. Ask something that should trigger the skill
3. Verify skill guidance appears in response

### Test an Agent

```bash
# In Claude Code:
# "Use Task tool with subagent_type='my-agent' to review authentication"
```

### Test a Command

```bash
# In Claude Code:
/project:my-command test argument
```

### Test an Agent Team

```typescript
// 1. 환경 변수 확인
// settings.json: env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"

// 2. 소규모 팀으로 테스트
TeamCreate({ team_name: "test-team" })
TaskCreate({ subject: "Test task", description: "간단한 테스트", activeForm: "Testing" })
Task({ subagent_type: "Explore", team_name: "test-team", name: "tester", prompt: "프로젝트 구조 분석" })

// 3. 정리
SendMessage({ type: "shutdown_request", recipient: "tester", content: "테스트 완료" })
TeamDelete()
```

---

## Troubleshooting

### Extension Not Working

| Issue | Check |
|-------|-------|
| Skill not triggering | Description keywords match? |
| Hook not running | settings.json path correct? Execute permission? |
| Agent not found | File in `.claude/agents/`? |
| Command not found | File in `.claude/commands/`? |

### Debug Mode

```bash
# Run Claude Code with debug
claude --debug

# Check logs for extension loading
```

---

## Source References

| Topic | P1 Official Source |
|-------|-------------------|
| Hooks | [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) |
| Skills | [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) |
| Agents | [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) |
| Commands | [code.claude.com/docs/en/slash-commands](https://code.claude.com/docs/en/slash-commands) |
| Plugins | [github.com/anthropics/claude-code/plugins](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) |
| Agent Teams | [code.claude.com/docs/en/agent-teams](https://code.claude.com/docs/en/agent-teams) |
| Memory | [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) |
