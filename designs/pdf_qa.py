#!/usr/bin/env python3
"""
PDF Visual QA & Self-Check System

Four-layer quality assurance for generated PDFs:
  Layer 1: Programmatic checks (PyMuPDF + pikepdf + Pillow) — instant, free
  Layer 2: Visual regression (baseline comparison) — fast, free
  Layer 3: AI vision review (Claude Vision) — semantic, ~$0.01-0.03/page
  Layer 4: Auto-fix feedback loop — re-render with CSS adjustments

Usage:
  python3 pdf_qa.py survival-guide.pdf                    # Layer 1 only (default)
  python3 pdf_qa.py survival-guide.pdf --layers 1 2       # Layers 1 + 2
  python3 pdf_qa.py survival-guide.pdf --layers 1 2 3     # All check layers
  python3 pdf_qa.py survival-guide.pdf --full              # All layers + auto-fix
  python3 pdf_qa.py survival-guide.pdf --save-baseline     # Save current as baseline
  python3 pdf_qa.py survival-guide.pdf --pages 1-5         # Check specific pages only
"""

import argparse
import base64
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    PASS = "pass"

@dataclass
class Issue:
    layer: int
    check: str
    severity: str
    message: str
    page: Optional[int] = None
    details: Optional[dict] = None

@dataclass
class PageReport:
    page_number: int
    issues: list = field(default_factory=list)

    @property
    def severity(self) -> str:
        if any(i.severity == Severity.CRITICAL for i in self.issues):
            return Severity.CRITICAL
        if any(i.severity == Severity.WARNING for i in self.issues):
            return Severity.WARNING
        return Severity.PASS

@dataclass
class QAReport:
    pdf_path: str
    timestamp: str
    layers_run: list = field(default_factory=list)
    global_issues: list = field(default_factory=list)
    page_reports: list = field(default_factory=list)
    auto_fixes_applied: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)

    @property
    def overall_severity(self) -> str:
        all_issues = self.global_issues[:]
        for pr in self.page_reports:
            all_issues.extend(pr.issues)
        if any(i.severity == Severity.CRITICAL for i in all_issues):
            return Severity.CRITICAL
        if any(i.severity == Severity.WARNING for i in all_issues):
            return Severity.WARNING
        return Severity.PASS

    def to_dict(self):
        d = asdict(self)
        d["overall_severity"] = self.overall_severity
        return d

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HERE = Path(__file__).parent
BASELINE_DIR = HERE / "qa_baselines"

