<div align="center">
  <img src="nanobot_logo.png" alt="nanobot" width="500">
  <h1>nanobot: Ultra-Lightweight Personal AI Assistant</h1>
  <p>
    <a href="https://pypi.org/project/nanobot-ai/"><img src="https://img.shields.io/pypi/v/nanobot-ai" alt="PyPI"></a>
    <a href="https://pepy.tech/project/nanobot-ai"><img src="https://static.pepy.tech/badge/nanobot-ai" alt="Downloads"></a>
    <img src="https://img.shields.io/badge/python-≥3.11-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/Feishu-Group-E9DBFC?style=flat&logo=feishu&logoColor=white" alt="Feishu"></a>
    <a href="./COMMUNICATION.md"><img src="https://img.shields.io/badge/WeChat-Group-C5EAB4?style=flat&logo=wechat&logoColor=white" alt="WeChat"></a>
    <a href="https://discord.gg/MnCvHqpUGB"><img src="https://img.shields.io/badge/Discord-Community-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"></a>
  </p>
</div>

🐈 **nanobot** is an **ultra-lightweight** personal AI assistant inspired by [OpenClaw](https://github.com/openclaw/openclaw).

⚡️ Delivers core agent functionality with **99% fewer lines of code** than OpenClaw.

📏 Real-time line count: run `bash core_agent_lines.sh` to verify anytime.

> **Fork note**: This is a research fork by [Dakuo Wang](https://github.com/dakuow) that adds an [R01 Proposal Multi-Agent System](#r01-proposal-multi-agent-system) on top of the upstream [HKUDS/nanobot](https://github.com/HKUDS/nanobot) codebase.

## 📢 Fork Development Log

- **2026-03-06** Fixed PI publication search bug — literature agents now mandatory-cite 5+ PI papers and 3+ per co-PI. Added investigator verification gate that blocks the pipeline until all PIs are confirmed. Merged upstream HKUDS/nanobot (lazy imports, MCP SSE transport, Telegram streaming, Discord group policy). Generated missing healthcare and AI reference files.
- **2026-03-05** Built complete R01 multi-agent pipeline with 16 specialized skills. Implemented parallel literature search with citation graph traversal and snowball sampling. Added evolution system for learning from reviewer feedback across projects. Created writing voice calibration and domain-specific style guides. Built reviewer panel simulation with 3 domain reviewers plus panel synthesizer. Added subagent activity dashboard (HTTP API). Pushed 14 atomic commits.
- **2026-03-04** Added AWS Bedrock provider with env-based auth. Fixed Slack thread handling for DM threads. Implemented Exa search as fallback for Brave Search. Added Anthropic OAuth provider. Fixed media block handling for Bedrock compatibility.

<details>
<summary>Upstream news (HKUDS/nanobot)</summary>

- **2026-02-28** 🚀 Released **v0.1.4.post3** — cleaner context, hardened session history, and smarter agent. Please see [release notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post3) for details.
- **2026-02-27** 🧠 Experimental thinking mode support, DingTalk media messages, Feishu and QQ channel fixes.
- **2026-02-26** 🛡️ Session poisoning fix, WhatsApp dedup, Windows path guard, Mistral compatibility.
- **2026-02-25** 🧹 New Matrix channel, cleaner session context, auto workspace template sync.
- **2026-02-24** 🚀 Released **v0.1.4.post2** — a reliability-focused release with a redesigned heartbeat, prompt cache optimization, and hardened provider & channel stability. See [release notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post2) for details.
- **2026-02-23** 🔧 Virtual tool-call heartbeat, prompt cache optimization, Slack mrkdwn fixes.
- **2026-02-22** 🛡️ Slack thread isolation, Discord typing fix, agent reliability improvements.
- **2026-02-21** 🎉 Released **v0.1.4.post1** — new providers, media support across channels, and major stability improvements. See [release notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4.post1) for details.
- **2026-02-20** 🐦 Feishu now receives multimodal files from users. More reliable memory under the hood.
- **2026-02-19** ✨ Slack now sends files, Discord splits long messages, and subagents work in CLI mode.

<details>
<summary>Earlier upstream news</summary>

- **2026-02-18** ⚡️ nanobot now supports VolcEngine, MCP custom auth headers, and Anthropic prompt caching.
- **2026-02-17** 🎉 Released **v0.1.4** — MCP support, progress streaming, new providers, and multiple channel improvements. Please see [release notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.4) for details.
- **2026-02-16** 🦞 nanobot now integrates a [ClawHub](https://clawhub.ai) skill — search and install public agent skills.
- **2026-02-15** 🔑 nanobot now supports OpenAI Codex provider with OAuth login support.
- **2026-02-14** 🔌 nanobot now supports MCP! See [MCP section](#mcp-model-context-protocol) for details.
- **2026-02-13** 🎉 Released **v0.1.3.post7** — includes security hardening and multiple improvements. **Please upgrade to the latest version to address security issues**. See [release notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post7) for more details.
- **2026-02-12** 🧠 Redesigned memory system — Less code, more reliable. Join the [discussion](https://github.com/HKUDS/nanobot/discussions/566) about it!
- **2026-02-11** ✨ Enhanced CLI experience and added MiniMax support!
- **2026-02-10** 🎉 Released **v0.1.3.post6** with improvements! Check the updates [notes](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post6) and our [roadmap](https://github.com/HKUDS/nanobot/discussions/431).
- **2026-02-09** 💬 Added Slack, Email, and QQ support — nanobot now supports multiple chat platforms!
- **2026-02-08** 🔧 Refactored Providers—adding a new LLM provider now takes just 2 simple steps! Check [here](#providers).
- **2026-02-07** 🚀 Released **v0.1.3.post5** with Qwen support & several key improvements! Check [here](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post5) for details.
- **2026-02-06** ✨ Added Moonshot/Kimi provider, Discord integration, and enhanced security hardening!
- **2026-02-05** ✨ Added Feishu channel, DeepSeek provider, and enhanced scheduled tasks support!
- **2026-02-04** 🚀 Released **v0.1.3.post4** with multi-provider & Docker support! Check [here](https://github.com/HKUDS/nanobot/releases/tag/v0.1.3.post4) for details.
- **2026-02-03** ⚡ Integrated vLLM for local LLM support and improved natural language task scheduling!
- **2026-02-02** 🎉 nanobot officially launched! Welcome to try 🐈 nanobot!

</details>

</details>

## Key Features of nanobot:

🪶 **Ultra-Lightweight**: Just ~4,000 lines of core agent code — 99% smaller than Clawdbot.

🔬 **Research-Ready**: Clean, readable code that's easy to understand, modify, and extend for research.

⚡️ **Lightning Fast**: Minimal footprint means faster startup, lower resource usage, and quicker iterations.

💎 **Easy-to-Use**: One-click to deploy and you're ready to go.

## 🏗️ Architecture

<p align="center">
  <img src="nanobot_arch.png" alt="nanobot architecture" width="800">
</p>

---

## R01 Proposal Multi-Agent System

This fork adds a complete NIH R01 proposal auto-generation system built on nanobot's subagent infrastructure. Sixteen specialized agents work together in a phased pipeline to produce a full 15-page Research Strategy, Project Summary, Project Narrative, and Budget Justification — targeting human-centered AI research proposals that span HCI, Healthcare, and AI/ML domains.

The system is designed around a real research workflow: the PI interacts at three checkpoints (idea selection, outline review, draft feedback), while agents handle the literature search, writing, review simulation, and revision in parallel. After each project, an evolution agent extracts patterns from reviewer feedback and updates the shared style guides for future runs.

### Pipeline Architecture

```
                    ┌──────────────────────────────────────┐
                    │           r01-orchestrator            │
                    │    State machine + phase dispatch     │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
   Phase 1: Init              Phase 1.5: Gate               Phase 2: Ideation
   Setup workspace            Investigator                  ┌──────────────────┐
   Load PI profile            Verification                  │   r01-ideation   │
   Init state.json            (blocks until                 │  Tree-search     │
                              PIs confirmed)                │  hypothesis gen  │
                                                            └────────┬─────────┘
                                                                     │
                                                            ┌────────▼─────────┐
                                                            │ r01-novelty-     │
                                                            │ checker          │
                                                            │ Multi-round lit  │
                                                            │ search + overlap │
                                                            └────────┬─────────┘
                                                                     │
                                                         [PI selects idea]
                                                                     │
                              Phase 3: Literature (PARALLEL)         │
          ┌───────────────────────────────────────────────────────── ▼ ──────┐
          │                          │                          │             │
  ┌───────┴──────┐          ┌────────┴─────┐          ┌────────┴──────┐      │
  │ r01-lit-hci  │          │ r01-lit-      │          │ r01-lit-ai    │      │
  │ ACM DL       │          │ healthcare    │          │ arXiv         │      │
  │ CHI/CSCW     │          │ PubMed        │          │ Papers w/Code │      │
  │ snowball     │          │ ClinicalTrials│          │ snowball      │      │
  └──────┬───────┘          └──────┬────────┘          └──────┬────────┘      │
         └──────────────────┬──────┘───────────────────────────┘              │
                            │  Merge + dedup (30-50 refs)                     │
                            ▼                                                  │
                   ┌────────────────┐                                          │
                   │ r01-writer-    │  Phase 4: Outline                        │
                   │ integrator     │  3-pass skeleton → detail → review       │
                   └────────┬───────┘                                          │
                            │  [PI reviews outline]                            │
                            │                                                  │
                            │  Phase 5: Writing (PARALLEL)                     │
          ┌─────────────────┼──────────────────────────────────┐               │
          │                 │                 │                 │               │
  ┌───────┴──────┐  ┌───────┴──────┐  ┌──────┴───────┐  ┌─────┴────────┐      │
  │ r01-writer-  │  │ r01-writer-  │  │ r01-writer-  │  │ r01-writer-  │      │
  │ hci          │  │ healthcare   │  │ ai           │  │ integrator   │      │
  │ Aim 1 draft  │  │ Aim 3 draft  │  │ Aim 2 draft  │  │ Significance │      │
  │ CHI voice    │  │ Clinical     │  │ NeurIPS      │  │ Innovation   │      │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬────────┘      │
         └─────────────────┴──────────────────┴────────────────┘               │
                            │  Assemble research_strategy_v1.md                │
                            │                                                  │
                   Phase 6  │                                                  │
          ┌─────────────────┼──────────────────┐                               │
          │                                    │                               │
  ┌───────┴──────┐                    ┌────────┴──────┐                        │
  │ r01-figures  │                    │ r01-budget    │                        │
  │ matplotlib   │                    │ NIH format    │                        │
  │ VLM review   │                    │ 5-year table  │                        │
  └──────┬───────┘                    └────────┬──────┘                        │
         └─────────────────┬──────────────────┘                                │
                           │                                                   │
                           │  Phase 7: Review (PARALLEL)                       │
          ┌────────────────┼──────────────────────────────┐                    │
          │                │                              │                    │
  ┌───────┴──────┐  ┌──────┴───────┐             ┌───────┴──────┐             │
  │ r01-reviewer │  │ r01-reviewer │             │ r01-reviewer │             │
  │ -hci         │  │ -healthcare  │             │ -ai          │             │
  │ Dual-bias    │  │ Dual-bias    │             │ Dual-bias    │             │
  │ + reflection │  │ + reflection │             │ + reflection │             │
  └──────┬───────┘  └──────┬───────┘             └──────┬───────┘             │
         └─────────────────┴──────────────────────────── ┘                    │
                           │  (then sequential)                                │
                  ┌────────▼────────┐                                          │
                  │ r01-reviewer-   │                                          │
                  │ panel           │                                          │
                  │ 4-persona sim   │                                          │
                  │ Impact score    │                                          │
                  └────────┬────────┘                                          │
                           │  score < 5 and rounds remain?                     │
                           │                                                   │
                  ┌────────▼────────┐                                          │
                  │  r01-reviser    │  Phase 8: Revision                       │
                  │  Diff tracking  │  Self-generated plan                     │
                  │  Word budget    │  23 priority items                       │
                  └────────┬────────┘                                          │
                           │  loop back to Phase 7 if needed                  │
                           │                                                   │
                  ┌────────▼────────┐                                          │
                  │  Export         │  Phase 9: Final assembly                 │
                  │  research_      │  research_strategy_v2.md                 │
                  │  strategy_v2.md │  package manifest                        │
                  └────────┬────────┘                                          │
                           │                                                   │
                  ┌────────▼────────┐                                          │
                  │ r01-evolution   │  Phase 10: Learn                         │
                  │ Pattern extract │  Update reviewer_patterns.json           │
                  │ Style proposals │  Propose style_guide.md changes          │
                  └─────────────────┘                                          │
                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Skills Reference

All 16 skills ship as built-in nanobot skills in `nanobot/skills/` and are auto-discovered on startup.

| Skill | Role |
|-------|------|
| `r01-orchestrator` | Central state machine — dispatches all phases, manages user checkpoints, collects agent learnings |
| `r01-ideation` | Tree-search hypothesis generation with 5-step DIVERGE/DEVELOP/FILTER/CONVERGE/CHECKPOINT pipeline |
| `r01-novelty-checker` | Multi-round Semantic Scholar + web search; 4-level overlap classification; verdict categories |
| `r01-literature` | Domain-parameterized literature agent (hci/healthcare/ai); snowball sampling; claim-evidence mapping; contradiction detection |
| `r01-writer-hci` | HCI domain writer with CHI/CSCW voice calibration and agent learnings output |
| `r01-writer-healthcare` | Healthcare domain writer with clinical/regulatory voice and NEJM/JAMA conventions |
| `r01-writer-ai` | AI/ML domain writer with NeurIPS/ICML voice, baseline comparisons, anti-hype language guide |
| `r01-writer-integrator` | Cross-domain synthesis; 3-pass outline refinement; word-target feedback loop; terminology concordance |
| `r01-reviewer-hci` | Simulated HCI reviewer; dual-bias protocol (critical + supportive passes); reflection loop; scratchpad |
| `r01-reviewer-healthcare` | Simulated healthcare reviewer; PubMed/ClinicalTrials.gov background retrieval; dual-bias; reflection |
| `r01-reviewer-ai` | Simulated AI/ML reviewer; arXiv/Papers With Code background retrieval; dual-bias; reflection |
| `r01-reviewer-panel` | 4-persona panel simulation (Senior Methodologist, Clinical Champion, Innovation Advocate, Devil's Advocate); overall impact score 1-9 |
| `r01-reviser` | Self-generated revision plan with dependency graph; diff tracking; word budget reconciliation |
| `r01-figures` | matplotlib figure generation from YAML specs; VLM quality review loop; SVG + 300 DPI PNG export |
| `r01-budget` | NIH budget table (5-year, direct cost cap); personnel, equipment, travel, F&A justification |
| `r01-evolution` | Cross-project learning loop; extracts reviewer patterns; proposes style guide updates with user approval |

There's also `r01-foa-finder` for locating relevant NIH Funding Opportunity Announcements.

### Key Features

**PI publication awareness.** The investigator verification gate (Phase 1.5) confirms all PIs before the pipeline proceeds. Literature agents are required to cite 5+ PI papers and 3+ per co-PI, so the proposal reflects the team's actual research trajectory rather than generic background.

**Three-tier voice calibration.** Writers read a hierarchy of style files: domain-specific voice (`writing_voice_hci.md`) overrides generic PI voice (`writing_voice.md`), which overrides NIH conventions (`style_guide.md`). Voice files are seeded from real prior proposals and update automatically from feedback.

**Evolution system.** After each completed project, `r01-evolution` extracts patterns from reviewer scores and revision diffs, updates `reviewer_patterns.json`, and proposes changes to the shared style guide. Patterns that appear 3+ times across projects get promoted automatically.

**Reviewer panel simulation.** Four distinct reviewer personas debate the proposal before producing a consensus impact score. The panel tracks score trajectories across revision rounds and maintains a priority matrix (impact vs. effort) for revision guidance.

**Workspace override for subagents.** Each spawned subagent writes to a configurable shared workspace (default: `~/Dropbox/AgentWorkspace/PaperAutoGen/{project}/`). Paths are set in `project.yaml` per project, not hardcoded.

### Quick Start

```bash
# 1. Clone this fork and install
git clone https://github.com/dakuow/nanobot.git
cd nanobot
pip install -e .

# 2. Set up shared workspace
mkdir -p ~/Dropbox/AgentWorkspace/PaperAutoGen
mkdir -p ~/Dropbox/AgentWorkspace/PriorNIHR01Examples
cp -r r01-proposal/workspace/_templates ~/Dropbox/AgentWorkspace/PaperAutoGen/
cp -r r01-proposal/workspace/_system ~/Dropbox/AgentWorkspace/PaperAutoGen/

# 3. Create a project
mkdir -p ~/Dropbox/AgentWorkspace/PaperAutoGen/my-project
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/project.yaml \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-project/
cp ~/Dropbox/AgentWorkspace/PaperAutoGen/_templates/state.json \
   ~/Dropbox/AgentWorkspace/PaperAutoGen/my-project/
# Edit project.yaml with your research topic, aims, and team

# 4. Run
nanobot agent -m "Start R01 pipeline for my-project"
```

See [r01-proposal/PLAN.md](./r01-proposal/PLAN.md) for the full architecture, phase status, and design decisions.

---

## ✨ Features

<table align="center">
  <tr align="center">
    <th><p align="center">📈 24/7 Real-Time Market Analysis</p></th>
    <th><p align="center">🚀 Full-Stack Software Engineer</p></th>
    <th><p align="center">📅 Smart Daily Routine Manager</p></th>
    <th><p align="center">📚 Personal Knowledge Assistant</p></th>
  </tr>
  <tr>
    <td align="center"><p align="center"><img src="case/search.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/code.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/scedule.gif" width="180" height="400"></p></td>
    <td align="center"><p align="center"><img src="case/memory.gif" width="180" height="400"></p></td>
  </tr>
  <tr>
    <td align="center">Discovery • Insights • Trends</td>
    <td align="center">Develop • Deploy • Scale</td>
    <td align="center">Schedule • Automate • Organize</td>
    <td align="center">Learn • Memory • Reasoning</td>
  </tr>
</table>

## 📦 Install

**Install from source** (latest features, recommended for development)

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
pip install -e .
```

**Install with [uv](https://github.com/astral-sh/uv)** (stable, fast)

```bash
uv tool install nanobot-ai
```

**Install from PyPI** (stable)

```bash
pip install nanobot-ai
```

## 🚀 Quick Start

> [!TIP]
> Set your API key in `~/.nanobot/config.json`.
> Get API keys: [OpenRouter](https://openrouter.ai/keys) (Global) · [Brave Search](https://brave.com/search/api/) (optional, for web search)

**1. Initialize**

```bash
nanobot onboard
```

**2. Configure** (`~/.nanobot/config.json`)

Add or merge these **two parts** into your config (other options have defaults).

*Set your API key* (e.g. OpenRouter, recommended for global users):
```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  }
}
```

*Set your model* (optionally pin a provider — defaults to auto-detection):
```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

**3. Chat**

```bash
nanobot agent
```

That's it! You have a working AI assistant in 2 minutes.

## 💬 Chat Apps

Connect nanobot to your favorite chat platform.

| Channel | What you need |
|---------|---------------|
| **Telegram** | Bot token from @BotFather |
| **Discord** | Bot token + Message Content intent |
| **WhatsApp** | QR code scan |
| **Feishu** | App ID + App Secret |
| **Mochat** | Claw token (auto-setup available) |
| **DingTalk** | App Key + App Secret |
| **Slack** | Bot token + App-Level token |
| **Email** | IMAP/SMTP credentials |
| **QQ** | App ID + App Secret |

<details>
<summary><b>Telegram</b> (Recommended)</summary>

**1. Create a bot**
- Open Telegram, search `@BotFather`
- Send `/newbot`, follow prompts
- Copy the token

**2. Configure**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

> You can find your **User ID** in Telegram settings. It is shown as `@yourUserId`.
> Copy this value **without the `@` symbol** and paste it into the config file.


**3. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Mochat (Claw IM)</b></summary>

Uses **Socket.IO WebSocket** by default, with HTTP polling fallback.

**1. Ask nanobot to set up Mochat for you**

Simply send this message to nanobot (replace `xxx@xxx` with your real email):

```
Read https://raw.githubusercontent.com/HKUDS/MoChat/refs/heads/main/skills/nanobot/skill.md and register on MoChat. My Email account is xxx@xxx Bind me as your owner and DM me on MoChat.
```

nanobot will automatically register, configure `~/.nanobot/config.json`, and connect to Mochat.

**2. Restart gateway**

```bash
nanobot gateway
```

That's it — nanobot handles the rest!

<br>

<details>
<summary>Manual configuration (advanced)</summary>

If you prefer to configure manually, add the following to `~/.nanobot/config.json`:

> Keep `claw_token` private. It should only be sent in `X-Claw-Token` header to your Mochat API endpoint.

```json
{
  "channels": {
    "mochat": {
      "enabled": true,
      "base_url": "https://mochat.io",
      "socket_url": "https://mochat.io",
      "socket_path": "/socket.io",
      "claw_token": "claw_xxx",
      "agent_user_id": "6982abcdef",
      "sessions": ["*"],
      "panels": ["*"],
      "reply_delay_mode": "non-mention",
      "reply_delay_ms": 120000
    }
  }
}
```



</details>

</details>

<details>
<summary><b>Discord</b></summary>

**1. Create a bot**
- Go to https://discord.com/developers/applications
- Create an application → Bot → Add Bot
- Copy the bot token

**2. Enable intents**
- In the Bot settings, enable **MESSAGE CONTENT INTENT**
- (Optional) Enable **SERVER MEMBERS INTENT** if you plan to use allow lists based on member data

**3. Get your User ID**
- Discord Settings → Advanced → enable **Developer Mode**
- Right-click your avatar → **Copy User ID**

**4. Configure**

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

> `groupPolicy` controls how the bot responds in group channels:
> - `"mention"` (default) — Only respond when @mentioned
> - `"open"` — Respond to all messages
> DMs always respond when the sender is in `allowFrom`.

**5. Invite the bot**
- OAuth2 → URL Generator
- Scopes: `bot`
- Bot Permissions: `Send Messages`, `Read Message History`
- Open the generated invite URL and add the bot to your server

**6. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Matrix (Element)</b></summary>

Install Matrix dependencies first:

```bash
pip install nanobot-ai[matrix]
```

**1. Create/choose a Matrix account**

- Create or reuse a Matrix account on your homeserver (for example `matrix.org`).
- Confirm you can log in with Element.

**2. Get credentials**

- You need:
  - `userId` (example: `@nanobot:matrix.org`)
  - `accessToken`
  - `deviceId` (recommended so sync tokens can be restored across restarts)
- You can obtain these from your homeserver login API (`/_matrix/client/v3/login`) or from your client's advanced session settings.

**3. Configure**

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://matrix.org",
      "userId": "@nanobot:matrix.org",
      "accessToken": "syt_xxx",
      "deviceId": "NANOBOT01",
      "e2eeEnabled": true,
      "allowFrom": ["@your_user:matrix.org"],
      "groupPolicy": "open",
      "groupAllowFrom": [],
      "allowRoomMentions": false,
      "maxMediaBytes": 20971520
    }
  }
}
```

> Keep a persistent `matrix-store` and stable `deviceId` — encrypted session state is lost if these change across restarts.

| Option | Description |
|--------|-------------|
| `allowFrom` | User IDs allowed to interact. Empty = all senders. |
| `groupPolicy` | `open` (default), `mention`, or `allowlist`. |
| `groupAllowFrom` | Room allowlist (used when policy is `allowlist`). |
| `allowRoomMentions` | Accept `@room` mentions in mention mode. |
| `e2eeEnabled` | E2EE support (default `true`). Set `false` for plaintext-only. |
| `maxMediaBytes` | Max attachment size (default `20MB`). Set `0` to block all media. |




**4. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>WhatsApp</b></summary>

Requires **Node.js ≥18**.

**1. Link device**

```bash
nanobot channels login
# Scan QR with WhatsApp → Settings → Linked Devices
```

**2. Configure**

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+1234567890"]
    }
  }
}
```

**3. Run** (two terminals)

```bash
# Terminal 1
nanobot channels login

# Terminal 2
nanobot gateway
```

</details>

<details>
<summary><b>Feishu (飞书)</b></summary>

Uses **WebSocket** long connection — no public IP required.

**1. Create a Feishu bot**
- Visit [Feishu Open Platform](https://open.feishu.cn/app)
- Create a new app → Enable **Bot** capability
- **Permissions**: Add `im:message` (send messages) and `im:message.p2p_msg:readonly` (receive messages)
- **Events**: Add `im.message.receive_v1` (receive messages)
  - Select **Long Connection** mode (requires running nanobot first to establish connection)
- Get **App ID** and **App Secret** from "Credentials & Basic Info"
- Publish the app

**2. Configure**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": ["ou_YOUR_OPEN_ID"]
    }
  }
}
```

> `encryptKey` and `verificationToken` are optional for Long Connection mode.
> `allowFrom`: Add your open_id (find it in nanobot logs when you message the bot). Use `["*"]` to allow all users.

**3. Run**

```bash
nanobot gateway
```

> [!TIP]
> Feishu uses WebSocket to receive messages — no webhook or public IP needed!

</details>

<details>
<summary><b>QQ (QQ单聊)</b></summary>

Uses **botpy SDK** with WebSocket — no public IP required. Currently supports **private messages only**.

**1. Register & create bot**
- Visit [QQ Open Platform](https://q.qq.com) → Register as a developer (personal or enterprise)
- Create a new bot application
- Go to **开发设置 (Developer Settings)** → copy **AppID** and **AppSecret**

**2. Set up sandbox for testing**
- In the bot management console, find **沙箱配置 (Sandbox Config)**
- Under **在消息列表配置**, click **添加成员** and add your own QQ number
- Once added, scan the bot's QR code with mobile QQ → open the bot profile → tap "发消息" to start chatting

**3. Configure**

> - `allowFrom`: Add your openid (find it in nanobot logs when you message the bot). Use `["*"]` for public access.
> - For production: submit a review in the bot console and publish. See [QQ Bot Docs](https://bot.q.qq.com/wiki/) for the full publishing flow.

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"]
    }
  }
}
```

**4. Run**

```bash
nanobot gateway
```

Now send a message to the bot from QQ — it should respond!

</details>

<details>
<summary><b>DingTalk (钉钉)</b></summary>

Uses **Stream Mode** — no public IP required.

**1. Create a DingTalk bot**
- Visit [DingTalk Open Platform](https://open-dev.dingtalk.com/)
- Create a new app -> Add **Robot** capability
- **Configuration**:
  - Toggle **Stream Mode** ON
- **Permissions**: Add necessary permissions for sending messages
- Get **AppKey** (Client ID) and **AppSecret** (Client Secret) from "Credentials"
- Publish the app

**2. Configure**

```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_APP_KEY",
      "clientSecret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_STAFF_ID"]
    }
  }
}
```

> `allowFrom`: Add your staff ID. Use `["*"]` to allow all users.

**3. Run**

```bash
nanobot gateway
```

</details>

<details>
<summary><b>Slack</b></summary>

Uses **Socket Mode** — no public URL required.

**1. Create a Slack app**
- Go to [Slack API](https://api.slack.com/apps) → **Create New App** → "From scratch"
- Pick a name and select your workspace

**2. Configure the app**
- **Socket Mode**: Toggle ON → Generate an **App-Level Token** with `connections:write` scope → copy it (`xapp-...`)
- **OAuth & Permissions**: Add bot scopes: `chat:write`, `reactions:write`, `app_mentions:read`
- **Event Subscriptions**: Toggle ON → Subscribe to bot events: `message.im`, `message.channels`, `app_mention` → Save Changes
- **App Home**: Scroll to **Show Tabs** → Enable **Messages Tab** → Check **"Allow users to send Slash commands and messages from the messages tab"**
- **Install App**: Click **Install to Workspace** → Authorize → copy the **Bot Token** (`xoxb-...`)

**3. Configure nanobot**

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-...",
      "appToken": "xapp-...",
      "allowFrom": ["YOUR_SLACK_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

**4. Run**

```bash
nanobot gateway
```

DM the bot directly or @mention it in a channel — it should respond!

> [!TIP]
> - `groupPolicy`: `"mention"` (default — respond only when @mentioned), `"open"` (respond to all channel messages), or `"allowlist"` (restrict to specific channels).
> - DM policy defaults to open. Set `"dm": {"enabled": false}` to disable DMs.

</details>

<details>
<summary><b>Email</b></summary>

Give nanobot its own email account. It polls **IMAP** for incoming mail and replies via **SMTP** — like a personal email assistant.

**1. Get credentials (Gmail example)**
- Create a dedicated Gmail account for your bot (e.g. `my-nanobot@gmail.com`)
- Enable 2-Step Verification → Create an [App Password](https://myaccount.google.com/apppasswords)
- Use this app password for both IMAP and SMTP

**2. Configure**

> - `consentGranted` must be `true` to allow mailbox access. This is a safety gate — set `false` to fully disable.
> - `allowFrom`: Add your email address. Use `["*"]` to accept emails from anyone.
> - `smtpUseTls` and `smtpUseSsl` default to `true` / `false` respectively, which is correct for Gmail (port 587 + STARTTLS). No need to set them explicitly.
> - Set `"autoReplyEnabled": false` if you only want to read/analyze emails without sending automatic replies.

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "imap.gmail.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@gmail.com",
      "imapPassword": "your-app-password",
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "fromAddress": "my-nanobot@gmail.com",
      "allowFrom": ["your-real-email@gmail.com"]
    }
  }
}
```


**3. Run**

```bash
nanobot gateway
```

</details>

## 🌐 Agent Social Network

🐈 nanobot is capable of linking to the agent social network (agent community). **Just send one message and your nanobot joins automatically!**

| Platform | How to Join (send this message to your bot) |
|----------|-------------|
| [**Moltbook**](https://www.moltbook.com/) | `Read https://moltbook.com/skill.md and follow the instructions to join Moltbook` |
| [**ClawdChat**](https://clawdchat.ai/) | `Read https://clawdchat.ai/skill.md and follow the instructions to join ClawdChat` |

Simply send the command above to your nanobot (via CLI or any chat channel), and it will handle the rest.

## ⚙️ Configuration

Config file: `~/.nanobot/config.json`

### Providers

> [!TIP]
> - **Groq** provides free voice transcription via Whisper. If configured, Telegram voice messages will be automatically transcribed.
> - **Zhipu Coding Plan**: If you're on Zhipu's coding plan, set `"apiBase": "https://open.bigmodel.cn/api/coding/paas/v4"` in your zhipu provider config.
> - **MiniMax (Mainland China)**: If your API key is from MiniMax's mainland China platform (minimaxi.com), set `"apiBase": "https://api.minimaxi.com/v1"` in your minimax provider config.
> - **VolcEngine Coding Plan**: If you're on VolcEngine's coding plan, set `"apiBase": "https://ark.cn-beijing.volces.com/api/coding/v3"` in your volcengine provider config.
> - **Alibaba Cloud Coding Plan**: If you're on the Alibaba Cloud Coding Plan (BaiLian), set `"apiBase": "https://coding.dashscope.aliyuncs.com/v1"` in your dashscope provider config.

| Provider | Purpose | Get API Key |
|----------|---------|-------------|
| `custom` | Any OpenAI-compatible endpoint (direct, no LiteLLM) | — |
| `openrouter` | LLM (recommended, access to all models) | [openrouter.ai](https://openrouter.ai) |
| `anthropic` | LLM (Claude direct) | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | LLM (GPT direct) | [platform.openai.com](https://platform.openai.com) |
| `deepseek` | LLM (DeepSeek direct) | [platform.deepseek.com](https://platform.deepseek.com) |
| `groq` | LLM + **Voice transcription** (Whisper) | [console.groq.com](https://console.groq.com) |
| `gemini` | LLM (Gemini direct) | [aistudio.google.com](https://aistudio.google.com) |
| `minimax` | LLM (MiniMax direct) | [platform.minimaxi.com](https://platform.minimaxi.com) |
| `aihubmix` | LLM (API gateway, access to all models) | [aihubmix.com](https://aihubmix.com) |
| `siliconflow` | LLM (SiliconFlow/硅基流动) | [siliconflow.cn](https://siliconflow.cn) |
| `volcengine` | LLM (VolcEngine/火山引擎) | [volcengine.com](https://www.volcengine.com) |
| `dashscope` | LLM (Qwen) | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| `moonshot` | LLM (Moonshot/Kimi) | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `zhipu` | LLM (Zhipu GLM) | [open.bigmodel.cn](https://open.bigmodel.cn) |
| `vllm` | LLM (local, any OpenAI-compatible server) | — |
| `openai_codex` | LLM (Codex, OAuth) | `nanobot provider login openai-codex` |
| `github_copilot` | LLM (GitHub Copilot, OAuth) | `nanobot provider login github-copilot` |

<details>
<summary><b>OpenAI Codex (OAuth)</b></summary>

Codex uses OAuth instead of API keys. Requires a ChatGPT Plus or Pro account.

**1. Login:**
```bash
nanobot provider login openai-codex
```

**2. Set model** (merge into `~/.nanobot/config.json`):
```json
{
  "agents": {
    "defaults": {
      "model": "openai-codex/gpt-5.1-codex"
    }
  }
}
```

**3. Chat:**
```bash
nanobot agent -m "Hello!"
```

> Docker users: use `docker run -it` for interactive OAuth login.

</details>

<details>
<summary><b>Custom Provider (Any OpenAI-compatible API)</b></summary>

Connects directly to any OpenAI-compatible endpoint — LM Studio, llama.cpp, Together AI, Fireworks, Azure OpenAI, or any self-hosted server. Bypasses LiteLLM; model name is passed as-is.

```json
{
  "providers": {
    "custom": {
      "apiKey": "your-api-key",
      "apiBase": "https://api.your-provider.com/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "your-model-name"
    }
  }
}
```

> For local servers that don't require a key, set `apiKey` to any non-empty string (e.g. `"no-key"`).

</details>

<details>
<summary><b>vLLM (local / OpenAI-compatible)</b></summary>

Run your own model with vLLM or any OpenAI-compatible server, then add to config:

**1. Start the server** (example):
```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --port 8000
```

**2. Add to config** (partial — merge into `~/.nanobot/config.json`):

*Provider (key can be any non-empty string for local):*
```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  }
}
```

*Model:*
```json
{
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

</details>

<details>
<summary><b>Adding a New Provider (Developer Guide)</b></summary>

nanobot uses a **Provider Registry** (`nanobot/providers/registry.py`) as the single source of truth.
Adding a new provider only takes **2 steps** — no if-elif chains to touch.

**Step 1.** Add a `ProviderSpec` entry to `PROVIDERS` in `nanobot/providers/registry.py`:

```python
ProviderSpec(
    name="myprovider",                   # config field name
    keywords=("myprovider", "mymodel"),  # model-name keywords for auto-matching
    env_key="MYPROVIDER_API_KEY",        # env var for LiteLLM
    display_name="My Provider",          # shown in `nanobot status`
    litellm_prefix="myprovider",         # auto-prefix: model → myprovider/model
    skip_prefixes=("myprovider/",),      # don't double-prefix
)
```

**Step 2.** Add a field to `ProvidersConfig` in `nanobot/config/schema.py`:

```python
class ProvidersConfig(BaseModel):
    ...
    myprovider: ProviderConfig = ProviderConfig()
```

That's it! Environment variables, model prefixing, config matching, and `nanobot status` display will all work automatically.

**Common `ProviderSpec` options:**

| Field | Description | Example |
|-------|-------------|---------|
| `litellm_prefix` | Auto-prefix model names for LiteLLM | `"dashscope"` → `dashscope/qwen-max` |
| `skip_prefixes` | Don't prefix if model already starts with these | `("dashscope/", "openrouter/")` |
| `env_extras` | Additional env vars to set | `(("ZHIPUAI_API_KEY", "{api_key}"),)` |
| `model_overrides` | Per-model parameter overrides | `(("kimi-k2.5", {"temperature": 1.0}),)` |
| `is_gateway` | Can route any model (like OpenRouter) | `True` |
| `detect_by_key_prefix` | Detect gateway by API key prefix | `"sk-or-"` |
| `detect_by_base_keyword` | Detect gateway by API base URL | `"openrouter"` |
| `strip_model_prefix` | Strip existing prefix before re-prefixing | `True` (for AiHubMix) |

</details>


### MCP (Model Context Protocol)

> [!TIP]
> The config format is compatible with Claude Desktop / Cursor. You can copy MCP server configs directly from any MCP server's README.

nanobot supports [MCP](https://modelcontextprotocol.io/) — connect external tool servers and use them as native agent tools.

Add MCP servers to your `config.json`:

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
      },
      "my-remote-mcp": {
        "url": "https://example.com/mcp/",
        "headers": {
          "Authorization": "Bearer xxxxx"
        }
      }
    }
  }
}
```

Two transport modes are supported:

| Mode | Config | Example |
|------|--------|---------|
| **Stdio** | `command` + `args` | Local process via `npx` / `uvx` |
| **HTTP** | `url` + `headers` (optional) | Remote endpoint (`https://mcp.example.com/sse`) |

Use `toolTimeout` to override the default 30s per-call timeout for slow servers:

```json
{
  "tools": {
    "mcpServers": {
      "my-slow-server": {
        "url": "https://example.com/mcp/",
        "toolTimeout": 120
      }
    }
  }
}
```

MCP tools are automatically discovered and registered on startup. The LLM can use them alongside built-in tools — no extra configuration needed.




### Memory & Self-Improvement

nanobot has a layered memory system that works out of the box — no setup needed. Optional semantic memory adds AI-powered recall.

| Layer | What it does | Always on? |
|-------|-------------|-----------|
| **MEMORY.md** | Long-term facts (preferences, project context). Loaded into every prompt. | ✅ Yes |
| **HISTORY.md** | Append-only event log. Grep-searchable. | ✅ Yes |
| **Auto-Recall** | Extracts keywords from your message and automatically retrieves relevant history entries. | ✅ Yes |
| **Self-Improvement** | Logs errors, corrections, and knowledge gaps to `.learnings/`. Promotes recurring patterns to MEMORY.md. | ✅ Skill (load on demand) |
| **Semantic Memory (mem0)** | AI-powered memory using local Ollama embeddings. Understands meaning, not just keywords. | ❌ Opt-in |

#### Auto-Recall (built-in)

Every message you send is automatically matched against past history. Relevant entries appear in the agent's context as "Recalled History" — no manual grep needed.

#### Self-Improvement (built-in skill)

The `self-improvement` skill teaches nanobot to learn from mistakes:
- **Errors** → logged to `.learnings/ERRORS.md`
- **User corrections** → logged to `.learnings/LEARNINGS.md`
- **Feature requests** → logged to `.learnings/FEATURE_REQUESTS.md`
- **Recurring patterns** (3+ times) → automatically promoted to `MEMORY.md`

The `.learnings/` directory is created automatically during `nanobot onboard`.

<details>
<summary><b>Semantic Memory with mem0 (optional)</b></summary>

mem0 adds AI-powered semantic memory using local Ollama embeddings. Unlike keyword matching, it understands meaning — "I like dark theme" will match queries about "color preferences".

**Requirements:**
- [Ollama](https://ollama.ai) running locally
- Embedding + LLM models pulled

**1. Install mem0 dependencies:**

```bash
pip install nanobot-ai[mem0]
```

**2. Pull Ollama models:**

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

**3. Enable during onboarding:**

```bash
nanobot onboard
# Answer "y" when asked about mem0
```

**Or enable manually** in `~/.nanobot/config.json`:

```json
{
  "memory": {
    "mem0": {
      "enabled": true,
      "ollamaUrl": "http://localhost:11434",
      "embeddingModel": "nomic-embed-text",
      "llmModel": "llama3.2"
    }
  }
}
```

When enabled, mem0 runs alongside the existing memory system:
- User messages are automatically saved as semantic memories
- Relevant memories are retrieved and shown as "Semantic Memory" in the agent's context
- All data stays local (Ollama embeddings + local Qdrant at `~/.nanobot/mem0_store/`)

</details>

### Security

> [!TIP]
> For production deployments, set `"restrictToWorkspace": true` in your config to sandbox the agent.
> **Change in source / post-`v0.1.4.post3`:** In `v0.1.4.post3` and earlier, an empty `allowFrom` means "allow all senders". In newer versions (including building from source), **empty `allowFrom` denies all access by default**. To allow all senders, set `"allowFrom": ["*"]`.

| Option | Default | Description |
|--------|---------|-------------|
| `tools.restrictToWorkspace` | `false` | When `true`, restricts **all** agent tools (shell, file read/write/edit, list) to the workspace directory. Prevents path traversal and out-of-scope access. |
| `tools.exec.pathAppend` | `""` | Extra directories to append to `PATH` when running shell commands (e.g. `/usr/sbin` for `ufw`). |
| `channels.*.allowFrom` | `[]` (allow all) | Whitelist of user IDs. Empty = allow everyone; non-empty = only listed users can interact. |


## Multiple Instances

Run multiple nanobot instances simultaneously, each with its own workspace and configuration.

```bash
# Instance A - Telegram bot
nanobot gateway -w ~/.nanobot/botA -p 18791

# Instance B - Discord bot
nanobot gateway -w ~/.nanobot/botB -p 18792

# Instance C - Using custom config file
nanobot gateway -w ~/.nanobot/botC -c ~/.nanobot/botC/config.json -p 18793
```

| Option | Short | Description |
|--------|-------|-------------|
| `--workspace` | `-w` | Workspace directory (default: `~/.nanobot/workspace`) |
| `--config` | `-c` | Config file path (default: `~/.nanobot/config.json`) |
| `--port` | `-p` | Gateway port (default: `18790`) |

Each instance has its own:
- Workspace directory (MEMORY.md, HEARTBEAT.md, session files)
- Cron jobs storage (`workspace/cron/jobs.json`)
- Configuration (if using `--config`)


## CLI Reference

| Command | Description |
|---------|-------------|
| `nanobot onboard` | Initialize config & workspace |
| `nanobot agent -m "..."` | Chat with the agent |
| `nanobot agent` | Interactive chat mode |
| `nanobot agent --no-markdown` | Show plain-text replies |
| `nanobot agent --logs` | Show runtime logs during chat |
| `nanobot gateway` | Start the gateway |
| `nanobot status` | Show status |
| `nanobot provider login openai-codex` | OAuth login for providers |
| `nanobot channels login` | Link WhatsApp (scan QR) |
| `nanobot channels status` | Show channel status |

Interactive mode exits: `exit`, `quit`, `/exit`, `/quit`, `:q`, or `Ctrl+D`.

<details>
<summary><b>Heartbeat (Periodic Tasks)</b></summary>

The gateway wakes up every 30 minutes and checks `HEARTBEAT.md` in your workspace (`~/.nanobot/workspace/HEARTBEAT.md`). If the file has tasks, the agent executes them and delivers results to your most recently active chat channel.

**Setup:** edit `~/.nanobot/workspace/HEARTBEAT.md` (created automatically by `nanobot onboard`):

```markdown
## Periodic Tasks

- [ ] Check weather forecast and send a summary
- [ ] Scan inbox for urgent emails
```

The agent can also manage this file itself — ask it to "add a periodic task" and it will update `HEARTBEAT.md` for you.

> **Note:** The gateway must be running (`nanobot gateway`) and you must have chatted with the bot at least once so it knows which channel to deliver to.

</details>

## 🐳 Docker

> [!TIP]
> The `-v ~/.nanobot:/root/.nanobot` flag mounts your local config directory into the container, so your config and workspace persist across container restarts.

### Docker Compose

```bash
docker compose run --rm nanobot-cli onboard   # first-time setup
vim ~/.nanobot/config.json                     # add API keys
docker compose up -d nanobot-gateway           # start gateway
```

```bash
docker compose run --rm nanobot-cli agent -m "Hello!"   # run CLI
docker compose logs -f nanobot-gateway                   # view logs
docker compose down                                      # stop
```

### Docker

```bash
# Build the image
docker build -t nanobot .

# Initialize config (first time only)
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard

# Edit config on host to add API keys
vim ~/.nanobot/config.json

# Run gateway (connects to enabled channels, e.g. Telegram/Discord/Mochat)
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway

# Or run a single command
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot status
```

## 🐧 Linux Service

Run the gateway as a systemd user service so it starts automatically and restarts on failure.

**1. Find the nanobot binary path:**

```bash
which nanobot   # e.g. /home/user/.local/bin/nanobot
```

**2. Create the service file** at `~/.config/systemd/user/nanobot-gateway.service` (replace `ExecStart` path if needed):

```ini
[Unit]
Description=Nanobot Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

**3. Enable and start:**

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-gateway
```

**Common operations:**

```bash
systemctl --user status nanobot-gateway        # check status
systemctl --user restart nanobot-gateway       # restart after config changes
journalctl --user -u nanobot-gateway -f        # follow logs
```

If you edit the `.service` file itself, run `systemctl --user daemon-reload` before restarting.

> **Note:** User services only run while you are logged in. To keep the gateway running after logout, enable lingering:
>
> ```bash
> loginctl enable-linger $USER
> ```

## 📁 Project Structure

```
nanobot/
├── agent/          # 🧠 Core agent logic
│   ├── loop.py     #    Agent loop (LLM ↔ tool execution)
│   ├── context.py  #    Prompt builder
│   ├── memory.py   #    Persistent memory
│   ├── skills.py   #    Skills loader
│   ├── subagent.py #    Background task execution
│   └── tools/      #    Built-in tools (incl. spawn)
├── skills/         # 🎯 Bundled skills
│   ├── r01-orchestrator/   #    R01 pipeline controller
│   ├── r01-ideation/       #    Hypothesis generation
│   ├── r01-novelty-checker/#    Literature overlap check
│   ├── r01-literature/     #    Domain literature search
│   ├── r01-writer-*/       #    Domain writers (hci, healthcare, ai, integrator)
│   ├── r01-reviewer-*/     #    Domain reviewers + panel
│   ├── r01-reviser/        #    Targeted revision
│   ├── r01-figures/        #    Figure generation
│   ├── r01-budget/         #    NIH budget
│   ├── r01-evolution/      #    Cross-project learning
│   ├── r01-foa-finder/     #    FOA discovery
│   └── (github, self-improvement, weather, ...)
├── channels/       # 📱 Chat channel integrations
├── bus/            # 🚌 Message routing
├── cron/           # ⏰ Scheduled tasks
├── heartbeat/      # 💓 Proactive wake-up
├── providers/      # 🤖 LLM providers (OpenRouter, etc.)
├── session/        # 💬 Conversation sessions
├── config/         # ⚙️ Configuration
└── cli/            # 🖥️ Commands

r01-proposal/
├── PLAN.md         # Full architecture, phase status, design decisions
├── workspace/
│   ├── _templates/ # project.yaml, state.json, cost/event schemas
│   └── _system/    # style_guide.md, writing_voice*.md, reviewer_patterns.json
└── r01_figure_renderer.py  # Standalone matplotlib renderer
```

## 🤝 Contribute & Roadmap

PRs welcome! The codebase is intentionally small and readable. 🤗

**Roadmap** — Pick an item and [open a PR](https://github.com/HKUDS/nanobot/pulls)!

- [ ] **Multi-modal** — See and hear (images, voice, video)
- [x] **Long-term memory** — Auto-recall, semantic memory (mem0), and persistent context
- [ ] **Better reasoning** — Multi-step planning and reflection
- [ ] **More integrations** — Calendar and more
- [x] **Self-improvement** — Learn from feedback and mistakes

### Contributors

<a href="https://github.com/HKUDS/nanobot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=HKUDS/nanobot&max=100&columns=12&updated=20260210" alt="Contributors" />
</a>


## ⭐ Star History

<div align="center">
  <a href="https://star-history.com/#HKUDS/nanobot&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=HKUDS/nanobot&type=Date" style="border-radius: 15px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);" />
    </picture>
  </a>
</div>

<p align="center">
  <em> Thanks for visiting ✨ nanobot!</em><br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUDS.nanobot&style=for-the-badge&color=00d4ff" alt="Views">
</p>


<p align="center">
  <sub>nanobot is for educational, research, and technical exchange purposes only</sub>
</p>
