#!/usr/bin/env python3
"""
게임 스크린샷 배경 제거 스크립트

기능:
1. 격자무늬/단색 배경 제거 (투명화)
2. 불필요한 여백 자동 제거 (auto-crop)
3. 지정 크기로 스케일링

Usage:
    python remove_background.py <input> <output> [options]
    
Options:
    --width, -w       목표 너비 (픽셀)
    --height, -h      목표 높이 (픽셀)
    --saturation, -s  채도 임계값 (0.0~1.0, 기본값: 0.15)
    --padding, -p     크롭 후 여백 (픽셀, 기본값: 0)
    --no-crop         자동 크롭 비활성화
"""

import argparse
from pathlib import Path
from PIL import Image
import numpy as np


def remove_low_saturation_background(
    img: Image.Image,
    saturation_threshold: float = 0.15
) -> Image.Image:
    """
    채도가 낮은 픽셀(회색조/무채색)을 투명하게 변환
    
    격자무늬 배경은 대부분 회색/흰색 계열이므로 채도가 낮음.
    게임 아이템/캐릭터는 일반적으로 채도가 높음.
    
    Args:
        img: 입력 이미지 (RGBA로 변환됨)
        saturation_threshold: 이 값 미만의 채도를 가진 픽셀을 투명하게 (0.0~1.0)
    
    Returns:
        배경이 투명해진 RGBA 이미지
    """
    img = img.convert('RGBA')
    arr = np.array(img, dtype=np.float32)
    
    # RGB 채널 추출
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # Saturation 계산 (HSV의 S 값)
    max_rgb = np.maximum(np.maximum(r, g), b)
    min_rgb = np.minimum(np.minimum(r, g), b)
    delta = max_rgb - min_rgb
    
    # max가 0이면 saturation도 0
    saturation = np.where(max_rgb > 0, delta / max_rgb, 0)
    
    # 채도가 임계값 미만인 픽셀을 투명하게
    alpha = arr[:, :, 3].copy()
    alpha[saturation < saturation_threshold] = 0
    arr[:, :, 3] = alpha
    
    return Image.fromarray(arr.astype(np.uint8), 'RGBA')


def auto_crop(img: Image.Image, padding: int = 0) -> Image.Image:
    """
    투명하지 않은 픽셀 기준으로 이미지 자동 크롭
    
    Args:
        img: RGBA 이미지
        padding: 크롭 후 추가할 여백 (픽셀)
    
    Returns:
        크롭된 이미지
    """
    arr = np.array(img)
    alpha = arr[:, :, 3]
    
    # 투명하지 않은 픽셀 위치 찾기
    non_transparent = np.argwhere(alpha > 0)
    
    if len(non_transparent) == 0:
        # 모든 픽셀이 투명한 경우 원본 반환
        return img
    
    # Bounding box 계산
    y_min, x_min = non_transparent.min(axis=0)
    y_max, x_max = non_transparent.max(axis=0)
    
    # Padding 적용
    height, width = arr.shape[:2]
    y_min = max(0, y_min - padding)
    x_min = max(0, x_min - padding)
    y_max = min(height - 1, y_max + padding)
    x_max = min(width - 1, x_max + padding)
    
    return img.crop((x_min, y_min, x_max + 1, y_max + 1))


def resize_image(
    img: Image.Image,
    width: int = None,
    height: int = None,
    keep_aspect: bool = True
) -> Image.Image:
    """
    이미지 크기 조정
    
    Args:
        img: 입력 이미지
        width: 목표 너비 (None이면 비율에 따라 계산)
        height: 목표 높이 (None이면 비율에 따라 계산)
        keep_aspect: True면 비율 유지, False면 강제 스트레치
    
    Returns:
        리사이즈된 이미지
    """
    if width is None and height is None:
        return img
    
    orig_w, orig_h = img.size
    
    if keep_aspect:
        if width and height:
            # 둘 다 지정: 비율 유지하며 지정 크기에 맞춤
            ratio = min(width / orig_w, height / orig_h)
        elif width:
            ratio = width / orig_w
        else:
            ratio = height / orig_h
        
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
    else:
        new_w = width or orig_w
        new_h = height or orig_h
    
    return img.resize((new_w, new_h), Image.Resampling.LANCZOS)


def process_image(
    input_path: str,
    output_path: str,
    width: int = None,
    height: int = None,
    saturation_threshold: float = 0.15,
    padding: int = 0,
    auto_crop_enabled: bool = True
) -> dict:
    """
    이미지 처리 메인 함수
    
    Args:
        input_path: 입력 이미지 경로
        output_path: 출력 이미지 경로
        width: 목표 너비 (선택)
        height: 목표 높이 (선택)
        saturation_threshold: 배경 제거 채도 임계값
        padding: 크롭 후 여백
        auto_crop_enabled: 자동 크롭 활성화 여부
    
    Returns:
        처리 결과 정보 딕셔너리
    """
    # 이미지 로드
    img = Image.open(input_path)
    original_size = img.size
    
    # 1. 배경 제거
    img = remove_low_saturation_background(img, saturation_threshold)
    
    # 2. 자동 크롭
    if auto_crop_enabled:
        img = auto_crop(img, padding)
    
    cropped_size = img.size
    
    # 3. 리사이즈
    if width or height:
        img = resize_image(img, width, height)
    
    final_size = img.size
    
    # 저장
    img.save(output_path)
    
    return {
        'input': input_path,
        'output': output_path,
        'original_size': original_size,
        'cropped_size': cropped_size,
        'final_size': final_size
    }


def main():
    parser = argparse.ArgumentParser(
        description='게임 스크린샷에서 배경 제거 및 크롭'
    )
    parser.add_argument('input', help='입력 이미지 경로')
    parser.add_argument('output', help='출력 이미지 경로')
    parser.add_argument('-w', '--width', type=int, help='목표 너비 (픽셀)')
    parser.add_argument('-ht', '--height', type=int, help='목표 높이 (픽셀)')
    parser.add_argument(
        '-s', '--saturation', type=float, default=0.15,
        help='채도 임계값 (0.0~1.0, 기본값: 0.15)'
    )
    parser.add_argument(
        '-p', '--padding', type=int, default=0,
        help='크롭 후 여백 (픽셀, 기본값: 0)'
    )
    parser.add_argument(
        '--no-crop', action='store_true',
        help='자동 크롭 비활성화'
    )
    
    args = parser.parse_args()
    
    result = process_image(
        args.input,
        args.output,
        width=args.width,
        height=args.height,
        saturation_threshold=args.saturation,
        padding=args.padding,
        auto_crop_enabled=not args.no_crop
    )
    
    print(f"처리 완료!")
    print(f"  입력: {result['input']}")
    print(f"  출력: {result['output']}")
    print(f"  원본 크기: {result['original_size']}")
    print(f"  크롭 후: {result['cropped_size']}")
    print(f"  최종 크기: {result['final_size']}")


if __name__ == '__main__':
    main()
