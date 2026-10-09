# Agente de IA no WhatsApp (UAZAPI + Gemini)

Aplicação Flask mínima que recebe mensagens do WhatsApp via webhook da UAZAPI, junta as mensagens
que chegam em sequência (debounce) em um único turno, responde com o Google Gemini 2.5 Flash
e envia a resposta dividida em várias mensagens, com o indicador "digitando" entre elas.
Tudo em memória + `threading`: sem Redis, banco ou Celery (o histórico some ao reiniciar).

## 1. Instalar
```bash
pip install -r requirements.txt
```

## 2. Configurar
```bash
cp .env.example .env
```
Preencha o `.env`. A `GEMINI_API_KEY` se obtém grátis em https://aistudio.google.com/apikey.
`UAZAPI_INSTANCE_TOKEN` é o token da instância (retornado em `POST /instance/init`).

## 3. Rodar
```bash
python app.py
```

## 4. Expor para a internet
```bash
ngrok http 5000
```

## 5. Configurar o webhook na UAZAPI
Conforme a seção "ENDPOINTS — WEBHOOK" do `llms-uazapi.txt` (`PUT /webhook`, header `token`):
```bash
curl -X PUT "$UAZAPI_BASE_URL/webhook" \
  -H "token: <INSTANCE_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"webhookUrl": "https://SEU-NGROK.ngrok.io/webhook", "events": ["message"]}'
```
Pronto: mande uma mensagem de outro número para o WhatsApp da instância.

## Como funciona
`POST /webhook` → ignora `fromMe`, grupos e tipos diferentes de `text` → `mark_read` → buffer por
usuário (espera `BUFFER_SECONDS` desde a última mensagem) → `flush`: `composing`, histórico,
Gemini, resposta dividida por `\n\n` (blocos > 800 chars são quebrados por frase) e enviada em
mensagens separadas, `paused` no fim.

## Adicionando tools no futuro
Em `llm.py`, `generate_reply` já recebe o parâmetro `tools` (hoje `None`). Basta passar
`tools=[types.Tool(function_declarations=[...])]` em `handle_flush` (`app.py`) e, em `llm.py`,
tratar `response.candidates[0].content.parts` procurando `part.function_call` (onde está o `TODO`):
executar a função, devolver o resultado como `part` de `function_response` no histórico e chamar o
modelo de novo até vir texto.

## Expandindo features
Consulte o `llms-uazapi.txt` para:
- receber mídia: `POST /send/download-media` (eventos `message` com `type` = image/audio/video/document)
- enviar imagem/áudio: `POST /send/image`, `POST /send/audio`
- botões interativos, listas e enquetes: `POST /send/menu` (respostas chegam como `button_reply`/`list_reply`)
- suporte a grupos (`isGroup`, `groupJid`) e endpoints `/group/*`
- chatbot nativo da UAZAPI: `/chatbot/*`
