#!/bin/bash

# Claude Code Skill 초기화 스크립트
# Usage: ./init-skill.sh <skill-name>

set -e

SKILL_NAME="$1"

if [ -z "$SKILL_NAME" ]; then
  echo "Usage: $0 <skill-name>"
  echo "Example: $0 my-awesome-skill"
  exit 1
fi

# Skill 디렉토리 생성
SKILL_DIR=".claude/skills/$SKILL_NAME"

if [ -d "$SKILL_DIR" ]; then
  echo "Error: Skill directory already exists: $SKILL_DIR"
  exit 1
fi

echo "Creating skill: $SKILL_NAME"
echo "Directory: $SKILL_DIR"

# 디렉토리 구조 생성
mkdir -p "$SKILL_DIR"
mkdir -p "$SKILL_DIR/references"
mkdir -p "$SKILL_DIR/scripts"

# SKILL.md 생성
cat > "$SKILL_DIR/SKILL.md" << 'EOF'
---
name: SKILL_NAME_PLACEHOLDER
description: [TODO: 트리거 키워드와 사용 시점을 포함한 상세 설명 (최대 1024자)]
---

# SKILL_TITLE_PLACEHOLDER

## 목적

[TODO: 이 skill이 해결하는 문제]

## 사용 시점

다음을 언급할 때 자동 활성화됩니다:
- [TODO: 시나리오 1]
- [TODO: 시나리오 2]
- [TODO: 시나리오 3]

---

## 빠른 시작

[TODO: 기본 사용법]

---

## 핵심 가이드

[TODO: 실제 구현 가이드, 예제, 패턴]

---

## 참조 문서

상세 정보는 다음을 참조:
- [Advanced Guide](references/advanced-guide.md)

---

**Skill 상태**: DRAFT
**줄 수**: < 500 (500-line rule 준수)
**Progressive Disclosure**: 상세 정보를 위한 references 활용
EOF

# Placeholder 치환
sed -i.bak "s/SKILL_NAME_PLACEHOLDER/$SKILL_NAME/g" "$SKILL_DIR/SKILL.md"
sed -i.bak "s/SKILL_TITLE_PLACEHOLDER/$(echo $SKILL_NAME | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')/g" "$SKILL_DIR/SKILL.md"
rm "$SKILL_DIR/SKILL.md.bak"

# Reference 예제 생성
cat > "$SKILL_DIR/references/advanced-guide.md" << 'EOF'
# Advanced Guide

## 고급 패턴

[TODO: 상세 가이드]

## 예제

[TODO: 실제 예제]

## 문제 해결

[TODO: 일반적인 문제와 해결책]
EOF

# skill-rules.json에 항목 추가
SKILL_RULES_FILE=".claude/skills/skill-rules.json"

if [ ! -f "$SKILL_RULES_FILE" ]; then
  echo "{}" > "$SKILL_RULES_FILE"
fi

# jq를 사용하여 skill-rules.json 업데이트
if command -v jq &> /dev/null; then
  TEMP_FILE=$(mktemp)
  jq ". + {\"$SKILL_NAME\": {\"type\": \"domain\", \"enforcement\": \"suggest\", \"priority\": \"medium\", \"promptTriggers\": {\"keywords\": [\"$SKILL_NAME\"], \"intentPatterns\": []}}}" "$SKILL_RULES_FILE" > "$TEMP_FILE"
  mv "$TEMP_FILE" "$SKILL_RULES_FILE"
  echo "✅ Updated skill-rules.json"
else
  echo "⚠️  jq not found. Please manually add to skill-rules.json:"
  echo ""
  echo "  \"$SKILL_NAME\": {"
  echo "    \"type\": \"domain\","
  echo "    \"enforcement\": \"suggest\","
  echo "    \"priority\": \"medium\","
  echo "    \"promptTriggers\": {"
  echo "      \"keywords\": [\"$SKILL_NAME\"],"
  echo "      \"intentPatterns\": []"
  echo "    }"
  echo "  }"
fi

echo ""
echo "✅ Skill created successfully!"
echo ""
echo "Next steps:"
echo "1. Edit $SKILL_DIR/SKILL.md"
echo "2. Update description and keywords in YAML frontmatter"
echo "3. Add content to SKILL.md (keep under 500 lines)"
echo "4. Add detailed content to references/ files"
echo "5. Test with: echo '{\"prompt\":\"test $SKILL_NAME\"}' | npx tsx .claude/hooks/skill-activation-prompt.ts"
