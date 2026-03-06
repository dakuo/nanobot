from __future__ import annotations

import asyncio
import json
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

/* --- Token gate --- */
#token-gate{display:flex;align-items:center;justify-content:center;height:100vh;flex-direction:column;gap:12px}
#token-gate input{padding:10px 16px;width:320px;border-radius:8px;border:1px solid #333;background:#16213e;color:#e0e0e0;font-size:14px}
#token-gate button{padding:10px 24px;border-radius:8px;border:none;background:#0f3460;color:#e0e0e0;cursor:pointer;font-size:14px}
#token-gate button:hover{background:#1a4a8a}

/* --- Main layout --- */
#app{display:none;flex-direction:row;height:100vh;width:100%}

/* --- Sidebar --- */
#sidebar{width:260px;min-width:200px;background:#12122a;border-right:1px solid #2a2a4a;display:flex;flex-direction:column;overflow:hidden}
#sidebar-header{padding:14px 16px;font-weight:600;font-size:15px;border-bottom:1px solid #2a2a4a;display:flex;justify-content:space-between;align-items:center}
#sidebar-header .count{font-size:12px;color:#666;font-weight:400}
#session-list{flex:1;overflow-y:auto;padding:6px 0}
.session-item{padding:10px 16px;cursor:pointer;border-left:3px solid transparent;transition:background .15s}
.session-item:hover{background:#1a1a3a}
.session-item.active{background:#0f3460;border-left-color:#4a9eff}
.session-item .label{font-size:13px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.session-item .meta{font-size:11px;color:#666;margin-top:2px;display:flex;justify-content:space-between}
.session-item .meta .msg-count{color:#4a9eff}

/* --- Chat panel --- */
#chat-panel{flex:1;display:flex;flex-direction:column;min-width:0}
#chat-header{padding:10px 16px;background:#16213e;border-bottom:1px solid #333;font-size:13px;color:#888;display:flex;justify-content:space-between;align-items:center}
#chat-header .title{font-weight:600;color:#e0e0e0;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:8px}
#empty-state{display:flex;align-items:center;justify-content:center;flex:1;color:#555;font-size:14px;text-align:center;padding:20px}
.msg{max-width:80%;padding:10px 14px;border-radius:12px;line-height:1.5;white-space:pre-wrap;word-wrap:break-word;font-size:14px}
.msg.user{align-self:flex-end;background:#0f3460;color:#e0e0e0}
.msg.assistant{align-self:flex-start;background:#16213e;border:1px solid #2a2a4a;color:#e0e0e0}
.loading{align-self:flex-start;color:#666;font-style:italic;padding:10px 14px;font-size:13px}
#input-bar{display:flex;padding:12px;gap:8px;background:#16213e;border-top:1px solid #333}
#input-bar input{flex:1;padding:10px 14px;border-radius:8px;border:1px solid #333;background:#1a1a2e;color:#e0e0e0;font-size:14px;outline:none}
#input-bar input:focus{border-color:#0f3460}
#input-bar button{padding:10px 20px;border-radius:8px;border:none;background:#0f3460;color:#e0e0e0;cursor:pointer;font-size:14px}
#input-bar button:hover{background:#1a4a8a}
#input-bar button:disabled{opacity:.5;cursor:not-allowed}
#error-banner{display:none;padding:8px 16px;background:#4a1010;color:#ff6b6b;font-size:13px;text-align:center}
#agent-panel{height:0;overflow:hidden;transition:height .3s;background:#12122a;border-top:1px solid #2a2a4a;display:flex;flex-direction:column}
#agent-panel.open{height:240px}
#agent-toggle{padding:6px 16px;background:#16213e;border-top:1px solid #333;cursor:pointer;font-size:12px;color:#888;display:flex;justify-content:space-between;align-items:center;user-select:none}
#agent-toggle:hover{background:#1a1a3a}
#agent-toggle .badge{background:#0f3460;color:#4a9eff;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px}
#agent-events{flex:1;overflow-y:auto;padding:8px 16px;font-family:'SF Mono',Monaco,monospace;font-size:12px;line-height:1.6}
.agent-evt{padding:2px 0;border-bottom:1px solid #1a1a2e}
.agent-evt .time{color:#555;margin-right:8px}
.agent-evt .label{color:#4a9eff;font-weight:500;margin-right:6px}
.agent-evt .tool{color:#c4f042}
.agent-evt .status-ok{color:#4ade80}
.agent-evt .status-error{color:#ff6b6b}
.agent-evt .preview{color:#888;margin-left:4px}
</style>
</head>
<body>

<div id="token-gate">
  <div style="font-size:24px;font-weight:600">&#x1f408; nanobot</div>
  <div style="color:#888;font-size:13px;margin-bottom:8px">Enter your API token to connect</div>
  <input id="token-input" type="password" placeholder="Bearer token" onkeydown="if(event.key==='Enter')connectWithToken()">
  <button onclick="connectWithToken()">Connect</button>
  <div id="gate-error" style="color:#ff6b6b;font-size:12px;display:none"></div>
</div>

<div id="app">
  <div id="sidebar">
    <div id="sidebar-header">
      <span>&#x1f408; nanobot</span>
      <span class="count" id="total-count"></span>
    </div>
    <div id="session-list"></div>
  </div>
  <div id="chat-panel">
    <div id="chat-header">
      <span class="title" id="chat-title">Select a session</span>
    </div>
    <div id="error-banner"></div>
    <div id="empty-state">Select a session from the sidebar to view messages.</div>
    <div id="messages" style="display:none"></div>
    <div id="agent-toggle" onclick="toggleAgentPanel()">
      <span>&#x1f527; Agent Activity <span id="agent-badge" class="badge" style="display:none">0</span></span>
      <span id="agent-arrow">&#x25B2;</span>
    </div>
    <div id="agent-panel">
      <div id="agent-events"></div>
    </div>
    <div id="input-bar">
      <input id="msg-input" placeholder="Type a message..." onkeydown="if(event.key==='Enter')sendMsg()" disabled>
      <button id="send-btn" onclick="sendMsg()" disabled>Send</button>
    </div>
  </div>
</div>

<script>
let TOKEN = '';
let SESSION_KEY = '';
const params = new URLSearchParams(location.search);
const conversationMsgs = [];

// ---- Init ----
(function init() {
  const urlToken = params.get('token');
  const urlSession = params.get('session');
  if (urlSession) SESSION_KEY = urlSession;
  if (urlToken) {
    TOKEN = urlToken;
    enterApp();
  }
})();

function connectWithToken() {
  TOKEN = document.getElementById('token-input').value.trim();
  if (!TOKEN) return;
  enterApp();
}

async function enterApp() {
  // Verify token works before showing app
  try {
    const r = await fetch('/api/sessions', {
      headers: { 'Authorization': 'Bearer ' + TOKEN }
    });
    if (r.status === 401) {
      const ge = document.getElementById('gate-error');
      ge.textContent = 'Invalid token';
      ge.style.display = 'block';
      return;
    }
  } catch (e) {
    // If /api/sessions fails, still enter - might be older server
  }

  document.getElementById('token-gate').style.display = 'none';
  document.getElementById('app').style.display = 'flex';
  await loadSessions();

  connectSSE();

  if (SESSION_KEY) {
    selectSession(SESSION_KEY);
  }
}

// ---- Sidebar ----
async function loadSessions() {
  try {
    const r = await fetch('/api/sessions', {
      headers: { 'Authorization': 'Bearer ' + TOKEN }
    });
    if (!r.ok) return;
    const data = await r.json();
    const sessions = data.sessions || [];
    const list = document.getElementById('session-list');
    list.innerHTML = '';

    let totalMsgs = 0;
    for (const s of sessions) {
      totalMsgs += s.message_count || 0;
      const div = document.createElement('div');
      div.className = 'session-item' + (s.key === SESSION_KEY ? ' active' : '');
      div.dataset.key = s.key;
      div.onclick = function() { selectSession(s.key); };

      const label = document.createElement('div');
      label.className = 'label';
      label.textContent = s.key;
      div.appendChild(label);

      const meta = document.createElement('div');
      meta.className = 'meta';
      const count = document.createElement('span');
      count.className = 'msg-count';
      count.textContent = (s.message_count || 0) + ' msgs';
      const updated = document.createElement('span');
      updated.textContent = s.updated_at ? new Date(s.updated_at).toLocaleDateString() : '';
      meta.appendChild(count);
      meta.appendChild(updated);
      div.appendChild(meta);

      list.appendChild(div);
    }

    document.getElementById('total-count').textContent =
      sessions.length + ' sessions, ' + totalMsgs + ' msgs';
  } catch (e) {
    console.error('Failed to load sessions:', e);
  }
}

async function selectSession(key) {
  SESSION_KEY = key;
  conversationMsgs.length = 0;

  // Update sidebar active state
  document.querySelectorAll('.session-item').forEach(function(el) {
    el.classList.toggle('active', el.dataset.key === key);
  });

  // Update URL without reload
  const url = new URL(location);
  url.searchParams.set('session', key);
  if (TOKEN) url.searchParams.set('token', TOKEN);
  history.replaceState(null, '', url);

  // Update header
  document.getElementById('chat-title').textContent = key;

  // Show messages panel, hide empty state
  document.getElementById('empty-state').style.display = 'none';
  const msgDiv = document.getElementById('messages');
  msgDiv.style.display = 'flex';
  msgDiv.innerHTML = '';

  // Enable input
  document.getElementById('msg-input').disabled = false;
  document.getElementById('send-btn').disabled = false;

  // Load messages
  await loadHistory();
  document.getElementById('msg-input').focus();
}

// ---- Messages ----
function showError(msg) {
  const banner = document.getElementById('error-banner');
  banner.textContent = msg;
  banner.style.display = 'block';
  setTimeout(function() { banner.style.display = 'none'; }, 5000);
}

function renderMsg(role, content) {
  const d = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = 'msg ' + role;
  el.textContent = content;
  d.appendChild(el);
  return el;
}

function scrollToBottom() {
  const d = document.getElementById('messages');
  d.scrollTop = d.scrollHeight;
}

async function loadHistory() {
  if (!SESSION_KEY) return;
  try {
    const r = await fetch('/api/session?key=' + encodeURIComponent(SESSION_KEY), {
      headers: { 'Authorization': 'Bearer ' + TOKEN }
    });
    if (!r.ok) {
      if (r.status === 401) showError('Invalid token');
      else showError('Failed to load session (HTTP ' + r.status + ')');
      return;
    }
    const data = await r.json();
    const messages = data.messages || [];
    for (const m of messages) {
      renderMsg(m.role, m.content);
    }
    if (messages.length === 0) {
      const d = document.getElementById('messages');
      const hint = document.createElement('div');
      hint.style.cssText = 'color:#555;align-self:center;margin-top:20vh;font-size:14px';
      hint.textContent = 'No messages in this session yet.';
      d.appendChild(hint);
    }
    scrollToBottom();
  } catch (e) {
    showError('Failed to load history: ' + e.message);
  }
}

async function sendMsg() {
  const inp = document.getElementById('msg-input');
  const text = inp.value.trim();
  if (!text || !SESSION_KEY) return;
  inp.value = '';

  renderMsg('user', text);
  conversationMsgs.push({ role: 'user', content: text });
  scrollToBottom();

  const btn = document.getElementById('send-btn');
  btn.disabled = true;
  inp.disabled = true;

  const d = document.getElementById('messages');
  const loading = document.createElement('div');
  loading.className = 'loading';
  loading.textContent = 'nanobot is thinking...';
  d.appendChild(loading);
  scrollToBottom();

  try {
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + TOKEN,
      'x-nanobot-session-key': SESSION_KEY
    };
    const r = await fetch('/v1/chat/completions', {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ messages: conversationMsgs })
    });
    loading.remove();
    const j = await r.json();
    if (j.error) {
      showError(j.error);
      renderMsg('assistant', 'Error: ' + j.error);
    } else {
      const c = j.choices[0].message.content;
      conversationMsgs.push({ role: 'assistant', content: c });
      renderMsg('assistant', c);
    }
  } catch (e) {
    loading.remove();
    showError('Request failed: ' + e.message);
    renderMsg('assistant', 'Error: ' + e.message);
  }
  scrollToBottom();
  btn.disabled = false;
  inp.disabled = false;
  inp.focus();
}

let evtSource = null;
const activeAgents = {};

function connectSSE() {
  if (evtSource) evtSource.close();
  evtSource = new EventSource('/api/events?token=' + encodeURIComponent(TOKEN));
  evtSource.onmessage = function(e) {
    try { renderAgentEvent(JSON.parse(e.data)); } catch(err) {}
  };
  evtSource.onerror = function() {
    setTimeout(connectSSE, 3000);
  };
}

function renderAgentEvent(evt) {
  var div = document.getElementById('agent-events');
  var el = document.createElement('div');
  el.className = 'agent-evt';
  var time = new Date(evt.timestamp * 1000).toLocaleTimeString();
  if (evt.type === 'start') {
    activeAgents[evt.task_id] = evt.label;
    el.innerHTML = '<span class="time">' + time + '</span><span class="label">[' + evt.label + ']</span> started';
  } else if (evt.type === 'tool_call') {
    var label = activeAgents[evt.task_id] || evt.task_id;
    el.innerHTML = '<span class="time">' + time + '</span><span class="label">[' + label + ']</span> <span class="tool">' + evt.tool + '</span><span class="preview"> ' + (evt.args_preview || '').substring(0, 120) + '</span>';
  } else if (evt.type === 'tool_result') {
    var label = activeAgents[evt.task_id] || evt.task_id;
    el.innerHTML = '<span class="time">' + time + '</span><span class="label">[' + label + ']</span> <span class="tool">' + evt.tool + '</span> &#x2192; <span class="preview">' + (evt.result_preview || '').substring(0, 100) + '</span>';
  } else if (evt.type === 'thinking') {
    var label = activeAgents[evt.task_id] || evt.task_id;
    el.innerHTML = '<span class="time">' + time + '</span><span class="label">[' + label + ']</span> &#x1F4AD; <span class="preview">' + (evt.content_preview || '').substring(0, 150) + '</span>';
  } else if (evt.type === 'complete') {
    var label = activeAgents[evt.task_id] || evt.label || evt.task_id;
    var cls = evt.status === 'ok' ? 'status-ok' : 'status-error';
    el.innerHTML = '<span class="time">' + time + '</span><span class="label">[' + label + ']</span> <span class="' + cls + '">' + (evt.status === 'ok' ? '&#x2713; done' : '&#x2717; failed') + '</span>';
    delete activeAgents[evt.task_id];
  }
  div.appendChild(el);
  div.scrollTop = div.scrollHeight;
  updateBadge();
}

function updateBadge() {
  var badge = document.getElementById('agent-badge');
  var count = Object.keys(activeAgents).length;
  if (count > 0) {
    badge.textContent = count + ' active';
    badge.style.display = 'inline';
  } else {
    badge.style.display = 'none';
  }
}

function toggleAgentPanel() {
  var panel = document.getElementById('agent-panel');
  var arrow = document.getElementById('agent-arrow');
  panel.classList.toggle('open');
  arrow.innerHTML = panel.classList.contains('open') ? '&#x25BC;' : '&#x25B2;';
}
</script>
</body>
</html>"""


_NO_AUTH_ROUTES = {("GET", "/api/health"), ("GET", "/chat"), ("GET", "/api/events")}


def _extract_visible_messages(session) -> list[dict]:
    """Extract user/assistant messages from a session, filtering tool calls."""
    messages = []
    for m in session.messages:
        role = m.get("role")
        content = m.get("content", "")
        if role not in ("user", "assistant") or not content:
            continue
        if role == "assistant" and m.get("tool_calls") and not content:
            continue
        if isinstance(content, list):
            text_parts = [p.get("text", "") for p in content if p.get("type") == "text"]
            content = "\n".join(t for t in text_parts if t)
            if not content:
                continue
        if isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content.strip()})
    return messages


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

    async def _list_sessions(self, _request: web.Request) -> web.Response:
        """List all sessions with message counts."""
        raw = self.agent.sessions.list_sessions()
        sessions = []
        for info in raw:
            key = info.get("key", "")
            session = self.agent.sessions.get_or_create(key)
            visible = _extract_visible_messages(session)
            sessions.append(
                {
                    "key": key,
                    "message_count": len(visible),
                    "updated_at": info.get("updated_at"),
                    "created_at": info.get("created_at"),
                }
            )
        return web.json_response({"sessions": sessions})

    async def _get_session(self, request: web.Request) -> web.Response:
        """Return message history for a session."""
        key = request.query.get("key", "")
        if not key:
            return web.json_response({"error": "Missing 'key' parameter"}, status=400)

        session = self.agent.sessions.get_or_create(key)
        messages = _extract_visible_messages(session)
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

    async def _events_stream(self, request: web.Request) -> web.StreamResponse:
        """SSE endpoint streaming subagent events in real-time."""
        token = request.query.get("token", "")
        if token != self.token:
            return web.json_response({"error": "Unauthorized"}, status=401)

        response = web.StreamResponse(
            status=200,
            reason="OK",
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            },
        )
        await response.prepare(request)

        queue = self.agent.subagents.subscribe_events()
        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    data = json.dumps(event, ensure_ascii=False)
                    await response.write(f"data: {data}\n\n".encode())
                except asyncio.TimeoutError:
                    await response.write(b": keepalive\n\n")
                except ConnectionResetError:
                    break
        finally:
            self.agent.subagents.unsubscribe_events(queue)
        return response

    async def _chat_page(self, _request: web.Request) -> web.Response:
        return web.Response(text=_CHAT_HTML, content_type="text/html")

    async def start(self) -> None:
        app = web.Application(middlewares=[self._auth_middleware])
        app.router.add_get("/api/health", self._health)
        app.router.add_get("/api/sessions", self._list_sessions)
        app.router.add_get("/api/session", self._get_session)
        app.router.add_post("/v1/chat/completions", self._chat_completions)
        app.router.add_get("/api/events", self._events_stream)
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
