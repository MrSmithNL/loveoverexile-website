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

### WP-001 — Map existing WordPress site structure
**Priority:** ✅ Done — 2026-02-27
**See:** `docs/site-map.md`

**Summary of findings:**
- 13 published pages + 1 draft (Privacy Policy — needs finishing)
- Site is a recruitment agency: Home, About, Our Services (4 sub-pages), Case Studies, Hiring Advice, News Insights, Contact
- 6 real blog posts (all Nov 2024) + 2 default WordPress placeholders to delete
- No posts for ~3 months — content workflow is the next priority
- Plugins and theme still need checking manually in wp-admin

---

### WP-002 — Create content drafting workflow
**Priority:** 🟡 Medium
**Depends on:** WP-001

**What needs doing:**
Set up a clear process for creating, reviewing, and publishing content:
1. Draft content locally (in this project folder)
2. Review with Malcolm before publishing
3. Push to WordPress via REST API
4. Confirm live on site

**Steps (to design in a future session):**
- Decide on a folder structure for drafts (e.g., `content/drafts/`)
- Decide on file format (Markdown is simplest)
- Write a simple script or process to push a draft to WordPress as a draft post
- Malcolm reviews in wp-admin, then publishes manually

---

### WP-003 — Document VPS and domain registrar details
**Priority:** 🟡 Medium
**Relates to:** TOOL-003 in global todo

**What needs doing:**
The VPS provider and domain registrar are listed as "TBD" in the architecture. We need to:
1. Identify the VPS provider (Malcolm knows this)
2. Identify the domain registrar (Malcolm knows this)
3. Confirm credentials are in Bitwarden
4. Update `docs/accounts-and-access.md` and `docs/architecture.md`

---

### WP-004 — Confirm Open WebUI setup and access
**Priority:** 🟢 Low

**What needs doing:**
Open WebUI is listed in the architecture as "Active" but with TBD credentials. Confirm:
1. What URL is Open WebUI accessible at?
2. How is it secured (login, API key)?
3. Is it still being used?
4. Update architecture and accounts-and-access.md accordingly

---

## Completed Items

| ID | What | Completed |
|----|------|-----------|
| — | Project folder and docs created | 2026-02-27 |
| — | GitHub repo set up (private) | 2026-02-27 |
| — | GitHub 2FA enabled | 2026-02-27 |
| — | Bitwarden set up with 2FA | 2026-02-27 |
| — | WordPress REST API connected and tested | 2026-02-27 |
| WP-001 | WordPress site structure mapped → `docs/site-map.md` | 2026-02-27 |

---

## Session Log

| Date | What was worked on |
|------|--------------------|
| 2026-02-27 | Full environment setup — Claude Code, VS Code, GitHub, Bitwarden, WordPress REST API |
| 2026-02-27 | WP-001 — Mapped full site structure via REST API, documented in site-map.md |
