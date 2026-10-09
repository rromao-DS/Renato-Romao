import mimetypes
import os
import time

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
    _call("POST", "/message/presence", {"number": number, "presence": presence})


def mark_read(message_id: str) -> None:
    _call("POST", "/message/markread", {"id": [message_id]})


def download_media(message_id: str, folder: str) -> tuple[str, str] | None:
    """POST /message/download -> fileURL (válida por 2 dias); salva em folder. Retorna (caminho, mimetype)."""
    try:
        r = requests.post(BASE_URL + "/message/download", json={"id": message_id}, headers=HEADERS, timeout=60)
        data = r.json()
        if r.status_code >= 400 or not data.get("fileURL"):
            print(f"[uazapi] download erro http={r.status_code}")
            return None
        mime = (data.get("mimetype") or "application/octet-stream").split(";")[0]
        content = requests.get(data["fileURL"], timeout=120).content
    except (requests.RequestException, ValueError) as e:
        print(f"[uazapi] download falhou: {e}")
        return None
    os.makedirs(folder, exist_ok=True)
    ext = mimetypes.guess_extension(mime) or ""
    path = os.path.join(folder, f"{time.strftime('%Y%m%d-%H%M%S')}_{message_id.split(':')[-1]}{ext}")
    with open(path, "wb") as f:
        f.write(content)
    return path, mime
