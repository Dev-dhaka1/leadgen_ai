import schedule
import time
from dotenv import load_dotenv
from leadgen_ai.crew import LeadGenCrew

load_dotenv()

QUERY = "SaaS startups in HR tech"


def run_leadgen():
    print(f"\n⏰ Scheduled run started for query: '{QUERY}'")
    try:
        result = LeadGenCrew().crew().kickoff(inputs={"query": QUERY})
        print("✅ Scheduled run complete.")
        print(result)
    except Exception as e:
        print(f"❌ Scheduled run failed: {str(e)}")


# --- Set your schedule here ---
schedule.every().day.at("09:00").do(run_leadgen)   # every day at 9am
# schedule.every().monday.at("09:00").do(run_leadgen)  # every Monday
# schedule.every(2).hours.do(run_leadgen)              # every 2 hours

print("⏰ Scheduler running. Press Ctrl+C to stop.")
print(f"Next run: {schedule.next_run()}")

while True:
    schedule.run_pending()
    time.sleep(60)