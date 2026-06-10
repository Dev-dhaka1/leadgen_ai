import requests
from bs4 import BeautifulSoup
from crewai.tools import tool


@tool("Website Scraper Tool")
def scraper_tool(url: str) -> str:
    """Scrape a company website and extract key text content for research."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Limit output to avoid overwhelming the LLM context
        lines = [line for line in text.splitlines() if len(line.strip()) > 30]
        clean_text = "\n".join(lines[:80])

        return clean_text if clean_text else "No readable content found on this page."

    except requests.exceptions.RequestException as e:
        return f"Failed to scrape {url}: {str(e)}"