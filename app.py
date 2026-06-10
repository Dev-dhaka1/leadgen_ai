import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_SERVER_NOFILE"] = "65536"

import streamlit as st
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="LeadGen AI",
    page_icon="🚀",
    layout="wide"
)

# ── Header ──────────────────────────────────────
st.title("🚀 LeadGen AI")
st.markdown(
    "Automated Lead Generation and Cold Outreach — Powered by CrewAI"
)

# ── Sidebar ──────────────────────────────────────
with st.sidebar:
    st.header("⚙️ System Status")

    provider = os.getenv("MODEL_PROVIDER", "ollama").upper()
    st.markdown(f"**Model:** {provider}")

    checks = {
        "Serper Search": "SERPER_API_KEY",
        "Hunter Contacts": "HUNTER_API_KEY",
        "SMTP Email": "SMTP_USER",
        "HubSpot CRM": "HUBSPOT_API_KEY",
    }
    for label, key in checks.items():
        icon = "✅" if os.getenv(key) else "❌"
        st.markdown(f"{icon} {label}")

    st.markdown("---")
    st.markdown("**Output saved to:**")
    st.code("src/leadgen_ai/data/")

# ── Input ────────────────────────────────────────
st.header("1️⃣ Define Your Target Market")

query = st.text_area(
    "What kind of companies are you looking for?",
    placeholder=(
        "Examples:\n"
        "• B2B SaaS startups in HR tech\n"
        "• Fintech companies in Europe\n"
        "• Healthcare AI startups in the US"
    ),
    height=100,
)

col1, col2 = st.columns(2)
with col1:
    max_leads = st.selectbox(
        "Number of leads", [3, 5, 10], index=0
    )
with col2:
    send_emails = st.checkbox(
        "Send cold emails automatically", value=False
    )

# ── Run ──────────────────────────────────────────
run = st.button(
    "🚀 Start Lead Generation",
    type="primary",
    disabled=not query.strip()
)

if run:
    with st.spinner("🤖 AI agents working... please wait"):
        try:
            from leadgen_ai.crew import LeadGenCrew

            inputs = {
                "query": query.strip(),
                "max_leads": max_leads,
                "send_emails": send_emails,
            }

            result = LeadGenCrew().crew().kickoff(inputs=inputs)

            st.success("✅ Lead generation complete!")
            st.header("2️⃣ Results")

            # Clean output
            output = str(result)
            output = re.sub(r'<think>[\s\S]*?</think>', '', output)
            output = re.sub(r'<[^>]+>', '', output)
            output = re.sub(r'\n{3,}', '\n\n', output)

            st.text_area("Generated Emails", output, height=600)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ── Log Table ─────────────────────────────────────
st.header("3️⃣ Sent Emails Log")

log_path = os.path.join(
    os.path.dirname(__file__),
    "src", "leadgen_ai", "data", "sent_emails_log.csv"
)

if os.path.exists(log_path):
    df = pd.read_csv(log_path)
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
        sent = len(df[df["status"] == "sent"])
        st.metric("Emails Sent", sent)
else:
    st.info(
        "No emails logged yet. "
        "Run a campaign above to see results here."
    )