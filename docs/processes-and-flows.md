# Processes & Flows — Love Over Exile

> How things get done on this project. Step-by-step workflows for every repeatable process.
> Last updated: 2026-03-01

---

## 1. Content Publishing Flow

How a new page or article goes from idea to live on the website.

```
Write content (Markdown or Astro)
    ↓
Claude reviews / revises for SEO + tone
    ↓
git add + git commit + git push to main
    ↓
Vercel auto-deploys (triggered by push to main)
    ↓
Live at loveoverexile-website.vercel.app
    ↓
(After DNS cutover → live at loveoverexile.com)
```

**Steps in detail:**

1. **Write** — Create or edit a file in `site/src/pages/` (Astro pages) or `site/src/content/` (articles). Use the page structure from `docs/site-structure.md` and keyword targets from `docs/seo-strategy.md`.
2. **Review** — Claude checks for SEO (keywords, meta description, internal links), tone (resilience language, not victim language), accessibility (alt text, heading hierarchy), and technical correctness (valid Astro/Tailwind syntax).
3. **Commit and push** — `git add` the changed files, commit with a descriptive message, `git push origin main`.
4. **Auto-deploy** — Vercel detects the push to `main` and builds the site automatically. Build takes about 30 seconds. If the build fails, Vercel keeps the previous version live and reports the error.
5. **Verify** — Check the live URL to confirm the page looks correct.

**Old WordPress workflow (archived):** The original flow used `scripts/push-to-wordpress.py` to push Markdown files as WordPress drafts. See `docs/content-workflow.md` for the full detail — kept for reference but no longer the primary workflow since the pivot to Astro on 2026-02-28.

> **See also:** `docs/content-workflow.md` for the legacy WordPress content workflow documentation.

---

## 2. Image Generation Flow

How images are created, optimised, and added to the site.

```
Define image needed (description, aspect ratio, SEO filename)
    ↓
Generate with Google AI Studio (Imagen 4 API)
    ↓
Optimise with Pillow (file size targets)
    ↓
Save to site/public/images/
    ↓
Reference in Astro page with proper alt text
    ↓
Commit + push → auto-deploy
```

**Steps in detail:**

1. **Define** — Write a clear prompt describing the image. Include the desired aspect ratio and an SEO-friendly filename (see naming convention in `docs/seo-strategy.md`).
2. **Generate** — Run `python3 scripts/generate-images.py` with the prompt and parameters. This calls the Imagen 4 API via the Google AI Studio API key stored in `.env`.
3. **Optimise** — The script automatically optimises the output with Pillow. Target sizes:
   - 16:9 backgrounds: under 150 KB
   - Card images: under 90 KB
   - Inline images: under 90 KB
   - Mobile hero: under 100 KB
4. **Save** — Output goes to `site/public/images/` with the SEO filename.
5. **Add to page** — Reference the image in the relevant Astro page with proper alt text (80-125 characters, descriptive, keyword-natural). See alt text standards in `docs/seo-strategy.md`.
6. **Deploy** — Commit and push. Vercel auto-deploys with the new image.

**Skill available:** `~/.claude/skills/loe-image-generator/SKILL.md` — check this before generating images.

---

## 3. Email Capture Flow

How visitors become subscribers. This flow is pending MailerLite account setup (see SITE-004 in `docs/todo.md`).

```
Visitor lands on page with signup form
    ↓
Enters email address → submits form
    ↓
MailerLite receives submission
    ↓
Subscriber added to appropriate group
    ↓
Welcome automation triggers
    ↓
(If Free Guide) → guide PDF delivered by email
```

**Steps in detail:**

1. **Visitor arrives** — Pages with signup forms: `/the-book` (waitlist), `/free-guide` (guide download), `/community` (notify me), Homepage (waitlist CTA).
2. **Form submission** — MailerLite embedded form captures email. Form is embedded directly in the Astro page markup (replacing the current placeholder `<form>` tags).
3. **Group assignment** — MailerLite routes the subscriber to the correct group:
   - **"Waitlist — Book"** — subscribers from `/the-book` and Homepage
   - **"Free Guide Downloads"** — subscribers from `/free-guide`
   - **"Community Interest"** — subscribers from `/community`
4. **Welcome automation** — MailerLite triggers a welcome email sequence:
   - Waitlist: "Thanks for joining — here's what Love Over Exile is about"
   - Free Guide: "Here's your guide" + PDF attachment or download link
   - Community: "We'll let you know when the community launches"
5. **Ongoing** — Subscribers receive the newsletter when content is published. Unsubscribe link in every email (MailerLite handles this automatically).

**Status:** Pending. Requires MailerLite account creation (free tier: 1,000 contacts). See `docs/todo.md` items SITE-004 and WP-008.

---

## 4. Deployment Flow

How code changes reach the live site.

```
Local development (site/ folder)
    ↓
npm run build (local check — catches errors before push)
    ↓
git push origin main
    ↓
Vercel GitHub App detects push
    ↓
Vercel runs: npm ci → npm run build
    ↓
If build succeeds → deployed to production
If build fails → previous version stays live, error reported
```

**Key details:**

- **Hosting:** Vercel (connected via GitHub App)
- **Build command:** `npm run build` (runs `astro build`)
- **Output:** Static HTML + CSS + JS
- **Auto-deploy:** Every push to `main` triggers a production deploy
- **PR previews:** Vercel creates preview deployments for pull requests
- **Rollback:** Previous deployments are kept in Vercel — can be promoted back to production from the Vercel dashboard

---

## 5. SEO Content Pipeline

How articles are planned, written, and optimised for search.

```
Pick keyword target from docs/seo-strategy.md
    ↓
Research topic (book manuscript + external sources)
    ↓
Write article (1,200+ words, keyword-optimised)
    ↓
Claude reviews for SEO checklist
    ↓
Add internal links (→ /the-book, /community, related articles)
    ↓
Commit + push → auto-deploy
    ↓
Submit URL to Google Search Console (after GSC setup)
```

**SEO checklist for every article:**

- Primary keyword in title tag, H1, first 100 words, and URL slug
- Secondary keywords used naturally throughout
- Meta description under 155 characters, includes primary keyword
- At least 2 internal links (one to `/the-book`, one to a related page)
- Image with SEO filename and descriptive alt text
- Minimum 1,200 words
- FAQ section at the bottom (targets Featured Snippets)

**Content sources:**

- Malcolm's book manuscript (50KB summary available in `content/source/`)
- Original research and statistics
- Community stories (with permission, once the community is established)

---

## Change Log

| Date | What changed |
|------|-------------|
| 2026-03-01 | Initial version — 5 workflows documented |
