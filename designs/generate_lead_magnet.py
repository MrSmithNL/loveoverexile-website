#!/usr/bin/env python3
"""Generate a short marketing-style lead magnet PDF using Playwright.

This demonstrates the full-CSS pipeline: clip-path, box-shadow,
backdrop-filter, text-shadow, blend-mode — everything WeasyPrint can't do.

Output: lead-magnet.pdf (A4, ~8 pages)
"""

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
IMG_DIR = HERE.parent / "site" / "public" / "images"
DESIGN_IMG_DIR = HERE / "images"
HTML_PATH = HERE / "lead-magnet.html"
PDF_PATH = HERE / "lead-magnet.pdf"

# Font Awesome 6 solid codepoints
FA = {
    "heart": "\uf004",
    "shield": "\uf3ed",
    "brain": "\uf5dc",
    "users": "\uf0c0",
    "star": "\uf005",
    "check": "\uf00c",
    "warning": "\uf071",
    "book": "\uf02d",
    "lightbulb": "\uf0eb",
    "arrow": "\uf061",
}

# Brand colours
TEAL = "#0C5E5D"
TEAL_DARK = "#074443"
AMBER = "#E2480C"
GOLD = "#D4910A"
CREAM = "#F8F4EF"
WHITE = "#FFFFFF"

FONT_DIR = HERE / "fonts"


def build_html() -> str:
    """Build the complete lead magnet HTML with inline CSS."""

    cover_img = DESIGN_IMG_DIR / "cover-artwork-v2.jpg"
    community_img = IMG_DIR / "community-help-for-alienated-parents.jpg"
    landscape_img = IMG_DIR / "parental-alienation-landscape.png"
    wound_img = DESIGN_IMG_DIR / "section-wound.jpg"
    logo_img = DESIGN_IMG_DIR / "logo.png"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
/* ===== FONTS ===== */
@font-face {{
  font-family: 'Lora';
  font-weight: 400;
  src: url('file://{FONT_DIR}/Lora-Regular.ttf');
}}
@font-face {{
  font-family: 'Lora';
  font-weight: 700;
  src: url('file://{FONT_DIR}/Lora-Bold.ttf');
}}
@font-face {{
  font-family: 'Lora';
  font-weight: 400;
  font-style: italic;
  src: url('file://{FONT_DIR}/Lora-Italic.ttf');
}}
@font-face {{
  font-family: 'Inter';
  font-weight: 400;
  src: url('file://{FONT_DIR}/Inter-Regular.ttf');
}}
@font-face {{
  font-family: 'Inter';
  font-weight: 700;
  src: url('file://{FONT_DIR}/Inter-Bold.ttf');
}}
@font-face {{
  font-family: 'FA6Solid';
  font-weight: 900;
  src: url('file://{FONT_DIR}/fa-solid-900.ttf');
}}

/* ===== DESIGN TOKENS — 3-LAYER ARCHITECTURE ===== */

