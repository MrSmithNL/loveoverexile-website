# Love Over Exile — Website Project

**Website:** loveoverexile.com
**Platform:** WordPress
**Managed by:** Malcolm Smith + Claude Code

## What This Project Is

This is the local workspace for managing the loveoverexile.com WordPress website. All content drafts, configuration, documentation, and technical architecture records live here.

## Folder Structure

```
loveoverexile-website/
├── README.md                         ← You are here
├── docs/
│   ├── architecture.md               ← Visual diagram of the full technical setup
│   ├── setup-steps.md                ← Every step taken, in order, with reversal instructions
│   ├── decisions-log.md              ← Why we made each technical choice
│   ├── accounts-and-access.md        ← Registry of all platforms, APIs, accounts (NO passwords)
│   └── security-risk-log.md          ← Active security risks, temporary fixes, and review schedule
├── content/                          ← Draft pages, blog posts, articles before publishing
│   ├── pages/
│   └── posts/
└── assets/                           ← Images, media, files for the website
```

## Key Rules

1. **No passwords or secrets in this folder** — credentials go in `.env` files (gitignored) or your password manager
2. **Every technical change gets documented** — if we can't explain it, we don't do it
3. **Draft before publish** — all content is reviewed locally before going live
4. **Reversibility** — every setup step includes how to undo it
5. **Security risks are named and tracked** — every known risk goes in `docs/security-risk-log.md` immediately, with a review date; temporary solutions are never left undocumented
