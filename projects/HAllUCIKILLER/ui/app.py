import os
import streamlit as st
import streamlit.components.v1 as components

# Configure page
st.set_page_config(
    page_title="HALLUCIKILLER // 3D TACTICAL ANIME DEFENSE MATRIX",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply Cyber-Anime Deep Obsidian Theme to Streamlit Chrome
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;900&family=Rajdhani:wght@500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg-base: #050104;
    --anime-red: #ff0044;
    --anime-cyan: #00f0ff;
    --text-primary: #fdf2f4;
}

/* Force Streamlit Full Bleed & Tactical Dark Mode */
.stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Completely Eliminate Streamlit Chrome & Black Top Bar */
header[data-testid="stHeader"],
#MainMenu,
footer,
.stDeployButton,
div[data-testid="stToolbar"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    overflow: hidden !important;
}

.main, .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100vw !important;
    height: 100vh !important;
    overflow: hidden !important;
}

iframe {
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    z-index: 10 !important;
}
</style>
""", unsafe_allow_html=True)

# Build self-contained 3D Anime bundle directly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB_DIR = os.path.join(BASE_DIR, "web")

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

# Inline all assets
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

# Render Full 3D Anime Suite
components.html(
    index_html,
    height=1350,
    scrolling=True
)
