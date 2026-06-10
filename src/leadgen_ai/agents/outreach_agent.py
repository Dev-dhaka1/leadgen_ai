from crewai import Agent, LLM
from leadgen_ai.tools.email_tool import email_tool, send_email_tool
from leadgen_ai.tools.hubspot_tool import hubspot_tool


def outreach_agent(llm: LLM) -> Agent:
    return Agent(
        role="Cold Outreach Copywriter",
        goal=(
            "Write a full professional cold email for every lead. "
            "Save all emails. Send each email. "
            "Add each contact to HubSpot CRM."
        ),
        backstory=(
            "You are a cold email expert who has written thousands "
            "of B2B emails. You always write the COMPLETE email — "
            "never a summary, never a placeholder. "
            "Every email has: greeting, personalized opening, "
            "problem statement, value proposition, CTA, sign-off. "
            "Minimum 80 words per email. You always use the tools "
            "to save, send, and log every email without skipping any."
        ),
        tools=[email_tool, send_email_tool, hubspot_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
        max_retry_limit=2,
    )