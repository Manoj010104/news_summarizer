import streamlit as st
from fetch_news import fetch_google_news
from summarizer import summarize_article, compute_rouge
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Material color palette
PRIMARY_COLOR = "#1976d2"
SECONDARY_COLOR = "#00bcd4"
TEXT_PRIMARY = "#212121"
TEXT_SECONDARY = "#757575"
BACKGROUND_LIGHT = "#fafafa"
BACKGROUND_DARK = "#121212"

st.set_page_config(
    page_title="NovaNews 🕵️",
    page_icon="📰",
    layout="centered"
)

# Theme
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# Load styles (fallback-safe)
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header
st.markdown(f"""
<div class="section-header">
    <h1>NovaNews 📰</h1>
    <p><i>Rewriting the headlines with LLaMA 3 & Groq speed.</i></p>
</div>
""", unsafe_allow_html=True)

# Main input form in center
with st.form("news_form", clear_on_submit=False):
    st.markdown("### 🔍 Search for News")
    keyword = st.text_input("Enter a keyword or topic", value="Artificial Intelligence", max_chars=50)
    num_articles = st.slider("Number of articles", 1, 10, 3)
    show_images = st.checkbox("Show article images", value=True)
    fav_mode = st.checkbox("Show favorites only")
    submitted = st.form_submit_button("Fetch & Summarize")

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# Extract image
@st.cache_data(show_spinner=False)
def extract_image_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.content, "html.parser")

        # Prefer Open Graph image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content") and og_image["content"].startswith("http"):
            return urljoin(url, og_image["content"])

        # Fallback: First image in page
        img = soup.find("img")
        if img and img.get("src"):
            src = img["src"]
            if src.startswith("http") or src.startswith("//"):
                return urljoin(url, src)
    except Exception as e:
        print(f"Image fetch error: {e}")
    return None

def show_article(article, with_summary=True):
    img_url = article.get("image")
    if show_images and not img_url:
        img_url = extract_image_from_url(article["link"])
        article["image"] = img_url

    st.markdown('<div class="card">', unsafe_allow_html=True)
    cols = st.columns([1, 4])

    if show_images and img_url:
        cols[0].image(img_url, use_container_width=True)
    else:
        cols[0].empty()

    with cols[1]:
        st.markdown(f'<div class="article-title">{article["title"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="article-meta">📅 {article["published"]} | '
            f'<a href="{article["link"]}" target="_blank">Read full article</a></div>',
            unsafe_allow_html=True,
        )

        with st.expander("Details + Summary", expanded=True):
            st.markdown(
                f'<div class="summary-section"><b>Original:</b><br>{article["summary"]}</div>',
                unsafe_allow_html=True,
            )

            if with_summary:
                with st.spinner("Summarizing..."):
                    summary = summarize_article(article["summary"])
                    st.markdown(
                        f'<div class="summary-section"><b>AI Summary:</b><br>{summary}</div>',
                        unsafe_allow_html=True,
                    )
                    try:
                        rouge = compute_rouge(article["summary"], summary)
                        st.markdown(f"""
                        <div style='margin-top:0.5rem;'>
                            <span style='font-weight:600; color:{PRIMARY_COLOR};'>
                                ROUGE-L F1 Score: <b>{rouge['rougeL']:.2f}</b>
                            </span>
                        </div>""", unsafe_allow_html=True)
                    except:
                        pass

        fav_key = f"fav_{article['link']}"
        if st.button("⭐ Add to Favorites", key=fav_key):
            if article not in st.session_state.favorites:
                st.session_state.favorites.append(article)
                st.success("Added to favorites!")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    with st.spinner("Fetching articles..."):
        try:
            articles = fetch_google_news(keyword.strip(), num_articles)
        except Exception as e:
            st.error(f"Error: {e}")
            articles = []

    if not articles:
        st.warning("No articles found. Try another topic.")
    else:
        content_list = st.session_state.favorites if fav_mode else articles
        for article in content_list:
            show_article(article)
elif fav_mode and st.session_state.favorites:
    st.info("🌟 Showing favorites")
    for article in st.session_state.favorites:
        show_article(article, with_summary=False)
else:
    st.info("Enter a topic and hit Fetch & Summarize to begin.")

# Footer
st.markdown(f"""
<footer style="text-align:center; padding:2rem 0 1rem 0;">
    <span>Made with ❤️ by <b>Manoj Chirraboyina</b></span><br>
    <span style="color:{PRIMARY_COLOR}; font-weight:600;">Powered by Groq + LangChain</span>
</footer>
""", unsafe_allow_html=True)
