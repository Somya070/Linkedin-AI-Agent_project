from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not found! Please set it in your .env or Streamlit Secrets.")

# Initialize the LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)

# Optional: simple test if run directly
if __name__ == "__main__":
    user_input = input("Enter your question: ")
    response = llm.invoke(user_input)
    print(response.content)
