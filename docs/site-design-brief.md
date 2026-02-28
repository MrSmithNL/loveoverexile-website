# Love Over Exile — Site Design Brief & Technical Architecture

> **Status:** Approved plan — approved by Malcolm before build starts
> **Last updated:** 2026-02-28
> **Purpose:** Full specification for the new website build (Astro from scratch)

---

## 1. Competitor Analysis — Key Findings

### Benchmark Sites Reviewed

| Site | What They Do Well | What's Missing |
|------|------------------|----------------|
| **jamesclear.com** (Atomic Habits) | Warm beige palette, minimalist, Articles + Newsletter + Books hub. 3.1M subscribers. | No community |
| **glennondoyle.com** | Raw personal story → millions of readers. Podcast + books + newsletter. "Pod Squad" community. | Complex multi-person ecosystem |
| **markmanson.net** | Content hub + "Solved" paid membership community + podcast. Clear content→community funnel. | Paid/gated |
| **parentalalienationuk.info** | Professional tone, muted earth tones, advocacy content. | Dry, no community interaction, no lived experience voice, no hope |
| **PASG (pasg.info)** | World's leading voice on PA — recognised authority. | Advocacy-focused, not healing-focused |
| **PA advocacy sites generally** | Cover the problem and the legal battle. | None cover the transformation and inner freedom journey |

### The Gap — Malcolm's Competitive Advantage

