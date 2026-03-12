"""투표 서비스 - 투표 로직 및 Block Kit 생성"""

import json
from typing import Optional

# 숫자 이모지 (1~10)
NUMBER_EMOJIS = [
    ":one:", ":two:", ":three:", ":four:", ":five:",
    ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"
]


def parse_options(text: str) -> list[str]:
    """
    쉼표로 구분된 옵션 텍스트 파싱

    Args:
        text: "apple, banana, melon" 형태의 문자열

    Returns:
        ["apple", "banana", "melon"]
    """
    if not text or not text.strip():
        return []

    options = [opt.strip() for opt in text.split(',')]
    # 빈 문자열 제거
    options = [opt for opt in options if opt]
    return options


def create_vote_blocks(options: list[str]) -> list[dict]:
    """
    투표 Block Kit 블록 생성 (초기 상태)

    Args:
        options: 투표 옵션 리스트

    Returns:
        Slack Block Kit 블록 리스트
    """
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":ballot_box_with_ballot: *투표*"
            }
        },
        {"type": "divider"}
    ]

    for idx, option in enumerate(options):
        emoji = NUMBER_EMOJIS[idx] if idx < len(NUMBER_EMOJIS) else f"*{idx + 1}.*"

        # 버튼 value에 저장할 데이터
        value_data = {
            "idx": idx,
            "opt": option,
            "v": []  # 투표자 목록 (User ID)
        }

        blocks.append({
            "type": "section",
            "block_id": f"vote_block_{idx}",
            "text": {
                "type": "mrkdwn",
                "text": f"{emoji} *{option}*\n_아직 투표 없음_"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "투표 (0)",
                    "emoji": True
                },
                "action_id": f"vote_action_{idx}",
                "value": json.dumps(value_data, ensure_ascii=False)
            }
        })

    # 안내 문구
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": ":information_source: 여러 항목 선택 가능 | 다시 클릭하면 취소"
            }
        ]
    })

    return blocks


def toggle_vote(voters: list[str], user_id: str) -> list[str]:
    """
    투표 토글: 이미 투표했으면 취소, 아니면 추가

    Args:
        voters: 현재 투표자 User ID 목록
        user_id: 클릭한 사용자의 User ID

    Returns:
        업데이트된 투표자 목록
    """
    if user_id in voters:
        voters.remove(user_id)
    else:
        voters.append(user_id)
    return voters


def format_voters_text(voters: list[str], option: str, emoji: str) -> str:
    """
    투표자 목록을 텍스트로 포맷

    Args:
        voters: 투표자 User ID 목록
        option: 옵션 텍스트
        emoji: 숫자 이모지

    Returns:
        포맷된 텍스트
    """
    if not voters:
        return f"{emoji} *{option}*\n_아직 투표 없음_"

    # @mention 형식으로 사용자 표시
    voter_mentions = " ".join([f"<@{uid}>" for uid in voters])
    return f"{emoji} *{option}*\n{voter_mentions}"


def update_vote_blocks(
    current_blocks: list[dict],
    clicked_action_id: str,
    user_id: str
) -> list[dict]:
    """
    투표 클릭 후 블록 업데이트

    Args:
        current_blocks: 현재 메시지의 블록들
        clicked_action_id: 클릭된 버튼의 action_id
        user_id: 클릭한 사용자 ID

    Returns:
        업데이트된 블록 리스트
    """
    updated_blocks = []

    for block in current_blocks:
        if block.get("type") != "section" or "accessory" not in block:
            updated_blocks.append(block)
            continue

        accessory = block.get("accessory", {})
        if accessory.get("type") != "button":
            updated_blocks.append(block)
            continue

        action_id = accessory.get("action_id", "")
        value_str = accessory.get("value", "{}")

        try:
            value_data = json.loads(value_str)
        except json.JSONDecodeError:
            updated_blocks.append(block)
            continue

        idx = value_data.get("idx", 0)
        option = value_data.get("opt", "")
        voters = value_data.get("v", [])

        # 클릭된 버튼이면 투표 토글
        if action_id == clicked_action_id:
            voters = toggle_vote(voters, user_id)

        # 이모지 결정
        emoji = NUMBER_EMOJIS[idx] if idx < len(NUMBER_EMOJIS) else f"*{idx + 1}.*"

        # 새 value 데이터
        new_value_data = {
            "idx": idx,
            "opt": option,
            "v": voters
        }

        # 업데이트된 블록 생성
        updated_block = {
            "type": "section",
            "block_id": block.get("block_id", f"vote_block_{idx}"),
            "text": {
                "type": "mrkdwn",
                "text": format_voters_text(voters, option, emoji)
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": f"투표 ({len(voters)})",
                    "emoji": True
                },
                "action_id": action_id,
                "value": json.dumps(new_value_data, ensure_ascii=False)
            }
        }

        updated_blocks.append(updated_block)

    return updated_blocks


def validate_options(options: list[str]) -> Optional[str]:
    """
    옵션 유효성 검사

    Args:
        options: 옵션 리스트

    Returns:
        에러 메시지 (없으면 None)
    """
    if not options:
        return "사용법: `/투표 옵션1, 옵션2, 옵션3`\n예: `/투표 짜장면, 짬뽕, 탕수육`"

    if len(options) < 2:
        return "최소 2개 이상의 옵션이 필요합니다.\n예: `/투표 옵션1, 옵션2`"

    if len(options) > 10:
        return "최대 10개까지 옵션을 입력할 수 있습니다."

    # 각 옵션 길이 체크
    for opt in options:
        if len(opt) > 50:
            return f"옵션이 너무 깁니다 (최대 50자): {opt[:20]}..."

    return None
