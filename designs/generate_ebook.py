#!/usr/bin/env python3
"""Generate the Love Over Exile Survival Guide PDF from markdown + CSS."""

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HERE = Path(__file__).parent
IMG_DIR = HERE.parent / "site" / "public" / "images"
DESIGN_IMG_DIR = HERE / "images"
CSS_PATH = HERE / "ebook.css"
MD_PATH = HERE / "ebook-text-3.md"
HTML_PATH = HERE / "ebook.html"
PDF_PATH = HERE / "survival-guide.pdf"

# ---------------------------------------------------------------------------
# Data Maps
# ---------------------------------------------------------------------------

# Font Awesome 6 Solid Unicode codepoints
FA_ICONS = {
    "health": "\uf21e",      # medkit
    "support": "\uf0c0",     # users
    "tactics": "\uf11b",     # gamepad
    "loving": "\uf004",      # heart
    "warning": "\uf071",     # triangle-exclamation
    "key": "\uf084",         # key
    "insight": "\uf0eb",     # lightbulb
    "shield": "\uf3ed",      # shield-alt
    "brain": "\uf5dc",       # brain
    "child": "\uf1ae",       # child
    "balance": "\uf24e",     # balance-scale
    "book": "\uf02d",        # book
    "quote": "\uf10d",       # quote-left
    "check": "\uf00c",       # check
    "star": "\uf005",        # star
    "arrow": "\uf061",       # arrow-right
}

# Watercolour illustrations placed alongside H2 headings
SECTION_IMAGES = {
    "The Wound You Are Carrying": "section-wound.jpg",
    "Your Body Is Keeping Score": "section-body.jpg",
    "The Map for Survival": "section-map.jpg",
    "Community and Support": "section-community.jpg",
}

# Diagram placeholder text → image file (None = no standalone image)
DIAGRAM_MAP = {
    "The Machine of Erasure Model": "alienating-parent-machine-of-erasure-model.png",
    "The Power and Control Wheel": None,
    "The Diagnostic Bridge": None,
    "The Parental Alienation Landscape": "parental-alienation-landscape.png",
    "The 2D Alienation Trauma Pain Model": "2d-alienation-trauma-pain-model.png",
    "The Alienated Child": "alienated-child-systemic-conditioning-model.png",
    "The Alienated Parent Sphere of Influence": "alienated-parent-sphere-of-influence.png",
    "The Alienated Parent Survival and Engagement Model": "alienated-parent-survival-and-engagement-model-love-over-exile.png",
}

# Decorative motif images — one per Part
CHAPTER_MOTIFS = {
    1: "chapter-motif-1.png",
    2: "chapter-motif-2.png",
    3: "chapter-motif-3.png",
    4: "chapter-motif-4.png",
    5: "chapter-motif-5.png",
    6: "chapter-motif-6.png",
}


# ---------------------------------------------------------------------------
# Inline Markdown Processing
# ---------------------------------------------------------------------------

def process_inline(text: str) -> str:
    """Convert inline markdown to HTML: bold, italic, links."""
    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic: *text* (single asterisks not part of **)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    # Links: [text](url)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


# ---------------------------------------------------------------------------
# Table Renderer
# ---------------------------------------------------------------------------

def render_table(rows: list) -> str:
    """Convert pipe-separated markdown table rows to an HTML <table>."""
    html = "<table>"
    for idx, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        if idx == 0:
            # Header row
            html += "<thead><tr>"
            for cell in cells:
                html += f"<th>{process_inline(cell)}</th>"
            html += "</tr></thead><tbody>"
        elif idx == 1 and all(c.strip().replace("-", "") == "" for c in cells):
            # Separator row — skip
            continue
        else:
            html += "<tr>"
            for cell in cells:
                html += f"<td>{process_inline(cell)}</td>"
            html += "</tr>"
    html += "</tbody></table>"
    return html


# ---------------------------------------------------------------------------
# Markdown → HTML Converter
# ---------------------------------------------------------------------------

def md_to_html(md_text: str) -> tuple[str, list]:
    """Convert markdown to HTML with ebook-specific structure.

    Returns (html_content, toc_entries) where toc_entries is a list of
    dicts with keys: type ('part' or 'chapter'), id, title.
    """
    lines = md_text.split("\n")
    html_parts: list[str] = []
    toc_entries: list[dict] = []
    in_list = False
    in_ordered_list = False
    in_table = False
    table_rows: list[str] = []
    in_blockquote = False
    blockquote_lines: list[str] = []
    current_part_num = 0
    chapter_counter = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # --- Diagram placeholders: *[DIAGRAM: Name] ---
        if line.startswith("*[DIAGRAM:"):
            desc = line.strip("*[]")
            for key, img_file in DIAGRAM_MAP.items():
                if key in desc and img_file:
                    img_path = IMG_DIR / img_file
                    html_parts.append(
                        f'<figure class="model-diagram">'
                        f'<img src="{img_path}" alt="{key}">'
                        f"</figure>"
                    )
                    break
            i += 1
            continue

        # --- Close open lists if the current line is not a list item ---
        if in_list and not line.startswith("- ") and line.strip() != "":
            html_parts.append("</ul>")
            in_list = False

        if in_ordered_list and not re.match(r"^\d+\.\s", line) and line.strip() != "":
            html_parts.append("</ol>")
            in_ordered_list = False

        # --- Table handling ---
        if line.startswith("|") and not in_table:
            in_table = True
            table_rows = [line]
            i += 1
            continue
        elif in_table and line.startswith("|"):
            table_rows.append(line)
            i += 1
            continue
        elif in_table and not line.startswith("|"):
            html_parts.append(render_table(table_rows))
            in_table = False
            table_rows = []
            # Fall through to process current line

        # --- Horizontal rule ---
        if line.strip() == "---":
            html_parts.append(
                '<div class="divider"><span class="ornament">\u2726</span></div>'
            )
            i += 1
            continue

        # --- Part headers: # PART N: TITLE ---
        m = re.match(r"^# (PART \d+: .+)$", line)
        if m:
            current_part_num += 1
            title = m.group(1)
            parts = title.split(": ", 1)
            part_label = parts[0]
            part_title = parts[1] if len(parts) > 1 else ""

            part_id = f"part-{current_part_num}"
            toc_entries.append({
                "type": "part",
                "id": part_id,
                "title": title,
            })

            # Chapter motif image
            motif_html = ""
            motif_file = CHAPTER_MOTIFS.get(current_part_num)
            if motif_file:
                motif_path = DESIGN_IMG_DIR / motif_file
                if motif_path.exists():
                    motif_html = (
                        f'<img class="chapter-motif" src="{motif_path}" alt="">'
                    )

            html_parts.append(
                f'<section class="chapter-opener" id="{part_id}">'
                f"{motif_html}"
                f'<div class="chapter-number">{part_label}</div>'
                f'<div class="chapter-rule"></div>'
                f'<div class="chapter-title">{part_title}</div>'
                f'<div class="chapter-part-bg">{current_part_num}</div>'
                f"</section>"
            )
            i += 1
            continue

        # --- H1 (non-part — book title, handled by cover) ---
        if line.startswith("# ") and not line.startswith("# PART"):
            chapter_counter += 1
            title = process_inline(line[2:])
            html_parts.append(f'<h1 id="ch-{chapter_counter}">{title}</h1>')
            toc_entries.append({
                "type": "chapter",
                "id": f"ch-{chapter_counter}",
                "title": re.sub(r"<[^>]+>", "", title),
            })
            i += 1
            continue

        # --- H2 ---
        if line.startswith("## "):
            chapter_counter += 1
            raw_title = line[3:].strip()
            title = process_inline(raw_title)
            chapter_id = f"ch-{chapter_counter}"
            plain_title = re.sub(r"<[^>]+>", "", title)

            toc_entries.append({
                "type": "chapter",
                "id": chapter_id,
                "title": plain_title,
            })

            # Check for section image
            section_img = SECTION_IMAGES.get(raw_title)
            if section_img:
                img_path = DESIGN_IMG_DIR / section_img
                if img_path.exists():
                    html_parts.append(
                        f'<div class="section-opener">'
                        f'<img src="{img_path}" alt="{plain_title}">'
                        f'<div class="text-content">'
                        f'<h2 id="{chapter_id}">{title}</h2>'
                        f"</div></div>"
                    )
                    i += 1
                    continue

            html_parts.append(f'<h2 id="{chapter_id}">{title}</h2>')
            i += 1
            continue

        # --- H3 ---
        if line.startswith("### "):
            chapter_counter += 1
            title = process_inline(line[4:].strip())
            html_parts.append(f'<h3 id="ch-{chapter_counter}">{title}</h3>')
            i += 1
            continue

        # --- Blockquote ---
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = process_inline(" ".join(quote_lines))
            if "\u2014" in quote_text:
                parts = quote_text.rsplit("\u2014", 1)
                html_parts.append(
                    f'<div class="pull-quote-enhanced">'
                    f"<p>{parts[0].strip()}</p>"
                    f"<cite>\u2014 {parts[1].strip()}</cite>"
                    f"</div>"
                )
            else:
                html_parts.append(
                    f'<blockquote><p>{quote_text}</p></blockquote>'
                )
            continue

        # --- Unordered list ---
        if line.startswith("- "):
            if not in_list:
                html_parts.append('<ul class="custom">')
                in_list = True
            content = process_inline(line[2:])
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # --- Ordered list: 1. item ---
        ol_match = re.match(r"^(\d+)\.\s+(.+)$", line)
        if ol_match and not re.match(r"^\*\*\d+\.", line):
            if not in_ordered_list:
                html_parts.append("<ol>")
                in_ordered_list = True
            content = process_inline(ol_match.group(2))
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # --- Numbered bold items: **1. Title** rest ---
        m = re.match(r"^\*\*(\d+)\.\s+(.+?)\*\*\s*(.*)$", line)
        if m:
            num = m.group(1)
            title = m.group(2)
            rest = process_inline(m.group(3))
            instead = ""
            if i + 1 < len(lines) and lines[i + 1].startswith("*Instead:"):
                instead_text = process_inline(
                    lines[i + 1].strip("*").replace("Instead: ", "")
                )
                instead = (
                    f'<br><span class="text-sage">'
                    f"<em>Instead: {instead_text}</em></span>"
                )
                i += 1
            html_parts.append(
                f'<div class="numbered-item avoid-break">'
                f'<div class="num">{num}</div>'
                f'<div class="content"><strong>{title}</strong>'
                f"<p>{rest}{instead}</p></div></div>"
            )
            i += 1
            continue

        # --- Bold label paragraph: **Label**\ndescription ---
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line)
        if m and i + 1 < len(lines) and lines[i + 1].strip():
            label = m.group(1)
            i += 1
            desc_lines = []
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith("**")
                and not lines[i].startswith("#")
                and not lines[i].startswith("> ")
                and not lines[i].startswith("- ")
                and not lines[i].startswith("*[")
            ):
                desc_lines.append(lines[i])
                i += 1
            desc = process_inline(" ".join(desc_lines))
            html_parts.append(f"<p><strong>{label}</strong><br>{desc}</p>")
            continue

        # --- Regular paragraph ---
        if line.strip():
            para_lines = [line]
            i += 1
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith("#")
                and not lines[i].startswith("> ")
                and not lines[i].startswith("- ")
                and not lines[i].startswith("**")
                and not lines[i].startswith("|")
                and not lines[i].startswith("*[")
                and not re.match(r"^\d+\.\s", lines[i])
            ):
                para_lines.append(lines[i])
                i += 1
            text = process_inline(" ".join(para_lines))
            html_parts.append(f"<p>{text}</p>")
            continue

        # --- Empty line — skip ---
        i += 1

    # Close any open containers
    if in_list:
        html_parts.append("</ul>")
    if in_ordered_list:
        html_parts.append("</ol>")
    if in_table:
        html_parts.append(render_table(table_rows))

    return "\n".join(html_parts), toc_entries


