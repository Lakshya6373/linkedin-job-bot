"""
Keep-alive web server for Replit
This keeps the deployment active by running Flask on main thread
"""
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

# Global status for display
bot_status = {
    "running": True,
    "last_check": "Starting...",
    "jobs_found": 0
}

@app.route('/')
def home():
    return f"""
    <html>
        <head>
            <title>LinkedIn Job Bot</title>
            <meta http-equiv="refresh" content="30">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{ color: #0077b5; }}
                .status {{ 
                    padding: 10px; 
                    background: #d4edda; 
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 LinkedIn Job Bot</h1>
                <div class="status">
                    ✅ <strong>Status:</strong> Bot is running!
                </div>
                <p><strong>Monitoring:</strong> DevOps Engineer, Cloud Engineer</p>
                <p><strong>Location:</strong> India</p>
                <p><strong>Check Interval:</strong> Every 10 minutes</p>
                <p><strong>Experience Level:</strong> Entry level & Associate level</p>
                <p><strong>Last Check:</strong> {bot_status['last_check']}</p>
                <p><strong>Jobs Found:</strong> {bot_status['jobs_found']}</p>
                <hr>
                <p>Your bot is actively monitoring LinkedIn for new job postings.</p>
                <p>You'll receive Telegram notifications when new jobs are found!</p>
                <p><small>Page auto-refreshes every 30 seconds</small></p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "running", "bot": "active"}, 200

def update_status(last_check, jobs_found):
    """Update bot status for display"""
    bot_status['last_check'] = last_check
    bot_status['jobs_found'] = jobs_found

def run_flask():
    """Run Flask server on main thread"""
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def run_bot_in_background():
    """Run the bot in a background thread"""
    import time
    from datetime import datetime
    
    # Import here to avoid circular imports
    from linkedin_scraper import LinkedInJobScraper
    from telegram_notifier import TelegramNotifier
    from database import JobDatabase
    
    try:
        import config_render as config
    except ImportError:
        import config
    
    print("🤖 Starting LinkedIn Job Bot in background...")
    
    scraper = LinkedInJobScraper()
    db = JobDatabase(config.DATABASE_PATH)
    
    # Initialize Telegram notifier
    if config.TELEGRAM_BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
        notifier = TelegramNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
        
        # Test connection and send startup message
        if notifier.test_connection():
            startup_msg = "✅ <b>LinkedIn Job Bot Started on Replit!</b>\n\n"
            startup_msg += f"🔍 Monitoring: {', '.join(config.JOB_TITLES)}\n"
            startup_msg += f"📍 Location: {config.LOCATION}\n"
            startup_msg += f"⏰ Check interval: {config.CHECK_INTERVAL/60} minutes"
            notifier.send_message(startup_msg)
    else:
        notifier = None
        print("⚠️ Telegram not configured")
    
    # Main bot loop
    iteration = 0
    while True:
        try:
            iteration += 1
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n{'='*70}")
            print(f"🔄 Iteration #{iteration} - {now}")
            print(f"{'='*70}")
            
            # Scrape jobs
            jobs = scraper.scrape_jobs(config.JOB_TITLES, config.LOCATION)
            print(f"📊 Found {len(jobs)} total jobs")
            
            # Filter new jobs
            new_jobs = db.get_new_jobs(jobs)
            print(f"✨ {len(new_jobs)} new jobs")
            
            # Update status for web display
            update_status(now, len(jobs))
            
            # Log scraping activity
            db.log_scrape(len(jobs), len(new_jobs), config.JOB_TITLES)
            
            # Send notifications
            if new_jobs and notifier:
                print(f"📱 Sending {len(new_jobs)} notification(s)...")
                notifier.send_multiple_jobs(new_jobs)
                print("✅ Notifications sent!")
            elif new_jobs:
                print(f"📋 {len(new_jobs)} new jobs found (notifications disabled)")
            else:
                print("😴 No new jobs found")
            
            # Show stats
            stats = db.get_stats()
            print(f"\n📈 Database Stats:")
            print(f"   Total jobs tracked: {stats['total_jobs']}")
            print(f"   Jobs in last 24h: {stats['recent_jobs']}")
            
            # Wait for next iteration
            print(f"\n⏳ Waiting {config.CHECK_INTERVAL} seconds until next check...")
            time.sleep(config.CHECK_INTERVAL)
            
        except Exception as e:
            print(f"❌ Error in bot loop: {str(e)}")
            if notifier:
                error_msg = f"⚠️ <b>Bot Error</b>\n\n{str(e)}"
                notifier.send_message(error_msg)
            time.sleep(60)  # Wait 1 minute before retrying

def start_replit_bot():
    """Start bot in background thread, Flask on main thread"""
    print("🚀 Starting Replit bot with keep-alive server...")
    
    # Start bot in background thread
    bot_thread = Thread(target=run_bot_in_background)
    bot_thread.daemon = True
    bot_thread.start()
    print("✅ Bot thread started")
    
    # Run Flask on main thread (blocks here)
    run_flask()