def parse_page_range(spec: str, total: int) -> list:
    """Parse '1-5' or '3' or '1,5,10' into a list of 0-based page indices."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            for p in range(int(start), int(end) + 1):
                if 1 <= p <= total:
                    pages.add(p - 1)
        else:
            p = int(part)
            if 1 <= p <= total:
                pages.add(p - 1)
    return sorted(pages)

def render_page_to_image(doc, page_idx: int, dpi: int = 150):
    """Render a PDF page to a PIL Image."""
    from PIL import Image
    import io
    page = doc[page_idx]
    mat = __import__("fitz").Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    return Image.open(io.BytesIO(img_data))


# ===================================================================
# LAYER 1: PROGRAMMATIC CHECKS
# ===================================================================

def layer1_programmatic(pdf_path: str, page_indices: list = None,
                        expected_pages: tuple = None,
                        expected_size_kb: tuple = None,
                        min_dpi: int = 72,
                        min_font_size: float = 6.0,
                        margin_mm: float = 20.0) -> list:
    """
    Run all programmatic checks. Returns a list of Issues.

    Parameters:
        expected_pages: (min, max) page count range. None = skip check.
        expected_size_kb: (min, max) file size in KB. None = skip check.
        min_dpi: minimum acceptable image DPI.
        min_font_size: minimum acceptable font size in points.
        margin_mm: expected minimum margin in mm (for text overflow check).
    """
    import fitz
    from PIL import Image, ImageStat
    import io

    issues = []
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    file_size_kb = os.path.getsize(pdf_path) / 1024

    if page_indices is None:
        page_indices = list(range(total_pages))

    # --- Check 1: Page count ---
    if expected_pages:
        lo, hi = expected_pages
        if not (lo <= total_pages <= hi):
            issues.append(Issue(
                layer=1, check="page_count", severity=Severity.CRITICAL,
                message=f"Page count {total_pages} outside expected range {lo}-{hi}",
                details={"actual": total_pages, "expected_min": lo, "expected_max": hi}
            ))
        else:
            issues.append(Issue(
                layer=1, check="page_count", severity=Severity.PASS,
                message=f"Page count {total_pages} within range {lo}-{hi}"
            ))

    # --- Check 2: File size ---
    if expected_size_kb:
        lo, hi = expected_size_kb
        if not (lo <= file_size_kb <= hi):
            issues.append(Issue(
                layer=1, check="file_size", severity=Severity.WARNING,
                message=f"File size {file_size_kb:.0f} KB outside expected range {lo}-{hi} KB",
                details={"actual_kb": round(file_size_kb), "expected_min_kb": lo, "expected_max_kb": hi}
            ))
        else:
            issues.append(Issue(
                layer=1, check="file_size", severity=Severity.PASS,
                message=f"File size {file_size_kb:.0f} KB within range"
            ))

    # --- Check 3: Page size consistency ---
    page_sizes = set()
    for i in range(total_pages):
        rect = doc[i].rect
        w, h = round(rect.width, 1), round(rect.height, 1)
        page_sizes.add((w, h))
    if len(page_sizes) > 1:
        issues.append(Issue(
            layer=1, check="page_size_consistency", severity=Severity.WARNING,
            message=f"Inconsistent page sizes: {len(page_sizes)} different sizes found",
            details={"sizes_pt": [list(s) for s in page_sizes]}
        ))
    else:
        issues.append(Issue(
            layer=1, check="page_size_consistency", severity=Severity.PASS,
            message=f"All pages same size: {list(page_sizes)[0]}"
        ))

    # --- Check 4: Blank page detection ---
    for idx in page_indices:
        page = doc[idx]
        text = page.get_text().strip()
        images = page.get_images()
        # Also check for drawn paths (vector graphics)
        drawings = page.get_drawings()
        if not text and not images and not drawings:
            issues.append(Issue(
                layer=1, check="blank_page", severity=Severity.CRITICAL,
                page=idx + 1,
                message=f"Page {idx + 1} appears completely blank (no text, images, or drawings)"
            ))
        elif not text and not images:
            # Has drawings but no text/images — could be decorative only
            # Verify via pixel analysis
            img = render_page_to_image(doc, idx, dpi=72)
            stat = ImageStat.Stat(img)
            # Check if image is nearly uniform (low variance = likely blank/solid)
            variance = sum(stat.var) / len(stat.var)
            if variance < 50:
                issues.append(Issue(
                    layer=1, check="blank_page", severity=Severity.WARNING,
                    page=idx + 1,
                    message=f"Page {idx + 1} has no text content (may be intentional decorative page)",
                    details={"pixel_variance": round(variance, 2)}
                ))

    # --- Check 5: Font embedding ---
    # Note: Subset-embedded fonts have a 6-letter prefix like "MVZTFL+" before
    # the font name. This prefix indicates the font IS embedded (as a subset).
    # We only flag fonts that have NO FontFile reference AND no subset prefix.
    fonts_checked = set()
    unembedded = []
    import re as _re
    subset_prefix_re = _re.compile(r"^[A-Z]{6}\+")
    for idx in page_indices:
        page = doc[idx]
        for font in page.get_fonts(full=True):
            font_name = font[3] if len(font) > 3 else str(font[0])
            if font_name in fonts_checked:
                continue
            fonts_checked.add(font_name)
            # Subset prefix means the font IS embedded (as a subset)
            if subset_prefix_re.match(str(font_name)):
                continue
            # Check for FontFile stream in the font dictionary
            xref = font[0]
            try:
                font_dict = doc.xref_object(xref, compressed=False)
                if "FontFile" not in font_dict and "FontFile2" not in font_dict and "FontFile3" not in font_dict:
                    std14 = ["Courier", "Helvetica", "Times", "Symbol", "ZapfDingbats"]
                    is_std = any(s in str(font_name) for s in std14)
                    if not is_std:
                        unembedded.append(str(font_name))
            except Exception:
                pass

    if unembedded:
        issues.append(Issue(
            layer=1, check="font_embedding", severity=Severity.WARNING,
            message=f"{len(unembedded)} font(s) may not be embedded: {', '.join(unembedded[:5])}",
            details={"unembedded_fonts": unembedded}
        ))
    else:
        issues.append(Issue(
            layer=1, check="font_embedding", severity=Severity.PASS,
            message=f"All {len(fonts_checked)} fonts embedded ({sum(1 for f in fonts_checked if subset_prefix_re.match(str(f)))} subset-embedded)"
        ))

    # --- Check 6: Image DPI ---
    low_dpi_images = []
    for idx in page_indices:
        page = doc[idx]
        for img_info in page.get_images():
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                if base_image:
                    img_w = base_image.get("width", 0)
                    img_h = base_image.get("height", 0)
                    if img_w > 0 and img_h > 0:
                        # Get rendered size on page
                        for img_rect in page.get_image_rects(xref):
                            rendered_w_pt = img_rect.width
                            rendered_h_pt = img_rect.height
                            if rendered_w_pt > 0:
                                dpi_x = img_w / (rendered_w_pt / 72)
                                dpi_y = img_h / (rendered_h_pt / 72)
                                effective_dpi = min(dpi_x, dpi_y)
                                if effective_dpi < min_dpi:
                                    low_dpi_images.append({
                                        "page": idx + 1,
                                        "dpi": round(effective_dpi),
                                        "image_size": f"{img_w}x{img_h}",
                                    })
                            break  # first rect is enough
            except Exception:
                pass

    if low_dpi_images:
        issues.append(Issue(
            layer=1, check="image_dpi", severity=Severity.WARNING,
            message=f"{len(low_dpi_images)} image(s) below {min_dpi} DPI threshold",
            details={"low_dpi_images": low_dpi_images[:10]}
        ))
    else:
        issues.append(Issue(
            layer=1, check="image_dpi", severity=Severity.PASS,
            message=f"All images meet {min_dpi} DPI minimum"
        ))

    # --- Check 7: Text overflow / margin violation ---
    # Note: WeasyPrint places running headers, footers, and page numbers in
    # margin boxes — these intentionally sit outside the body content margins.
    # We exclude: (a) text blocks in header/footer zones (running headers,
    # page numbers), (b) full-bleed pages (cover, chapter openers, photo
    # pages, stat pages, etc.) that intentionally use zero margins.
    margin_pt = margin_mm * 72 / 25.4  # convert mm to points
    header_zone_pt = 22 * 72 / 25.4    # top 22mm matches @page margin-top
    footer_zone_pt = 28 * 72 / 25.4    # bottom 28mm matches @page margin-bottom
    overflow_pages = []
    for idx in page_indices:
        page = doc[idx]
        page_rect = page.rect
        safe_rect = fitz.Rect(
            page_rect.x0 + margin_pt,
            page_rect.y0 + margin_pt,
            page_rect.x1 - margin_pt,
            page_rect.y1 - margin_pt
        )
        # Detect full-bleed pages: if the page has an image that covers
        # most of the page area, it's likely a cover/photo/chapter opener
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]
        page_area = page_rect.width * page_rect.height
        has_fullbleed_image = False
        for block in blocks:
            if block["type"] == 1:  # image block
                img_rect = fitz.Rect(block["bbox"])
                if img_rect.width * img_rect.height > page_area * 0.5:
                    has_fullbleed_image = True
                    break
        if has_fullbleed_image:
            continue  # skip full-bleed pages entirely

        page_has_overflow = False
        for block in blocks:
            if block["type"] == 0:  # text block
                bbox = fitz.Rect(block["bbox"])
                # Skip any text in header/footer margin zones
                in_header_zone = bbox.y1 < header_zone_pt
                in_footer_zone = bbox.y0 > (page_rect.y1 - footer_zone_pt)
                if in_header_zone or in_footer_zone:
                    continue
                # Check if text extends significantly beyond margins (>4pt tolerance)
                if (bbox.x0 < safe_rect.x0 - 4 or bbox.x1 > safe_rect.x1 + 4 or
                    bbox.y0 < safe_rect.y0 - 4 or bbox.y1 > safe_rect.y1 + 4):
                    overflow_pages.append({
                        "page": idx + 1,
                        "block_bbox": [round(c, 1) for c in block["bbox"]],
                        "safe_area": [round(c, 1) for c in [safe_rect.x0, safe_rect.y0, safe_rect.x1, safe_rect.y1]]
                    })
                    page_has_overflow = True
                    break  # one violation per page is enough

    if overflow_pages:
        issues.append(Issue(
            layer=1, check="text_overflow", severity=Severity.WARNING,
            message=f"Text extends beyond {margin_mm}mm margins on {len(overflow_pages)} page(s)",
            details={"overflow_pages": overflow_pages[:10]}
        ))
    else:
        issues.append(Issue(
            layer=1, check="text_overflow", severity=Severity.PASS,
            message=f"All text within {margin_mm}mm margins"
        ))

    # --- Check 8: Minimum font size ---
    tiny_fonts = []
    for idx in page_indices:
        page = doc[idx]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] < min_font_size and span["text"].strip():
                            tiny_fonts.append({
                                "page": idx + 1,
                                "size": round(span["size"], 1),
                                "sample": span["text"][:30]
                            })
                            if len(tiny_fonts) >= 10:
                                break
                    if len(tiny_fonts) >= 10:
                        break
            if len(tiny_fonts) >= 10:
                break
        if len(tiny_fonts) >= 10:
            break

    if tiny_fonts:
        issues.append(Issue(
            layer=1, check="min_font_size", severity=Severity.WARNING,
            message=f"Found text smaller than {min_font_size}pt",
            details={"tiny_fonts": tiny_fonts}
        ))
    else:
        issues.append(Issue(
            layer=1, check="min_font_size", severity=Severity.PASS,
            message=f"All text {min_font_size}pt or larger"
        ))

    # --- Check 9: PDF metadata ---
    meta = doc.metadata
    missing_meta = []
    if not meta.get("title"):
        missing_meta.append("title")
    if not meta.get("author"):
        missing_meta.append("author")
    if missing_meta:
        issues.append(Issue(
            layer=1, check="metadata", severity=Severity.INFO,
            message=f"Missing PDF metadata: {', '.join(missing_meta)}",
            details={"metadata": meta}
        ))
    else:
        issues.append(Issue(
            layer=1, check="metadata", severity=Severity.PASS,
            message="PDF metadata present (title, author)"
        ))

    # --- Check 10: Heading hierarchy ---
    all_headings = []
    for idx in page_indices:
        page = doc[idx]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        sz = span["size"]
                        txt = span["text"].strip()
                        if sz >= 14 and txt and len(txt) < 100:
                            all_headings.append({
                                "page": idx + 1,
                                "size": round(sz, 1),
                                "text": txt[:50],
                                "bold": "Bold" in span.get("font", "") or "bold" in span.get("font", "").lower()
                            })
    # Just report — not a pass/fail, informational
    if all_headings:
        sizes = sorted(set(h["size"] for h in all_headings), reverse=True)
        issues.append(Issue(
            layer=1, check="heading_hierarchy", severity=Severity.PASS,
            message=f"Found {len(all_headings)} headings across {len(sizes)} size levels: {sizes[:5]}",
            details={"heading_count": len(all_headings), "size_levels": sizes}
        ))

    doc.close()
    return issues


# ===================================================================
# LAYER 2: VISUAL REGRESSION
# ===================================================================

def layer2_save_baseline(pdf_path: str, page_indices: list = None):
    """Render each page as an image and save as baseline for future comparison."""
    import fitz
    doc = fitz.open(pdf_path)
    total = len(doc)
    if page_indices is None:
        page_indices = list(range(total))

    baseline_name = Path(pdf_path).stem
    baseline_path = BASELINE_DIR / baseline_name
    baseline_path.mkdir(parents=True, exist_ok=True)

    for idx in page_indices:
        img = render_page_to_image(doc, idx, dpi=150)
        img.save(baseline_path / f"page_{idx + 1:03d}.png")

    # Save metadata
    meta = {
        "source": str(pdf_path),
        "total_pages": total,
        "saved_pages": [i + 1 for i in page_indices],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dpi": 150,
    }
    (baseline_path / "baseline_meta.json").write_text(json.dumps(meta, indent=2))
    doc.close()
    return baseline_path


def layer2_visual_regression(pdf_path: str, page_indices: list = None,
                              diff_threshold: float = 0.02) -> list:
    """
    Compare current PDF pages against saved baseline images.
    Returns a list of Issues.

    diff_threshold: fraction of different pixels to trigger a warning (0.02 = 2%).
    """
    import fitz
    from PIL import Image, ImageChops, ImageStat
    import io

    issues = []
    doc = fitz.open(pdf_path)
    total = len(doc)
    if page_indices is None:
        page_indices = list(range(total))

    baseline_name = Path(pdf_path).stem
    baseline_path = BASELINE_DIR / baseline_name

    if not baseline_path.exists():
        issues.append(Issue(
            layer=2, check="baseline_exists", severity=Severity.INFO,
            message=f"No baseline found at {baseline_path}. Run with --save-baseline first. Skipping visual regression."
        ))
        doc.close()
        return issues

    # Load baseline metadata
    meta_file = baseline_path / "baseline_meta.json"
    if meta_file.exists():
        meta = json.loads(meta_file.read_text())
        baseline_pages = meta.get("saved_pages", [])
    else:
        baseline_pages = []

    # Page count comparison
    if meta_file.exists():
        baseline_total = meta.get("total_pages", 0)
        if total != baseline_total:
            issues.append(Issue(
                layer=2, check="page_count_change", severity=Severity.WARNING,
                message=f"Page count changed: baseline={baseline_total}, current={total}"
            ))

    diff_dir = BASELINE_DIR / f"{baseline_name}_diffs"
    diff_dir.mkdir(parents=True, exist_ok=True)

    changed_pages = []
    for idx in page_indices:
        page_num = idx + 1
        baseline_img_path = baseline_path / f"page_{page_num:03d}.png"
        if not baseline_img_path.exists():
            continue

        # Render current page
        current_img = render_page_to_image(doc, idx, dpi=150)
        baseline_img = Image.open(baseline_img_path)

        # Resize if dimensions don't match (safety)
        if current_img.size != baseline_img.size:
            current_img = current_img.resize(baseline_img.size)

        # Compute difference
        diff = ImageChops.difference(current_img.convert("RGB"), baseline_img.convert("RGB"))
        diff_stat = ImageStat.Stat(diff)
        # Mean difference across RGB channels
        mean_diff = sum(diff_stat.mean) / (3 * 255)  # normalise to 0-1

        if mean_diff > diff_threshold:
            # Save diff image with amplified differences
            from PIL import ImageEnhance
            amplified = ImageEnhance.Contrast(diff).enhance(10.0)
            amplified.save(diff_dir / f"diff_page_{page_num:03d}.png")

            changed_pages.append({
                "page": page_num,
                "diff_score": round(mean_diff * 100, 2),
                "diff_image": str(diff_dir / f"diff_page_{page_num:03d}.png"),
            })
            issues.append(Issue(
                layer=2, check="visual_diff", severity=Severity.WARNING,
                page=page_num,
                message=f"Page {page_num} differs from baseline by {mean_diff * 100:.1f}%",
                details={"diff_score_pct": round(mean_diff * 100, 2)}
            ))
        else:
            issues.append(Issue(
                layer=2, check="visual_diff", severity=Severity.PASS,
                page=page_num,
                message=f"Page {page_num} matches baseline ({mean_diff * 100:.2f}% diff)"
            ))

    # Self-consistency check: compare all chapter openers to each other
    # (pages that have large headings and teal backgrounds)
    # This is a heuristic check — compare similar page types

    if not changed_pages:
        issues.append(Issue(
            layer=2, check="visual_regression_summary", severity=Severity.PASS,
            message=f"All {len(page_indices)} checked pages match baseline"
        ))
    else:
        issues.append(Issue(
            layer=2, check="visual_regression_summary", severity=Severity.WARNING,
            message=f"{len(changed_pages)} page(s) differ from baseline",
            details={"changed_pages": changed_pages}
        ))

    doc.close()
    return issues


# ===================================================================
# LAYER 3: AI VISION REVIEW
# ===================================================================

def layer3_ai_vision(pdf_path: str, page_indices: list = None,
                      api_key: str = None,
                      model: str = "claude-sonnet-4-20250514",
                      max_pages: int = 10) -> list:
    """
    Send PDF pages to Claude Vision for semantic layout review.
    Returns a list of Issues.

    Uses claude-sonnet-4-20250514 by default (fast, cheap, good vision).
    Set max_pages to limit cost.
    """
    import fitz

    issues = []

    # Find API key
    if not api_key:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Try .env file
        env_file = HERE.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        issues.append(Issue(
            layer=3, check="api_key", severity=Severity.INFO,
            message="No ANTHROPIC_API_KEY found. Set it in environment or .env file. Skipping AI vision review."
        ))
        return issues

    try:
        import anthropic
    except ImportError:
        issues.append(Issue(
            layer=3, check="anthropic_sdk", severity=Severity.INFO,
            message="anthropic package not installed. Run: pip install anthropic"
        ))
        return issues

    client = anthropic.Anthropic(api_key=api_key)
    doc = fitz.open(pdf_path)
    total = len(doc)

    if page_indices is None:
        page_indices = list(range(total))

    # Limit pages to review
    review_indices = page_indices[:max_pages]
    if len(page_indices) > max_pages:
        issues.append(Issue(
            layer=3, check="page_limit", severity=Severity.INFO,
            message=f"AI review limited to {max_pages} pages (of {len(page_indices)} requested). Use --max-ai-pages to increase."
        ))

    review_prompt = """You are a professional PDF layout quality inspector. Review this ebook page image for layout and design issues.