/* Layer 1: Primitives — raw brand values */
@layer primitives {{
  :root {{
    /* Colours */
    --color-teal-600: {TEAL};
    --color-teal-800: {TEAL_DARK};
    --color-amber-600: {AMBER};
    --color-gold-500: {GOLD};
    --color-cream-50: {CREAM};
    --color-white: {WHITE};
    --color-charcoal: #2C2C2C;
    --color-grey-600: #4A4A4A;

    /* Typography */
    --font-serif: 'Lora', Georgia, serif;
    --font-sans: 'Inter', 'Helvetica Neue', sans-serif;
    --font-icon: 'FA6Solid';
    --font-size-xs: 8pt;
    --font-size-sm: 9pt;
    --font-size-base: 11pt;
    --font-size-md: 13pt;
    --font-size-lg: 22pt;
    --font-size-xl: 26pt;
    --font-size-2xl: 30pt;
    --font-size-3xl: 42pt;
    --font-size-hero: 56pt;
    --font-size-display: 72pt;
    --font-size-icon-sm: 18pt;
    --font-size-icon-lg: 36pt;
    --font-size-quote-mark: 80pt;

    /* Spacing */
    --space-2: 2mm;
    --space-4: 4mm;
    --space-5: 5mm;
    --space-6: 6mm;
    --space-8: 8mm;
    --space-10: 10mm;
    --space-12: 12mm;
    --space-15: 15mm;
    --space-18: 18mm;
    --space-20: 20mm;
    --space-25: 25mm;
    --space-30: 30mm;
    --space-35: 35mm;
    --space-40: 40mm;
    --space-50: 50mm;

    /* Borders & Radii */
    --radius-sm: 2mm;
    --radius-md: 3mm;
    --radius-lg: 4mm;
    --border-accent: 3mm;

    /* Line heights */
    --leading-tight: 1.1;
    --leading-snug: 1.2;
    --leading-normal: 1.6;
    --leading-relaxed: 1.65;
    --leading-loose: 1.7;

    /* Letter spacing */
    --tracking-wide: 2pt;
    --tracking-wider: 3pt;
  }}
}}

/* Layer 2: Semantic tokens — purpose-based */
@layer semantic {{
  :root {{
    --color-primary: var(--color-teal-600);
    --color-primary-dark: var(--color-teal-800);
    --color-accent: var(--color-amber-600);
    --color-highlight: var(--color-gold-500);
    --color-surface: var(--color-cream-50);
    --color-surface-white: var(--color-white);
    --color-text: var(--color-charcoal);
    --color-text-muted: var(--color-grey-600);

    /* Derived colours using color-mix() */
    --color-primary-soft: color-mix(in srgb, var(--color-primary) 15%, white);
    --color-primary-overlay-light: color-mix(in srgb, var(--color-primary-dark) 10%, transparent);
    --color-primary-overlay-medium: color-mix(in srgb, var(--color-primary-dark) 60%, transparent);
    --color-primary-overlay-heavy: color-mix(in srgb, var(--color-primary-dark) 95%, transparent);
    --color-accent-glow: color-mix(in srgb, var(--color-accent) 40%, transparent);
    --color-text-on-dark: var(--color-white);
    --color-text-on-dark-muted: color-mix(in srgb, white 80%, transparent);
    --color-text-on-dark-subtle: color-mix(in srgb, white 75%, transparent);
    --color-highlight-subtle: color-mix(in srgb, var(--color-highlight) 15%, transparent);
    --color-highlight-faint: color-mix(in srgb, var(--color-highlight) 8%, transparent);

    --font-heading: var(--font-serif);
    --font-body: var(--font-sans);
    --text-body: var(--font-size-base);
    --text-body-large: var(--font-size-md);
    --text-label: var(--font-size-xs);
    --text-small: var(--font-size-sm);

    --shadow-soft: 0 1mm 4mm rgba(0,0,0,0.05);
    --shadow-card: 0 2mm 10mm rgba(0,0,0,0.06);
    --shadow-elevated: 0 2mm 6mm rgba(0,0,0,0.3);
    --shadow-deep: 0 3mm 12mm rgba(0,0,0,0.4);
  }}
}}

/* Layer 3: Component tokens — element-specific */
@layer components {{
  :root {{
    /* Cover */
    --cover-bg: var(--color-primary-dark);
    --cover-title-size: var(--font-size-3xl);
    --cover-subtitle-size: var(--font-size-md);

    /* Key point callout */
    --callout-bg: linear-gradient(135deg, var(--color-surface), color-mix(in srgb, var(--color-primary) 12%, white));
    --callout-border: var(--color-primary);
    --callout-border-width: var(--border-accent);
    --callout-radius: 0 var(--radius-md) var(--radius-md) 0;
    --callout-text-color: var(--color-primary-dark);

    /* Stat card */
    --stat-number-color: var(--color-primary);
    --stat-number-size: var(--font-size-hero);

    /* Feature card */
    --feature-bg: var(--color-surface);
    --feature-icon-color: var(--color-primary);
    --feature-title-color: var(--color-primary-dark);

    /* CTA button */
    --cta-bg: var(--color-accent);
    --cta-shadow: 0 3mm 12mm var(--color-accent-glow);
    --cta-radius: var(--radius-md);

    /* Thing header (content pages) */
    --thing-header-bg: var(--color-primary);
    --thing-header-clip: polygon(0 0, 100% 0, 100% 85%, 0 100%);
    --thing-number-opacity: 0.12;
    --thing-label-color: var(--color-highlight);
  }}
}}

