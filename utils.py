import requests
from bs4 import BeautifulSoup

def summarize_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Simple text extraction
        paragraphs = soup.find_all('p')
        text = " ".join(p.get_text() for p in paragraphs[:5])  # first 5 paragraphs
        summary = text[:300] + "..." if len(text) > 300 else text

        return summary
    except Exception as e:
        return f"Error summarizing URL: {str(e)}"