# ---------------------------------------------------------------------------
# Table of Contents Builder
# ---------------------------------------------------------------------------

def build_toc_html(toc_entries: list) -> str:
    """Build table of contents from toc_entries list."""
    items = []
    for entry in toc_entries:
        css_class = "toc-part" if entry["type"] == "part" else "toc-chapter"
        items.append(
            f'<li class="{css_class}">'
            f'<a href="#{entry["id"]}">{entry["title"]}</a>'
            f"</li>"
        )

    return (
        '<nav class="toc">\n'
        "  <h2>Contents</h2>\n"
        '  <ul class="toc-auto">\n'
        f'    {"".join(items)}\n'
        "  </ul>\n"
        "</nav>"
    )


# ---------------------------------------------------------------------------
# Post-Processing: All 69 Visual Injections
# ---------------------------------------------------------------------------

def post_process_html(html: str) -> str:
    """Apply ALL 69 visual injections via string search-and-replace."""
    I = FA_ICONS

    # ===================================================================
    # #1: KEY FACTS STRIP — After "The numbers are staggering:"
    # ===================================================================
    facts_strip = (
        '<div class="key-facts-strip">'
        '<div class="fact"><span class="fact-number">22M</span>'
        '<span class="fact-label">Affected Parents</span></div>'
        '<div class="fact"><span class="fact-number">13.4%</span>'
        '<span class="fact-label">Of All Parents</span></div>'
        '<div class="fact"><span class="fact-number">39.2%</span>'
        '<span class="fact-label">UK Separated</span></div>'
        '<div class="fact"><span class="fact-number">40%</span>'
        '<span class="fact-label">Research Since 2016</span></div>'
        "</div>"
    )
    html = html.replace(
        "<p>The numbers are staggering:</p>",
        "<p>The numbers are staggering:</p>" + facts_strip,
    )

    # ===================================================================
    # #2: HERO BAND — "It Is Not Conflict. It Is Abuse."
    # ===================================================================
    html = re.sub(
        r'<h2 id="(ch-\d+)">It Is Not Conflict\. It Is Abuse\.</h2>',
        r'<div class="hero-band hero-band-teal">'
        f'<h2 id="\\1" style="color:white;margin:0;">'
        f'{I["warning"]} It Is Not Conflict. It Is Abuse.</h2>'
        "</div>",
        html,
    )

    # ===================================================================
    # #3: ICON BLOCKS — Four Pillars of Support
    # ===================================================================
    support_icons = [
        (I["health"], "A PA-Aware Therapist",
         "Your emotional anchor \u2014 someone who specifically understands "
         "parental alienation and high-conflict separation."),
        (I["balance"], "A Specialist Family Lawyer",
         "Your strategic advisor \u2014 with specific experience in alienation "
         "cases and high-conflict litigation."),
        (I["support"], "One Trusted Friend",
         "Your reality check \u2014 the person who loves you, sees you, and "
         "keeps you grounded."),
        (I["loving"], "A Support Group",
         "Your community \u2014 people living the same reality who truly "
         "understand."),
    ]
    icon_blocks_html = ""
    for icon, title, desc in support_icons:
        icon_blocks_html += (
            f'<div class="icon-block">'
            f'<div class="icon-block-icon">{icon}</div>'
            f'<div class="icon-block-content">'
            f"<strong>{title}</strong>"
            f"<p>{desc}</p>"
            f"</div></div>"
        )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Four Pillars of Support</h3>)',
        r"\1" + icon_blocks_html,
        html,
    )

    # ===================================================================
    # #4: ACCENT CARD — Crisis Support
    # ===================================================================
    emergency_card = (
        f'<div class="accent-card accent-card-amber">'
        f'<div class="accent-card-icon">{I["warning"]}</div>'
        f'<div class="accent-card-content">'
        f"<h4>Crisis Support</h4>"
        f"<p><strong>UK:</strong> Samaritans \u2014 116 123<br>"
        f"<strong>US:</strong> 988 Suicide &amp; Crisis Lifeline \u2014 988<br>"
        f"<strong>International:</strong> befrienders.org</p>"
        f"</div></div>"
    )
    html = html.replace(
        "<p>Your child needs you alive. Everything else is secondary.</p>",
        emergency_card
        + "<p>Your child needs you alive. Everything else is secondary.</p>",
    )

    # ===================================================================
    # #5: ACCENT CARD — BIFF Method
    # ===================================================================
    biff_card = (
        f'<div class="accent-card accent-card-teal">'
        f'<div class="accent-card-icon">{I["shield"]}</div>'
        f'<div class="accent-card-content">'
        f"<h4>The BIFF Method</h4>"
        f"<p><strong>Brief</strong> \u2014 Say only what is necessary<br>"
        f"<strong>Informative</strong> \u2014 Factual, not emotional<br>"
        f"<strong>Friendly</strong> \u2014 Polite but not warm<br>"
        f"<strong>Firm</strong> \u2014 Clear boundaries</p>"
        f"</div></div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Communication: The BIFF Method</h3>)',
        r"\1" + biff_card,
        html,
    )

    # ===================================================================
    # #6: STEP INDICATOR — After "What This Guide Covers"
    # ===================================================================
    steps = [
        ("1", "Understand", "The Epidemic"),
        ("2", "Recognise", "The Signs"),
        ("3", "Name", "The Wounds"),
        ("4", "Survive", "The Framework"),
        ("5", "Endure", "The Road"),
        ("6", "Connect", "Your People"),
    ]
    steps_inner = ""
    for num, label, desc in steps:
        steps_inner += (
            f'<div class="step"><span class="step-number">{num}</span>'
            f'<span class="step-label">{label}</span><br>'
            f'<span class="step-desc">{desc}</span></div>'
        )
    steps_html = f'<div class="step-indicator">{steps_inner}</div>'
    html = re.sub(
        r'(<h2 id="ch-\d+">What This Guide Covers</h2>)',
        r"\1" + steps_html,
        html,
    )

    # ===================================================================
    # #7: CHECKLIST PANEL — After "Documentation"
    # ===================================================================
    checklist_items = [
        "Date, time, and location of every interaction",
        "Missed handovers and blocked communications",
        "Screenshots of messages (factual, no commentary)",
        "Witness names and contact details",
        "School reports, medical records, event attendance",
        "Financial records of legal costs",
    ]
    checklist_li = "".join(f"<li>{item}</li>" for item in checklist_items)
    checklist_html = (
        '<div class="checklist-panel">'
        f'<h4>{I["check"]} Documentation Checklist</h4>'
        f"<ul>{checklist_li}</ul>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Documentation</h3>)',
        r"\1" + checklist_html,
        html,
    )

    # ===================================================================
    # #8: COMPARISON PANEL — After "The Cognitive Diet"
    # ===================================================================
    comparison_html = (
        '<div class="comparison-panel">'
        '<div class="panel-do">'
        f'<h4>{I["check"]} Let In</h4>'
        "<p>Educational content about alienation. Supportive communities. "
        "Professional guidance. Content that builds hope and resilience.</p>"
        "</div>"
        '<div class="panel-dont">'
        f'<h4>{I["warning"]} Shut Out</h4>'
        "<p>Doom-scrolling. The alienator's social media. Toxic forums. "
        "Unsolicited advice. Constant review of case details.</p>"
        "</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Cognitive Diet</h3>)',
        r"\1" + comparison_html,
        html,
    )

    # ===================================================================
    # #9: HERO BAND — Inner Freedom
    # ===================================================================
    html = re.sub(
        r'<h2 id="(ch-\d+)">Inner Freedom</h2>',
        r'<div class="hero-band hero-band-teal">'
        r'<h2 id="\1" style="color:white;margin:0;">Inner Freedom</h2>'
        '<p style="color:rgba(255,255,255,0.9);margin-bottom:0;">'
        "The state of knowing who you are at a depth that no court, "
        "no allegation, and no rejection can touch.</p>"
        "</div>",
        html,
    )

    # ===================================================================
    # #10: ICON BLOCKS — Sphere of Influence
    # ===================================================================
    sphere_icons = [
        (I["shield"], "Circle 1: What You Control",
         "Your health, your mindset, your character, your documentation, "
         "your parenting quality."),
        (I["key"], "Circle 2: What You Can Influence",
         "Your legal strategy, your communication approach, your "
         "professional team, your public narrative."),
        (I["loving"], "Circle 3: What You Can Only Accept",
         "The court system, the alienating parent\u2019s behaviour, your "
         "child\u2019s current feelings, other people\u2019s opinions."),
    ]
    sphere_html = ""
    for icon, title, desc in sphere_icons:
        sphere_html += (
            f'<div class="icon-block">'
            f'<div class="icon-block-icon">{icon}</div>'
            f'<div class="icon-block-content">'
            f"<strong>{title}</strong>"
            f"<p>{desc}</p>"
            f"</div></div>"
        )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Sphere of Influence</h2>)',
        r"\1" + sphere_html,
        html,
    )

    # ===================================================================
    # #11: ACCENT CARD — Stockdale Paradox
    # ===================================================================
    stockdale_card = (
        f'<div class="accent-card accent-card-teal">'
        f'<div class="accent-card-icon">{I["insight"]}</div>'
        f'<div class="accent-card-content">'
        f"<h4>The Stockdale Paradox</h4>"
        f"<p>Unwavering faith that you will prevail, combined with "
        f"brutal realism about how long it may take.</p>"
        f"</div></div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Stockdale Paradox</h3>)',
        r"\1" + stockdale_card,
        html,
    )

    # ===================================================================
    # #12: HERO BAND — A Final Word
    # ===================================================================
    html = re.sub(
        r'<h2 id="(ch-\d+)">A Final Word</h2>',
        r'<div class="hero-band hero-band-teal">'
        r'<h2 id="\1" style="color:white;margin:0;">A Final Word</h2>'
        "</div>",
        html,
    )

    # ===================================================================
    # #13: PAGE SECTION COLOURED — About the Book
    # ===================================================================
    html = re.sub(
        r'<h2 id="(ch-\d+)">About the Book</h2>',
        r'<div class="page-section-coloured">'
        r'<h2 id="\1" style="margin-top:0;">About the Book</h2>'
        "</div>",
        html,
    )

    # ===================================================================
    # #14: DROP CAPS (first set)
    # ===================================================================
    drop_cap_sections_1 = [
        "What Is Parental Alienation?",
        "The Cast of Characters",
        "When Letting Go Keeps the Door Open",
    ]
    for section_title in drop_cap_sections_1:
        marker = f">{section_title}</h2>"
        pos = html.find(marker)
        if pos >= 0:
            p_pos = html.find("<p>", pos + len(marker))
            if p_pos >= 0:
                html = html[:p_pos] + '<p class="drop-cap">' + html[p_pos + 3:]

    # ===================================================================
    # #15: KEY TAKEAWAYS — Part 1
    # ===================================================================
    takeaways_p1 = (
        '<div class="key-takeaways">'
        f'<h4><span class="fa-icon">{I["key"]}</span> Key Takeaways</h4>'
        "<ol>"
        "<li>Parental alienation is a recognised pattern of psychological "
        "abuse \u2014 not a custody dispute.</li>"
        "<li>22 million parents in the US and Canada alone report being "
        "targeted.</li>"
        "<li>It maps directly onto the Duluth Power and Control Wheel for "
        "domestic violence.</li>"
        "<li>Each of the eight behavioural signs in the child is a direct "
        "consequence of a specific coercive control tactic.</li>"
        "<li>40% of all research has been published since 2016 \u2014 the "
        "science is young, but it is real.</li>"
        "</ol>"
        "</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-2">',
        takeaways_p1 + '<section class="chapter-opener" id="part-2">',
    )

    # ===================================================================
    # #16: ADMONITION — Legal Warning
    # ===================================================================
    legal_admonition = (
        f'<div class="admonition admonition-legal">'
        f'<div class="admonition-header">'
        f'<span class="admonition-icon">{I["balance"]}</span> Legal Note</div>'
        f"<p>This guide provides general information based on research and "
        f"lived experience. It is not legal, medical, or therapeutic advice. "
        f"Always consult qualified professionals for your specific "
        f"situation.</p>"
        f"</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The non-negotiables</h3>)',
        legal_admonition + r"\1",
        html,
    )

    # ===================================================================
    # #17: BEFORE/AFTER — Common Mistakes
    # ===================================================================
    before_after = (
        f'<div class="before-after">'
        f'<div class="before-box"><h4>{I["warning"]} Before</h4>'
        f'<p>"They badmouthed me, so I told the children exactly what '
        f"their mother did. I showed them the court documents. I wanted "
        f'them to know the truth."</p></div>'
        f'<div class="transition-arrow">{I["arrow"]}</div>'
        f'<div class="after-box"><h4>{I["check"]} After</h4>'
        f'<p>"I stopped trying to counter the narrative. I focused on '
        f"being calm, present, and consistent. I let my behaviour speak "
        f"for itself. The children will find the truth when they are "
        f'ready."</p></div>'
        f"</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 10 Most Common Mistakes</h2>)',
        r"\1" + before_after,
        html,
    )

    # ===================================================================
    # #18: DIALOGUE — BIFF Example
    # ===================================================================
    dialogue = (
        '<div class="dialogue">'
        '<div class="dialogue-msg dialogue-msg-left">'
        '<span class="speaker">Alienating parent</span>'
        "\"The children don't want to see you this weekend. They have "
        'plans. Stop forcing them."'
        "</div>"
        '<div class="dialogue-msg dialogue-msg-right">'
        '<span class="speaker">Your BIFF response</span>'
        '"Thank you for letting me know. I will be at the agreed location '
        "at the agreed time, as per the court order. I look forward to "
        'seeing them."'
        "</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Universal Agreement</h3>)',
        dialogue + r"\1",
        html,
    )

    # ===================================================================
    # #19: EVIDENCE LOG — Before "Parallel Parenting"
    # ===================================================================
    evidence_fields = [
        ("Date:", "evidence-log-field"),
        ("Time:", "evidence-log-field"),
        ("Location:", "evidence-log-field"),
        ("Witnesses:", "evidence-log-field"),
        ("Incident:", "evidence-log-field-large"),
        ("Evidence:", "evidence-log-field-large"),
    ]
    evidence_rows = ""
    for label, cls in evidence_fields:
        evidence_rows += (
            f'<div class="evidence-log-row">'
            f'<span class="evidence-log-label">{label}</span>'
            f'<span class="{cls}"></span>'
            f"</div>"
        )
    evidence_log = (
        '<div class="evidence-log">'
        f'<h4>{I["book"]} Incident Record Template</h4>'
        f"{evidence_rows}"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Parallel Parenting</h3>)',
        evidence_log + r"\1",
        html,
    )

    # ===================================================================
    # #20: ANNOTATION STRIPE — Before "Self-Compassion Is Not Optional"
    # ===================================================================
    annotation = (
        '<div class="annotation-stripe">'
        "Remember: Your child needs you alive, healthy, and whole"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        annotation + r"\1",
        html,
    )

    # ===================================================================
    # #21: KEY TAKEAWAYS — Part 4
    # ===================================================================
    takeaways_p4 = (
        '<div class="key-takeaways">'
        f'<h4><span class="fa-icon">{I["key"]}</span> Key Takeaways</h4>'
        "<ol>"
        "<li>Stabilise yourself first \u2014 sleep, movement, nutrition, "
        "and professional support are non-negotiable.</li>"
        "<li>Build four pillars: PA-aware therapist, specialist lawyer, "
        "one trusted friend, and a support group.</li>"
        "<li>Focus energy on what you control. Accept what you cannot "
        "change.</li>"
        "<li>Use BIFF communication: Brief, Informative, Friendly, "
        "Firm.</li>"
        "<li>Document everything. Facts, not feelings.</li>"
        "</ol>"
        "</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-5">',
        takeaways_p4 + '<section class="chapter-opener" id="part-5">',
    )

    # ===================================================================
    # #22: ADMONITION — Hope/Tip
    # ===================================================================
    hope_admonition = (
        f'<div class="admonition admonition-tip">'
        f'<div class="admonition-header">'
        f'<span class="admonition-icon">{I["star"]}</span> '
        f"There Is Hope</div>"
        f"<p>69\u201381% of general estrangements are not permanent "
        f"(Pillemer, 2020). Many alienated children reconnect as adults. "
        f"Your consistency today is building the foundation for reunion "
        f"tomorrow.</p>"
        f"</div>"
    )
    html = html.replace(
        "<p><strong>69-81% of general estrangements are not permanent"
        "</strong>",
        hope_admonition
        + "<p><strong>69-81% of general estrangements are not permanent"
        "</strong>",
    )

    # ===================================================================
    # #23: ORNAMENTAL DIVIDERS — Replace .divider spans globally
    # ===================================================================
    divider_pattern = (
        '<div class="divider"><span class="ornament">\u2726</span></div>'
    )
    ornamental_set = [
        '<div class="ornamental-divider">'
        '<span class="ornament">\u2766 \u2767</span></div>',
        '<div class="ornamental-divider">'
        '<span class="ornament">\u2053</span></div>',
        '<div class="ornamental-divider">'
        '<span class="ornament">\u2726 \u2726 \u2726</span></div>',
    ]
    divider_count = 0
    while divider_pattern in html:
        divider_count += 1
        if divider_count % 3 == 0:
            replacement = ornamental_set[
                (divider_count // 3 - 1) % len(ornamental_set)
            ]
            html = html.replace(divider_pattern, replacement, 1)
        else:
            html = html.replace(
                divider_pattern, '<div class="divider-fade"></div>', 1
            )

    # ===================================================================
    # #24: SIDEBAR CALLOUT — After "What Is Parental Alienation?"
    # ===================================================================
    sidebar_callout = (
        '<div class="sidebar-callout">'
        f'<div class="sidebar-callout-title">{I["insight"]} Key Insight'
        "</div>"
        "<p>Research shows that children who maintain a relationship with "
        "both parents after separation have significantly better outcomes "
        "across all measures of wellbeing.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">What Is Parental Alienation\?</h2>)',
        r"\1" + sidebar_callout,
        html,
    )

    # ===================================================================
    # #25: BAR CHART — Research statistics
    # ===================================================================
    bar_chart = (
        '<div class="bar-chart">'
        '<div class="bar-chart-title">Research Growth in Parental '
        "Alienation</div>"
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Since 2016</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill" '
        'style="width:40%">'
        '<span class="bar-chart-value">40%</span></div></div></div>'
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Since 2010</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill" '
        'style="width:65%">'
        '<span class="bar-chart-value">65%</span></div></div></div>'
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Total Studies</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill '
        'bar-chart-fill-gold" style="width:100%">'
        '<span class="bar-chart-value">1,200+</span>'
        "</div></div></div>"
        "</div>"
    )
    html = html.replace(
        "<p><strong>40% of all parental alienation research has been "
        "published since 2016</strong>",
        bar_chart
        + "<p><strong>40% of all parental alienation research has been "
        "published since 2016</strong>",
    )

    # ===================================================================
    # #26: INSET PULL QUOTE — After "The Map for Survival"
    # ===================================================================
    inset_quote = (
        '<div class="inset-pull-quote">'
        "<p>Your child needs a parent who is alive, healthy, and whole. "
        "Everything else is secondary.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Map for Survival</h2>)',
        r"\1" + inset_quote,
        html,
    )

    # ===================================================================
    # #27: RIBBON BANNER — "The Four Pillars of Support"
    # ===================================================================
    html = re.sub(
        r'(<h3 id="ch-\d+">The Four Pillars of Support</h3>)',
        r'<div class="ribbon-banner">\1</div>',
        html,
    )

    # ===================================================================
    # #28: VERTICAL TIMELINE — After "The Wound You Are Carrying"
    # ===================================================================
    timeline_stages = [
        ("Stage 1: Crisis",
         "Shock, grief, disbelief. The world has changed overnight.", ""),
        ("Stage 2: Stabilisation",
         "Building your team. Finding your footing. Establishing routines.",
         ""),
        ("Stage 3: Strategic Action",
         "Documentation, legal strategy, communication discipline.",
         " timeline-item-active"),
        ("Stage 4: Endurance",
         "The long road. Maintaining hope while accepting reality.", ""),
        ("Stage 5: Inner Freedom",
         "Knowing who you are at a depth no court can touch.", ""),
    ]
    timeline_inner = ""
    for title, desc, cls in timeline_stages:
        timeline_inner += (
            f'<div class="timeline-item{cls}">'
            f'<div class="timeline-item-title">{title}</div>'
            f"<p>{desc}</p></div>"
        )
    timeline = f'<div class="vertical-timeline">{timeline_inner}</div>'
    html = re.sub(
        r'(<h2 id="ch-\d+">The Wound You Are Carrying</h2>)',
        r"\1" + timeline,
        html,
    )

    # ===================================================================
    # #29: CORNER FRAME — Wrap first .key-takeaways
    # ===================================================================
    html = html.replace(
        '<div class="key-takeaways">',
        '<div class="corner-frame"><div class="key-takeaways">',
        1,  # Only first instance
    )
    kt_start = html.find('<div class="corner-frame"><div class="key-takeaways">')
    if kt_start >= 0:
        search_from = kt_start + len('<div class="corner-frame">')
        depth = 1
        pos = search_from
        while depth > 0 and pos < len(html):
            next_open = html.find("<div", pos + 1)
            next_close = html.find("</div>", pos + 1)
            if next_close < 0:
                break
            if next_open >= 0 and next_open < next_close:
                depth += 1
                pos = next_open
            else:
                depth -= 1
                pos = next_close
        if depth == 0:
            html = html[: pos + 6] + "</div>" + html[pos + 6:]

    # ===================================================================
    # #30: DID YOU KNOW — Children Vulnerable
    # ===================================================================
    did_you_know = (
        '<div class="did-you-know pattern-dots">'
        f'<div class="did-you-know-label">{I["brain"]} Did You Know?</div>'
        "<p>Children who are alienated from a parent show measurable "
        "changes in brain development, particularly in areas governing "
        "attachment, trust, and emotional regulation. The effects mirror "
        "those seen in other forms of psychological abuse.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Why Children Are Vulnerable</h2>)',
        r"\1" + did_you_know,
        html,
    )

    # ===================================================================
    # #31: SECTION WASHES (Teal)
    # ===================================================================
    wash_sections = [
        "The Cast of Characters",
        "The Map for Survival",
        "Self-Compassion Is Not Optional",
    ]
    for section_title in wash_sections:
        marker = f">{section_title}</h2>"
        pos = html.find(marker)
        if pos >= 0:
            h2_start = html.rfind("<h2", 0, pos)
            if h2_start < 0:
                h2_start = html.rfind("<div", 0, pos)
            if h2_start >= 0:
                html = (
                    html[:h2_start]
                    + '<div class="section-wash-teal">'
                    + html[h2_start:]
                )
                # Close after 3rd </p> following the marker
                close_pos = pos + len(marker)
                for _ in range(3):
                    next_p = html.find("</p>", close_pos + 1)
                    if next_p >= 0:
                        close_pos = next_p
                if close_pos > pos:
                    html = (
                        html[: close_pos + 4] + "</div>" + html[close_pos + 4:]
                    )

    # ===================================================================
    # #32: CONTENT WARNING — Before part-3
    # ===================================================================
    content_warning = (
        f'<div class="content-warning">'
        f'<div class="content-warning-header">{I["warning"]} Content Note'
        f"</div>"
        f"<p>This section discusses the psychological impact of parental "
        f"alienation, including trauma, grief, and suicidal ideation. If "
        f"you are in distress, please reach out to a crisis service (see "
        f"Part 6) before continuing.</p>"
        f"</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-3">',
        content_warning + '<section class="chapter-opener" id="part-3">',
    )

    # ===================================================================
    # #33: MYTH VS REALITY TABLE — After "What the Data Shows"
    # ===================================================================
    myth_rows = [
        ("\u201CThe child just needs time to adjust\u201D",
         "Without intervention, alienation typically worsens over time, "
         "not improves"),
        ("\u201CBoth parents are equally to blame\u201D",
         "Alienation is a pattern of coercive control by one parent "
         "against the other"),
        ("\u201CIf the child says it, it must be true\u201D",
         "Children repeat coached narratives they believe are their own "
         "thoughts"),
        ("\u201CA good parent would just move on\u201D",
         "Refusing to abandon your child is an act of love, not "
         "obsession"),
        ("\u201CCourts always get it right\u201D",
         "Most family courts lack training to identify alienation "
         "dynamics"),
    ]
    myth_inner = (
        '<div class="myth-row">'
        '<div class="myth-header">Myth</div>'
        '<div class="reality-header">Reality</div></div>'
    )
    for myth, reality in myth_rows:
        myth_inner += (
            '<div class="myth-row">'
            f'<div class="myth-cell">{myth}</div>'
            f'<div class="reality-cell">{reality}</div></div>'
        )
    myth_reality = f'<div class="myth-reality">{myth_inner}</div>'
    html = re.sub(
        r'(<h2 id="ch-\d+">What the Data Shows</h2>)',
        r"\1" + myth_reality,
        html,
    )

    # ===================================================================
    # #34: SELF-ASSESSMENT — Before "When all five factors align..."
    # ===================================================================
    assessment_items = [
        "Your child refuses or resists contact with you",
        "You previously had a positive, loving relationship with your "
        "child",
        "There is no history of abuse or neglect on your part",
        "The other parent has engaged in behaviours that undermine your "
        "relationship",
        "Your child shows signs: campaign of denigration, weak reasons, "
        "lack of remorse, \u201Cindependent thinker\u201D claim",
    ]
    assessment_inner = ""
    for item in assessment_items:
        assessment_inner += (
            '<div class="self-assessment-item">'
            '<div class="self-assessment-check"></div>'
            f"<div>{item}</div></div>"
        )
    self_assessment = (
        '<div class="self-assessment">'
        f'<div class="self-assessment-header">{I["check"]} '
        f"Self-Assessment: Is This Alienation?</div>"
        f"{assessment_inner}"
        '<div class="self-assessment-note">If all five factors are '
        "present, you are likely dealing with parental alienation. Seek "
        "a PA-aware professional for assessment.</div>"
        "</div>"
    )
    html = html.replace(
        "<p>When all five factors align, you are not looking at a child "
        "who has made a free choice.",
        self_assessment
        + "<p>When all five factors align, you are not looking at a child "
        "who has made a free choice.",
    )

    # ===================================================================
    # #35: BREATHING PAUSE — Before "The Eight Amplification Factors"
    # ===================================================================
    breathing_pause = (
        '<div class="breathing-pause">'
        f'<div class="breathing-pause-title">{I["loving"]} '
        f"Pause Here If You Need To</div>"
        '<div class="breathing-steps">'
        "<strong>Breathe in</strong> for 4 counts. "
        "<strong>Hold</strong> for 4 counts. "
        "<strong>Breathe out</strong> for 6 counts.<br>"
        "Repeat three times. You are safe right now."
        "</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Eight Amplification Factors</h3>)',
        breathing_pause + r"\1",
        html,
    )

    # ===================================================================
    # #36: NORMALISATION — Before "Understanding ambiguous loss..."
    # ===================================================================
    normalisation = (
        '<div class="normalisation">'
        "<p><strong>It is completely normal</strong> to feel like you are "
        "going mad. The confusion, the obsessive thinking, the inability "
        'to "move on" \u2014 these are not signs of weakness. They are '
        "the documented consequences of a loss the human brain was never "
        "designed to process.</p>"
        "</div>"
    )
    html = html.replace(
        "<p>Understanding ambiguous loss and disenfranchised grief is not "
        "academic.",
        normalisation
        + "<p>Understanding ambiguous loss and disenfranchised grief is "
        "not academic.",
    )

    # ===================================================================
    # #37: HIGHLIGHT BAR — PTSD
    # ===================================================================
    highlight_ptsd = (
        '<div class="highlight-bar">'
        f"<p>{I['warning']} Up to 50% of targeted parents meet clinical "
        f"criteria for PTSD. You are not overreacting. You are "
        f"appropriately responding to an impossible situation.</p>"
        "</div>"
    )
    html = html.replace(
        "<p><strong>Up to 50% of targeted parents</strong>",
        highlight_ptsd
        + "<p><strong>Up to 50% of targeted parents</strong>",
    )

    # ===================================================================
    # #38: TESTIMONY CARD — Unopened Cards
    # ===================================================================
    testimony = (
        '<div class="testimony-card">'
        '<div class="testimony-text">"I found the box of birthday cards '
        "my dad had sent every year. Dozens of them, unopened. That was "
        "the moment I realised everything I had been told was a lie. He "
        'never stopped loving me."</div>'
        '<div class="testimony-attribution">\u2014 Adult survivor of '
        "childhood alienation (composite, based on Dr. Amy Baker\u2019s "
        "research)</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">What alienated children remember</h3>)',
        r"\1" + testimony,
        html,
    )

    # ===================================================================
    # #39: SCENARIO CARD — School Event
    # ===================================================================
    scenario = (
        '<div class="scenario-card">'
        '<div class="scenario-header">Scenario: The School Event</div>'
        '<div class="scenario-body">'
        '<div class="scenario-situation">'
        "Your child\u2019s school play is next week. The alienating "
        "parent has told the school you are \u201Cnot welcome.\u201D "
        "Your child has not mentioned it to you."
        "</div>"
        '<div class="scenario-response">'
        "<strong>Response:</strong> Contact the school directly (you "
        "have parental rights to attend). Arrive calmly, sit where your "
        "child can see you. Do not approach the alienating parent. Take "
        "photos for your records. If your child acknowledges you, "
        "respond warmly but without pressure. If they don\u2019t, that "
        "is okay too. Your presence is the message."
        "</div></div></div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Staying Connected</h3>)',
        scenario + r"\1",
        html,
    )

    # ===================================================================
    # #40: COPING CARD — 5-4-3-2-1 Grounding
    # ===================================================================
    coping_card = (
        '<div class="coping-card">'
        f'<div class="coping-card-header">{I["shield"]} Grounding '
        f"Technique: The 5-4-3-2-1 Method</div>"
        "<p>When panic or emotional flooding hits, use your senses to "
        "anchor yourself:</p>"
        "<ol>"
        "<li><strong>5 things</strong> you can see</li>"
        "<li><strong>4 things</strong> you can touch</li>"
        "<li><strong>3 things</strong> you can hear</li>"
        "<li><strong>2 things</strong> you can smell</li>"
        "<li><strong>1 thing</strong> you can taste</li>"
        "</ol>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">When to seek emergency help</h3>)',
        coping_card + r"\1",
        html,
    )

    # ===================================================================
    # #41: TRY THIS — Self-Compassion Letter
    # ===================================================================
    try_this_compassion = (
        '<div class="try-this">'
        f'<div class="try-this-header">{I["star"]} Try This: The '
        f"Self-Compassion Letter</div>"
        "<p>Write a letter to yourself from the perspective of a loving, "
        "wise friend who knows everything you have been through. What "
        "would they say? How would they describe your strength? Let "
        "their words replace the harsh inner critic.</p>"
        '<div class="writing-lines">'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        "</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        r"\1" + try_this_compassion,
        html,
    )

    # ===================================================================
    # #42: TRY THIS — Sphere Circles
    # ===================================================================
    try_this_sphere = (
        '<div class="try-this">'
        f'<div class="try-this-header">{I["key"]} Try This: Map Your '
        f"Circles</div>"
        "<p>Take a piece of paper and draw three concentric circles. "
        "Write in each:</p>"
        "<p><strong>Inner circle:</strong> What you control right now "
        "(list 3 things)<br>"
        "<strong>Middle circle:</strong> What you can influence "
        "(list 2 things)<br>"
        "<strong>Outer circle:</strong> What you must accept "
        "(list 1 thing)</p>"
        "<p>Commit to spending 80% of your energy on the inner circle "
        "this week.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Circle 3: What You Can Only Accept</h3>)',
        try_this_sphere + r"\1",
        html,
    )

    # ===================================================================
    # #43: AFFIRMATION CARD — Before "69-81%..." paragraph
    # ===================================================================
    affirmation = (
        '<div class="affirmation-card">'
        '<span class="affirmation-label">Remember</span>'
        "<p>Your consistency today is building the foundation for "
        "reunion tomorrow. Every birthday card sent, every calm response "
        "given, every moment of restraint is a seed planted in your "
        "child\u2019s future memory.</p>"
        "</div>"
    )
    html = html.replace(
        "<p><strong>69-81% of general estrangements are not permanent"
        "</strong>",
        affirmation
        + "<p><strong>69-81% of general estrangements are not permanent"
        "</strong>",
    )

    # ===================================================================
    # #44: REFLECTION PROMPTS (3 locations)
    # ===================================================================
    reflection_parts = {
        "part-2": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} '
            f"Reflect</div>"
            "<p>Which of the 17 strategies have you observed in your own "
            "situation? How does naming them change how you feel about "
            "what is happening?</p>"
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            "</div></div>"
        ),
        "part-3": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} '
            f"Reflect</div>"
            "<p>Of the four wound levels, which feels most present for "
            "you right now? What would you say to a friend carrying the "
            "same wound?</p>"
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            "</div></div>"
        ),
        "part-5": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} '
            f"Reflect</div>"
            '<p>What does "inner freedom" mean to you? Where do you find '
            "your sense of self when every external source of validation "
            "has been stripped away?</p>"
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            "</div></div>"
        ),
    }
    for part_id, reflection_html in reflection_parts.items():
        html = html.replace(
            f'<section class="chapter-opener" id="{part_id}">',
            reflection_html
            + f'<section class="chapter-opener" id="{part_id}">',
        )

    # ===================================================================
    # #45: SECTION SUMMARY — Before part-5
    # ===================================================================
    summary_items = [
        "Stabilise yourself first: sleep, movement, nutrition, "
        "professional support",
        "Build four pillars: PA-aware therapist, specialist lawyer, "
        "trusted friend, support group",
        "Focus energy on what you control; influence what you can; "
        "accept the rest",
        "Communicate using BIFF: Brief, Informative, Friendly, Firm",
        "Document everything with facts, not emotions",
        "Love unconditionally \u2014 your consistency is the path to "
        "reconnection",
    ]
    summary_li = "".join(f"<li>{item}</li>" for item in summary_items)
    summary_p4 = (
        '<div class="section-summary">'
        f'<div class="section-summary-label">{I["check"]} Section '
        f"Summary</div>"
        f"<ul>{summary_li}</ul>"
        "</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-5">',
        summary_p4 + '<section class="chapter-opener" id="part-5">',
    )

    # ===================================================================
    # #46: HIGHLIGHT BAR — Stockdale Principle
    # ===================================================================
    highlight_stockdale = (
        '<div class="highlight-bar">'
        f"<p>{I['star']} Unwavering faith that you will prevail \u2014 "
        f"combined with brutal realism about how long it may take.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The Stockdale Paradox</h3>)',
        r"\1" + highlight_stockdale,
        html,
    )

    # ===================================================================
    # #47: BREATHING PAUSE — Stillness
    # ===================================================================
    breathing_inner = (
        '<div class="breathing-pause">'
        f'<div class="breathing-pause-title">{I["loving"]} A Moment of '
        f"Stillness</div>"
        '<div class="breathing-steps">'
        "Close your eyes. Place one hand on your heart.<br>"
        '<strong>Say to yourself:</strong> "I am more than this '
        "situation. I am more than what any court or accusation says "
        'about me."<br>'
        "Breathe. Feel the truth of those words."
        "</div>"
        "</div>"
    )
    html = html.replace(
        "<p>This is not religious instruction.",
        breathing_inner + "<p>This is not religious instruction.",
    )

    # ===================================================================
    # #48: END MARKS — After "Love over exile" and "A Final Word"
    # ===================================================================
    end_mark = '<div class="end-mark">\u25C6 \u25C6 \u25C6</div>'
    end_mark_sections = ["Love over exile", "A Final Word"]
    for section_title in end_mark_sections:
        # Try H3 first, then H2
        for tag in ["h3", "h2"]:
            pattern = re.compile(
                rf'<{tag} id="ch-\d+">{re.escape(section_title)}</{tag}>'
            )
            match = pattern.search(html)
            if match:
                pos = match.end()
                # Find next heading or section boundary
                next_h2 = html.find("<h2", pos)
                next_h3 = html.find("<h3", pos)
                next_section = html.find("<section", pos)
                next_divider = html.find('<div class="divider', pos)
                candidates = [
                    x
                    for x in [next_h2, next_h3, next_section, next_divider]
                    if x > 0
                ]
                if candidates:
                    insert_pos = min(candidates)
                    html = (
                        html[:insert_pos] + end_mark + html[insert_pos:]
                    )
                break

    # ===================================================================
    # #49: DID YOU KNOW — 17 Strategies
    # ===================================================================
    did_you_know_2 = (
        '<div class="did-you-know pattern-dots">'
        f'<div class="did-you-know-label">{I["brain"]} Did You Know?'
        "</div>"
        "<p>Dr. Amy Baker identified <strong>17 distinct strategies"
        "</strong> that alienating parents use. These map directly onto "
        "the Duluth Model\u2019s Power and Control Wheel \u2014 the "
        "same framework used to understand domestic violence.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 17 Strategies of Erasure</h2>)',
        r"\1" + did_you_know_2,
        html,
    )

    # ===================================================================
    # #50: TESTIMONY CARD — Reunion
    # ===================================================================
    testimony_2 = (
        '<div class="testimony-card">'
        '<div class="testimony-text">"After seven years of silence, my '
        "daughter called. She said: \u2018I always knew you loved me, "
        "Dad. I just couldn\u2019t say it.\u2019 Those seven years of "
        "birthday cards and unanswered messages \u2014 they all "
        'mattered."</div>'
        '<div class="testimony-attribution">\u2014 Anonymous alienated '
        "father, reunited after 7 years</div>"
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">Love over exile</h3>)',
        r"\1" + testimony_2,
        html,
    )

    # ===================================================================
    # #51: EPIGRAPHS (2 locations)
    # ===================================================================
    # Before H2 id="ch-1": Amy Baker quote
    epigraph_baker = (
        '<div class="epigraph">'
        '<p>"\u200BThe truth, while suppressed, is rarely destroyed '
        'completely."</p>'
        "<cite>Dr. Amy Baker</cite>"
        "</div>"
    )
    html = html.replace(
        '<h2 id="ch-1">',
        epigraph_baker + '<h2 id="ch-1">',
    )

    # After Part 5 opener: Viktor Frankl quote
    epigraph_frankl = (
        '<div class="epigraph">'
        '<p>"Everything can be taken from a person but one thing: the '
        "last of the human freedoms \u2014 to choose one\u2019s "
        'attitude in any given set of circumstances."</p>'
        "<cite>Viktor Frankl</cite>"
        "</div>"
    )
    p5_close = html.find("</section>", html.find('id="part-5"'))
    if p5_close >= 0:
        p5_close += len("</section>")
        next_h2_p5 = html.find("<h2", p5_close)
        if next_h2_p5 >= 0:
            html = html[:next_h2_p5] + epigraph_frankl + html[next_h2_p5:]

    # ===================================================================
    # #52: ADDITIONAL DROP CAPS
    # ===================================================================
    additional_drop_caps = [
        "The Wound You Are Carrying",
        "Ambiguous Loss and Disenfranchised Grief",
        "Inner Freedom",
        "Community and Support",
        "The Sleeper Effect",
        "The Map for Survival",
    ]
    for section_title in additional_drop_caps:
        marker = f">{section_title}</h2>"
        pos = html.find(marker)
        if pos >= 0:
            p_pos = html.find("<p>", pos + len(marker))
            if p_pos >= 0 and html[p_pos: p_pos + 20] != '<p class="drop-cap">':
                html = (
                    html[:p_pos] + '<p class="drop-cap">' + html[p_pos + 3:]
                )

    # ===================================================================
    # #53: NORMALISATION — Body Trauma
    # ===================================================================
    normalisation_body = (
        '<div class="normalisation">'
        "<p><strong>Your trauma responses are not character flaws."
        "</strong> The hypervigilance, the intrusive thoughts, the "
        "emotional flashbacks \u2014 these are injury symptoms. They are "
        "your nervous system doing exactly what it was designed to "
        "do.</p>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Your Body Is Keeping Score</h2>)',
        r"\1" + normalisation_body,
        html,
    )

    # ===================================================================
    # #54: HIGHLIGHT BAR — Unconditional Love
    # ===================================================================
    highlight_love = (
        '<div class="highlight-bar">'
        f"<p>{I['loving']} Consistent, unconditional love is the "
        f"strongest predictor of eventual reconnection. It is the most "
        f"active, disciplined, and courageous choice available to "
        f"you.</p>"
        "</div>"
    )
    html = html.replace(
        "<p>Consistent, unconditional love is the strongest predictor "
        "of eventual reconnection.",
        highlight_love,
    )

    # ===================================================================
    # #55: STAT PAGE — 22M
    # ===================================================================
    stat_page_22m = (
        '<div class="stat-page">'
        '<div class="stat-number">22M</div>'
        '<div class="stat-label">Parents Affected by Alienation</div>'
        '<div class="stat-desc">An estimated 22 million adults in the '
        "US alone have experienced parental alienation \u2014 roughly "
        "one in six parents. Yet most have never heard the term.</div>"
        '<div class="stat-source">Harman, Kruk &amp; Hines, 2018</div>'
        "</div>"
    )
    # Insert before the "It Is Not Conflict" hero band
    conflict_marker = "It Is Not Conflict. It Is Abuse.</h2>"
    conflict_pos = html.find(conflict_marker)
    if conflict_pos >= 0:
        band_start = html.rfind('<div class="hero-band', 0, conflict_pos)
        if band_start < 0:
            band_start = html.rfind("<h2", 0, conflict_pos)
        if band_start >= 0:
            html = html[:band_start] + stat_page_22m + html[band_start:]

    # ===================================================================
    # #56: PHOTO OVERLAY — Before Part 3
    # ===================================================================
    photo_page_1 = (
        '<div class="photo-page">'
        f'<img src="{IMG_DIR / "surviving-parental-alienation.jpg"}" '
        f'alt="">'
        '<div class="photo-overlay"></div>'
        '<div class="photo-content">'
        '<div class="photo-label">Part 3</div>'
        '<div class="photo-title">The Impact<br>on You</div>'
        '<div class="photo-text">What this experience does to your mind, '
        "body, identity, and spirit. Naming the wound is the first step "
        "to surviving it.</div>"
        "</div></div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-3">',
        photo_page_1 + '<section class="chapter-opener" id="part-3">',
    )

    # ===================================================================
    # #57: ICON GRID — Four Pillars overview
    # ===================================================================
    icon_grid_pillars = (
        '<div class="icon-grid">'
        f'<div class="icon-grid-item"><span class="grid-icon">'
        f'{I["health"]}</span>'
        '<div class="grid-title">Your Health</div>'
        '<div class="grid-desc">Protect your mental and physical '
        "wellbeing first</div></div>"
        f'<div class="icon-grid-item"><span class="grid-icon">'
        f'{I["support"]}</span>'
        '<div class="grid-title">Your Team</div>'
        '<div class="grid-desc">Build a support network that '
        "understands</div></div>"
        f'<div class="icon-grid-item"><span class="grid-icon">'
        f'{I["tactics"]}</span>'
        '<div class="grid-title">Your Tactics</div>'
        '<div class="grid-desc">Evidence-based strategies for the '
        "long haul</div></div>"
        f'<div class="icon-grid-item"><span class="grid-icon">'
        f'{I["loving"]}</span>'
        '<div class="grid-title">Your Love</div>'
        '<div class="grid-desc">A new way of loving that endures '
        "distance</div></div>"
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Pillar 1: Your Health and Safety</h2>)',
        icon_grid_pillars + r"\1",
        html,
    )

    # ===================================================================
    # #58: SPLIT LAYOUT — Common Mistakes
    # ===================================================================
    feature_items = [
        ("01", "Badmouthing the other parent",
         "Even when provoked \u2014 it gives the alienator ammunition"),
        ("02", "Trying to force contact",
         "Pressure pushes the child further away"),
        ("03", "Giving up too soon",
         "Withdrawal is interpreted as proof you never cared"),
        ("04", "Relying on the court alone",
         "Legal systems were not designed for this kind of abuse"),
        ("05", "Isolating yourself",
         "Silence and shame are the alienator\u2019s greatest allies"),
    ]
    feature_inner = ""
    for num, title, desc in feature_items:
        feature_inner += (
            f'<div class="feature-item"><div class="feature-num">{num}'
            f"</div>"
            f'<div class="feature-text"><strong>{title}</strong>'
            f"<p>{desc}</p></div></div>"
        )
    split_mistakes = (
        '<div class="split-layout">'
        '<div class="split-sidebar">'
        '<div class="split-label">Warning</div>'
        '<div class="split-sidebar-title">The 10 Mistakes That Make It '
        "Worse</div>"
        '<div class="split-sidebar-text">Even loving parents can '
        "unknowingly sabotage their own case. These are the most common "
        "patterns \u2014 and how to avoid them.</div>"
        "</div>"
        '<div class="split-main">'
        f'<div class="feature-list">{feature_inner}</div>'
        "</div></div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 10 Most Common Mistakes</h2>)',
        split_mistakes + r"\1",
        html,
    )

    # ===================================================================
    # #59: QUOTE PAGE — Viktor Frankl
    # ===================================================================
    quote_page = (
        '<div class="quote-page">'
        '<div class="quote-mark">\u201C</div>'
        '<div class="quote-text">Everything can be taken from a person '
        "but one thing: the last of the human freedoms \u2014 to choose "
        "one\u2019s attitude in any given set of circumstances.</div>"
        '<div class="quote-author">Viktor Frankl</div>'
        "</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-5">',
        quote_page + '<section class="chapter-opener" id="part-5">',
    )

    # ===================================================================
    # #60: STAT PAGE — 82%
    # ===================================================================
    stat_page_82 = (
        '<div class="stat-page">'
        '<div class="stat-number">82%</div>'
        '<div class="stat-label">Of Alienated Children Eventually Seek '
        "Reconnection</div>"
        '<div class="stat-desc">Research consistently shows that the '
        "vast majority of alienated children, once they reach adulthood, "
        "begin to question the false narrative and seek out the rejected "
        "parent.</div>"
        '<div class="stat-source">Baker &amp; Ben-Ami, 2011</div>'
        "</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Sleeper Effect</h2>)',
        stat_page_82 + r"\1",
        html,
    )

    # ===================================================================
    # #61: PHOTO OVERLAY — Before Part 6
    # ===================================================================
    photo_page_2 = (
        '<div class="photo-page">'
        f'<img src="{IMG_DIR / "community-help-for-alienated-parents.jpg"}'
        f'" alt="">'
        '<div class="photo-overlay"></div>'
        '<div class="photo-content">'
        '<div class="photo-label">Part 6</div>'
        '<div class="photo-title">You Are<br>Not Alone</div>'
        '<div class="photo-text">There is a growing community of parents '
        "who understand exactly what you are going through. Connection is "
        "survival.</div>"
        "</div></div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-6">',
        photo_page_2 + '<section class="chapter-opener" id="part-6">',
    )

    # ===================================================================
    # #62: ICON GRID — Six Steps of Resilience
    # ===================================================================
    resilience_items = [
        (I["shield"], "Accept Reality",
         "Acknowledge what you cannot control"),
        (I["insight"], "Reframe Meaning",
         "Find purpose beyond the pain"),
        (I["support"], "Build Connection",
         "You cannot do this alone"),
        (I["shield"], "Protect Yourself",
         "Physical and mental health are non-negotiable"),
        (I["star"], "Practise Hope",
         "Hope is a discipline, not a feeling"),
        (I["loving"], "Keep Loving",
         "Love that endures is the ultimate act of courage"),
    ]
    resilience_inner = ""
    for icon, title, desc in resilience_items:
        resilience_inner += (
            f'<div class="icon-grid-item"><span class="grid-icon">'
            f"{icon}</span>"
            f'<div class="grid-title">{title}</div>'
            f'<div class="grid-desc">{desc}</div></div>'
        )
    icon_grid_resilience = (
        f'<div class="icon-grid">{resilience_inner}</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        icon_grid_resilience + r"\1",
        html,
    )

    # ===================================================================
    # #63: COLOUR BAND DIVIDERS — Before part-4 and part-5
    # ===================================================================
    for part_id in ["part-4", "part-5"]:
        marker = f'id="{part_id}"'
        pos = html.find(marker)
        if pos >= 0:
            section_start = html.rfind("<section", 0, pos)
            if section_start < 0:
                section_start = pos
            # Walk back past any injected divs to find the right spot
            # Insert colour band before the section opener
            html = (
                html[:section_start]
                + '<div class="colour-band"></div>'
                + html[section_start:]
            )

    # ===================================================================
    # #64: PROGRESS TRACKER — Before "The non-negotiables"
    # ===================================================================
    progress_nodes = [
        ("You Are<br>Here", " progress-node-active"),
        ("Understand", ""),
        ("Survive", ""),
        ("Endure", ""),
        ("Inner<br>Freedom", ""),
    ]
    progress_inner = ""
    for label, cls in progress_nodes:
        progress_inner += (
            f'<div class="progress-node{cls}">'
            f'<div class="progress-dot"></div>'
            f'<div class="progress-label">{label}</div></div>'
        )
    progress_tracker = (
        '<div class="progress-tracker">'
        '<div class="progress-track-bar">'
        '<div class="progress-track-fill"></div>'
        "</div>"
        f'<div class="progress-nodes">{progress_inner}</div>'
        "</div>"
    )
    html = re.sub(
        r'(<h3 id="ch-\d+">The non-negotiables</h3>)',
        progress_tracker + r"\1",
        html,
    )

    # ===================================================================
    # #65: KEY PRINCIPLE CARD — Before "Ambiguous Loss..."
    # ===================================================================
    key_principle = (
        f'<div class="key-principle">'
        f'<div class="key-principle-icon">{I["insight"]}</div>'
        f'<div class="key-principle-text">'
        f"<strong>Naming the wound is the first step to surviving it."
        f"</strong> When you can identify what is happening to you "
        f"\u2014 clinically, precisely \u2014 the chaos begins to "
        f"resolve into something you can understand and fight.</div>"
        f"</div>"
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Ambiguous Loss and Disenfranchised Grief</h2>)',
        key_principle + r"\1",
        html,
    )

    # ===================================================================
    # #66: STAT PAGE — 69-81%
    # ===================================================================
    stat_page_69 = (
        '<div class="stat-page">'
        '<div class="stat-number">69\u201381%</div>'
        '<div class="stat-label">Of Estrangements Are Not Permanent'
        "</div>"
        '<div class="stat-desc">The research consistently shows that '
        "most alienated children eventually question the false narrative. "
        "Your consistency today is building the bridge they will one day "
        "cross.</div>"
        '<div class="stat-source">Pillemer, 2020</div>'
        "</div>"
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-6">',
        stat_page_69 + '<section class="chapter-opener" id="part-6">',
    )

    # ===================================================================
    # #67: REFERENCE COLUMNS — Middle H3s under "Community and Support"
    # ===================================================================
    community_marker = ">Community and Support</h2>"
    community_pos = html.find(community_marker)
    if community_pos >= 0:
        h3_count = 0
        search_pos = community_pos + len(community_marker)
        first_h3 = None
        for _ in range(20):
            next_h3 = html.find("<h3", search_pos)
            if next_h3 < 0:
                break
            h3_count += 1
            if h3_count == 2:
                first_h3 = next_h3
            if h3_count == 4:
                html = (
                    html[:first_h3]
                    + '<div class="reference-columns">'
                    + html[first_h3:next_h3]
                    + "</div>"
                    + html[next_h3:]
                )
                break
            search_pos = next_h3 + 4

    # ===================================================================
    # #68: ANGLED SECTION — Cast of Characters
    # ===================================================================
    html = re.sub(
        r'(<h2 id="ch-\d+">The Cast of Characters</h2>)',
        r'<div class="angled-section-teal">\1',
        html,
    )
    cast_marker = ">The Cast of Characters</h2>"
    cast_pos = html.find(cast_marker)
    if cast_pos >= 0:
        close_pos = cast_pos
        for _ in range(3):
            next_p = html.find("</p>", close_pos + 1)
            if next_p >= 0:
                close_pos = next_p
        if close_pos > cast_pos:
            html = html[: close_pos + 4] + "</div>" + html[close_pos + 4:]

    # ===================================================================
    # #69: GRID-12 — Four Pillars icon blocks
    # ===================================================================
    pillars_marker = ">The Four Pillars of Support</h3></div>"
    pillars_pos = html.find(pillars_marker)
    if pillars_pos >= 0:
        blocks_start = pillars_pos + len(pillars_marker)
        block_count = 0
        search = blocks_start
        for _ in range(20):
            next_block = html.find("</div></div>", search)
            if next_block < 0:
                break
            block_count += 1
            if block_count == 4:
                blocks_end = next_block + len("</div></div>")
                html = (
                    html[:blocks_start]
                    + '<div class="grid-12">'
                    + html[blocks_start:blocks_end]
                    + "</div>"
                    + html[blocks_end:]
                )
                break
            search = next_block + 12

    return html


