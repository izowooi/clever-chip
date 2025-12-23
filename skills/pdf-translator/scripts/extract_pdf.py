#!/usr/bin/env python3
"""
PDF 텍스트 추출 스크립트
PDF 파일에서 텍스트를 추출하여 텍스트 파일로 저장합니다.
"""

import sys
import pdfplumber


def extract_text_from_pdf(input_path: str, output_path: str) -> None:
    """
    PDF 파일에서 텍스트를 추출하여 파일로 저장
    
    Args:
        input_path: 입력 PDF 파일 경로
        output_path: 출력 텍스트 파일 경로
    """
    extracted_text = []
    
    with pdfplumber.open(input_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"총 {total_pages} 페이지 처리 중...")
        
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                extracted_text.append(f"--- 페이지 {i} ---\n{text}\n")
            print(f"  페이지 {i}/{total_pages} 완료")
    
    # 결과 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(extracted_text))
    
    print(f"\n✅ 텍스트 추출 완료: {output_path}")


def main():
    if len(sys.argv) != 3:
        print("사용법: python3 extract_pdf.py <입력PDF> <출력TXT>")
        print("예시: python3 extract_pdf.py document.pdf output.txt")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    
    extract_text_from_pdf(input_pdf, output_txt)


if __name__ == "__main__":
    main()
