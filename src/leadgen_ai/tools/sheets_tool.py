import os
import json
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from crewai.tools import tool


def get_sheet():
    """Connect to Google Sheet and return the worksheet."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds_file = os.getenv(
        "GOOGLE_CREDENTIALS_FILE",
        "google_credentials.json"
    )
    sheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID not set in .env")

    # Support both file path and JSON string in env
    if os.path.exists(creds_file):
        creds = Credentials.from_service_account_file(
            creds_file, scopes=scopes
        )
    else:
        raise FileNotFoundError(
            f"google_credentials.json not found. "
            f"Download it from Google Cloud Console."
        )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    return sheet.sheet1


@tool("Google Sheets CRM Tool")
def sheets_tool(
    company: str,
    prospect_name: str,
    email: str,
    subject: str,
    body: str,
    status: str = "contacted",
    website: str = "",
    notes: str = ""
) -> str:
    """Save lead contact information to Google Sheets CRM."""

    try:
        worksheet = get_sheet()

        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            company,
            prospect_name,
            email,
            subject,
            body[:500],  # Limit body length in sheet
            status,
            website,
            notes[:300],
        ]

        worksheet.append_row(row)

        return (
            f"✅ Lead saved to Google Sheets: "
            f"{prospect_name} at {company}"
        )

    except Exception as e:
        return f"❌ Google Sheets error: {str(e)}"