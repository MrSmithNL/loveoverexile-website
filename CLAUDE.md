# Project Instructions — Love Over Exile Website

These instructions apply to this project in every session.

---

## Research-First Protocol — Always Before Planning or Building

Before planning or building any feature, capability, architecture decision, or methodology: run online research FIRST. Find latest frameworks, best practices, lessons learned, anti-patterns, and existing solutions. Mandatory sequence: **Research → Plan → Build**. No exceptions unless Malcolm says "skip research". Save research to `research/` folder with sources and URLs.

---

## Skills Check — Always First

Before taking any action (installing tools, running scripts, setting up integrations, publishing content, building workflows), check `~/.claude/skills/` for a relevant skill. 40 core skills installed (plus ~832 Composio tool connectors). This is non-negotiable.

```
ls ~/.claude/skills/ | grep -i [relevant keyword]
```

If a skill exists: read it, understand what it needs, and use it.
If no skill exists: proceed with the direct approach.

---

## Capability Hierarchy — Mandatory

This project follows the agency's 5-layer capability hierarchy: **Products → Capabilities → Agents → Skills → Tools**. See the [Capability Hierarchy](~/Claude Code/Projects/smith-ai-agency/docs/capability-hierarchy.md) reference. Use terms precisely: Tools are external connections (Composio, MCP, APIs). Skills are procedural knowledge (`~/.claude/skills/`). Agents are autonomous workers (`~/.claude/agents/`). Capabilities are business-level abilities. Products are sellable platforms.

---

## Related Projects

- **Agency standards:** `~/Claude Code/Projects/smith-ai-agency/docs/capabilities/`
- **SEO engine (PROD-001):** `~/Claude Code/Projects/seo-toolkit/` — audits and content optimization
- **CLIENT-002 Hairgenetix:** `~/Claude Code/Projects/hairgenetix/`

---

## Agency-Wide Delivery Framework

This project operates under the agency's autonomous delivery framework. All standards, processes, and department manager oversight apply here:

- **Quality Manager** — Code quality, testing, documentation standards (`smith-ai-agency/docs/capabilities/quality-manager.md`)
- **DevOps Manager** — CI/CD, deployment, infrastructure reliability (`smith-ai-agency/docs/capabilities/devops-manager.md`)
- **Technical Architect** — Architecture decisions, fitness functions, dependency governance (`smith-ai-agency/docs/capabilities/technical-architect.md`)
- **Delivery Manager** — Sprint planning, objective tracking, blocker resolution (`smith-ai-agency/docs/capabilities/delivery-manager.md`)
- **Requirements Engineering** — Spec-driven development, 3-gate process (`smith-ai-agency/docs/capabilities/requirements-engineering.md`)
- **Sprint Management** — 2-week cadence, velocity tracking (`smith-ai-agency/objectives/sprints/`)

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
