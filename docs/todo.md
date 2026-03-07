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
(See website-image-generator skill)

---

### SITE-004 — Connect MailerLite forms
**Priority:** ✅ Done — 2026-03-02
**Status:** Complete — all 3 automations active and sending

- MailerLite account: info@loveoverexile.com (Free plan, 500 subscribers, trial ends 2026-03-14)
- Connected via Composio/Rube MCP (API key auth)
- Three subscriber groups created: Book Waitlist, Free Guide Downloads, Community Notify
- Vercel adapter added (hybrid mode) for server-side `/api/subscribe` endpoint
- Forms wired up on: the-book.astro, free-guide.astro, community.astro
- MAILERLITE_API_KEY set in Vercel env vars (tested + working)
- Domain DNS records correct (DKIM, SPF, DMARC, verification TXT all verified)
- HTML email templates written: `docs/email-templates/` (3 branded templates)
- Malcolm created email designs in MailerLite UI for all 3 automations
- All 3 automation triggers configured via API (subscriber_joins_group → correct group)
- All 3 automations enabled and confirmed working (1 email sent each as of 2026-03-04)

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

### SITE-007 — Write and publish real content (all pages)
**Priority:** 🔴 High
**See:** `docs/site-structure.md` for full page list and implementation order

**Implementation order:**
1. ~~Privacy Policy~~ ✅
2. ~~The Book page~~ ✅
3. ~~Home~~ ✅
4. ~~Understanding What's Happening~~ ✅
5. ~~Malcolm's Story~~ ✅
6. ~~Survival Guide~~ ✅
7. ~~Inner Freedom~~ ✅
8. Articles/Blog — continue publishing content
9. Community/Forum — forum integration
10. Resources — reading list

---

### SITE-008 — Forum / community setup
**Priority:** 🟡 Medium
**Depends on:** SITE-007 (site content established first)

**What needs doing:**
- Choose forum approach for Astro (embedded Discourse, custom, or third-party)
- Set up forum categories mirroring site sections
- Configure moderation (Malcolm as moderator)
- Create /community/forum/ page

---

### SITE-009 — Social media content pipeline
**Priority:** 🟡 Medium
**Depends on:** SITE-007 (content exists first)

**What needs doing:**
Every article structured with: key quote (LinkedIn/Instagram), summary paragraph (newsletter), 5-point list (LinkedIn carousel). Design article template to make repurposing systematic.

---

### SITE-010 — Document VPS and domain registrar details
**Priority:** 🟡 Medium

Malcolm to confirm: VPS provider name + control panel URL, domain registrar. Update `docs/accounts-and-access.md`.

---

### SITE-011 — Confirm Open WebUI setup and access
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
| WP-001 | WordPress site structure mapped → `docs/site-map.md` (pre-Astro) | 2026-02-27 |
| WP-002 | Content workflow built — push script + folder structure (pre-Astro) | 2026-02-27 |
| WP-006 | Book manuscript read in full + memory file written → `memory/book-summary.md` | 2026-02-27 |
| WP-007 | Real site structure designed → `docs/site-structure.md` | 2026-02-27 |
| WP-008 | Email waitlist — superseded by SITE-004 (MailerLite) | 2026-03-02 |
| WP-009 | SEO foundation — moved to SEO Toolkit project (PROD-001) | 2026-02-28 |
| SITE-006 | DNS cutover — loveoverexile.com live on Vercel (GoDaddy → Vercel) | 2026-03-02 |
| — | robots.txt created (all crawlers + AI bots, sitemap reference) | 2026-03-02 |
| — | llms.txt created (AI discovery file — site structure, topics, author) | 2026-03-02 |
| — | FAQPage JSON-LD schema added to FAQ page (12 Q&As, rich snippet eligible) | 2026-03-02 |
| — | Article JSON-LD schema added to article template | 2026-03-02 |
| — | Book JSON-LD schema added to The Book page | 2026-03-02 |
| — | Person schema sameAs URLs commented out until social profiles exist | 2026-03-02 |
| — | Full technical SEO audit — all 17 pages checked (titles, meta, h1, OG, schema) | 2026-03-02 |
| — | GA4 activated (G-HLYGWZ5HZY) — tracking live | 2026-03-02 |
| — | GSC domain property added (sc-domain:loveoverexile.com) — DNS verified | 2026-03-02 |
| — | SerpAPI connected via Composio (100 free searches/month) | 2026-03-02 |
| — | Email routing fixed after DNS cutover (cPanel Local Mail Exchanger) | 2026-03-02 |
| — | Old WordPress files cleaned from cPanel hosting (email-only now) | 2026-03-02 |
| SITE-004 | MailerLite integration — 3 groups, API endpoint, 3 forms wired, 3 automations created | 2026-03-02 |
| SITE-004 | MailerLite automations all active and sending | 2026-03-04 |
| — | MailerLite welcome emails parked — domain auth issue, HTML templates written in docs/email-templates/ | 2026-03-02 |
| — | MailerLite automation triggers configured via API (all 3 bound to groups, complete: true) | 2026-03-02 |
| — | Hub pages filled: Understanding (Part I), Survival Guide (Part II), Inner Freedom (Part III) — all with full content | 2026-03-02 |
| — | 3 real articles published: Signs of PA (8 min), How to Cope (12 min), Choosing Love Over Exile (10 min) | 2026-03-02 |
| — | Contact form backend live — /api/contact endpoint, MailerLite Contact Messages group | 2026-03-02 |

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
| 2026-02-27 | WP-005 — Home page: LOE text content + 13 AI images (Imagen 4, web-optimised) pushed as draft. website-image-generator skill created. |
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
| 2026-03-02 | GA4 activated (G-HLYGWZ5HZY). GSC domain verified. SerpAPI connected. Email routing fixed. WordPress cleaned up (cPanel email-only). |
| 2026-03-02 | SITE-004 — MailerLite integration: Vercel adapter, /api/subscribe endpoint, 3 subscriber groups, 3 forms wired, 3 welcome automations. API key added to Vercel, endpoint tested working. |
| 2026-03-02 | MailerLite welcome emails: domain auth stuck (API says false despite correct DNS). 3 HTML templates written (docs/email-templates/). MailerLite API can't create email design objects. Parked — revisit later. |
| 2026-03-02 | MailerLite automation triggers configured via API. All 3 automations complete: true but enabled: false — MailerLite API has no activation endpoint (confirmed via docs). Malcolm needs to toggle Active in UI. |
| 2026-03-02 | WP-005 — Hub pages filled with real content: Understanding (6 topic cards, key insight, article preview), Survival Guide (6-layer resilience framework, practical tools), Inner Freedom (6 path cards, self-compassion). |
| 2026-03-02 | WP-005 — 3 articles written: Signs of PA (1500 words, Gardner/Baker), How to Cope (2000 words, BIFF/Stockdale/Sphere), Choosing Love Over Exile (1500 words, radical acceptance/surrender). |
| 2026-03-02 | Contact form: /api/contact.ts endpoint created, MailerLite Contact Messages group (180832854326904301), form wired with JS, success/error states. |
