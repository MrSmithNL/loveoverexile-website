# Project Architecture — Love Over Exile

> **Scope: Project-specific — components unique to loveoverexile.com.**
> This project is built on the global foundation. See `~/.claude/docs/architecture.md` for the shared tooling layer (Claude Code, VS Code, Bitwarden, GitHub CLI, etc.).
>
> **Last updated:** 2026-02-27
> **Status:** Active — content workflow live, home page LOE content + AI images pushed as draft. Rube MCP removed (broken). Composio setup pending.

---

## Project System Diagram

```mermaid
graph TD
    subgraph GLOBAL["Global Foundation"]
        CC[Claude Code + VS Code<br/>MacBook Pro]
        BW[Bitwarden<br/>Credential Vault]
    end

    subgraph AUTOMATION["Automation Layer"]
        COMPOSIO[Composio<br/>Service Connector<br/>⚠️ Account needed]
    end

    subgraph VPS["VPS Server"]
        WP[WordPress<br/>loveoverexile.com<br/>Theme: Avada]
        WPAPI[WordPress REST API<br/>Application Password]
        EMAIL_SRV[Email Server<br/>info / contact / malcolm<br/>@loveoverexile.com]
        OWUI[Open WebUI<br/>Claude Bot]
        WP --- WPAPI
    end

    subgraph EMAIL_MARKETING["Email Marketing"]
        ML[MailerLite<br/>Waitlist + Newsletter<br/>⚠️ Account needed]
    end

    subgraph EMAIL_ACCOUNTS["Email Accounts"]
        ZOHO[Zoho Mail<br/>loveoverexile.com inboxes<br/>⚠️ Setup pending]
    end

    subgraph GITHUB_PROJECT["GitHub"]
        REPO[loveoverexile-website<br/>github.com/MrSmithNL<br/>Private repo]
    end

    subgraph EXTERNAL["External Services"]
        DOMAIN[Domain Registrar<br/>loveoverexile.com — TBD]
        GSC[Google Search Console<br/>⚠️ Setup pending]
        GAIAPI[Google AI Studio<br/>Imagen 4 — image generation<br/>✅ API key in .env]
    end

    CC -->|git push| REPO
    CC -->|REST API — .env credentials| WPAPI
    CC -->|MCP tools — pending setup| COMPOSIO
    CC -->|API key — .env| GAIAPI
    COMPOSIO -->|OAuth| ZOHO
    COMPOSIO -->|OAuth| ML
    COMPOSIO -->|OAuth| WPAPI
    DOMAIN -->|DNS| VPS
    WP -->|Email delivery| EMAIL_SRV
    ZOHO -.->|Planned: manage inboxes| EMAIL_SRV

    style GLOBAL fill:#e8f4f8,stroke:#2196F3,stroke-width:2px,stroke-dasharray:5 5
    style AUTOMATION fill:#f3e5f5,stroke:#9C27B0,stroke-width:2px
    style VPS fill:#e8f5e9,stroke:#4CAF50,stroke-width:2px
    style EMAIL_MARKETING fill:#fff8e1,stroke:#FFC107,stroke-width:2px
    style EMAIL_ACCOUNTS fill:#fff8e1,stroke:#FFC107,stroke-width:2px
    style GITHUB_PROJECT fill:#f5f5f5,stroke:#333,stroke-width:2px
    style EXTERNAL fill:#fff3e0,stroke:#FF9800,stroke-width:2px
```

---

## Components

| # | Component | What It Is | Where It Lives | Status |
|---|-----------|-----------|----------------|--------|
| 1 | WordPress | Website CMS — Avada theme | VPS Server | ✅ Active |
| 2 | WordPress REST API | Programmatic content management | VPS Server | ✅ Active — credentials in .env |
| 3 | Email Server | loveoverexile.com mailboxes | VPS Server | ✅ Active — info, contact, malcolm |
| 4 | Rube MCP | Bridge connecting Claude to external services | rube.app/mcp | ❌ Removed — auth model changed, broken |
| 5 | Composio | OAuth connector for external service APIs | composio.dev | ⚠️ Account needed — direct setup (no Rube) |
| 6 | Zoho Mail | Manages loveoverexile.com inboxes with full API | Zoho cloud | ⚠️ Account needed — will connect via Composio |
| 7 | MailerLite | Email waitlist + newsletter for book launch | MailerLite cloud | ⚠️ Account needed — will connect via Composio |
| 8 | Google Search Console | SEO monitoring and indexing | Google | ⚠️ Setup pending |
| 9 | Open WebUI | Self-hosted AI chat interface | VPS Server | ❓ Status TBD |
| 10 | VPS Server | Hosts WordPress + email + Open WebUI | Cloud — provider TBD | ✅ Active |
| 11 | Domain — loveoverexile.com | Domain name + DNS | Registrar TBD | ✅ Active |
| 12 | GitHub Repo | Version control and project backup | github.com/MrSmithNL | ✅ Active — private |
| 13 | Google AI Studio (Imagen 4) | AI image generation for website | Google cloud | ✅ Active — API key in .env |

---

## Connections

| From | To | How | Status | Purpose |
|------|----|-----|--------|---------|
| Claude Code | WordPress REST API | HTTPS + Application Password (.env) | ✅ Active | Push content, publish pages, manage posts |
| Claude Code | Google AI Studio | HTTPS + API Key (.env) | ✅ Active | Generate images with Imagen 4 |
| Claude Code | Composio MCP | HTTP MCP server | ⚠️ Pending — account needed | Gateway to Zoho Mail + MailerLite automations |
| Composio | Zoho Mail | OAuth | ⚠️ Pending connection | Read, send, monitor loveoverexile.com inboxes |
| Composio | MailerLite | OAuth | ⚠️ Pending connection | Manage waitlist subscribers and campaigns |
| Project folder | GitHub | git push via CLI | ✅ Active | Version control + backup |
| Domain Registrar | VPS | DNS records | ✅ Active | Routes loveoverexile.com to server |

