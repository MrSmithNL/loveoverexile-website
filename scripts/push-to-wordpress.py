#!/usr/bin/env python3
"""
push-to-wordpress.py
Reads a Markdown file and pushes it to WordPress as a draft via the REST API.

Usage:
  python3 scripts/push-to-wordpress.py content/pages/privacy-policy.md
  python3 scripts/push-to-wordpress.py content/posts/what-is-parental-alienation.md

Each file must have YAML frontmatter at the top. Example:

---
title: "Privacy Policy"
type: page          # 'page' or 'post'
slug: privacy-policy
status: draft       # always draft — Malcolm publishes manually
wp_id:              # leave blank for new content; fill in after first push to update
---

Content goes here in Markdown...
"""

import sys
import os
import requests
import frontmatter
import markdown

# ── Load credentials from .env ───────────────────────────────────────────────

def load_env():
    env = {}
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, val = line.partition('=')
                env[key.strip()] = val.strip()
    return env

# ── Push to WordPress ─────────────────────────────────────────────────────────

def push(filepath):
    env = load_env()
    site_url   = env['WP_SITE_URL']
    username   = env['WP_USERNAME']
    app_password = env['WP_APP_PASSWORD']

    # Parse the file
    post = frontmatter.load(filepath)
    meta    = post.metadata
    content = post.content

    title   = meta.get('title', 'Untitled')
    type_   = meta.get('type', 'post')       # 'page' or 'post'
    slug    = meta.get('slug', '')
    status  = meta.get('status', 'draft')    # always draft
    wp_id   = meta.get('wp_id', None)        # existing WP ID (for updates)

    # Convert Markdown to HTML
    html = markdown.markdown(content, extensions=['extra', 'nl2br'])

    # Build payload
    payload = {
        'title':   title,
        'content': html,
        'status':  status,
    }
    if slug:
        payload['slug'] = slug

    # Determine endpoint
    endpoint = f"{site_url}/wp-json/wp/v2/{'pages' if type_ == 'page' else 'posts'}"
    auth = (username, app_password)

    # Create or update
    if wp_id:
        print(f"Updating existing {type_} (ID: {wp_id}): {title}")
        response = requests.post(f"{endpoint}/{wp_id}", json=payload, auth=auth)
    else:
        print(f"Creating new {type_}: {title}")
        response = requests.post(endpoint, json=payload, auth=auth)

    # Handle response
    if response.status_code in (200, 201):
        data = response.json()
        new_id   = data.get('id')
        edit_url = f"{site_url}/wp-admin/{'page' if type_ == 'page' else 'post'}.php?post={new_id}&action=edit"
        print(f"✅ Success! ID: {new_id}")
        print(f"   Review in wp-admin: {edit_url}")
        print(f"   Preview: {data.get('link', '')}")
        if not wp_id:
            print(f"\n   👉 Add this to your file's frontmatter so future pushes UPDATE instead of create:")
            print(f"   wp_id: {new_id}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        sys.exit(1)

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/push-to-wordpress.py <path-to-markdown-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)

    push(filepath)
