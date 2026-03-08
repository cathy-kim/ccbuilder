# Skill 평가 가이드

**Version**: 1.0.0
**Last Updated**: 2026-03-08
**Based on**: anthropics/skills skill-creator eval pattern

## 목차

1. [개요](#1-개요)
2. [Eval 워크플로우](#2-eval-워크플로우)
3. [evals.json 작성법](#3-evalsjson-작성법)
4. [테스트 실행](#4-테스트-실행)
5. [채점 (Grading)](#5-채점-grading)
6. [벤치마크 집계](#6-벤치마크-집계)
7. [결과 리뷰](#7-결과-리뷰)
8. [스킬 개선 루프](#8-스킬-개선-루프)
9. [Description 최적화](#9-description-최적화)
10. [블라인드 비교 (A/B)](#10-블라인드-비교-ab)
11. [Quick Reference](#11-quick-reference)

---

## 1. 개요

ccbuilder의 eval 시스템은 Anthropic 공식 skill-creator 패턴을 따릅니다.

핵심 루프:
```
스킬 작성 → evals.json 작성 (2-3개) → subagent 실행 (with_skill + baseline)
→ assertion 채점 → 벤치마크 집계 → 리뷰 → 개선 → 반복
```

### Eval vs Improve vs Benchmark

| 모드 | 목적 | 실행 방법 |
|------|------|-----------|
| **Eval** | 스킬 유/무 비교 테스트 | `/ccbuilder eval <skill-path>` |
| **Improve** | eval 피드백 기반 개선 | `/ccbuilder improve <skill-path>` |
| **Benchmark** | 다수 실행 통계 집계 | `/ccbuilder benchmark <skill-path>` |

## 2. Eval 워크플로우

전체 시퀀스 — 중간에 멈추지 않고 끝까지 실행합니다.

### 디렉토리 구조

결과는 스킬 디렉토리와 같은 레벨의 `<skill-name>-workspace/`에 저장합니다:

```
<skill-name>-workspace/
├── iteration-1/
│   ├── eval-1-descriptive-name/
│   │   ├── with_skill/
│   │   │   ├── outputs/          # 스킬이 생성한 파일들
│   │   │   ├── timing.json       # 토큰/시간 데이터
│   │   │   └── grading.json      # 채점 결과
│   │   ├── without_skill/        # (또는 old_skill/)
│   │   │   ├── outputs/
│   │   │   ├── timing.json
│   │   │   └── grading.json
│   │   └── eval_metadata.json    # 프롬프트 + assertions
│   ├── benchmark.json            # 집계 결과
│   └── benchmark.md              # 마크다운 리포트
├── iteration-2/
│   └── ...
└── feedback.json                 # 사용자 리뷰
```

### Step 1: 모든 실행을 한 턴에 시작

각 테스트 케이스마다 두 subagent를 **같은 턴에** 시작합니다:

**With-skill 실행:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
```

**Baseline 실행** (스킬 없이 같은 프롬프트):
- 새 스킬 만들기: 스킬 없이 같은 프롬프트 → `without_skill/outputs/`
- 기존 스킬 개선: 이전 버전 스냅샷 → `old_skill/outputs/`

각 eval에 `eval_metadata.json` 작성:
```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: 대기 중 assertion 작성

실행을 기다리는 동안 정량적 assertion을 작성합니다:

- 객관적으로 검증 가능한 것만 assertion으로
- 주관적 품질은 정성적 리뷰에서 평가
- assertion 이름은 벤치마크 뷰어에서 한눈에 알 수 있도록 서술적으로

`eval_metadata.json`과 `evals/evals.json`에 assertions 추가.

### Step 3: 실행 완료 시 timing 즉시 캡처

subagent 완료 notification에서 `total_tokens`, `duration_ms`를 즉시 저장:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

**주의**: 이 데이터는 notification에서만 얻을 수 있습니다 — 바로 저장하세요.

### Step 4: 채점 + 집계 + 리뷰

1. **채점**: grader agent (또는 인라인)가 각 assertion을 outputs에 대해 PASS/FAIL 판정
   - `grading.json`의 expectations 배열은 반드시 `text`, `passed`, `evidence` 필드 사용
   - 프로그래밍으로 체크 가능한 assertion은 스크립트로 검증 (눈으로 확인 X)

2. **집계**:
   ```bash
   python skills/ccbuilder/scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
   ```
   → `benchmark.json` + `benchmark.md` 생성

3. **분석**: 벤치마크 데이터에서 패턴 분석
   - 스킬 유무 관계없이 항상 PASS하는 assertion (비변별적)
   - 분산이 높은 eval (flaky)
   - 시간/토큰 트레이드오프

4. **리뷰**: 결과를 사용자에게 보여주고 피드백 요청

## 3. evals.json 작성법

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "실제 사용자가 말할 법한 구체적 프롬프트",
      "expected_output": "기대 결과 설명",
      "files": [],
      "expectations": [
        "출력에 X 파일이 포함됨",
        "Y 섹션이 존재함"
      ]
    }
  ]
}
```

### 좋은 테스트 프롬프트

- 실제 사용자가 말할 법한 것 (2-3개 권장)
- 구체적이고 상세한 요청
- Edge case 포함

### 좋은 assertion

- 객관적으로 검증 가능 (파일 존재, 라인 수, 키워드 포함)
- 서술적 이름 (벤치마크에서 한눈에 이해)
- 주관적 품질은 assertion으로 강제하지 않음 → 정성 리뷰

## 4. 테스트 실행

### Subagent 실행 패턴

각 eval에 대해 두 개의 subagent를 병렬로 실행합니다:

1. **with_skill**: 대상 스킬을 활성화한 상태에서 eval prompt 실행
2. **without_skill** (또는 **old_skill**): 스킬 없이 (또는 이전 버전으로) 같은 prompt 실행

```
Task(subagent_type="general-purpose", prompt="...", skill_path="<path>")  # with_skill
Task(subagent_type="general-purpose", prompt="...")                        # without_skill
```

### Baseline 전략

| 시나리오 | Baseline |
|----------|----------|
| 새 스킬 평가 | `without_skill/` — 스킬 없이 동일 prompt |
| 스킬 개선 후 비교 | `old_skill/` — 이전 버전 스냅샷 사용 |
| A/B 비교 | 두 버전 모두 별도 디렉토리 |

### 타이밍 캡처

subagent 완료 시 notification에서 즉시 `timing.json` 저장:
- `total_tokens`: 총 사용 토큰
- `duration_ms`: 실행 시간 (밀리초)
- `total_duration_seconds`: 실행 시간 (초)

## 5. 채점 (Grading)

Grader agent 사용: `agents/grader.md` 참조.

### 채점 프로세스

1. 각 eval의 `with_skill/outputs/`와 `without_skill/outputs/` 읽기
2. `eval_metadata.json`의 assertions를 하나씩 검증
3. 프로그래밍 가능한 assertion은 스크립트로 자동 검증
4. 결과를 `grading.json`에 저장

### 출력 스키마 (`grading.json`)

```json
{
  "eval_id": 1,
  "skill_name": "my-skill",
  "expectations": [
    {"text": "SKILL.md가 500줄 이하", "passed": true, "evidence": "wc -l 결과: 487줄"}
  ],
  "summary": {
    "passed": 7, "failed": 2, "total": 9, "pass_rate": 0.78
  },
  "execution_metrics": {},
  "timing": {}
}
```

### 채점 규칙

- `expectations` 배열의 각 항목은 반드시 `text`, `passed`, `evidence` 필드 포함
- `evidence`는 PASS/FAIL 근거 (파일 경로, 명령 출력 등)
- 주관적 품질은 채점하지 않음 → 정성 리뷰에서 별도 평가

## 6. 벤치마크 집계

```bash
python skills/ccbuilder/scripts/aggregate_benchmark.py <workspace>/iteration-N --skill-name <name>
```

### 결과 파일

- **`benchmark.json`**: 기계 판독용
  - `pass_rate`: mean +/- stddev
  - `tokens`: with_skill vs without_skill 평균
  - `duration`: with_skill vs without_skill 평균
  - assertion별 pass rate

- **`benchmark.md`**: 마크다운 테이블
  - 전체 요약 (pass rate, 토큰, 시간)
  - eval별 상세 결과
  - assertion별 pass/fail 히트맵

### 분석 포인트

| 패턴 | 의미 | 조치 |
|------|------|------|
| 양쪽 다 PASS | 비변별적 assertion | assertion 강화 또는 제거 |
| 높은 분산 | Flaky eval | prompt 구체화 |
| with_skill만 PASS | 스킬 고유 가치 | 핵심 assertion으로 유지 |
| 토큰 2x+ 증가 | 비용 트레이드오프 | 스킬 간결화 검토 |

## 7. 결과 리뷰

정성적 + 정량적 결과를 사용자에게 보여줍니다:

### 제시 내용

- 각 테스트 케이스의 입력/출력 요약
- Assertion PASS/FAIL 결과 (테이블)
- 벤치마크 요약 (pass_rate, 토큰, 시간)
- with_skill vs without_skill 차이 하이라이트

### 피드백 수집

- `feedback.json`에 사용자 피드백 저장
- 피드백이 비어있으면 = 만족한 것
- 불만이 있는 테스트 케이스에 집중하여 개선

## 8. 스킬 개선 루프

### 개선 원칙

1. **일반화**: 테스트 케이스에 overfitting하지 말 것. 특정 예제만 고치는 게 아니라 패턴을 개선
2. **경량 유지**: 효과 없는 지시문 제거. 트랜스크립트를 읽고 비생산적 행동 유발하는 부분 삭제
3. **이유 설명**: ALWAYS/NEVER 대신 왜 중요한지 설명
4. **반복 작업 감지**: 모든 테스트에서 동일한 스크립트를 작성한다면 → `scripts/`에 번들링

### 반복 루프

1. 스킬 개선 적용
2. 새 `iteration-<N+1>/`에 모든 테스트 재실행 (baseline 포함)
3. 사용자 리뷰
4. 피드백 읽기 → 개선 → 반복

### 종료 조건

- 사용자가 만족
- 피드백이 모두 빈칸
- 의미 있는 진전이 없음

## 9. Description 최적화

스킬의 `description` 필드를 최적화하여 트리거 정확도를 높입니다.

### Step 1: 트리거 eval 쿼리 생성

should-trigger (8-10개) + should-not-trigger (8-10개), 총 20개:

```json
[
  {"query": "구체적이고 현실적인 사용자 프롬프트...", "should_trigger": true},
  {"query": "유사하지만 다른 스킬이 필요한 프롬프트...", "should_trigger": false}
]
```

**좋은 쿼리**:
- 구체적, 상세, 개인 컨텍스트 포함
- Near-miss (키워드는 비슷하지만 실제로는 다른 작업)

**나쁜 쿼리**:
- 너무 뻔한 것 ("Format this data")
- 완전히 무관한 것 ("Write fibonacci")

### Step 2: 최적화 루프 실행

```bash
python -m scripts.run_loop \
  --eval-set <trigger-eval.json> \
  --skill-path <skill-path> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

- 60% train / 40% test 자동 분할
- 쿼리당 3회 실행으로 신뢰도 확보
- Test score 기준으로 best description 선택 (overfitting 방지)

## 10. 블라인드 비교 (A/B)

두 버전 비교 시: comparator agent가 어떤 버전인지 모르고 품질 판정.

- Content (정확성, 완전성) + Structure (구성, 포맷) 1-5점
- Optional -- 대부분 사용자는 직접 리뷰로 충분

`agents/comparator.md` 참조.

## 11. Quick Reference

### 명령어 요약

| 명령 | 용도 |
|------|------|
| `/ccbuilder eval <skill-path>` | 스킬 평가 실행 |
| `/ccbuilder improve <skill-path>` | 피드백 기반 개선 |
| `/ccbuilder benchmark <skill-path>` | 벤치마크 집계 |
| `python scripts/quick_validate.py <SKILL.md>` | frontmatter 검증 |
| `python scripts/aggregate_benchmark.py <dir>` | 벤치마크 집계 |
| `python -m scripts.run_loop --eval-set ... --skill-path ...` | description 최적화 |

### 파일 구조

```
<skill-dir>/
├── SKILL.md
├── evals/
│   └── evals.json         # 테스트 케이스
├── agents/
│   ├── grader.md           # 채점 기준
│   ├── comparator.md       # 블라인드 비교 (optional)
│   └── analyzer.md         # 벤치마크 분석 (optional)
├── scripts/
│   ├── quick_validate.py   # frontmatter 검증
│   ├── aggregate_benchmark.py  # 벤치마크 집계
│   ├── run_eval.py         # 트리거 감지
│   └── run_loop.py         # description 최적화 루프
└── references/
    └── eval-guide.md       # 이 파일
```

### JSON 스키마 요약

| 파일 | 위치 | 용도 |
|------|------|------|
| `evals.json` | `evals/` | 테스트 프롬프트 + assertions |
| `eval_metadata.json` | 각 eval 디렉토리 | 개별 eval 메타 |
| `grading.json` | 각 run 디렉토리 | 채점 결과 |
| `timing.json` | 각 run 디렉토리 | 토큰/시간 |
| `benchmark.json` | iteration 디렉토리 | 집계 통계 |
| `feedback.json` | workspace 루트 | 사용자 피드백 |

---

**Based on**: [anthropics/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
**See also**: [agents/grader.md](../agents/grader.md) | [agents/comparator.md](../agents/comparator.md) | [agents/analyzer.md](../agents/analyzer.md)
