# AGENTS.md — Love Over Exile (CLIENT-001)

> Tool-agnostic agent instructions. Works with Claude Code, Cursor, Codex, Aider, and any tool that supports AGENTS.md.

## Project Overview

Website for "Love Over Exile" — a book on parental alienation by Malcolm Smith. WordPress site at loveoverexile.com serving as book platform, content repository, community hub, and marketing engine. Built with Astro + Vercel.

## Tech Stack

- **CMS:** WordPress (REST API with Application Password)
- **Frontend:** Astro
- **Hosting:** Vercel
- **Linting:** ESLint (flat config, Astro + TypeScript strict)
- **Formatting:** Prettier (with prettier-plugin-astro)
- **Pre-commit:** Husky + lint-staged
- **CI:** GitHub Actions (lint + build, all hard gates)
- **Accessibility:** pa11y-ci (WCAG2AA)
- **Email:** MailerLite

## Commands

```bash
# Lint
npx eslint .

# Format check
npx prettier --check .

# Build
npm run build

# Accessibility check
npx pa11y-ci
```

## Project Structure

```
site/src/        # Astro source (pages, components, layouts)
content/         # Book content, articles, images
docs/            # Architecture, todo, decisions, SEO strategy
research/        # Market and competitor analysis
designs/         # Visual assets, ebook generation
```

## Style Guide

- TypeScript strict, no `any`
- Astro components: `.astro` files with scoped styles
- ESLint + Prettier on every commit (via lint-staged)
- Commit messages: imperative mood

## Boundaries

- **Always do:** Run lint + build before committing. Update docs/todo.md after changes.
- **Ask first:** Code changes to live site, WordPress content changes, sending emails.
- **Never do:** Commit .env files, hardcode credentials, modify DNS without approval.
