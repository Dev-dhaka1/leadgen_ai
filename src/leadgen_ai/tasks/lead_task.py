from crewai import Task, Agent


def lead_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Search for {max_leads} real companies matching: {query}\n\n"
            "For each company return:\n"
            "1. Company Name\n"
            "2. Website URL (real and working)\n"
            "3. One sentence: what they do\n"
            "4. One sentence: why they are a good outreach target\n\n"
            "Format as a numbered list. Plain text only. "
            "No HTML. No markdown symbols. No made-up companies."
        ),
        expected_output=(
            "Numbered list of {max_leads} real companies. "
            "Each entry: Name | URL | What they do | Why target them"
        ),
        agent=agent,
    )