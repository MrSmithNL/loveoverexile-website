"""Layout intelligence engine for ebook PDF generation.

Provides:
- ContentClassifier: classifies markdown blocks by type, weight, and length
- PageTemplateLibrary: 12 reusable page templates returning HTML
- LayoutPlanner: sequences classified blocks into templates following rhythm rules

Usage:
    from layout_engine import ContentClassifier, PageTemplateLibrary, LayoutPlanner

    blocks = ContentClassifier.classify_markdown(markdown_text)
    planner = LayoutPlanner(blocks, theme="loe")
    pages = planner.plan()
    html = PageTemplateLibrary.render_pages(pages)
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ─── Content Classification ───────────────────────────────────────────────

class ContentType(Enum):
    """What the content IS."""
    NARRATIVE = "narrative"
    STATISTIC = "statistic"
    QUOTE = "quote"
    LIST = "list"
    EXERCISE = "exercise"
    DEFINITION = "definition"
    WARNING = "warning"
    TIP = "tip"
    EXAMPLE = "example"
    CASE_STUDY = "case_study"
    CHAPTER_START = "chapter_start"
    CHAPTER_END = "chapter_end"
    SECTION_HEADING = "section_heading"


class ContentWeight(Enum):
    """How important the content is visually."""
    HERO = "hero"          # Chapter-defining, gets a full page
    MAJOR = "major"        # Section-defining, gets prominent treatment
    SUPPORTING = "supporting"  # Standard body content
    MINOR = "minor"        # Supplementary detail


class ContentLength(Enum):
    """How much space the content needs."""
    MICRO = "micro"        # < 30 words
    SHORT = "short"        # 30-100 words
    MEDIUM = "medium"      # 100-300 words
    LONG = "long"          # 300+ words


@dataclass
class ContentBlock:
    """A classified piece of content ready for template assignment."""
    raw_text: str
    html: str = ""
    content_type: ContentType = ContentType.NARRATIVE
    weight: ContentWeight = ContentWeight.SUPPORTING
    length: ContentLength = ContentLength.MEDIUM
    word_count: int = 0
    heading: str = ""
    heading_level: int = 0
    has_image: bool = False
    image_path: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def density(self) -> str:
        """Visual density: light (visual breather), medium, heavy (text-dense)."""
        if self.content_type in (ContentType.QUOTE, ContentType.STATISTIC):
            return "light"
        if self.length in (ContentLength.MICRO, ContentLength.SHORT):
            return "light"
        if self.length == ContentLength.LONG:
            return "heavy"
        return "medium"


class ContentClassifier:
    """Classifies markdown content blocks by type, weight, and length."""

    # Patterns that indicate content types
    STAT_PATTERNS = [
        r'\d+[%$€£]',           # Numbers with currency/percent
        r'[$€£]\d+',            # Currency prefix
        r'\d+\s*(million|billion|thousand|percent)',
        r'\b\d{1,3}(,\d{3})+\b',  # Large numbers with commas
        r'\b\d+(\.\d+)?\s*(x|times)\b',  # Multipliers
    ]

    QUOTE_PATTERNS = [
        r'^>\s',                 # Markdown blockquote
        r'["""\u201C\u201D].*["""\u201C\u201D]',  # Quoted text
        r'^\s*[-—]\s*.+$',      # Attribution line
    ]

    EXERCISE_PATTERNS = [
        r'\b(exercise|activity|try this|worksheet|practice|reflection)\b',
        r'\b(write down|list your|think about|consider)\b',
        r'\[\s*\]',             # Checkboxes
    ]

    WARNING_PATTERNS = [
        r'\b(warning|caution|danger|important|critical)\b',
        r'\b(do not|never|avoid|stop)\b.*\b(if|when|before)\b',
    ]

    TIP_PATTERNS = [
        r'\b(tip|hint|remember|pro tip|key point|note)\b',
        r'\b(try|consider|you can|one way)\b',
    ]

    LIST_PATTERNS = [
        r'^\s*[-*+]\s',         # Unordered list
        r'^\s*\d+[\.)]\s',      # Ordered list
    ]

    DEFINITION_PATTERNS = [
        r'\b(defined as|means|refers to|is when|is the)\b',
        r'^[A-Z][^.]+:',       # Term: definition format
    ]

    @classmethod
    def classify_text(cls, text: str, heading: str = "",
                      heading_level: int = 0) -> ContentBlock:
        """Classify a single block of text."""
        word_count = len(text.split())
        block = ContentBlock(
            raw_text=text,
            heading=heading,
            heading_level=heading_level,
            word_count=word_count,
            length=cls._classify_length(word_count),
        )

        # Classify content type
        block.content_type = cls._classify_type(text, heading, heading_level)

        # Classify weight based on type + heading level
        block.weight = cls._classify_weight(
            block.content_type, heading_level, word_count
        )

        return block

    @classmethod
    def _classify_length(cls, word_count: int) -> ContentLength:
        if word_count < 30:
            return ContentLength.MICRO
        if word_count < 100:
            return ContentLength.SHORT
        if word_count < 300:
            return ContentLength.MEDIUM
        return ContentLength.LONG

    @classmethod
    def _classify_type(cls, text: str, heading: str,
                       heading_level: int) -> ContentType:
        """Determine content type from text patterns."""
        # Chapter/section starts take priority
        if heading_level == 1:
            return ContentType.CHAPTER_START
        if heading_level == 2 and heading:
            return ContentType.SECTION_HEADING

        text_lower = text.lower()

        # Check each type's patterns — order matters!

        # Lists first (before quote, since - lines can match quote patterns)
        lines = text.strip().split('\n')
        list_lines = sum(
            1 for line in lines
            if any(re.match(p, line) for p in cls.LIST_PATTERNS)
        )
        if lines and list_lines / len(lines) > 0.5:
            return ContentType.LIST

        if any(re.search(p, text_lower, re.MULTILINE)
               for p in cls.EXERCISE_PATTERNS):
            return ContentType.EXERCISE

        if any(re.search(p, text, re.IGNORECASE | re.MULTILINE)
               for p in cls.STAT_PATTERNS):
            return ContentType.STATISTIC

        if any(re.search(p, text, re.IGNORECASE | re.MULTILINE)
               for p in cls.QUOTE_PATTERNS):
            return ContentType.QUOTE

        if any(re.search(p, text_lower, re.MULTILINE)
               for p in cls.WARNING_PATTERNS):
            return ContentType.WARNING

        if any(re.search(p, text_lower, re.MULTILINE)
               for p in cls.TIP_PATTERNS):
            return ContentType.TIP

        if any(re.search(p, text, re.IGNORECASE | re.MULTILINE)
               for p in cls.DEFINITION_PATTERNS):
            return ContentType.DEFINITION

        return ContentType.NARRATIVE

    @classmethod
    def _classify_weight(cls, content_type: ContentType,
                         heading_level: int, word_count: int) -> ContentWeight:
        """Determine visual weight."""
        if content_type == ContentType.CHAPTER_START:
            return ContentWeight.HERO
        if content_type == ContentType.SECTION_HEADING:
            return ContentWeight.MAJOR
        if content_type in (ContentType.QUOTE, ContentType.STATISTIC):
            if word_count < 50:
                return ContentWeight.MAJOR
            return ContentWeight.SUPPORTING
        if content_type in (ContentType.EXERCISE, ContentType.WARNING):
            return ContentWeight.MAJOR
        if word_count > 300:
            return ContentWeight.SUPPORTING
        return ContentWeight.SUPPORTING

    @classmethod
    def classify_markdown(cls, markdown: str) -> list[ContentBlock]:
        """Split markdown into classified blocks.

        Splits on headings and double newlines, classifies each block.
        Headings become their own blocks; subsequent paragraphs are classified
        independently (heading_level=0) but retain the parent heading text
        for context.
        """
        blocks = []
        current_heading = ""
        current_text_lines = []

        for line in markdown.split('\n'):
            # Check for heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                # Flush previous body text block (level=0, it's body text)
                if current_text_lines:
                    text = '\n'.join(current_text_lines).strip()
                    if text:
                        blocks.append(cls.classify_text(
                            text, current_heading, 0
                        ))
                    current_text_lines = []

                level = len(heading_match.group(1))
                current_heading = heading_match.group(2).strip()
                # Add the heading itself as a classified block
                blocks.append(cls.classify_text(
                    current_heading, current_heading, level
                ))
                continue

            # Check for block separator (blank line after content)
            if not line.strip() and current_text_lines:
                text = '\n'.join(current_text_lines).strip()
                if text:
                    blocks.append(cls.classify_text(
                        text, current_heading, 0
                    ))
                current_text_lines = []
                continue

            if line.strip():
                current_text_lines.append(line)

        # Flush final block
        if current_text_lines:
            text = '\n'.join(current_text_lines).strip()
            if text:
                blocks.append(cls.classify_text(
                    text, current_heading, 0
                ))

        return blocks


# ─── Page Templates ───────────────────────────────────────────────────────

class TemplateType(Enum):
    """Available page template types."""
    CHAPTER_OPENER = "chapter-opener"
    TEXT_ONLY = "text-only"
    TEXT_WITH_SIDEBAR = "text-with-sidebar"
    TEXT_TWO_COLUMN = "text-two-column"
    FEATURE_SPREAD = "feature-spread"
    STAT_PANEL = "stat-panel"
    PULLQUOTE_BREAK = "pullquote-break"
    EXERCISE_PAGE = "exercise-page"
    CHECKLIST_PAGE = "checklist-page"
    COMPARISON_PAGE = "comparison-page"
    TIMELINE_PAGE = "timeline-page"
    CHAPTER_CLOSER = "chapter-closer"


@dataclass
class PageAssignment:
    """A content block assigned to a specific template."""
    template: TemplateType
    block: ContentBlock
    variant: str = ""  # e.g. "teal", "amber", "gold" for colour variety
    extra_blocks: list = field(default_factory=list)  # sidebar content etc.


class PageTemplateLibrary:
    """Reusable page templates that return HTML strings."""

    @staticmethod
    def render_chapter_opener(
        title: str, subtitle: str = "", chapter_num: int = 1,
        image_url: str = "", variant: str = "teal"
    ) -> str:
        bg_class = f"chapter-opener-{variant}"
        image_html = (
            f'<img class="opener-bg-image" src="{image_url}" alt="">'
            if image_url else ''
        )
        return f"""
        <div class="page {bg_class} chapter-opener-page">
          {image_html}
          <div class="opener-gradient"></div>
          <div class="opener-content">
            <div class="opener-number">{chapter_num:02d}</div>
            <h1 class="opener-title">{title}</h1>
            {f'<p class="opener-subtitle">{subtitle}</p>' if subtitle else ''}
            <div class="opener-rule"></div>
          </div>
        </div>
        """

    @staticmethod
    def render_text_only(body_html: str, heading: str = "") -> str:
        heading_html = f'<h2 class="text-page-heading">{heading}</h2>' if heading else ''
        return f"""
        <div class="page text-only-page">
          <div class="text-only-content">
            {heading_html}
            {body_html}
          </div>
        </div>
        """

    @staticmethod
    def render_text_with_sidebar(
        body_html: str, sidebar_html: str, heading: str = ""
    ) -> str:
        heading_html = f'<h2>{heading}</h2>' if heading else ''
        return f"""
        <div class="page text-sidebar-page">
          <div class="main-column">
            {heading_html}
            {body_html}
          </div>
          <aside class="sidebar-column">
            {sidebar_html}
          </aside>
        </div>
        """

    @staticmethod
    def render_text_two_column(body_html: str, heading: str = "") -> str:
        heading_html = (
            f'<h2 class="column-span-heading">{heading}</h2>'
            if heading else ''
        )
        return f"""
        <div class="page two-column-page">
          {heading_html}
          <div class="two-column-content">
            {body_html}
          </div>
        </div>
        """

    @staticmethod
    def render_stat_panel(
        stats: list[dict], heading: str = "", variant: str = "teal"
    ) -> str:
        """Render a page with 2-4 big statistics.

        stats: list of {"number": "22M", "label": "...", "icon": "..."}
        """
        stats_html = ""
        for stat in stats[:4]:
            icon = stat.get("icon", "")
            icon_html = (
                f'<div class="stat-icon">{icon}</div>' if icon else ''
            )
            stats_html += f"""
            <div class="stat-card">
              {icon_html}
              <div class="stat-number">{stat["number"]}</div>
              <div class="stat-label">{stat["label"]}</div>
            </div>
            """
        heading_html = f'<h2 class="stat-heading">{heading}</h2>' if heading else ''
        cols = min(len(stats), 2)
        return f"""
        <div class="page stat-panel-page stat-panel-{variant}">
          {heading_html}
          <div class="stat-grid stat-grid-{cols}">
            {stats_html}
          </div>
        </div>
        """

    @staticmethod
    def render_pullquote_break(
        quote: str, author: str = "", variant: str = "teal"
    ) -> str:
        return f"""
        <div class="page pullquote-page pullquote-{variant}">
          <div class="pullquote-deco-1"></div>
          <div class="pullquote-deco-2"></div>
          <div class="pullquote-mark">\u201C</div>
          <div class="pullquote-text">{quote}</div>
          <div class="pullquote-rule"></div>
          {f'<div class="pullquote-author">{author}</div>' if author else ''}
        </div>
        """

    @staticmethod
    def render_exercise_page(
        title: str, instructions: str, prompts: list[str],
        variant: str = "teal"
    ) -> str:
        prompts_html = "\n".join(
            f'<div class="exercise-prompt">'
            f'<span class="exercise-num">{i+1}</span>'
            f'<div class="exercise-text">{p}</div>'
            f'</div>'
            for i, p in enumerate(prompts)
        )
        return f"""
        <div class="page exercise-page exercise-{variant}">
          <div class="exercise-header">
            <div class="exercise-badge">Exercise</div>
            <h2>{title}</h2>
          </div>
          <div class="exercise-body">
            <p class="exercise-instructions">{instructions}</p>
            {prompts_html}
          </div>
        </div>
        """

    @staticmethod
    def render_checklist_page(
        title: str, items: list[str], intro: str = ""
    ) -> str:
        items_html = "\n".join(
            f'<div class="check-item">'
            f'<span class="check-box"></span>'
            f'<span class="check-text">{item}</span>'
            f'</div>'
            for item in items
        )
        return f"""
        <div class="page checklist-page">
          <div class="checklist-header">
            <h2>{title}</h2>
            {f'<p>{intro}</p>' if intro else ''}
          </div>
          <div class="checklist-body">
            {items_html}
          </div>
        </div>
        """

    @staticmethod
    def render_feature_spread(
        image_url: str, heading: str, body_html: str,
        variant: str = "teal"
    ) -> str:
        return f"""
        <div class="page feature-spread-page feature-spread-{variant}">
          <div class="feature-image-area">
            <img src="{image_url}" alt="" class="feature-image">
            <div class="feature-overlay"></div>
          </div>
          <div class="feature-text-area">
            <h2>{heading}</h2>
            {body_html}
          </div>
        </div>
        """

    @staticmethod
    def render_comparison_page(
        title: str, left_label: str, right_label: str,
        rows: list[tuple[str, str]]
    ) -> str:
        rows_html = "\n".join(
            f'<div class="compare-row">'
            f'<div class="compare-left">{left}</div>'
            f'<div class="compare-right">{right}</div>'
            f'</div>'
            for left, right in rows
        )
        return f"""
        <div class="page comparison-page">
          <h2 class="compare-title">{title}</h2>
          <div class="compare-header">
            <div class="compare-label-left">{left_label}</div>
            <div class="compare-label-right">{right_label}</div>
          </div>
          {rows_html}
        </div>
        """

    @staticmethod
    def render_timeline_page(
        title: str, steps: list[dict]
    ) -> str:
        """steps: list of {"title": "...", "desc": "...", "icon": "..."}"""
        steps_html = ""
        for i, step in enumerate(steps):
            icon = step.get("icon", "")
            steps_html += f"""
            <div class="timeline-step">
              <div class="timeline-marker">
                {f'<span class="timeline-icon">{icon}</span>' if icon else f'<span class="timeline-num">{i+1}</span>'}
              </div>
              <div class="timeline-content">
                <h3>{step["title"]}</h3>
                <p>{step["desc"]}</p>
              </div>
            </div>
            """
        return f"""
        <div class="page timeline-page">
          <h2 class="timeline-title">{title}</h2>
          <div class="timeline-track">
            {steps_html}
          </div>
        </div>
        """

    @staticmethod
    def render_chapter_closer(
        heading: str = "Key Takeaways",
        takeaways: list[str] = None,
        next_chapter: str = ""
    ) -> str:
        if takeaways is None:
            takeaways = []
        items_html = "\n".join(
            f'<li class="takeaway-item">{t}</li>' for t in takeaways
        )
        next_html = (
            f'<div class="next-chapter">Next: {next_chapter}</div>'
            if next_chapter else ''
        )
        return f"""
        <div class="page closer-page">
          <div class="closer-content">
            <div class="closer-badge">Summary</div>
            <h2>{heading}</h2>
            <ul class="takeaway-list">
              {items_html}
            </ul>
            {next_html}
          </div>
        </div>
        """

    @classmethod
    def render_page(cls, assignment: PageAssignment) -> str:
        """Render a PageAssignment using the appropriate template."""
        t = assignment.template
        b = assignment.block
        v = assignment.variant or "teal"

        if t == TemplateType.CHAPTER_OPENER:
            return cls.render_chapter_opener(
                b.heading, b.raw_text, b.metadata.get("chapter_num", 1),
                b.image_path, v
            )
        if t == TemplateType.TEXT_ONLY:
            return cls.render_text_only(b.html or f"<p>{b.raw_text}</p>", b.heading)
        if t == TemplateType.TEXT_WITH_SIDEBAR:
            sidebar = ""
            if assignment.extra_blocks:
                sidebar = assignment.extra_blocks[0].html or assignment.extra_blocks[0].raw_text
            return cls.render_text_with_sidebar(
                b.html or f"<p>{b.raw_text}</p>", sidebar, b.heading
            )
        if t == TemplateType.PULLQUOTE_BREAK:
            return cls.render_pullquote_break(
                b.raw_text, b.metadata.get("author", ""), v
            )
        if t == TemplateType.STAT_PANEL:
            stats = b.metadata.get("stats", [{"number": "—", "label": b.raw_text}])
            return cls.render_stat_panel(stats, b.heading, v)
        if t == TemplateType.EXERCISE_PAGE:
            prompts = b.metadata.get("prompts", [b.raw_text])
            return cls.render_exercise_page(
                b.heading, b.metadata.get("instructions", ""), prompts, v
            )
        if t == TemplateType.CHAPTER_CLOSER:
            takeaways = b.metadata.get("takeaways", [b.raw_text])
            return cls.render_chapter_closer(
                b.heading or "Key Takeaways", takeaways,
                b.metadata.get("next_chapter", "")
            )
        # Default: text-only
        return cls.render_text_only(b.html or f"<p>{b.raw_text}</p>", b.heading)

    @classmethod
    def render_pages(cls, assignments: list[PageAssignment]) -> str:
        """Render a full sequence of page assignments into HTML."""
        return "\n".join(cls.render_page(a) for a in assignments)


# ─── Layout Planner ───────────────────────────────────────────────────────

class LayoutPlanner:
    """Sequences classified content blocks into page templates.

    Follows editorial rhythm rules:
    1. Density alternation — no two heavy pages back-to-back
    2. 3-page rule — max 3 consecutive same-density pages
    3. Visual anchors every spread (every 2 pages)
    4. Component frequency caps (pull quotes, stats, etc.)
    5. Opening energy — chapters start with high visual energy
    6. Closing emphasis — chapters end with takeaway boxes
    """

    # Template selection map: (content_type, weight) → preferred templates
    TEMPLATE_MAP: dict[tuple[ContentType, ContentWeight], list[TemplateType]] = {
        (ContentType.CHAPTER_START, ContentWeight.HERO): [TemplateType.CHAPTER_OPENER],
        (ContentType.CHAPTER_END, ContentWeight.HERO): [TemplateType.CHAPTER_CLOSER],
        (ContentType.QUOTE, ContentWeight.MAJOR): [TemplateType.PULLQUOTE_BREAK],
        (ContentType.QUOTE, ContentWeight.SUPPORTING): [TemplateType.TEXT_WITH_SIDEBAR],
        (ContentType.STATISTIC, ContentWeight.MAJOR): [TemplateType.STAT_PANEL],
        (ContentType.STATISTIC, ContentWeight.SUPPORTING): [TemplateType.TEXT_WITH_SIDEBAR],
        (ContentType.EXERCISE, ContentWeight.MAJOR): [TemplateType.EXERCISE_PAGE],
        (ContentType.WARNING, ContentWeight.MAJOR): [TemplateType.TEXT_WITH_SIDEBAR],
        (ContentType.LIST, ContentWeight.SUPPORTING): [TemplateType.CHECKLIST_PAGE, TemplateType.TEXT_ONLY],
        (ContentType.NARRATIVE, ContentWeight.SUPPORTING): [TemplateType.TEXT_ONLY, TemplateType.TEXT_TWO_COLUMN],
    }

    # Frequency caps: max occurrences per N pages
    FREQUENCY_CAPS = {
        TemplateType.PULLQUOTE_BREAK: 4,   # Max 1 per 4 pages
        TemplateType.STAT_PANEL: 3,         # Max 1 per 3 pages
        TemplateType.EXERCISE_PAGE: 5,      # Max 1 per 5 pages
        TemplateType.FEATURE_SPREAD: 6,     # Max 1 per 6 pages
    }

    # Density classification for templates
    TEMPLATE_DENSITY = {
        TemplateType.CHAPTER_OPENER: "light",
        TemplateType.TEXT_ONLY: "heavy",
        TemplateType.TEXT_WITH_SIDEBAR: "medium",
        TemplateType.TEXT_TWO_COLUMN: "heavy",
        TemplateType.FEATURE_SPREAD: "light",
        TemplateType.STAT_PANEL: "light",
        TemplateType.PULLQUOTE_BREAK: "light",
        TemplateType.EXERCISE_PAGE: "medium",
        TemplateType.CHECKLIST_PAGE: "medium",
        TemplateType.COMPARISON_PAGE: "medium",
        TemplateType.TIMELINE_PAGE: "medium",
        TemplateType.CHAPTER_CLOSER: "medium",
    }

    # Colour rotation for variety
    COLOUR_VARIANTS = ["teal", "amber", "gold", "teal-dark"]

    def __init__(self, blocks: list[ContentBlock], theme: str = "loe"):
        self.blocks = blocks
        self.theme = theme
        self.assignments: list[PageAssignment] = []
        self.density_history: list[str] = []
        self.template_last_used: dict[TemplateType, int] = {}
        self.colour_index = 0

    def plan(self) -> list[PageAssignment]:
        """Assign content blocks to page templates following rhythm rules."""
        for block in self.blocks:
            template = self._select_template(block)
            variant = self._pick_variant(template)
            assignment = PageAssignment(
                template=template,
                block=block,
                variant=variant,
            )
            self.assignments.append(assignment)
            self._record_assignment(template)

        return self.assignments

    def _select_template(self, block: ContentBlock) -> TemplateType:
        """Pick the best template for a block, respecting rhythm rules."""
        # Get candidate templates from the map
        key = (block.content_type, block.weight)
        candidates = self.TEMPLATE_MAP.get(key, [])

        # Fallback: try just by content type with any weight
        if not candidates:
            for (ct, _), templates in self.TEMPLATE_MAP.items():
                if ct == block.content_type:
                    candidates = templates
                    break

        # Final fallback
        if not candidates:
            candidates = [TemplateType.TEXT_ONLY]

        # Score each candidate
        best = candidates[0]
        best_score = -1

        for candidate in candidates:
            score = self._score_template(candidate, block)
            if score > best_score:
                best_score = score
                best = candidate

        return best

    def _score_template(self, template: TemplateType,
                        block: ContentBlock) -> float:
        """Score a template choice (0-1) based on rhythm rules."""
        score = 0.5  # Base score

        page_num = len(self.assignments)
        density = self.TEMPLATE_DENSITY.get(template, "medium")

        # Rule 1: Density alternation — reward contrasting density
        if self.density_history:
            last_density = self.density_history[-1]
            if density != last_density:
                score += 0.2
            elif density == "heavy" and last_density == "heavy":
                score -= 0.3  # Penalise consecutive heavy pages

        # Rule 2: 3-page rule — penalise 3+ consecutive same density
        if len(self.density_history) >= 2:
            if (self.density_history[-1] == self.density_history[-2] == density):
                score -= 0.4

        # Rule 3: Frequency caps
        if template in self.FREQUENCY_CAPS:
            cap = self.FREQUENCY_CAPS[template]
            last_used = self.template_last_used.get(template, -cap)
            pages_since = page_num - last_used
            if pages_since < cap:
                score -= 0.5  # Heavy penalty for exceeding frequency cap

        # Rule 4: Content-template fit
        if block.content_type == ContentType.NARRATIVE and block.length == ContentLength.LONG:
            if template == TemplateType.TEXT_TWO_COLUMN:
                score += 0.15
        if block.content_type == ContentType.QUOTE and block.length == ContentLength.MICRO:
            if template == TemplateType.PULLQUOTE_BREAK:
                score += 0.2

        return max(0.0, min(1.0, score))

    def _pick_variant(self, template: TemplateType) -> str:
        """Pick a colour variant for variety."""
        if template in (TemplateType.TEXT_ONLY, TemplateType.TEXT_TWO_COLUMN):
            return ""  # Text pages don't need colour variants
        variant = self.COLOUR_VARIANTS[self.colour_index % len(self.COLOUR_VARIANTS)]
        self.colour_index += 1
        return variant

    def _record_assignment(self, template: TemplateType):
        """Track assignment for rhythm rules."""
        density = self.TEMPLATE_DENSITY.get(template, "medium")
        self.density_history.append(density)
        self.template_last_used[template] = len(self.assignments) - 1

    def get_plan_summary(self) -> str:
        """Return a human-readable summary of the layout plan."""
        lines = ["Layout Plan:", "=" * 50]
        for i, a in enumerate(self.assignments):
            density = self.TEMPLATE_DENSITY.get(a.template, "?")
            lines.append(
                f"  Page {i+1}: {a.template.value:20s} "
                f"[{density:6s}] "
                f"{'(' + a.variant + ')' if a.variant else '':12s} "
                f"← {a.block.content_type.value}: "
                f"{a.block.heading or a.block.raw_text[:40]}"
            )
        return "\n".join(lines)
