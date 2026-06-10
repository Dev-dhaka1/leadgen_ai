import os
import requests
from crewai.tools import tool


@tool("HubSpot CRM Tool")
def hubspot_tool(
    email: str,
    first_name: str,
    last_name: str,
    company: str,
    website: str = "",
    notes: str = ""
) -> str:
    """Create a new contact in HubSpot CRM after finding a lead."""
    api_key = os.getenv("HUBSPOT_API_KEY")

    if not api_key:
        return "Error: HUBSPOT_API_KEY not found in environment variables."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # --- Create Contact ---
    contact_payload = {
        "properties": {
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
            "company": company,
            "website": website,
            "hs_lead_status": "NEW",
            "notes_last_updated": notes,
        }
    }

    try:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/contacts",
            headers=headers,
            json=contact_payload,
            timeout=10,
        )

        if response.status_code == 409:
            return f"⚠️ Contact {email} already exists in HubSpot."

        response.raise_for_status()
        contact_id = response.json().get("id")
        return f"✅ Contact created in HubSpot: {first_name} {last_name} at {company} (ID: {contact_id})"

    except requests.exceptions.RequestException as e:
        return f"❌ HubSpot API error: {str(e)}"