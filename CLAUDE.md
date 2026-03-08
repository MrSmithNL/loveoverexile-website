# Project Instructions — Love Over Exile Website

These instructions apply to this project in every session.

---

## Research-First Protocol — Always Before Planning or Building

Before planning or building any feature, capability, architecture decision, or methodology: run online research FIRST. Find latest frameworks, best practices, lessons learned, anti-patterns, and existing solutions. Mandatory sequence: **Research → Plan → Build**. No exceptions unless Malcolm says "skip research". Save research to `research/` folder with sources and URLs.

---

## Skills Check — Always First

Before taking any action (installing tools, running scripts, setting up integrations, publishing content, building workflows), check `~/.claude/skills/` for a relevant skill. 864 are installed. This is non-negotiable.

```
ls ~/.claude/skills/ | grep -i [relevant keyword]
```

If a skill exists: read it, understand what it needs, and use it.
If no skill exists: proceed with the direct approach.

---

## Architecture Maintenance — Always Automatic

After any change that adds, modifies, or removes a service, tool, account, connection, or credential:
1. Update `docs/architecture.md` — diagram, components, connections, accounts, change log
2. Update `docs/todo.md` — mark completed items, add new ones
3. Commit and push both files

This happens automatically without being asked. Malcolm should never need to request it.

---

## Autonomous Permissions

Malcolm has granted full autonomous permission for the following — no confirmation needed:

- **Update any `.md` documentation file** — site-map.md, todo.md, decisions-log.md, accounts-and-access.md, architecture.md, setup-steps.md, security-risk-log.md, or any new docs file
- **Create new documentation files** in the `docs/` folder
- **Commit and push** documentation-only changes to GitHub
- **Update project memory files** in `~/.claude/projects/.../memory/`

For code changes, scripts, or anything that touches the live WordPress site — still confirm with Malcolm first.

---

## Project Summary

**Love Over Exile** is a book written by Malcolm Smith on the topic of parental alienation.

The website serves four purposes:
1. **Book platform** — pre-launch waitlist, eventual sales/info page
2. **Content repository** — articles and resources for alienated parents, grounded in the book
3. **Community hub** — moderated forum for alienated parents to connect
4. **Marketing engine** — content repurposed across LinkedIn, social media, and other channels

The book structure drives the site structure. The book is not yet published.

## Tech Stack

- **CMS:** WordPress at loveoverexile.com
- **Theme:** Avada (installed with Recruitment demo — all demo content will be replaced)
- **API access:** WordPress REST API with Application Password (credentials in .env)
- **Version control:** GitHub — github.com/MrSmithNL/loveoverexile-website (private)
- **Credentials:** Bitwarden

## Key Docs

| File | What It Covers |
|------|---------------|
| `docs/todo.md` | All open and completed tasks — check at session start |
| `docs/site-map.md` | Current WordPress page/post structure + planned real structure |
| `docs/decisions-log.md` | Every technical decision with reasoning |
| `docs/architecture.md` | Project-specific infrastructure diagram |
| `docs/accounts-and-access.md` | All platforms, accounts, and credentials reference |
