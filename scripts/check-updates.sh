#!/bin/bash
#
# check-updates.sh - Claude Code 버전 업데이트 체크 스크립트
#
# 사용법:
#   ./check-updates.sh           # 기본 체크
#   ./check-updates.sh --verbose # 상세 출력
#   ./check-updates.sh --fetch   # 공식 문서 다운로드 포함
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_FILE="$SKILL_DIR/SKILL.md"
CHANGELOG_URL="https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
OFFICIAL_DOCS_DIR="$SKILL_DIR/references/official-docs"

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

VERBOSE=false
FETCH=false

# 인자 파싱
for arg in "$@"; do
  case $arg in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --fetch|-f)
      FETCH=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--verbose|-v] [--fetch|-f]"
      echo ""
      echo "Options:"
      echo "  --verbose, -v    Show detailed output"
      echo "  --fetch, -f      Download official documentation"
      exit 0
      ;;
  esac
done

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}       Claude Code Extension Builder - Update Checker       ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# 현재 스킬 버전 추출
CURRENT_VERSION=$(grep "Claude Code Version" "$SKILL_FILE" | grep -oE "v[0-9]+\.[0-9]+\.[0-9]+" | head -1 || echo "unknown")
echo -e "📌 Current Skill Version: ${GREEN}$CURRENT_VERSION${NC}"

# 공식 CHANGELOG에서 최신 버전 추출
echo -e "🔍 Fetching latest version from GitHub..."
TEMP_CHANGELOG=$(mktemp)
curl -s "$CHANGELOG_URL" -o "$TEMP_CHANGELOG" 2>/dev/null

if [ ! -s "$TEMP_CHANGELOG" ]; then
  echo -e "${RED}❌ Failed to fetch CHANGELOG from GitHub${NC}"
  rm -f "$TEMP_CHANGELOG"
  exit 1
fi

LATEST_VERSION=$(grep -m1 "^## [0-9]" "$TEMP_CHANGELOG" | sed 's/## //' | tr -d ' ')
echo -e "🌐 Latest Claude Code Version: ${GREEN}$LATEST_VERSION${NC}"
echo ""

# 버전 비교
CURRENT_CLEAN=$(echo "$CURRENT_VERSION" | sed 's/v//' | sed 's/+//')
LATEST_CLEAN=$(echo "$LATEST_VERSION" | sed 's/v//')

if [ "$CURRENT_CLEAN" = "$LATEST_CLEAN" ]; then
  echo -e "${GREEN}✅ Already up to date!${NC}"
  UPDATE_NEEDED=false
else
  echo -e "${YELLOW}⚠️  Update needed: $CURRENT_VERSION → v$LATEST_VERSION${NC}"
  UPDATE_NEEDED=true
fi

echo ""

# 상세 모드: 최근 변경사항 표시
if [ "$VERBOSE" = true ]; then
  echo -e "${BLUE}── Recent Changes ──────────────────────────────────────────${NC}"
  # 최근 3개 버전의 헤더 추출
  grep -E "^## [0-9]|^### " "$TEMP_CHANGELOG" | head -30
  echo ""
fi

# 공식 문서 다운로드
if [ "$FETCH" = true ]; then
  echo -e "${BLUE}── Downloading Official Docs ───────────────────────────────${NC}"
  mkdir -p "$OFFICIAL_DOCS_DIR"

  cp "$TEMP_CHANGELOG" "$OFFICIAL_DOCS_DIR/CHANGELOG.md"
  echo -e "  ✓ CHANGELOG.md"

  echo -e "${GREEN}✅ Official docs saved to: $OFFICIAL_DOCS_DIR${NC}"
  echo ""
fi

# 정리
rm -f "$TEMP_CHANGELOG"

# 업데이트 필요 시 안내
if [ "$UPDATE_NEEDED" = true ]; then
  echo -e "${BLUE}── Next Steps ──────────────────────────────────────────────${NC}"
  echo "1. Review: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
  echo "2. Update SKILL.md version header"
  echo "3. Update reference documents:"
  echo "   - references/skills-guide.md"
  echo "   - references/hooks-guide.md"
  echo "   - references/subagents-guide.md"
  echo "4. Update CHANGELOG.md"
  echo "5. Create release backup in releases/"
  echo ""
  echo "See: references/version-sync.md for detailed checklist"
fi

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

# 종료 코드: 업데이트 필요 시 1
if [ "$UPDATE_NEEDED" = true ]; then
  exit 1
else
  exit 0
fi
