---
name: pdf-translator
description: PDF 문서를 한국어로 번역하여 Markdown 파일로 출력하는 skill. 사용자가 "PDF 번역", "PDF를 한국어로", "문서 번역해줘", "이 PDF 번역" 등을 요청할 때 사용. 영어, 일본어, 중국어 등 다양한 언어의 PDF를 한국어 Markdown으로 변환.
---

# PDF Translator

PDF 문서에서 텍스트를 추출하고 한국어로 번역하여 Markdown 파일로 저장하는 스킬.

## 워크플로우

1. **텍스트 추출**: `scripts/extract_pdf.py` 실행
2. **번역**: 추출된 텍스트를 한국어로 번역 (Claude가 직접 수행)
3. **Markdown 저장**: 번역된 내용을 `.md` 파일로 저장

## 사용법

### Step 1: PDF 텍스트 추출

```bash
python3 scripts/extract_pdf.py /path/to/input.pdf /path/to/output.txt
```

### Step 2: 번역 및 Markdown 작성

추출된 텍스트를 읽고 한국어로 번역하여 Markdown 파일 생성.

## 번역 가이드라인

### 전문 용어 처리

- **기술 용어**: 원어 유지 (예: API, SDK, Framework, Class, Method)
- **코드**: 절대 번역하지 않음 (변수명, 함수명, 코드 블록 모두 원본 유지)
- **주석만 번역**: 코드 내 주석은 한국어로 번역

### Markdown 구조화

```markdown
# 제목 (번역)

## 섹션 제목 (번역)

본문 내용 (번역)

```code
// 코드는 원본 유지
// 주석만 한국어로
```
```

### 품질 기준

- 자연스러운 한국어 문장
- 원문의 의미와 뉘앙스 유지
- 기술 문서의 정확성 보장
