import os
import threading

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))
_history: dict[str, list[dict]] = {}
_lock = threading.Lock()


def append(user: str, role: str, text: str) -> None:
    """role: 'user' ou 'model' (formato nativo do Gemini)."""
    with _lock:
        msgs = _history.setdefault(user, [])
        msgs.append({"role": role, "parts": [{"text": text}]})
        del msgs[:-MAX_HISTORY]
        while msgs and msgs[0]["role"] != "user":  # Gemini espera começar por 'user'
            msgs.pop(0)


def get(user: str) -> list:
    with _lock:
        return list(_history.get(user, []))


def reset(user: str) -> None:
    with _lock:
        _history.pop(user, None)
