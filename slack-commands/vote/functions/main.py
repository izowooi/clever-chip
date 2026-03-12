"""Slack 투표 봇 - Firebase Functions 진입점"""

import json
import os
from urllib.parse import parse_qs

from firebase_functions import https_fn, options
from firebase_admin import initialize_app

from slack_utils import verify_slack_signature, update_message, post_message
from vote_service import (
    parse_options,
    create_vote_blocks,
    update_vote_blocks,
    validate_options
)

# Firebase Admin 초기화
initialize_app()

# 기본 옵션 설정 (서울 리전)
options.set_global_options(region=options.SupportedRegion.ASIA_NORTHEAST3)


@https_fn.on_request(
    memory=options.MemoryOption.MB_256,
    timeout_sec=60,
    secrets=["SLACK_SIGNING_SECRET", "SLACK_BOT_TOKEN"]
)
def slack_vote(req: https_fn.Request) -> https_fn.Response:
    """
    슬래시 커맨드 처리 (/투표, /vote)

    Slack에서 POST 요청으로 전송:
    - command: /투표 또는 /vote
    - text: 옵션들 (쉼표로 구분)
    - user_id: 요청한 사용자 ID
    - channel_id: 채널 ID
    - response_url: 응답 URL
    """
    # POST 요청만 허용
    if req.method != "POST":
        return https_fn.Response("Method Not Allowed", status=405)

    # Slack 서명 검증
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    timestamp = req.headers.get("X-Slack-Request-Timestamp", "")
    signature = req.headers.get("X-Slack-Signature", "")
    body = req.get_data()

    if not verify_slack_signature(signing_secret, timestamp, signature, body):
        return https_fn.Response("Invalid signature", status=401)

    # 폼 데이터 파싱
    form_data = parse_qs(body.decode("utf-8"))

    # 단일 값 추출 헬퍼
    def get_value(key: str) -> str:
        values = form_data.get(key, [""])
        return values[0] if values else ""

    text = get_value("text")
    channel_id = get_value("channel_id")

    # 옵션 파싱
    vote_options = parse_options(text)

    # 유효성 검사
    error_msg = validate_options(vote_options)
    if error_msg:
        return https_fn.Response(
            json.dumps({
                "response_type": "ephemeral",
                "text": error_msg
            }),
            status=200,
            content_type="application/json"
        )

    # 투표 블록 생성
    blocks = create_vote_blocks(vote_options)

    # 봇이 직접 채널에 메시지 전송 (chat.update 가능하도록)
    try:
        post_message(channel_id, blocks)
    except Exception as e:
        print(f"메시지 전송 실패: {e}")
        return https_fn.Response(
            json.dumps({"response_type": "ephemeral", "text": "투표 생성에 실패했습니다."}),
            status=200,
            content_type="application/json"
        )

    return https_fn.Response("", status=200)


@https_fn.on_request(
    memory=options.MemoryOption.MB_256,
    timeout_sec=60,
    secrets=["SLACK_SIGNING_SECRET", "SLACK_BOT_TOKEN"]
)
def slack_vote_interactive(req: https_fn.Request) -> https_fn.Response:
    """
    Interactive 컴포넌트 처리 (버튼 클릭)

    Slack에서 payload 파라미터로 JSON 전송:
    - type: block_actions
    - user: 클릭한 사용자 정보
    - channel: 채널 정보
    - message: 현재 메시지 정보 (blocks 포함)
    - actions: 클릭한 액션 정보
    """
    # POST 요청만 허용
    if req.method != "POST":
        return https_fn.Response("Method Not Allowed", status=405)

    # Slack 서명 검증
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET", "")
    timestamp = req.headers.get("X-Slack-Request-Timestamp", "")
    signature = req.headers.get("X-Slack-Signature", "")
    body = req.get_data()

    if not verify_slack_signature(signing_secret, timestamp, signature, body):
        return https_fn.Response("Invalid signature", status=401)

    # payload 파싱
    form_data = parse_qs(body.decode("utf-8"))
    payload_str = form_data.get("payload", [""])[0]

    if not payload_str:
        return https_fn.Response("Missing payload", status=400)

    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        return https_fn.Response("Invalid payload", status=400)

    # block_actions 타입만 처리
    if payload.get("type") != "block_actions":
        return https_fn.Response("", status=200)

    # 필요한 정보 추출
    user = payload.get("user", {})
    user_id = user.get("id", "")

    channel = payload.get("channel", {})
    channel_id = channel.get("id", "")

    message = payload.get("message", {})
    message_ts = message.get("ts", "")
    current_blocks = message.get("blocks", [])

    actions = payload.get("actions", [])
    if not actions:
        return https_fn.Response("", status=200)

    clicked_action = actions[0]
    clicked_action_id = clicked_action.get("action_id", "")

    # 투표 액션인지 확인
    if not clicked_action_id.startswith("vote_action_"):
        return https_fn.Response("", status=200)

    # 블록 업데이트
    updated_blocks = update_vote_blocks(current_blocks, clicked_action_id, user_id)

    # 메시지 업데이트
    try:
        update_message(channel_id, message_ts, updated_blocks)
    except Exception as e:
        print(f"메시지 업데이트 실패: {e}")
        # 에러가 발생해도 200 반환 (Slack이 재시도하지 않도록)

    # 빈 응답 (Slack은 200 OK만 기대)
    return https_fn.Response("", status=200)
