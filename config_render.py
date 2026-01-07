import os

# ============================================
# TELEGRAM CONFIGURATION
# ============================================
# Read from environment variables (Render) or use defaults (local)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE')

# ============================================
# JOB SEARCH CONFIGURATION
# ============================================
JOB_TITLES = [
    "DevOps Engineer",
    "Cloud Engineer",
]

LOCATION = "India"
EXPERIENCE_LEVEL = "Entry level & Associate level"

# ============================================
# SCRAPING CONFIGURATION
# ============================================
CHECK_INTERVAL = 600  # 10 minutes
DATABASE_PATH = "jobs.db"
MAX_JOBS_PER_SEARCH = 10
CLEAR_OLD_JOBS_AFTER_DAYS = 30

# ============================================
# ADVANCED SETTINGS
# ============================================
ENABLE_NOTIFICATIONS = True
SEND_SCRAPE_SUMMARY = True
RETRY_ON_ERROR = True
MAX_RETRIES = 3
LOG_FILE = "job_scraper.log"
ENABLE_LOGGING = True
