# Setup Steps — Love Over Exile

> Every technical step taken on this project, in chronological order.
> Each step includes what was done, why, and **how to reverse it**.
>
> If something breaks, find the step and follow the reversal instructions.

---

## Step 1 — Installed Claude Code on MacBook Pro

**Date:** 2026-02-27
**Category:** Tool installation

**What was done:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Result:**
- Claude Code v2.1.62 installed to `~/.local/bin/claude`

**How to reverse:**
```bash
rm ~/.local/bin/claude
```

---

## Step 2 — Added Claude Code to system PATH

**Date:** 2026-02-27
**Category:** System configuration

**What was done:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

**What this means in plain English:**
This tells your terminal "when I type `claude`, look in the `~/.local/bin/` folder to find it." Without this, your terminal wouldn't know where Claude Code is installed.

**Note:** This command was run twice, so there are two identical lines in ~/.zshrc. This is harmless but we can clean it up later.

**How to reverse:**
Open ~/.zshrc in a text editor and remove the line:
```
export PATH="$HOME/.local/bin:$PATH"
```

---

## Step 3 — Created project folder structure

**Date:** 2026-02-27
**Category:** File structure

**What was done:**
```bash
mkdir ~/Projects/loveoverexile-website
mkdir ~/Projects/loveoverexile-website/docs
```

**What this means in plain English:**
Created a folder called "loveoverexile-website" inside a "Projects" folder in your home directory, with a "docs" subfolder for documentation.

**How to reverse:**
```bash
rm -rf ~/Projects/loveoverexile-website
```
> WARNING: This deletes the entire project folder and everything in it. Only do this if you want to start completely from scratch.

---

## Step 4 — Created documentation framework

**Date:** 2026-02-27
**Category:** Documentation

**What was done:**
Created the following files using Claude Code:
- `README.md` — Project overview and folder structure guide
- `docs/architecture.md` — Visual diagram of the technical setup (Mermaid)
- `docs/decisions-log.md` — Record of all technical decisions with reasoning
- `docs/setup-steps.md` — This file (chronological steps with reversal instructions)
- `docs/accounts-and-access.md` — Registry of all platforms, accounts, and APIs

**What this means in plain English:**
Set up a documentation system so every technical choice and configuration is recorded, visual, and reversible.

**How to reverse:**
Delete any individual file, or all of them. They're documentation only — removing them doesn't break anything technical.

---

## Step 5 — Installed VS Code

**Date:** 2026-02-27
**Category:** Tool installation

**What was done:**
```bash
brew install --cask visual-studio-code
```

**What this means in plain English:**
Installed Visual Studio Code — a free code editor made by Microsoft. It's our main workspace for viewing project files, previewing diagrams, and running Claude Code.

**How to reverse:**
```bash
brew uninstall --cask visual-studio-code
```

---

## Step 6 — Installed GitHub CLI

**Date:** 2026-02-27
**Category:** Tool installation

**What was done:**
```bash
brew install gh
```
Result: GitHub CLI v2.87.3 installed.

**What this means in plain English:**
Installed a command-line tool that lets us create and manage GitHub repositories from the terminal, instead of having to use the website.

**How to reverse:**
```bash
brew uninstall gh
```

---

## Step 7 — Installed Mermaid extension for VS Code

**Date:** 2026-02-27
**Category:** VS Code extension

**What was done:**
```bash
code --install-extension bierner.markdown-mermaid
```

**What this means in plain English:**
Added an extension to VS Code that renders Mermaid diagram code (the text in architecture.md) as actual visual diagrams with boxes and arrows. View any .md file with Cmd + Shift + V to see it.

**How to reverse:**
```bash
code --uninstall-extension bierner.markdown-mermaid
```

---

## Step 8 — Installed Claude Code extension for VS Code

**Date:** 2026-02-27
**Category:** VS Code extension

**What was done:**
```bash
code --install-extension anthropic.claude-code
```

**What this means in plain English:**
Added Claude Code as a chat panel inside VS Code (right sidebar). This means you can talk to Claude, view files, and see diagram previews all in one window instead of switching between apps.

**How to reverse:**
```bash
code --uninstall-extension anthropic.claude-code
```

---

## Step 9 — Created symlink so VS Code can find Claude Code

**Date:** 2026-02-27
**Category:** System configuration

**What was done:**
```bash
sudo mkdir -p /usr/local/bin
sudo ln -sf ~/.local/bin/claude /usr/local/bin/claude
```

**What this means in plain English:**
VS Code couldn't find Claude Code because it was installed in a folder VS Code doesn't check. This created a "signpost" at /usr/local/bin/claude pointing to the real location. Think of it like a shortcut on your Desktop that points to an app.

**Why this was needed:**
The Claude Code extension in VS Code was showing "Error: Claude Code process exited with code 1" because it couldn't locate the claude command.

**How to reverse:**
```bash
sudo rm /usr/local/bin/claude
```

---

## Step 10 — Created GitHub account

**Date:** 2026-02-27
**Category:** Account creation

