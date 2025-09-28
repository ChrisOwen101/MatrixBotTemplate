import asyncio
import time
import types
import pytest
from bot.handlers import on_message, START_TIME_MS, HISTORICAL_SKEW_MS


class DummyResp:
    def __init__(self):
        self.transport_response = types.SimpleNamespace(ok=True)


class DummyClient:
    def __init__(self):
        self.sent = []

    async def room_send(self, **kwargs):  # mimic nio interface used
        self.sent.append(kwargs)
        return DummyResp()


class DummyRoom:
    def __init__(self, room_id="!BHXRvKRXKeMuirqrlY:example.org"):
        self.room_id = room_id


class DummyEvent:
    event_id = "$abcdef:example.org"
    sender = "@someone:example.org"
    body = "!ping"

    def __init__(self, ts):
        self.server_timestamp = ts


@pytest.mark.asyncio
async def test_historical_event_ignored():
    client = DummyClient()
    old_ts = START_TIME_MS - HISTORICAL_SKEW_MS - 1000
    event = DummyEvent(old_ts)
    room = DummyRoom()
    await on_message(client, room, event)
    assert client.sent == []  # no messages sent


@pytest.mark.asyncio
async def test_recent_event_processed():
    client = DummyClient()
    new_ts = int(time.time()*1000)
    event = DummyEvent(new_ts)
    room = DummyRoom()
    await on_message(client, room, event)
    assert len(client.sent) == 1
    content = client.sent[0]["content"]
    assert content["body"] == "pong"  # reply to !ping
