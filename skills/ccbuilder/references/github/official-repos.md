# T1 - Anthropic Official Repositories

> Anthropic 공식 레포지토리. 구현의 정답 기준.

**Last Updated**: 2026-02-11

---

## 1. anthropics/skills

- **URL**: https://github.com/anthropics/skills
- **Stars**: ~67,900
- **제공**: 공식 Agent Skills (SKILL.md + 스크립트 + 리소스)

### 주요 Skills

| 카테고리 | Skills |
|----------|--------|
| 문서 처리 | DOCX, PDF, PPTX, XLSX (Python 구현) |
| 디자인 | Algorithmic Art (p5.js), Canvas Design, Slack GIF Creator |
| 개발 | Webapp Testing (Playwright), MCP Builder, Frontend Design |
| 엔터프라이즈 | Brand Guidelines, Internal Comms |
| 메타 | Skill Creator (대화형 Skill 생성기) |

### 학습 포인트

1. **YAML Frontmatter 스키마** - `name`, `description` 필수 필드의 정확한 사용법
2. **Progressive Disclosure** - 메타데이터 → 본문 → 리소스 3단계 로딩
3. **Supporting Files 구조** - templates/, scripts/, resources/ 배치 패턴
4. **Template 디렉토리** - 새 Skill 생성 시 참조할 표준 구조
5. **Plugin 설치** - `/plugin install example-skills@anthropic-agent-skills`

### 유즈 케이스

- **"공식 Skill은 어떻게 만들어?"** → 이 레포의 아무 Skill이나 참조
- **"문서 처리 자동화"** → DOCX/PDF/PPTX/XLSX Skills 참조
- **"Skill Creator로 새 Skill 만들기"** → skill-creator/ 참조

---

## 2. anthropics/claude-code

- **URL**: https://github.com/anthropics/claude-code
- **Stars**: ~66,100
- **제공**: 공식 CLI, Hook 예시, Plugin 구조, CHANGELOG

### 핵심 참조 경로

| 경로 | 내용 |
|------|------|
| `examples/hooks/` | Hook 구현 레퍼런스 (bash_command_validator 등) |
| `plugins/` | Plugin 구조 가이드 + README |
| `.claude-plugin/marketplace.json` | 공식 마켓플레이스 레지스트리 |
| `.claude/commands/` | Slash Command 예시 |
| `CHANGELOG.md` | 버전별 변경 사항 (Breaking Changes 확인 필수) |

### 학습 포인트

1. **Plugin 구조 표준** - `.claude-plugin/plugin.json`, `commands/`, `agents/`, `skills/`
2. **Hook 자동 로드** - Plugin 설치 시 hooks 폴더 자동 인식 (plugin.json 선언 불필요)
3. **CHANGELOG 추적** - Breaking Changes, Deprecation 최신 정보

### 유즈 케이스

- **"Hook 어떻게 만들어?"** → `examples/hooks/` 참조
- **"Plugin 구조가 뭐야?"** → `plugins/README.md` 참조
- **"최신 변경 사항 확인"** → `CHANGELOG.md` 참조

---

## 3. anthropics/claude-plugins-official

- **URL**: https://github.com/anthropics/claude-plugins-official
- **Stars**: ~7,200
- **제공**: 공식 관리 Plugin 디렉토리

### 구조

```
plugins/          → Anthropic 내부 제작
external_plugins/ → 서드파티 파트너 (품질 심사 통과)
```

### 학습 포인트

1. **Plugin 품질 기준** - 승인에 필요한 보안/품질 요건
2. **레퍼런스 구현** - `/plugins/example-plugin` 표준 예시
3. **제출 프로세스** - 외부 플러그인 등록 절차

### 유즈 케이스

- **"Plugin 마켓에 등록하려면?"** → 제출 가이드 참조
- **"승인된 Plugin 예시"** → example-plugin 참조

---

## 4. anthropics/claude-cookbooks

- **URL**: https://github.com/anthropics/claude-cookbooks
- **Stars**: -
- **제공**: Claude API 활용 패턴 (Skills보다는 API 레벨)

### 유즈 케이스

- **"Agent SDK 예시"** → agent-sdk 관련 쿡북 참조
- **"Tool Use 패턴"** → tool-use 예시 참조

---

## 5. anthropics/claude-code-action

- **URL**: https://github.com/anthropics/claude-code-action
- **Stars**: -
- **제공**: GitHub Actions에서 Claude Code 실행

### 유즈 케이스

- **"CI/CD에서 Claude 실행"** → Action 설정 참조
- **"PR 자동 리뷰"** → 워크플로우 예시 참조
