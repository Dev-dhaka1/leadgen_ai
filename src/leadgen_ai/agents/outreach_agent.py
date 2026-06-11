from crewai import Agent, LLM
from leadgen_ai.tools.email_tool import email_tool, send_email_tool
from leadgen_ai.tools.sheets_tool import sheets_tool


def outreach_agent(llm: LLM) -> Agent:
    return Agent(
        role="Cold Outreach Copywriter",
        goal=(
            "Write complete professional cold emails for every lead. "
            "Send each email. Save every lead to Google Sheets CRM. "
            "No shortcuts. Complete every step for every lead."
        ),
        backstory=(
            "You are a cold email expert. You write full professional "
            "emails with subject lines, personalized body, and clear CTA. "
            "You always write minimum 80 words per email. "
            "After writing and sending each email you always save "
            "the lead details to Google Sheets immediately."
        ),
        tools=[email_tool, send_email_tool, sheets_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_retry_limit=2,
    )