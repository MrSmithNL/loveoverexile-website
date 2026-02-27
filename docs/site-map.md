# Site Map — loveoverexile.com

> Pulled via WordPress REST API on 2026-02-27.
> Re-run the API calls in `docs/setup-steps.md` to refresh this whenever the site changes.

---

## What the Site Is

**Love Over Exile** is a recruitment agency website. The site offers services for both employers (hiring) and job seekers (career advice, salary guidance). It has a blog section with articles on recruitment and career topics.

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

**Last real content published:** November 2024 — the site has had no new posts in ~3 months.

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

## Cleanup Needed

These two items are default WordPress placeholders that were never removed:

| Item | Type | ID | Action |
|------|------|----|--------|
| "Sample Page" | Page | 2 | Delete — it's just a WordPress demo page |
| "Hello world!" | Post | 1 | Delete — it's just a WordPress demo post |

And one important item that needs finishing:

| Item | Type | ID | Action |
|------|------|----|--------|
| Privacy Policy | Page (draft) | 3 | Write and publish — required for GDPR compliance |

---

## What to Do Next

Based on this map, the logical priorities are:

1. **Content workflow (WP-002)** — set up a process for drafting and publishing new posts
2. **Privacy Policy** — finish and publish the draft (legal requirement)
3. **Cleanup** — delete the two placeholder items once confirmed
4. **Check plugins and theme** — do this manually via wp-admin (REST API doesn't expose plugin list)
