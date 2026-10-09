import os
import threading
import time
from collections import defaultdict

from dotenv import load_dotenv

load_dotenv()  # antes dos imports locais, que leem o ambiente

from flask import Flask, jsonify, request  # noqa: E402

import llm  # noqa: E402
import memory  # noqa: E402
from buffer import MessageBuffer  # noqa: E402
from uazapi import mark_read, send_presence, send_text  # noqa: E402

BUFFER_SECONDS = float(os.getenv("BUFFER_SECONDS", "8"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Você é um assistente útil. Seja breve.").replace("\\n", "\n")
PORT = int(os.getenv("PORT", "5000"))

app = Flask(__name__)
_user_locks = defaultdict(threading.Lock)  # evita dois flushes simultâneos do mesmo usuário


def split_reply(text: str, max_len: int = 800) -> list[str]:
    chunks = []
    for part in text.split("\n\n"):
        part = part.strip()
        if len(part) <= max_len:
            chunks.append(part)
            continue
        current = ""
        for sentence in part.split(". "):
            sentence = sentence if sentence.endswith(".") else sentence + "."
            if current and len(current) + len(sentence) + 1 > max_len:
                chunks.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        chunks.append(current)
    return [c.strip() for c in chunks if c.strip()]


def handle_flush(user: str, texts: list[str]) -> None:
    with _user_locks[user]:
        try:
            send_presence(user, "composing")
            memory.append(user, "user", "\n".join(texts))
            reply = llm.generate_reply(memory.get(user), SYSTEM_PROMPT)
            print(f"[llm] reply len={len(reply)}")
            if not reply:
                return
            memory.append(user, "model", reply)
            chunks = split_reply(reply)
            for chunk in chunks:
                send_presence(user, "composing")
                time.sleep(1 + len(chunk) / 200)
                send_text(user, chunk)
            print(f"[send] user={user} msgs={len(chunks)}")
        except Exception as e:  # não derruba a thread do timer
            print(f"[flush] erro user={user}: {e}")
        finally:
            send_presence(user, "paused")


buffer = MessageBuffer(BUFFER_SECONDS, on_flush=handle_flush)


@app.get("/")
def health():
    return "ok"


@app.post("/webhook")
def webhook():
    payload = request.get_json(silent=True) or {}
    msg = payload.get("message") or {}
    if (
        payload.get("EventType") != "messages"
        or msg.get("fromMe")
        or msg.get("isGroup")
        or msg.get("messageType") not in ("Conversation", "ExtendedTextMessage")
        or not msg.get("text")
        or not msg.get("chatid")
    ):
        return jsonify({"ok": True})
    number = msg["chatid"].split("@")[0]
    print(f"[webhook] message user={number}")
    threading.Thread(target=mark_read, args=(msg.get("messageid") or msg["id"],), daemon=True).start()
    buffer.add(number, msg["text"])
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
