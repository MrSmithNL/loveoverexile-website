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

## Next Steps (Not Yet Done)

- [ ] Create GitHub account (Malcolm — must do this manually at github.com)
- [ ] Initialize Git repository and push project to GitHub
- [ ] Set up WordPress REST API access (application password)
- [ ] Create content drafting workflow (local → review → publish)
- [ ] Map existing WordPress site structure (pages, menus, plugins)
