# CLAUDE.md

## Project Overview

**ccbuilder** — Claude Code 확장 기능(Skills, Hooks, Agents, Agent Teams, Ralph Loops) 빌더 플러그인.
33개 레퍼런스 가이드와 6개 공식 문서 요약을 포함하는 지식 베이스.

## Project Structure

```
skills/ccbuilder/
├── SKILL.md                     # 메인 스킬 파일 (500줄 미만 필수)
├── references/                  # 레퍼런스 가이드 (22개)
│   ├── official/                # Claude Code 공식 문서 요약 (6개)
│   └── github/                  # 커뮤니티 에코시스템 (5 docs + 11 submodules)
releases/                        # SKILL.md 버전 백업 (v{VERSION}_{YYYYMMDD}_SKILL.md)
.claude-plugin/                  # 플러그인 매니페스트 (plugin.json, marketplace.json)
.github/workflows/               # CI/CD 워크플로우
scripts/                         # 유틸리티 스크립트
evaluations/                     # 스킬 평가 프레임워크
```

## Key Rules

- **SKILL.md는 500줄 미만** 유지 필수
- **Semantic Versioning**: MAJOR.MINOR.PATCH (ccbuilder 자체 버전)
- **releases/ 백업**: 버전 변경 전 `releases/v{VERSION}_{YYYYMMDD}_SKILL.md`로 백업
- **CHANGELOG.md**: Keep a Changelog 형식 준수
- **한국어 콘텐츠**: 문서 내용은 한국어, 코드/기술 용어는 영어
- **파일 삭제 금지**: `deprecated/YYYYMMDD_설명/`으로 이동 (예외: tmp, log, cache)

## Version Sync

Claude Code 새 버전 릴리스 시 `auto-version-sync.yml` 워크플로우가:
1. SKILL.md를 releases/에 백업
2. Shell(sed)로 버전 번호 업데이트
3. Claude Code Action으로 CHANGELOG 분석 및 콘텐츠 업데이트
4. PR 자동 생성

## Code Review Criteria

PR 리뷰 시 확인 사항:
- SKILL.md 500줄 제한 준수
- Semantic Versioning 형식
- CHANGELOG.md에 실제 기능 목록 포함 (단순 "version updated" 불가)
- releases/에 이전 버전 백업 존재
- version-sync.md에 새 버전 추적 엔트리 추가
- Shell 스크립트의 커맨드 인젝션 위험 없음
- GitHub Actions 워크플로우의 시크릿 노출 없음
