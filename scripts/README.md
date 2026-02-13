# Claude Code Extension Builder Scripts

이 디렉토리에는 Claude Code 확장 기능을 빠르게 생성하고 테스트하기 위한 유틸리티 스크립트가 포함되어 있습니다.

## 사용 가능한 스크립트

### 1. init-skill.sh

새로운 Skill을 초기화합니다.

**사용법:**
```bash
./scripts/init-skill.sh <skill-name>
```

**예제:**
```bash
./scripts/init-skill.sh my-awesome-skill
```

**생성 내용:**
- `.claude/skills/my-awesome-skill/SKILL.md` - 메인 skill 파일 (템플릿)
- `.claude/skills/my-awesome-skill/references/` - 참조 문서 디렉토리
- `.claude/skills/my-awesome-skill/scripts/` - 스크립트 디렉토리
- `skill-rules.json`에 자동 항목 추가 (jq 사용 가능 시)

---

### 2. init-agent.sh

새로운 Agent를 초기화합니다.

**사용법:**
```bash
./scripts/init-agent.sh <agent-name>
```

**예제:**
```bash
./scripts/init-agent.sh code-reviewer
```

**생성 내용:**
- `.claude/agents/code-reviewer.md` - Agent 정의 파일 (템플릿)

---

### 3. init-hook.sh

새로운 Hook을 초기화합니다.

**사용법:**
```bash
./scripts/init-hook.sh <hook-name> <hook-type>
```

**Hook 타입:**
- `UserPromptSubmit` - 사용자 프롬프트 전에 실행
- `PreToolUse` - 도구 실행 전에 실행
- `Stop` - 응답 완료 후 실행

**예제:**
```bash
./scripts/init-hook.sh my-validator UserPromptSubmit
./scripts/init-hook.sh file-guard PreToolUse
./scripts/init-hook.sh reminder Stop
```

**생성 내용:**
- `.claude/hooks/<hook-name>.ts` - Hook 구현 파일 (TypeScript 템플릿)

---

### 4. test-hook.sh

Hook을 테스트합니다.

**사용법:**
```bash
./scripts/test-hook.sh <hook-file> <hook-type> [test-case]
```

**Test cases:**
- `default` - 기본 테스트 입력 사용
- `custom` - 커스텀 입력 프롬프트

**예제:**
```bash
# 기본 테스트
./scripts/test-hook.sh .claude/hooks/my-validator.ts UserPromptSubmit

# 커스텀 테스트
./scripts/test-hook.sh .claude/hooks/file-guard.ts PreToolUse custom
```

**출력:**
- 테스트 입력 JSON
- Hook 실행 결과 (stdout/stderr)
- 종료 코드 및 해석

---

## 워크플로우 예제

### Skill 생성 워크플로우

```bash
# 1. Skill 초기화
./scripts/init-skill.sh pdf-processor

# 2. SKILL.md 편집
vim .claude/skills/pdf-processor/SKILL.md

# 3. skill-rules.json 확인
cat .claude/skills/skill-rules.json | jq .

# 4. 테스트 (UserPromptSubmit hook 필요)
echo '{"prompt":"process pdf"}' | npx tsx .claude/hooks/skill-activation-prompt.ts
```

### Agent 생성 워크플로우

```bash
# 1. Agent 초기화
./scripts/init-agent.sh security-auditor

# 2. Agent 파일 편집
vim .claude/agents/security-auditor.md

# 3. 테스트
# Claude에게: "security-auditor agent를 사용해서 코드를 검토해줘"
```

### Hook 생성 및 테스트 워크플로우

```bash
# 1. Hook 초기화
./scripts/init-hook.sh my-validator UserPromptSubmit

# 2. Hook 로직 구현
vim .claude/hooks/my-validator.ts

# 3. Hook 테스트
./scripts/test-hook.sh .claude/hooks/my-validator.ts UserPromptSubmit

# 4. settings.json에 등록
# {
#   "hooks": {
#     "UserPromptSubmit": ".claude/hooks/my-validator.ts"
#   }
# }
```

---

## 요구사항

### 필수
- `bash` - 스크립트 실행
- `node` / `npx` - TypeScript hook 실행 (tsx 사용)

### 선택
- `jq` - JSON 처리 (skill-rules.json 자동 업데이트)
  ```bash
  # macOS
  brew install jq

  # Ubuntu/Debian
  apt-get install jq
  ```

---

## 문제 해결

### 권한 오류

```bash
# 스크립트에 실행 권한 부여
chmod +x scripts/*.sh
```

### Hook 테스트 오류

```bash
# tsx 설치 확인
npx tsx --version

# 없으면 프로젝트에 설치
npm install -D tsx
```

### skill-rules.json 오류

```bash
# JSON 검증
jq . .claude/skills/skill-rules.json

# 파일이 없으면 생성
echo '{}' > .claude/skills/skill-rules.json
```

---

## 고급 사용법

### 배치 생성

여러 확장 기능을 한 번에 생성:

```bash
# 여러 skill 생성
for skill in pdf-processor image-editor video-converter; do
  ./scripts/init-skill.sh $skill
done

# 여러 agent 생성
for agent in code-reviewer security-auditor performance-analyzer; do
  ./scripts/init-agent.sh $agent
done
```

### 자동 테스트

모든 hook 자동 테스트:

```bash
for hook in .claude/hooks/*.ts; do
  echo "Testing: $hook"
  ./scripts/test-hook.sh "$hook" UserPromptSubmit default
done
```

---

## 참고 자료

- [Infrastructure Showcase](../references/infrastructure-showcase/)
- [Skill Developer Guide](../references/infrastructure-showcase/.claude/skills/skill-developer/SKILL.md)
- [Hook Examples](../references/infrastructure-showcase/.claude/hooks/)
- [Agent Examples](../references/infrastructure-showcase/.claude/agents/)
