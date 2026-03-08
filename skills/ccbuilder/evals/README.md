# ccbuilder Evals

공식 [anthropics/skills skill-creator eval 패턴](https://github.com/anthropics/skills)을 따르는 ccbuilder 평가 시스템입니다.

## 구조

```
skills/ccbuilder/
├── evals/
│   ├── evals.json             # 공식 형식 테스트 케이스 (5개)
│   └── README.md              # 이 파일
├── agents/
│   └── grader.md              # grader 에이전트 지시문
└── scripts/
    ├── quick_validate.py      # SKILL.md frontmatter 검증기
    └── aggregate_benchmark.py # 벤치마크 집계 스크립트
```

## evals.json 형식

```json
{
  "skill_name": "ccbuilder",
  "evals": [
    {
      "id": 1,
      "prompt": "사용자 태스크 프롬프트",
      "expected_output": "기대 결과 설명",
      "files": [],
      "expectations": [
        "출력에 SKILL.md 파일이 포함된다",
        "SKILL.md에 name 필드가 있는 YAML frontmatter가 존재한다"
      ]
    }
  ]
}
```

- `id`: 정수형 테스트 케이스 번호
- `prompt`: ccbuilder 스킬에 전달할 실제 사용자 프롬프트
- `expected_output`: 사람이 읽을 수 있는 기대 결과 설명
- `files`: 사전에 워크스페이스에 배치할 파일 목록 (현재 모두 빈 배열)
- `expectations`: grader가 PASS/FAIL로 판정하는 구체적 단언 목록

## 테스트 케이스 목록

| ID | 카테고리 | 설명 |
|----|----------|------|
| 1 | skill-creation | pdf-analyzer 스킬 생성 (P0) |
| 2 | agent-creation | frontend-code-reviewer 에이전트 생성 (P0) |
| 3 | hook-creation | PreToolUse 경로 검증 Hook 생성 (P1) |
| 4 | command-creation | /review-pr 슬래시 커맨드 생성 (P1) |
| 5 | best-practices | Progressive Disclosure 준수 확인 (P0) |

## 수동 실행 방법

### 1. 테스트 프롬프트 실행

```bash
# Claude Code 실행
claude

# 스킬 활성화 후 프롬프트 실행
/ccbuilder
"Create a new skill called 'pdf-analyzer' that helps analyze PDF documents..."
```

### 2. SKILL.md 검증

```bash
python3 skills/ccbuilder/scripts/quick_validate.py skills/pdf-analyzer/SKILL.md
```

### 3. grader 에이전트로 채점

Claude Code에서 grader 에이전트를 실행하여 `grading.json`을 생성합니다:

```bash
# grader.md 지시문에 따라 에이전트 실행
claude --agent skills/ccbuilder/agents/grader.md
```

### 4. 벤치마크 집계

여러 실행 결과를 집계할 때:

```bash
python3 skills/ccbuilder/scripts/aggregate_benchmark.py ./eval-results/
```

## 서브에이전트를 이용한 자동화

ccbuilder 그레이더는 Claude Code 서브에이전트로 실행할 수 있습니다:

```python
# Claude Code SDK 활용 예시
result = await client.run_agent(
    agent_file="skills/ccbuilder/agents/grader.md",
    context={"eval_id": 1, "workspace": "./eval-workspace/"}
)
```

## 이전 평가 시스템

이전 `evaluations/` 디렉토리의 파일들은 참조용으로 보존됩니다.
새 테스트를 추가하거나 기존 테스트를 수정할 때는 `evals.json`을 편집하세요.

---

**패턴 출처**: [anthropics/skills — skill-creator eval pattern](https://github.com/anthropics/skills)
**Last Updated**: 2026-03-08