/* ===== PAGE SETUP ===== */
@page {{
  size: A4;
  margin: 0;
}}

* {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

body {{
  font-family: var(--font-body);
  font-size: var(--text-body);
  line-height: var(--leading-normal);
  color: var(--color-text);
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  orphans: 3;
  widows: 3;
}}

/* ===== SHARED UTILITIES ===== */
.page {{
  width: 210mm;
  height: 297mm;
  position: relative;
  overflow: hidden;
  break-after: page;
  break-inside: avoid;
}}

.icon {{
  font-family: var(--font-icon);
  font-weight: 900;
}}

/* ===== PAGE 1: COVER ===== */
.cover {{
  background: var(--cover-bg);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0;
}}

.cover-bg {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.35;
  mix-blend-mode: luminosity;
}}

.cover-gradient {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: linear-gradient(
    180deg,
    var(--color-primary-overlay-light) 0%,
    var(--color-primary-overlay-medium) 40%,
    var(--color-primary-overlay-heavy) 70%
  );
}}

.cover-content {{
  position: relative;
  z-index: 2;
  padding: 0 var(--space-40) var(--space-50) var(--space-35);
  color: var(--color-text-on-dark);
}}

.cover-badge {{
  display: inline-block;
  background: var(--color-accent);
  color: var(--color-text-on-dark);
  font-size: var(--text-label);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  padding: var(--space-2) var(--space-5);
  border-radius: var(--radius-sm);
  margin-bottom: var(--space-8);
  box-shadow: var(--shadow-elevated);
}}

.cover-title {{
  font-family: var(--font-heading);
  font-size: var(--cover-title-size);
  font-weight: 700;
  line-height: var(--leading-tight);
  margin-bottom: var(--space-6);
  text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}}

.cover-subtitle {{
  font-size: var(--cover-subtitle-size);
  color: var(--color-text-on-dark-muted);
  max-width: 130mm;
  line-height: 1.5;
  margin-bottom: var(--space-10);
}}

.cover-rule {{
  width: 40mm;
  height: 1mm;
  background: var(--color-highlight);
  margin-bottom: var(--space-6);
}}

.cover-author {{
  font-size: 10pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  color: var(--color-highlight);
}}

.cover-logo {{
  position: absolute;
  top: var(--space-20);
  left: var(--space-30);
  height: var(--space-18);
  z-index: 3;
  filter: brightness(10);
}}

/* ===== PAGE 2: INTRO / WHY THIS MATTERS ===== */
.intro-page {{
  background: var(--color-surface);
  display: flex;
}}

.intro-sidebar {{
  width: 75mm;
  background: var(--color-primary);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--space-30) var(--space-12) var(--space-30) var(--space-18);
  color: var(--color-text-on-dark);
  position: relative;
}}

.intro-sidebar::after {{
  content: '';
  position: absolute;
  right: -20mm;
  top: 0;
  width: 40mm;
  height: 100%;
  background: var(--color-primary);
  clip-path: polygon(0 0, 50% 0, 100% 100%, 0 100%);
}}

.intro-sidebar .sidebar-label {{
  font-size: var(--text-label);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-highlight);
  margin-bottom: var(--space-6);
}}

