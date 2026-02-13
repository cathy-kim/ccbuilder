# Claude Code Extension Builder - Evaluation System

## 목적

ccbuilder 스킬의 품질과 정확성을 검증하기 위한 자동화된 평가 시스템입니다.

## 구조

```
evaluations/
├── test-cases.json           # 테스트 케이스 정의
├── golden-outputs/           # 예상 출력 (정답)
│   ├── TC001-skill-template.md
│   ├── TC002-agent-template.md
│   └── ...
├── eval-results/             # 평가 결과 저장
│   ├── {timestamp}-evaluation.json
│   └── {timestamp}-evaluation.md
├── run_evaluation.py         # 평가 실행 스크립트
└── README.md                 # 이 파일
```

## 테스트 케이스

| ID | Category | Priority | Description |
|----|----------|----------|-------------|
| TC001 | skill-creation | P0 | Create a basic skill with minimal configuration |
| TC002 | agent-creation | P0 | Create an agent with routing configuration |
| TC003 | hook-creation | P1 | Create a validation hook |
| TC004 | command-creation | P1 | Create a slash command |
| TC005 | best-practices | P0 | Verify progressive disclosure |

## 실행 방법

### 1. 전체 테스트 실행

```bash
cd .claude
python3 skills/ccbuilder/evaluations/run_evaluation.py
```

선택 옵션:
1. Run all tests (모든 테스트)
2. Run P0 tests only (핵심 테스트만)
3. Run specific test (특정 테스트)

### 2. 단일 테스트 실행 (예시)

```bash
# TC001: Skill 생성 테스트
python3 skills/ccbuilder/evaluations/run_evaluation.py

# 프롬프트에서 '3' 선택 후 'TC001' 입력
```

### 3. 수동 테스트 (권장)

가장 간단한 방법:

```bash
# 1. Claude Code 실행
claude

# 2. 스킬 활성화
/skill ccbuilder

# 3. 테스트 프롬프트 실행
"Create a new skill called 'pdf-analyzer' that helps analyze PDF documents..."

# 4. 결과 확인
ls -la skills/pdf-analyzer/
cat skills/pdf-analyzer/SKILL.md
```

## 평가 기준

### TC001: Skill 생성

**입력 프롬프트:**
```
Create a new skill called 'pdf-analyzer' that helps analyze PDF documents
and extract key information. The skill should use PDF parsing tools and
provide structured output.
```

**기대 결과:**
- ✅ `skills/pdf-analyzer/SKILL.md` 생성
- ✅ YAML frontmatter 존재
- ✅ `name: pdf-analyzer` 필드 존재
- ✅ `description` 필드에 "PDF", "analyze" 키워드 포함
- ✅ 500줄 이하
- ✅ 필수 섹션 존재: "목적", "사용 시점", "빠른 시작"
- ✅ `skills/pdf-analyzer/references/` 디렉토리 생성

**Golden Output과 비교:**
- 구조적 유사도 확인
- 섹션 제목 일치도
- 길이 비율

### TC002: Agent 생성

**입력 프롬프트:**
```
Create a frontend code reviewer agent that reviews React/TypeScript code.
When it encounters backend API issues, it should route to the backend-reviewer agent.
```

**기대 결과:**
- ✅ `agents/frontend-code-reviewer.md` 생성
- ✅ "## Role" 섹션 존재
- ✅ "## Responsibilities" 섹션 존재
- ✅ "## Routing" 섹션 존재
- ✅ `backend-reviewer` 언급됨

## 결과 해석

### JSON 결과 (`eval-results/{timestamp}-evaluation.json`)

```json
{
  "timestamp": "2025-12-23T06:45:00",
  "total_tests": 5,
  "passed": 4,
  "failed": 0,
  "partial": 1,
  "results": [
    {
      "test_id": "TC001",
      "status": "PASS",
      "checks": {
        "files_created": {...},
        "skill_structure": {...},
        "golden_comparison": {
          "similarity_score": 0.85
        }
      }
    }
  ]
}
```

### Markdown 리포트 (`eval-results/{timestamp}-evaluation.md`)

사람이 읽기 쉬운 형식으로 결과 요약 제공.

## 성공 기준

**전체 통과 (100%):**
- 모든 P0 테스트 PASS
- P1 테스트 80% 이상 PASS

**부분 통과 (80%):**
- P0 테스트 80% 이상 PASS
- 구조적 요구사항 충족

**실패 (< 80%):**
- P0 테스트 실패
- 필수 파일 미생성

## 문제 해결

### "File not found" 에러

```bash
# 작업 디렉토리 확인
pwd
# → .claude 여야 함

# 스킬 디렉토리 확인
ls -la skills/pdf-analyzer/
```

### Golden Output과 차이가 큼

- 예상됨: Claude의 출력은 매번 약간씩 다름
- **구조적 유사도 > 70%**면 PASS
- 내용이 의미적으로 올바른지 수동 확인 필요

### 테스트 재실행

```bash
# 이전 결과 정리
rm -rf skills/pdf-analyzer
rm -rf agents/frontend-code-reviewer.md

# 재실행
python3 skills/ccbuilder/evaluations/run_evaluation.py
```

## 유지보수

### Golden Output 업데이트

스킬 로직이 변경되면 Golden Output도 업데이트:

```bash
# 1. 새로운 출력 생성
claude --skill ccbuilder --prompt "..."

# 2. 검토 후 Golden Output으로 저장
cp skills/pdf-analyzer/SKILL.md \
   skills/ccbuilder/evaluations/golden-outputs/TC001-skill-template.md
```

### 새 테스트 케이스 추가

1. `test-cases.json`에 새 테스트 추가
2. Golden Output 생성
3. 테스트 실행 및 검증

## ROI 분석

**투자:**
- 초기 설정: 2-3시간
- 테스트 케이스 작성: 30분/케이스
- Golden Output 생성: 15분/케이스
- **총 초기 투자: ~5시간**

**효과:**
- 스킬 변경 시 regression 자동 감지
- 품질 저하 조기 발견
- 리팩토링 안전성 확보
- **연간 절약 시간: ~20-30시간**

## 다음 단계

1. ✅ TC001 수동 실행 및 검증
2. ✅ TC002 수동 실행 및 검증
3. ⏸️ 나머지 테스트 케이스 추가
4. ⏸️ CI/CD 통합 (선택)
5. ⏸️ 다른 P0 스킬에 확장

---

**Last Updated**: 2025-12-23
**Status**: ACTIVE
