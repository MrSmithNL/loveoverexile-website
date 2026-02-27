# Skills Registry — Claude Code

> This document tracks every skill installed in Claude Code.
> Skills extend what Claude can do — think of them as specialist tools that activate when relevant.
>
> **Source:** https://github.com/ComposioHQ/awesome-claude-skills
> **Install location:** `~/.claude/skills/`
> **Total installed:** 864 skills (32 core + 832 Composio automations)
> **Last updated:** 2026-02-27

---

## How Skills Work

Skills are markdown instruction files stored in `~/.claude/skills/`. Claude automatically uses them when the task matches. No activation needed — they work in the background.

To invoke a skill directly: type `/skill-name` in the chat.

---

## Core Skills (32 installed)

### Document Processing

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **PDF Tools** | `pdf` | Extract text/tables, merge/split/annotate PDFs, OCR support | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/document-skills/pdf) |
| **Word Documents** | `docx` | Create, edit, analyse .docx files with tracked changes and comments | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/document-skills/docx) |
| **PowerPoint** | `pptx` | Create and edit .pptx slides with layouts, templates, speaker notes | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/document-skills/pptx) |
| **Excel/Spreadsheets** | `xlsx` | Create, edit, analyse spreadsheets with formulas, charts, data analysis | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/document-skills/xlsx) |

### Writing & Content

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **Content Research Writer** | `content-research-writer` | Collaborative research and writing: outlines, hooks, citations, section feedback | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/content-research-writer) |
| **Article Extractor** | (via connect-apps) | Extract full article text and metadata from web pages | Free | — |
| **Internal Comms** | `internal-comms` | Write internal communications: newsletters, FAQs, status updates, incident reports | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/internal-comms) |
| **Twitter/X Optimizer** | `twitter-algorithm-optimizer` | Optimise posts for maximum reach using algorithm insights | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/twitter-algorithm-optimizer) |
| **Brainstorming** | (built-in) | Transform rough ideas into structured designs through questioning | Free | — |

### Creative & Design

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **Canvas Design** | `canvas-design` | Create visual art (posters, documents) in PDF/PNG — 90% visual, minimal text | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/canvas-design) |
| **Theme Factory** | `theme-factory` | Apply professional colour/font themes to artifacts (10 pre-set themes) | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/theme-factory) |
| **Brand Guidelines** | `brand-guidelines` | Apply official brand colours and typography to artifacts | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/brand-guidelines) |
| **Image Enhancer** | `image-enhancer` | Improve image resolution, sharpness, and clarity | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/image-enhancer) |
| **Slack GIF Creator** | `slack-gif-creator` | Create animated GIFs optimised for Slack with size validators | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/slack-gif-creator) |
| **Artifacts Builder** | `artifacts-builder` | Build React artifacts with Tailwind CSS, shadcn/ui, and Vite | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/artifacts-builder) |

### Research & Analysis

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **Changelog Generator** | `changelog-generator` | Auto-generate user-facing changelogs from git commit history | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/changelog-generator) |
| **Competitive Ads Extractor** | `competitive-ads-extractor` | Scrape and analyse competitor ads from Facebook/LinkedIn libraries | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/competitive-ads-extractor) |
| **Meeting Insights Analyzer** | `meeting-insights-analyzer` | Analyse meeting transcripts for communication patterns and leadership insights | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/meeting-insights-analyzer) |
| **Developer Growth Analysis** | `developer-growth-analysis` | Analyse Claude Code chat history to identify coding patterns and learning gaps | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/developer-growth-analysis) |
| **Lead Research Assistant** | `lead-research-assistant` | Identify and qualify sales leads with fit scores and outreach strategies | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/lead-research-assistant) |

