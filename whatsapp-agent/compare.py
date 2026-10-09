"""Compara Gemini x Claude no mesmo arquivo/pergunta.
Uso: python compare.py <arquivo ou pasta> "pergunta"   (precisa das duas chaves no .env)"""
import mimetypes
import os
import sys
import time

from dotenv import load_dotenv

load_dotenv()
import llm  # noqa: E402

target, question = sys.argv[1], sys.argv[2]
paths = [os.path.join(target, f) for f in sorted(os.listdir(target))] if os.path.isdir(target) else [target]
system = os.getenv("SYSTEM_PROMPT", "Você é um assistente útil.").replace("\n", "\n")
for path in paths:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    print(f"\n===== {os.path.basename(path)} ({mime}) =====")
    for provider in ("gemini", "claude"):
        t = time.time()
        try:
            out = llm.generate_reply([{"role": "user", "text": question}], system, files=[(path, mime)], provider=provider)
        except Exception as e:
            out = f"ERRO: {e}"
        print(f"\n--- {provider} ({time.time() - t:.1f}s) ---\n{out}")
