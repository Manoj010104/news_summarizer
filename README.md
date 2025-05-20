# 🧠 AI News Summarizer 🚀

An intelligent, visually-enhanced AI-powered web app that fetches the latest news based on user-defined topics, generates concise AI summaries, and evaluates summary quality using ROUGE scores. Built with Streamlit, Groq's LLaMA 3 API, and LangChain for high performance and readability.

---

## 🌐 Live Demo

▶️ [Launch on Streamlit](https://newssummarizer-kdmaspgfudh9rvejtdmsn8.streamlit.app/)

---
---

## 🚀 Features

- 🔍 **Google News Integration**: Fetch top news articles based on any keyword.
- 🧠 **AI Summarization**: Summarize articles instantly using LLaMA 3 via Groq's high-speed API.
- 📊 **ROUGE Evaluation**: Assess summary quality with ROUGE-L F1 scores.
- 🖼 **Image Preview**: Auto-fetch and display article images when available.
- 🌗 **Dark/Light Theme Toggle**: Choose your preferred viewing mode.
- ⭐ **Favorites**: Save and revisit your favorite news articles.
- ⚡ **Fast Deployment**: Ready for instant deployment on Streamlit Cloud.

---

## 🛠️ Tech Stack

| Layer         | Tech                          |
|---------------|------------------------------|
| Frontend UI   | Streamlit + Custom CSS        |
| Backend       | Python                        |
| AI Model      | LLaMA 3 (via `langchain_groq`)|
| News Source   | Google News RSS (`feedparser`)|
| Summarizer    | LangChain + Groq API          |
| Metrics       | ROUGE Score                   |

---

## 📦 Installation

### 1. Clone this repository

```bash
git clone https://github.com/Manoj010104/news_summarizer.git
cd news_summarizer
```

### 2. Create a `.env` file

```env
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

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Select this repo to deploy.
4. In the **Secrets** tab, add:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```
5. Click **Deploy** and you're live!

---

## 📁 Project Structure

```text
.
├── app.py                 # Main Streamlit app
├── fetch_news.py          # Google News RSS fetcher
├── summarizer.py          # LLaMA 3 summarization + ROUGE scorer
├── requirements.txt       # All dependencies
└── README.md              # Project documentation
```

---

## 📊 Example Summary Output

```
📰 Article: Google announces new AI chip for faster model inference...

🤖 Summary:
Google unveiled a new AI chip designed for faster inference and lower latency, positioning itself to compete with NVIDIA in the edge AI space. The chip supports popular frameworks and is optimized for Google's internal workloads. Industry experts predict this may influence AI infrastructure trends globally.

📈 ROUGE-L F1: 0.87
```

---

## 👨‍💻 Author

**Manoj Chirraboyina**  
[LinkedIn](https://linkedin.com/in/manoj010104) • [Email](mailto:manoj010104@gmail.com)

---

## 🧠 Powered by

- [OpenAI](https://openai.com/)
- [Groq](https://groq.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)

---

## 📝 License

This project is licensed under the MIT License.

---

## ⭐ Show your support

If you found this project useful, please give it a ⭐ on [GitHub](https://github.com/Manoj010104/news_summarizer)!
