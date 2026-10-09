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
from uazapi import download_media, mark_read, send_presence, send_text  # noqa: E402

BUFFER_SECONDS = float(os.getenv("BUFFER_SECONDS", "8"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Você é um assistente útil. Seja breve.").replace("\\n", "\n")
ERROR_MESSAGE = os.getenv("ERROR_MESSAGE", "Desculpe, tive um problema para responder agora. Pode repetir em alguns instantes?")
PORT = int(os.getenv("PORT", "5000"))
INSTANCE_TOKEN = os.getenv("UAZAPI_INSTANCE_TOKEN", "")

app = Flask(__name__)
_user_locks = defaultdict(threading.Lock)  # evita dois flushes simultâneos do mesmo usuário
_pending_files = defaultdict(list)  # {numero: [(caminho, mimetype)]} do buffer atual
_files_lock = threading.Lock()
TEXT_TYPES = ("Conversation", "ExtendedTextMessage")


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
            with _files_lock:
                files = _pending_files.pop(user, [])
            memory.append(user, "user", "\n".join(texts))  # arquivos só vão no turno atual; o histórico guarda o texto
            reply = llm.generate_reply(memory.get(user), SYSTEM_PROMPT, files=files)
            print(f"[llm] reply len={len(reply)}")
            if not reply:
                send_text(user, ERROR_MESSAGE)
                return
            memory.append(user, "assistant", reply)
            chunks = split_reply(reply)
            for chunk in chunks:
                send_presence(user, "composing")
                time.sleep(1 + len(chunk) / 200)
                send_text(user, chunk)
            print(f"[send] user={user} msgs={len(chunks)}")
        except Exception as e:  # não derruba a thread do timer
            print(f"[flush] erro user={user}: {e}")
            send_text(user, ERROR_MESSAGE)  # o cliente não fica sem resposta
        finally:
            send_presence(user, "paused")


buffer = MessageBuffer(BUFFER_SECONDS, on_flush=handle_flush)


@app.get("/")
def health():
    return "ok"


def handle_media(number: str, msg: dict) -> None:
    """Baixa o arquivo para arquivos/<numero>/ e entra no buffer junto com a legenda."""
    got = download_media(msg.get("messageid") or msg["id"], os.path.join("arquivos", number))
    if not got:
        return
    path, mime = got
    print(f"[media] user={number} mime={mime} file={os.path.basename(path)}")
    with _files_lock:
        _pending_files[number].append(got)
    caption = msg.get("text") or ""
    buffer.add(number, f"{caption}\n[arquivo enviado: {os.path.basename(path)}]".strip())


@app.post("/webhook")
def webhook():
    payload = request.get_json(silent=True) or {}
    msg = payload.get("message") or {}
    if payload.get("token") and payload["token"] != INSTANCE_TOKEN:  # webhook global: outra instância do servidor
        return jsonify({"ok": True})
    if (
        payload.get("EventType") != "messages"
        or msg.get("fromMe")
        or msg.get("isGroup")
        or not msg.get("chatid")
    ):
        return jsonify({"ok": True})
    number = msg["chatid"].split("@")[0]
    msg_id = msg.get("messageid") or msg.get("id", "")
    if msg.get("messageType") in TEXT_TYPES:
        if not msg.get("text"):
            return jsonify({"ok": True})
        print(f"[webhook] text user={number}")
        buffer.add(number, msg["text"])
    else:  # qualquer outro tipo: tenta baixar como mídia (pdf/imagem); sem mídia, ignora
        print(f"[webhook] media? user={number} type={msg.get('messageType')} mediaType={msg.get('mediaType')}")
        threading.Thread(target=handle_media, args=(number, msg), daemon=True).start()
    threading.Thread(target=mark_read, args=(msg_id,), daemon=True).start()  # não bloqueia
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
