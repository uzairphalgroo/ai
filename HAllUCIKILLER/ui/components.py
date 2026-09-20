"""
2027 Futuristic Cybernetic Glassmorphic UI Components and Canvas Animations for Hallucikiller.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")


def get_bundled_2027_dashboard_html() -> str:
    """
    Inlines HTML, CSS, Canvas animations, Audio synthesizer, and Chart.js app
    into a self-contained single-page bundle for Streamlit rendering.
    """
    css_path = os.path.join(WEB_DIR, "css", "style.css")
    canvas_path = os.path.join(WEB_DIR, "js", "canvas.js")
    audio_path = os.path.join(WEB_DIR, "js", "audio.js")
    app_path = os.path.join(WEB_DIR, "js", "app.js")
    index_path = os.path.join(WEB_DIR, "index.html")

    css_content = ""
    canvas_content = ""
    audio_content = ""
    app_content = ""
    index_html = ""

    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()

    if os.path.exists(canvas_path):
        with open(canvas_path, "r", encoding="utf-8") as f:
            canvas_content = f.read()

    if os.path.exists(audio_path):
        with open(audio_path, "r", encoding="utf-8") as f:
            audio_content = f.read()

    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            app_content = f.read()

    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()

    # Replace external links with inlined content
    index_html = index_html.replace(
        '<link rel="stylesheet" href="css/style.css" />',
        f"<style>\n{css_content}\n</style>"
    )
    index_html = index_html.replace(
        '<script src="js/audio.js"></script>',
        f"<script>\n{audio_content}\n</script>"
    )
    index_html = index_html.replace(
        '<script src="js/canvas.js"></script>',
        f"<script>\n{canvas_content}\n</script>"
    )
    index_html = index_html.replace(
        '<script src="js/app.js"></script>',
        f"<script>\n{app_content}\n</script>"
    )

    return index_html


def get_cyber_theme_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg-base: #030712;
    --bg-card: rgba(14, 18, 36, 0.72);
    --neon-cyan: #00f2fe;
    --neon-purple: #7928ca;
    --neon-pink: #ff0080;
    --neon-green: #00f5a0;
    --neon-amber: #ff9900;
    --neon-red: #ff3366;
    --text-primary: #f0f4fc;
    --text-muted: #8e9bb4;
}

/* Force Streamlit Full Bleed & Dark Obsidian Mode */
.stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

header[data-testid="stHeader"] {
    background-color: rgba(3, 7, 18, 0.85) !important;
    backdrop-filter: blur(12px) !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

/* Remove default iframe borders */
iframe {
    border: none !important;
    border-radius: 16px !important;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.6) !important;
}
</style>
"""
