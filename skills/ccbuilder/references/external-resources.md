# External Resources

> Claude Code 확장 기능 개발 시 참고할 수 있는 외부 리소스 (신뢰도 등급별 정리)

**Last Updated**: 2026-02-11

---

## P1 - Official Sources (Must Reference)

| Source | URL |
|--------|-----|
| Claude Code GitHub | https://github.com/anthropics/claude-code |
| Official Docs - Skills | https://code.claude.com/docs/en/skills |
| Official Docs - Hooks | https://code.claude.com/docs/en/hooks |
| Official Docs - Subagents | https://code.claude.com/docs/en/sub-agents |
| Official Docs - Commands | https://code.claude.com/docs/en/slash-commands |
| Official Docs - Settings | https://code.claude.com/docs/en/settings |
| Agent Skills API | https://platform.claude.com/docs/en/agents-and-tools/agent-skills |

## P2 - Authoritative Sources (90% Trust)

| Source | URL |
|--------|-----|
| Anthropic Engineering Blog | https://www.anthropic.com/engineering |
| Claude Cookbooks | https://github.com/anthropics/claude-cookbooks |
| Claude Code Action | https://github.com/anthropics/claude-code-action |
| Official Plugins Collection | https://github.com/anthropics/claude-code/tree/main/plugins |

## P3 - Expert Sources (Verify Against P1)

| Source | URL |
|--------|-----|
| GitHub Issues (Claude Code) | https://github.com/anthropics/claude-code/issues |
| Stack Overflow (claude-code) | https://stackoverflow.com/questions/tagged/claude-code |

---

## Community GitHub Repositories (Verified 2026-02-04)

### Official & Comprehensive Collections

| Repository | Description | Stars |
|------------|-------------|-------|
| [anthropics/skills](https://github.com/anthropics/skills) | **Official Anthropic** - Production skills for docx, pdf, pptx, xlsx | 62.3k |
| [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | **Anthropic Hackathon Winner** - Battle-tested configs from 10+ months | 39.1k |
| [wshobson/agents](https://github.com/wshobson/agents) | 108 agents + 129 skills + 15 orchestrators - Complete automation | 27.7k |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Curated list of skills, hooks, commands, orchestrators | 22.7k |

### Specialized Resources

| Repository | Description | Stars |
|------------|-------------|-------|
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 100+ specialized subagents for full-stack development | 9.5k |
| [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) | Auto-activating skills via hooks | 8.8k |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Official & community skills collection with tutorials | 6.5k |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 200+ skills compatible with Codex, Gemini CLI, Cursor | 6.0k |
| [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | GitHub Actions workflows + scheduled maintenance | 5.2k |
| [disler/claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | All 13 hook events + security filtering + TTS integration | 2.3k |

---

## Community Resources

### 포럼 및 커뮤니티

- **Anthropic Discord**: https://discord.gg/anthropic
- **GitHub Discussions**: https://github.com/anthropics/claude-code/discussions

### 블로그 및 튜토리얼

- **Anthropic Blog**: https://www.anthropic.com/blog
- **Claude Code 시작하기**: https://docs.anthropic.com/claude-code/quickstart

---

## Git Submodule로 추가하기 (선택)

로컬에서 참조할 경우 submodule로 추가할 수 있습니다:

```bash
cd <your-project-root>
mkdir -p .claude/skills/ccbuilder/references/community-repos

# Official & Comprehensive
git submodule add https://github.com/anthropics/skills .claude/skills/ccbuilder/references/community-repos/anthropics-skills
git submodule add https://github.com/affaan-m/everything-claude-code .claude/skills/ccbuilder/references/community-repos/everything-claude-code
git submodule add https://github.com/wshobson/agents .claude/skills/ccbuilder/references/community-repos/wshobson-agents
git submodule add https://github.com/hesreallyhim/awesome-claude-code .claude/skills/ccbuilder/references/community-repos/awesome-claude-code

# Specialized
git submodule add https://github.com/VoltAgent/awesome-claude-code-subagents .claude/skills/ccbuilder/references/community-repos/awesome-subagents
git submodule add https://github.com/diet103/claude-code-infrastructure-showcase .claude/skills/ccbuilder/references/community-repos/infrastructure-showcase
git submodule add https://github.com/travisvn/awesome-claude-skills .claude/skills/ccbuilder/references/community-repos/awesome-skills
git submodule add https://github.com/VoltAgent/awesome-agent-skills .claude/skills/ccbuilder/references/community-repos/awesome-agent-skills
git submodule add https://github.com/ChrisWiles/claude-code-showcase .claude/skills/ccbuilder/references/community-repos/claude-code-showcase
git submodule add https://github.com/disler/claude-code-hooks-mastery .claude/skills/ccbuilder/references/community-repos/hooks-mastery
```

---

## Reference Priority

```
When implementing an extension:
1. ALWAYS check P1 sources first (Official docs = correct behavior)
2. Use P2 sources for patterns and examples
3. P3 sources for troubleshooting (GitHub issues = known problems)
4. Community repos for ideas only (verify against P1/P2)
```
