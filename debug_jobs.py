"""
Debug script to check what jobs are being scraped
"""
from linkedin_scraper import LinkedInJobScraper
import config

scraper = LinkedInJobScraper()

print("=" * 70)
print("🔍 Scraping LinkedIn Jobs - DEBUG MODE")
print("=" * 70)

jobs = scraper.scrape_jobs(config.JOB_TITLES[:1], config.LOCATION)

print(f"\n📊 Total jobs found: {len(jobs)}")
print("=" * 70)

for i, job in enumerate(jobs, 1):
    print(f"\n📋 Job #{i}")
    print(f"   Job ID: {job['job_id']}")
    print(f"   Title: {job['title']}")
    print(f"   Company: {job['company']}")
    print(f"   Location: {job['location']}")
    print(f"   Posted: {job['posted_date']}")
    print(f"   URL: {job['url']}")
    print(f"   Search Term: {job['search_term']}")
    print("-" * 70)

if jobs:
    print("\n🧪 Testing Telegram notification with first job...")
    from telegram_notifier import TelegramNotifier
    
    notifier = TelegramNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
    success = notifier.send_job_alert(jobs[0])
    
    if success:
        print("✅ Notification sent! Check your Telegram.")
    else:
        print("❌ Failed to send notification.")
