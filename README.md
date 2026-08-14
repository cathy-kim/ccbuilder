<div align="center">

# ccbuilder

**Build Claude Code extensions in seconds, not hours.**

Skills, Hooks, Agents, Agent Teams, Ralph Loops, MCP, Memory — one plugin, all covered.

![Version](https://img.shields.io/badge/version-2.12.0-blue)
![Claude Code](https://img.shields.io/badge/Claude_Code-v2.1.232+-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)
![Docs](https://img.shields.io/badge/reference_docs-28-orange)
![Extensions](https://img.shields.io/badge/extension_types-7-brightgreen)

<!-- TODO: Replace with actual demo GIF
<img src="docs/demo.gif" alt="ccbuilder demo" width="700">
-->

</div>

---

## Why ccbuilder?

Building Claude Code extensions today means:

- Scattered docs across 20+ pages — no single source of truth
- Copy-pasting boilerplate and guessing at correct file structures
- No validation until you actually try running it
- Zero reference to what the community has already built

**ccbuilder** gives you one command to scaffold any Claude Code extension — backed by 28 reference docs (17 guides + 6 official + 5 ecosystem), and the entire ecosystem knowledge base from 11 curated community repos.

## Quick Start

### Install

```bash
claude plugin install github:cathy-kim/ccbuilder
```

### Use

Invoke via slash command:

```bash
/ccbuilder skill my-skill              # Scaffold a new skill
/ccbuilder hook PreToolUse             # Scaffold a new hook
/ccbuilder agent my-agent              # Scaffold a new agent
/ccbuilder team my-team                # Set up an agent team
/ccbuilder ralph my-project            # Set up a Ralph Loop (autonomous dev loop)
/ccbuilder question "How do hooks work?"
```

Or just ask naturally — ccbuilder activates automatically when you mention skills, hooks, agents, agent teams, ralph loops, MCP, or memory system topics.

## Features

**One-Command Scaffolding** — Generate complete, validated extension structures with a single slash command. YAML frontmatter, directory layout, reference templates — all handled.

**28 Built-in Reference Docs** — Every Claude Code extension type documented with examples, patterns, and best practices. No more tab-switching between docs.

**7 Extension Types Supported** — Skills, Hooks, Agents, Agent Teams, Ralph Loops, Memory, and Rules. All supported out of the box with type-specific scaffolding.

**Ecosystem Knowledge Base** — Curated analysis of 11 top community repos (339+ skills, 126+ subagents, 112 agents) with cross-referenced patterns.

**Auto-Detection** — Mention skills, hooks, or agents in conversation and ccbuilder activates automatically. No slash command needed.

**Official Docs Built-in** — Summaries of all 6 Claude Code official documentation pages, so Claude has the latest API surface without you copy-pasting docs.

## Supported Extension Types

| Type | Purpose | Location |
|------|---------|----------|
| **Skill** | Knowledge injection + slash commands | `.claude/skills/` |
| **Subagent** | Independent agent definitions | `.claude/agents/` |
| **Agent Team** | Multi-agent team collaboration | `~/.claude/teams/` |
| **Hook** | Workflow control (16 lifecycle events) | `settings.json` |
| **Memory** | Cross-session knowledge persistence | `~/.claude/projects/*/memory/` |
| **Rules** | Path-scoped modular rules | `.claude/rules/` |
| **Ralph Loop** | Autonomous development loop (fresh context) | `TASK.md` + `loop.sh` |

## Documentation

<details>
<summary><strong>Reference Guides (17 files)</strong></summary>

| Guide | Description |
|-------|-------------|
| [skills-guide.md](skills/ccbuilder/references/skills-guide.md) | Skills development guide |
| [hooks-guide.md](skills/ccbuilder/references/hooks-guide.md) | Hooks implementation guide (16 events) |
| [subagents-guide.md](skills/ccbuilder/references/subagents-guide.md) | Subagents + Plugin guide |
| [agent-teams-guide.md](skills/ccbuilder/references/agent-teams-guide.md) | Agent Teams collaboration guide |
| [ralph-loop-guide.md](skills/ccbuilder/references/ralph-loop-guide.md) | Ralph Loop (autonomous dev loop) guide |
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
| [what-goes-where-guide.md](skills/ccbuilder/references/what-goes-where-guide.md) | What-goes-where decision guide |

</details>

<details>
<summary><strong>Official Documentation Summaries (6 files)</strong></summary>

Built-in summaries of Claude Code official docs — so Claude always has the latest API surface:

| Doc | Description |
|-----|-------------|
| [official/skills.md](skills/ccbuilder/references/official/skills.md) | Skills official docs |
| [official/hooks.md](skills/ccbuilder/references/official/hooks.md) | Hooks official docs (16 events) |
| [official/subagents.md](skills/ccbuilder/references/official/subagents.md) | Sub-agents official docs |
| [official/mcp.md](skills/ccbuilder/references/official/mcp.md) | MCP official docs |
| [official/memory-rules.md](skills/ccbuilder/references/official/memory-rules.md) | Memory & Rules official docs |
| [official/tools.md](skills/ccbuilder/references/official/tools.md) | Built-in Tools reference (28+ tools) |

</details>

<details>
<summary><strong>GitHub Ecosystem References (5 docs + 11 submodules)</strong></summary>

Curated, tier-ranked analysis of the Claude Code ecosystem:

| Doc | Description |
|-----|-------------|
| [github/README.md](skills/ccbuilder/references/github/README.md) | Tier-based repo index |
| [github/official-repos.md](skills/ccbuilder/references/github/official-repos.md) | Anthropic official repos (T1) |
| [github/ecosystem-collections.md](skills/ccbuilder/references/github/ecosystem-collections.md) | Ecosystem collections 10k+ stars (T2) |
| [github/specialized-tools.md](skills/ccbuilder/references/github/specialized-tools.md) | Specialized tools & use cases (T3/T4) |
| [github/patterns.md](skills/ccbuilder/references/github/patterns.md) | Cross-repo verified patterns |

#### Included Submodules (11 repos)

For code-level reference, 11 community repos are bundled as git submodules:

| Repo | Highlights |
|------|------------|
| [anthropics/skills](https://github.com/anthropics/skills) | Official skill implementations (DOCX, PDF, etc.) |
| [obra/superpowers](https://github.com/obra/superpowers) | TDD, debugging, subagent workflows |
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 15 agents, 30+ skills, hooks |
| [wshobson/agents](https://github.com/wshobson/agents) | 112 agents, 16 orchestrators |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Ecosystem directory |
| [awesome-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 126+ sub-agents |
| [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Skills comparison & tutorials |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 339+ multi-agent compatible skills |
| [hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | 13 hook events implementation |
| [claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | GitHub Actions, JIRA workflows |
| [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | System prompts, tool specs |

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/cathy-kim/ccbuilder.git

# Or add submodules to an existing clone
git submodule update --init --depth 1
```

</details>

<details>
<summary><strong>Scripts</strong></summary>

| Script | Description |
|--------|-------------|
| `scripts/init-skill.sh` | Initialize a new skill scaffold |
| `scripts/init-agent.sh` | Initialize a new agent scaffold |
| `scripts/init-hook.sh` | Initialize a new hook scaffold |
| `scripts/init-ralph.sh` | Initialize a Ralph Loop (simple/hook/full) |
| `scripts/test-hook.sh` | Test hook execution |
| `scripts/check-updates.sh` | Check for Claude Code official doc updates |

</details>

<details>
<summary><strong>Evaluations</strong></summary>

The `evaluations/` directory contains a skill evaluation framework:

- `evaluation-framework.md` — Evaluation methodology
- `test-cases.json` — 5 test scenarios (P0/P1 prioritized)
- `run_evaluation.py` — Automated evaluation runner
- `golden-outputs/` — Expected output references

</details>

## Contributing

Contributions welcome! Here's how you can help:

- **Add reference guides** — Found a useful Claude Code pattern? Submit a PR to `skills/ccbuilder/references/`
- **Improve scaffolding** — Better templates, more extension types
- **Report issues** — Bug reports and feature requests via [GitHub Issues](https://github.com/cathy-kim/ccbuilder/issues)

## Version

Current: **v2.55.0** (2026-08-14) — Claude Code v2.1.181+ compatible. See [CHANGELOG.md](CHANGELOG.md) for full history.

## License

[MIT](LICENSE)
