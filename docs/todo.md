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

**What needs doing:**
Visitors need a way to sign up to be notified when the book launches. Must be live before any real content goes live.

**Steps:**
- Malcolm to confirm: do you already have a Mailchimp or ConvertKit/Kit account?
- Set up signup form on homepage and /the-book/ page
- Connect form to email list
- Set up welcome/confirmation email

---

### WP-002 — Set up content drafting and publishing workflow
**Priority:** 🔴 High

**What needs doing:**
A reliable way to write content locally and push it to WordPress:
1. Draft locally as Markdown files in `content/pages/` and `content/posts/`
2. Review with Malcolm
3. Push to WordPress via REST API as a draft
4. Malcolm publishes manually from wp-admin

**Steps:**
- Create folder structure: `content/pages/` and `content/posts/`
- Write a push script: Markdown → WordPress draft via REST API
- Test with Privacy Policy (first real page to publish)

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