.intro-sidebar h2 {{
  font-family: var(--font-heading);
  font-size: var(--font-size-lg);
  font-weight: 700;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-6);
}}

.intro-sidebar p {{
  font-size: var(--text-small);
  line-height: var(--leading-normal);
  color: var(--color-text-on-dark-subtle);
}}

.intro-main {{
  flex: 1;
  padding: var(--space-35) var(--space-25) var(--space-30) var(--space-30);
  display: flex;
  flex-direction: column;
  justify-content: center;
}}

.intro-main .big-stat {{
  text-align: center;
  margin-bottom: var(--space-10);
  padding: var(--space-8);
  background: var(--color-surface-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}}

.intro-main .big-stat .number {{
  font-family: var(--font-heading);
  font-size: var(--stat-number-size);
  font-weight: 700;
  color: var(--stat-number-color);
  line-height: 1;
}}

.intro-main .big-stat .label {{
  font-size: 10pt;
  color: var(--color-text-muted);
  margin-top: var(--space-2);
}}

.intro-main p {{
  font-size: 10pt;
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-4);
}}

/* ===== PAGE 3-7: CONTENT PAGES (5 Things) ===== */
.thing-page {{
  background: var(--color-surface-white);
  padding: 0;
  display: flex;
  flex-direction: column;
}}

.thing-header {{
  background: var(--thing-header-bg);
  padding: var(--space-25) var(--space-30) var(--space-20) var(--space-30);
  color: var(--color-text-on-dark);
  position: relative;
  clip-path: var(--thing-header-clip);
  min-height: 90mm;
}}

.thing-header .thing-number {{
  font-family: var(--font-heading);
  font-size: var(--font-size-display);
  font-weight: 700;
  color: rgba(255,255,255, var(--thing-number-opacity));
  position: absolute;
  top: var(--space-15);
  right: var(--space-30);
  line-height: 1;
}}

.thing-header .thing-label {{
  font-size: var(--text-label);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--thing-label-color);
  margin-bottom: var(--space-4);
}}

.thing-header h2 {{
  font-family: var(--font-heading);
  font-size: var(--font-size-xl);
  font-weight: 700;
  line-height: var(--leading-snug);
  max-width: 130mm;
}}

.thing-body {{
  flex: 1;
  padding: var(--space-15) var(--space-30) var(--space-25) var(--space-30);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}}

.thing-body p {{
  font-size: 10.5pt;
  line-height: var(--leading-loose);
  margin-bottom: var(--space-5);
}}

.thing-body .key-point {{
  background: var(--callout-bg);
  border-left: var(--callout-border-width) solid var(--callout-border);
  padding: var(--space-6) var(--space-8);
  margin: var(--space-6) 0;
  border-radius: var(--callout-radius);
  box-shadow: var(--shadow-soft);
  break-inside: avoid;
}}

.thing-body .key-point p {{
  margin: 0;
  font-weight: 700;
  color: var(--callout-text-color);
}}

/* Alternate teal/white backgrounds for variety */
.thing-page.alt .thing-header {{
  background: var(--color-accent);
}}

.thing-page.gold .thing-header {{
  background: linear-gradient(135deg, var(--color-primary-dark), var(--color-primary));
}}

/* ===== PAGE 3 SPECIAL: IMAGE BACKGROUND ===== */
.thing-page.with-image .thing-header {{
  min-height: 110mm;
  clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%);
}}

.thing-page.with-image .thing-header img {{
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.2;
  mix-blend-mode: overlay;
}}

/* ===== PAGE 6: QUOTE PAGE ===== */
.quote-spread {{
  background: var(--color-primary-dark);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--space-50) var(--space-40);
  color: var(--color-text-on-dark);
}}

.quote-spread .deco-circle {{
  position: absolute;
  width: 120mm;
  height: 120mm;
  border-radius: 50%;
  border: 1px solid var(--color-highlight-subtle);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}}

