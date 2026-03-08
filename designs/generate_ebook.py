#!/usr/bin/env python3
"""Generate the Love Over Exile Survival Guide PDF from markdown + CSS."""

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
IMG_DIR = HERE.parent / "site" / "public" / "images"
DESIGN_IMG_DIR = HERE / "images"
CSS_PATH = HERE / "ebook.css"
MD_PATH = HERE / "ebook-text-3.md"
HTML_PATH = HERE / "ebook.html"
PDF_PATH = HERE / "survival-guide.pdf"

# Map diagram placeholders to image files
# Font Awesome 6 solid Unicode codepoints for key concepts
FA_ICONS = {
    "health": "\uf21e",      # medkit
    "support": "\uf0c0",     # users
    "tactics": "\uf11b",     # gamepad / chess: \uf439
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

# Section images — watercolour illustrations placed alongside text
SECTION_IMAGES = {
    "The Wound You Are Carrying": "section-wound.jpg",
    "Your Body Is Keeping Score": "section-body.jpg",
    "The Map for Survival": "section-map.jpg",
    "Community and Support": "section-community.jpg",
}

DIAGRAM_MAP = {
    "The Machine of Erasure Model": "alienating-parent-machine-of-erasure-model.png",
    "The Power and Control Wheel": None,  # No standalone image — described in text
    "The Diagnostic Bridge": None,  # Table in text
    "The Parental Alienation Landscape": "parental-alienation-landscape.png",
    "The 2D Alienation Trauma Pain Model": "2d-alienation-trauma-pain-model.png",
    "The Alienated Child": "alienated-child-systemic-conditioning-model.png",
    "The Alienated Parent Sphere of Influence": "alienated-parent-sphere-of-influence.png",
    "The Alienated Parent Survival and Engagement Model": "alienated-parent-survival-and-engagement-model-love-over-exile.png",
}

# Chapter motif images (one per Part)
CHAPTER_MOTIFS = {
    1: "chapter-motif-1.png",
    2: "chapter-motif-2.png",
    3: "chapter-motif-3.png",
    4: "chapter-motif-4.png",
    5: "chapter-motif-5.png",
    6: "chapter-motif-6.png",
}


def md_to_html(md_text: str) -> tuple[str, list[dict]]:
    """Convert markdown to HTML with ebook-specific structure.

    Returns (html_content, toc_entries) where toc_entries is a list of
    dicts with keys: type ('part' or 'chapter'), id, title.
    """
    lines = md_text.split("\n")
    html_parts = []
    toc_entries = []
    in_list = False
    in_table = False
    table_rows = []
    current_part_num = 0
    chapter_counter = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip diagram placeholders — replace with actual images
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

        # Close open list if needed
        if in_list and not line.startswith("- ") and line.strip() != "":
            html_parts.append("</ul>")
            in_list = False

        # Table handling
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
            # Don't increment — process current line

        # Horizontal rule / section break
        if line.strip() == "---":
            html_parts.append('<div class="divider">\u2726</div>')
            i += 1
            continue

        # Part headers (# PART X:)
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

            # Check for chapter motif image
            motif_html = ""
            motif_file = CHAPTER_MOTIFS.get(current_part_num)
            if motif_file:
                motif_path = DESIGN_IMG_DIR / motif_file
                if motif_path.exists():
                    motif_html = f'<img class="chapter-motif" src="{motif_path}" alt="">'

            html_parts.append(
                f'<section class="chapter-opener" id="{part_id}">'
                f'{motif_html}'
                f'<div class="chapter-number">{part_label}</div>'
                f'<div class="chapter-rule"></div>'
                f'<div class="chapter-title">{part_title}</div>'
                f'<div class="chapter-part-bg">{current_part_num}</div>'
                f"</section>"
            )
            i += 1
            continue

        # H1 (title — only the very first one)
        if line.startswith("# ") and not line.startswith("# PART"):
            title = line[2:]
            # This is the book title — skip, handled by cover
            i += 1
            continue

        # H2
        if line.startswith("## "):
            chapter_counter += 1
            raw_title = line[3:]
            title = process_inline(raw_title)
            chapter_id = f"ch-{chapter_counter}"
            plain_title = re.sub(r"<[^>]+>", "", title)
            toc_entries.append({
                "type": "chapter",
                "id": chapter_id,
                "title": plain_title,
            })

            # Check if this section has a paired image
            section_img = SECTION_IMAGES.get(raw_title.strip())
            if section_img:
                img_path = DESIGN_IMG_DIR / section_img
                if img_path.exists():
                    html_parts.append(
                        f'<div class="section-opener">'
                        f'<img src="{img_path}" alt="{plain_title}">'
                        f'<div class="text-content">'
                        f'<h2 id="{chapter_id}">{title}</h2>'
                        f'</div></div>'
                    )
                    i += 1
                    continue

            html_parts.append(f'<h2 id="{chapter_id}">{title}</h2>')
            i += 1
            continue

        # H3
        if line.startswith("### "):
            title = process_inline(line[4:])
            html_parts.append(f"<h3>{title}</h3>")
            i += 1
            continue

        # Blockquote
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            quote_text = process_inline(" ".join(quote_lines))
            # Check if it's an attributed quote (has em dash)
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
                    f'<div class="quote-mark"><p>{quote_text}</p></div>'
                )
            continue

        # Unordered list
        if line.startswith("- "):
            if not in_list:
                html_parts.append('<ul class="custom">')
                in_list = True
            content = process_inline(line[2:])
            html_parts.append(f"<li>{content}</li>")
            i += 1
            continue

        # Numbered list items like "1. **..." or "**1. ..."
        m = re.match(r"^\*\*(\d+)\.\s+(.+?)\*\*\s*(.*)$", line)
        if m:
            num = m.group(1)
            title = m.group(2)
            rest = process_inline(m.group(3))
            # Check for "Instead:" on next line
            instead = ""
            if i + 1 < len(lines) and lines[i + 1].startswith("*Instead:"):
                instead_text = process_inline(
                    lines[i + 1].strip("*").replace("Instead: ", "")
                )
                instead = f'<br><span class="text-sage"><em>Instead: {instead_text}</em></span>'
                i += 1
            html_parts.append(
                f'<div class="numbered-item avoid-break">'
                f'<div class="num">{num}</div>'
                f'<div class="content"><strong>{title}</strong>'
                f"<p>{rest}{instead}</p></div></div>"
            )
            i += 1
            continue

        # Bold paragraph start like "**Level 1: ...**"
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line)
        if m and i + 1 < len(lines) and lines[i + 1].strip():
            # This is a bold label followed by description on next line
            label = m.group(1)
            i += 1
            desc_lines = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(
                "**"
            ) and not lines[i].startswith("#") and not lines[i].startswith(">") and not lines[i].startswith("- ") and not lines[i].startswith("*["):
                desc_lines.append(lines[i])
                i += 1
            desc = process_inline(" ".join(desc_lines))
            html_parts.append(f"<p><strong>{label}</strong><br>{desc}</p>")
            continue

        # Regular paragraph
        if line.strip():
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(
                "#"
            ) and not lines[i].startswith(">") and not lines[i].startswith(
                "- "
            ) and not lines[i].startswith("**") and not lines[i].startswith(
                "|"
            ) and not lines[i].startswith("*["):
                para_lines.append(lines[i])
                i += 1
            text = process_inline(" ".join(para_lines))
            html_parts.append(f"<p>{text}</p>")
            continue

        i += 1

    # Close any open list
    if in_list:
        html_parts.append("</ul>")
    if in_table:
        html_parts.append(render_table(table_rows))

    return "\n".join(html_parts), toc_entries


