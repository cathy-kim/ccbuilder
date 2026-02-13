#!/bin/bash

# Claude Code Agent 초기화 스크립트
# Usage: ./init-agent.sh <agent-name>

set -e

AGENT_NAME="$1"

if [ -z "$AGENT_NAME" ]; then
  echo "Usage: $0 <agent-name>"
  echo "Example: $0 code-reviewer"
  exit 1
fi

# Agent 파일 생성
AGENT_FILE=".claude/agents/$AGENT_NAME.md"

if [ -f "$AGENT_FILE" ]; then
  echo "Error: Agent file already exists: $AGENT_FILE"
  exit 1
fi

# .claude/agents 디렉토리 생성
mkdir -p ".claude/agents"

echo "Creating agent: $AGENT_NAME"
echo "File: $AGENT_FILE"

# 제목 생성 (하이픈을 공백으로, 첫 글자 대문자)
AGENT_TITLE=$(echo $AGENT_NAME | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')

# Agent 파일 생성
cat > "$AGENT_FILE" << EOF
---
name: $AGENT_NAME
description: "[TODO: 이 agent의 역할과 사용 시점 설명]"
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
permissionMode: default
---

# $AGENT_TITLE

## 목적

[TODO: 이 agent가 수행하는 작업]

## 역할

이 agent는 다음을 담당합니다:
- [TODO: 책임 1]
- [TODO: 책임 2]
- [TODO: 책임 3]

## 사용 시점

다음과 같은 상황에서 이 agent를 사용합니다:
- [TODO: 시나리오 1]
- [TODO: 시나리오 2]
- [TODO: 시나리오 3]

---

## 지시사항

다음 단계를 순서대로 수행합니다:

### 1. 초기 분석

[TODO: 초기 분석 수행 방법]

### 2. 작업 실행

[TODO: 주요 작업 실행 방법]

### 3. 결과 검증

[TODO: 결과 검증 방법]

### 4. 보고서 생성

[TODO: 보고서 생성 방법]

---

## 사용 가능한 도구

이 agent는 다음 도구를 사용할 수 있습니다:

**파일 작업:**
- \`Read\`: 파일 읽기
- \`Write\`: 새 파일 생성
- \`Edit\`: 기존 파일 수정
- \`Glob\`: 파일 패턴 검색
- \`Grep\`: 내용 검색

**시스템 작업:**
- \`Bash\`: 명령 실행

**웹 작업 (필요시):**
- \`WebSearch\`: 웹 검색
- \`WebFetch\`: 웹 페이지 가져오기

---

## 예상 출력

Agent는 다음 형식의 종합 보고서를 반환합니다:

\`\`\`markdown
## 분석 결과

[분석 결과 요약]

## 발견 사항

### 주요 발견
- [발견 1]
- [발견 2]

### 세부 사항
[상세 내용]

## 권장 사항

1. [권장사항 1]
2. [권장사항 2]
3. [권장사항 3]

## 다음 단계

- [다음 단계 1]
- [다음 단계 2]
\`\`\`

---

## 예제

### 사용법

\`\`\`
User: "$AGENT_NAME agent를 사용해서 [작업]해줘"
\`\`\`

### 예상 시나리오

**시나리오 1:**
\`\`\`
User: "$AGENT_NAME agent를 사용해서 src/ 디렉토리를 분석해줘"
\`\`\`

**시나리오 2:**
\`\`\`
User: "$AGENT_NAME agent를 사용해서 최근 변경사항을 리뷰해줘"
\`\`\`

---

## 제약사항

- [TODO: 제약사항 1]
- [TODO: 제약사항 2]

## 참고사항

- [TODO: 참고사항 1]
- [TODO: 참고사항 2]
EOF

echo ""
echo "✅ Agent created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $AGENT_FILE"
echo "2. Complete all [TODO] sections"
echo "3. Add specific instructions for autonomous execution"
echo "4. Define expected output format"
echo "5. Test with: \"$AGENT_NAME agent를 사용해서 [작업]해줘\""