.quote-spread .deco-circle-2 {{
  position: absolute;
  width: 160mm;
  height: 160mm;
  border-radius: 50%;
  border: 1px solid var(--color-highlight-faint);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}}

.quote-spread .quote-mark {{
  font-family: var(--font-heading);
  font-size: var(--font-size-quote-mark);
  color: var(--color-highlight);
  line-height: 0.5;
  margin-bottom: var(--space-10);
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  position: relative;
  z-index: 2;
}}

.quote-spread .quote-text {{
  font-family: var(--font-heading);
  font-size: 24pt;
  font-style: italic;
  font-weight: 400;
  line-height: 1.4;
  max-width: 130mm;
  margin-bottom: var(--space-10);
  position: relative;
  z-index: 2;
  text-shadow: 0 1px 6px rgba(0,0,0,0.2);
}}

.quote-spread .quote-author {{
  font-size: 10pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-highlight);
  position: relative;
  z-index: 2;
}}

.quote-spread .quote-rule {{
  width: 30mm;
  height: 0.5mm;
  background: var(--color-highlight);
  margin: 0 auto var(--space-5) auto;
  position: relative;
  z-index: 2;
}}

/* ===== PAGE 8: CTA / BACK COVER ===== */
.cta-page {{
  background: linear-gradient(160deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--space-40);
  color: var(--color-text-on-dark);
}}

.cta-page .cta-icon {{
  font-family: var(--font-icon);
  font-weight: 900;
  font-size: var(--font-size-icon-lg);
  color: var(--color-highlight);
  margin-bottom: var(--space-8);
}}

.cta-page h2 {{
  font-family: var(--font-heading);
  font-size: var(--font-size-2xl);
  font-weight: 700;
  line-height: var(--leading-snug);
  margin-bottom: var(--space-8);
}}

.cta-page p {{
  font-size: 12pt;
  line-height: var(--leading-normal);
  color: var(--color-text-on-dark-muted);
  max-width: 120mm;
  margin-bottom: var(--space-10);
}}

.cta-button {{
  display: inline-block;
  background: var(--cta-bg);
  color: var(--color-text-on-dark);
  font-size: var(--text-body);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  padding: var(--space-5) var(--space-12);
  border-radius: var(--cta-radius);
  text-decoration: none;
  box-shadow: var(--cta-shadow);
}}

.cta-page .cta-url {{
  font-size: 10pt;
  color: var(--color-highlight);
  margin-top: var(--space-6);
  font-weight: 700;
  letter-spacing: 1pt;
}}

.cta-page .cta-logo {{
  position: absolute;
  bottom: var(--space-25);
  height: 14mm;
  filter: brightness(10);
}}

/* ===== ICON FEATURES GRID ===== */
.features-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
  margin: var(--space-6) 0;
}}

.feature-card {{
  background: var(--feature-bg);
  border-radius: var(--radius-md);
  padding: var(--space-5) var(--space-6);
  box-shadow: 0 1mm 3mm rgba(0,0,0,0.04);
  break-inside: avoid;
  container-type: inline-size;
}}

.feature-card .feat-icon {{
  font-family: var(--font-icon);
  font-weight: 900;
  font-size: var(--font-size-icon-sm);
  color: var(--feature-icon-color);
  margin-bottom: var(--space-2);
}}

.feature-card .feat-title {{
  font-weight: 700;
  font-size: 9.5pt;
  color: var(--feature-title-color);
  margin-bottom: 1mm;
}}

.feature-card .feat-desc {{
  font-size: 8.5pt;
  color: var(--color-text-muted);
  line-height: 1.45;
}}

/* ===== CONDITIONAL STYLES WITH :has() ===== */
/* When a page has a key-point as last child, add bottom breathing room */
.thing-body:has(> .key-point:last-child) {{
  padding-bottom: var(--space-30);
}}

/* When feature grid is inside intro, tighten spacing */
.intro-main:has(.features-grid) p {{
  margin-bottom: var(--space-2);
}}

