import os
import re
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_NOFILE"] = "65536"
os.environ["CREWAI_STORAGE_DIR"] = "/tmp/crewai"

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="LeadGen AI",
    page_icon="🚀",
    layout="wide"
)

# ── Header ────────────────────────────────────────
st.title("🚀 LeadGen AI")
st.markdown(
    "Automated Lead Generation and Cold Outreach — Powered by CrewAI + OpenAI"
)

# ── Sidebar ───────────────────────────────────────
with st.sidebar:
    st.header("⚙️ System Status")

    provider = os.getenv("MODEL_PROVIDER", "openai").upper()
    model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    st.markdown(f"**Model:** {provider} — {model}")

    st.markdown("---")
    st.markdown("**API Connections:**")

    checks = {
        "🔍 Serper Search": "SERPER_API_KEY",
        "📧 Hunter Contacts": "HUNTER_API_KEY",
        "📨 Resend Email": "RESEND_API_KEY",
        "📊 Google Sheets CRM": "GOOGLE_SHEET_ID",
    }
    for label, key in checks.items():
        icon = "✅" if os.getenv(key) else "❌"
        st.markdown(f"{icon} {label}")

    st.markdown("---")

    # Google Sheet link
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if sheet_id:
        sheet_url = (
            f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        )
        st.markdown("**📊 Live CRM:**")
        st.markdown(f"[Open Google Sheets]({sheet_url})")
    else:
        st.markdown("❌ Google Sheet not configured")

    st.markdown("---")

    # Resend sender info
    from_email = os.getenv("RESEND_FROM_EMAIL", "Not configured")
    st.markdown(f"**📨 Sending From:**")
    st.markdown(f"`{from_email}`")

    st.markdown("---")
    st.markdown("**Output Files:**")
    st.code("src/leadgen_ai/data/")

# ── Input Section ─────────────────────────────────
st.header("1️⃣ Define Your Target Market")

query = st.text_area(
    "What kind of companies are you looking for?",
    placeholder=(
        "Examples:\n"
        "• B2B SaaS startups in HR tech\n"
        "• Fintech companies in Europe\n"
        "• Healthcare AI startups in the US\n"
        "• Recruitment agencies in UK"
    ),
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    max_leads = st.selectbox(
        "Number of leads to find",
        [3, 5, 10],
        index=0
    )
with col2:
    send_emails = st.checkbox(
        "Auto-send cold emails to prospects",
        value=False
    )

# ── Run Button ────────────────────────────────────
st.markdown("---")
run = st.button(
    "🚀 Start Lead Generation",
    type="primary",
    disabled=not query.strip()
)

if run:
    with st.spinner(
        "🤖 AI agents working... "
        "Finding leads, researching companies, "
        "writing emails. Please wait 2-5 minutes..."
    ):
        try:
            from leadgen_ai.crew import LeadGenCrew

            inputs = {
                "query": query.strip(),
                "max_leads": max_leads,
                "send_emails": send_emails,
            }

            result = LeadGenCrew().crew().kickoff(inputs=inputs)

            st.success("✅ Lead generation complete!")

            # ── Results ───────────────────────────
            st.header("2️⃣ Generated Emails")

            output = str(result)
            output = re.sub(
                r'<think>[\s\S]*?</think>', '', output
            )
            output = re.sub(r'<[^>]+>', '', output)
            output = re.sub(r'\n{3,}', '\n\n', output)
            output = output.strip()

            st.text_area(
                "AI Generated Cold Emails",
                output,
                height=600
            )

            # ── Quick Stats ───────────────────────
            st.markdown("---")
            st.header("3️⃣ Campaign Summary")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Leads Found", max_leads)
            with col2:
                st.metric(
                    "Emails Written", max_leads
                )
            with col3:
                status = "Sent ✅" if send_emails else "Draft Only"
                st.metric("Email Status", status)

            if send_emails:
                st.success(
                    "📨 Emails sent via Resend. "
                    "Check your Google Sheet for all leads."
                )
                if sheet_id:
                    st.markdown(
                        f"**[📊 View All Leads in Google Sheets]"
                        f"({sheet_url})**"
                    )
            else:
                st.info(
                    "💡 Emails were written but not sent. "
                    "Enable 'Auto-send cold emails' to send them."
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.markdown("**Possible fixes:**")
            st.markdown("- Check all API keys in secrets/env")
            st.markdown(
                "- Make sure google_credentials.json is present"
            )
            st.markdown(
                "- Check Resend domain is verified"
            )

# ── Sent Emails Log ───────────────────────────────
st.markdown("---")
st.header("4️⃣ Sent Emails Log")

log_path = os.path.join(
    os.path.dirname(__file__),
    "src", "leadgen_ai", "data", "sent_emails_log.csv"
)

if os.path.exists(log_path):
    df = pd.read_csv(log_path)

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total = len(df)
        st.metric("Total Campaigns Run", total)
    with col2:
        sent = len(df[df["status"] == "sent"])
        st.metric("Emails Sent", sent)
    with col3:
        failed = len(df[df["status"] != "sent"])
        st.metric("Failed", failed)

    st.dataframe(df, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            "leads_log.csv",
            "text/csv",
        )
    with col2:
        if sheet_id:
            st.markdown(
                f"[📊 View in Google Sheets]({sheet_url})"
            )
else:
    st.info(
        "No emails logged yet. "
        "Run a campaign above to see results here."
    )

# ── How It Works ──────────────────────────────────
st.markdown("---")
with st.expander("ℹ️ How LeadGen AI Works"):
    st.markdown("""
**Step 1 — Lead Research**
AI searches for companies matching your target market using Serper.

**Step 2 — Company Research**
AI visits each company website and extracts business intelligence.

**Step 3 — Contact Finding**
AI finds verified contact emails using Hunter.io.

**Step 4 — Personalization**
AI creates personalized outreach hooks for each company.

**Step 5 — Email Writing**
AI writes a complete professional cold email for each lead.

**Step 6 — Email Sending**
Emails sent via Resend using your verified domain.

**Step 7 — CRM Logging**
Every lead saved to Google Sheets automatically.

All of this happens automatically in 2-5 minutes.
    """)