### Productivity & Organisation

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **File Organizer** | `file-organizer` | Intelligently organise files: find duplicates, suggest folder structures | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/file-organizer) |
| **Invoice Organizer** | `invoice-organizer` | Organise invoices/receipts for tax prep: extract data, rename, create CSV | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/invoice-organizer) |
| **Tailored Resume Generator** | `tailored-resume-generator` | Generate resumes tailored to specific job descriptions with ATS optimisation | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/tailored-resume-generator) |
| **Domain Name Brainstormer** | `domain-name-brainstormer` | Generate creative domain names and check availability across TLDs | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/domain-name-brainstormer) |
| **Raffle Winner Picker** | `raffle-winner-picker` | Cryptographically random winner selection from lists or spreadsheets | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/raffle-winner-picker) |

### Development & Automation

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **Connect** | `connect` | Connect Claude to 1000+ apps (Gmail, Slack, GitHub, Notion, etc.) via Composio | Free (Composio account needed) | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/connect) |
| **Connect Apps** | `connect-apps` | Simplified app connection for email, chat, dev tools, docs, CRM, storage | Free (Composio account needed) | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/connect-apps) |
| **Webapp Testing** | `webapp-testing` | Test local web apps using Playwright: verify functionality, capture screenshots | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/webapp-testing) |
| **MCP Builder** | `mcp-builder` | Guide for creating MCP servers to integrate external APIs with Claude | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/mcp-builder) |
| **LangSmith Fetch** | `langsmith-fetch` | Debug LangChain/LangGraph agents by fetching execution traces | Free (LangSmith account needed) | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/langsmith-fetch) |
| **Video Downloader** | `video-downloader` | Download YouTube and other platform videos; extract audio as MP3 | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/video-downloader) |

### Skill Management

| Skill | Folder | What It Does | Cost | Source |
|-------|--------|-------------|------|--------|
| **Skill Creator** | `skill-creator` | Guided workflow for building new custom Claude skills | Free | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/skill-creator) |
| **Skill Share** | `skill-share` | Create and share skills to a Slack channel for team collaboration | Free (Slack needed) | [GitHub](https://github.com/ComposioHQ/awesome-claude-skills/tree/main/skill-share) |

---

## Composio Automation Skills (832 installed)

These skills connect Claude to specific SaaS platforms for automation (send emails, create tasks, post updates, etc.). Each requires a free Composio account at [platform.composio.dev](https://platform.composio.dev) and OAuth authentication with the relevant service.

All 832 are **free** (Composio free tier).

**Categories covered:**

| Category | Examples |
|----------|---------|
| CRM & Sales | HubSpot, Salesforce, Pipedrive, Close, Zoho |
| Project Management | Jira, Asana, Notion, Linear, Trello, ClickUp, Monday |
| Communication | Slack, Discord, Microsoft Teams, Telegram, WhatsApp |
| Email | Gmail, Outlook, SendGrid, Mailchimp, ConvertKit |
| Code & DevOps | GitHub, GitLab, Vercel, CircleCI, Sentry, Supabase |
| Storage | Google Drive, Dropbox, OneDrive, Box |
| Spreadsheets | Airtable, Google Sheets, Coda |
| Social Media | LinkedIn, Twitter/X, Instagram, TikTok, Reddit, YouTube |
| E-commerce | Shopify, Stripe, Square |
| Design | Figma, Canva, Webflow, Miro |
| Analytics | Google Analytics, Mixpanel, Amplitude, PostHog |
| Calendar | Google Calendar, Calendly, Outlook Calendar |
| Support | Zendesk, Freshdesk, Help Scout, Intercom |

To see all 832: `ls ~/.claude/skills/ | grep -automation`

---

## Status Summary

| Status | Count |
|--------|-------|
| Installed — active | 32 core skills |
| Installed — active | 832 Composio skills |
| Requires Composio account | `connect`, `connect-apps` + all 832 automation skills |
| Requires external account | `langsmith-fetch` (LangSmith), `skill-share` (Slack) |

---

## Adding New Skills

```bash
# From a GitHub repo
git clone <repo-url> /tmp/new-skill
cp -r /tmp/new-skill/skill-folder ~/.claude/skills/skill-name

# Verify
ls ~/.claude/skills/skill-name/SKILL.md
```

Skills take effect immediately — no restart needed.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-02-27 | Initial install — 32 core skills + 832 Composio automation skills from awesome-claude-skills repo |
