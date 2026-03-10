from collections import defaultdict
from queue import Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Type


class EventBus:

    def __init__(self):

        self._subscribers = defaultdict(list)

        self._queue = Queue()

        self._executor = ThreadPoolExecutor(max_workers=8)

        self._worker = Thread(target=self._event_loop, daemon=True)
        self._worker.start()

    def subscribe(self, event_type: Type, handler: Callable):

        self._subscribers[event_type].append(handler)

    def emit(self, event):

        self._queue.put(event)

    def _event_loop(self):

        while True:

            event = self._queue.get()

            handlers = list(self._subscribers[type(event)])

            for handler in handlers:
                self._executor.submit(handler, event)

            self._queue.task_done()