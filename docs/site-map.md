# Site Map — loveoverexile.com

> Pulled via WordPress REST API on 2026-02-27. Theme confirmed via wp-admin: **Avada Recruitment**.
> Re-run the API calls in `docs/setup-steps.md` to refresh this whenever the site changes.

---

## Theme: Avada Recruitment

The site uses the **Avada Recruitment** theme — a premium WordPress theme purpose-built for recruitment agencies. It ships with a full demo content pack, which is what is currently live on the site.

**This means: all current content (pages, posts, images, text) is demo content from the theme installer — none of it is real Love Over Exile content.**

The demo content is useful because it shows us:
- What page layouts and sections the theme supports (hero banners, service cards, testimonials, case study layouts, team sections, etc.)
- What the navigation structure could look like
- What blog post formats and categories the theme supports
- What content *types* we need to create (e.g. we'll need real case studies, real service descriptions, real team bios)

The task ahead is to **replace all demo content with real Love Over Exile content**, using the existing page structure as a template.

---

## What the Site Is

**Love Over Exile** is a recruitment agency. The site's structure (set up by the Avada Recruitment demo) covers both sides of recruitment: services for employers (hiring) and resources for job seekers (career advice, salary guidance). The blog section is called "News Insights".

---

## Page Structure (13 published + 1 draft)

### Top-Level Pages

| ID | Title | URL | Notes |
|----|-------|-----|-------|
| 1023 | Recruitment Home Alt | https://loveoverexile.com/ | **Actual homepage** — served at the root URL |
| 21 | Recruitment Home | https://loveoverexile.com/recruitment-home/ | Old/alternative homepage — not linked from nav |
| 1887 | About Us | https://loveoverexile.com/about-us/ | |
| 2324 | Our Services | https://loveoverexile.com/our-services/ | Parent page for service sub-pages |
| 2530 | News Insights | https://loveoverexile.com/news-insights/ | Blog index page |
| 2420 | Contact Us | https://loveoverexile.com/contact-us/ | |
| 3446 | Case Studies | https://loveoverexile.com/case-studies/ | |
| 3836 | Hiring Advice | https://loveoverexile.com/hiring-advice/ | |
| 2 | Sample Page | https://loveoverexile.com/sample-page/ | ⚠️ Default WordPress placeholder — should be deleted |

### Service Sub-Pages (children of Our Services, ID: 2324)

| ID | Title | URL |
|----|-------|-----|
| 3242 | Career Counseling | https://loveoverexile.com/our-services/career-counseling/ |
| 3418 | Executive Search | https://loveoverexile.com/our-services/executive-search/ |
| 3424 | Talent Sourcing | https://loveoverexile.com/our-services/talent-sourcing/ |
| 3429 | Jobs Advertising | https://loveoverexile.com/our-services/jobs-advertising/ |

### Draft Pages (not yet published)

| ID | Title | Notes |
|----|-------|-------|
| 3 | Privacy Policy | Required by law — needs to be finished and published |

---

## Posts (7 published, 0 drafts)

| ID | Title | Date | URL |
|----|-------|------|-----|
| 638 | Attracting the top talent: Strategies for hiring executives | 2024-11-19 | https://loveoverexile.com/attracting-the-top-talent-strategies-for-hiring-executives/ |
| 640 | Get recruiter's insider tips for crafting the perfect resume | 2024-11-19 | https://loveoverexile.com/get-recruiters-insider-tips-for-crafting-the-perfect-resume/ |
| 642 | How recruitment agencies can help startups build teams | 2024-11-20 | https://loveoverexile.com/how-recruitment-agencies-can-help-startups-build-teams/ |
| 645 | Your perfect guide to navigate salary negotiations | 2024-11-20 | https://loveoverexile.com/your-perfect-guide-to-navigate-salary-negotiations/ |
| 653 | The future of recruitment: Trends to watch by job seekers | 2024-11-20 | https://loveoverexile.com/the-future-of-recruitment-trends-to-watch-by-job-seekers/ |
| 656 | Why soft skills are key to career growth in today's market | 2024-11-20 | https://loveoverexile.com/why-soft-skills-are-key-to-career-growth-in-todays-market/ |
| 1 | Hello world! | 2026-02-13 | https://loveoverexile.com/hello-world/ | ⚠️ Default WordPress placeholder — should be deleted |

**Note:** All 6 posts are demo content from the Avada Recruitment theme — not real Love Over Exile articles. They need to be replaced with real content (or deleted and replaced).

---

## Post Categories (5)

| ID | Name | Post Count |
|----|------|-----------|
| 46 | For Employers | 2 |
| 48 | Talent Strategies | 2 |
| 47 | Recruitment | 1 |
| 45 | Case Study | 1 |
| 1 | Uncategorized | 1 — "Hello world!" placeholder |

## Post Tags (7)

HR Process, Jobs, Leadership, Marketing, Productivity, Research, Trending

---

## What Needs to Be Done

### 1. Replace all demo content with real content
Every page and post needs real Love Over Exile content. The demo gives us the structure and layout options — we fill it with the real story, services, and expertise.

| Page / Section | What's Needed |
|----------------|--------------|
| Homepage | Real headline, value proposition, real service highlights |
| About Us | Real company story, team, mission |
| Our Services (x4) | Real descriptions of each service Love Over Exile actually offers |
| Case Studies | Real case studies (or remove if none ready yet) |
| Hiring Advice | Real advice content (or use blog posts) |
| News Insights (blog) | Real articles — replace all 6 demo posts |
| Contact Us | Real contact details, real form |

### 2. Fix the privacy policy
| Item | Type | ID | Action |
|------|------|----|--------|
| Privacy Policy | Page (draft) | 3 | Write and publish — legally required (GDPR) |

### 3. Delete the WordPress default placeholders
| Item | Type | ID | Action |
|------|------|----|--------|
| "Sample Page" | Page | 2 | Delete |
| "Hello world!" | Post | 1 | Delete |

---

## What to Do Next

1. **Decide on real content** — What are Love Over Exile's actual services? What's the real story? This is the content we'll write.
2. **Content workflow (WP-002)** — Set up a process to draft content here locally, review it, then publish to WordPress
3. **Privacy Policy** — Can be generated and published quickly once we know the company details
4. **Cleanup** — Delete the two WordPress default placeholders
