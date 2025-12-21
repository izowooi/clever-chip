---
name: image-background-remover
description: 이미지에서 배경을 제거하고 투명 PNG로 변환하는 skill. 격자무늬/단색 배경 제거, 불필요한 여백 자동 크롭, 지정 크기로 리사이즈 기능 제공. 사용자가 "배경 제거", "배경 투명하게", "여백 제거", "이미지 크롭" 등을 요청할 때 사용.
---

# Image Background Remover

이미지에서 배경을 제거하고 투명 PNG로 변환하는 skill.

## 핵심 기능

1. **배경 제거**: 격자무늬/단색 배경을 투명하게 변환 (채도 기반)
2. **자동 크롭**: 불필요한 여백 제거
3. **리사이즈**: 지정 크기로 스케일링 (비율 유지 또는 강제 스트레치)

## 사용법

### 스크립트 실행

```bash
python scripts/remove_background.py <input> <output> [options]

# 옵션
-w, --width       목표 너비 (픽셀)
-ht, --height     목표 높이 (픽셀)  
-s, --saturation  채도 임계값 (0.0~1.0, 기본값: 0.15)
-p, --padding     크롭 후 여백 (픽셀)
--no-crop         자동 크롭 비활성화
--stretch         비율 무시하고 지정 크기로 강제 스트레치
```

### 예시

```bash
# 기본 사용 (배경 제거 + 크롭)
python scripts/remove_background.py input.png output.png

# 100x100으로 리사이즈 (비율 유지)
python scripts/remove_background.py input.png output.png -w 100 -ht 100

# 100x100으로 강제 스트레치 (비율 무시)
python scripts/remove_background.py input.png output.png -w 100 -ht 100 --stretch

# 채도 임계값 조정 (더 많은 배경 제거)
python scripts/remove_background.py input.png output.png -s 0.25
```

### Python 모듈로 사용

```python
from scripts.remove_background import process_image, resize_image

# 전체 파이프라인 (비율 무시하고 강제 스트레치)
result = process_image(
    'input.png',
    'output.png',
    width=100,
    height=100,
    keep_aspect=False  # 비율 무시
)

# resize_image 직접 사용
from PIL import Image
img = Image.open('input.png')
img = resize_image(img, width=100, height=100, keep_aspect=False)
img.save('output.png')
```

## 채도 임계값 가이드

| 값 | 용도 |
|----|------|
| 0.10 | 순수 회색만 제거 (보수적) |
| 0.15 | 기본값, 대부분의 격자무늬 배경 |
| 0.20~0.25 | 약간 색이 있는 배경까지 제거 |
| 0.30+ | 공격적 제거 (주의: 원본 손실 가능) |

## 의존성

- Python 3.8+
- Pillow (`pip install pillow`)
- NumPy (`pip install numpy`)
