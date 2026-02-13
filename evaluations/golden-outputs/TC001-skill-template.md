---
name: pdf-analyzer
description: Helps analyze PDF documents and extract key information using PDF parsing tools and providing structured output.
---

# PDF Analyzer

## 목적

PDF 문서를 분석하고 핵심 정보를 추출하여 구조화된 결과를 제공합니다.

## 사용 시점

- PDF 문서에서 텍스트, 표, 이미지를 추출해야 할 때
- 대량의 PDF 파일을 일괄 처리해야 할 때
- PDF 메타데이터나 구조 정보가 필요할 때

## 빠른 시작

```bash
# Install dependencies
npm install pdf-parse pdf-lib

# Basic usage
claude --skill pdf-analyzer --prompt "Analyze contract.pdf and extract key terms"
```

## 핵심 기능

### 1. 텍스트 추출
- 전체 문서 텍스트 추출
- 페이지별 텍스트 분리
- 폰트 및 스타일 정보 유지

### 2. 구조화 분석
- 제목, 소제목 자동 인식
- 표(Table) 데이터 추출
- 목차(TOC) 생성

### 3. 메타데이터
- 작성자, 생성일, 수정일
- 페이지 수, 파일 크기
- PDF 버전 정보

## 도구 사용

### PDF Parse
```typescript
import pdfParse from 'pdf-parse';

const dataBuffer = fs.readFileSync('document.pdf');
const data = await pdfParse(dataBuffer);

console.log(data.text);      // 전체 텍스트
console.log(data.numpages);   // 페이지 수
console.log(data.info);       // 메타데이터
```

## 출력 형식

```json
{
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "pages": 10
  },
  "content": {
    "text": "Extracted text...",
    "tables": [...],
    "images": [...]
  },
  "summary": "Key points extracted from the document..."
}
```

## 제약사항

- 암호화된 PDF는 비밀번호 필요
- 스캔된 이미지 PDF는 OCR 필요 (별도 처리)
- 매우 큰 파일(>100MB)은 메모리 제한 고려

## Advanced Topics

For detailed implementation guides:
- [Advanced Parsing Techniques](references/advanced-parsing.md)
- [OCR Integration Guide](references/ocr-integration.md)
- [Batch Processing](references/batch-processing.md)

---

**Status**: PRODUCTION-READY
**Last Updated**: 2025-12-23
