# 🗞️ NovaNews – Rewriting the headlines with LLaMA 3 & Groq speed 🚀

NovaNews is a sleek, AI-powered web app that delivers **ultra-fast news summaries** using **Groq's blazing LLaMA 3 models**. It intelligently fetches trending articles, distills them into crisp summaries, and evaluates their quality using ROUGE metrics — all within a beautifully themed interface built on Streamlit.

---

## 🌐 Live App
▶️ [Try NovaNews](https://newssummarizer-kdmaspgfudh9rvejtdmsn8.streamlit.app/)  

---

## 🚀 Features

- 🔍 **Search Any Topic**: Instantly fetch articles via Google News RSS.
- 🧠 **AI Summarization (LLaMA 3)**: Powered by LangChain and Groq's ultra-fast inference API.
- 📊 **ROUGE-L Scoring**: Quantitative evaluation of summary quality.
- 🌗 **Dark & Light Themes**: Adaptive design with Material-inspired styles.
- ⭐ **Favorites**: Save the best articles with one click.
- 🖼 **Auto Image Preview**: Pulls article thumbnails from open graph metadata.
- ⚡ **Fast Deployment**: Deployable via Streamlit Cloud in under 2 minutes.

---

## 🛠️ Tech Stack

| Layer         | Tech                             |
|---------------|----------------------------------|
| Frontend UI   | Streamlit + Custom Material CSS  |
| Backend       | Python                           |
| AI Model      | LLaMA 3 (via `langchain_groq`)   |
| News Feed     | Google News RSS (`feedparser`)   |
| Metrics       | ROUGE Score (`rouge-score`)      |

---

## 📦 Installation

### 1. Clone this repo

```bash
git clone https://github.com/manoj010104/news_summarizer.git
cd news_summarizer
```

### 2. Create a `.env` file

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run locally

```bash
streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Deploy your repo as a new app.
4. In the **Secrets** section, add:
    ```toml
    GROQ_API_KEY = "your_actual_groq_api_key_here"
    ```
5. Click **Deploy** — your NovaNews app is live!

---

## 📁 Project Structure

```
.
├── app.py                 # Streamlit app logic and UI
├── fetch_news.py          # Google News article fetcher
├── summarizer.py          # LLaMA 3 summarizer + ROUGE score
├── requirements.txt       # All dependencies
└── README.md              # You're here!
```

---

## ✨ Sample Output

```
🔍 Topic: Artificial Intelligence

📰 Article: OpenAI releases GPT-5 preview to selected partners

🤖 AI Summary:
OpenAI has rolled out a preview of GPT-5 to a limited group of enterprise partners, focusing on better reasoning, longer context, and faster inference. This marks a strategic step in its alignment with Groq’s hardware acceleration. Early benchmarks suggest significant gains over GPT-4.

📈 ROUGE-L F1 Score: 0.89
```

---

## 👨‍💻 Author

**Manoj Chirraboyina**  
[LinkedIn](https://linkedin.com/in/manoj010104)

---

## 🧠 Powered by

- Groq
- LangChain
- Streamlit
- OpenAI

---

## 📝 License

This project is licensed under the MIT License.

---

## ⭐ Show Some ❤️

If NovaNews helped you save time or inspired your own project, give it a ⭐ on [GitHub](https://github.com/manoj010104/news_summarizer)!