</style>
</head>
<body>

<!-- ===== PAGE 1: COVER ===== -->
<div class="page cover">
  <img class="cover-bg" src="file://{cover_img}" alt="">
  <div class="cover-gradient"></div>
  <img class="cover-logo" src="file://{logo_img}" alt="Love Over Exile">
  <div class="cover-content">
    <div class="cover-badge">Free Guide</div>
    <h1 class="cover-title">5 Things Every<br>Alienated Parent<br>Needs to Know</h1>
    <p class="cover-subtitle">The essential truths that will change how you understand what is happening to you and your child.</p>
    <div class="cover-rule"></div>
    <p class="cover-author">Malcolm Smith</p>
  </div>
</div>

<!-- ===== PAGE 2: INTRO ===== -->
<div class="page intro-page">
  <div class="intro-sidebar">
    <div class="sidebar-label">Why This Matters</div>
    <h2>You Are Living Through an Invisible Crisis</h2>
    <p>Parental alienation is one of the most devastating experiences a person can endure — yet most people have never heard the term. This guide gives you the five most important things to understand right now.</p>
  </div>
  <div class="intro-main">
    <div class="big-stat">
      <div class="number">22M</div>
      <div class="label">adults in the US have experienced parental alienation</div>
    </div>
    <p>That is roughly <strong>one in six parents</strong>. Yet despite its scale, parental alienation remains largely invisible — to the public, to mental health professionals, and to the courts.</p>
    <p>The research is clear: this is not a custody dispute. It is a form of <strong>psychological abuse</strong> that damages both parent and child.</p>
    <div class="features-grid">
      <div class="feature-card">
        <div class="feat-icon">{FA["brain"]}</div>
        <div class="feat-title">Psychological Impact</div>
        <div class="feat-desc">PTSD, depression, and complex grief affect the majority of alienated parents</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">{FA["shield"]}</div>
        <div class="feat-title">It Has a Name</div>
        <div class="feat-desc">Recognised by researchers worldwide as a distinct form of family violence</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">{FA["users"]}</div>
        <div class="feat-title">You Are Not Alone</div>
        <div class="feat-desc">A growing community of parents understands exactly what you face</div>
      </div>
      <div class="feature-card">
        <div class="feat-icon">{FA["star"]}</div>
        <div class="feat-title">There Is Hope</div>
        <div class="feat-desc">The vast majority of alienated children eventually seek reconnection</div>
      </div>
    </div>
  </div>
</div>

<!-- ===== PAGE 3: THING 1 ===== -->
<div class="page thing-page with-image">
  <div class="thing-header">
    <img src="file://{wound_img}" alt="">
    <div class="thing-number">01</div>
    <div class="thing-label">Thing One</div>
    <h2>This Is Not a Custody Dispute.<br>It Is Abuse.</h2>
  </div>
  <div class="thing-body">
    <p>Parental alienation is not about two parents who cannot get along. It is a systematic campaign by one parent to destroy the relationship between a child and the other parent.</p>
    <p>The alienating parent uses a range of tactics — from subtle undermining to outright fabrication — to turn the child against the targeted parent. The child is weaponised as a tool of control.</p>
    <div class="key-point">
      <p>{FA["warning"]} <span class="icon"></span> Parental alienation meets the clinical definition of psychological abuse of both the child and the targeted parent.</p>
    </div>
    <p>Understanding this distinction is critical. When you stop seeing it as conflict and start seeing it as abuse, everything changes — your strategy, your self-compassion, and your path forward.</p>
  </div>
</div>

