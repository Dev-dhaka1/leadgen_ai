import os
import requests
from crewai.tools import tool


@tool("Contact Finder Tool")
def hunter_tool(domain: str) -> str:
    """Find verified contact email addresses for a company domain using Hunter.io."""
    api_key = os.getenv("HUNTER_API_KEY")

    if not api_key:
        return "Error: HUNTER_API_KEY not found in environment variables."

    try:
        response = requests.get(
            "https://api.hunter.io/v2/domain-search",
            params={
                "domain": domain,
                "api_key": api_key,
                "limit": 5,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json().get("data", {})

        emails = data.get("emails", [])
        organization = data.get("organization", "Unknown Company")

        if not emails:
            return f"No verified emails found for {domain}."

        results = [
            f"Company: {organization}",
            f"Domain: {domain}",
            "Contacts found:"
        ]

        for contact in emails:
            first = contact.get("first_name", "")
            last = contact.get("last_name", "")
            email = contact.get("value", "")
            position = contact.get("position", "Unknown Role")
            confidence = contact.get("confidence", 0)
            results.append(
                f"  - {first} {last} | {position} | "
                f"{email} | Confidence: {confidence}%"
            )

        return "\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Hunter.io request failed: {str(e)}"