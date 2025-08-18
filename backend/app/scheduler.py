# Dummy scheduler for outreach sequencing
import time

def schedule_outreach(campaign, prospects, messages):
    # In real use, use Celery or APScheduler
    for prospect, message in zip(prospects, messages):
        print(f"Scheduled message to {prospect['name']}: {message}")
        time.sleep(1)  # Simulate delay