Check for these specific problems:
1. TEXT OVERFLOW — text cut off at edges or overflowing containers
2. ORPHANS — single line at bottom of page starting a new paragraph
3. WIDOWS — single line at top of page finishing a previous paragraph
4. STRETCHED IMAGES — images with wrong aspect ratio
5. SPACING ISSUES — inconsistent or excessive gaps between elements
6. OVERLAPPING — text or elements overlapping each other
7. ALIGNMENT — misaligned columns, headers, or elements
8. EMPTY SPACE — large unexplained blank areas
9. FONT ISSUES — missing characters, wrong encoding, rendering problems
10. COLOUR/CONTRAST — text hard to read against background
11. BROKEN LAYOUT — elements in wrong positions, containers not containing content
12. DESIGN QUALITY — overall professional quality assessment

Return ONLY a JSON object (no markdown, no code fences) with this exact structure:
{
  "issues": [
    {"type": "orphan", "description": "Single line 'they were...' at top of page", "severity": "warning"},
    {"type": "spacing", "description": "Large gap between heading and first paragraph", "severity": "info"}
  ],
  "page_quality": "good|acceptable|poor",
  "confidence": 0.85
}

If the page looks fine, return: {"issues": [], "page_quality": "good", "confidence": 0.9}"""

    for idx in review_indices:
        page_num = idx + 1
        try:
            # Render page to PNG
            img = render_page_to_image(doc, idx, dpi=150)
            import io
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_b64,
                            }
                        },
                        {
                            "type": "text",
                            "text": f"This is page {page_num} of a {total}-page ebook PDF. {review_prompt}"
                        }
                    ]
                }]
            )

            # Parse response
            response_text = response.content[0].text.strip()
            # Clean up if wrapped in code fences
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                issues.append(Issue(
                    layer=3, check="ai_parse_error", severity=Severity.INFO,
                    page=page_num,
                    message=f"Could not parse AI response for page {page_num}",
                    details={"raw_response": response_text[:200]}
                ))
                continue

            page_issues = result.get("issues", [])
            quality = result.get("page_quality", "unknown")
            confidence = result.get("confidence", 0)

            if not page_issues:
                issues.append(Issue(
                    layer=3, check="ai_review", severity=Severity.PASS,
                    page=page_num,
                    message=f"Page {page_num}: AI review PASS (quality={quality}, confidence={confidence})"
                ))
            else:
                for ai_issue in page_issues:
                    sev_map = {"critical": Severity.CRITICAL, "warning": Severity.WARNING, "info": Severity.INFO}
                    sev = sev_map.get(ai_issue.get("severity", "info"), Severity.INFO)
                    issues.append(Issue(
                        layer=3, check=f"ai_{ai_issue.get('type', 'unknown')}",
                        severity=sev, page=page_num,
                        message=f"Page {page_num}: {ai_issue.get('description', 'Issue detected')}",
                        details={"ai_confidence": confidence, "page_quality": quality}
                    ))

        except Exception as e:
            issues.append(Issue(
                layer=3, check="ai_error", severity=Severity.INFO,
                page=page_num,
                message=f"AI review failed for page {page_num}: {str(e)[:100]}"
            ))

    doc.close()
    return issues


# ===================================================================
# LAYER 4: AUTO-FIX FEEDBACK LOOP
# ===================================================================

def layer4_auto_fix(pdf_path: str, all_issues: list,
                     css_path: str = None,
                     generator_script: str = None,
                     max_iterations: int = 3) -> list:
    """
    Attempt to auto-fix detected issues by adjusting CSS and re-rendering.
    Returns a list of fixes applied (or attempted).

    Only fixes issues with known remediation strategies:
    - blank_page: no CSS fix possible, flag for manual review
    - text_overflow: increase page margins or reduce font size
    - min_font_size: increase font size
    - orphan/widow: tighten orphans/widows CSS values
    - metadata: add metadata via pikepdf
    """
    import subprocess

    fixes = []

    if css_path is None:
        css_path = str(HERE / "ebook.css")
    if generator_script is None:
        generator_script = str(HERE / "generate_ebook.py")

    css_file = Path(css_path)
    if not css_file.exists():
        fixes.append({
            "fix": "skip",
            "reason": f"CSS file not found: {css_path}",
            "applied": False
        })
        return fixes

    css_content = css_file.read_text()
    css_modified = False

    # Categorise issues — include INFO for fixable items like metadata
    issue_types = {}
    for issue in all_issues:
        if issue.severity in (Severity.CRITICAL, Severity.WARNING, Severity.INFO):
            key = issue.check
            if key not in issue_types:
                issue_types[key] = []
            issue_types[key].append(issue)

    # --- Fix: Missing metadata ---
    if "metadata" in issue_types:
        try:
            import pikepdf
            pdf = pikepdf.open(pdf_path, allow_overwriting_input=True)
            with pdf.open_metadata() as meta:
                if not meta.get("{http://purl.org/dc/elements/1.1/}title"):
                    meta["{http://purl.org/dc/elements/1.1/}title"] = "Love Over Exile — Survival Guide"
                if not meta.get("{http://purl.org/dc/elements/1.1/}creator"):
                    meta["{http://purl.org/dc/elements/1.1/}creator"] = "Malcolm Smith"
            pdf.save(pdf_path)
            pdf.close()
            fixes.append({
                "fix": "metadata_added",
                "description": "Added title and author metadata via pikepdf",
                "applied": True,
                "requires_regeneration": False
            })
        except Exception as e:
            fixes.append({
                "fix": "metadata_failed",
                "description": f"Could not add metadata: {str(e)[:100]}",
                "applied": False
            })

    # --- Fix: Orphan/widow (AI-detected) ---
    orphan_widow_issues = [i for i in all_issues if "orphan" in i.check or "widow" in i.check]
    if orphan_widow_issues:
        # Tighten orphan/widow CSS
        if "orphans:" in css_content:
            # Increase existing value
            import re
            current = re.search(r"orphans:\s*(\d+)", css_content)
            if current and int(current.group(1)) < 4:
                new_val = int(current.group(1)) + 1
                css_content = re.sub(r"orphans:\s*\d+", f"orphans: {new_val}", css_content)
                css_modified = True
                fixes.append({
                    "fix": "orphans_increased",
                    "description": f"Increased orphans from {current.group(1)} to {new_val}",
                    "applied": True,
                    "requires_regeneration": True
                })
        else:
            # Add orphans/widows rule to body
            css_content = css_content.replace(
                "text-align: justify;",
                "text-align: justify;\n  orphans: 3;\n  widows: 3;",
                1  # only first occurrence (body)
            )
            css_modified = True
            fixes.append({
                "fix": "orphans_widows_added",
                "description": "Added orphans: 3; widows: 3; to body text",
                "applied": True,
                "requires_regeneration": True
            })

    # --- Fix: Text overflow (widen margins slightly) ---
    overflow_issues = [i for i in all_issues if i.check == "text_overflow" and i.severity == Severity.CRITICAL]
    if overflow_issues:
        # This is risky to auto-fix — just flag it
        fixes.append({
            "fix": "text_overflow_flagged",
            "description": f"Text overflow on {len(overflow_issues)} pages — requires manual CSS review",
            "applied": False,
            "pages": [i.page for i in overflow_issues if i.page]
        })

    # --- Write modified CSS ---
    if css_modified:
        css_file.write_text(css_content)
        fixes.append({
            "fix": "css_updated",
            "description": f"CSS file updated: {css_path}",
            "applied": True
        })

        # --- Re-generate PDF ---
        gen_path = Path(generator_script)
        if gen_path.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(gen_path)],
                    capture_output=True, text=True, timeout=120,
                    cwd=str(HERE)
                )
                if result.returncode == 0:
                    fixes.append({
                        "fix": "pdf_regenerated",
                        "description": "PDF successfully regenerated after CSS fixes",
                        "applied": True
                    })
                else:
                    fixes.append({
                        "fix": "regeneration_failed",
                        "description": f"PDF generation failed: {result.stderr[:200]}",
                        "applied": False
                    })
            except subprocess.TimeoutExpired:
                fixes.append({
                    "fix": "regeneration_timeout",
                    "description": "PDF generation timed out after 120s",
                    "applied": False
                })
        else:
            fixes.append({
                "fix": "no_generator",
                "description": f"Generator script not found: {generator_script}",
                "applied": False
            })

    return fixes


# ===================================================================
# REPORT AGGREGATOR
# ===================================================================

def aggregate_report(pdf_path: str, all_issues: list,
                     layers_run: list, auto_fixes: list = None) -> QAReport:
    """Combine all layer results into a single report."""
    report = QAReport(
        pdf_path=str(pdf_path),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
        layers_run=layers_run,
        auto_fixes_applied=auto_fixes or [],
    )

    # Separate global vs page-specific issues
    page_issues = {}
    for issue in all_issues:
        if issue.page:
            if issue.page not in page_issues:
                page_issues[issue.page] = PageReport(page_number=issue.page)
            page_issues[issue.page].issues.append(issue)
        else:
            report.global_issues.append(issue)

    report.page_reports = [page_issues[p] for p in sorted(page_issues.keys())]

    # Build summary
    total_issues = len(all_issues)
    by_severity = {s.value: 0 for s in Severity}
    for issue in all_issues:
        by_severity[issue.severity] += 1

    report.summary = {
        "total_checks": total_issues,
        "critical": by_severity[Severity.CRITICAL],
        "warnings": by_severity[Severity.WARNING],
        "info": by_severity[Severity.INFO],
        "passed": by_severity[Severity.PASS],
    }

    return report


# ===================================================================
# CLI OUTPUT
# ===================================================================

def print_report(report: QAReport, verbose: bool = False):
    """Print a human-readable report to the console."""
    sev = report.overall_severity
    icon = {"critical": "FAIL", "warning": "WARN", "pass": "PASS"}
    colour = {"critical": "\033[91m", "warning": "\033[93m", "pass": "\033[92m"}
    reset = "\033[0m"

    print(f"\n{'='*60}")
    print(f"  PDF QA Report — {colour.get(sev, '')}{icon.get(sev, '???')}{reset}")
    print(f"  {report.pdf_path}")
    print(f"  {report.timestamp}")
    print(f"{'='*60}")

    s = report.summary
    print(f"\n  Layers run: {report.layers_run}")
    print(f"  Total checks: {s.get('total_checks', 0)}")
    print(f"  {colour.get('pass', '')}Passed: {s.get('passed', 0)}{reset}  |  "
          f"{colour.get('warning', '')}Warnings: {s.get('warnings', 0)}{reset}  |  "
          f"{colour.get('critical', '')}Critical: {s.get('critical', 0)}{reset}  |  "
          f"Info: {s.get('info', 0)}")

    # Global issues
    non_pass_global = [i for i in report.global_issues if i.severity != Severity.PASS]
    if non_pass_global:
        print(f"\n--- Global Issues ---")
        for issue in non_pass_global:
            sev_icon = {"critical": "X", "warning": "!", "info": "i"}.get(issue.severity, "?")
            print(f"  [{sev_icon}] L{issue.layer} {issue.check}: {issue.message}")
            if verbose and issue.details:
                for k, v in issue.details.items():
                    print(f"      {k}: {v}")

    # Page issues
    non_pass_pages = [pr for pr in report.page_reports
                      if any(i.severity != Severity.PASS for i in pr.issues)]
    if non_pass_pages:
        print(f"\n--- Page Issues ---")
        for pr in non_pass_pages:
            for issue in pr.issues:
                if issue.severity != Severity.PASS:
                    sev_icon = {"critical": "X", "warning": "!", "info": "i"}.get(issue.severity, "?")
                    print(f"  [{sev_icon}] Page {pr.page_number} — L{issue.layer} {issue.check}: {issue.message}")

    # Auto-fixes
    if report.auto_fixes_applied:
        print(f"\n--- Auto-Fixes ---")
        for fix in report.auto_fixes_applied:
            status = "Applied" if fix.get("applied") else "Skipped"
            print(f"  [{status}] {fix.get('fix', '?')}: {fix.get('description', '')}")

    # Pass summary
    if not non_pass_global and not non_pass_pages:
        print(f"\n  {colour.get('pass', '')}All checks passed.{reset}")

    print(f"\n{'='*60}\n")


def save_report(report: QAReport, output_path: str = None):
    """Save report as JSON."""
    if output_path is None:
        output_path = str(Path(report.pdf_path).with_suffix(".qa.json"))
    Path(output_path).write_text(json.dumps(report.to_dict(), indent=2, default=str))
    return output_path


# ===================================================================
# MAIN
# ===================================================================

def run_qa(pdf_path: str, layers: list = None, pages: str = None,
           save_baseline: bool = False, verbose: bool = False,
           max_ai_pages: int = 10, auto_fix: bool = False,
           expected_pages: tuple = None, expected_size_kb: tuple = None) -> QAReport:
    """
    Run the full QA pipeline.

    Args:
        pdf_path: Path to the PDF file.
        layers: Which layers to run (default: [1]). Use [1,2,3] for all checks.
        pages: Page range string (e.g. "1-5"). None = all pages.
        save_baseline: If True, save current PDF as baseline and exit.
        verbose: Show detailed output.
        max_ai_pages: Maximum pages to send to AI review.
        auto_fix: If True, attempt to auto-fix detected issues (Layer 4).
        expected_pages: (min, max) page count range.
        expected_size_kb: (min, max) file size range in KB.
    """
    import fitz

    if layers is None:
        layers = [1]

    pdf_path = str(Path(pdf_path).resolve())
    if not Path(pdf_path).exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)

    # Get total page count for page range parsing
    doc = fitz.open(pdf_path)
    total = len(doc)
    doc.close()

    page_indices = parse_page_range(pages, total) if pages else None

    # Save baseline mode
    if save_baseline:
        print(f"Saving baseline for {Path(pdf_path).name} ({total} pages)...")
        baseline_path = layer2_save_baseline(pdf_path, page_indices)
        print(f"Baseline saved to: {baseline_path}")
        return None

    all_issues = []
    layers_run = []

    # Layer 1
    if 1 in layers:
        print("Layer 1: Running programmatic checks...")
        issues = layer1_programmatic(
            pdf_path, page_indices,
            expected_pages=expected_pages,
            expected_size_kb=expected_size_kb
        )
        all_issues.extend(issues)
        layers_run.append(1)
        passed = sum(1 for i in issues if i.severity == Severity.PASS)
        flagged = sum(1 for i in issues if i.severity in (Severity.CRITICAL, Severity.WARNING))
        print(f"  -> {passed} passed, {flagged} flagged")

    # Layer 2
    if 2 in layers:
        print("Layer 2: Running visual regression...")
        issues = layer2_visual_regression(pdf_path, page_indices)
        all_issues.extend(issues)
        layers_run.append(2)
        flagged = sum(1 for i in issues if i.severity in (Severity.CRITICAL, Severity.WARNING))
        print(f"  -> {len(issues)} checks, {flagged} differences found")

    # Layer 3
    if 3 in layers:
        print(f"Layer 3: Running AI vision review (max {max_ai_pages} pages)...")
        issues = layer3_ai_vision(pdf_path, page_indices, max_pages=max_ai_pages)
        all_issues.extend(issues)
        layers_run.append(3)
        flagged = sum(1 for i in issues if i.severity in (Severity.CRITICAL, Severity.WARNING))
        print(f"  -> {len(issues)} checks, {flagged} issues found")

    # Layer 4
    auto_fixes = []
    if auto_fix or 4 in layers:
        flagged_issues = [i for i in all_issues if i.severity in (Severity.CRITICAL, Severity.WARNING)]
        if flagged_issues:
            print("Layer 4: Attempting auto-fixes...")
            auto_fixes = layer4_auto_fix(pdf_path, all_issues)
            layers_run.append(4)
            applied = sum(1 for f in auto_fixes if f.get("applied"))
            print(f"  -> {applied} fixes applied, {len(auto_fixes) - applied} skipped")
        else:
            print("Layer 4: No issues to fix.")

    # Aggregate
    report = aggregate_report(pdf_path, all_issues, layers_run, auto_fixes)
    print_report(report, verbose=verbose)

    # Save JSON report
    json_path = save_report(report)
    print(f"Report saved: {json_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="PDF Visual QA & Self-Check System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 pdf_qa.py survival-guide.pdf                     # Layer 1 only
  python3 pdf_qa.py survival-guide.pdf --layers 1 2 3      # All check layers
  python3 pdf_qa.py survival-guide.pdf --full               # All layers + auto-fix
  python3 pdf_qa.py survival-guide.pdf --save-baseline      # Save baseline
  python3 pdf_qa.py survival-guide.pdf --pages 1-5 -v       # Check pages 1-5, verbose
  python3 pdf_qa.py survival-guide.pdf --expected-pages 70 75  # Validate page count
        """
    )
    parser.add_argument("pdf", help="Path to the PDF file to check")
    parser.add_argument("--layers", nargs="+", type=int, default=[1],
                        help="Which layers to run (1=programmatic, 2=visual, 3=AI). Default: 1")
    parser.add_argument("--full", action="store_true",
                        help="Run all layers including auto-fix")
    parser.add_argument("--pages", type=str, default=None,
                        help="Page range to check (e.g. '1-5' or '1,3,5')")
    parser.add_argument("--save-baseline", action="store_true",
                        help="Save current PDF as visual regression baseline")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show detailed issue information")
    parser.add_argument("--max-ai-pages", type=int, default=10,
                        help="Maximum pages to send to AI vision review (default: 10)")
    parser.add_argument("--expected-pages", nargs=2, type=int, metavar=("MIN", "MAX"),
                        help="Expected page count range")
    parser.add_argument("--expected-size", nargs=2, type=int, metavar=("MIN_KB", "MAX_KB"),
                        help="Expected file size range in KB")

    args = parser.parse_args()

    layers = [1, 2, 3, 4] if args.full else args.layers
    expected_pages = tuple(args.expected_pages) if args.expected_pages else None
    expected_size = tuple(args.expected_size) if args.expected_size else None

    run_qa(
        pdf_path=args.pdf,
        layers=layers,
        pages=args.pages,
        save_baseline=args.save_baseline,
        verbose=args.verbose,
        max_ai_pages=args.max_ai_pages,
        auto_fix=args.full,
        expected_pages=expected_pages,
        expected_size_kb=expected_size,
    )


if __name__ == "__main__":
    main()
