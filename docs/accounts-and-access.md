# Accounts & Access Registry — Love Over Exile

> Lists every platform, account, and integration point for this project.
> **NEVER put actual passwords, tokens, or secrets in this file.**
> This is a reference for *what exists and how to access it* — not the credentials themselves.
>
> Store actual credentials in: your password manager (e.g., 1Password, Bitwarden, Apple Keychain)

---

## Platforms & Accounts

### 1. Anthropic (Claude)
| Field | Value |
|-------|-------|
| **What it is** | AI platform powering Claude Code and Open WebUI |
| **URL** | https://console.anthropic.com |
| **Account holder** | Malcolm Smith |
| **Used for** | Claude Code authentication, API access |
| **Subscription** | TBD — confirm plan (Pro/Max/Teams) |
| **Credentials stored in** | TBD — password manager |

### 2. WordPress — loveoverexile.com
| Field | Value |
|-------|-------|
| **What it is** | Website content management system |
| **Admin URL** | https://loveoverexile.com/wp-admin |
| **Account holder** | Malcolm Smith |
| **Used for** | Website pages, blog posts, menus, content |
| **Hosting** | VPS (details TBD) |
| **API access** | Not yet set up — need application password |
| **Credentials stored in** | TBD — password manager |

### 3. VPS Server
| Field | Value |
|-------|-------|
| **What it is** | Virtual Private Server hosting WordPress + Open WebUI |
| **Provider** | TBD — confirm provider name |
| **IP address** | TBD |
| **Access method** | TBD (SSH / control panel) |
| **Used for** | Hosting loveoverexile.com, running Open WebUI |
| **Credentials stored in** | TBD — password manager |

### 4. Domain — loveoverexile.com
| Field | Value |
|-------|-------|
| **What it is** | Domain name registration |
| **Registrar** | TBD — confirm (GoDaddy, Namecheap, Cloudflare, etc.) |
| **Managed at** | TBD — registrar URL |
| **DNS points to** | VPS server |
| **Expiry date** | TBD — important to track! |
| **Credentials stored in** | TBD — password manager |

### 5. Open WebUI (VPS)
| Field | Value |
|-------|-------|
| **What it is** | Self-hosted AI chat interface |
| **URL** | TBD — confirm access URL |
| **Used for** | Quick AI chat when away from MacBook |
| **Connected to** | Claude API (Anthropic) |
| **Credentials stored in** | TBD — password manager |

### 6. Bitwarden (Password Manager)
| Field | Value |
|-------|-------|
| **What it is** | Password manager — master vault for all credentials |
| **URL** | https://vault.bitwarden.com |
| **Account email** | msmithnl@gmail.com |
| **Account holder** | Malcolm Smith |
| **Used for** | Storing all passwords, API keys, and credentials across all projects |
| **CLI installed** | Yes — `bw` v2025.12.1 at /opt/homebrew/bin/bw |
| **Desktop app** | Yes — Bitwarden.app v2026.1.1 in /Applications/ |
| **CLI unlock command** | `bwunlock` (defined in ~/.zshrc) |
| **2FA enabled** | ❓ Unconfirmed — see RISK-007 in security-risk-log.md |
| **Session model** | Malcolm runs `bwunlock` → vault active for that terminal session only |

### 7. GitHub
| Field | Value |
|-------|-------|
| **What it is** | Version control and offsite backup platform |
| **URL** | https://github.com/MrSmithNL |
| **Account holder** | Malcolm Smith |
| **Username** | MrSmithNL |
| **Repository** | https://github.com/MrSmithNL/loveoverexile-website (private) |
| **Used for** | Version control, backup, project history |
| **2FA enabled** | ❌ Not yet — see RISK-001 in security-risk-log.md |
| **CLI auth** | GitHub CLI (gh) authenticated via OAuth, stored in macOS keyring |
| **Credentials stored in** | Password manager |

---

## API Keys & Integrations

| # | Service | Key Type | Status | Where Stored | Purpose |
|---|---------|----------|--------|-------------- |---------|
| 1 | Anthropic | API key | Active (via Claude Code login) | Managed by Claude Code | Powers AI assistant |
| 2 | WordPress REST API | Application password | NOT YET SET UP | Will go in .env file | Programmatic content management |

---

## TBD Items to Fill In

> These are details Malcolm needs to confirm. Update this file as information is gathered.

- [ ] VPS provider name and control panel URL
- [ ] VPS IP address
- [ ] Domain registrar name
- [ ] Domain expiry date
- [ ] WordPress admin username
- [ ] Anthropic subscription plan
- [ ] Open WebUI access URL
- [x] Preferred password manager: **Bitwarden** ✅
- [ ] VPS provider name and control panel URL
- [ ] VPS IP address
- [ ] Domain registrar name
- [ ] Domain expiry date
- [ ] WordPress admin username
- [ ] Anthropic subscription plan
- [ ] Open WebUI access URL
