"""HTML page building utilities for CraftX.py."""

from typing import Optional


def build_page(title: str, content: str, output: str = "page.html",
               css_styles: Optional[str] = None) -> str:
    """Build a simple HTML page with the given content.

    Args:
        title: Page title
        content: HTML content for the body
        output: Output filename
        css_styles: Optional CSS styles to include

    Returns:
        Success message with filename
    """
    default_styles = """
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            padding: 2rem;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 { color: #1B1F3B; }
        .highlight { color: #00F0FF; }
        .warning { color: #FFB300; }
        code {
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
        }
    """

    styles = css_styles or default_styles

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{styles}</style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
</body>
</html>"""

    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(html)
        return f"✅ Page saved as {output}"
    except IOError as e:
        return f"❌ Failed to save page: {str(e)}"


def build_craftx_page(title: str, content: str, output: str = "craftx_page.html") -> str:
    """Build an HTML page with CraftX.py branding.

    Args:
        title: Page title
        content: HTML content
        output: Output filename

    Returns:
        Success message with filename
    """
    craftx_styles = """
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #1B1F3B;
            color: #F0F0F0;
            margin: 0;
            padding: 2rem;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        .logo {
            color: #00F0FF;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .tagline {
            color: #FFB300;
            font-style: italic;
        }
        .content {
            max-width: 800px;
            margin: 0 auto;
        }
        h1, h2, h3 { color: #00F0FF; }
        .highlight { color: #FFB300; }
        code {
            background: #2E2E2E;
            color: #00F0FF;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'JetBrains Mono', monospace;
        }
        .cta {
            background: #00F0FF;
            color: #1B1F3B;
            padding: 1rem 2rem;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 1rem 0;
        }
    """

    branded_content = f"""
    <div class="header">
        <div class="logo">CraftX.py</div>
        <div class="tagline">Python-native intelligence, modular by design.</div>
    </div>
    <div class="content">
        {content}
    </div>
    """

    return build_page(title, branded_content, output, craftx_styles)