# ---------------------------------------------------------------------------
# Full HTML Document Builder
# ---------------------------------------------------------------------------

def build_html(content_html: str, toc_html: str) -> str:
    """Wrap content in full HTML document with cover, TOC, and back cover."""
    # Cover artwork (prefer v2, fall back to v1)
    cover_img_path = DESIGN_IMG_DIR / "cover-artwork-v2.jpg"
    if not cover_img_path.exists():
        cover_img_path = DESIGN_IMG_DIR / "cover-artwork.jpg"
    cover_image_html = ""
    cover_overlay_html = ""
    if cover_img_path.exists():
        cover_image_html = (
            f'<img class="cover-image" src="{cover_img_path}" alt="">'
        )
        cover_overlay_html = '<div class="cover-overlay"></div>'

    # Logo
    logo_path = DESIGN_IMG_DIR / "logo.png"
    logo_html = ""
    if logo_path.exists():
        logo_html = (
            f'<img class="cover-logo" src="{logo_path}" '
            f'alt="Love Over Exile">'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Survival Guide for Alienated Parents</title>
  <link rel="stylesheet" href="{CSS_PATH}">
</head>
<body>

<!-- ====== COVER ====== -->
<section class="cover">
  {cover_image_html}
  {cover_overlay_html}
  <div class="cover-accent"></div>
  <div class="cover-content">
    {logo_html}
    <div class="cover-badge">Love Over Exile</div>
    <h1 class="cover-title">The Survival Guide<br>for Alienated Parents</h1>
    <p class="cover-subtitle"><em>Understanding What Is Happening to You &mdash; And How to Endure It</em></p>
    <div class="cover-rule"></div>
    <p class="cover-author">Malcolm Smith</p>
    <p class="cover-url">loveoverexile.com</p>
  </div>
</section>

<!-- ====== TABLE OF CONTENTS ====== -->
{toc_html}

<!-- ====== CONTENT ====== -->
{content_html}

<!-- ====== ABOUT THE AUTHOR ====== -->
<section class="page-bio author-note">
  <div class="bio-photo-frame">
    <div style="width:100%;height:100%;background:linear-gradient(135deg,#0C5E5D,#D4910A);display:flex;align-items:center;justify-content:center;font-family:'Lora',serif;font-size:24pt;color:#fff;font-weight:700;">MS</div>
  </div>
  <div class="bio-name">Malcolm Smith</div>
  <div class="bio-tagline">Author &bull; Advocate &bull; Alienated Father</div>
  <div class="bio-text">
    <p>Malcolm Smith is an alienated father and the founder of Love Over Exile, a platform dedicated to supporting alienated parents through research-based guidance and lived experience. After more than a decade navigating parental alienation firsthand, he created the resources he wished had existed at the beginning of his own journey.</p>
    <p>He writes from a place of hard-won understanding. His work draws on the research of the world&rsquo;s leading experts in parental alienation, coercive control, attachment, and trauma &mdash; translated into plain language for parents in crisis.</p>
    <p>Malcolm lives in the Netherlands and continues to advocate for greater recognition of parental alienation as a form of family violence. He created loveoverexile.com as a lifeline for parents who are fighting to stay connected to their children against impossible odds.</p>
  </div>
  <div class="bio-links">
    <span class="bio-link">loveoverexile.com</span>
  </div>
</section>

<!-- ====== BACK COVER ====== -->
<section class="back-cover">
  <blockquote>&ldquo;The truth, while suppressed, is rarely destroyed completely.&rdquo;<br>&mdash; Dr. Amy Baker</blockquote>
  <h2>Love Over Exile</h2>
  <p class="cover-subtitle"><em>Bearing the Unbearable</em></p>
  <p>A comprehensive guide for parents navigating parental alienation.</p>
  <p class="cover-author">Malcolm Smith</p>
  <p class="cover-url">loveoverexile.com</p>
</section>

</body>
</html>"""


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    """Generate the PDF ebook from markdown source."""
    print("Reading markdown...")
    md_text = MD_PATH.read_text(encoding="utf-8")

    print("Converting to HTML...")
    content_html, toc_entries = md_to_html(md_text)

    print(f"Building TOC ({len(toc_entries)} entries)...")
    toc_html = build_toc_html(toc_entries)

    print("Post-processing: injecting layout components...")
    content_html = post_process_html(content_html)

    full_html = build_html(content_html, toc_html)

    print(f"Writing HTML to {HTML_PATH}...")
    HTML_PATH.write_text(full_html, encoding="utf-8")

    print("Generating PDF with WeasyPrint...")
    result = subprocess.run(
        ["/opt/homebrew/bin/weasyprint", str(HTML_PATH), str(PDF_PATH)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"WeasyPrint error:\n{result.stderr}")
        sys.exit(1)

    print(f"PDF generated: {PDF_PATH}")
    print(f"Size: {PDF_PATH.stat().st_size // 1024} KB")

    if result.stderr:
        warnings = [ln for ln in result.stderr.split("\n") if ln.strip()]
        if warnings:
            print(f"WeasyPrint warnings ({len(warnings)}):")
            for w in warnings[:5]:
                print(f"  {w}")
            if len(warnings) > 5:
                print(f"  ... and {len(warnings) - 5} more")


if __name__ == "__main__":
    main()
