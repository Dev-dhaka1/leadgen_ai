from crewai import Task, Agent


def outreach_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Using the personalization briefs, "
            "complete these steps for EVERY lead:\n\n"
            "STEP 1 — Write cold email in this exact format:\n\n"
            "================================================\n"
            "LEAD: [Company Name]\n"
            "CONTACT: [Full Name]\n"
            "TO: [email address]\n"
            "SUBJECT: [Specific subject line]\n\n"
            "Hi [First Name],\n\n"
            "[Hook — specific detail about their company]\n\n"
            "[Problem — their specific pain point]\n\n"
            "[Solution — value you offer]\n\n"
            "[CTA — ask for 15 minute call]\n\n"
            "Best regards,\n"
            "[Sender Name]\n\n"
            "Reply STOP to unsubscribe.\n"
            "================================================\n\n"
            "STEP 2 — Use Email Saver Tool to save all emails\n\n"
            "STEP 3 — Use Email Sender Tool to send each email\n\n"
            "STEP 4 — Use Google Sheets CRM Tool to save each lead\n"
            "with company name, contact name, email, subject, "
            "body, status, website, and research notes\n\n"
            "RULES:\n"
            "- Complete ALL 4 steps for EVERY lead\n"
            "- Minimum 80 words per email body\n"
            "- Plain text only — no HTML\n"
            "- Every email unique and personalized\n"
            "- Never skip any step"
        ),
        expected_output=(
            "Full formatted emails for every lead. "
            "Confirmation all emails sent. "
            "Confirmation all leads saved to Google Sheets.\n\n"
            "Summary: LEAD: name | TO: email | "
            "SUBJECT: line | STATUS: sent | SHEET: saved"
        ),
        agent=agent,
    )