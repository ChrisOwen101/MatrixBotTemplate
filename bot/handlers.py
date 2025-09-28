from __future__ import annotations
from nio import RoomMessageText, AsyncClient, RoomSendResponse
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

# Record bot start time (ms) to filter historical events on first sync.
START_TIME_MS = int(time.time() * 1000)
HISTORICAL_SKEW_MS = 5000  # allow 5s clock skew / startup delay

ALLOWED_ROOMS = ["!BHXRvKRXKeMuirqrlY:matrix.campaignlab.uk"]


async def generate_reply(body: str) -> str | None:
    """Very simple reply logic; extend with NLP or command parsing."""
    body_lower = body.strip().lower()
    if body_lower.startswith("!ping"):
        return "pong"
    if body_lower in {"hi", "hello", "hey"}:
        return "Hello! I'm a Matrix bot."

    return None


def is_old_event(event) -> bool:
    server_ts = getattr(event, "server_timestamp", None)
    return isinstance(server_ts, (int, float)) and server_ts < START_TIME_MS - HISTORICAL_SKEW_MS


async def on_message(client: AsyncClient, room, event: RoomMessageText):
    # Ignore events that are older than when the bot started (minus skew)
    if is_old_event(event):
        logger.debug("Ignoring old event %s from %s in %s",
                     event.event_id, event.sender, room.room_id)
        return

    if not room.room_id in ALLOWED_ROOMS:
        return

    try:
        reply = await generate_reply(event.body)

        if not reply:
            return  # Nothing to send

        logger.info("Replying in %s to %s: %s",
                    room.room_id, event.sender, reply)
        resp: RoomSendResponse = await client.room_send(
            room_id=room.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": reply,
                "m.relates_to": {
                    "m.in_reply_to": {"event_id": event.event_id}
                },
            },
        )
        # type: ignore[attr-defined]
        if hasattr(resp, 'transport_response') and resp.transport_response.ok:
            logger.debug("Message sent successfully")
        else:
            logger.warning("Message send may have failed: %s", resp)
    except Exception:  # pragma: no cover - log unexpected
        logger.exception("Failed handling message event")
