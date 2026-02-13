# Claude Code 버전 동기화 가이드

> 이 스킬을 최신 Claude Code 버전과 동기화하기 위한 가이드

**최종 동기화**: 2026-02-11
**현재 지원 버전**: v2.1.39+

---

## 자동화 설정

### GitHub Actions (권장)

`.github/workflows/sync-claude-code-docs.yml` 워크플로우가 매일 자동 실행됩니다:

- **스케줄**: 매일 오전 9시 (UTC) = 한국시간 오후 6시
- **동작**: 새 버전 감지 시 GitHub Issue 자동 생성
- **수동 트리거**: Actions 탭에서 "Run workflow" 가능

### 알림 받기

1. GitHub Issue 알림 활성화
2. (선택) Slack 웹훅 설정 (워크플로우 파일 참조)

---

## 주간 업데이트 체크리스트

### 1. 공식 소스 확인

- [ ] [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [ ] [Skills 문서](https://code.claude.com/docs/en/skills)
- [ ] [Hooks 문서](https://code.claude.com/docs/en/hooks)
- [ ] [Subagents 문서](https://code.claude.com/docs/en/sub-agents)
- [ ] [Slash Commands 문서](https://code.claude.com/docs/en/slash-commands)
- [ ] [MCP 문서](https://code.claude.com/docs/en/mcp)
- [ ] [Memory 문서](https://code.claude.com/docs/en/memory)

### 2. 변경 사항 분석

| 확인 항목 | 체크 |
|----------|------|
| 새로운 Hook 이벤트 | [ ] |
| 새로운 frontmatter 필드 | [ ] |
| Deprecated 기능 | [ ] |
| 새로운 내장 Subagent | [ ] |
| 새로운 도구/명령어 | [ ] |
| 버그 수정 영향 | [ ] |

### 3. 업데이트 적용

```bash
# 1. 버전 백업 생성
cp SKILL.md releases/v$(date +%Y%m%d)_SKILL.md

# 2. SKILL.md 버전 헤더 업데이트
# **Claude Code Version**: vX.X.X+

# 3. 관련 참조 문서 업데이트
# - references/skills-guide.md
# - references/hooks-guide.md
# - references/subagents-guide.md

# 4. CHANGELOG.md 기록

# 5. 테스트
```

### 4. 검증

- [ ] SKILL.md < 500줄 유지
- [ ] 모든 링크 유효성 확인
- [ ] 예시 코드 검증
- [ ] frontmatter 옵션 테스트

---

## 버전별 주요 변경 사항 추적

### v2.1.39 (2026-02-11 동기화)

**새로운 기능:**
- PDF 페이지 파라미터 지원
- `/debug` 명령어
- PR 리뷰 상태 표시기
- 68% 메모리 감소 (`--resume`)
- Task 의존성 관리 시스템
- 커스텀 키보드 단축키

**Skills 변경:**
- `disable-model-invocation` 필드 추가
- Skill scopes 계층 (Enterprise > Personal > Project > Plugin)

**Hooks 변경:**
- Setup 이벤트 상세 스키마
- Hook output의 `decision` 필드

### v2.1.30 (이전)

- SubagentStart, PostToolUseFailure 이벤트
- prompt, agent Hook 타입
- async Hook 지원

---

## 긴급 업데이트 절차

Breaking Change 감지 시:

1. **즉시 Issue 생성**
   ```bash
   gh issue create --title "[URGENT] Claude Code Breaking Change" \
     --body "Breaking change detected in vX.X.X" \
     --label "urgent,breaking-change"
   ```

2. **SKILL.md 경고 추가**
   ```markdown
   > ⚠️ **주의**: v2.X.X에서 XXX가 deprecated되었습니다.
   ```

3. **마이그레이션 가이드 작성**
   - `references/migration-vX.md` 생성

---

## 자동화 스크립트

### 로컬 버전 체크

```bash
# scripts/check-updates.sh 실행
scripts/check-updates.sh
```

### 수동 동기화

```bash
# 공식 CHANGELOG 다운로드
curl -s https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md \
  -o references/official-docs/CHANGELOG.md

# 버전 비교
LATEST=$(grep -m1 "^## [0-9]" references/official-docs/CHANGELOG.md | sed 's/## //')
CURRENT=$(grep "Claude Code Version" SKILL.md | grep -oE "v[0-9]+\.[0-9]+\.[0-9]+")
echo "Latest: $LATEST, Current: $CURRENT"
```

---

## 관련 파일

| 파일 | 용도 |
|------|------|
| `SKILL.md` | 메인 스킬 파일 |
| `CHANGELOG.md` | 스킬 변경 이력 |
| `scripts/check-updates.sh` | 로컬 버전 체크 |
| `.github/workflows/sync-claude-code-docs.yml` | 자동 동기화 |
| `references/official-docs/` | 공식 문서 백업 |

---

*이 가이드는 스킬 유지보수의 핵심 문서입니다.*
