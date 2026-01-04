#!/usr/bin/env python3
"""
노노그램 맵 데이터 검증 스크립트
"""

import json
import sys
from typing import Any

# 유효한 색상 매핑
VALID_COLORS = {
    0: "empty",
    1: "black",
    2: "red",
    3: "blue",
    4: "green",
    5: "yellow",
    6: "orange",
    7: "purple",
    8: "brown"
}

COLOR_NAME_TO_INDEX = {v: k for k, v in VALID_COLORS.items() if k != 0}

REQUIRED_FIELDS = ["id", "title", "hint", "category", "difficulty", "size", "palette", "grid"]

# 그리드 크기 설정 (가로 25, 세로 20)
GRID_WIDTH = 25
GRID_HEIGHT = 20


def validate_nonogram(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    노노그램 맵 데이터 검증
    
    Returns:
        (is_valid, errors): 유효성 여부와 에러 목록
    """
    errors = []
    
    # 1. 필수 필드 확인
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"필수 필드 누락: {field}")
    
    if errors:
        return False, errors
    
    # 2. size 검증 (25x20 고정: 가로 25, 세로 20)
    if data["size"] != [GRID_WIDTH, GRID_HEIGHT]:
        errors.append(f"size는 [{GRID_WIDTH}, {GRID_HEIGHT}]여야 합니다. 현재: {data['size']}")
    
    # 3. difficulty 검증 (1-10)
    if not isinstance(data["difficulty"], int) or not (1 <= data["difficulty"] <= 10):
        errors.append(f"difficulty는 1-10 사이 정수여야 합니다. 현재: {data['difficulty']}")
    
    # 4. palette 검증 (정확히 2가지 색상)
    palette = data["palette"]
    if not isinstance(palette, list) or len(palette) != 2:
        errors.append(f"palette는 정확히 2가지 색상이어야 합니다. 현재: {palette}")
    else:
        for color in palette:
            if color not in COLOR_NAME_TO_INDEX:
                errors.append(f"유효하지 않은 색상: {color}. 유효한 색상: {list(COLOR_NAME_TO_INDEX.keys())}")
    
    # 5. grid 검증 (20행, 25열)
    grid = data["grid"]
    if not isinstance(grid, list) or len(grid) != GRID_HEIGHT:
        errors.append(f"grid는 {GRID_HEIGHT}행이어야 합니다. 현재: {len(grid) if isinstance(grid, list) else 'not a list'}행")
    else:
        for row_idx, row in enumerate(grid):
            if not isinstance(row, list) or len(row) != GRID_WIDTH:
                errors.append(f"grid[{row_idx}]는 {GRID_WIDTH}열이어야 합니다. 현재: {len(row) if isinstance(row, list) else 'not a list'}열")
    
    # 6. grid 값 검증
    if isinstance(grid, list) and len(grid) == GRID_HEIGHT:
        # palette에 해당하는 색상 인덱스 계산
        valid_indices = {0}  # empty는 항상 허용
        if isinstance(palette, list) and len(palette) == 2:
            for color in palette:
                if color in COLOR_NAME_TO_INDEX:
                    valid_indices.add(COLOR_NAME_TO_INDEX[color])
        
        used_colors = set()
        for row_idx, row in enumerate(grid):
            if isinstance(row, list):
                for col_idx, val in enumerate(row):
                    if not isinstance(val, int) or val < 0 or val > 8:
                        errors.append(f"grid[{row_idx}][{col_idx}] 값이 유효하지 않음: {val} (0-8 범위여야 함)")
                    elif val not in valid_indices:
                        errors.append(f"grid[{row_idx}][{col_idx}] 색상 {val}({VALID_COLORS.get(val, '?')})이 palette에 없음")
                    elif val != 0:
                        used_colors.add(val)
        
        # 7. 정확히 2가지 색상 사용 확인
        if len(used_colors) != 2:
            color_names = [VALID_COLORS.get(c, str(c)) for c in used_colors]
            errors.append(f"grid에서 정확히 2가지 색상을 사용해야 합니다. 현재 사용: {color_names}")
    
    # 8. 문자열 필드 검증
    if not isinstance(data.get("id"), str) or not data["id"]:
        errors.append("id는 비어있지 않은 문자열이어야 합니다")
    if not isinstance(data.get("title"), str) or not data["title"]:
        errors.append("title은 비어있지 않은 문자열이어야 합니다")
    if not isinstance(data.get("hint"), str) or not data["hint"]:
        errors.append("hint는 비어있지 않은 문자열이어야 합니다")
    if not isinstance(data.get("category"), str) or not data["category"]:
        errors.append("category는 비어있지 않은 문자열이어야 합니다")
    
    return len(errors) == 0, errors


def visualize_grid(data: dict[str, Any]) -> str:
    """
    그리드를 시각화하여 문자열로 반환
    """
    grid = data.get("grid", [])
    palette = data.get("palette", [])
    
    # 색상별 심볼 매핑
    symbols = {
        0: "⬜",  # empty
        1: "⬛",  # black
        2: "🟥",  # red
        3: "🟦",  # blue
        4: "🟩",  # green
        5: "🟨",  # yellow
        6: "🟧",  # orange
        7: "🟪",  # purple
        8: "🟫",  # brown
    }
    
    lines = []
    lines.append(f"📊 Grid Visualization ({data.get('title', 'Unknown')})")
    lines.append(f"   Palette: {palette}")
    lines.append("")
    
    for row in grid:
        line = ""
        for val in row:
            line += symbols.get(val, "?")
        lines.append(line)
    
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_nonogram.py <json_file>")
        print("       python validate_nonogram.py <json_file> --visualize")
        sys.exit(1)
    
    json_file = sys.argv[1]
    visualize = "--visualize" in sys.argv or "-v" in sys.argv
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        sys.exit(1)
    
    is_valid, errors = validate_nonogram(data)
    
    if is_valid:
        print("✅ Valid - 노노그램 맵 데이터가 유효합니다!")
        print(f"   ID: {data['id']}")
        print(f"   Title: {data['title']}")
        print(f"   Hint: {data['hint']}")
        print(f"   Category: {data['category']}")
        print(f"   Difficulty: {data['difficulty']}/10")
        print(f"   Palette: {data['palette']}")
        
        if visualize:
            print()
            print(visualize_grid(data))
    else:
        print("❌ Invalid - 다음 오류가 발견되었습니다:")
        for error in errors:
            print(f"   • {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