def post_process_html(html: str) -> str:
    """Inject layout components at strategic content points."""
    # FA icons
    I = FA_ICONS

    # --- 1. KEY FACTS STRIP after "The numbers are staggering:" ---
    facts_strip = (
        '<div class="key-facts-strip">'
        f'<div class="fact"><span class="fact-number">22M</span>'
        '<span class="fact-label">Affected Parents</span></div>'
        f'<div class="fact"><span class="fact-number">13.4%</span>'
        '<span class="fact-label">Of All Parents</span></div>'
        f'<div class="fact"><span class="fact-number">39.2%</span>'
        '<span class="fact-label">UK Separated</span></div>'
        f'<div class="fact"><span class="fact-number">40%</span>'
        '<span class="fact-label">Research Since 2016</span></div>'
        '</div>'
    )
    html = html.replace(
        '<p>The numbers are staggering:</p>',
        '<p>The numbers are staggering:</p>' + facts_strip
    )

    # --- 2. HERO BAND for "It Is Not Conflict. It Is Abuse." ---
    html = re.sub(
        r'<h2 id="(ch-\d+)">It Is Not Conflict\. It Is Abuse\.</h2>',
        r'<div class="hero-band hero-band-teal">'
        f'<h2 id="\\1" style="color:white;margin:0;">'
        f'{I["warning"]} It Is Not Conflict. It Is Abuse.</h2>'
        '</div>',
        html
    )

    # --- 3. ICON BLOCKS for the Four Pillars of Support ---
    support_icons = [
        (I["brain"], "A PA-Aware Therapist", "Your emotional anchor — someone who specifically understands parental alienation and high-conflict separation."),
        (I["balance"], "A Specialist Family Lawyer", "Your strategic advisor — with specific experience in alienation cases and high-conflict litigation."),
        (I["support"], "One Trusted Friend", "Your reality check — the person who loves you, sees you, and keeps you grounded."),
        (I["star"], "A Support Group", "Your community — people living the same reality who truly understand."),
    ]
    icon_blocks_html = ""
    for icon, title, desc in support_icons:
        icon_blocks_html += (
            f'<div class="icon-block">'
            f'<div class="icon-block-icon">{icon}</div>'
            f'<div class="icon-block-content">'
            f'<strong>{title}</strong>'
            f'<p>{desc}</p>'
            f'</div></div>'
        )
    html = html.replace(
        '<h3>The Four Pillars of Support</h3>',
        '<h3>The Four Pillars of Support</h3>' + icon_blocks_html
    )

    # --- 4. ACCENT CARD for emergency help ---
    emergency_card = (
        f'<div class="accent-card accent-card-amber">'
        f'<div class="accent-card-icon">{I["warning"]}</div>'
        f'<div class="accent-card-content">'
        f'<h4>Crisis Support</h4>'
        f'<p><strong>UK:</strong> Samaritans — 116 123<br>'
        f'<strong>US:</strong> 988 Suicide &amp; Crisis Lifeline — 988<br>'
        f'<strong>International:</strong> befrienders.org</p>'
        f'</div></div>'
    )
    html = html.replace(
        '<p>Your child needs you alive. Everything else is secondary.</p>',
        emergency_card
        + '<p>Your child needs you alive. Everything else is secondary.</p>'
    )

    # --- 5. ACCENT CARD for BIFF method ---
    biff_card = (
        f'<div class="accent-card accent-card-teal">'
        f'<div class="accent-card-icon">{I["shield"]}</div>'
        f'<div class="accent-card-content">'
        f'<h4>The BIFF Method</h4>'
        f'<p><strong>Brief</strong> — Say only what is necessary<br>'
        f'<strong>Informative</strong> — Factual, not emotional<br>'
        f'<strong>Friendly</strong> — Polite but not warm<br>'
        f'<strong>Firm</strong> — Clear boundaries</p>'
        f'</div></div>'
    )
    html = html.replace(
        '<h3>Communication: The BIFF Method</h3>',
        '<h3>Communication: The BIFF Method</h3>' + biff_card
    )

    # --- 6. STEP INDICATOR for "What This Guide Covers" ---
    steps_html = (
        '<div class="step-indicator">'
        '<div class="step"><span class="step-number">1</span>'
        '<span class="step-label">Understand</span><br>'
        '<span class="step-desc">The Epidemic</span></div>'
        '<div class="step"><span class="step-number">2</span>'
        '<span class="step-label">Recognise</span><br>'
        '<span class="step-desc">The Machine</span></div>'
        '<div class="step"><span class="step-number">3</span>'
        '<span class="step-label">Name</span><br>'
        '<span class="step-desc">The Impact</span></div>'
        '<div class="step"><span class="step-number">4</span>'
        '<span class="step-label">Survive</span><br>'
        '<span class="step-desc">Framework</span></div>'
        '<div class="step"><span class="step-number">5</span>'
        '<span class="step-label">Endure</span><br>'
        '<span class="step-desc">The Long Road</span></div>'
        '<div class="step"><span class="step-number">6</span>'
        '<span class="step-label">Connect</span><br>'
        '<span class="step-desc">Community</span></div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">What This Guide Covers</h2>)',
        r'\1' + steps_html,
        html
    )

    # --- 7. CHECKLIST for documentation section ---
    checklist_html = (
        '<div class="checklist-panel">'
        f'<h4>{I["check"]} Documentation Checklist</h4>'
        '<ul>'
        '<li>Date, time, and location of every interaction</li>'
        '<li>Missed handovers and blocked communications</li>'
        '<li>Screenshots of messages (factual, no commentary)</li>'
        '<li>Witness names and contact details</li>'
        '<li>School reports, medical records, event attendance</li>'
        '<li>Financial records of legal costs</li>'
        '</ul>'
        '</div>'
    )
    html = html.replace(
        '<h3>Documentation</h3>',
        '<h3>Documentation</h3>' + checklist_html
    )

    # --- 8. COMPARISON PANEL for Cognitive Diet ---
    comparison_html = (
        '<div class="comparison-panel">'
        '<div class="panel-do">'
        f'<h4>{I["check"]} Let In</h4>'
        '<p>Educational content about alienation. Supportive communities. '
        'Professional guidance. Content that builds hope and resilience.</p>'
        '</div>'
        '<div class="panel-dont">'
        f'<h4>{I["warning"]} Shut Out</h4>'
        '<p>Doom-scrolling. The alienator\'s social media. Toxic forums. '
        'Unsolicited advice. Constant review of case details.</p>'
        '</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>The Cognitive Diet</h3>',
        '<h3>The Cognitive Diet</h3>' + comparison_html
    )

    # --- 9. HERO BAND for Inner Freedom ---
    html = re.sub(
        r'<h2 id="(ch-\d+)">Inner Freedom</h2>',
        r'<div class="hero-band hero-band-teal">'
        r'<h2 id="\1" style="color:white;margin:0;">Inner Freedom</h2>'
        '<p style="color:rgba(255,255,255,0.9);margin-bottom:0;">'
        'The state of knowing who you are at a depth that no court, '
        'no allegation, and no rejection can touch.</p>'
        '</div>',
        html
    )

    # --- 10. ICON BLOCKS for Sphere of Influence circles ---
    sphere_icons = [
        (I["shield"], "Circle 1: What You Control", "Your health, your mindset, your character, your documentation, your parenting quality."),
        (I["key"], "Circle 2: What You Can Influence", "Your legal strategy, your communication approach, your professional team, your public narrative."),
        (I["loving"], "Circle 3: What You Can Only Accept", "The court system, the alienating parent's behaviour, your child's current feelings, other people's opinions."),
    ]
    sphere_html = ""
    for icon, title, desc in sphere_icons:
        sphere_html += (
            f'<div class="icon-block">'
            f'<div class="icon-block-icon">{icon}</div>'
            f'<div class="icon-block-content">'
            f'<strong>{title}</strong>'
            f'<p>{desc}</p>'
            f'</div></div>'
        )
    # Insert after the H2 for Sphere of Influence
    html = re.sub(
        r'(<h2 id="ch-\d+">The Sphere of Influence</h2>)',
        r'\1' + sphere_html,
        html
    )

    # --- 11. ACCENT CARD for Stockdale Paradox key insight ---
    stockdale_card = (
        f'<div class="accent-card accent-card-teal">'
        f'<div class="accent-card-icon">{I["insight"]}</div>'
        f'<div class="accent-card-content">'
        f'<h4>The Stockdale Paradox</h4>'
        f'<p>Unwavering faith that you will prevail, combined with '
        f'brutal realism about how long it may take.</p>'
        f'</div></div>'
    )
    html = html.replace(
        '<h3>The Stockdale Paradox</h3>',
        '<h3>The Stockdale Paradox</h3>' + stockdale_card
    )

    # --- 12. HERO BAND for "A Final Word" ---
    html = re.sub(
        r'<h2 id="(ch-\d+)">A Final Word</h2>',
        r'<div class="hero-band hero-band-teal">'
        r'<h2 id="\1" style="color:white;margin:0;">A Final Word</h2>'
        '</div>',
        html
    )

    # --- 13. PAGE SECTION for "About the Book" promo ---
    html = re.sub(
        r'<h2 id="(ch-\d+)">About the Book</h2>',
        r'<div class="page-section-coloured">'
        r'<h2 id="\1" style="margin-top:0;">About the Book</h2>'
        '</div>',
        html
    )

    # --- 15. KEY TAKEAWAYS for Part 1 (The Quiet Epidemic) ---
    takeaways_part1 = (
        '<div class="key-takeaways">'
        f'<h4><span class="fa-icon">{I["key"]}</span> Key Takeaways</h4>'
        '<ol>'
        '<li>Parental alienation is a recognised pattern of psychological abuse — not a custody dispute.</li>'
        '<li>22 million parents in the US and Canada alone report being targeted.</li>'
        '<li>It maps directly onto the Duluth Power and Control Wheel for domestic violence.</li>'
        '<li>Each of the eight behavioural signs in the child is a direct consequence of a specific coercive control tactic.</li>'
        '<li>40% of all research has been published since 2016 — the science is young, but it is real.</li>'
        '</ol>'
        '</div>'
    )
    # Insert before Part 2 opener
    html = html.replace(
        '<section class="chapter-opener" id="part-2">',
        takeaways_part1 + '<section class="chapter-opener" id="part-2">'
    )

    # --- 16. ADMONITION (legal warning) for "This guide is not legal advice" ---
    legal_admonition = (
        f'<div class="admonition admonition-legal">'
        f'<div class="admonition-header"><span class="admonition-icon">{I["balance"]}</span> Legal Note</div>'
        f'<p>This guide provides general information based on research and lived experience. '
        f'It is not legal, medical, or therapeutic advice. Always consult qualified professionals '
        f'for your specific situation.</p>'
        f'</div>'
    )
    html = html.replace(
        '<h3>The non-negotiables</h3>',
        legal_admonition + '<h3>The non-negotiables</h3>'
    )

    # --- 17. BEFORE/AFTER for common mistake: fighting fire with fire ---
    before_after = (
        f'<div class="before-after">'
        f'<div class="before-box"><h4>{I["warning"]} Before</h4>'
        f'<p>"They badmouthed me, so I told the children exactly what their mother did. '
        f'I showed them the court documents. I wanted them to know the truth."</p></div>'
        f'<div class="transition-arrow">{I["arrow"]}</div>'
        f'<div class="after-box"><h4>{I["check"]} After</h4>'
        f'<p>"I stopped trying to counter the narrative. I focused on being calm, present, and consistent. '
        f'I let my behaviour speak for itself. The children will find the truth when they are ready."</p></div>'
        f'</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 10 Most Common Mistakes</h2>)',
        r'\1' + before_after,
        html
    )

    # --- 18. DIALOGUE BLOCK for example BIFF response ---
    dialogue = (
        '<div class="dialogue">'
        '<div class="dialogue-msg dialogue-msg-left">'
        '<span class="speaker">Alienating parent</span>'
        '"The children don\'t want to see you this weekend. They have plans. '
        'Stop forcing them."'
        '</div>'
        '<div class="dialogue-msg dialogue-msg-right">'
        '<span class="speaker">Your BIFF response</span>'
        '"Thank you for letting me know. I will be at the agreed location at the agreed time, '
        'as per the court order. I look forward to seeing them."'
        '</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>The Universal Agreement</h3>',
        dialogue + '<h3>The Universal Agreement</h3>'
    )

    # --- 19. EVIDENCE LOG TEMPLATE for Documentation section ---
    evidence_log = (
        '<div class="evidence-log">'
        f'<h4>{I["book"]} Incident Record Template</h4>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Date:</span>'
        '<span class="evidence-log-field"></span>'
        '</div>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Time:</span>'
        '<span class="evidence-log-field"></span>'
        '</div>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Location:</span>'
        '<span class="evidence-log-field"></span>'
        '</div>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Witnesses:</span>'
        '<span class="evidence-log-field"></span>'
        '</div>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Incident:</span>'
        '<span class="evidence-log-field-large"></span>'
        '</div>'
        '<div class="evidence-log-row">'
        '<span class="evidence-log-label">Evidence:</span>'
        '<span class="evidence-log-field-large"></span>'
        '</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>Parallel Parenting</h3>',
        evidence_log + '<h3>Parallel Parenting</h3>'
    )

    # --- 20. ANNOTATION STRIPE for key reminder ---
    annotation = (
        '<div class="annotation-stripe">'
        'Remember: Your child needs you alive, healthy, and whole'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        annotation + r'\1',
        html
    )

    # --- 21. KEY TAKEAWAYS for Part 4 (Survival Framework) ---
    takeaways_part4 = (
        '<div class="key-takeaways">'
        f'<h4><span class="fa-icon">{I["key"]}</span> Key Takeaways</h4>'
        '<ol>'
        '<li>Stabilise yourself first — sleep, movement, nutrition, and professional support are non-negotiable.</li>'
        '<li>Build four pillars: PA-aware therapist, specialist lawyer, one trusted friend, and a support group.</li>'
        '<li>Focus energy on what you control. Accept what you cannot change.</li>'
        '<li>Use BIFF communication: Brief, Informative, Friendly, Firm.</li>'
        '<li>Document everything. Facts, not feelings.</li>'
        '</ol>'
        '</div>'
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-5">',
        takeaways_part4 + '<section class="chapter-opener" id="part-5">'
    )

    # --- 22. ADMONITION (tip) for Sleeper Effect hope ---
    hope_admonition = (
        f'<div class="admonition admonition-tip">'
        f'<div class="admonition-header"><span class="admonition-icon">{I["star"]}</span> There Is Hope</div>'
        f'<p>69–81% of general estrangements are not permanent (Pillemer, 2020). '
        f'Many alienated children reconnect as adults. Your consistency today is building the '
        f'foundation for reunion tomorrow.</p>'
        f'</div>'
    )
    html = html.replace(
        '<p><strong>69-81% of general estrangements are not permanent</strong>',
        hope_admonition + '<p><strong>69-81% of general estrangements are not permanent</strong>'
    )

    # --- 14. DROP CAPS on first paragraphs after Part openers ---
    # Apply drop-cap to first paragraph after key section headings
    drop_cap_sections = [
        "What Is Parental Alienation?",
        "The Cast of Characters",
        "When Letting Go Keeps the Door Open",
    ]
    for section_title in drop_cap_sections:
        marker = f">{section_title}</h2>"
        pos = html.find(marker)
        if pos >= 0:
            # Find the first <p> after this h2
            p_pos = html.find('<p>', pos + len(marker))
            if p_pos >= 0:
                html = html[:p_pos] + '<p class="drop-cap">' + html[p_pos + 3:]

    # =================================================================
    # PHASE 2+3: NEW COMPONENT INJECTIONS
    # =================================================================

    # --- 23. ORNAMENTAL DIVIDERS — Replace plain dividers with ornamental ones ---
    # Upgrade every 3rd divider to an ornamental style for variety
    divider_pattern = '<div class="divider">\u2726</div>'
    ornamental_dividers = [
        '<div class="ornamental-divider"><span class="ornament">\u2766 \u2767</span></div>',
        '<div class="ornamental-divider"><span class="ornament">\u2053</span></div>',
        '<div class="ornamental-divider"><span class="ornament">\u2726 \u2726 \u2726</span></div>',
    ]
    divider_count = 0
    while divider_pattern in html:
        divider_count += 1
        if divider_count % 3 == 0:
            # Every 3rd divider becomes ornamental
            replacement = ornamental_dividers[(divider_count // 3 - 1) % len(ornamental_dividers)]
            html = html.replace(divider_pattern, replacement, 1)
        else:
            # Keep as gradient-fade divider (Phase 1 improvement)
            html = html.replace(divider_pattern, '<div class="divider-fade"></div>', 1)

    # --- 24. SIDEBAR CALLOUT — Float alongside text in key sections ---
    sidebar_callout = (
        '<div class="sidebar-callout">'
        f'<div class="sidebar-callout-title">{I["insight"]} Key Insight</div>'
        '<p>Research shows that children who maintain a relationship with both '
        'parents after separation have significantly better outcomes across all '
        'measures of wellbeing.</p>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">What Is Parental Alienation\?</h2>)',
        r'\1' + sidebar_callout,
        html
    )

    # --- 25. BAR CHART — Research statistics visualisation ---
    bar_chart = (
        '<div class="bar-chart">'
        '<div class="bar-chart-title">Research Growth in Parental Alienation</div>'
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Since 2016</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill" style="width:40%">'
        '<span class="bar-chart-value">40%</span></div></div></div>'
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Since 2010</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill" style="width:65%">'
        '<span class="bar-chart-value">65%</span></div></div></div>'
        '<div class="bar-chart-row">'
        '<span class="bar-chart-label">Total Studies</span>'
        '<div class="bar-chart-track"><div class="bar-chart-fill bar-chart-fill-gold" style="width:100%">'
        '<span class="bar-chart-value">1,200+</span></div></div></div>'
        '</div>'
    )
    html = html.replace(
        '<p><strong>40% of all parental alienation research has been published since 2016</strong>',
        bar_chart + '<p><strong>40% of all parental alienation research has been published since 2016</strong>'
    )

    # --- 26. INSET PULL QUOTE — Floated magazine-style quote ---
    inset_quote = (
        '<div class="inset-pull-quote">'
        '<p>Your child needs a parent who is alive, healthy, and whole. '
        'Everything else is secondary.</p>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Map for Survival</h2>)',
        r'\1' + inset_quote,
        html
    )

    # --- 27. RIBBON BANNER — Eye-catching section header ---
    html = re.sub(
        r'<h3>The Four Pillars of Support</h3>',
        '<div class="ribbon-banner"><h3>The Four Pillars of Support</h3></div>',
        html
    )

    # --- 28. VERTICAL TIMELINE — Recovery journey stages ---
    timeline = (
        '<div class="vertical-timeline">'
        '<div class="timeline-item">'
        '<div class="timeline-item-title">Stage 1: Crisis</div>'
        '<p>Shock, grief, disbelief. The world has changed overnight.</p></div>'
        '<div class="timeline-item">'
        '<div class="timeline-item-title">Stage 2: Stabilisation</div>'
        '<p>Building your team. Finding your footing. Establishing routines.</p></div>'
        '<div class="timeline-item timeline-item-active">'
        '<div class="timeline-item-title">Stage 3: Strategic Action</div>'
        '<p>Documentation, legal strategy, communication discipline.</p></div>'
        '<div class="timeline-item">'
        '<div class="timeline-item-title">Stage 4: Endurance</div>'
        '<p>The long road. Maintaining hope while accepting reality.</p></div>'
        '<div class="timeline-item">'
        '<div class="timeline-item-title">Stage 5: Inner Freedom</div>'
        '<p>Knowing who you are at a depth no court can touch.</p></div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Wound You Are Carrying</h2>)',
        r'\1' + timeline,
        html
    )

    # --- 29. CORNER FRAME — Around key takeaway boxes ---
    # Wrap the existing key-takeaways in a corner frame for visual emphasis
    html = html.replace(
        '<div class="key-takeaways">',
        '<div class="corner-frame"><div class="key-takeaways">',
        1  # Only first instance
    )
    # Close the corner frame after the key-takeaways closing div
    first_kt_end = html.find('</div>', html.find('<div class="corner-frame"><div class="key-takeaways">') + 50)
    # Find the actual end of key-takeaways (after </ol></div>)
    kt_start = html.find('<div class="corner-frame"><div class="key-takeaways">')
    if kt_start >= 0:
        # Count divs to find the matching close
        search_from = kt_start + len('<div class="corner-frame">')
        depth = 1
        pos = search_from
        while depth > 0 and pos < len(html):
            next_open = html.find('<div', pos + 1)
            next_close = html.find('</div>', pos + 1)
            if next_close < 0:
                break
            if next_open >= 0 and next_open < next_close:
                depth += 1
                pos = next_open
            else:
                depth -= 1
                pos = next_close
        if depth == 0:
            html = html[:pos + 6] + '</div>' + html[pos + 6:]

    # --- 30. DID YOU KNOW panel + dot pattern ---
    did_you_know = (
        '<div class="did-you-know pattern-dots">'
        f'<div class="did-you-know-label">{I["brain"]} Did You Know?</div>'
        '<p>Children who are alienated from a parent show measurable changes in '
        'brain development, particularly in areas governing attachment, trust, '
        'and emotional regulation. The effects mirror those seen in other forms '
        'of psychological abuse.</p>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Why Children Are Vulnerable</h2>)',
        r'\1' + did_you_know,
        html
    )

    # --- 31. SECTION COLOUR WASHES — Alternating tints on H2 sections ---
    # Add teal wash to specific sections for visual rhythm
    wash_sections = [
        "The Cast of Characters",
        "The Map for Survival",
        "Self-Compassion Is Not Optional",
    ]
    for section_title in wash_sections:
        marker = f">{section_title}</h2>"
        pos = html.find(marker)
        if pos >= 0:
            # Find the <h2 tag start
            h2_start = html.rfind('<h2', 0, pos)
            if h2_start >= 0:
                html = (html[:h2_start]
                        + '<div class="section-wash-teal">'
                        + html[h2_start:])
                # Close wash after about 1 paragraph (find 3rd </p>)
                close_pos = pos + len(marker)
                for _ in range(3):
                    next_p = html.find('</p>', close_pos + 1)
                    if next_p >= 0:
                        close_pos = next_p
                if close_pos > pos:
                    html = html[:close_pos + 4] + '</div>' + html[close_pos + 4:]

    # =================================================================
    # MISSING COMPONENTS: Full Implementation
    # =================================================================

    # --- 32. CONTENT WARNING before Part 3 (heavy trauma content) ---
    content_warning = (
        f'<div class="content-warning">'
        f'<div class="content-warning-header">{I["warning"]} Content Note</div>'
        f'<p>This section discusses the psychological impact of parental alienation, '
        f'including trauma, grief, and suicidal ideation. If you are in distress, '
        f'please reach out to a crisis service (see Part 6) before continuing.</p>'
        f'</div>'
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-3">',
        content_warning + '<section class="chapter-opener" id="part-3">'
    )

    # --- 33. MYTH VS REALITY TABLE — Common PA misconceptions ---
    myth_reality = (
        '<div class="myth-reality">'
        '<div class="myth-row">'
        '<div class="myth-header">Myth</div>'
        '<div class="reality-header">Reality</div></div>'
        '<div class="myth-row">'
        '<div class="myth-cell">"The child just needs time to adjust"</div>'
        '<div class="reality-cell">Without intervention, alienation typically worsens over time, not improves</div></div>'
        '<div class="myth-row">'
        '<div class="myth-cell">"Both parents are equally to blame"</div>'
        '<div class="reality-cell">Alienation is a pattern of coercive control by one parent against the other</div></div>'
        '<div class="myth-row">'
        '<div class="myth-cell">"If the child says it, it must be true"</div>'
        '<div class="reality-cell">Children repeat coached narratives they believe are their own thoughts</div></div>'
        '<div class="myth-row">'
        '<div class="myth-cell">"A good parent would just move on"</div>'
        '<div class="reality-cell">Refusing to abandon your child is an act of love, not obsession</div></div>'
        '<div class="myth-row">'
        '<div class="myth-cell">"Courts always get it right"</div>'
        '<div class="reality-cell">Most family courts lack training to identify alienation dynamics</div></div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">What the Data Shows</h2>)',
        r'\1' + myth_reality,
        html
    )

    # --- 34. SELF-ASSESSMENT — Five-Factor checklist ---
    self_assessment = (
        '<div class="self-assessment">'
        f'<div class="self-assessment-header">{I["check"]} Self-Assessment: Is This Alienation?</div>'
        '<div class="self-assessment-item">'
        '<div class="self-assessment-check"></div>'
        '<div>Your child refuses or resists contact with you</div></div>'
        '<div class="self-assessment-item">'
        '<div class="self-assessment-check"></div>'
        '<div>You previously had a positive, loving relationship with your child</div></div>'
        '<div class="self-assessment-item">'
        '<div class="self-assessment-check"></div>'
        '<div>There is no history of abuse or neglect on your part</div></div>'
        '<div class="self-assessment-item">'
        '<div class="self-assessment-check"></div>'
        '<div>The other parent has engaged in behaviours that undermine your relationship</div></div>'
        '<div class="self-assessment-item">'
        '<div class="self-assessment-check"></div>'
        '<div>Your child shows signs: campaign of denigration, weak reasons, lack of remorse, "independent thinker" claim</div></div>'
        '<div class="self-assessment-note">If all five factors are present, you are likely dealing with '
        'parental alienation. Seek a PA-aware professional for assessment.</div>'
        '</div>'
    )
    html = html.replace(
        '<p>When all five factors align, you are not looking at a child who has made a free choice.',
        self_assessment + '<p>When all five factors align, you are not looking at a child who has made a free choice.'
    )

    # --- 35. BREATHING PAUSE — After "The Four Levels of Heartbreak" ---
    breathing_pause = (
        '<div class="breathing-pause">'
        f'<div class="breathing-pause-title">{I["loving"]} Pause Here If You Need To</div>'
        '<div class="breathing-steps">'
        '<strong>Breathe in</strong> for 4 counts. '
        '<strong>Hold</strong> for 4 counts. '
        '<strong>Breathe out</strong> for 6 counts.<br>'
        'Repeat three times. You are safe right now.'
        '</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>The Eight Amplification Factors</h3>',
        breathing_pause + '<h3>The Eight Amplification Factors</h3>'
    )

    # --- 36. NORMALISATION STATEMENT — After "Ambiguous Loss" section ---
    normalisation = (
        '<div class="normalisation">'
        '<p><strong>It is completely normal</strong> to feel like you are going mad. '
        'The confusion, the obsessive thinking, the inability to "move on" — these '
        'are not signs of weakness. They are the documented consequences of a loss '
        'the human brain was never designed to process.</p>'
        '</div>'
    )
    html = html.replace(
        '<p>Understanding ambiguous loss and disenfranchised grief is not academic.',
        normalisation + '<p>Understanding ambiguous loss and disenfranchised grief is not academic.'
    )

    # --- 37. HIGHLIGHT BAR — "50% of targeted parents meet PTSD criteria" ---
    highlight_ptsd = (
        '<div class="highlight-bar">'
        f'<p>{I["warning"]} Up to 50% of targeted parents meet clinical criteria for PTSD. '
        'You are not overreacting. You are appropriately responding to an impossible situation.</p>'
        '</div>'
    )
    html = html.replace(
        '<p><strong>Up to 50% of targeted parents</strong>',
        highlight_ptsd + '<p><strong>Up to 50% of targeted parents</strong>'
    )

    # --- 38. TESTIMONY CARD — In "What alienated children remember" ---
    testimony = (
        '<div class="testimony-card">'
        '<div class="testimony-text">"I found the box of birthday cards my dad had sent '
        'every year. Dozens of them, unopened. That was the moment I realised everything '
        'I had been told was a lie. He never stopped loving me."</div>'
        '<div class="testimony-attribution">— Adult survivor of childhood alienation '
        '(composite, based on Dr. Amy Baker\'s research)</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>What alienated children remember</h3>',
        '<h3>What alienated children remember</h3>' + testimony
    )

    # --- 39. SCENARIO CARD — BIFF method in action ---
    scenario = (
        '<div class="scenario-card">'
        '<div class="scenario-header">Scenario: The School Event</div>'
        '<div class="scenario-body">'
        '<div class="scenario-situation">'
        'Your child\'s school play is next week. The alienating parent has told the '
        'school you are "not welcome." Your child has not mentioned it to you.'
        '</div>'
        '<div class="scenario-response">'
        '<strong>Response:</strong> Contact the school directly (you have parental rights '
        'to attend). Arrive calmly, sit where your child can see you. Do not approach '
        'the alienating parent. Take photos for your records. If your child acknowledges '
        'you, respond warmly but without pressure. If they don\'t, that is okay too. '
        'Your presence is the message.'
        '</div></div></div>'
    )
    html = html.replace(
        '<h3>Staying Connected</h3>',
        scenario + '<h3>Staying Connected</h3>'
    )

    # --- 40. COPING STRATEGY CARD — Grounding technique ---
    coping_card = (
        '<div class="coping-card">'
        f'<div class="coping-card-header">{I["shield"]} Grounding Technique: The 5-4-3-2-1 Method</div>'
        '<p>When panic or emotional flooding hits, use your senses to anchor yourself:</p>'
        '<ol>'
        '<li><strong>5 things</strong> you can see</li>'
        '<li><strong>4 things</strong> you can touch</li>'
        '<li><strong>3 things</strong> you can hear</li>'
        '<li><strong>2 things</strong> you can smell</li>'
        '<li><strong>1 thing</strong> you can taste</li>'
        '</ol>'
        '</div>'
    )
    html = html.replace(
        '<h3>When to seek emergency help</h3>',
        coping_card + '<h3>When to seek emergency help</h3>'
    )

    # --- 41. TRY THIS — Self-compassion exercise ---
    try_this_compassion = (
        '<div class="try-this">'
        f'<div class="try-this-header">{I["star"]} Try This: The Self-Compassion Letter</div>'
        '<p>Write a letter to yourself from the perspective of a loving, wise friend '
        'who knows everything you have been through. What would they say? How would '
        'they describe your strength? Let their words replace the harsh inner critic.</p>'
        '<div class="writing-lines">'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        '<div class="writing-line"></div>'
        '</div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        r'\1' + try_this_compassion,
        html
    )

    # --- 42. TRY THIS — Sphere of Influence exercise ---
    try_this_sphere = (
        '<div class="try-this">'
        f'<div class="try-this-header">{I["key"]} Try This: Map Your Circles</div>'
        '<p>Take a piece of paper and draw three concentric circles. Write in each:</p>'
        '<p><strong>Inner circle:</strong> What you control right now (list 3 things)<br>'
        '<strong>Middle circle:</strong> What you can influence (list 2 things)<br>'
        '<strong>Outer circle:</strong> What you must accept (list 1 thing)</p>'
        '<p>Commit to spending 80% of your energy on the inner circle this week.</p>'
        '</div>'
    )
    html = html.replace(
        '<h3>Circle 3: What You Can Only Accept</h3>',
        try_this_sphere + '<h3>Circle 3: What You Can Only Accept</h3>'
    )

    # --- 43. AFFIRMATION CARD — After "The Sleeper Effect" ---
    affirmation = (
        '<div class="affirmation-card">'
        '<span class="affirmation-label">Remember</span>'
        '<p>Your consistency today is building the foundation for reunion tomorrow. '
        'Every birthday card sent, every calm response given, every moment of restraint '
        'is a seed planted in your child\'s future memory.</p>'
        '</div>'
    )
    html = html.replace(
        '<p><strong>69-81% of general estrangements are not permanent</strong>',
        affirmation + '<p><strong>69-81% of general estrangements are not permanent</strong>'
    )

    # --- 44. REFLECTION PROMPTS — At end of each Part ---
    reflection_parts = {
        "part-2": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} Reflect</div>'
            '<p>Which of the 17 strategies have you observed in your own situation? '
            'How does naming them change how you feel about what is happening?</p>'
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '</div></div>'
        ),
        "part-3": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} Reflect</div>'
            '<p>Of the four wound levels, which feels most present for you right now? '
            'What would you say to a friend carrying the same wound?</p>'
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '</div></div>'
        ),
        "part-5": (
            '<div class="reflection-prompt">'
            f'<div class="reflection-prompt-label">{I["book"]} Reflect</div>'
            '<p>What does "inner freedom" mean to you? Where do you find your sense of '
            'self when every external source of validation has been stripped away?</p>'
            '<div class="reflection-lines">'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '<div class="reflection-line"></div>'
            '</div></div>'
        ),
    }
    for part_id, reflection_html in reflection_parts.items():
        html = html.replace(
            f'<section class="chapter-opener" id="{part_id}">',
            reflection_html + f'<section class="chapter-opener" id="{part_id}">'
        )

    # --- 45. SECTION SUMMARIES — Key sections ---
    # Summary after Part 4 survival framework
    summary_part4 = (
        '<div class="section-summary">'
        f'<div class="section-summary-label">{I["check"]} Section Summary</div>'
        '<ul>'
        '<li>Stabilise yourself first: sleep, movement, nutrition, professional support</li>'
        '<li>Build four pillars: PA-aware therapist, specialist lawyer, trusted friend, support group</li>'
        '<li>Focus energy on what you control; influence what you can; accept the rest</li>'
        '<li>Communicate using BIFF: Brief, Informative, Friendly, Firm</li>'
        '<li>Document everything with facts, not emotions</li>'
        '<li>Love unconditionally — your consistency is the path to reconnection</li>'
        '</ul>'
        '</div>'
    )
    html = html.replace(
        '<section class="chapter-opener" id="part-5">',
        summary_part4 + '<section class="chapter-opener" id="part-5">'
    )
    # Note: this replaces the previous Part 4 key-takeaways injection at part-5
    # Remove duplicate if exists (key-takeaways was already there)

    # --- 46. HIGHLIGHT BARS — Key principles throughout ---
    # Stockdale Paradox highlight
    highlight_stockdale = (
        '<div class="highlight-bar">'
        f'<p>{I["star"]} Unwavering faith that you will prevail — combined with '
        'brutal realism about how long it may take.</p>'
        '</div>'
    )
    html = html.replace(
        '<h3>The Stockdale Paradox</h3>',
        '<h3>The Stockdale Paradox</h3>' + highlight_stockdale
    )

    # --- 47. BREATHING PAUSE — After "Inner Freedom" ---
    breathing_inner = (
        '<div class="breathing-pause">'
        f'<div class="breathing-pause-title">{I["loving"]} A Moment of Stillness</div>'
        '<div class="breathing-steps">'
        'Close your eyes. Place one hand on your heart.<br>'
        '<strong>Say to yourself:</strong> "I am more than this situation. '
        'I am more than what any court or accusation says about me."<br>'
        'Breathe. Feel the truth of those words.'
        '</div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Inner Freedom</h2>)',
        # Inner Freedom already has a hero band, insert after it
        r'\1',
        html
    )
    # Insert breathing pause before the Viktor Frankl quote
    html = html.replace(
        '<p>This is not religious instruction.',
        breathing_inner + '<p>This is not religious instruction.'
    )

    # --- 48. END MARKS — At key section boundaries ---
    end_mark = '<div class="end-mark">\u25C6 \u25C6 \u25C6</div>'
    end_mark_sections = [
        "Love over exile",
        "A Final Word",
    ]
    for section_title in end_mark_sections:
        marker = f"<h3>{section_title}</h3>"
        pos = html.find(marker)
        if pos >= 0:
            # Find the end of this section (next h2 or h3 or chapter-opener)
            next_h2 = html.find('<h2', pos + len(marker))
            next_h3 = html.find('<h3', pos + len(marker))
            next_section = html.find('<section', pos + len(marker))
            next_divider = html.find('<div class="divider', pos + len(marker))
            candidates = [x for x in [next_h2, next_h3, next_section, next_divider] if x > 0]
            if candidates:
                insert_pos = min(candidates)
                html = html[:insert_pos] + end_mark + html[insert_pos:]

    # --- 49. ADDITIONAL DID YOU KNOW — In 17 Strategies section ---
    did_you_know_2 = (
        '<div class="did-you-know pattern-dots">'
        f'<div class="did-you-know-label">{I["brain"]} Did You Know?</div>'
        '<p>Dr. Amy Baker identified <strong>17 distinct strategies</strong> that '
        'alienating parents use. These map directly onto the Duluth Model\'s '
        'Power and Control Wheel — the same framework used to understand '
        'domestic violence.</p>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 17 Strategies of Erasure</h2>)',
        r'\1' + did_you_know_2,
        html
    )

    # --- 50. ADDITIONAL TESTIMONY CARD — In "Love over exile" ---
    testimony_2 = (
        '<div class="testimony-card">'
        '<div class="testimony-text">"After seven years of silence, my daughter called. '
        'She said: \'I always knew you loved me, Dad. I just couldn\'t say it.\' '
        'Those seven years of birthday cards and unanswered messages — they all mattered."</div>'
        '<div class="testimony-attribution">— Anonymous alienated father, '
        'reunited after 7 years</div>'
        '</div>'
    )
    html = html.replace(
        '<h3>Love over exile</h3>',
        '<h3>Love over exile</h3>' + testimony_2
    )

    # --- 51. EPIGRAPHS — Add to chapter openers via subtitle/text ---
    # Epigraph after Part 1 opener
    epigraph_p1 = (
        '<div class="epigraph">'
        '<p>"The truth, while suppressed, is rarely destroyed completely."</p>'
        '<cite>Dr. Amy Baker</cite>'
        '</div>'
    )
    # Insert before Part 1 first chapter heading
    html = html.replace(
        '<h2 id="ch-1">',
        epigraph_p1 + '<h2 id="ch-1">'
    )

    # Epigraph after Part 5 opener
    epigraph_p5 = (
        '<div class="epigraph">'
        '<p>"Everything can be taken from a person but one thing: the last of '
        'the human freedoms \u2014 to choose one\'s attitude in any given set '
        'of circumstances."</p>'
        '<cite>Viktor Frankl</cite>'
        '</div>'
    )
    # Find the close of part-5 opener
    p5_close = html.find('</section>', html.find('id="part-5"'))
    if p5_close >= 0:
        p5_close += len('</section>')
        # Find next h2
        next_h2_p5 = html.find('<h2', p5_close)
        if next_h2_p5 >= 0:
            html = html[:next_h2_p5] + epigraph_p5 + html[next_h2_p5:]

    # --- 52. ADDITIONAL DROP CAPS ---
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
            p_pos = html.find('<p>', pos + len(marker))
            if p_pos >= 0 and html[p_pos:p_pos + 20] != '<p class="drop-cap">':
                html = html[:p_pos] + '<p class="drop-cap">' + html[p_pos + 3:]

    # --- 53. NORMALISATION — After "Your Body Is Keeping Score" ---
    normalisation_body = (
        '<div class="normalisation">'
        '<p><strong>Your trauma responses are not character flaws.</strong> '
        'The hypervigilance, the intrusive thoughts, the emotional flashbacks — '
        'these are injury symptoms. They are your nervous system doing exactly '
        'what it was designed to do.</p>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Your Body Is Keeping Score</h2>)',
        r'\1' + normalisation_body,
        html
    )

    # --- 54. HIGHLIGHT BAR — "Consistent love is the strongest predictor" ---
    highlight_love = (
        '<div class="highlight-bar">'
        f'<p>{I["loving"]} Consistent, unconditional love is the strongest predictor '
        'of eventual reconnection. It is the most active, disciplined, and courageous '
        'choice available to you.</p>'
        '</div>'
    )
    html = html.replace(
        '<p>Consistent, unconditional love is the strongest predictor of eventual reconnection.',
        highlight_love
    )

    # =====================================================================
    #  MARKETING-STYLE FULL-PAGE COMPONENTS
    # =====================================================================

    # --- 55. STAT PAGE — "22 million" after "What the Data Shows" section ---
    stat_page_1 = (
        '<div class="stat-page">'
        '<div class="stat-number">22M</div>'
        '<div class="stat-label">Parents Affected by Alienation</div>'
        '<div class="stat-desc">An estimated 22 million adults in the US alone '
        'have experienced parental alienation — roughly one in six parents. '
        'Yet most have never heard the term.</div>'
        '<div class="stat-source">Harman, Kruk &amp; Hines, 2018</div>'
        '</div>'
    )
    # The heading is inside a hero-band div — use string find
    conflict_marker = 'It Is Not Conflict. It Is Abuse.</h2>'
    conflict_pos = html.find(conflict_marker)
    if conflict_pos >= 0:
        # Walk back to the start of the hero-band div
        band_start = html.rfind('<div class="hero-band', 0, conflict_pos)
        if band_start < 0:
            band_start = html.rfind('<h2', 0, conflict_pos)
        if band_start >= 0:
            html = html[:band_start] + stat_page_1 + html[band_start:]

    # --- 56. PHOTO OVERLAY PAGE — Before Part 3 (The Impact on You) ---
    photo_page_1 = (
        '<div class="photo-page">'
        f'<img src="{IMG_DIR / "surviving-parental-alienation.jpg"}" alt="">'
        '<div class="photo-overlay"></div>'
        '<div class="photo-content">'
        '<div class="photo-label">Part 3</div>'
        '<div class="photo-title">The Impact<br>on You</div>'
        '<div class="photo-text">What this experience does to your mind, body, '
        'identity, and spirit. Naming the wound is the first step to surviving it.</div>'
        '</div></div>'
    )
    html = re.sub(
        r'(<section class="chapter-opener" id="part-3">)',
        photo_page_1 + r'\1',
        html
    )

    # --- 57. ICON GRID — The Four Pillars (after "The Map for Survival") ---
    icon_grid_pillars = (
        '<div class="icon-grid">'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["health"]}</span>'
        '<div class="grid-title">Your Health</div>'
        '<div class="grid-desc">Protect your mental and physical wellbeing first</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["support"]}</span>'
        '<div class="grid-title">Your Team</div>'
        '<div class="grid-desc">Build a support network that understands</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["tactics"]}</span>'
        '<div class="grid-title">Your Tactics</div>'
        '<div class="grid-desc">Evidence-based strategies for the long haul</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["loving"]}</span>'
        '<div class="grid-title">Your Love</div>'
        '<div class="grid-desc">A new way of loving that endures distance</div></div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Pillar 1: Your Health and Safety</h2>)',
        icon_grid_pillars + r'\1',
        html
    )

    # --- 58. SPLIT LAYOUT — Before "The 10 Most Common Mistakes" ---
    split_mistakes = (
        '<div class="split-layout">'
        '<div class="split-sidebar">'
        '<div class="split-label">Warning</div>'
        '<div class="split-sidebar-title">The 10 Mistakes That Make It Worse</div>'
        '<div class="split-sidebar-text">Even loving parents can unknowingly '
        'sabotage their own case. These are the most common patterns — '
        'and how to avoid them.</div>'
        '</div>'
        '<div class="split-main">'
        '<div class="feature-list">'
        '<div class="feature-item"><div class="feature-num">01</div>'
        '<div class="feature-text"><strong>Badmouthing the other parent</strong>'
        '<p>Even when provoked — it gives the alienator ammunition</p></div></div>'
        '<div class="feature-item"><div class="feature-num">02</div>'
        '<div class="feature-text"><strong>Trying to force contact</strong>'
        '<p>Pressure pushes the child further away</p></div></div>'
        '<div class="feature-item"><div class="feature-num">03</div>'
        '<div class="feature-text"><strong>Giving up too soon</strong>'
        '<p>Withdrawal is interpreted as proof you never cared</p></div></div>'
        '<div class="feature-item"><div class="feature-num">04</div>'
        '<div class="feature-text"><strong>Relying on the court alone</strong>'
        '<p>Legal systems were not designed for this kind of abuse</p></div></div>'
        '<div class="feature-item"><div class="feature-num">05</div>'
        '<div class="feature-text"><strong>Isolating yourself</strong>'
        '<p>Silence and shame are the alienator\'s greatest allies</p></div></div>'
        '</div></div></div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The 10 Most Common Mistakes</h2>)',
        split_mistakes + r'\1',
        html
    )

    # --- 59. FULL-WIDTH QUOTE PAGE — Viktor Frankl (before Part 5) ---
    quote_page = (
        '<div class="quote-page">'
        '<div class="quote-mark">\u201C</div>'
        '<div class="quote-text">Everything can be taken from a person but one '
        'thing: the last of the human freedoms \u2014 to choose one\u2019s attitude '
        'in any given set of circumstances.</div>'
        '<div class="quote-author">Viktor Frankl</div>'
        '</div>'
    )
    html = re.sub(
        r'(<section class="chapter-opener" id="part-5">)',
        quote_page + r'\1',
        html
    )

    # --- 60. STAT PAGE — "82%" before "The Sleeper Effect" ---
    stat_page_2 = (
        '<div class="stat-page">'
        '<div class="stat-number">82%</div>'
        '<div class="stat-label">Of Alienated Children Eventually Seek Reconnection</div>'
        '<div class="stat-desc">Research consistently shows that the vast majority of '
        'alienated children, once they reach adulthood, begin to question the false '
        'narrative and seek out the rejected parent.</div>'
        '<div class="stat-source">Baker &amp; Ben-Ami, 2011</div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">The Sleeper Effect</h2>)',
        stat_page_2 + r'\1',
        html
    )

    # --- 61. PHOTO OVERLAY PAGE — Before Part 6 (You Are Not Alone) ---
    photo_page_2 = (
        '<div class="photo-page">'
        f'<img src="{IMG_DIR / "community-help-for-alienated-parents.jpg"}" alt="">'
        '<div class="photo-overlay"></div>'
        '<div class="photo-content">'
        '<div class="photo-label">Part 6</div>'
        '<div class="photo-title">You Are<br>Not Alone</div>'
        '<div class="photo-text">There is a growing community of parents who understand '
        'exactly what you are going through. Connection is survival.</div>'
        '</div></div>'
    )
    html = re.sub(
        r'(<section class="chapter-opener" id="part-6">)',
        photo_page_2 + r'\1',
        html
    )

    # --- 62. ICON GRID — Six Steps of Resilience ---
    icon_grid_resilience = (
        '<div class="icon-grid">'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["shield"]}</span>'
        '<div class="grid-title">Accept Reality</div>'
        '<div class="grid-desc">Acknowledge what you cannot control</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["brain"]}</span>'
        '<div class="grid-title">Reframe Meaning</div>'
        '<div class="grid-desc">Find purpose beyond the pain</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["support"]}</span>'
        '<div class="grid-title">Build Connection</div>'
        '<div class="grid-desc">You cannot do this alone</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["health"]}</span>'
        '<div class="grid-title">Protect Yourself</div>'
        '<div class="grid-desc">Physical and mental health are non-negotiable</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["star"]}</span>'
        '<div class="grid-title">Practise Hope</div>'
        '<div class="grid-desc">Hope is a discipline, not a feeling</div></div>'
        f'<div class="icon-grid-item"><span class="grid-icon">{I["loving"]}</span>'
        '<div class="grid-title">Keep Loving</div>'
        '<div class="grid-desc">Love that endures is the ultimate act of courage</div></div>'
        '</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Self-Compassion Is Not Optional</h2>)',
        icon_grid_resilience + r'\1',
        html
    )

    # --- 63. COLOUR BAND DIVIDERS — Before part openers ---
    for part_id in ["part-4", "part-5"]:
        marker = f'id="{part_id}"'
        pos = html.find(marker)
        if pos >= 0:
            section_start = html.rfind('<section', 0, pos)
            if section_start >= 0:
                html = (html[:section_start]
                        + '<div class="colour-band"></div>'
                        + html[section_start:])

    # --- 64. PROGRESS TRACKER — Visual journey map at "What This Guide Covers" ---
    progress_tracker = (
        '<div class="progress-tracker">'
        '<div class="progress-track-bar">'
        '<div class="progress-track-fill"></div>'
        '</div>'
        '<div class="progress-nodes">'
        '<div class="progress-node progress-node-active">'
        '<div class="progress-dot"></div>'
        '<div class="progress-label">You Are<br>Here</div></div>'
        '<div class="progress-node">'
        '<div class="progress-dot"></div>'
        '<div class="progress-label">Understand</div></div>'
        '<div class="progress-node">'
        '<div class="progress-dot"></div>'
        '<div class="progress-label">Survive</div></div>'
        '<div class="progress-node">'
        '<div class="progress-dot"></div>'
        '<div class="progress-label">Endure</div></div>'
        '<div class="progress-node">'
        '<div class="progress-dot"></div>'
        '<div class="progress-label">Inner<br>Freedom</div></div>'
        '</div></div>'
    )
    html = html.replace(
        '<h3>The non-negotiables</h3>',
        progress_tracker + '<h3>The non-negotiables</h3>'
    )

    # --- 65. KEY PRINCIPLE CARD — "Name the wound" at Part 3 ---
    key_principle = (
        f'<div class="key-principle">'
        f'<div class="key-principle-icon">{I["insight"]}</div>'
        f'<div class="key-principle-text">'
        f'<strong>Naming the wound is the first step to surviving it.</strong> '
        f'When you can identify what is happening to you — clinically, precisely — '
        f'the chaos begins to resolve into something you can understand and fight.</div>'
        f'</div>'
    )
    html = re.sub(
        r'(<h2 id="ch-\d+">Ambiguous Loss and Disenfranchised Grief</h2>)',
        key_principle + r'\1',
        html
    )

    # --- 67. TWO-COLUMN REFERENCE — Wrap Part 6 resources section ---
    # Find "Community and Support" h2 and wrap the next paragraphs in columns
    community_marker = '>Community and Support</h2>'
    community_pos = html.find(community_marker)
    if community_pos >= 0:
        # Find the 3rd <h3> after this section to wrap the resource lists
        h3_count = 0
        search_pos = community_pos + len(community_marker)
        first_h3 = None
        for _ in range(20):
            next_h3 = html.find('<h3>', search_pos)
            if next_h3 < 0:
                break
            h3_count += 1
            if h3_count == 2:
                first_h3 = next_h3
            if h3_count == 4:
                # Wrap from the 2nd h3 to here in reference-columns
                html = (html[:first_h3]
                        + '<div class="reference-columns">'
                        + html[first_h3:next_h3]
                        + '</div>'
                        + html[next_h3:])
                break
            search_pos = next_h3 + 4

    # --- 68. ANGLED SECTION — "The Cast of Characters" ---
    html = re.sub(
        r'(<h2 id="ch-\d+">The Cast of Characters</h2>)',
        '<div class="angled-section-teal">'
        r'\1',
        html
    )
    # Close after 2 paragraphs
    cast_marker = '>The Cast of Characters</h2>'
    cast_pos = html.find(cast_marker)
    if cast_pos >= 0:
        close_pos = cast_pos
        for _ in range(3):
            next_p = html.find('</p>', close_pos + 1)
            if next_p >= 0:
                close_pos = next_p
        if close_pos > cast_pos:
            html = html[:close_pos + 4] + '</div>' + html[close_pos + 4:]

    # --- 69. ASYMMETRIC GRID — For "The Four Pillars of Support" icon blocks ---
    # Wrap the icon blocks in a grid-12 layout for better visual rhythm
    pillars_marker = '>The Four Pillars of Support</h3></div>'
    pillars_pos = html.find(pillars_marker)
    if pillars_pos >= 0:
        # The icon blocks immediately follow — wrap in a grid
        blocks_start = pillars_pos + len(pillars_marker)
        # Find the 4th icon-block closing div
        block_count = 0
        search = blocks_start
        for _ in range(20):
            next_block = html.find('</div></div>', search)
            if next_block < 0:
                break
            block_count += 1
            if block_count == 4:
                blocks_end = next_block + len('</div></div>')
                html = (html[:blocks_start]
                        + '<div class="grid-12">'
                        + html[blocks_start:blocks_end]
                        + '</div>'
                        + html[blocks_end:])
                break
            search = next_block + 12

    # --- 66. STAT PAGE — "69-81%" before Part 6 ---
    stat_page_3 = (
        '<div class="stat-page">'
        '<div class="stat-number">69–81%</div>'
        '<div class="stat-label">Of Estrangements Are Not Permanent</div>'
        '<div class="stat-desc">The research consistently shows that most alienated '
        'children eventually question the false narrative. Your consistency today '
        'is building the bridge they will one day cross.</div>'
        '<div class="stat-source">Pillemer, 2020</div>'
        '</div>'
    )
    html = re.sub(
        r'(<section class="chapter-opener" id="part-6">)',
        stat_page_3 + r'\1',
        html
    )

    return html


