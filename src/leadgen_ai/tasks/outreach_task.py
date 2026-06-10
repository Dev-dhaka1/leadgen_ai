from crewai import Task, Agent


def outreach_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Using the personalization briefs, "
            "write and send a cold email for EVERY lead.\n\n"
            "Use this EXACT format for every email:\n\n"
            "================================================\n"
            "LEAD: [Company Name]\n"
            "CONTACT: [Full Name]\n"
            "TO: [email address]\n"
            "SUBJECT: [Specific compelling subject line]\n\n"
            "Hi [First Name],\n\n"
            "[Hook — one sentence using specific company detail]\n\n"
            "[Problem — one to two sentences about their pain point]\n\n"
            "[Solution — one to two sentences about the value offered]\n\n"
            "[CTA — ask for a 15-minute call, one sentence]\n\n"
            "Best regards,\n"
            "[Sender Name]\n\n"
            "Reply STOP to unsubscribe.\n"
            "================================================\n\n"
            "RULES — no exceptions:\n"
            "- Write the COMPLETE email every time\n"
            "- Minimum 80 words per email body\n"
            "- Plain text only — no HTML, no bullet points\n"
            "- Every email must be unique and personalized\n"
            "- After writing ALL emails call Email Saver Tool\n"
            "- Call Email Sender Tool for each email\n"
            "- Call HubSpot CRM Tool for each contact\n"
            "- Never skip any tool call"
        ),
        expected_output=(
            "Full formatted emails for every lead "
            "followed by this summary:\n\n"
            "LEAD: name | TO: email | SUBJECT: line | STATUS: sent"
        ),
        agent=agent,
    )