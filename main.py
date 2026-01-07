"""
Main Job Automation Script
Runs the scraper every 10 minutes and sends notifications
"""
import time
import sys
import os
from datetime import datetime
from linkedin_scraper import LinkedInJobScraper
from telegram_notifier import TelegramNotifier
from database import JobDatabase

# Try to import config_render (for Render.com), fallback to config (for local)
try:
    import config_render as config
except ImportError:
    import config

# Start keep-alive server for Replit (must be before JobAutomation)
if os.environ.get('REPL_ID') or os.environ.get('REPLIT_DEPLOYMENT'):
    print("🔍 Detected Replit environment")
    from keep_alive import keep_alive
    keep_alive()
    time.sleep(2)  # Give server time to start
    print("✅ Keep-alive server started")

class JobAutomation:
    def __init__(self):
        """Initialize automation components"""
        self.scraper = LinkedInJobScraper()
        self.db = JobDatabase(config.DATABASE_PATH)
        
        # Initialize Telegram notifier if configured
        if config.TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
            self.notifier = TelegramNotifier(
                config.TELEGRAM_BOT_TOKEN,
                config.TELEGRAM_CHAT_ID
            )
            self.notifications_enabled = True
        else:
            self.notifier = None
            self.notifications_enabled = False
            print("⚠️ Telegram not configured. Notifications disabled.")
    
    def run_once(self):
        """Run scraper once"""
        print("\n" + "=" * 70)
        print(f"🚀 Job Scraper Running - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        try:
            # Scrape jobs
            jobs = self.scraper.scrape_jobs(config.JOB_TITLES, config.LOCATION)
            
            print(f"\n📊 Found {len(jobs)} total jobs")
            
            # Filter new jobs
            new_jobs = self.db.get_new_jobs(jobs)
            
            print(f"✨ {len(new_jobs)} new jobs")
            
            # Log scraping activity
            self.db.log_scrape(len(jobs), len(new_jobs), config.JOB_TITLES)
            
            # Send notifications for new jobs
            if new_jobs and self.notifications_enabled and config.ENABLE_NOTIFICATIONS:
                print(f"\n📱 Sending {len(new_jobs)} notification(s)...")
                self.notifier.send_multiple_jobs(new_jobs)
                print("✅ Notifications sent!")
            elif new_jobs:
                print("\n📋 New jobs found (notifications disabled):")
                for job in new_jobs:
                    print(f"   - {job['title']} at {job['company']}")
            else:
                print("\n😴 No new jobs found")
            
            # Show stats
            stats = self.db.get_stats()
            print(f"\n📈 Database Stats:")
            print(f"   Total jobs tracked: {stats['total_jobs']}")
            print(f"   Total scrapes: {stats['total_scrapes']}")
            print(f"   Jobs in last 24h: {stats['recent_jobs']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during scraping: {str(e)}")
            
            if self.notifications_enabled:
                error_msg = f"⚠️ <b>Job Scraper Error</b>\n\n"
                error_msg += f"Error: {str(e)}\n"
                error_msg += f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.notifier.send_message(error_msg)
            
            return False
    
    def run_continuous(self):
        """Run scraper continuously every X minutes"""
        print("=" * 70)
        print("🤖 LinkedIn Job Automation Bot Started")
        print("=" * 70)
        print(f"⏰ Check interval: {config.CHECK_INTERVAL} seconds ({config.CHECK_INTERVAL/60} minutes)")
        print(f"🔍 Job titles: {', '.join(config.JOB_TITLES)}")
        print(f"📍 Location: {config.LOCATION}")
        print(f"📱 Notifications: {'Enabled' if self.notifications_enabled else 'Disabled'}")
        print("=" * 70)
        
        # Test Telegram connection
        if self.notifications_enabled:
            print("\n🔌 Testing Telegram connection...")
            if self.notifier.test_connection():
                # Send startup notification
                startup_msg = f"✅ <b>Job Scraper Started!</b>\n\n"
                startup_msg += f"🔍 Monitoring: {', '.join(config.JOB_TITLES)}\n"
                startup_msg += f"📍 Location: {config.LOCATION}\n"
                startup_msg += f"⏰ Check interval: {config.CHECK_INTERVAL/60} minutes\n"
                startup_msg += f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.notifier.send_message(startup_msg)
        
        print("\n💡 Press Ctrl+C to stop\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                print(f"\n{'='*70}")
                print(f"🔄 Iteration #{iteration}")
                
                # Run scraper
                self.run_once()
                
                # Wait for next iteration
                print(f"\n⏳ Waiting {config.CHECK_INTERVAL} seconds until next check...")
                print(f"⏰ Next check at: {self.get_next_check_time()}")
                
                time.sleep(config.CHECK_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping job scraper...")
            
            if self.notifications_enabled:
                shutdown_msg = f"⏹️ <b>Job Scraper Stopped</b>\n\n"
                shutdown_msg += f"Total iterations: {iteration}\n"
                shutdown_msg += f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                self.notifier.send_message(shutdown_msg)
            
            print("👋 Goodbye!")
            sys.exit(0)
    
    def get_next_check_time(self):
        """Calculate next check time"""
        next_time = datetime.now().timestamp() + config.CHECK_INTERVAL
        return datetime.fromtimestamp(next_time).strftime('%Y-%m-%d %H:%M:%S')
    
    def test_setup(self):
        """Test the complete setup"""
        print("🧪 Testing Job Automation Setup\n")
        
        # Test database
        print("1️⃣ Testing database...")
        stats = self.db.get_stats()
        print(f"   ✅ Database connected - {stats['total_jobs']} jobs tracked\n")
        
        # Test Telegram
        print("2️⃣ Testing Telegram...")
        if self.notifications_enabled:
            if self.notifier.test_connection():
                test_msg = "🧪 <b>Test Message</b>\n\nYour LinkedIn job scraper is working!"
                self.notifier.send_message(test_msg)
                print("   ✅ Telegram bot working!\n")
            else:
                print("   ❌ Telegram connection failed\n")
        else:
            print("   ⚠️ Telegram not configured\n")
        
        # Test scraper
        print("3️⃣ Testing LinkedIn scraper...")
        jobs = self.scraper.scrape_jobs(config.JOB_TITLES[:1], config.LOCATION)
        print(f"   ✅ Scraper working - Found {len(jobs)} jobs\n")
        
        print("=" * 70)
        print("✅ All tests completed!")
        print("=" * 70)


def main():
    """Main entry point"""
    automation = JobAutomation()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            automation.test_setup()
        elif command == "once":
            automation.run_once()
        elif command == "stats":
            stats = automation.db.get_stats()
            print(f"\n📈 Database Statistics:")
            print(f"   Total jobs tracked: {stats['total_jobs']}")
            print(f"   Total scrapes: {stats['total_scrapes']}")
            print(f"   Jobs in last 24h: {stats['recent_jobs']}")
        else:
            print("Unknown command. Use: test, once, stats, or no argument to run continuously")
    else:
        # Run continuously
        automation.run_continuous()


if __name__ == "__main__":
    main()
