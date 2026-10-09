import os

import requests

BASE_URL = os.getenv("UAZAPI_BASE_URL", "").rstrip("/")
HEADERS = {"token": os.getenv("UAZAPI_INSTANCE_TOKEN", ""), "Content-Type": "application/json"}


def _call(method: str, path: str, body: dict) -> None:
    try:
        r = requests.request(method, BASE_URL + path, json=body, headers=HEADERS, timeout=15)
        if r.status_code >= 400:
            print(f"[uazapi] {path} erro http={r.status_code}")
    except requests.RequestException as e:
        print(f"[uazapi] {path} falhou: {e}")


def send_text(number: str, text: str) -> None:
    _call("POST", "/send/text", {"number": number, "text": text})


def send_presence(number: str, presence: str) -> None:
    """presence: 'composing' (digitando) ou 'paused'."""
    _call("POST", "/send/presence", {"number": number, "presence": presence})


def mark_read(number: str, message_id: str) -> None:
    _call("PUT", "/send/read", {"number": number, "messageId": message_id})
