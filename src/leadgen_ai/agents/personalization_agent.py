from crewai import Agent, LLM


def personalization_agent(llm: LLM) -> Agent:
    return Agent(
        role="Outreach Personalization Strategist",
        goal=(
            "For each company, create a personalization brief "
            "with a specific hook, two pain points, "
            "a value proposition, and recommended tone."
        ),
        backstory=(
            "You are a growth strategist who writes outreach for "
            "top B2B companies. You use real research details — "
            "never generic lines. Every hook references something "
            "specific about the company. You know what pain points "
            "each type of business faces."
        ),
        tools=[],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_retry_limit=2,
    )