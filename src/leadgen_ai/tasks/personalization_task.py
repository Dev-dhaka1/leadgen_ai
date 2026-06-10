from crewai import Task, Agent


def personalization_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Using the company research profiles, "
            "write a personalization brief for each company.\n\n"
            "Use this exact format:\n\n"
            "COMPANY: [Name]\n"
            "CONTACT NAME: [Full name]\n"
            "CONTACT EMAIL: [Email]\n"
            "WHAT THEY DO: [One sentence]\n"
            "PAIN POINT 1: [Specific challenge they face]\n"
            "PAIN POINT 2: [Another specific challenge]\n"
            "HOOK: [One sentence using a real specific detail "
            "from their website or news]\n"
            "VALUE PROP: [How outreach solves their problem]\n"
            "TONE: [Professional or Friendly]\n\n"
            "Use real details from research. "
            "Never write generic hooks."
        ),
        expected_output=(
            "One personalization brief per company "
            "using the exact format above. "
            "All fields filled with specific real information."
        ),
        agent=agent,
    )