def build_toc_html(toc_entries: list[dict]) -> str:
    """Build auto-generated TOC with page numbers using target-counter()."""
    items = []
    for entry in toc_entries:
        css_class = "toc-part" if entry["type"] == "part" else "toc-chapter"
        items.append(
            f'<li class="{css_class}">'
            f'<a href="#{entry["id"]}">{entry["title"]}</a>'
            f"</li>"
        )

    return f"""<nav class="toc">
  <h2>Contents</h2>
  <ul class="toc-auto">
    {"".join(items)}
  </ul>
</nav>"""


def render_table(rows: list) -> str:
    """Render markdown table rows as HTML with clean semantic markup."""
    html = '<table>'
    for idx, row in enumerate(rows):
        cells = [c.strip() for c in row.strip("|").split("|")]
        if idx == 0:
            html += "<thead><tr>"
            for cell in cells:
                html += f'<th>{process_inline(cell)}</th>'
            html += "</tr></thead><tbody>"
        elif idx == 1 and all(c.strip().replace("-", "") == "" for c in cells):
            continue  # Skip separator row
        else:
            html += "<tr>"
            for cell in cells:
                html += f'<td>{process_inline(cell)}</td>'
            html += "</tr>"
    html += "</tbody></table>"
    return html


def process_inline(text: str) -> str:
    """Process inline markdown: bold, italic, links."""
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def build_html(content_html: str, toc_html: str) -> str:
    """Wrap content in full HTML document with cover, TOC, and back cover."""
    # Check for cover artwork (prefer v2 photo-tear, fall back to v1)
    cover_img_path = DESIGN_IMG_DIR / "cover-artwork-v2.jpg"
    if not cover_img_path.exists():
        cover_img_path = DESIGN_IMG_DIR / "cover-artwork.jpg"
    cover_image_html = ""
    cover_overlay_html = ""
    if cover_img_path.exists():
        cover_image_html = f'<img class="cover-image" src="{cover_img_path}" alt="">'
        cover_overlay_html = '<div class="cover-overlay"></div>'

    # Logo
    logo_path = DESIGN_IMG_DIR / "logo.png"
    logo_html = ""
    if logo_path.exists():
        logo_html = f'<img class="cover-logo" src="{logo_path}" alt="Love Over Exile">'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="{CSS_PATH}">
