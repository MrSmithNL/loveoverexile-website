# Content Workflow — Love Over Exile

> How we write and publish content to WordPress.
> Last updated: 2026-02-27

---

## The Workflow (4 steps)

```
1. Write locally (Markdown file)  →  2. Claude reviews / revises
       ↓
3. Push to WordPress as DRAFT     →  4. Malcolm publishes from wp-admin
```

Content is always pushed as a **draft**. Malcolm reviews it in wp-admin and publishes when ready. Nothing goes live without Malcolm's approval.

---

## Folder Structure

```
content/
├── pages/          ← Website pages (About, Book, Privacy Policy, etc.)
│   └── privacy-policy.md
├── posts/          ← Blog articles and resources
└── source/         ← Original book files (read-only reference)
    ├── love-over-exile-book.docx
    ├── love-over-exile-book.txt
    ├── love-over-exile-book.pdf
    ├── part-2-extended.docx
    ├── part-2-extended.txt
    └── part-2-extended.pdf
```

---

## File Format

Every content file is a Markdown file (`.md`) with YAML frontmatter at the top:

```markdown
---
title: "Page or Article Title"
type: page          # 'page' for website pages, 'post' for blog articles
slug: url-slug-here
status: draft       # always 'draft' — Malcolm publishes manually
wp_id:              # leave blank for NEW content
                    # fill in the ID returned after first push (for future updates)
---

Content goes here in normal Markdown...

## Heading

Paragraph text. **Bold** and *italic* work. [Links](https://example.com) work.

- Bullet lists work
- Like this

1. Numbered lists too
2. Like this
```

---

## How to Push a File to WordPress

```bash
python3 scripts/push-to-wordpress.py content/pages/my-page.md
python3 scripts/push-to-wordpress.py content/posts/my-article.md
```

**First push (new content):** Creates a new draft in WordPress. The script prints the WordPress ID — add that as `wp_id:` in the file's frontmatter.

**Subsequent pushes (updates):** If `wp_id:` is set in the frontmatter, it updates the existing draft. Use this to revise content before publishing.

---

## Reviewing and Publishing (Malcolm's step)

After a push, the script prints a direct link to the draft in wp-admin:

```
✅ Success! ID: 42
   Review in wp-admin: https://loveoverexile.com/wp-admin/page.php?post=42&action=edit
   Preview: https://loveoverexile.com/?page_id=42
```

1. Open the wp-admin link
2. Review the content (Fusion Builder / block editor)
3. Make any formatting tweaks in Avada if needed
4. Click **Publish** when ready

---

## Content Already Drafted

| File | Type | WP ID | Status |
|------|------|-------|--------|
| `content/pages/privacy-policy.md` | Page | 3 | Draft in WordPress — ready to publish |

---

## Tips

- **Write in plain Markdown** — the script converts it to HTML automatically
- **Don't worry about formatting details** in the Markdown — Avada's styling handles the look
- **Keep the `wp_id` updated** — it's what tells the script whether to create or update
- **Never edit directly in wp-admin for pages managed here** — changes would be overwritten on the next push
