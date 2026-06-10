from dotenv import load_dotenv
load_dotenv()

from leadgen_ai.crew import LeadGenCrew


def parse_query(raw: str) -> dict:
    inputs = {
        "query": raw,
        "max_leads": 3,
        "send_emails": False,
    }
    q = raw.lower()
    for word, num in [
        ("10", 10), ("ten", 10),
        ("5", 5), ("five", 5),
        ("3", 3), ("three", 3),
    ]:
        if word in q:
            inputs["max_leads"] = num
            break
    if any(w in q for w in ["send", "reach out", "contact them", "email them"]):
        inputs["send_emails"] = True
    return inputs


def main():
    print("\n🚀 LeadGen AI — Powered by CrewAI\n")
    print("Examples:")
    print("  → Find 3 HR tech SaaS startups")
    print("  → B2B fintech companies in Europe")
    print("  → Find 5 healthcare AI startups and send emails\n")

    raw = input("Enter your query: ").strip()
    if not raw:
        print("❌ No query entered.")
        return

    inputs = parse_query(raw)
    print(f"\n✅ Query   : {inputs['query']}")
    print(f"✅ Leads   : {inputs['max_leads']}")
    print(f"✅ Sending : {inputs['send_emails']}\n")

    result = LeadGenCrew().crew().kickoff(inputs=inputs)
    print("\n✅ Done!\n")
    print(result)


if __name__ == "__main__":
    main()