---

## Authentication

| Service | Auth Method | Status | Where Stored |
|---------|------------|--------|-------------|
| WordPress REST API | Application Password | ✅ Active | `.env` file (gitignored) + Bitwarden |
| WordPress Admin | Username + password | ✅ Active | Bitwarden |
| GitHub | OAuth via GitHub CLI | ✅ Active | macOS keyring |
| Rube MCP | N/A — removed | ❌ Removed | Deleted from `~/.claude.json` |
| Composio | Per-service OAuth tokens | ⚠️ Pending | Managed by Composio |
| Zoho Mail | OAuth via Composio | ⚠️ Pending | Composio |
| MailerLite | OAuth via Composio | ⚠️ Pending | Composio |
| Email server (VPS) | TBD | ✅ Accounts created | Malcolm manages |
| Domain Registrar | TBD | ✅ Active | Malcolm manages |
| VPS Server | TBD (SSH / control panel) | ✅ Active | Malcolm manages |
| Open WebUI | TBD | ❓ Unknown | TBD |
| Google Search Console | Google OAuth | ⚠️ Not yet set up | TBD |
| Google AI Studio | API Key | ✅ Active | `.env` file (gitignored) + Bitwarden |

---

## Accounts

| Service | URL | Purpose | Account |
|---------|-----|---------|---------|
| WordPress Admin | https://loveoverexile.com/wp-admin | Manage website | loveoverexile (user) |
| GitHub | https://github.com/MrSmithNL | Version control | MrSmithNL |
| Bitwarden | https://vault.bitwarden.com | Credential vault | msmithnl@gmail.com |
| Composio | https://composio.dev | Automation bridge | ⚠️ Account to be created |
| Zoho Mail | https://mail.zoho.com | Email management | ⚠️ To be created |
| MailerLite | https://mailerlite.com | Email marketing | ⚠️ To be created |
| Google Search Console | https://search.google.com/search-console | SEO monitoring | ⚠️ To be set up |
| Google AI Studio | https://aistudio.google.com | Imagen 4 API for image generation | msmithnl@gmail.com |
| VPS Provider | TBD | Server management | Malcolm |
| Domain Registrar | TBD | DNS + renewal | Malcolm |

---

## Image Workflow (built 2026-02-27)

```
Define images needed for a page
    ↓ (prompts, aspect ratios, SEO filenames)
python3 scripts/generate-images.py
    ↓ (Imagen 4 → Pillow optimise → WordPress media upload)
Image URLs returned → inserted into Avada shortcodes
    ↓ (REST API → WordPress draft)
Preview at wp-admin link
```

Scripts: `scripts/generate-images.py`
Skill: `~/.claude/skills/loe-image-generator/SKILL.md`
Optimisation targets: 16:9 backgrounds < 150 KB, cards < 90 KB, inline < 90 KB, mobile hero < 100 KB

---

## Content Workflow (built 2026-02-27)

```
Write Markdown file locally
    ↓ (content/pages/ or content/posts/)
python3 scripts/push-to-wordpress.py <file>
    ↓ (REST API → WordPress draft)
Preview at wp-admin link (must be logged in)
    ↓ (Malcolm reviews)
Publish via REST API or wp-admin
```

Scripts: `scripts/push-to-wordpress.py`
Docs: `docs/content-workflow.md`

---

## Pages Live on Site

| Page | URL | Status |
|------|-----|--------|
| Privacy Policy | https://loveoverexile.com/privacy-policy/ | ✅ Published |
| Home | https://loveoverexile.com/ | ⚠️ Draft — LOE text + Imagen 4 images pushed, awaiting Malcolm review |
| The Book | https://loveoverexile.com/the-book/ | ⚠️ Draft — needs Avada layout (currently plain text) |
| Malcolm's Story (About Us) | https://loveoverexile.com/about-us/ | ⚠️ Draft — full LOE content pushed (ID 1887), awaiting Malcolm review |
| All other pages | — | ⚠️ Demo content — to be replaced |

---

## Change Log

| Date | What Changed | Diagram Updated |
|------|-------------|----------------|
| 2026-02-27 | Initial setup — Claude Code, VS Code, GitHub, Bitwarden, WordPress REST API | Yes |
| 2026-02-27 | Site purpose clarified — book platform + parental alienation community | No |
| 2026-02-27 | Book manuscript read, memory file written, site structure designed | No |
| 2026-02-27 | Content workflow built — push script, folder structure, Privacy Policy published | No |
| 2026-02-27 | File permissions configured — Read/Edit/Write auto-approved in settings.json | No |
| 2026-02-27 | Rube MCP configured in ~/.claude.json — gateway to Composio integrations | Yes |
| 2026-02-27 | Email accounts created on VPS: info, contact, malcolm @loveoverexile.com | Yes |
| 2026-02-27 | Rube MCP removed — auth model changed, broken. Composio direct setup needed instead. | Yes |
| 2026-02-27 | Google AI Studio added — Imagen 4 API key stored in .env. loe-image-generator skill created. | Yes |
| 2026-02-27 | Home page updated — LOE text content + 13 Imagen 4 images generated, optimised, and pushed as draft (ID 1023) | No |
| 2026-02-27 | Malcolm's Story page — About Us (ID 1887) replaced with full LOE narrative content across all 6 Avada sections (53 replacements). Script: scripts/replace-about-us.py | No |
