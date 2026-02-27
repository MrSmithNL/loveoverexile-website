# Security Risk Log — Love Over Exile

> This document tracks every known security risk, authentication decision, and temporary solution
> in this project. Its purpose is to keep us in control as the system grows in complexity.
>
> **Review cadence:** Check this file before every major change, and do a full review at least once a month.
> When a risk is resolved, mark it resolved — don't delete it. History matters.

---

## How to Read This Log

Each entry includes:
- **Risk level:** 🔴 High / 🟡 Medium / 🟢 Low
- **Status:** Open / Temporary fix in place / Resolved
- **What the risk is**
- **Current mitigation** (what we're doing about it right now)
- **Better long-term solution** (what we should move to when time allows)
- **Review by:** Suggested deadline to revisit

---

## Active Risks

---

### RISK-001 — GitHub account has no 2-factor authentication yet

**Risk level:** 🔴 High
**Status:** Open — account created, 2FA not yet enabled
**Category:** Authentication

**What the risk is:**
GitHub account (MrSmithNL) exists with only a password. If the password is compromised, someone gains full access to all code, documentation, and project history.

**Current mitigation:**
Account created 2026-02-27. Password presumably stored in password manager.

**Better long-term solution:**
Enable 2FA immediately using an authenticator app (e.g., Apple's built-in, Google Authenticator, or 1Password). Authenticator apps are more secure than SMS-based 2FA.
Path: github.com → Settings → Password and authentication → Enable 2FA

**Review by:** Next session — do this before any other work.

---

### RISK-007 — Bitwarden account has no 2-factor authentication confirmed

**Risk level:** 🟢 Low
**Status:** Resolved — moved to Resolved Risks section below

---

### RISK-002 — WordPress REST API access not yet configured

**Risk level:** 🟡 Medium
**Status:** Open
**Category:** API access

**What the risk is:**
When we set up the WordPress REST API with an application password, that password will grant programmatic write access to the website. If it's stored insecurely or scoped too broadly, it's a meaningful attack surface.

**Current mitigation:**
Not set up yet — no risk exists until it's created.

**Better long-term solution:**
- Use WordPress Application Passwords (built-in feature) with a descriptive label so we know what each one is for
- Store in a `.env` file that is gitignored (never pushed to GitHub)
- Create one application password per use case (e.g., one for Claude Code, one for any future automation) — not a single shared password for everything
- Revoke individual passwords if a use case changes

**Review by:** When WordPress REST API is set up.

---

### RISK-003 — Duplicate PATH entry in ~/.zshrc

**Risk level:** 🟢 Low
**Status:** Resolved — moved to Resolved Risks section below

---

### RISK-004 — Unknown/unaudited accounts and access points

**Risk level:** 🟡 Medium
**Status:** Open — TBD items in accounts-and-access.md
**Category:** Access inventory

**What the risk is:**
Several accounts and services are listed as "TBD" in `accounts-and-access.md`: VPS provider, domain registrar, Open WebUI access URL, and credentials storage method. Unknown access points can't be monitored or secured.

**Current mitigation:**
Documented as TBD — at least we know they're unknown.

**Better long-term solution:**
Complete the TBD items in `docs/accounts-and-access.md`. For each one:
- Confirm what the login is and where it's stored
- Enable 2FA wherever available
- Review whether access is still needed

**Review by:** Within the next two weeks.

---

### RISK-005 — GitHub CLI token scope

**Risk level:** 🟢 Low
**Status:** Acceptable — scopes reviewed and documented
**Category:** Authentication / Access scope

**What the risk is:**
The GitHub CLI OAuth token grants Claude Code broad terminal access to GitHub as MrSmithNL.

**Current mitigation:**
Token granted scopes: `repo`, `gist`, `read:org`, `workflow`. No destructive admin scopes (`admin:org`, `delete_repo`) were granted. Stored in macOS keyring.

**Better long-term solution:**
Monitor token at: github.com → Settings → Developer settings → Authorized OAuth Apps → "GitHub CLI"
Revoke if device is lost or access needs to be removed: `gh auth logout`

**Review by:** Routine — check during monthly security review.

---

### RISK-006 — No offsite backup of project folder

**Risk level:** 🟢 Low
**Status:** Resolved — moved to Resolved Risks section below

---

## Resolved Risks

---

### RISK-003 — Duplicate PATH entry in ~/.zshrc ✅

**Risk level:** 🟢 Low → Resolved
**Resolved on:** 2026-02-27
**Category:** System configuration

**What the risk was:**
`~/.zshrc` contained two identical `export PATH` lines from Step 2. Harmless but messy.

**How it was resolved:**
`~/.zshrc` was rewritten during Bitwarden setup (Step 13) — duplicate removed, single clean PATH entry remains.

---

### RISK-007 — Bitwarden account 2FA ✅

**Risk level:** 🔴 High → Resolved
**Resolved on:** 2026-02-27
**Category:** Authentication

**What the risk was:**
Bitwarden vault had unconfirmed 2FA status. As the master credential vault for all projects, a compromised account without 2FA would expose everything.

**How it was resolved:**
2FA enabled on Bitwarden account (`msmithnl@gmail.com`) using Google Authenticator.

**Note:** Preferred 2FA method going forward is Apple Passwords (built-in, no extra account needed). Google Authenticator works fine but is an extra app. Consider migrating to Apple Passwords authenticator when convenient.

---

### RISK-006 — No offsite backup of project folder ✅

**Risk level:** 🟡 Medium → Resolved
**Resolved on:** 2026-02-27
**Category:** Data resilience

**What the risk was:**
Project folder existed only on MacBook. Loss or failure of the machine would lose all work.

**How it was resolved:**
Private GitHub repository created at https://github.com/MrSmithNL/loveoverexile-website and project pushed. All future commits are automatically backed up offsite.

**Ongoing requirement:**
Commit and push regularly — backup only covers what has been committed.

---

## Review History

| Date | Reviewed by | Notes |
|------|-------------|-------|
| 2026-02-27 | Malcolm + Claude | Initial log created. 6 risks identified and documented. |

---

## Principles for Managing Security Risk

1. **Name the risk before it bites you** — document risks when they're created, not after something goes wrong
2. **Temporary is only temporary if you write it down** — undocumented "temporary" solutions become permanent by default
3. **Least privilege** — every account and token should have only the access it actually needs
4. **One credential per purpose** — don't reuse passwords or tokens across different use cases
5. **Audit regularly** — review this log at least monthly and before any major change
6. **No account sprawl** — never create a new account to support another account; if a feature requires a third-party service, find the built-in alternative first; every account must justify its existence
