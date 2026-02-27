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
- Theme: **Avada Recruitment** — a premium recruitment agency theme
- All existing content (pages, posts, text, images) is **demo content from the theme** — none of it is real
- Site structure: Home, About, Our Services (4 sub-pages), Case Studies, Hiring Advice, News Insights, Contact
- 1 draft page: Privacy Policy (needs writing and publishing)
- 2 WordPress default placeholders to delete: "Sample Page" and "Hello world!"
- The real job: replace ALL demo content with real Love Over Exile content

---

### WP-002 — Set up content drafting workflow
**Priority:** 🔴 High
**Depends on:** WP-001 ✅

**What needs doing:**
Now that we know all content is demo, we need a reliable way to write and publish real content. The workflow:
1. Draft content locally as Markdown files (in `content/` folder)
2. Review with Malcolm before publishing
3. Push to WordPress via REST API as a draft
4. Malcolm reviews in wp-admin, then publishes manually

**Steps:**
- Create `content/pages/` and `content/posts/` folder structure
- Write a push script: reads a Markdown file → sends it to WordPress as a draft via REST API
- Test with one page (e.g. About Us draft)

---

### WP-005 — Write real content for all pages and posts
**Priority:** 🔴 High
**Depends on:** WP-002

**What needs doing:**
Replace all Avada Recruitment demo content with real Love Over Exile content. Needs input from Malcolm on:
- What services does Love Over Exile actually offer?
- What's the company story / About Us?
- Who are the team members?
- What are the real contact details?
- Do we have any real case studies yet?

**Pages to rewrite (in rough priority order):**
1. Homepage — most important, first thing visitors see
2. About Us — company story and credibility
3. Our Services (x4 sub-pages) — what we actually sell
4. Contact Us — real details
5. Privacy Policy — legal requirement, unblock this draft
6. Case Studies — only if real ones exist
7. Hiring Advice / News Insights — can use blog posts once workflow is set up

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
