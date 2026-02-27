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
- Theme: **Avada** (installed with Recruitment demo — all demo content, none of it real)
- Site purpose: Book platform + parental alienation community + marketing engine
- All 13 pages and 6 posts are demo content — will be replaced
- Draft Privacy Policy exists (ID: 3) — needs writing and publishing
- Two default WP placeholders to delete: "Sample Page" and "Hello world!"

---

### WP-006 — Get book manuscript into the project
**Priority:** 🔴 High — blocks everything else

**What needs doing:**
The book is the core of the entire website. Without it, we can't design the site structure, write any content, or plan the SEO strategy.

Malcolm has the book files on Google Drive (manuscript + images).

**Options to share the file:**
1. **Download and drop into project folder** — Malcolm downloads from Drive, places in `content/source/` folder in this project. Claude can then read it directly.
2. **Share Google Drive link** — Malcolm shares the folder/file as a link; Claude fetches it.

**Next step:** Malcolm to share the file however works best.

---

### WP-007 — Design the real site structure (based on book)
**Priority:** 🔴 High
**Depends on:** WP-006 (need the book first)

**What needs doing:**
Once we have the book, map its structure (chapters / themes) to a site structure:
- What pages does the site need?
- What goes in the main navigation menu?
- What content sections mirror the book's chapters?
- What extra content does the site add that the book doesn't cover?

Document the result in `docs/site-structure.md`.

---

### WP-008 — Set up email waitlist / subscription
**Priority:** 🔴 High — book not yet published, visitors need a way to sign up

**What needs doing:**
Visitors who land on the site before the book is published need to be able to sign up for a notification when it launches. This is the most important conversion action on the site right now.

**Steps (to design):**
- Choose an email platform (Mailchimp, Kit/ConvertKit, or similar)
- Set up a signup form on the homepage and "The Book" page
- Connect form to email list
- Set up a welcome/confirmation email

---

### WP-002 — Set up content drafting and publishing workflow
**Priority:** 🔴 High

**What needs doing:**
A reliable way to write content locally and push it to WordPress:
1. Draft locally as Markdown files in `content/` folder
2. Review with Malcolm before publishing
3. Push to WordPress via REST API as a draft post/page
4. Malcolm reviews in wp-admin, publishes manually

**Steps:**
- Create `content/pages/` and `content/posts/` folder structure
- Write a push script: Markdown file → WordPress draft via REST API
- Test with one page

---

### WP-009 — SEO foundation setup
**Priority:** 🔴 High — should be done before any real content goes live

**What needs doing:**
Before publishing any real pages, the SEO basics need to be in place:
- Install and configure an SEO plugin (Yoast or Rank Math) — check if already installed
- Set site title and tagline correctly
- Set up Google Search Console
- Plan keyword strategy based on the book's topics
- Every page will need: title tag, meta description, proper heading structure (H1/H2/H3), internal links

---

### WP-005 — Write real content for all pages
**Priority:** 🔴 High
**Depends on:** WP-006 (book), WP-007 (structure), WP-002 (workflow)

**Pages to create (rough order):**
1. Homepage — headline, book intro, waitlist signup
2. About Malcolm — story, credentials, why this book
3. The Book — what it covers, who it's for, waitlist CTA
4. Topic/chapter pages — one page per major theme in the book
5. Articles/blog — expanded content on each topic
6. Community / Forum — intro page + forum setup
7. Resources — external links, support organisations
8. Contact Us — real details
9. Privacy Policy — legal requirement (GDPR)

---

### WP-010 — Forum setup
**Priority:** 🟡 Medium
**Depends on:** WP-007 (structure)

**What needs doing:**
A moderated forum where alienated parents can connect. Options:
- **bbPress** — free WordPress plugin, integrates natively, simple to moderate
- **BuddyPress** — more social network-style, heavier
- Recommendation: bbPress first, can upgrade later

**Steps (future session):**
- Install bbPress plugin
- Set up forum categories based on the book's topics
- Configure moderation settings
- Create forum landing page

---

### WP-011 — Social media content pipeline
**Priority:** 🟡 Medium
**Depends on:** WP-005 (content exists first)

**What needs doing:**
Articles written for the website should be structured so they can easily be:
- Cut down into LinkedIn posts
- Turned into Twitter/X threads
- Used as newsletter content

This is a workflow design task — not building the social accounts, just making sure the content is structured to work across channels.

---

### WP-003 — Document VPS and domain registrar details
**Priority:** 🟡 Medium

**What needs doing:**
VPS provider and domain registrar are listed as "TBD" in the architecture docs. Malcolm to confirm:
1. VPS provider name and control panel URL
2. Domain registrar name
3. Confirm credentials are in Bitwarden
4. Update `docs/accounts-and-access.md` and `docs/architecture.md`

---

### WP-004 — Confirm Open WebUI setup and access
**Priority:** 🟢 Low

**What needs doing:**
Open WebUI is listed as "Active" but with TBD credentials. Confirm:
1. What URL is it accessible at?
2. How is it secured?
3. Is it still being used?

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
| 2026-02-27 | Site purpose clarified — book platform + parental alienation community. All docs updated. |