<!-- ===== PAGE 4: THING 2 ===== -->
<div class="page thing-page gold">
  <div class="thing-header">
    <div class="thing-number">02</div>
    <div class="thing-label">Thing Two</div>
    <h2>Your Child Still Loves You.<br>Even When They Say They Don\u2019t.</h2>
  </div>
  <div class="thing-body">
    <p>The hardest thing to believe when your child rejects you is that their love has not disappeared. It has been suppressed under layers of loyalty conflict, fear, and manufactured narratives.</p>
    <p>Research by Dr Amy Baker shows that alienated children carry a <strong>deep, often unconscious attachment</strong> to the rejected parent — even when their behaviour suggests the opposite.</p>
    <div class="key-point">
      <p>{FA["heart"]} <span class="icon"></span> The \u201Csleeper effect\u201D: the vast majority of alienated children, once they reach adulthood, begin to question the false narrative and seek out the rejected parent.</p>
    </div>
    <p>Your love is not wasted. Every message you send, every birthday you remember, every moment of patience \u2014 your child may not acknowledge it now, but they are absorbing it.</p>
  </div>
</div>

<!-- ===== PAGE 5: THING 3 ===== -->
<div class="page thing-page">
  <div class="thing-header">
    <div class="thing-number">03</div>
    <div class="thing-label">Thing Three</div>
    <h2>What You Are Feeling<br>Is a Normal Response to<br>an Abnormal Situation</h2>
  </div>
  <div class="thing-body">
    <p>The grief you feel is unlike any other. Researchers call it <strong>ambiguous loss</strong> \u2014 your child is alive but psychologically absent. There is no closure, no funeral, no social recognition of your pain.</p>
    <p>You may experience intrusive thoughts, hypervigilance, emotional numbness, rage, shame, or a sense of going crazy. These are not character flaws. They are <strong>injury symptoms</strong>.</p>
    <div class="key-point">
      <p>{FA["brain"]} <span class="icon"></span> Your nervous system is doing exactly what it was designed to do in the face of ongoing threat. You are not broken \u2014 you are injured.</p>
    </div>
    <p>Naming the wound is the first step to surviving it. When you understand that your responses are normal, you can stop fighting yourself and start healing.</p>
  </div>
</div>

<!-- ===== PAGE 6: QUOTE PAGE ===== -->
<div class="page quote-spread">
  <div class="deco-circle"></div>
  <div class="deco-circle-2"></div>
  <div class="quote-mark">\u201C</div>
  <div class="quote-text">The truth, while suppressed, is rarely destroyed completely. It lives on in the child\u2019s unconscious, waiting for the right moment to surface.</div>
  <div class="quote-rule"></div>
  <div class="quote-author">Dr Amy Baker</div>
</div>

<!-- ===== PAGE 7: THING 4 ===== -->
<div class="page thing-page alt">
  <div class="thing-header">
    <div class="thing-number">04</div>
    <div class="thing-label">Thing Four</div>
    <h2>The Court System<br>Was Not Built for This</h2>
  </div>
  <div class="thing-body">
    <p>Family courts operate on the principle that both parents should compromise. But alienation is not a conflict between equals \u2014 it is one parent systematically erasing the other.</p>
    <p>Legal proceedings can be slow, expensive, and retraumatising. Judges often lack training to recognise alienation. Court orders may be ignored without consequence.</p>
    <div class="key-point">
      <p>{FA["shield"]} <span class="icon"></span> Do not rely on the court alone. Build a multi-layered survival strategy: health, support, documentation, and consistent love.</p>
    </div>
    <p>This does not mean you should abandon legal avenues. But the court is one tool among many \u2014 and often not the most effective one.</p>
  </div>
</div>

