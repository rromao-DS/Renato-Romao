import functools
import os
import time

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini" ou "claude"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-5-5")
CLAUDE_MIMES = ("application/pdf", "image/jpeg", "image/png", "image/gif", "image/webp")


@functools.cache
def _gemini_client():
    from google import genai
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@functools.cache
def _claude_client():
    import anthropic
    return anthropic.Anthropic()  # lê ANTHROPIC_API_KEY


def generate_reply(history: list[dict], system: str, files: list | None = None,
                   tools: list | None = None, provider: str | None = None) -> str:
    """history: [{"role": "user"|"assistant", "text": str}], o último é o turno atual.
    files: [(caminho, mimetype)] anexados ao último turno. tools=None hoje (function calling depois)."""
    call = _claude if (provider or PROVIDER) == "claude" else _gemini
    for attempt in range(3):  # 429/5xx/529 costumam ser picos temporários do provedor
        try:
            return call(history, system, files or [], tools)
        except Exception as e:
            code = getattr(e, "code", None) or getattr(e, "status_code", None)
            if attempt == 2 or code not in (429, 500, 503, 529):
                raise
            wait = 3 * (attempt + 1)
            print(f"[llm] erro {code}, tentando de novo em {wait}s")
            time.sleep(wait)


def _gemini(history, system, files, tools):
    from google.genai import types
    contents = [
        types.Content(role="model" if m["role"] == "assistant" else "user", parts=[types.Part(text=m["text"])])
        for m in history
    ]
    for path, mime in files:
        with open(path, "rb") as f:
            contents[-1].parts.insert(0, types.Part.from_bytes(data=f.read(), mime_type=mime))
    config = types.GenerateContentConfig(system_instruction=system, max_output_tokens=1024, tools=tools)
    response = _gemini_client().models.generate_content(model=GEMINI_MODEL, contents=contents, config=config)
    # TODO: handle function_call parts quando tools for usado
    return (response.text or "").strip()


def _claude(history, system, files, tools):
    import base64
    messages = [{"role": m["role"], "content": m["text"]} for m in history]
    blocks = []
    for path, mime in files:
        if mime not in CLAUDE_MIMES:
            continue
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode()
        kind = "document" if mime == "application/pdf" else "image"
        blocks.append({"type": kind, "source": {"type": "base64", "media_type": mime, "data": data}})
    if blocks:
        messages[-1]["content"] = blocks + [{"type": "text", "text": messages[-1]["content"]}]
    kwargs = {"tools": tools} if tools else {}  # formato de tools do Claude difere do Gemini
    response = _claude_client().messages.create(
        model=CLAUDE_MODEL, max_tokens=4096, system=system, messages=messages,
        output_config={"effort": "low"}, **kwargs,
    )
    # TODO: handle tool_use blocks quando tools for usado
    return "".join(b.text for b in response.content if b.type == "text").strip()