**No existing parental alienation resource combines:**
1. A lived-experience first-person story (Malcolm's)
2. A real community of people who have been through it
3. A healing and transformation narrative (not just survival)
4. A professional, warm, human design

All current PA sites feel like advocacy organisations, not communities. Love Over Exile can be the first personal, human, hopeful, community-driven platform in this niche.

---

## 2. Design Brief

### Tone
**Warm and personal with a clean professional feel.**
Like a humanitarian foundation or community charity — not corporate, not clinical, not cold.
Feels like: being spoken to by someone who has been through it and came out the other side.

Reference feel: Charity:Water, The Gottman Institute, NAMI (warmth + credibility), British Red Cross (clean + compassionate).

### Colour Palette

| Role | Colour | Hex | Usage |
|------|--------|-----|-------|
| Background | Warm ivory/cream | `#F7F3EE` | Page background |
| Background alt | Warm white | `#FDFBF8` | Cards, sections |
| Primary (headings) | Deep forest green | `#1E3328` | H1, H2, nav |
| Primary alt | Warm charcoal | `#2C2C2C` | Body text |
| Accent | Warm amber/gold | `#C49A3C` | CTAs, highlights, links |
| Accent soft | Pale sage | `#8FA888` | Secondary buttons, tags |
| Dark section | Deep green/dark | `#162B20` | Footer, dark hero sections |

Not stark white/black — everything warm. Not medical blue — hope and nature, not clinical.

### Typography

| Role | Font | Why |
|------|------|-----|
| Headings | **Lora** or **Cormorant Garamond** | Serif — feels like a real book. Literary, personal. |
| Body text | **Inter** or **Source Sans 3** | Clean, readable, professional |
| Pull quotes | Heading font, larger, italic | Highlight Malcolm's voice |
| Navigation | Body font, uppercase tracking | Clean, modern |

All fonts free via Google Fonts. No licence cost.

### Photography Style
- People from behind or in side profile (established in Imagen 4 generation)
- Warm amber/honey tones
- Nature: paths, forests, open water
- Objects of meaning: candle, letter, empty chair
- Never cold or clinical — always warm, hopeful, human
- Generate with Google Imagen 4 (`imagen-4.0-generate-001`)

### Overall Feel
- Generous white space — not cluttered
- Soft border radii (rounded cards, not sharp corners)
- Subtle shadows — depth without heaviness
- Strong typography hierarchy — headings do the heavy lifting
- Full-width section backgrounds that alternate: warm ivory / deep green / ivory

---

## 3. Site Navigation & Structure

### Primary Navigation (always visible)
```
[LOGO]  Home  |  The Book  |  About the Author  |  Articles  |  Community  |  [Get the Free Guide →]
```

Note: CTA is "Get the Free Guide" (the Survival Guide brochure) — offers immediate tangible value. Email/community signup happens as part of the download flow.

### Full Site Map

```
/                              Home

/the-book                      The Book
                               (waitlist, book description, what's inside)

/about                         About the Author
                               (Malcolm's personal journey and story)

/you-are-not-alone             You Are Not Alone
                               (research data — statistics, studies, evidence)

/free-guide                    Free Survival Guide
                               (landing page — PDF download gated behind email/community signup)

/faq                           FAQ
                               ├── Section 1: About Love Over Exile
                               └── Section 2: About Parental Alienation

/articles                      Articles  (all articles index)
  /articles/[slug]             Individual articles

/understanding                 Understanding Parental Alienation (Part 1 hub)
  /articles/understanding/...  Part 1 articles

/survival-guide                Survival Guide (Part 2 hub)
  /articles/survival/...       Part 2 articles

/inner-freedom                 Inner Freedom (Part 3 hub)
  /articles/freedom/...        Part 3 articles

/start-here                    Start Here
                               (curated entry point for first-time visitors)

/community                     Community (Discourse forum landing + link)

/resources                     Resources
  /resources/professionals     Professional Directory (therapists, lawyers, coaches who understand PA)

/contact                       Contact form → info@ email

/privacy-policy                Privacy Policy (already written and published)
```

### Homepage Sections (in order)
1. **Hero** — Malcolm's core statement + "Get the Free Guide" CTA
2. **The Problem** — What parental alienation is (brief, compassionate)
3. **About the Author** — Short version with link to full story
4. **The Book** — Cover + description + waitlist
5. **Three Journeys** (Understanding / Survival / Inner Freedom) — The site's three content hubs
6. **You Are Not Alone** — Key data point (e.g. "22 million children affected worldwide") with link
7. **From the Articles** — Latest 3 articles
8. **Community** — Forum teaser / join
9. **Free Guide** — Download CTA
10. **Footer** — Full navigation, social links, legal

### Footer Navigation
```
The Book          About the Author      You Are Not Alone
Articles          Understanding         Survival Guide
Inner Freedom     FAQ                   Free Guide
Community         Resources             Contact
Privacy Policy    [Social icons]
```

---

## 4. Technical Stack

### Core Site

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Framework | **Astro** | Free | Static site generation |
| Hosting | **Vercel** | Free tier | CDN, HTTPS, git-based deployment |
| Content (Malcolm edits) | **Sanity CMS** | Free tier | Headless CMS — Malcolm edits articles like a word processor |
| Content (articles/pages) | **Markdown + Sanity** | Free | Articles authored in Sanity, stored as structured data |
| Image generation | **Google Imagen 4** | Pay-per-use | AI-generated imagery via `scripts/generate-images.py` |
| Analytics | **Google Analytics 4** | Free | Page views, traffic sources, conversions — embedded in all pages via BaseLayout |
| Cookie consent | Custom GDPR banner | Free | Required for GA + EU visitors. Built into site layout. |
| SEO | **astro-seo** + JSON-LD | Free | Person, Book, Article schema; Open Graph; sitemaps |
| RSS feed | **@astrojs/rss** | Free | Triggers automation pipeline when articles publish |

**Malcolm's GA setup (one-time task, when ready):**
1. Go to analytics.google.com → sign in with msmithnl@gmail.com
2. Create Account: "Love Over Exile"
3. Create Property: "loveoverexile.com"
4. Choose Web → enter https://loveoverexile.com
5. Copy the Measurement ID (format: G-XXXXXXXXXX) → send to Claude → embedded in 2 minutes

### Email Marketing

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Email platform | **MailerLite** | Free → $10/mo | Waitlist, welcome sequences, newsletter |
| Signup form | MailerLite embed | Free | On homepage, The Book page, articles |
| API access | MailerLite API | Included | Claude adds subscribers, triggers campaigns |

### Social Media Automation

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Social API layer | **Ayrshare Premium** | $149/mo | Posts to 13 platforms via single API call |
| Workflow automation | **n8n** (self-hosted) | Free | RSS → Claude → Ayrshare pipeline |
| Platforms | LinkedIn, Instagram, TikTok, YouTube, Facebook, Pinterest | — | Priority order |
| Images for social | Google Imagen 4 | Pay-per-use | Carousel graphics, quote images |
| Claude connection | **Composio MCP** + `ayrshare-automation` skill | Composio fee | Claude calls Ayrshare via MCP tool |

### Community Forum

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Platform | **Discourse** | Free (self-hosted) | Community forum |
| Hosting | Dedicated VPS (Hetzner CX22 or similar) | ~$15/mo | Discourse requires 4 GB RAM |
| AI integration | **Discourse AI Plugin** | Free | Connects Discourse to Claude API |
| Webhook middleware | n8n (same VPS) | Free | Discourse → Claude → Discourse response loop |
| MCP (read) | Discourse MCP CLI | Free | Claude can read/search forum |
| Bot account | "LOE Community Support" | Free | Claude's forum identity — clearly labeled as AI |

### Email Management

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Email accounts | **Zoho Mail** | Free tier | info@, contact@, malcolm@ (already active) |
| Reading emails | Zoho Mail REST API or IMAP | Free | n8n polls every 10 minutes |
| Triage/classification | Claude via n8n | Included | Classify, draft, route, escalate |
| Initial mode | **Tier 1** (read + draft + flag) | — | No auto-send until validated |

### Domain & DNS

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Domain | GoDaddy — loveoverexile.com | Malcolm manages | Point to Vercel when ready |
| DNS change required | CNAME record: `@` → Vercel | One-time | Malcolm sets this in GoDaddy |
| Discourse subdomain | `community.loveoverexile.com` | — | Discourse on VPS |

### Development & Version Control

| Component | Tool | Cost | Purpose |
|-----------|------|------|---------|
| Git repo | GitHub (private) | Free | All site code |
| Deployment | Vercel git integration | Free | Push to main → site auto-rebuilds |
| Sanity Studio | Sanity dashboard | Free | Malcolm's content editing interface |

---

## 5. Total Monthly Cost Estimate

| Item | Monthly Cost |
|------|-------------|
| Vercel | $0 (free tier) |
| Sanity CMS | $0 (free tier, up to 3 users) |
| MailerLite | $0 (free to 500 subscribers) → $10/mo |
| Ayrshare Premium | $149/mo |
| Discourse VPS (Hetzner) | $15/mo |
| n8n (self-hosted on VPS) | $0 |
| Composio | TBC (free tier may suffice) |
| Google Imagen 4 | ~$5-20/mo (pay-per-image) |
| **Total** | **~$170-195/mo** |

Note: Ayrshare ($149) is the primary cost. This covers posting to all 13 social platforms for every article published. The rest of the stack is either free or low cost.

---

## 6. AI System Overview — What Claude Does

### Website Management (Claude Code sessions)
- Builds and maintains the Astro site code
- Writes and publishes articles (via Sanity API or Markdown files)
- Generates images via Imagen 4 script
- Updates and maintains documentation
- Monitors Google Search Console performance

### Social Media (Autonomous — triggered by RSS)
1. New article published → RSS updates → n8n detects
2. Claude reads article → generates: LinkedIn post, Instagram carousel text, TikTok script, newsletter segment
3. Claude calls Ayrshare API (via Composio) → schedules posts across all platforms
4. Claude calls MailerLite API → queues newsletter
5. Log written to `docs/social-posts/` in GitHub

### Forum Moderation (Autonomous — triggered by Discourse webhooks)
- `validate_post` webhook → pre-publication screening → block obvious violations before they go live
- `post_created` webhook → Claude reads → posts welcome/response as "LOE Community Support" bot
- Escalation protocol: crisis keywords → immediate alert to Malcolm, post held for review
- New member → Claude sends welcome message with community guidelines
- Claude clearly identified as AI in bot account profile

### Email (Tier 1 initially — read + draft + flag)
- n8n polls Zoho Mail every 10 minutes
- Claude classifies every incoming email
- FAQ/book enquiries → auto-draft reply for Malcolm's one-click approval
- Sensitive/personal → flagged urgent, no draft, Malcolm notified
- Daily digest sent to Malcolm each morning

---

## 7. Community Strategy

### What the Community Is
"A place for parents who understand, because they've lived it."

Not a support group with volunteers (no capacity). Not a social media group (no permanence). A moderated, AI-assisted forum where lived-experience peers support each other, with Malcolm and Claude as facilitators.

### Forum Categories
1. **Introduce Yourself** — Every new member starts here. Claude welcomes them personally.
2. **Understanding PA** — What is it? How does it work? Resources and explanations.
3. **Court & Legal** — Experiences with the legal system. (Disclaimer: not legal advice)
4. **Emotional Wellbeing** — The personal, emotional side. Most sensitive category.
5. **Survival Strategies** — Practical approaches that have worked for members.
6. **Success Stories** — When things improve. Hope and evidence.
7. **The Book** — Discussion of Love Over Exile chapters. Connects forum to the book.
8. **Resources** — Reading lists, organisations, therapy, podcasts.

### Crisis Protocol
Any post containing keywords related to: suicide, self-harm, harm to children, or expressions of severe distress → post held, immediate notification to Malcolm, Claude sends private message to member with crisis resources (phone lines, emergency services). Malcolm decides on response. Claude never handles crisis alone.

### AI Transparency
"LOE Community Support" bot account has:
- Clear avatar (distinct from Malcolm's photo)
- Profile description: "I'm an AI assistant that helps facilitate discussions and answer questions in this community. For personal or urgent matters, contact Malcolm directly."
- Every post ends with: "— LOE Community Support (AI)"

---

## 8. SEO & Blog Strategy

### Blog Is Not Optional
The blog is the primary growth engine. Without it, the site has no organic traffic pathway.

### Target Keywords (parental alienation niche — low-to-medium competition)
- "how to cope with parental alienation"
- "signs of parental alienation"
- "parental alienation recovery"
- "how to reconnect with alienated child"
- "surviving parental alienation as a father"
- "parental alienation legal options"
- "co-parenting with an alienating parent"

### Publishing Cadence
1-2 long-form articles per month (2,000–3,500 words each). Sustainable and sufficient for this niche.

### Article Structure (designed for repurposing)
Each article always contains:
- Personal hook from Malcolm's story (2-3 sentences)
- Primary keyword in title and first paragraph
- 3-5 numbered insights/steps (→ LinkedIn carousel, TikTok script)
- One key pull quote (→ Instagram graphic, social card)
- Closing CTA: book waitlist or newsletter signup

### SEO Timeline (parental alienation niche)
- Months 1-2: Indexed, zero traffic
- Months 3-4: First rankings (long-tail, position 15-30)
- Months 5-6: Trickle of organic traffic begins
- Months 8-12: Consistent traffic, some articles in top 10
- Month 12+: Compounding growth

### Structured Data
- **Person schema** (Malcolm Smith — author, E-E-A-T signals)
- **Book schema** (Love Over Exile)
- **Article schema** (every blog post)
- **Organization schema** (Love Over Exile)

---

## 9. Backup of WordPress

### Step 1 (immediate, before build starts)
Install UpdraftPlus plugin → export full site (files + database) → save to Google Drive.
This creates a permanent snapshot restorable to any WordPress host.

### Step 2 (when new site goes live)
Point loveoverexile.com to Vercel (Malcolm changes CNAME in GoDaddy — I'll give exact instructions).
Keep WordPress accessible at `classic.loveoverexile.com` as a live backup.

### What Malcolm needs to do in GoDaddy (when ready)
1. Log into GoDaddy DNS management for loveoverexile.com
2. Change the `@` A record to point to Vercel's IP (I'll give exact values)
3. Add a CNAME for `www` → `cname.vercel-dns.com`
4. Done — propagation takes 1-48 hours

---

## 10. Build Order

1. **Set up Sanity CMS** — Malcolm's content editing interface
2. **Build Astro site structure** — layouts, components, design system
3. **Home page** — hero, sections, newsletter signup
4. **The Book page** — waitlist, book description
5. **Malcolm's Story page** — author biography
6. **Articles system** — blog index, article template, Sanity integration
7. **Understanding / Survival / Inner Freedom hubs** — content category pages
8. **Resources page** — reading list
9. **Contact page** — form → email
10. **SEO layer** — JSON-LD, sitemap, Open Graph
11. **MailerLite integration** — waitlist form on homepage + The Book page
12. **Deploy to Vercel** — connect GitHub, deploy
13. **Google Search Console** — verify domain, submit sitemap
14. **Domain cutover** — Malcolm changes GoDaddy DNS
15. **Backup WordPress to classic.loveoverexile.com**
16. **Social media automation** — Ayrshare + n8n pipeline
17. **Email triage system** — n8n + Zoho Mail
18. **Discourse forum** — dedicated VPS, AI plugin, bot account
19. **Ayrshare social accounts** — connect LinkedIn, Instagram, TikTok, YouTube

---

*This document is the agreed plan. No coding begins until Malcolm has approved this brief.*
