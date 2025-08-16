# summarizer.py
from llm_helper import llm
try:
    # if you're using LangChain's ChatGroq / messages
    from langchain_core.messages import HumanMessage, SystemMessage
    USE_MESSAGES = True
except Exception:
    USE_MESSAGES = False

SYSTEM = (
    "You are a concise technical summarizer for LinkedIn context. "
    "Return 5-7 bullet points with key insights, facts, and a practical takeaway. "
    "Keep it crisp, no fluff."
)

def summarize_text(text: str, max_bullets: int = 6) -> str:
    """Summarize long web page text into LinkedIn-friendly bullets."""
    text = text[:12000]  # safety cut
    if USE_MESSAGES:
        resp = llm.invoke([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=f"Summarize in {max_bullets} bullets:\n\n{text}")
        ])
        return resp.content
    else:
        # if llm is a simple callable that takes a prompt string
        prompt = f"{SYSTEM}\n\nSummarize in {max_bullets} bullets:\n\n{text}"
        return llm(prompt)
