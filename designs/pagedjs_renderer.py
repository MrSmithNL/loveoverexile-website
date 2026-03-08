"""Paged.js + Playwright PDF renderer for long-form ebooks.

Uses the Paged.js polyfill to add CSS Paged Media features that
Chromium doesn't natively support:
- Running headers/footers with chapter titles
- Page counters (page X of Y)
- Margin boxes (@top-center, @bottom-right, etc.)
- Named strings (string-set, content(string))
- Cross-reference page numbers (target-counter)

Usage:
    from pagedjs_renderer import PagedJSRenderer

    renderer = PagedJSRenderer()
    renderer.render(
        html_content="<article>...</article>",
        css=open("ebook.css").read(),
        output_path="output.pdf",
        title="My Ebook",
        author="Author Name",
    )
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
PAGEDJS_PATH = HERE / "paged.polyfill.js"
FONT_DIR = HERE / "fonts"


class PagedJSRenderer:
    """Renders HTML to PDF using Playwright + Paged.js polyfill."""

    # CSS for running headers, footers, and page numbers
    PAGED_MEDIA_CSS = """
    /* Paged.js margin box styles */
    @page {
        size: A4;
        margin: 25mm 20mm 30mm 20mm;

        @top-center {
            content: string(chapter-title);
            font-family: 'Inter', sans-serif;
            font-size: 7.5pt;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1pt;
        }

        @bottom-center {
            content: counter(page);
            font-family: 'Inter', sans-serif;
            font-size: 8pt;
            color: #888;
        }
    }

    /* First page of document: no header, no page number */
    @page :first {
        @top-center { content: none; }
        @bottom-center { content: none; }
    }

    /* Chapter opener pages: no header, just page number */
    @page chapter-start {
        margin-top: 60mm;
        @top-center { content: none; }
    }

    /* Full-bleed pages (images, stats): no margins */
    @page full-bleed {
        margin: 0;
        @top-center { content: none; }
        @bottom-center { content: none; }
    }

    /* Set running header from chapter titles */
    h1, .chapter-title {
        string-set: chapter-title content();
    }

    /* Chapter openers */
    .chapter-opener {
        page: chapter-start;
        break-before: page;
    }

    /* Full bleed sections */
    .full-bleed, .stat-page, .photo-page {
        page: full-bleed;
        break-before: page;
    }

    /* Keep components together */
    .key-point, .callout, .tip-box, .exercise-box,
    .stat-panel, .timeline-step, .checklist-item {
        break-inside: avoid;
    }

    /* Global typography */
    body {
        orphans: 3;
        widows: 3;
    }
    """

    # JS to run after Paged.js finishes pagination
    POST_PAGINATION_JS = """
    () => {
        // Count pages and log
        const pages = document.querySelectorAll('.pagedjs_page');
        console.log(`Paged.js created ${pages.length} pages`);

        // Check for overflow in content boxes
        document.querySelectorAll('.pagedjs_page_content').forEach((page, i) => {
            if (page.scrollHeight > page.clientHeight + 5) {
                console.warn(`Page ${i+1} has overflow: ${page.scrollHeight - page.clientHeight}px`);
            }
        });

        return { pages: pages.length };
    }
    """

    def __init__(self):
        if not PAGEDJS_PATH.exists():
            raise FileNotFoundError(
                f"Paged.js polyfill not found at {PAGEDJS_PATH}. "
                f"Download it: curl -sL https://unpkg.com/pagedjs/dist/paged.polyfill.js -o {PAGEDJS_PATH}"
            )

    def render(
        self,
        html_content: str,
        css: str = "",
        output_path: str | Path = "output.pdf",
        title: str = "Ebook",
        author: str = "",
        extra_css: str = "",
        font_faces: str = "",
    ) -> Path:
        """Render HTML content to PDF using Paged.js.

        Args:
            html_content: The body HTML (without <html>/<head> wrappers)
            css: Main stylesheet content
            output_path: Where to save the PDF
            title: Document title (for PDF metadata)
            author: Author name
            extra_css: Additional CSS to append
            font_faces: @font-face declarations

        Returns:
            Path to the generated PDF
        """
        output_path = Path(output_path)

        # Build full HTML document
        full_html = self._build_document(
            html_content, css, title, author, extra_css, font_faces
        )

        # Write temp HTML
        html_path = output_path.with_suffix('.html')
        html_path.write_text(full_html, encoding='utf-8')

        # Render with Playwright
        print(f"Rendering with Paged.js + Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"file://{html_path.resolve()}")

            # Wait for fonts and resources
            page.wait_for_load_state("networkidle")

            # Wait for Paged.js to complete pagination
            # Paged.js sets a class on <html> when done
            print("  Waiting for Paged.js pagination...")
            page.wait_for_function(
                """() => {
                    return document.querySelector('.pagedjs_pages') !== null
                        || document.readyState === 'complete';
                }""",
                timeout=30000,
            )

            # Give Paged.js a moment to finish rendering
            page.wait_for_timeout(1000)

            # Run post-pagination JS
            result = page.evaluate(self.POST_PAGINATION_JS)
            print(f"  Paged.js created {result.get('pages', '?')} pages")

            # Generate PDF
            page.pdf(
                path=str(output_path),
                prefer_css_page_size=True,
                print_background=True,
                outline=True,
                tagged=True,
            )
            browser.close()

        size_kb = output_path.stat().st_size / 1024
        print(f"PDF generated: {output_path} ({size_kb:.0f} KB)")
        return output_path

    def _build_document(
        self, content: str, css: str, title: str,
        author: str, extra_css: str, font_faces: str,
    ) -> str:
        """Build the full HTML document with Paged.js script."""
        pagedjs_src = f"file://{PAGEDJS_PATH.resolve()}"

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="author" content="{author}">
<script src="{pagedjs_src}"></script>
<style>
{font_faces}
{self.PAGED_MEDIA_CSS}
{css}
{extra_css}
</style>
</head>
<body>
{content}
</body>
</html>"""
