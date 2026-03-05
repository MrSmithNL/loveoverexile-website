# Love Over Exile — Strategic Operating System

> Cascaded from the company-level Strategic OS (smith-ai-agency/docs/strategic-frameworks.md).
> Contains 4 frameworks adapted for this client engagement. Updated quarterly.
> Last updated: 2026-03-05

---

## 1. Engagement Model Canvas

| Block | Love Over Exile (CLIENT-001) |
|-------|----------------------------|
| **Client Profile** | Malcolm Smith, author. Building a platform for his memoir on parental alienation and family separation. Goal: become the definitive recovery/healing resource for alienated parents, and launch a book. |
| **Value Delivered** | SEO-optimised website (Astro + Vercel), content strategy (5 pillars), AI discoverability (llms.txt, full schema markup), audience building (email waitlist via MailerLite), and eventually book launch marketing. |
| **Delivery Channels** | Managed service — Claude Code executes, Malcolm approves. Fully automated SEO and content pipeline. |
| **Relationship Model** | Internal client. First project for every new agency capability. Continuous engagement, no contract end date. |
| **Revenue from Engagement** | Internal — no direct revenue. Strategic value = proof of concept for PROD-001, case study for agency credibility, and personal project for founder. |
| **Resources Required** | SEO Toolkit (5 agents currently: Audit, AI Discovery, Keywords, SERP, Content Optimizer). Content Writer agent (planned). Claude Code execution time. |
| **Key Activities** | Content publishing (target: 2 articles/week), monthly SEO audits, ongoing technical optimisation, email list building, book launch preparation. |
| **Agency Products Used** | PROD-001 SEO Toolkit (primary). PROD-003 Marketing Engine (planned, for book launch). |
| **Cost to Serve** | ~€0 incremental — shared infrastructure, no dedicated API costs beyond existing SEO Toolkit subscriptions. |

**Company BMC connection:** LOE is the proof-of-concept client in the Customer Segments block. It demonstrates the "AI Operations" primary activity and the "Content & SEO" value proposition. Revenue impact is indirect — credibility and case studies feed the agency's Customer Relationships and Channels blocks.

---

## 2. Client OKRs — Q2 2026 (April–June)

> Feeds into Company O2 (market credibility) and Production BU OKRs.
> See smith-ai-agency/docs/okrs/q2-2026.md for company-level OKRs.

**Objective: Build Love Over Exile into a credible book launch platform**

| # | Key Result | Target | Current | Score |
|---|-----------|--------|---------|-------|
| KR1 | Email waitlist subscribers | 500 | 0 (MailerLite not activated) | — |
| KR2 | Monthly organic sessions | 1,000 | 0 (GA4 not activated) | — |
| KR3 | Keywords in Google top 10 | 5+ | Not tracked (GSC pending) | — |
| KR4 | Articles published (2/week cadence) | 24 | ~5 (manual) | — |

**Alignment:**
- KR1 → Company O2 KR1 (Publish 3 case studies — LOE growth is a case study)
- KR2 → Company O2 KR2 (All client SEO scores at 80+)
- KR3 → SEO & Search Dept KR1 (Automated weekly audits for all clients)
- KR4 → Content & Creative Dept KR2 (Publish 10 optimised articles across client sites)

**Blockers to resolve:**
- GA4 property not created yet → cannot measure KR2
- GSC not connected yet → cannot measure KR3
- MailerLite not set up yet → cannot measure KR1
- DNS cutover to loveoverexile.com needed for GSC

---

## 3. Client Balanced Scorecard

