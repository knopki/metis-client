"""Stream endpoint namespace"""

from asyncio import Event, Task, create_task, sleep
from typing import Callable, Optional

from aiohttp_sse_client.client import MessageEvent

from ..models.event import MetisEvent, MetisMessageEvent, cast_event
from ..models.pubsub import MetisHub, MetisSubscription
from .base import BaseNamespace


class MetisStreamNamespace(BaseNamespace):
    """Stream endpoints namespace"""

    _hub: MetisHub
    _stream_task: Optional[Task] = None
    _subscribe_event: Event

    def __post_init__(self) -> None:
        self._hub = MetisHub()
        self._stream_task = create_task(self._stream_consumer())
        self._subscribe_event = Event()
        return super().__post_init__()

    async def _stream_consumer(self):
        sse_task: Optional[Task] = None

        def on_open():
            self._hub.set_connected()

        def on_message(evt: MessageEvent):
            self._hub.set_connected()
            evt_dto = MetisMessageEvent.from_dto(evt).to_dto()
            self._hub.publish(cast_event(evt_dto))
            # cancel streaming task if no subscribers
            if sse_task and len(self._hub) == 0:
                self._hub.set_disconnected()
                sse_task.cancel()

        while True:
            await self._subscribe_event.wait()
            if sse_task is None or sse_task.done():
                sse_task = create_task(
                    self._client.sse(self._base_url, on_message, on_open)
                )
            self._subscribe_event.clear()
            while not self._hub.connected:
                await sleep(0.1)
                await self._root.v0.ping()

    def close(self):
        "Close background stream consumer"
        if self._stream_task:
            self._stream_task.cancel()

    def subscribe(self, predicate: Optional[Callable[[MetisEvent], bool]] = None):
        "Subscribe to stream"
        self._subscribe_event.set()
        return MetisSubscription(self._hub, predicate=predicate)
