# Decisions Log — Love Over Exile

> Every technical decision we make gets recorded here with the reasoning.
> This lets you (or anyone) understand *why* things are the way they are — not just *what* was done.

---

## How to Read This Log

Each entry includes:
- **Decision**: What we chose
- **Alternatives considered**: What else we could have done
- **Why this choice**: The reasoning
- **Revisit if**: When this decision should be reconsidered

---

## Decision #001 — Use Claude Code locally (not VPS bot) for website management

**Date:** 2026-02-27
**Category:** Platform

**Decision:** Use Claude Code on MacBook Pro as the primary tool for managing the WordPress website.

**Alternatives considered:**
1. Open WebUI on VPS — already running, always-on
2. Claude Code locally — full toolset, browser control, file management

**Why this choice:**
- Claude Code can directly interact with WordPress admin via browser automation
- Claude Code can use the WordPress REST API from the terminal
- Full documentation and file management capabilities
- Content drafting workflow: write locally, review, then publish
- VPS bot is chat-only — can't click buttons or navigate websites

**Revisit if:**
- We need 24/7 automated publishing (VPS would be better)
- We set up a CI/CD pipeline that runs from the server

---

## Decision #002 — Project folder at ~/Projects/loveoverexile-website/

**Date:** 2026-02-27
**Category:** File structure

**Decision:** Store project files in ~/Projects/loveoverexile-website/ (not inside Claude Code folder or Desktop).

**Alternatives considered:**
1. ~/Claude Code/loveoverexile/ — inside the tool's folder
2. ~/Desktop/loveoverexile/ — quick access
3. ~/Projects/loveoverexile-website/ — dedicated workspace

**Why this choice:**
- Separates the tool (Claude Code) from the work (projects)
- ~/Projects/ is standard developer convention, scales to multiple projects
- Lowercase with hyphens avoids terminal issues with spaces
- Descriptive name makes it obvious what this folder is for

**Revisit if:**
- We adopt Git version control (folder structure stays the same, just add Git)

---

## Decision #003 — Comprehensive documentation from day one

**Date:** 2026-02-27
**Category:** Process

**Decision:** Maintain four documentation files: architecture diagram, setup steps, decisions log, and accounts registry.

**Alternatives considered:**
1. No documentation — just build things
2. Light notes in a single file
3. Full documentation suite with diagrams

**Why this choice:**
- Malcolm is non-technical — clear docs prevent confusion later
- Architecture diagram gives instant visual understanding of the full setup
- Setup steps with reversal instructions mean nothing is permanent or scary
- Decisions log prevents "why did we do this?" questions months from now

**Revisit if:**
- Documentation becomes burdensome (simplify, don't abandon)

---

## Decision #004 — Use Bitwarden as universal credential vault

**Date:** 2026-02-27
**Category:** Security / Credential management

**Decision:** Use Bitwarden (CLI + desktop) as the single credential vault for all projects. Session-based unlock model: Malcolm runs `bwunlock` at the start of any session requiring credentials; Claude Code reads/writes via the CLI for that session only.

**Alternatives considered:**
1. macOS Keychain — built-in, no extra setup, but no CLI that Claude can easily use
2. 1Password — popular, has a CLI, but paid and Malcolm already has Bitwarden
3. `.env` files only — simple, but no central vault, duplicates across projects
4. Bitwarden with persistent session token stored in a file — rejected (security risk)

**Why this choice:**
- Bitwarden account already existed (`msmithnl@gmail.com`)
- Open source, free tier covers all needs, end-to-end encrypted
- CLI (`bw`) allows Claude Code to read and create credentials autonomously during an unlocked session
- Session token expires when terminal closes — master password never stored anywhere
- One vault across all projects — single place to audit and manage access

**Revisit if:**
- Moving to a team setup (Bitwarden Teams adds shared vaults)
- Need for persistent automation without manual unlock (would require careful re-evaluation of security model)
