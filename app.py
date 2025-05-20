import streamlit as st
from fetch_news import fetch_google_news
from summarizer import summarize_article, compute_rouge
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Material color palette for reference:
PRIMARY_COLOR = "#1976d2"  # Blue 700
SECONDARY_COLOR = "#00bcd4"  # Cyan 500
TEXT_PRIMARY = "#212121"
TEXT_SECONDARY = "#757575"
BACKGROUND_LIGHT = "#fafafa"
BACKGROUND_DARK = "#121212"

st.set_page_config(
    page_title="AI News Summarizer 🚀",
    page_icon="🧠",
    layout="wide"
)

# Theme management with session state:
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

with st.sidebar:
    st.markdown("## 🎨 Theme")
    theme_toggle = st.checkbox("Dark Mode", value=st.session_state["theme"] == "dark")
    st.session_state["theme"] = "dark" if theme_toggle else "light"

# Fonts and Material UI inspired styles for light/dark themes
base_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

* {{
    font-family: 'Roboto', sans-serif;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

body {{
    background-color: {'{0}'.format(BACKGROUND_DARK) if st.session_state["theme"] == "dark" else BACKGROUND_LIGHT};
    color: {'#eeeeee' if st.session_state["theme"] == "dark" else TEXT_PRIMARY};
    margin: 0 !important;
    padding: 0 !important;
}}

h1, h2, h3, h4, h5, h6 {{
    font-weight: 500;
    margin-bottom: 0.2em;
}}

a {{
    color: {PRIMARY_COLOR};
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

.section-header {{
    background: linear-gradient(90deg, {PRIMARY_COLOR}, {SECONDARY_COLOR});
    color: white;
    padding: 2rem 1rem 1.2rem 1rem;
    border-radius: 12px;
    margin-bottom: 2.5rem;
    box-shadow: 0 4px 24px rgba(25, 118, 210, 0.3);
    user-select: none;
}}

.card {{
    background-color: {'#1e1e1e' if st.session_state["theme"] == "dark" else '#fff'};
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    padding: 1.5rem 1.5rem 1.5rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    gap: 1.5rem;
    align-items: flex-start;
    transition: box-shadow 0.3s ease;
}}

.card:hover {{
    box-shadow: 0 8px 30px rgba(25,118,210,0.35);
}}

.article-image {{
    border-radius: 10px;
    max-width: 160px;
    max-height: 120px;
    object-fit: cover;
    box-shadow: 0 2px 10px rgba(25,118,210,0.2);
}}

.article-content {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}}

.article-title {{
    font-size: 1.25rem;
    font-weight: 700;
    color: {PRIMARY_COLOR};
    margin-bottom: 0.4rem;
}}

.article-meta {{
    font-size: 0.85rem;
    color: {TEXT_SECONDARY};
    margin-bottom: 0.85rem;
}}

.article-meta a {{
    color: {SECONDARY_COLOR};
}}

.summary-section {{
    background: {'#272727' if st.session_state["theme"] == "dark" else '#f5f5f5'};
    border-radius: 10px;
    padding: 1rem 1rem 1rem 1rem;
    margin-top: 1rem;
    color: {'#ddd' if st.session_state["theme"] == "dark" else '#333'};
}}

.summary-title {{
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.button-primary {{
    position: relative;
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 24px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0 2px 6px rgba(25, 118, 210, 0.6);
}}

.button-primary:hover:not(:disabled) {{
    background-color: {SECONDARY_COLOR};
    box-shadow: 0 4px 14px rgba(0, 188, 212, 0.7);
}}

.button-primary:disabled {{
    background-color: #9e9e9e;
    cursor: not-allowed;
    box-shadow: none;
}}

button[aria-expanded="true"]::after {{
    content: "▲";
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.75rem;
    color: {PRIMARY_COLOR};
}}

button[aria-expanded="false"]::after {{
    content: "▼";
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.75rem;
    color: {PRIMARY_COLOR};
}}

footer {{
    text-align: center;
    margin-top: 3rem;
    padding: 1.5rem 0 1rem 0;
    font-size: 1rem;
    color: {TEXT_SECONDARY};
}}

.toast {{
    position: fixed;
    bottom: 1.5rem;
    right: 1.5rem;
    background-color: {SECONDARY_COLOR};
    color: white;
    padding: 1rem 1.3rem;
    border-radius: 24px;
    box-shadow: 0 4px 12px rgba(0,188,212,0.75);
    font-weight: 600;
    animation: fadein 0.5s, fadeout 0.5s 3s;
    user-select: none;
    z-index: 10000;
}}

@keyframes fadein {{
    from {{opacity: 0;}}
    to {{opacity: 1;}}
}}

@keyframes fadeout {{
    from {{opacity: 1;}}
    to {{opacity: 0;}}
}}

.toast.hide {{
    display: none;
}}

.toggle-switch {{
    position: relative;
    width: 48px;
    height: 24px;
    display: inline-block;
}}

.toggle-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    border-radius: 24px;
    transition: .4s;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    border-radius: 50%;
    transition: .4s;
}}

input:checked + .slider {{
    background-color: {PRIMARY_COLOR};
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Tooltip style for ROUGE explanation */
.tooltip {{
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted {TEXT_SECONDARY};
  cursor: help;
}}

.tooltip .tooltiptext {{
  visibility: hidden;
  width: 250px;
  background-color: {PRIMARY_COLOR};
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 0.5rem;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -125px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.85rem;
}}

.tooltip:hover .tooltiptext {{
  visibility: visible;
  opacity: 1;
}}

</style>
"""

st.markdown(base_css, unsafe_allow_html=True)

# TOAST UTILITY
def show_toast(msg, duration=4):
    toast_html = f"""
    <div class="toast" id="toast">{msg}</div>
    <script>
    setTimeout(function(){{
        var toast = document.getElementById('toast');
        if(toast) {{ toast.style.display = 'none'; }}
    }}, {duration * 1000});
    </script>
    """
    st.markdown(toast_html, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="section-header" role="banner" aria-label="App Header">
    <h1>🧠 AI News Summarizer</h1>
    <p>Summarize the world's news with AI — accessible for everyone.</p>
</div>""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("## 🔍 News Search")
    keyword = st.text_input("Enter a topic or keyword", value="Artificial Intelligence", max_chars=50)
    num_articles = st.slider("Number of articles to fetch", 1, 10, 3)
    show_images = st.checkbox("Show article images 🖼️", value=True)
    fav_mode = st.checkbox("Show Favorites Only ⭐")
    submit = st.button("Fetch & Summarize", help="Fetch news articles and generate AI summaries.")
    st.markdown("---")
    st.markdown("💡 Tip: Add your favorite articles for quick access!")

# Initialize favorites
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Extract image from URL with caching in session_state
def extract_image_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(resp.content, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return urljoin(url, og_image["content"])
        img = soup.find("img")
        if img and img.get("src"):
            return urljoin(url, img["src"])
    except:
        return None
    return None

def show_article(article, with_summary=True):
    img_url = article.get("image")
    if show_images and not img_url:
        img_url = extract_image_from_url(article["link"])
        article["image"] = img_url  # cache for future use

    st.markdown('<div class="card" role="article" tabindex="0">', unsafe_allow_html=True)
    cols = st.columns([1, 4])
    # Image column
    if show_images:
        if img_url:
            cols[0].image(img_url, use_container_width=True, caption="", output_format="PNG")
        else:
            cols[0].markdown('<div style="font-size:3rem; color: #ccc; text-align:center;">📰</div>', unsafe_allow_html=True)
    else:
        cols[0].empty()
    # Content column
    with cols[1]:
        st.markdown(f'<div class="article-title">{article["title"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="article-meta">📅 {article["published"]} | <a href="{article["link"]}" target="_blank" rel="noopener noreferrer">Read full article</a></div>',
            unsafe_allow_html=True,
        )
        with st.expander("Show Details & AI Summary", expanded=True):
            st.markdown(f'<div class="summary-section"><span class="summary-title">Original Content:</span><br>{article["summary"]}</div>', unsafe_allow_html=True)
            if with_summary:
                with st.spinner("Generating AI summary..."):
                    summary = summarize_article(article["summary"])
                    st.markdown(f'<div class="summary-section"><span class="summary-title">AI Summary:</span><br>{summary}</div>', unsafe_allow_html=True)
                    try:
                        rouge = compute_rouge(article["summary"], summary)
                        st.markdown(f"""
                        <div style="margin-top:0.5rem;">
                            <span style="font-weight:600; color: {PRIMARY_COLOR};">ROUGE-L F1:</span> <b>{rouge['rougeL']:.2f}</b>
                            <span class="tooltip" tabindex="0"> (?) 
                                <span class="tooltiptext">
                                    ROUGE-L F1 measures summary quality by the longest common subsequence overlap between original and summary.
                                </span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                    except:
                        pass
        # Favorite button
        fav_key = f"fav_{article['link']}"
        if st.button("⭐ Add to Favorites", key=fav_key):
            if article not in st.session_state.favorites:
                st.session_state.favorites.append(article)
                show_toast("Added to favorites!")
    st.markdown('</div>', unsafe_allow_html=True)

# Main logic
if submit:
    with st.spinner("Fetching news articles..."):
        try:
            articles = fetch_google_news(keyword.strip(), num_articles)
        except Exception as e:
            st.error(f"Error fetching news: {e}")
            articles = []
    if not articles:
        st.warning("No articles found for this topic. Try a different keyword.")
    else:
        content_list = st.session_state.favorites if fav_mode else articles
        for article in content_list:
            show_article(article)
elif fav_mode and st.session_state.favorites:
    st.info("Showing your ⭐ favorite articles:")
    for article in st.session_state.favorites:
        show_article(article, with_summary=False)
else:
    st.info("Type a topic & click 'Fetch & Summarize' to get news summaries!")

# Footer
st.markdown(f"""
<footer>
    Made with ❤️ by <b>Manoj Chirraboyina</b>.<br>
    <span style="color:{PRIMARY_COLOR}; font-weight:600;">Powered by Open AI and Groq.</span>
</footer>
""", unsafe_allow_html=True)

