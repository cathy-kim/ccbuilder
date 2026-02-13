# Claude Code Extension Builder

A comprehensive Claude Code plugin for building and deploying Claude Code extensions — skills, hooks, agents, agent teams, and more.

## Quick Start

### Install as Claude Code Plugin

```bash
claude plugin install github:cathy-kim/ccbuilder
```

### Usage

Once installed, invoke the skill via slash command:

```
/build-extension skill my-skill
/build-extension hook PreToolUse
/build-extension agent my-agent
/build-extension team my-team
/build-extension question "How do hooks work?"
```

Or just ask a question — the skill activates automatically when you mention skills, hooks, agents, agent teams, MCP, or memory system topics.

## What's Included

### Extension Types

| Type | Purpose | Location |
|------|---------|----------|
| **Skill** | Knowledge injection + slash commands | `.claude/skills/` |
| **Subagent** | Independent agent definitions | `.claude/agents/` |
| **Agent Team** | Multi-agent team collaboration | `~/.claude/teams/` |
| **Hook** | Workflow control (14 events) | `settings.json` |
| **Memory** | Cross-session knowledge persistence | `~/.claude/projects/*/memory/` |
| **Rules** | Path-scoped modular rules | `.claude/rules/` |

### Reference Guides (21 files)

| Guide | Description |
|-------|-------------|
| [skills-guide.md](skills/ccbuilder/references/skills-guide.md) | Skills development guide |
| [hooks-guide.md](skills/ccbuilder/references/hooks-guide.md) | Hooks implementation guide |
| [subagents-guide.md](skills/ccbuilder/references/subagents-guide.md) | Subagents + Plugin guide |
| [agent-teams-guide.md](skills/ccbuilder/references/agent-teams-guide.md) | Agent Teams collaboration guide |
| [mcp-guide.md](skills/ccbuilder/references/mcp-guide.md) | MCP setup and usage guide |
| [memory-rules-guide.md](skills/ccbuilder/references/memory-rules-guide.md) | Memory & Rules system guide |
| [implementation-guide.md](skills/ccbuilder/references/implementation-guide.md) | Step-by-step implementation |
| [review-system.md](skills/ccbuilder/references/review-system.md) | Skill review/validation system |
| [best-practices.md](skills/ccbuilder/references/best-practices.md) | Best practices collection |
| [skill-subagent-task-guide.md](skills/ccbuilder/references/skill-subagent-task-guide.md) | Skill/Subagent/Task comparison |
| [troubleshooting.md](skills/ccbuilder/references/troubleshooting.md) | Troubleshooting guide |
| [orchestrator-principles.md](skills/ccbuilder/references/orchestrator-principles.md) | Orchestrator core principles |
| [orchestrator-skill-creation-guide.md](skills/ccbuilder/references/orchestrator-skill-creation-guide.md) | Orchestrator creation guide |
| [external-resources.md](skills/ccbuilder/references/external-resources.md) | Community resources & links |
| [version-sync.md](skills/ccbuilder/references/version-sync.md) | Version sync checklist |

### Official Documentation Summaries (6 files)

| Doc | Description |
|-----|-------------|
| [official/skills.md](skills/ccbuilder/references/official/skills.md) | Skills official docs summary |
| [official/hooks.md](skills/ccbuilder/references/official/hooks.md) | Hooks official docs (14 events) |
| [official/subagents.md](skills/ccbuilder/references/official/subagents.md) | Sub-agents official docs |
| [official/mcp.md](skills/ccbuilder/references/official/mcp.md) | MCP official docs |
| [official/memory-rules.md](skills/ccbuilder/references/official/memory-rules.md) | Memory & Rules official docs |
| [official/tools.md](skills/ccbuilder/references/official/tools.md) | Built-in Tools reference (28+ tools) |

### GitHub Repository References (5 docs + 11 submodules)

Curated analysis of the Claude Code ecosystem:

| Doc | Description |
|-----|-------------|
| [github/README.md](skills/ccbuilder/references/github/README.md) | Tier-based repo index |
| [github/official-repos.md](skills/ccbuilder/references/github/official-repos.md) | Anthropic official repos (T1) |
| [github/ecosystem-collections.md](skills/ccbuilder/references/github/ecosystem-collections.md) | Ecosystem collections 10k+ stars (T2) |
| [github/specialized-tools.md](skills/ccbuilder/references/github/specialized-tools.md) | Specialized tools & use cases (T3/T4) |
| [github/patterns.md](skills/ccbuilder/references/github/patterns.md) | Cross-repo verified patterns |

#### Local Submodule Repos (optional)

For code-level reference, 11 community repos are available as git submodules:

| Repo | What to Search |
|------|----------------|
| [anthropics/skills](https://github.com/anthropics/skills) | Official skill implementations (DOCX, PDF, etc.) |
| [obra/superpowers](https://github.com/nichochar/superpowers) | TDD, debugging, subagent workflows |
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 15 agents, 30+ skills, hooks |
| [wshobson/agents](https://github.com/wshobson/agents) | 112 agents, 16 orchestrators |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Ecosystem directory |
| [awesome-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 126+ sub-agents |
| [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Skills comparison & tutorials |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 339+ multi-agent compatible skills |
| [hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | 13 hook events implementation |
| [claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | GitHub Actions, JIRA workflows |
| [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | System prompts, tool specs |

To clone with submodules:

```bash
git clone --recurse-submodules https://github.com/cathy-kim/ccbuilder.git
```

Or add submodules to an existing clone:

```bash
git submodule update --init --depth 1
```

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/check-updates.sh` | Check for Claude Code official doc updates |
| `scripts/init-skill.sh` | Initialize a new skill scaffold |
| `scripts/init-hook.sh` | Initialize a new hook scaffold |
| `scripts/init-agent.sh` | Initialize a new agent scaffold |
| `scripts/test-hook.sh` | Test hook execution |

## Evaluations

The `evaluations/` directory contains the skill evaluation framework:

- `evaluation-framework.md` — Evaluation methodology
- `test-cases.json` — Test scenarios
- `run_evaluation.py` — Automated evaluation runner
- `golden-outputs/` — Expected output references

## Version History

See [CHANGELOG.md](CHANGELOG.md) for the full version history.

Current version: **v2.9.0** (2026-02-11)

## License

[MIT](LICENSE)
