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

### SITE-001 — Deploy Astro site to Vercel
**Priority:** ✅ Done — 2026-02-28
**Status:** Live at https://loveoverexile-website.vercel.app/

- Vercel account created (GitHub login)
- GitHub repo connected via Vercel GitHub App
- All 18 pages building and loading correctly
- Auto-deploy active — pushes to `main` trigger new builds
- DNS cutover to loveoverexile.com pending (see SITE-006)

---

### SITE-002 — Set up Google Analytics 4
**Priority:** 🔴 High — should be in place before real traffic starts
**Status:** 🔲 Malcolm action needed

**What Malcolm does:**
1. Go to analytics.google.com → sign in with msmithnl@gmail.com
2. Create Account: "Love Over Exile"
3. Create Property: "loveoverexile.com", Web platform
4. Copy the Measurement ID (format: G-XXXXXXXXXX) → paste to Claude

**What Claude does:**
- Uncomment the GA4 script block in `site/src/layouts/BaseLayout.astro`
- Replace `G-XXXXXXXXXX` with the real ID
- Add GDPR cookie consent banner
- Commit + push → auto-deploys

---

### SITE-003 — Generate site images (Imagen 4)
**Priority:** 🔴 High — pages won't look finished without images
**Status:** 🔲 Ready to run

**Images needed** (all go in `site/public/images/`):
- `hero-path.jpg` — person walking toward light through forest
- `malcolm-smith-author.jpg` — warm author portrait style
- `book-cover.jpg` — book cover design
- `community-warmth.jpg` — warm candlelight / connection
- `survival-guide-cover.jpg` — guide document cover
- `og-default.jpg` — 1200×630 Open Graph default

**How:** Claude runs `scripts/generate-images.py` with new prompts for each
(See loe-image-generator skill)

---

### SITE-004 — Connect MailerLite forms
**Priority:** 🔴 High — waitlist + free guide download is the #1 conversion goal
**Status:** ⏸️ Waiting on MailerLite account setup

**What needs doing:**
1. Create MailerLite account (mailerlite.com — free to 500 contacts)
2. Create group: "Waitlist — Book"
3. Create group: "Free Guide Downloads"
4. Create form embed code → Claude replaces placeholder `<form>` tags in:
   - `site/src/pages/the-book.astro` (waitlist form)
   - `site/src/pages/free-guide.astro` (guide download form)
   - `site/src/pages/community.astro` (notify me form)
5. Set up welcome email + guide delivery automation

---

### SITE-005 — WordPress backup
**Priority:** ✅ Done — 2026-02-28
**Status:** Complete

- Content backup (all pages, posts, 104 media files) exported via REST API → `backups/wordpress-2026-02-28/` (local only, gitignored)
- Full .wpress backup (All-in-One WP Migration) → saved to Google Drive by Malcolm
- WordPress remains live at loveoverexile.com until DNS cutover

---

### SITE-006 — DNS cutover (GoDaddy)
**Priority:** ✅ Done — 2026-03-02
**Status:** Complete

- DNS pointed to Vercel (A record 76.76.21.21, www CNAME cname.vercel-dns.com)
- Custom domain added in Vercel project settings
- SSL certificate auto-provisioned
- Site live at https://loveoverexile.com

---

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

**Note:** Rube MCP is now connected (bearer token auth). MailerLite and Zoho can be connected through Rube once accounts are created.

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
**Status:** ⏭️ Moved to SEO Toolkit project

SEO is now managed by a separate standalone project: `~/Claude Code/Projects/seo-toolkit/`
GitHub: `github.com/MrSmithNL/seo-toolkit` (private)

This includes 8 dedicated agents: Audit, Keywords, Content Optimizer, Rank Tracker, Content Writer, Link Builder, AI Discovery, Reporter.

**Keyword strategy:** documented in `docs/seo-strategy.md` (this repo).
**Full SEO roadmap:** see `seo-toolkit/docs/todo.md`.

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
| SITE-006 | DNS cutover — loveoverexile.com live on Vercel (GoDaddy → Vercel) | 2026-03-02 |
| — | robots.txt created (all crawlers + AI bots, sitemap reference) | 2026-03-02 |
| — | llms.txt created (AI discovery file — site structure, topics, author) | 2026-03-02 |
| — | FAQPage JSON-LD schema added to FAQ page (12 Q&As, rich snippet eligible) | 2026-03-02 |
| — | Article JSON-LD schema added to article template | 2026-03-02 |
| — | Book JSON-LD schema added to The Book page | 2026-03-02 |
| — | Person schema sameAs URLs commented out until social profiles exist | 2026-03-02 |
| — | Full technical SEO audit — all 17 pages checked (titles, meta, h1, OG, schema) | 2026-03-02 |

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
| 2026-02-28 | Major pivot: Abandoned WordPress/Avada. Decision to build from scratch with Astro. |
| 2026-02-28 | Competitor analysis, SEO/social research, community strategy research. Design brief written. |
| 2026-02-28 | Navigation finalised with Malcolm. Astro project scaffolded. Design system, BaseLayout, Nav written. |
| 2026-02-28 | Full site build: 18 pages, Footer, Homepage (10 sections), all inner pages, article template. |
| 2026-02-28 | Build passes with zero errors. Sitemap generating. Pushed to GitHub. Ready for Vercel deploy. |
| 2026-02-28 | SITE-001 — Vercel deployed. All 18 pages live at https://loveoverexile-website.vercel.app/ GitHub auto-deploy active. |
| 2026-02-28 | Logo added, colours changed to teal/coral. SEO strategy written. Rube MCP fixed (bearer token). |
| 2026-02-28 | SEO Toolkit created as separate project (github.com/MrSmithNL/seo-toolkit). 8-agent architecture. Love Over Exile = first client. |
| 2026-03-02 | DNS cutover complete — loveoverexile.com live on Vercel. SEO audit: robots.txt, llms.txt, FAQPage/Article/Book schemas added. GSC + GA4 + SerpAPI OAuth initiated. |
