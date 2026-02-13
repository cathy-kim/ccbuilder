# GitHub Repository References

> Claude Code 확장 기능 개발 시 참고할 GitHub 레포지토리 (Tier별 정리)

**Last Updated**: 2026-02-11

---

## Tier 구분

| Tier | 기준 | 신뢰도 |
|------|------|--------|
| **T1 - Official** | Anthropic 공식 | 100% |
| **T2 - Comprehensive** | 10k+ Stars, 생태계 핵심 | 90% (P1 검증 필요) |
| **T3 - Specialized** | 1k-10k Stars, 특화 도구 | 80% (P1 검증 필요) |
| **T4 - Emerging** | <1k Stars, 유용한 아이디어 | 아이디어 참고만 |

## 상세 문서

| 파일 | 내용 |
|------|------|
| [official-repos.md](official-repos.md) | T1 - Anthropic 공식 레포 |
| [ecosystem-collections.md](ecosystem-collections.md) | T2 - 종합 컬렉션 (10k+) |
| [specialized-tools.md](specialized-tools.md) | T3/T4 - 특화 도구 & 유즈 케이스 |
| [patterns.md](patterns.md) | 크로스 레포 패턴 & 학습 포인트 |

## Quick Reference - Top 10

| # | Repository | Stars | 로컬 경로 (`repos/`) | 핵심 가치 |
|---|-----------|-------|---------------------|-----------|
| 1 | [anthropics/skills](https://github.com/anthropics/skills) | ~67.9k | `anthropics-skills` | 공식 Skills (PDF, DOCX 등) |
| 2 | [anthropics/claude-code](https://github.com/anthropics/claude-code) | ~66.1k | - | 공식 CLI + Hook 예시 |
| 3 | [obra/superpowers](https://github.com/obra/superpowers) | ~49.6k | `obra-superpowers` | TDD/디버깅 워크플로우 |
| 4 | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) | ~44.0k | `everything-claude-code` | 올인원 설정 (15 agents, 30+ skills) |
| 5 | [wshobson/agents](https://github.com/wshobson/agents) | ~28.4k | `wshobson-agents` | 112 agents + 16 orchestrators |
| 6 | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ~23.4k | `awesome-claude-code` | 생태계 디렉토리 |
| 7 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | ~10.2k | `awesome-subagents` | 126+ 서브에이전트 |
| 8 | [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | ~6.9k | `awesome-claude-skills` | Skills 비교표 & 튜토리얼 |
| 9 | [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | ~6.7k | `awesome-agent-skills` | 339+ 멀티 에이전트 호환 Skills |
| 10 | [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | ~5.3k | `claude-code-showcase` | GitHub Actions + JIRA 워크플로우 |
| 11 | [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | ~4.4k | `claude-code-system-prompts` | 시스템 프롬프트 원문, Tool 스펙 |

---

## 로컬 Submodule 검색 가이드

모든 레포는 `repos/` 하위에 git submodule로 설치되어 있습니다.

### Skill 예시 찾기

```bash
# 공식 Skill 구조 참조
Grep "SKILL.md" in repos/anthropics-skills/

# 특정 도메인 Skill 찾기 (예: PDF)
Grep "pdf" in repos/anthropics-skills/ glob="**/SKILL.md"

# 커뮤니티 Skill 패턴 탐색
Grep "frontmatter" in repos/awesome-claude-skills/
```

### Subagent 정의 찾기

```bash
# 126+ 서브에이전트에서 검색
Grep "description:" in repos/awesome-subagents/ glob="**/*.md"

# 특정 역할 찾기 (예: security)
Grep -i "security" in repos/awesome-subagents/ glob="**/*.md"

# 대규모 에이전트 컬렉션
Grep "model:" in repos/wshobson-agents/ glob="**/agents/**"
```

### Hook 패턴 찾기

```bash
# 전체 Hook 이벤트 구현
Grep "PreToolUse\|PostToolUse\|SessionStart" in repos/hooks-mastery/

# 실전 Hook 설정
Grep "hooks" in repos/everything-claude-code/ glob="**/settings.json"
```

### 워크플로우 패턴 찾기

```bash
# TDD 워크플로우
Grep "TDD\|test-first" in repos/obra-superpowers/

# GitHub Actions 자동화
Grep "schedule\|cron" in repos/claude-code-showcase/ glob="**/*.yml"

# Orchestrator 패턴
Grep "orchestrat" in repos/wshobson-agents/
```

### Task(Explore)로 깊은 분석

Grep보다 깊은 분석이 필요할 때 Explore agent를 사용합니다:

```
Task(subagent_type: "Explore", prompt: "repos/obra-superpowers에서 TDD 워크플로우 구조를 분석해줘")
Task(subagent_type: "Explore", prompt: "repos/everything-claude-code의 agents/ 디렉토리에서 가장 잘 만들어진 agent 3개를 분석해줘")
Task(subagent_type: "Explore", prompt: "repos/anthropics-skills에서 PDF skill의 progressive disclosure 패턴을 분석해줘")
```

### claude-context MCP (시맨틱 검색)

자연어로 코드를 검색하려면 [claude-context MCP](https://github.com/zilliztech/claude-context) 설치:

**Option A: Gemini + Zilliz Free** (간단)
```bash
# Zilliz Cloud 무료 가입: https://cloud.zilliz.com/signup
claude mcp add claude-context \
  -e EMBEDDING_PROVIDER=Gemini \
  -e GEMINI_API_KEY=${GEMINI_API_KEY} \
  -e MILVUS_TOKEN=<your-zilliz-api-key> \
  -- npx @zilliz/claude-context-mcp@latest
```

**Option B: Ollama + 로컬 Milvus** (오프라인)
```bash
ollama pull nomic-embed-text
docker run -d --name milvus -p 19530:19530 milvusdb/milvus:latest
claude mcp add claude-context \
  -e EMBEDDING_PROVIDER=Ollama \
  -e OLLAMA_HOST=http://127.0.0.1:11434 \
  -e EMBEDDING_MODEL=nomic-embed-text \
  -e MILVUS_ADDRESS=http://localhost:19530 \
  -- npx @zilliz/claude-context-mcp@latest
```

설치 후: `"repos/ 디렉토리를 인덱싱해줘"` → 자연어 검색 가능

### 업데이트

```bash
# 전체 submodule 최신화
git submodule update --remote --depth 1
```
