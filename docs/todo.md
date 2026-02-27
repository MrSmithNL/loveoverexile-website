# Project To-Do — Love Over Exile Website

> **This file is specific to loveoverexile.com.**
> Review and update at the start and end of every session.
> Cross-project and tooling tasks go in `~/.claude/docs/todo.md`.

---

## How This Works

- **Check this file at the start of every session** — pick up where we left off
- **Update it at the end of every session** — mark done items, add new ones
- Priority: 🔴 High / 🟡 Medium / 🟢 Low

---

## Open Items

### WP-008 — Set up email waitlist / subscription
**Priority:** 🔴 High — most important conversion action before book launch
**Status:** ⏸️ Paused — account setup issues. Resume when accounts are ready.

**What needs doing:**
1. Create Composio account at composio.dev → get API key
2. Create MailerLite account at mailerlite.com (free tier: 1,000 contacts)
3. Create Zoho Mail account at mail.zoho.com (to manage loveoverexile.com inboxes via Claude)
4. I'll write a script to generate Composio MCP URLs for each service
5. Add MCP servers with `claude mcp add` + authenticate each via browser OAuth
6. Set up waitlist signup form on homepage and /the-book/ page
7. Set up welcome/confirmation email

**Note:** Rube MCP (previously configured) is broken — Rube changed auth model. Old config removed from ~/.claude.json. Direct Composio approach needed instead.

---

### WP-002 — Set up content drafting and publishing workflow
**Priority:** ✅ Done — 2026-02-27
**See:** `docs/content-workflow.md`

**What was built:**
- `content/pages/` and `content/posts/` folder structure
- `scripts/push-to-wordpress.py` — pushes any Markdown file to WordPress as a draft
- Privacy Policy drafted, pushed, and **published** → loveoverexile.com/privacy-policy/
- Full workflow documented in `docs/content-workflow.md`

---

### WP-009 — SEO foundation setup
**Priority:** 🔴 High — before any real content goes live

**What needs doing:**
- Check if Yoast or Rank Math SEO plugin is already installed (Malcolm checks wp-admin → Plugins)
- Set correct site title: "Love Over Exile" and tagline
- Set up Google Search Console
- Keyword strategy documented in `docs/seo-strategy.md`

---

### WP-005 — Write and publish real content (all pages)
**Priority:** 🔴 High
**Depends on:** WP-002 (workflow), WP-009 (SEO setup)
**See:** `docs/site-structure.md` for full page list and implementation order

**Implementation order:**
1. Privacy Policy — legal requirement, must be live before email capture
2. The Book page — waitlist signup
3. Home — redesigned with book focus
4. Understanding What's Happening — highest SEO value
5. Malcolm's Story — author credibility
6. Survival Guide — practical value
7. Inner Freedom — Part 3 content
8. Articles/Blog — start publishing content
9. Community/Forum — bbPress setup
10. Resources — reading list

---

### WP-010 — Forum setup (bbPress)
**Priority:** 🟡 Medium
**Depends on:** WP-005 (site content established first)

**What needs doing:**
- Install bbPress plugin
- Set up forum categories mirroring site sections
- Configure moderation (Malcolm as moderator)
- Create /community/forum/ page

---

### WP-011 — Social media content pipeline
**Priority:** 🟡 Medium
**Depends on:** WP-005 (content exists first)

**What needs doing:**
Every article structured with: key quote (LinkedIn/Instagram), summary paragraph (newsletter), 5-point list (LinkedIn carousel). Design article template to make repurposing systematic.

---

### WP-003 — Document VPS and domain registrar details
**Priority:** 🟡 Medium

Malcolm to confirm: VPS provider name + control panel URL, domain registrar. Update `docs/accounts-and-access.md`.

---

### WP-004 — Confirm Open WebUI setup and access
**Priority:** 🟢 Low

Confirm URL, access method, whether still in use.

---

## Completed Items

| ID | What | Completed |
|----|------|-----------|
| — | Project folder and docs created | 2026-02-27 |
| — | GitHub repo set up (private) | 2026-02-27 |
| — | GitHub 2FA enabled | 2026-02-27 |
| — | Bitwarden set up with 2FA | 2026-02-27 |
| — | WordPress REST API connected and tested | 2026-02-27 |
| — | File write/edit permissions configured in settings.json | 2026-02-27 |
| WP-001 | WordPress site structure mapped → `docs/site-map.md` | 2026-02-27 |
| WP-006 | Book manuscript read in full + memory file written → `memory/book-summary.md` | 2026-02-27 |
| WP-007 | Real site structure designed → `docs/site-structure.md` | 2026-02-27 |
| WP-002 | Content workflow built — push script + folder structure → `docs/content-workflow.md` | 2026-02-27 |

---

## Session Log

| Date | What was worked on |
|------|--------------------|
| 2026-02-27 | Full environment setup — Claude Code, VS Code, GitHub, Bitwarden, WordPress REST API |
| 2026-02-27 | WP-001 — Mapped full site structure via REST API |
| 2026-02-27 | Site purpose clarified — book platform + parental alienation community. All docs updated. |
| 2026-02-27 | WP-006 — Both book files read in full. Comprehensive memory file written. |
| 2026-02-27 | WP-007 — Full site structure designed based on book's 3-part structure. |
| 2026-02-27 | File permissions configured — Read/Edit/Write now auto-approved in settings.json. |
| 2026-02-27 | WP-002 — Content workflow built. Push script works. Privacy Policy pushed to WP as draft. |
| 2026-02-27 | Rube MCP broken (auth changed). Removed from config. WP-008 paused — Composio/MailerLite/Zoho accounts needed. |
| 2026-02-27 | WP-005 — Started writing real site content (The Book page, Home page). |
| 2026-02-27 | WP-005 — Home page: LOE text content + 13 AI images (Imagen 4, web-optimised) pushed as draft. loe-image-generator skill created. |
| 2026-02-27 | WP-005 — Malcolm's Story page: About Us (ID 1887) fully replaced with LOE content — all 6 sections, 53 replacements. Script: scripts/replace-about-us.py |