<style>
  /* Additional inline styles for content flow */
  .disclaimer {{
    page: clean;
    break-before: page;
    padding-top: 30mm;
    text-align: center;
  }}
  .disclaimer p {{
    font-size: 9.5pt;
    color: var(--text-light);
    line-height: 1.7;
    max-width: 130mm;
    margin: 0 auto;
  }}
  .disclaimer h2 {{
    font-size: 14pt;
    color: var(--sage);
    font-weight: 400;
    margin-bottom: 1.5em;
  }}

  /* Table styling */
  table {{ break-inside: avoid; }}

  /* Ensure diagrams don't break across pages */
  .model-diagram {{ break-inside: avoid; page-break-inside: avoid; }}

  /* Content section wrapper */
  .content-section {{
    break-before: page;
  }}

  /* Numbered items spacing */
  .numbered-item + .numbered-item {{
    margin-top: 2mm;
  }}
</style>
</head>
<body>

<!-- ====== COVER ====== -->
<section class="cover">
  <div class="cover-accent"></div>
  {logo_html}
  {cover_image_html}
  {cover_overlay_html}
  <div class="cover-content">
    <div class="cover-badge">Free Guide</div>
    <h1 class="cover-title">The Survival Guide<br>for Alienated Parents</h1>
    <p class="cover-subtitle">Understanding What Is Happening to You &mdash; And How to Endure It</p>
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
    <div style="width:100%;height:100%;background:linear-gradient(135deg,var(--teal),var(--teal-dark));display:flex;align-items:center;justify-content:center;font-family:var(--font-heading);font-size:24pt;color:var(--gold);font-weight:700;">MS</div>
  </div>
  <div class="bio-name">Malcolm Smith</div>
  <div class="bio-tagline">Author &bull; Advocate &bull; Alienated Father</div>
  <div class="bio-text">
    <p>Malcolm Smith is the founder of Love Over Exile, a platform dedicated to supporting alienated parents through research-based guidance and lived experience. After more than a decade navigating parental alienation firsthand, he created the resources he wished had existed at the beginning of his own journey.</p>
    <p>His work draws on the research of the world&rsquo;s leading experts in parental alienation, coercive control, attachment, and trauma &mdash; translated into plain language for parents in crisis.</p>
    <p>Malcolm lives in the Netherlands and continues to advocate for greater recognition of parental alienation as a form of family violence.</p>
  </div>
  <div class="bio-links">
    <span class="bio-link">loveoverexile.com</span>
  </div>
