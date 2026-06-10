import os
import re
from dotenv import load_dotenv
load_dotenv()

from crewai import Crew, Process, LLM
from leadgen_ai.agents.lead_research_agent import lead_research_agent
from leadgen_ai.agents.company_research_agent import company_research_agent
from leadgen_ai.agents.personalization_agent import personalization_agent
from leadgen_ai.agents.outreach_agent import outreach_agent
from leadgen_ai.tasks.lead_task import lead_research_task
from leadgen_ai.tasks.research_task import company_research_task
from leadgen_ai.tasks.personalization_task import personalization_task
from leadgen_ai.tasks.outreach_task import outreach_task


def get_llm() -> LLM:
    provider = os.getenv("MODEL_PROVIDER", "ollama").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not set in .env"
            )
        print(f"✅ Using OpenAI — {model}")
        return LLM(
            model=f"openai/{model}",
            api_key=api_key,
            temperature=0.3,
        )

    # Default — Ollama local
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"✅ Using Ollama — {model}")
    return LLM(
        model=f"ollama/{model}",
        base_url=base_url,
        temperature=0.3,
        num_ctx=8192,
    )


class LeadGenCrew:
    def crew(self) -> Crew:
        llm = get_llm()

        agents = [
            lead_research_agent(llm),
            company_research_agent(llm),
            personalization_agent(llm),
            outreach_agent(llm),
        ]

        tasks = [
            lead_research_task(agents[0]),
            company_research_task(agents[1]),
            personalization_task(agents[2]),
            outreach_task(agents[3]),
        ]

        return Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )
        
        
# import os
# from dotenv import load_dotenv
# load_dotenv()

# from crewai import Crew, Process, LLM
# from leadgen_ai.agents.lead_research_agent import lead_research_agent
# from leadgen_ai.agents.company_research_agent import company_research_agent
# from leadgen_ai.agents.personalization_agent import personalization_agent
# from leadgen_ai.agents.outreach_agent import outreach_agent
# from leadgen_ai.tasks.lead_task import lead_research_task
# from leadgen_ai.tasks.research_task import company_research_task
# from leadgen_ai.tasks.personalization_task import personalization_task
# from leadgen_ai.tasks.outreach_task import outreach_task


# def get_llm() -> LLM:
#     groq_key = os.getenv("GROQ_API_KEY")
#     if groq_key:
#         print("✅ Using Groq — llama-3.3-70b-versatile")
#         return LLM(
#             model="groq/llama-3.3-70b-versatile",
#             api_key=groq_key,
#             base_url="https://api.groq.com/openai/v1",
#             temperature=0.3,
#         )
#     # Fallback to Ollama if Groq key not set
#     print("⚠️ Groq key not found — falling back to Ollama")
#     return LLM(
#         model="ollama/llama3.2",
#         base_url="http://localhost:11434",
#         temperature=0.3,
#     )


# class LeadGenCrew:
#     def crew(self) -> Crew:
#         llm = get_llm()

#         agents = [
#             lead_research_agent(llm),
#             company_research_agent(llm),
#             personalization_agent(llm),
#             outreach_agent(llm),
#         ]

#         tasks = [
#             lead_research_task(agents[0]),
#             company_research_task(agents[1]),
#             personalization_task(agents[2]),
#             outreach_task(agents[3]),
#         ]

#         return Crew(
#             agents=agents,
#             tasks=tasks,
#             process=Process.sequential,
#             verbose=True,
#         )