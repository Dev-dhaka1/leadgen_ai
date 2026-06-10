from crewai import Task, Agent


def company_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "For each company in the lead list:\n\n"
            "Step 1 — Scrape their website and extract:\n"
            "- Core product or service\n"
            "- Target customer type\n"
            "- Company size or stage\n"
            "- Any recent news or product launch\n\n"
            "Step 2 — Use Hunter.io to find contacts:\n"
            "- Extract domain from their URL\n"
            "- Search for verified emails\n"
            "- Get at least one contact name, role, and email\n\n"
            "Return a profile for each company. Plain text. "
            "No HTML. No made-up emails."
        ),
        expected_output=(
            "One profile per company containing: "
            "business summary, target customer, size, "
            "recent activity, and at least one real "
            "contact with name, role, and email address."
        ),
        agent=agent,
    )