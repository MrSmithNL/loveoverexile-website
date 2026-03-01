# Metrics & Analytics — Love Over Exile

> What we measure, where we measure it, and what success looks like.
> Last updated: 2026-03-01

---

## Analytics Setup

### Google Analytics 4 (GA4)

| Field | Value |
|-------|-------|
| **Status** | Pending — Malcolm needs to create the property and provide the Measurement ID |
| **Account** | msmithnl@gmail.com at analytics.google.com |
| **Property name** | Love Over Exile (to be created) |
| **Measurement ID** | `G-XXXXXXXXXX` (pending — format will be G- followed by 10 characters) |
| **Implementation** | Script block is pre-written in `site/src/layouts/BaseLayout.astro` — currently commented out. Replace the placeholder ID and uncomment to activate. |
| **GDPR** | Cookie consent banner required before activation. Will be added alongside GA4 setup. |

**To activate (see SITE-002 in `docs/todo.md`):**
1. Malcolm creates GA4 property at analytics.google.com
2. Copies the Measurement ID (G-XXXXXXXXXX) to Claude
3. Claude uncomments the script in BaseLayout.astro, replaces the placeholder
4. Claude adds GDPR cookie consent banner
5. Commit and push — auto-deploys

### Google Search Console (GSC)

| Field | Value |
|-------|-------|
| **Status** | Pending — requires DNS cutover to loveoverexile.com first |
| **Account** | msmithnl@gmail.com at search.google.com/search-console |
| **Verification method** | DNS TXT record (simplest after DNS cutover to Vercel) |
| **Sitemap** | Already generating at `/sitemap-index.xml` via Astro sitemap integration |

**To activate (see SITE-006 in `docs/todo.md`):**
1. Complete DNS cutover (point loveoverexile.com to Vercel)
2. Add property in GSC for loveoverexile.com
3. Verify via DNS TXT record in GoDaddy
4. Submit sitemap URL: `https://loveoverexile.com/sitemap-index.xml`

### MailerLite

| Field | Value |
|-------|-------|
| **Status** | Pending — account not yet created |
| **Free tier** | Up to 1,000 subscribers |
| **What it tracks** | Email signups, open rates, click rates, subscriber growth, group sizes |
| **Groups planned** | "Waitlist — Book", "Free Guide Downloads", "Community Interest" |

---

## Key Performance Indicators (KPIs)

### Primary KPIs — The Numbers That Matter Most

| KPI | Target | Timeframe | Measured In | Why It Matters |
|-----|--------|-----------|-------------|----------------|
| **Email signups** | 50+ per week | By month 3 | MailerLite | Email list is the #1 asset for book launch. Every subscriber is a potential buyer. |
| **Waitlist total** | 500 before book launch | Pre-launch period | MailerLite ("Waitlist — Book" group) | 500 engaged subscribers = strong launch day. This is the single most important pre-launch metric. |
| **Organic traffic** | 1,000+ sessions/month | By month 6 | GA4 | Proves SEO strategy is working. Organic traffic is free, compounding, and sustainable. |

### Secondary KPIs — Supporting Metrics

| KPI | Target | Timeframe | Measured In | Why It Matters |
|-----|--------|-----------|-------------|----------------|
| **Articles published** | 2 per week | Ongoing | Git commit history | Consistent publishing builds SEO authority and gives the newsletter content. |
| **Average session duration** | 2+ minutes | By month 3 | GA4 | People are reading, not bouncing. Indicates content quality and engagement. |
| **Pages per session** | 2+ pages | By month 3 | GA4 | Visitors are exploring, following internal links. Good for SEO and conversion. |
| **Bounce rate** | Under 60% | By month 3 | GA4 | Lower is better. Means visitors find what they came for and stay. |
| **Free guide downloads** | 100+ total | By month 3 | MailerLite ("Free Guide Downloads" group) | Validates the lead magnet. Each download is a warm lead. |
| **Search impressions** | 10,000+/month | By month 6 | Google Search Console | Site is showing up in search results. Awareness is growing. |
| **Click-through rate (search)** | 3%+ | By month 6 | Google Search Console | Title tags and meta descriptions are compelling enough to earn clicks. |
| **Top 10 keyword rankings** | 5+ keywords | By month 6 | Google Search Console / SEO Toolkit | Long-tail keywords are ranking. Proves content-SEO alignment. |

---

## Tracking Sources by KPI

| KPI | GA4 | GSC | MailerLite | Manual |
|-----|-----|-----|------------|--------|
| Email signups | | | Primary | |
| Waitlist total | | | Primary | |
| Organic traffic | Primary | Supporting | | |
| Articles published | | | | Git log |
| Session duration | Primary | | | |
| Pages per session | Primary | | | |
| Bounce rate | Primary | | | |
| Free guide downloads | | | Primary | |
| Search impressions | | Primary | | |
| Search CTR | | Primary | | |
| Keyword rankings | | Primary | | SEO Toolkit |

---

## Milestone Targets

Progress checkpoints to confirm the strategy is working.

### Month 1 (Launch Month)
- [ ] GA4 active and collecting data
- [ ] GSC verified and sitemap submitted
- [ ] MailerLite connected with all 3 groups
- [ ] 8 articles published (2/week)
- [ ] First email signups coming in
- [ ] Site appearing in GSC (impressions starting)

### Month 3
- [ ] 50+ email signups per week
- [ ] 24+ articles published total
- [ ] Average session duration over 2 minutes
- [ ] 100+ free guide downloads
- [ ] Organic traffic measurable and growing

### Month 6
- [ ] 1,000+ organic sessions per month
- [ ] 500+ total waitlist subscribers
- [ ] 5+ keywords in Google top 10
- [ ] 10,000+ search impressions per month
- [ ] Content repurposing pipeline active (newsletter, LinkedIn, social)

### Pre-Launch
- [ ] 500+ waitlist subscribers (minimum for a strong launch)
- [ ] Email open rate above 30%
- [ ] 3+ articles ranking on page 1 for long-tail keywords
- [ ] Community interest list growing

---

## Reporting Cadence

| Frequency | What | Where |
|-----------|------|-------|
| Weekly | Email signup count, articles published, any notable traffic spikes | Quick check — MailerLite dashboard + GA4 |
| Monthly | Full KPI review — all metrics in the table above | Documented in session notes or a monthly summary |
| Quarterly | Strategy review — are the content pillars working? Adjust keyword targets, publishing cadence, or conversion tactics as needed | Update this doc and `docs/content-strategy.md` |

---

## Future: BI Dashboard (INFRA-003)

The agency-level monitoring project (INFRA-003 in `~/Claude Code/Projects/smith-ai-agency/projects/agency-monitoring/`) plans a Looker Studio dashboard pulling data from Google Sheets. When that is built, Love Over Exile metrics will be one of the first data sources connected. Until then, metrics are tracked directly in GA4, GSC, and MailerLite dashboards.

---

## Relationship to Other Docs

| Doc | How it connects |
|-----|----------------|
| `docs/todo.md` | SITE-002 (GA4 setup) and SITE-006 (DNS cutover for GSC) |
| `docs/architecture.md` | GA4 and GSC listed as components with pending status |
| `docs/content-strategy.md` | Publishing targets (2/week) that feed the "articles published" KPI |
| `docs/seo-strategy.md` | Keyword targets that feed the "keyword rankings" KPI |

---

## Change Log

| Date | What changed |
|------|-------------|
| 2026-03-01 | Initial version — analytics setup, KPIs, milestones, reporting cadence |