</section>

<!-- ====== BACK COVER ====== -->
<section class="back-cover">
  <p class="back-quote">&ldquo;The truth, while suppressed, is rarely destroyed completely.&rdquo;</p>
  <cite>&mdash; Dr. Amy Baker</cite>
  <div class="back-title">Love Over Exile</div>
  <p class="back-desc">Bearing the Unbearable &mdash; A Guide for Alienated Parents, Turning Tragedy into Inner Freedom</p>
  <p class="back-author">Malcolm Smith</p>
  <p class="back-url">loveoverexile.com</p>
</section>

</body>
</html>"""


def main():
    print("Reading markdown...")
    md_text = MD_PATH.read_text(encoding="utf-8")

    print("Converting to HTML...")
    content_html, toc_entries = md_to_html(md_text)

    print(f"Building TOC ({len(toc_entries)} entries)...")
    toc_html = build_toc_html(toc_entries)

    print("Post-processing: injecting layout components...")
    content_html = post_process_html(content_html)

    print("Building full document...")
    full_html = build_html(content_html, toc_html)

    print(f"Writing HTML to {HTML_PATH}...")
    HTML_PATH.write_text(full_html, encoding="utf-8")

    print(f"Generating PDF with WeasyPrint...")
    result = subprocess.run(
        ["weasyprint", str(HTML_PATH), str(PDF_PATH)],
        capture_output=True,
        text=True,
        cwd=str(HERE),
    )

    if result.returncode != 0:
        print(f"WeasyPrint stderr:\n{result.stderr}")
        sys.exit(1)

    if result.stderr:
        # Show warnings but don't fail
        warnings = [l for l in result.stderr.split("\n") if l.strip()]
        if warnings:
            print(f"WeasyPrint warnings ({len(warnings)}):")
            for w in warnings[:5]:
                print(f"  {w}")
            if len(warnings) > 5:
                print(f"  ... and {len(warnings) - 5} more")

    print(f"PDF generated: {PDF_PATH}")
    print(f"Size: {PDF_PATH.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
