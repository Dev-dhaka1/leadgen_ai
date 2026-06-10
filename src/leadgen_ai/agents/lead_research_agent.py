from crewai import Agent, LLM
from leadgen_ai.tools.serper_tool import serper_tool


def lead_research_agent(llm: LLM) -> Agent:
    return Agent(
        role="Lead Research Specialist",
        goal=(
            "Find exactly {max_leads} real business companies "
            "matching the query: {query}. "
            "Return a clean numbered list with company name, "
            "website URL, and what they do."
        ),
        backstory=(
            "You are a senior B2B lead researcher with 10 years experience. "
            "You find real companies using search engines. "
            "You only return real companies with real websites. "
            "You never make up company names or URLs. "
            "You return clean structured output only."
        ),
        tools=[serper_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_retry_limit=2,
    )