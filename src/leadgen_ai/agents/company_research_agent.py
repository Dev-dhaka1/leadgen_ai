from crewai import Agent, LLM
from leadgen_ai.tools.scraper_tool import scraper_tool
from leadgen_ai.tools.hunter_tool import hunter_tool


def company_research_agent(llm: LLM) -> Agent:
    return Agent(
        role="Company Intelligence Analyst",
        goal=(
            "For each company from the lead list: "
            "visit their website, extract business intelligence, "
            "and find at least one verified contact email."
        ),
        backstory=(
            "You are a business intelligence analyst. "
            "You visit company websites and extract: "
            "what they do, who they serve, their size, recent news. "
            "You also find real verified contact emails using Hunter.io. "
            "You return structured profiles. No guessing."
        ),
        tools=[scraper_tool, hunter_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
        max_retry_limit=2,
    )