from __future__ import annotations

import pytest

# Check optional Slack dependencies before running tests
try:
    import slack_sdk  # noqa: F401
except ImportError:
    pytest.skip("Slack dependencies not installed (slack-sdk)", allow_module_level=True)

from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.slack import SlackChannel
from nanobot.channels.slack import SlackConfig
from nanobot.channels.slack import SlackDMConfig


class _FakeAsyncWebClient:
    def __init__(self) -> None:
        self.chat_post_calls: list[dict[str, object | None]] = []
        self.file_upload_calls: list[dict[str, object | None]] = []
        self.reactions_add_calls: list[dict[str, object | None]] = []
        self.reactions_remove_calls: list[dict[str, object | None]] = []

    async def chat_postMessage(
        self,
        *,
        channel: str,
        text: str,
        thread_ts: str | None = None,
    ) -> None:
        self.chat_post_calls.append(
            {
                "channel": channel,
                "text": text,
                "thread_ts": thread_ts,
            }
        )

    async def files_upload_v2(
        self,
        *,
        channel: str,
        file: str,
        thread_ts: str | None = None,
    ) -> None:
        self.file_upload_calls.append(
            {
                "channel": channel,
                "file": file,
                "thread_ts": thread_ts,
            }
        )

    async def reactions_add(
        self,
        *,
        channel: str,
        name: str,
        timestamp: str,
    ) -> None:
        self.reactions_add_calls.append(
            {
                "channel": channel,
                "name": name,
                "timestamp": timestamp,
            }
        )

    async def reactions_remove(
        self,
        *,
        channel: str,
        name: str,
        timestamp: str,
    ) -> None:
        self.reactions_remove_calls.append(
            {
                "channel": channel,
                "name": name,
                "timestamp": timestamp,
            }
        )


class _FakeSocketModeClient:
    async def send_socket_mode_response(self, response: SocketModeResponse) -> None:
        pass


@pytest.mark.asyncio
async def test_send_uses_thread_for_channel_messages() -> None:
    channel = SlackChannel(SlackConfig(enabled=True), MessageBus())
    fake_web = _FakeAsyncWebClient()
    channel._web_client = fake_web

    await channel.send(
        OutboundMessage(
            channel="slack",
            chat_id="C123",
            content="hello",
            media=["/tmp/demo.txt"],
            metadata={"slack": {"thread_ts": "1700000000.000100", "channel_type": "channel"}},
        )
    )

    assert len(fake_web.chat_post_calls) == 1
    assert fake_web.chat_post_calls[0]["text"] == "hello\n"
    assert fake_web.chat_post_calls[0]["thread_ts"] == "1700000000.000100"
    assert len(fake_web.file_upload_calls) == 1
    assert fake_web.file_upload_calls[0]["thread_ts"] == "1700000000.000100"


@pytest.mark.asyncio
async def test_send_uses_thread_for_dm_messages() -> None:
    channel = SlackChannel(SlackConfig(enabled=True), MessageBus())
    fake_web = _FakeAsyncWebClient()
    channel._web_client = fake_web

    await channel.send(
        OutboundMessage(
            channel="slack",
            chat_id="D123",
            content="hello",
            media=["/tmp/demo.txt"],
            metadata={"slack": {"thread_ts": "1700000000.000100", "channel_type": "im"}},
        )
    )

    assert len(fake_web.chat_post_calls) == 1
    assert fake_web.chat_post_calls[0]["text"] == "hello\n"
    assert fake_web.chat_post_calls[0]["thread_ts"] == "1700000000.000100"
    assert len(fake_web.file_upload_calls) == 1
    assert fake_web.file_upload_calls[0]["thread_ts"] == "1700000000.000100"


@pytest.mark.asyncio
async def test_send_updates_reaction_when_final_response_sent() -> None:
    channel = SlackChannel(SlackConfig(enabled=True, react_emoji="eyes"), MessageBus())
    fake_web = _FakeAsyncWebClient()
    channel._web_client = fake_web

    await channel.send(
        OutboundMessage(
            channel="slack",
            chat_id="C123",
            content="done",
            metadata={
                "slack": {"event": {"ts": "1700000000.000100"}, "channel_type": "channel"},
            },
        )
    )

    assert fake_web.reactions_remove_calls == [
        {"channel": "C123", "name": "eyes", "timestamp": "1700000000.000100"}
    ]
    assert fake_web.reactions_add_calls == [
        {"channel": "C123", "name": "white_check_mark", "timestamp": "1700000000.000100"}
    ]


@pytest.mark.asyncio
async def test_file_share_event_not_dropped() -> None:
    """Verify that file_share events (messages with file attachments) are processed."""
    config = SlackConfig(
        enabled=True,
        bot_token="xoxb-test",
        reply_in_thread=True,
        allow_from=["*"],
        dm=SlackDMConfig(enabled=True, policy="open"),
    )
    channel = SlackChannel(config, MessageBus())
    channel._bot_user_id = "B123"
    channel._web_client = _FakeAsyncWebClient()  # type: ignore

    # Track calls to _handle_message
    handle_message_calls: list[dict[str, object]] = []

    async def mock_handle_message(**kwargs: object) -> None:
        handle_message_calls.append(kwargs)  # type: ignore

    channel._handle_message = mock_handle_message  # type: ignore

    # Mock _download_slack_files to return a test file path
    async def mock_download_slack_files(event: dict[str, object]) -> list[str]:
        return ["/tmp/test.pdf"]

    channel._download_slack_files = mock_download_slack_files  # type: ignore

    # Create a file_share event
    event = {
        "type": "message",
        "subtype": "file_share",
        "user": "U_SENDER",
        "channel": "C123",
        "channel_type": "im",
        "text": "check this paper",
        "files": [
            {
                "id": "F001",
                "name": "paper.pdf",
                "url_private_download": "https://files.slack.com/...",
                "mimetype": "application/pdf",
            }
        ],
        "ts": "1700000000.000200",
    }

    # Create a SocketModeRequest
    request = SocketModeRequest(
        type="events_api",
        envelope_id="test",
        payload={"event": event},
    )

    # Call _on_socket_request
    fake_socket_client = _FakeSocketModeClient()
    await channel._on_socket_request(fake_socket_client, request)  # type: ignore

    # Verify _handle_message was called
    assert len(handle_message_calls) == 1, "file_share event should not be dropped"

    # Verify the call had the correct parameters
    call = handle_message_calls[0]
    assert call["sender_id"] == "U_SENDER"
    assert call["chat_id"] == "C123"
    assert call["content"] == "check this paper"
    assert call["media"] == ["/tmp/test.pdf"], "media should contain downloaded file path"
