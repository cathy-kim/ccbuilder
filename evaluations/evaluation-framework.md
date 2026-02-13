# Claude Code Extension Evaluation Framework

## 목적

Claude Code 확장 기능(Skills, Agents, Hooks, Commands)의 품질을 체계적으로 평가하고 지속적으로 개선하기 위한 프레임워크입니다.

> **공식 문서 기반**: 이 프레임워크는 Anthropic의 공식 평가 가이드를 기반으로 합니다.
> - [Define Success Criteria](https://platform.claude.com/docs/en/test-and-evaluate/define-success)
> - [Develop Tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
> - [Evaluation Tool](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)

---

## 목차

1. [평가 원칙](#1-평가-원칙)
2. [성공 기준 정의 (공식 가이드)](#2-성공-기준-정의-공식-가이드)
3. [Skill 평가](#3-skill-평가)
4. [Agent 평가](#4-agent-평가)
5. [Hook 평가](#5-hook-평가)
6. [Command 평가](#6-command-평가)
7. [평가 방법론 (공식 가이드)](#7-평가-방법론-공식-가이드)
8. [자동화된 테스트](#8-자동화된-테스트)
9. [품질 메트릭](#9-품질-메트릭)
10. [지속적 개선](#10-지속적-개선)

---

## 1. 평가 원칙

### 핵심 평가 기준

| 기준 | 설명 | 가중치 |
|------|------|--------|
| **정확성** | 의도한 대로 동작하는가? | 30% |
| **유용성** | 실제 문제를 해결하는가? | 25% |
| **신뢰성** | 일관되게 작동하는가? | 20% |
| **성능** | 빠르고 효율적인가? | 15% |
| **유지보수성** | 수정/확장이 쉬운가? | 10% |

### 평가 레벨

```
Level 1: 기본 (Basic)
  - 문법 오류 없음
  - 기본 기능 동작
  - 문서화 존재

Level 2: 표준 (Standard)
  - 모든 기본 요구사항 충족
  - 에러 처리 구현
  - 3개 이상 테스트 케이스 통과

Level 3: 프로덕션 (Production)
  - 모든 표준 요구사항 충족
  - 성능 기준 충족 (<100ms)
  - Edge case 처리
  - 10개 이상 테스트 케이스 통과

Level 4: 우수 (Excellent)
  - 모든 프로덕션 요구사항 충족
  - Self-evolution 메커니즘
  - 커뮤니티 피드백 반영
  - 지속적 개선 이력
```

---

## 2. 성공 기준 정의 (공식 가이드)

> Source: https://platform.claude.com/docs/en/test-and-evaluate/define-success

### SMART 기준

좋은 성공 기준은 **SMART**해야 합니다:

| 속성 | 설명 | 예시 |
|------|------|------|
| **Specific** | 명확하게 정의 | "good performance" ❌ → "accurate sentiment classification" ✅ |
| **Measurable** | 정량적 메트릭 사용 | "F1 score >= 0.85" |
| **Achievable** | 벤치마크/연구 기반 | 현재 모델 능력 범위 내 |
| **Relevant** | 목적/사용자와 관련 | 의료 앱의 경우 인용 정확도가 중요 |

### 좋은 기준 vs 나쁜 기준

**나쁜 예**:
```
모델이 감정을 잘 분류해야 한다
```

**좋은 예**:
```
10,000개의 다양한 Twitter 게시물 테스트 세트에서
감정 분석 모델은 최소 0.85의 F1 스코어를 달성해야 하며,
이는 현재 기준선 대비 5% 향상이다.
```

### 일반적인 성공 기준

| 기준 | 설명 |
|------|------|
| **Task Fidelity** | 모델이 작업을 얼마나 잘 수행하는가? |
| **Consistency** | 유사한 입력 → 유사한 응답? |
| **Relevance & Coherence** | 질문에 직접 답변? 논리적 흐름? |
| **Tone & Style** | 기대에 부합? 대상에 적합? |
| **Privacy Preservation** | 민감 정보를 올바르게 처리? |
| **Context Utilization** | 제공된 컨텍스트를 효과적으로 사용? |
| **Latency** | 허용 가능한 응답 시간? |
| **Price** | 예산 내? |

### 다차원 평가 예시

```yaml
criteria:
  - metric: F1 score >= 0.85
  - metric: 99.5% 출력이 비독성
  - metric: 90% 오류가 불편을 유발하지만 치명적이지 않음
  - metric: 95% 응답 시간 < 200ms
```

---

## 3. Skill 평가

### 3.1 구조 평가

```yaml
skill_structure_checklist:
  metadata:
    - [ ] name 필드 존재
    - [ ] description 필드 존재 (< 1024자)
    - [ ] description에 트리거 키워드 포함

  content:
    - [ ] 목적 섹션 존재
    - [ ] 사용 시점 섹션 존재
    - [ ] 핵심 가이드 섹션 존재
    - [ ] 예제 포함

  규칙:
    - [ ] SKILL.md < 500줄
    - [ ] 상세 내용은 references/ 활용
    - [ ] 100줄+ references 파일에 목차 존재
```

### 3.2 트리거 정확도 평가

**테스트 방법:**
```bash
# 트리거 테스트 스크립트
cat > test-skill-trigger.sh << 'EOF'
#!/bin/bash

SKILL_NAME="my-skill"
TEST_PROMPTS=(
  "should trigger: create my-skill component"
  "should trigger: help with my-skill"
  "should NOT trigger: random unrelated task"
  "should NOT trigger: other skill keyword"
)

for prompt in "${TEST_PROMPTS[@]}"; do
  echo "Testing: $prompt"
  echo "{\"prompt\":\"${prompt#*: }\"}" | \
    npx tsx .claude/hooks/skill-activation-prompt.ts
  echo "---"
done
EOF
```

**평가 메트릭:**
```typescript
interface TriggerAccuracyMetrics {
  truePositives: number;   // 올바르게 트리거됨
  falsePositives: number;  // 잘못 트리거됨
  trueNegatives: number;   // 올바르게 트리거 안됨
  falseNegatives: number;  // 트리거되어야 했지만 안됨

  precision: number;  // TP / (TP + FP)
  recall: number;     // TP / (TP + FN)
  f1Score: number;    // 2 * (precision * recall) / (precision + recall)
}

// 목표: F1 Score > 0.85
```

### 3.3 응답 품질 평가

**평가 기준:**
```yaml
response_quality:
  relevance:
    description: "응답이 skill 목적에 부합하는가?"
    scoring:
      - 5: 완벽히 부합
      - 4: 대체로 부합
      - 3: 부분적으로 부합
      - 2: 약간 벗어남
      - 1: 완전히 벗어남

  completeness:
    description: "필요한 모든 정보가 포함되었는가?"
    scoring:
      - 5: 모든 정보 포함
      - 4: 대부분 포함
      - 3: 절반 정도 포함
      - 2: 일부만 포함
      - 1: 거의 없음

  actionability:
    description: "실행 가능한 가이드를 제공하는가?"
    scoring:
      - 5: 즉시 실행 가능
      - 4: 약간의 추가 작업 필요
      - 3: 중간 정도 추가 작업 필요
      - 2: 상당한 추가 작업 필요
      - 1: 실행 불가능
```

### 3.4 Skill 평가 체크리스트

```markdown
## Skill Evaluation Checklist

### 기본 요구사항
- [ ] SKILL.md 파일 존재
- [ ] 500줄 미만
- [ ] Frontmatter (name, description) 포함
- [ ] 목적, 사용 시점, 핵심 가이드 섹션 존재

### 트리거 테스트 (최소 5개)
- [ ] 관련 키워드로 트리거됨
- [ ] 의도 패턴으로 트리거됨
- [ ] 무관한 프롬프트에 트리거 안됨
- [ ] 유사하지만 다른 skill에 트리거 안됨
- [ ] Edge case 처리

### 품질 테스트 (최소 3개 시나리오)
- [ ] 시나리오 1: [설명] - Pass/Fail
- [ ] 시나리오 2: [설명] - Pass/Fail
- [ ] 시나리오 3: [설명] - Pass/Fail

### 성능 테스트
- [ ] Hook 실행 시간 < 100ms
- [ ] 메모리 사용량 적정

### 점수
- 트리거 정확도: __/100
- 응답 품질: __/100
- 종합 점수: __/100
- 평가 레벨: Basic / Standard / Production / Excellent
```

---

## 4. Agent 평가

### 4.1 Agent 평가 기준

```yaml
agent_evaluation_criteria:
  autonomy:
    description: "자율적으로 작업을 완료할 수 있는가?"
    weight: 30%
    metrics:
      - completion_rate: "작업 완료율"
      - intervention_needed: "사용자 개입 필요 횟수"
      - error_recovery: "에러 자동 복구율"

  accuracy:
    description: "정확한 결과를 생성하는가?"
    weight: 25%
    metrics:
      - correctness: "결과 정확도"
      - consistency: "일관성"
      - hallucination_rate: "허위 정보 생성률"

  efficiency:
    description: "효율적으로 작업을 수행하는가?"
    weight: 20%
    metrics:
      - tool_calls: "도구 호출 횟수"
      - duration: "총 실행 시간"
      - token_usage: "토큰 사용량"

  reporting:
    description: "명확한 보고서를 생성하는가?"
    weight: 15%
    metrics:
      - clarity: "보고서 명확성"
      - completeness: "보고서 완전성"
      - actionability: "실행 가능한 권장사항"

  safety:
    description: "안전하게 작동하는가?"
    weight: 10%
    metrics:
      - destructive_ops: "파괴적 작업 수행 여부"
      - scope_adherence: "범위 준수"
      - permission_respect: "권한 존중"
```

### 4.2 Agent QA 테스트 형식

Instagram Card Generator 평가 시스템 참고하여 QA 기반 테스트:

```xml
<evaluation>
  <agent_name>code-architecture-reviewer</agent_name>
  <version>1.0.0</version>

  <qa_pair>
    <scenario>Simple React Component Review</scenario>
    <input>
      Review the UserProfile.tsx component for architecture issues.
      File content: [simple React component with 50 lines]
    </input>
    <expected_outputs>
      <contains>component structure analysis</contains>
      <contains>prop types review</contains>
      <contains>recommendations section</contains>
    </expected_outputs>
    <expected_tool_calls>
      <tool>Read</tool>
      <tool>Grep</tool>
    </expected_tool_calls>
    <max_duration_seconds>30</max_duration_seconds>
  </qa_pair>

  <qa_pair>
    <scenario>Complex Multi-file Review</scenario>
    <input>
      Review the authentication module (src/auth/*) for security issues.
    </input>
    <expected_outputs>
      <contains>security vulnerability assessment</contains>
      <contains>authentication flow analysis</contains>
      <contains>severity ratings</contains>
    </expected_outputs>
    <expected_tool_calls>
      <tool>Glob</tool>
      <tool>Read</tool>
      <tool>Grep</tool>
    </expected_tool_calls>
    <max_duration_seconds>120</max_duration_seconds>
  </qa_pair>
</evaluation>
```

### 4.3 Agent 평가 실행 스크립트

```typescript
#!/usr/bin/env npx tsx

interface AgentEvalResult {
  agentName: string;
  scenario: string;
  passed: boolean;
  metrics: {
    duration: number;
    toolCalls: number;
    outputContains: { expected: string; found: boolean }[];
    completionRate: number;
  };
  issues: string[];
}

async function evaluateAgent(
  agentName: string,
  evalFile: string
): Promise<AgentEvalResult[]> {
  // 평가 파일 파싱
  const evaluations = parseEvalFile(evalFile);
  const results: AgentEvalResult[] = [];

  for (const qa of evaluations) {
    const startTime = Date.now();

    // Agent 실행 (실제 구현 시 Task 도구 사용)
    const result = await runAgent(agentName, qa.input);

    const duration = Date.now() - startTime;

    // 결과 검증
    const outputChecks = qa.expectedOutputs.map(expected => ({
      expected,
      found: result.output.includes(expected)
    }));

    results.push({
      agentName,
      scenario: qa.scenario,
      passed: outputChecks.every(c => c.found) &&
              duration <= qa.maxDuration * 1000,
      metrics: {
        duration,
        toolCalls: result.toolCalls.length,
        outputContains: outputChecks,
        completionRate: outputChecks.filter(c => c.found).length /
                        outputChecks.length
      },
      issues: outputChecks
        .filter(c => !c.found)
        .map(c => `Missing: ${c.expected}`)
    });
  }

  return results;
}
```

### 4.4 Agent 평가 보고서 형식

```markdown
# Agent Evaluation Report

## Agent: code-architecture-reviewer
## Version: 1.0.0
## Date: 2025-01-27

### Summary

| Metric | Score | Target | Status |
|--------|-------|--------|--------|
| Completion Rate | 92% | 90% | ✅ |
| Accuracy | 88% | 85% | ✅ |
| Avg Duration | 45s | 60s | ✅ |
| Tool Efficiency | 8.5 calls/task | <15 | ✅ |

### Scenario Results

#### Scenario 1: Simple React Component Review
- **Status**: ✅ PASSED
- **Duration**: 28s
- **Tool Calls**: 5
- **Output Validation**:
  - ✅ Contains component structure analysis
  - ✅ Contains prop types review
  - ✅ Contains recommendations section

#### Scenario 2: Complex Multi-file Review
- **Status**: ⚠️ PARTIAL
- **Duration**: 95s
- **Tool Calls**: 12
- **Output Validation**:
  - ✅ Contains security vulnerability assessment
  - ⚠️ Missing: authentication flow analysis
  - ✅ Contains severity ratings
- **Issues**:
  - Authentication flow diagram not generated
  - Consider adding flow visualization

### Recommendations

1. **Improve flow analysis**: Add explicit step to generate authentication flow
2. **Optimize tool usage**: Consider caching repeated file reads
3. **Add timeout handling**: Long-running analysis should have checkpoints

### Overall Score: 87/100 (Production Ready)
```

---

## 5. Hook 평가

### 5.1 Hook 평가 기준

```yaml
hook_evaluation:
  performance:
    target: < 100ms
    critical: < 500ms
    unacceptable: >= 500ms

  reliability:
    crash_rate: 0%
    error_handling: "graceful degradation"
    state_management: "session-aware"

  correctness:
    exit_codes: "appropriate for hook type"
    output_format: "valid JSON/text"
    side_effects: "none or documented"

  integration:
    settings_json: "correctly registered"
    permissions: "minimal required"
    dependencies: "documented and pinned"
```

### 5.2 Hook 테스트 시나리오

```typescript
interface HookTestCase {
  name: string;
  hookType: 'UserPromptSubmit' | 'PreToolUse' | 'Stop';
  input: object;
  expectedExitCode: number;
  expectedStdout?: string | RegExp;
  expectedStderr?: string | RegExp;
  maxDuration: number;
}

const hookTests: HookTestCase[] = [
  // UserPromptSubmit 테스트
  {
    name: "skill-activation-prompt triggers for keyword",
    hookType: "UserPromptSubmit",
    input: { session_id: "test", prompt: "create frontend component" },
    expectedExitCode: 0,
    expectedStdout: /frontend-dev-guidelines/,
    maxDuration: 100
  },
  {
    name: "skill-activation-prompt ignores unrelated",
    hookType: "UserPromptSubmit",
    input: { session_id: "test", prompt: "hello world" },
    expectedExitCode: 0,
    expectedStdout: "",
    maxDuration: 50
  },

  // PreToolUse 테스트
  {
    name: "verification-guard blocks unauthorized edit",
    hookType: "PreToolUse",
    input: {
      tool_name: "Edit",
      tool_input: { file_path: "/etc/passwd" }
    },
    expectedExitCode: 2,
    expectedStderr: /blocked|denied/i,
    maxDuration: 50
  },

  // Stop 테스트
  {
    name: "error-handling-reminder suggests on error",
    hookType: "Stop",
    input: {
      session_id: "test",
      last_response: "Error: ENOENT file not found"
    },
    expectedExitCode: 0,
    expectedStdout: /error.*handling|suggest/i,
    maxDuration: 100
  }
];
```

### 5.3 Hook 벤치마크 스크립트

```bash
#!/bin/bash
# hook-benchmark.sh - Hook 성능 벤치마크

HOOK_PATH=".claude/hooks/skill-activation-prompt.ts"
ITERATIONS=100

echo "=== Hook Performance Benchmark ==="
echo "Hook: $HOOK_PATH"
echo "Iterations: $ITERATIONS"
echo ""

# 준비
INPUT='{"session_id":"bench","prompt":"test prompt"}'

# 벤치마크 실행
total_time=0
min_time=999999
max_time=0

for i in $(seq 1 $ITERATIONS); do
  start=$(date +%s%N)
  echo "$INPUT" | npx tsx "$HOOK_PATH" > /dev/null 2>&1
  end=$(date +%s%N)

  duration=$(( (end - start) / 1000000 ))  # ms
  total_time=$((total_time + duration))

  if [ $duration -lt $min_time ]; then min_time=$duration; fi
  if [ $duration -gt $max_time ]; then max_time=$duration; fi
done

avg_time=$((total_time / ITERATIONS))

echo "Results:"
echo "  Min: ${min_time}ms"
echo "  Max: ${max_time}ms"
echo "  Avg: ${avg_time}ms"
echo ""

# 평가
if [ $avg_time -lt 100 ]; then
  echo "✅ PASS: Average time < 100ms"
elif [ $avg_time -lt 500 ]; then
  echo "⚠️ WARNING: Average time >= 100ms but < 500ms"
else
  echo "❌ FAIL: Average time >= 500ms"
fi
```

---

## 6. Command 평가

### 6.1 Command 평가 기준

```yaml
command_evaluation:
  documentation:
    - clear_purpose: "명확한 목적 설명"
    - parameter_docs: "파라미터 문서화"
    - examples: "사용 예제 포함"

  functionality:
    - correct_behavior: "의도대로 동작"
    - error_messages: "명확한 에러 메시지"
    - edge_cases: "경계 조건 처리"

  usability:
    - intuitive_name: "직관적인 이름"
    - reasonable_defaults: "합리적인 기본값"
    - help_available: "도움말 제공"
```

### 6.2 Command 테스트 템플릿

```markdown
## Command Test: /dev-docs

### Test Case 1: Basic Execution
**Input**: `/dev-docs`
**Expected**:
- [ ] 문서 생성 시작
- [ ] 프로젝트 구조 분석
- [ ] README 또는 문서 파일 생성/업데이트

### Test Case 2: With Parameters
**Input**: `/dev-docs --format markdown --output ./docs`
**Expected**:
- [ ] 지정된 형식으로 출력
- [ ] 지정된 경로에 저장

### Test Case 3: Error Handling
**Input**: `/dev-docs --invalid-option`
**Expected**:
- [ ] 명확한 에러 메시지
- [ ] 올바른 사용법 안내

### Results
| Test Case | Status | Notes |
|-----------|--------|-------|
| Basic | ✅/❌ | |
| With Params | ✅/❌ | |
| Error | ✅/❌ | |
```

---

## 7. 평가 방법론 (공식 가이드)

> Source: https://platform.claude.com/docs/en/test-and-evaluate/develop-tests

### 7.1 평가 설계 원칙

1. **작업별 특화**: 실제 작업 분포를 반영하고 edge case 포함
2. **가능한 자동화**: 다지선다, 문자열 매칭, 코드 채점, LLM 채점
3. **양 우선**: 약간 낮은 신호의 자동 채점이 높은 품질의 수동 채점보다 낫다

### 7.2 공식 평가 방법 (Official Methods)

| 평가 유형 | 방법 | 사용 사례 |
|-----------|------|-----------|
| 범주형 답변 | Exact Match | 감정 분류, 카테고리화 |
| 일관성 | Cosine Similarity | FAQ 봇, 반복 쿼리 |
| 요약 품질 | ROUGE-L | 뉴스 요약, 문서 압축 |
| 주관적 품질 | LLM Likert Scale | 톤, 공감, 전문성 |
| 안전/개인정보 | LLM Binary | PHI 감지, 콘텐츠 필터링 |
| 컨텍스트 활용 | LLM Ordinal | 멀티턴 대화 |

### 7.3 Exact Match 평가

```python
def evaluate_exact_match(model_output, correct_answer):
    return model_output.strip().lower() == correct_answer.lower()

# 예제
tweets = [
    {"text": "This movie was terrible.", "sentiment": "negative"},
    {"text": "The album is amazing!", "sentiment": "positive"},
]
accuracy = sum(evaluate_exact_match(o, t['sentiment'])
               for o, t in zip(outputs, tweets)) / len(tweets)
```

### 7.4 Cosine Similarity 평가

```python
from sentence_transformers import SentenceTransformer
import numpy as np

def evaluate_cosine_similarity(outputs):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = [model.encode(output) for output in outputs]
    cosine_sims = np.dot(embeddings, embeddings.T) / \
        (np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embeddings, axis=1).T)
    return np.mean(cosine_sims)
```

### 7.5 LLM 기반 Likert Scale 평가

```python
def evaluate_likert(model_output, target_tone):
    prompt = f"""Rate this response on a scale of 1-5 for being {target_tone}:
    <response>{model_output}</response>
    1: Not at all {target_tone}
    5: Perfectly {target_tone}
    Output only the number."""

    # 평가용 모델은 생성 모델과 다르게
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    return int(response.content[0].text.strip())
```

### 7.6 채점 방법 선택

| 방법 | 속도 | 신뢰성 | 확장성 | 유연성 |
|------|------|--------|--------|--------|
| **코드 기반** | 가장 빠름 | 가장 높음 | 매우 높음 | 낮음 |
| **인간 채점** | 느림 | 높음 | 낮음 | 가장 높음 |
| **LLM 기반** | 빠름 | 중간 | 높음 | 높음 |

### 7.7 LLM 채점 모범 사례

1. **명확한 루브릭**: "답변은 첫 문장에 항상 'Acme Inc.'를 언급해야 함"
2. **경험적/구체적**: 'correct' 또는 'incorrect' 출력, 1-5 척도
3. **추론 권장**: 점수 결정 전 생각하도록 요청

```python
grader_prompt = """Grade this answer based on the rubric:
<rubric>{rubric}</rubric>
<answer>{answer}</answer>
Think through your reasoning in <thinking> tags,
then output 'correct' or 'incorrect' in <result> tags."""
```

---

## 8. 자동화된 테스트

### 8.1 CI/CD 통합

```yaml
# .github/workflows/claude-extension-tests.yml
name: Claude Extension Tests

on:
  push:
    paths:
      - '.claude/**'
  pull_request:
    paths:
      - '.claude/**'

jobs:
  test-extensions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd .claude/hooks
          npm ci

      - name: Validate skill structure
        run: |
          node scripts/validate-skills.js

      - name: Run hook tests
        run: |
          node scripts/test-hooks.js

      - name: Check 500-line rule
        run: |
          find .claude/skills -name "SKILL.md" -exec sh -c '
            lines=$(wc -l < "$1")
            if [ $lines -gt 500 ]; then
              echo "❌ $1: $lines lines (exceeds 500)"
              exit 1
            fi
            echo "✅ $1: $lines lines"
          ' _ {} \;

      - name: Generate evaluation report
        run: |
          node scripts/generate-eval-report.js

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: evaluation-report
          path: evaluation-report.md
```

### 8.2 자동화 스크립트

```typescript
// scripts/validate-skills.js
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'yaml';

interface ValidationResult {
  skill: string;
  valid: boolean;
  issues: string[];
}

function validateSkill(skillPath: string): ValidationResult {
  const issues: string[] = [];
  const skillMd = path.join(skillPath, 'SKILL.md');

  // 파일 존재 확인
  if (!fs.existsSync(skillMd)) {
    return { skill: skillPath, valid: false, issues: ['SKILL.md not found'] };
  }

  const content = fs.readFileSync(skillMd, 'utf-8');
  const lines = content.split('\n');

  // 500-line rule
  if (lines.length > 500) {
    issues.push(`SKILL.md exceeds 500 lines (${lines.length})`);
  }

  // Frontmatter 확인
  if (!content.startsWith('---')) {
    issues.push('Missing frontmatter');
  } else {
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const frontmatter = yaml.parse(frontmatterMatch[1]);
      if (!frontmatter.name) issues.push('Missing name in frontmatter');
      if (!frontmatter.description) issues.push('Missing description in frontmatter');
    }
  }

  // 필수 섹션 확인
  const requiredSections = ['목적', '사용 시점'];
  for (const section of requiredSections) {
    if (!content.includes(`## ${section}`)) {
      issues.push(`Missing section: ## ${section}`);
    }
  }

  return {
    skill: path.basename(skillPath),
    valid: issues.length === 0,
    issues
  };
}

// 실행
const skillsDir = '.claude/skills';
const skills = fs.readdirSync(skillsDir)
  .filter(f => fs.statSync(path.join(skillsDir, f)).isDirectory());

const results = skills.map(s => validateSkill(path.join(skillsDir, s)));

console.log('=== Skill Validation Results ===\n');
for (const result of results) {
  const status = result.valid ? '✅' : '❌';
  console.log(`${status} ${result.skill}`);
  for (const issue of result.issues) {
    console.log(`   - ${issue}`);
  }
}

const passed = results.filter(r => r.valid).length;
console.log(`\nTotal: ${passed}/${results.length} passed`);

process.exit(results.every(r => r.valid) ? 0 : 1);
```

---

## 9. 품질 메트릭

### 9.1 메트릭 대시보드

```typescript
interface ExtensionMetrics {
  // Skill 메트릭
  skills: {
    total: number;
    averageLines: number;
    triggerAccuracy: number;
    responseQuality: number;
    levelDistribution: {
      basic: number;
      standard: number;
      production: number;
      excellent: number;
    };
  };

  // Agent 메트릭
  agents: {
    total: number;
    averageCompletionRate: number;
    averageAccuracy: number;
    averageDuration: number;
    toolEfficiency: number;
  };

  // Hook 메트릭
  hooks: {
    total: number;
    averageLatency: number;
    errorRate: number;
    coverageRate: number;
  };

  // Command 메트릭
  commands: {
    total: number;
    documentationScore: number;
    usabilityScore: number;
  };

  // 전체 점수
  overallScore: number;
  lastUpdated: string;
}
```

### 9.2 점수 계산

```typescript
function calculateOverallScore(metrics: ExtensionMetrics): number {
  const weights = {
    skills: 0.35,
    agents: 0.30,
    hooks: 0.25,
    commands: 0.10
  };

  const skillScore = (
    metrics.skills.triggerAccuracy * 0.4 +
    metrics.skills.responseQuality * 0.4 +
    (1 - metrics.skills.averageLines / 500) * 0.2
  ) * 100;

  const agentScore = (
    metrics.agents.averageCompletionRate * 0.4 +
    metrics.agents.averageAccuracy * 0.4 +
    Math.min(1, 60 / metrics.agents.averageDuration) * 0.2
  ) * 100;

  const hookScore = (
    Math.min(1, 100 / metrics.hooks.averageLatency) * 0.5 +
    (1 - metrics.hooks.errorRate) * 0.3 +
    metrics.hooks.coverageRate * 0.2
  ) * 100;

  const commandScore = (
    metrics.commands.documentationScore * 0.5 +
    metrics.commands.usabilityScore * 0.5
  ) * 100;

  return (
    skillScore * weights.skills +
    agentScore * weights.agents +
    hookScore * weights.hooks +
    commandScore * weights.commands
  );
}
```

### 9.3 메트릭 보고서 형식

```markdown
# Extension Quality Report

## Summary
- **Overall Score**: 87/100
- **Last Updated**: 2025-01-27

## Skills (35%)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total | 12 | - | - |
| Avg Lines | 320 | <500 | ✅ |
| Trigger Accuracy | 89% | >85% | ✅ |
| Response Quality | 85% | >80% | ✅ |

### Level Distribution
- Basic: 2 (17%)
- Standard: 4 (33%)
- Production: 5 (42%)
- Excellent: 1 (8%)

## Agents (30%)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total | 10 | - | - |
| Completion Rate | 92% | >90% | ✅ |
| Accuracy | 88% | >85% | ✅ |
| Avg Duration | 45s | <60s | ✅ |

## Hooks (25%)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total | 6 | - | - |
| Avg Latency | 45ms | <100ms | ✅ |
| Error Rate | 0.1% | <1% | ✅ |
| Coverage | 85% | >80% | ✅ |

## Commands (10%)
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total | 4 | - | - |
| Documentation | 90% | >80% | ✅ |
| Usability | 85% | >80% | ✅ |
```

---

## 10. 지속적 개선

### 10.1 개선 프로세스

```
1. 데이터 수집
   ↓
2. 메트릭 분석
   ↓
3. 문제 식별
   ↓
4. 개선안 도출
   ↓
5. 구현 및 테스트
   ↓
6. 배포 및 모니터링
   ↓
(반복)
```

### 10.2 개선 로그 형식

```markdown
# Improvement Log

## v1.2.0 (2025-01-27)

### Issues Identified
1. **Skill trigger false positives**: 15% → needs reduction
2. **Agent timeout on complex tasks**: 8% timeout rate
3. **Hook latency spike**: P99 latency 250ms

### Changes Made
1. **Skill triggers**
   - Refined keyword matching regex
   - Added negative patterns
   - Result: False positives 15% → 5%

2. **Agent timeouts**
   - Added checkpointing for long tasks
   - Implemented progressive response
   - Result: Timeout rate 8% → 2%

3. **Hook performance**
   - Optimized JSON parsing
   - Added caching for session state
   - Result: P99 latency 250ms → 80ms

### Metrics Before/After
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Trigger Accuracy | 85% | 92% | +7% |
| Agent Completion | 88% | 95% | +7% |
| Hook P99 Latency | 250ms | 80ms | -68% |
| Overall Score | 78 | 87 | +9 |

---

## v1.1.0 (2025-01-20)
...
```

### 10.3 Self-Evolution 메커니즘

```typescript
interface ImprovementProposal {
  category: 'skill' | 'agent' | 'hook' | 'command';
  target: string;
  issue: string;
  recommendation: string;
  confidence: number;
  impact: 'low' | 'medium' | 'high';
  effort: 'low' | 'medium' | 'high';
  proposedChange?: {
    file: string;
    section: string;
    content: string;
  };
}

async function analyzeAndPropose(
  metrics: ExtensionMetrics,
  executionHistory: any[]
): Promise<ImprovementProposal[]> {
  const proposals: ImprovementProposal[] = [];

  // 트리거 정확도가 낮은 skill 분석
  if (metrics.skills.triggerAccuracy < 0.85) {
    proposals.push({
      category: 'skill',
      target: 'all',
      issue: 'Low trigger accuracy',
      recommendation: 'Review and refine trigger keywords in descriptions',
      confidence: 0.9,
      impact: 'high',
      effort: 'medium'
    });
  }

  // Hook 지연 분석
  if (metrics.hooks.averageLatency > 100) {
    proposals.push({
      category: 'hook',
      target: 'performance',
      issue: 'High average latency',
      recommendation: 'Optimize JSON parsing and reduce I/O operations',
      confidence: 0.85,
      impact: 'medium',
      effort: 'low'
    });
  }

  // 실행 이력에서 패턴 분석
  const failurePatterns = analyzeFailures(executionHistory);
  for (const pattern of failurePatterns) {
    proposals.push({
      category: pattern.category,
      target: pattern.target,
      issue: pattern.description,
      recommendation: pattern.fix,
      confidence: pattern.confidence,
      impact: pattern.impact,
      effort: pattern.effort
    });
  }

  return proposals.filter(p => p.confidence > 0.7);
}
```

---

## 부록

### A. 평가 도구 설치

```bash
# 필수 의존성
npm install -g tsx
cd .claude/hooks && npm install

# 평가 스크립트 설치
cp -r path/to/evaluation-scripts .claude/scripts/
chmod +x .claude/scripts/*.sh
```

### B. 빠른 평가 명령어

```bash
# 전체 평가 실행
.claude/scripts/run-full-evaluation.sh

# Skill만 평가
.claude/scripts/evaluate-skills.sh

# Hook 벤치마크
.claude/scripts/hook-benchmark.sh

# 평가 보고서 생성
.claude/scripts/generate-report.sh > evaluation-report.md
```

### C. 참고 자료

#### 공식 문서 (Anthropic)
- [Define Success Criteria](https://platform.claude.com/docs/en/test-and-evaluate/define-success)
- [Develop Tests](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)
- [Evaluation Tool](https://platform.claude.com/docs/en/test-and-evaluate/eval-tool)
- [Reduce Latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency)

#### 로컬 참조
- [LLM Evaluation Guide (공식 문서 요약)](official-docs/llm-evaluation-guide.md)
- [Instagram Card Generator Evaluation Framework](../../instagram-card-generator/references/evaluation-framework.md)
- [MCP Server Evaluation Guide](../../mcp-builder/reference/evaluation.md)
- [Infrastructure Showcase](infrastructure-showcase/README.md)

---

**문서 상태**: PRODUCTION-READY ✅
**마지막 업데이트**: 2025-12-14
**공식 문서 기반**: ✅
