# CLAUDE.md

## Project Overview

**ccbuilder** — Claude Code 확장 기능(Skills, Hooks, Agents, Agent Teams, Ralph Loops) 빌더 플러그인.
28개 레퍼런스 문서(17개 가이드 + 6개 공식 + 5개 에코시스템)를 포함하는 지식 베이스.

- **ccbuilder version**: 2.43.0 (Semantic Versioning)
- **Claude Code compatibility**: v2.1.178+
- **Last sync**: 2026-06-16

## Project Structure

```
CLAUDE.md                        # 이 파일 — 프로젝트 컨텍스트 (Claude Code Action 자동 참조)
CHANGELOG.md                     # Keep a Changelog 형식
README.md                        # 프로젝트 소개 + 배지 + 문서 링크
releases/                        # SKILL.md 버전 백업 (v{VERSION}_{YYYYMMDD}_SKILL.md)
skills/ccbuilder/
├── SKILL.md                     # 메인 스킬 파일 (500줄 미만 필수)
├── references/                  # 레퍼런스 가이드 (17개)
│   ├── official/                # Claude Code 공식 문서 요약 (6개)
│   ├── github/                  # 커뮤니티 에코시스템 (5 docs + 13 submodules)
│   └── version-sync.md          # 버전 동기화 추적 (헤더 메타데이터 + 버전별 변경 사항)
.claude-plugin/                  # 플러그인 매니페스트 (plugin.json, marketplace.json)
.github/workflows/
├── auto-version-sync.yml        # Claude Code 새 버전 자동 동기화 (daily cron)
└── claude-review.yml            # PR 자동 리뷰 + @claude 멘션 응답
scripts/                         # 유틸리티 스크립트
evaluations/                     # 스킬 평가 프레임워크
```

## Version Management

### 두 가지 버전 체계
| 버전 | 예시 | 의미 |
|------|------|------|
| **ccbuilder version** | 2.12.0 | 이 플러그인 자체 버전 (Semantic Versioning) |
| **Claude Code version** | v2.1.63 | 호환 대상 Claude Code CLI 버전 |

### 버전 동기화 시 업데이트 대상 파일
| 파일 | 업데이트 내용 |
|------|--------------|
| `skills/ccbuilder/SKILL.md` | Version 헤더, Last Updated, Claude Code 호환 버전, 핵심 변경 사항 |
| `CHANGELOG.md` | 새 엔트리 (실제 기능 목록 포함) |
| `.claude-plugin/plugin.json` | `"version"` 필드 |
| `.claude-plugin/marketplace.json` | `"version"` 필드 |
| `README.md` | 배지(version, Claude Code), 날짜, Hook 이벤트 수 |
| `releases/` | 이전 SKILL.md 백업 (`v{VERSION}_{YYYYMMDD}_SKILL.md`) |
| `references/version-sync.md` | 헤더 메타데이터 + 새 버전 추적 엔트리 |
| `CLAUDE.md` | ccbuilder version, Claude Code compatibility, Last sync |

## Key Rules

- **SKILL.md는 500줄 미만** 유지 필수
- **Semantic Versioning**: MAJOR (breaking), MINOR (새 기능), PATCH (버그 수정)
- **releases/ 백업**: 버전 변경 전 이전 SKILL.md를 반드시 백업
- **CHANGELOG.md**: Keep a Changelog 형식, 실제 기능 목록 기재 (단순 "version updated" 불가)
- **한국어 콘텐츠**: 문서 본문은 한국어, 코드/기술 용어는 영어
- **파일 삭제 금지**: `deprecated/YYYYMMDD_설명/`으로 이동 (예외: tmp, log, cache)
- **Hook 이벤트 수**: 현재 16개 — 파일 간 일관성 유지 필수

## CI/CD Workflows

### auto-version-sync.yml
Claude Code 새 버전 릴리스 시 자동 실행 (daily cron + manual dispatch):
1. SKILL.md를 releases/에 백업
2. Shell(sed)로 버전 번호 업데이트 (SKILL.md, plugin.json, marketplace.json, README, version-sync.md 헤더, CLAUDE.md)
3. Claude Code Action으로 CHANGELOG 분석 및 콘텐츠 업데이트
4. PR 자동 생성

### claude-review.yml
PR 리뷰 자동화:
- **auto-review**: PR 생성/업데이트 시 자동 리뷰
- **mention-response**: `@claude` 멘션 시 응답

## Code Review Criteria

PR 리뷰 시 확인 사항:
- SKILL.md 500줄 제한 준수
- Semantic Versioning 형식
- CHANGELOG.md에 실제 기능 목록 포함
- releases/에 이전 버전 백업 존재
- version-sync.md 헤더 메타데이터와 추적 엔트리 모두 업데이트 확인
- README.md 배지/날짜/Hook 이벤트 수 최신 상태
- CLAUDE.md 버전 정보 최신 상태
- Shell 스크립트의 커맨드 인젝션 위험 없음
- GitHub Actions 워크플로우의 시크릿 노출 없음
- 파일 간 버전 번호/Hook 이벤트 수 등 일관성 유지
