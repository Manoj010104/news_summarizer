import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import Runnable
from typing import Dict, Optional
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize the pipeline once
class SummarizationPipeline:
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name=model_name,
            temperature=0.3,
        )
        self.prompt_template = PromptTemplate(
            input_variables=["article"],
            template="Generate a concise 3-sentence summary of this news article:\n{article}",
        )
        self.chain = self.prompt_template | self.llm

    @lru_cache(maxsize=100)
    def summarize_article(self, article_text: str) -> Optional[str]:
        if not article_text.strip():
            return None
        try:
            response = self.chain.invoke({"article": article_text[:3000]})
            return response.content.strip()
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            return None

# Create module-level instance
pipeline = SummarizationPipeline()

# Export the function interface expected by Streamlit
def summarize_article(article_text: str) -> str:
    result = pipeline.summarize_article(article_text)
    return result if result else "Summary unavailable"

def compute_rouge(reference: str, summary: str) -> Dict[str, float]:
    try:
        from rouge_score import rouge_scorer
    except ImportError:
        raise ImportError("ROUGE scoring requires 'pip install rouge-score'")

    if not reference or not summary:
        return {k: 0.0 for k in ["rouge1", "rouge2", "rougeL"]}

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, summary)
    # Return only F1 scores for simplicity
    return {k: v.fmeasure for k, v in scores.items()}
