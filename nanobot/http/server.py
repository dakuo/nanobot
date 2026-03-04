from __future__ import annotations

import secrets
import time
import uuid

from aiohttp import web
from loguru import logger


_CHAT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>nanobot chat</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#1a1a2e;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;height:100vh;display:flex;flex-direction:column}
#token-gate{display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:12px}
#token-gate input{padding:10px 16px;width:320px;border-radius:8px;border:1px solid #333;background:#16213e;color:#e0e0e0;font-size:14px}
#token-gate button{padding:10px 24px;border-radius:8px;border:none;background:#0f3460;color:#e0e0e0;cursor:pointer;font-size:14px}
#token-gate button:hover{background:#1a4a8a}
#chat-container{display:none;flex-direction:column;height:100vh}
#header{padding:10px 16px;background:#16213e;border-bottom:1px solid #333;font-size:13px;color:#888;display:flex;justify-content:space-between;align-items:center}
#header .title{font-weight:600;color:#e0e0e0;font-size:15px}
#header .session-id{font-size:11px;color:#666;max-width:50%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px}
#messages:empty::after{content:'No messages yet. Start a conversation below.';color:#555;align-self:center;margin-top:40vh;font-size:14px}
.msg{max-width:80%;padding:10px 14px;border-radius:12px;line-height:1.5;white-space:pre-wrap;word-wrap:break-word;font-size:14px}
.msg.user{align-self:flex-end;background:#0f3460;color:#e0e0e0}
.msg.assistant{align-self:flex-start;background:#16213e;border:1px solid #2a2a4a;color:#e0e0e0}
.msg.history{opacity:0.7}
.loading{align-self:flex-start;color:#666;font-style:italic;padding:10px 14px;font-size:13px}
#input-bar{display:flex;padding:12px;gap:8px;background:#16213e;border-top:1px solid #333}
#input-bar input{flex:1;padding:10px 14px;border-radius:8px;border:1px solid #333;background:#1a1a2e;color:#e0e0e0;font-size:14px;outline:none}
#input-bar input:focus{border-color:#0f3460}
#input-bar button{padding:10px 20px;border-radius:8px;border:none;background:#0f3460;color:#e0e0e0;cursor:pointer;font-size:14px}
#input-bar button:hover{background:#1a4a8a}
#input-bar button:disabled{opacity:.5;cursor:not-allowed}
#error-banner{display:none;padding:8px 16px;background:#4a1010;color:#ff6b6b;font-size:13px;text-align:center}
</style>
</head>
<body>
<div id="token-gate">
  <div style="font-size:24px;font-weight:600">&#x1f408; nanobot</div>
  <div style="color:#888;font-size:13px;margin-bottom:8px">Enter your API token to connect</div>
  <input id="token-input" type="password" placeholder="Bearer token" onkeydown="if(event.key==='Enter')connectWithToken()">
  <button onclick="connectWithToken()">Connect</button>
</div>
<div id="chat-container">
  <div id="header">
    <span class="title">&#x1f408; nanobot</span>
    <span class="session-id" id="session-label"></span>
  </div>
  <div id="error-banner"></div>
  <div id="messages"></div>
  <div id="input-bar">
    <input id="msg-input" placeholder="Type a message..." onkeydown="if(event.key==='Enter')sendMsg()">
    <button id="send-btn" onclick="sendMsg()">Send</button>
  </div>
</div>
<script>
let TOKEN = '';
let SESSION_KEY = '';
const params = new URLSearchParams(location.search);

// Auto-connect if token is in URL
(function init() {
  const urlToken = params.get('token');
  const urlSession = params.get('session');
  if (urlSession) SESSION_KEY = urlSession;
  if (urlToken) {
    TOKEN = urlToken;
    showChat();
    loadHistory();
  }
})();

function connectWithToken() {
  TOKEN = document.getElementById('token-input').value.trim();
  if (!TOKEN) return;
  showChat();
  loadHistory();
}

function showChat() {
  document.getElementById('token-gate').style.display = 'none';
  const c = document.getElementById('chat-container');
  c.style.display = 'flex';
  if (SESSION_KEY) {
    document.getElementById('session-label').textContent = SESSION_KEY;
  }
  document.getElementById('msg-input').focus();
}

function showError(msg) {
  const banner = document.getElementById('error-banner');
  banner.textContent = msg;
  banner.style.display = 'block';
  setTimeout(function() { banner.style.display = 'none'; }, 5000);
}

function renderMsg(role, content, isHistory) {
  const d = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'msg ' + role + (isHistory ? ' history' : '');
  el.textContent = content;
  d.appendChild(el);
  return el;
}

function scrollToBottom() {
  const d = document.getElementById('messages');
  d.scrollTop = d.scrollHeight;
}

// Track only new messages for the completions API context
const conversationMsgs = [];

async function loadHistory() {
  if (!SESSION_KEY) return;
  try {
    const r = await fetch('/api/session?key=' + encodeURIComponent(SESSION_KEY), {
      headers: { 'Authorization': 'Bearer ' + TOKEN }
    });
    if (!r.ok) {
      if (r.status === 401) showError('Invalid token');
      return;
    }
    const data = await r.json();
    const messages = data.messages || [];
    for (const m of messages) {
      renderMsg(m.role, m.content, true);
    }
    scrollToBottom();
  } catch (e) {
    console.error('Failed to load history:', e);
  }
}

async function sendMsg() {
  const inp = document.getElementById('msg-input');
  const text = inp.value.trim();
  if (!text) return;
  inp.value = '';

  renderMsg('user', text, false);
  conversationMsgs.push({ role: 'user', content: text });
  scrollToBottom();

  const btn = document.getElementById('send-btn');
  btn.disabled = true;
  inp.disabled = true;

  // Show typing indicator
  const d = document.getElementById('messages');
  const loading = document.createElement('div');
  loading.className = 'loading';
  loading.textContent = 'nanobot is thinking...';
  d.appendChild(loading);
  scrollToBottom();

  try {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + TOKEN
    };
    if (SESSION_KEY) {
      headers['x-nanobot-session-key'] = SESSION_KEY;
    }
    const r = await fetch('/v1/chat/completions', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ messages: conversationMsgs })
    });
    loading.remove();
    const j = await r.json();
    if (j.error) {
      showError(j.error);
      renderMsg('assistant', 'Error: ' + j.error, false);
    } else {
      const c = j.choices[0].message.content;
      conversationMsgs.push({ role: 'assistant', content: c });
      renderMsg('assistant', c, false);
    }
  } catch (e) {
    loading.remove();
    showError('Request failed: ' + e.message);
    renderMsg('assistant', 'Error: ' + e.message, false);
  }
  scrollToBottom();
  btn.disabled = false;
  inp.disabled = false;
  inp.focus();
}
</script>
</body>
</html>"""


_NO_AUTH_ROUTES = {("GET", "/api/health"), ("GET", "/chat")}


class HTTPServer:
    def __init__(self, agent, host: str, port: int, token: str) -> None:
        self.agent = agent
        self.host = host
        self.port = port
        if not token:
            token = secrets.token_urlsafe(32)
            logger.info("HTTP API token: {}", token)
        self.token = token
        self._runner: web.AppRunner | None = None

    @web.middleware
    async def _auth_middleware(self, request: web.Request, handler):
        key = (request.method, request.path)
        if key not in _NO_AUTH_ROUTES:
            auth = request.headers.get("Authorization", "")
            if auth != f"Bearer {self.token}":
                return web.json_response({"error": "Unauthorized"}, status=401)
        return await handler(request)

    async def _health(self, _request: web.Request) -> web.Response:
        return web.json_response({"status": "ok", "port": self.port})

    async def _get_session(self, request: web.Request) -> web.Response:
        """Return message history for a session."""
        key = request.query.get("key", "")
        if not key:
            return web.json_response({"error": "Missing 'key' parameter"}, status=400)

        session = self.agent.sessions.get_or_create(key)
        messages = []
        for m in session.messages:
            role = m.get("role")
            content = m.get("content", "")
            if role not in ("user", "assistant") or not content:
                continue
            # Skip assistant messages that were just tool-call wrappers (no text)
            if role == "assistant" and m.get("tool_calls") and not content:
                continue
            # Handle multimodal content (list of parts)
            if isinstance(content, list):
                text_parts = [p.get("text", "") for p in content if p.get("type") == "text"]
                content = "\n".join(t for t in text_parts if t)
                if not content:
                    continue
            if isinstance(content, str) and content.strip():
                messages.append({"role": role, "content": content.strip()})

        return web.json_response({"key": key, "messages": messages})

    async def _chat_completions(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()
            messages = body.get("messages", [])
            user_msg = ""
            for m in reversed(messages):
                if m.get("role") == "user":
                    user_msg = m.get("content", "")
                    break

            session_key = request.headers.get("x-nanobot-session-key", "http:direct")
            chat_id = session_key.split(":", 1)[-1]

            response = await self.agent.process_direct(
                content=user_msg,
                session_key=session_key,
                channel="http",
                chat_id=chat_id,
            )

            return web.json_response(
                {
                    "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": self.agent.model,
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": response},
                            "finish_reason": "stop",
                        }
                    ],
                }
            )
        except Exception as exc:
            logger.exception("chat completions error")
            return web.json_response({"error": str(exc)}, status=500)

    async def _chat_page(self, _request: web.Request) -> web.Response:
        return web.Response(text=_CHAT_HTML, content_type="text/html")

    async def start(self) -> None:
        app = web.Application(middlewares=[self._auth_middleware])
        app.router.add_get("/api/health", self._health)
        app.router.add_get("/api/session", self._get_session)
        app.router.add_post("/v1/chat/completions", self._chat_completions)
        app.router.add_get("/chat", self._chat_page)

        self._runner = web.AppRunner(app)
        runner = self._runner
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

    async def stop(self) -> None:
        if self._runner:
            await self._runner.cleanup()
            self._runner = None