| Perspective | KPI | Current | Target | Source |
|------------|-----|---------|--------|--------|
| **Financial** | Cost to serve | ~€0 incremental | <€20/month | Infrastructure costs |
| **Financial** | Case study value | Not published | 1 published case study | — |
| **Financial** | Book pre-orders | N/A (no book yet) | Launch funnel ready | — |
| **Customer** | SEO audit score | Not measured | 85+ | Audit Agent |
| **Customer** | AI Discovery score | 100 (llms.txt live) | Maintain 85+ | AI Discovery Agent |
| **Customer** | Content quality score | Not measured | 70+ per article | Content Optimizer Agent |
| **Customer** | Email list growth | 0 | 500 by end Q2 | MailerLite |
| **Internal Process** | Publishing cadence | Irregular (~1/month) | 2/week | Content pipeline |
| **Internal Process** | Time from brief to published | Not tracked | <24 hours | — |
| **Internal Process** | Automated audit coverage | Manual per session | Weekly automated | Audit Agent |
| **Learning & Growth** | Parental alienation keyword mastery | Partial (SEO strategy doc) | Full keyword map with monthly tracking | Keywords Agent |
| **Learning & Growth** | Astro/Vercel deployment patterns | Established | Documented and reusable | [architecture.md](architecture.md) |
| **Learning & Growth** | Reusable content templates | 0 | 3 templates (article, guide, resource) | — |

**Company BSC connection:** Engagement feeds the Customer perspective (client SEO improvement metrics). Publishing output feeds Internal Process (factory process compliance). Learnings feed Learning & Growth (new capabilities developed here first, then applied to other clients). See smith-ai-agency/docs/strategic-frameworks.md § Balanced Scorecard.

---

## 4. Client SWOT

> Last reviewed: 2026-03-05 (baseline). Next review: June 2026 (Q2 scoring).

### Strengths (Internal)

- **Unique positioning** — recovery and healing angle, not legal or clinical. No direct competitor covers the same approach.
- **Authentic author voice** — Malcolm's lived experience of parental alienation gives content genuine authority and emotional resonance.
- **AI Discovery score 100** — llms.txt deployed, full schema markup, structured data. Ahead of virtually all competitors on AI visibility.
- **Strong content strategy** — 5 pillars defined, publishing schedule planned, content workflow documented. See [content-strategy.md](content-strategy.md).
- **Modern tech stack** — Astro + Vercel = fast, SEO-friendly, cheap to host, easy to deploy.
- **First-mover advantage** — first project for every new agency capability. Gets the latest tools first.

### Weaknesses (Internal)

- **Pre-launch** — no book published yet. The platform exists but the core product (the book) is not ready.
- **No email list** — MailerLite not set up. No subscriber base to market to.
- **Analytics not active** — GA4 and GSC not connected. Cannot measure organic traffic or keyword rankings.
- **No social media presence** — no Instagram, X/Twitter, or community channels active.
- **Content production slow** — ~5 articles created manually. Target is 2/week but pipeline not yet automated.
- **Single language** — English only. Potential Dutch/international audience not served.

### Opportunities (External)

- **22M+ Americans affected** by parental alienation (Harman research). Large, underserved audience.
- **WHO recognition growing** — parental alienation increasingly recognised in clinical and legal frameworks. Topic gaining mainstream visibility.
- **Healing content massively underserved** — most PA content is legal/adversarial. Recovery-focused resources are rare.
- **Community building potential** — email list, support groups, book clubs, workshops. High engagement potential.
- **Book launch creates marketing moment** — concentrated PR opportunity when book publishes. Website must be ready.
- **Parenting and family wellness keywords** growing in search volume. Topic is trending.

### Threats (External)

- **Established PA organisations** (PASG, ISNAF) have significant domain authority and years of content.
- **Law firm SEO budgets** — family law firms spend heavily on SEO for PA-related keywords.
- **Google algorithm sensitivity** — health/wellness/YMYL content faces higher scrutiny. E-E-A-T matters.
- **Emotional topic risk** — content needs careful handling. Poorly written content could harm rather than help.
- **Book timeline uncertainty** — if the book is delayed, the platform may lose momentum before launch.

**Company SWOT connection:** LOE's unique content positioning is a specific instance of the company's "Early mover on AI visibility" strength. Analytics not being active mirrors the company's "Incomplete financial visibility" weakness. The 22M+ market size opportunity feeds into the company's "Author/book market" opportunity (Book Rocket vertical). See smith-ai-agency/docs/swot-analysis.md.
