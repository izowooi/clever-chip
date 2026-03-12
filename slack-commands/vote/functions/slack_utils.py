"""Slack 유틸리티 - 서명 검증 및 API 호출"""

import hmac
import hashlib
import time
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def verify_slack_signature(
    signing_secret: str,
    timestamp: str,
    signature: str,
    body: bytes
) -> bool:
    """
    Slack 요청 서명 검증

    Args:
        signing_secret: Slack App의 Signing Secret
        timestamp: X-Slack-Request-Timestamp 헤더 값
        signature: X-Slack-Signature 헤더 값
        body: 요청 body (bytes)

    Returns:
        검증 성공 여부
    """
    # 5분 이상 된 요청 거부 (Replay Attack 방지)
    if abs(time.time() - int(timestamp)) > 300:
        return False

    # 서명 생성
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    my_signature = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    # 타이밍 공격 방지를 위한 상수 시간 비교
    return hmac.compare_digest(my_signature, signature)


def get_slack_client() -> WebClient:
    """Slack WebClient 인스턴스 반환"""
    bot_token = os.environ.get('SLACK_BOT_TOKEN')
    if not bot_token:
        raise ValueError("SLACK_BOT_TOKEN 환경 변수가 설정되지 않았습니다")
    return WebClient(token=bot_token)


def post_message(channel: str, blocks: list) -> dict:
    """
    Slack 채널에 새 메시지 전송

    Args:
        channel: 채널 ID
        blocks: Block Kit 블록들

    Returns:
        Slack API 응답
    """
    client = get_slack_client()
    try:
        response = client.chat_postMessage(
            channel=channel,
            blocks=blocks,
            text="투표"
        )
        return response
    except SlackApiError as e:
        print(f"Slack API 에러: {e.response['error']}")
        raise


def update_message(channel: str, ts: str, blocks: list) -> dict:
    """
    Slack 메시지 업데이트

    Args:
        channel: 채널 ID
        ts: 메시지 타임스탬프
        blocks: 업데이트할 Block Kit 블록들

    Returns:
        Slack API 응답
    """
    client = get_slack_client()
    try:
        response = client.chat_update(
            channel=channel,
            ts=ts,
            blocks=blocks,
            text="투표"  # fallback text
        )
        return response
    except SlackApiError as e:
        print(f"Slack API 에러: {e.response['error']}")
        raise