<!-- ===== PAGE 8: THING 5 ===== -->
<div class="page thing-page gold">
  <div class="thing-header">
    <div class="thing-number">05</div>
    <div class="thing-label">Thing Five</div>
    <h2>Consistent Love Is<br>the Most Powerful<br>Thing You Can Do</h2>
  </div>
  <div class="thing-body">
    <p>When everything else is taken from you, one thing remains entirely in your control: <strong>the quality and consistency of your love</strong>.</p>
    <p>Research shows that consistent, unconditional love is the strongest predictor of eventual reconnection. Not legal victories. Not proving you are right. Love that endures.</p>
    <div class="key-point">
      <p>{FA["heart"]} <span class="icon"></span> Keep sending messages. Keep remembering birthdays. Keep the door open. Your child\u2019s future self will look for evidence that you never stopped caring.</p>
    </div>
    <p>This is not passive. It is the most active, disciplined, and courageous choice available to you. It is love as a verb \u2014 something you do, not something you feel.</p>
  </div>
</div>

<!-- ===== PAGE 9: CTA ===== -->
<div class="page cta-page">
  <div class="cta-icon">{FA["book"]}</div>
  <h2>Want the Full<br>Survival Guide?</h2>
  <p>This was just a glimpse. The complete Survival Guide for Alienated Parents covers everything \u2014 the research, the tactics, the healing framework, and the path to inner freedom.</p>
  <a class="cta-button" href="https://loveoverexile.com">Download Free</a>
  <div class="cta-url">loveoverexile.com</div>
  <img class="cta-logo" src="file://{logo_img}" alt="Love Over Exile">
</div>

</body>
</html>"""


JS_PREPROCESS = """
() => {
    // --- 1. Overflow detection and font-size reduction ---
    // If a content box overflows its container, shrink text until it fits
    document.querySelectorAll('.thing-body, .intro-main, .exercise-body').forEach(box => {
        let attempts = 0;
        while (box.scrollHeight > box.clientHeight + 2 && attempts < 20) {
            const current = parseFloat(getComputedStyle(box).fontSize);
            if (current <= 7) break;  // Don't go below 7pt
            box.style.fontSize = (current - 0.3) + 'pt';
            attempts++;
        }
        if (attempts > 0) {
            console.log(`Adjusted font-size on ${box.className}: ${attempts} steps`);
        }
    });

    // --- 2. Image aspect ratio normalisation ---
    document.querySelectorAll('img').forEach(img => {
        if (img.naturalWidth && img.naturalHeight) {
            const ratio = img.naturalWidth / img.naturalHeight;
            if (ratio > 2.5) {
                img.style.objectFit = 'cover';
                img.style.objectPosition = 'center 30%';
            }
        }
    });

    // --- 3. Key-point overflow prevention ---
    // If a key-point box overflows, slightly reduce its padding
    document.querySelectorAll('.key-point').forEach(box => {
        if (box.scrollHeight > box.clientHeight + 2) {
            box.style.padding = '4mm 6mm';
            box.style.fontSize = '9.5pt';
        }
    });

    // --- 4. Feature card equalisation ---
    // Make feature cards in each grid the same height
    document.querySelectorAll('.features-grid').forEach(grid => {
        const cards = grid.querySelectorAll('.feature-card');
        let maxH = 0;
        cards.forEach(c => { maxH = Math.max(maxH, c.offsetHeight); });
        cards.forEach(c => { c.style.minHeight = maxH + 'px'; });
    });

    return {
        processed: true,
        pages: document.querySelectorAll('.page').length
    };
}
"""


def main():
    print("Building lead magnet HTML...")
    html = build_html()

    print(f"Writing HTML to {HTML_PATH}...")
    HTML_PATH.write_text(html, encoding="utf-8")

    print("Generating PDF with Playwright (Chromium)...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{HTML_PATH.resolve()}")
        # Wait for fonts and images to load
        page.wait_for_load_state("networkidle")

        # Run JS pre-processing before PDF generation
        result = page.evaluate(JS_PREPROCESS)
        print(f"  Pre-processed {result.get('pages', '?')} pages")

        page.pdf(
            path=str(PDF_PATH),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            outline=True,   # Generate PDF bookmarks from headings
            tagged=True,    # Accessible tagged PDF
        )
        browser.close()

    print(f"PDF generated: {PDF_PATH}")
    print(f"Size: {PDF_PATH.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
