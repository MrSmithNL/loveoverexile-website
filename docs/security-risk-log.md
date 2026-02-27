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
**Status:** Open — account not yet created
**Category:** Authentication

**What the risk is:**
GitHub account will be created with only a password. If the password is compromised, someone gains full access to all code, documentation, and project history.

**Current mitigation:**
None yet — account not created.

**Better long-term solution:**
Enable 2FA immediately after account creation using an authenticator app (e.g., Apple's built-in, Google Authenticator, or 1Password). Authenticator apps are more secure than SMS-based 2FA.

**Review by:** Same session as GitHub account creation.

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
**Status:** Temporary fix in place
**Category:** System configuration

**What the risk is:**
During Step 2 (adding Claude Code to PATH), the same line was added to `~/.zshrc` twice. This is harmless in practice but creates minor configuration debt and is a sign of a slightly messy system.

**Current mitigation:**
Accepted — duplicates don't cause any functional or security issue.

**Better long-term solution:**
Open `~/.zshrc` and remove the duplicate line. The file should contain:
```
export PATH="$HOME/.local/bin:$PATH"
```
...only once.

**Review by:** Next routine maintenance session.

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

**Risk level:** 🟡 Medium
**Status:** Open — not yet authenticated
**Category:** Authentication / Access scope

**What the risk is:**
When we run `gh auth login`, the GitHub CLI will request OAuth permissions. By default it requests broad access. Claude Code, acting through this CLI on your machine, will have the same permissions the token grants.

**Current mitigation:**
Not yet set up.

**Better long-term solution:**
During `gh auth login`, choose the minimal required scopes:
- `repo` — access to repositories (needed for our work)
- Avoid granting `admin:org`, `delete_repo`, or other destructive scopes unless specifically needed

Review token permissions at: **github.com → Settings → Developer settings → Personal access tokens**

**Review by:** Same session as GitHub account creation.

---

### RISK-006 — No offsite backup of project folder

**Risk level:** 🟡 Medium
**Status:** Temporary — GitHub push will resolve this
**Category:** Data resilience

**What the risk is:**
The project folder currently exists only on your MacBook. If the machine is lost, stolen, or fails, all documentation, content drafts, and configuration records are gone.

**Current mitigation:**
None yet. Waiting for GitHub setup.

**Better long-term solution:**
Push the repository to GitHub (private repo). This provides an offsite backup automatically on every commit.

**Review by:** End of current GitHub setup session.

---

## Resolved Risks

> Nothing resolved yet — this section will grow over time.

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