**What was done:**
Malcolm created a GitHub account at github.com.
- **Username:** MrSmithNL
- **Account URL:** https://github.com/MrSmithNL

**What this means in plain English:**
GitHub is a cloud platform that stores code and project files with full version history. Every change we make gets saved as a "commit" — a permanent record you can always go back to.

**How to reverse:**
GitHub account deletion: github.com → Settings → Account → Delete account (irreversible — avoid unless certain).

---

## Step 11 — Authenticated GitHub CLI

**Date:** 2026-02-27
**Category:** Authentication

**What was done:**
```bash
gh auth login
```
- Protocol: HTTPS
- Authentication: web browser (OAuth)
- Token scopes granted: `repo`, `gist`, `read:org`, `workflow`
- Token stored in: macOS keyring

**What this means in plain English:**
Linked the GitHub CLI tool on your MacBook to your GitHub account. Claude Code can now create repos, commit files, and push changes to GitHub — all acting as you (MrSmithNL).

**How to reverse:**
```bash
gh auth logout
```

---

## Step 12 — Initialized Git repository and pushed to GitHub

**Date:** 2026-02-27
**Category:** Version control

**What was done:**
```bash
git init
git add .
git commit -m "Initial commit — project documentation framework"
gh repo create loveoverexile-website --private --push
```

- Created `.gitignore` to exclude secrets, `.claude/` settings, and macOS junk files
- Set git commit identity: Malcolm Smith / MrSmithNL@users.noreply.github.com (privacy-preserving)
- Repository created as **private** at: https://github.com/MrSmithNL/loveoverexile-website

**What this means in plain English:**
The project folder is now backed up to GitHub. Every time we make changes and commit, the full history is saved in the cloud. If your MacBook dies, nothing is lost.

**Note on email:** Git commits use `MrSmithNL@users.noreply.github.com` — a GitHub-provided address that keeps your real email private.

**How to reverse:**
- Delete the GitHub repo: github.com/MrSmithNL/loveoverexile-website → Settings → Delete repository
- Remove local git history: `rm -rf .git` (removes version control from the folder, keeps the files)

---

## Step 13 — Set up Bitwarden password manager

**Date:** 2026-02-27
**Category:** Credential management

**What was done:**
- Bitwarden CLI (v2025.12.1) was already installed — account `msmithnl@gmail.com` already existed
- Installed Bitwarden desktop app:
```bash
brew install --cask bitwarden
```
- Fixed duplicate PATH entry in `~/.zshrc` (resolves RISK-003)
- Added `bwunlock` shell function to `~/.zshrc`:
```bash
bwunlock() {
  export BW_SESSION=$(bw unlock --raw)
  ...
}
```

**What this means in plain English:**
Bitwarden is a secure password manager. The desktop app lets you browse and manage credentials visually. The CLI lets Claude Code read and create credentials automatically during a session. Running `bwunlock` in the terminal at the start of a session activates vault access for that session only — the vault re-locks when the terminal closes.

**How to use at the start of a session:**
```bash
bwunlock
# Enter master password when prompted
# Vault is now active for this terminal session
```

**How to reverse:**
- Remove `bwunlock` function from `~/.zshrc`
- Uninstall desktop app: `brew uninstall --cask bitwarden`
- CLI was pre-existing — leave in place

---

## Step 14 — Installed Claude Code skills library

**Date:** 2026-02-27
**Category:** Tool enhancement

**What was done:**
Installed all 864 skills from the [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) repository into `~/.claude/skills/`.

```bash
# Clone the repository
git clone https://github.com/ComposioHQ/awesome-claude-skills.git /tmp/awesome-claude-skills

# Install each skill directory
for dir in /tmp/awesome-claude-skills/*/; do
  skill_name=$(basename "$dir")
  cp -r "$dir" ~/.claude/skills/"$skill_name"
done
```

**Result:**
- 32 core skills installed (document processing, writing, design, research, productivity, development)
- 832 Composio automation skills installed (CRM, project management, email, social media, etc.)
- Skills take effect immediately — no restart needed
- Full registry documented in: `~/.claude/docs/skills-registry.md` (global — applies to all projects)

**What this means in plain English:**
Skills are instruction files that teach Claude Code how to do specific tasks — like creating PDFs, writing Twitter posts, downloading videos, or connecting to apps like Gmail, Slack, and Notion. With 864 skills installed, Claude can now handle a much wider range of tasks automatically.

**How to check what's installed:**
```bash
ls ~/.claude/skills/ | wc -l    # Count of installed skills
ls ~/.claude/skills/             # List all skills
```

**How to reverse:**
```bash
rm -rf ~/.claude/skills/
```
> WARNING: This removes all installed skills. Reinstall from the source repo if needed.

---

## Next Steps (Not Yet Done)

- [x] Enable 2-factor authentication on GitHub account ✅ (2026-02-27)
- [x] Enable 2FA on Bitwarden account ✅ (2026-02-27)
- [ ] Set up WordPress REST API access (application password)
- [ ] Create content drafting workflow (local → review → publish)
- [ ] Map existing WordPress site structure (pages, menus, plugins)
