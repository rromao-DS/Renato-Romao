import threading
from typing import Callable


class MessageBuffer:
    """Debounce por usuário: cada mensagem nova reseta o timer."""

    def __init__(self, wait_seconds: float, on_flush: Callable[[str, list[str]], None]):
        self.wait = wait_seconds
        self.on_flush = on_flush
        self._lock = threading.Lock()
        self._texts: dict[str, list[str]] = {}
        self._timers: dict[str, threading.Timer] = {}

    def add(self, user: str, text: str) -> None:
        with self._lock:
            self._texts.setdefault(user, []).append(text)
            if user in self._timers:
                self._timers[user].cancel()
            timer = threading.Timer(self.wait, self._flush, [user])
            timer.daemon = True
            self._timers[user] = timer
            timer.start()

    def _flush(self, user: str) -> None:
        with self._lock:
            texts = self._texts.pop(user, [])
            self._timers.pop(user, None)
        if texts:
            print(f"[buffer] flush user={user} msgs={len(texts)}")
            self.on_flush(user, texts)
