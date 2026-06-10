import os
import requests
from crewai.tools import tool


@tool("Serper Search Tool")
def serper_tool(query: str) -> str:
    """Search the web for business leads and company information using Serper API."""
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        return "Error: SERPER_API_KEY not found in environment variables."

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    payload = {"q": query, "num": 10}

    try:
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()

        organic = results.get("organic", [])
        if not organic:
            return "No results found."

        output = []
        for item in organic[:5]:
            title = item.get("title", "N/A")
            link = item.get("link", "N/A")
            snippet = item.get("snippet", "N/A")
            output.append(f"Title: {title}\nURL: {link}\nSnippet: {snippet}\n")

        return "\n".join(output)

    except requests.exceptions.RequestException as e:
        return f"Search failed: {str(e)}"