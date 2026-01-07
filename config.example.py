"""
Configuration File - EXAMPLE
Copy this to config.py and add your real credentials
"""

# ============================================
# TELEGRAM CONFIGURATION
# ============================================
# Get your bot token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Get your chat ID from @userinfobot on Telegram
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"


# ============================================
# JOB SEARCH CONFIGURATION
# ============================================
# Job titles to search for
JOB_TITLES = [
    "DevOps Engineer",
    "Cloud Engineer",
    # Add more job titles here
    # "Site Reliability Engineer",
    # "Platform Engineer",
]

# Location for job search
LOCATION = "India"  # Change to your preferred location

# Experience level filter
# Filters: Entry level (2) AND Associate level (3)
EXPERIENCE_LEVEL = "Entry level & Associate level"


# ============================================
# SCRAPING CONFIGURATION
# ============================================
# How often to check for new jobs (in seconds)
# 600 seconds = 10 minutes
CHECK_INTERVAL = 600

# Database file path
DATABASE_PATH = "jobs.db"

# Maximum number of jobs to scrape per search
MAX_JOBS_PER_SEARCH = 10

# Clear old jobs after this many days
CLEAR_OLD_JOBS_AFTER_DAYS = 30


# ============================================
# ADVANCED SETTINGS
# ============================================
# Enable/disable notifications
ENABLE_NOTIFICATIONS = True

# Send summary of scraping activity
SEND_SCRAPE_SUMMARY = True

# Retry on error
RETRY_ON_ERROR = True
MAX_RETRIES = 3

# Logging
LOG_FILE = "job_scraper.log"
ENABLE_LOGGING = True
