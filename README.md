# 🤖 LinkedIn Job Automation Bot

Automatically scrapes LinkedIn for DevOps and Cloud Engineer jobs every 10 minutes and sends Telegram notifications for new postings.

## 🌟 Features

- ✅ Scrapes LinkedIn for job postings
- ✅ Searches for DevOps Engineer & Cloud Engineer roles
- ✅ Runs automatically every 10 minutes
- ✅ Sends instant Telegram notifications
- ✅ Tracks seen jobs to avoid duplicates
- ✅ SQLite database for job history
- ✅ Detailed logging and statistics

## 📋 Prerequisites

- Python 3.7 or higher
- Telegram account
- Internet connection

## 🚀 Quick Start

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 2: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the **Bot Token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 3: Get Your Chat ID

1. Search for `@userinfobot` on Telegram
2. Send `/start` command
3. Copy your **Chat ID** (a number like: `123456789`)

### Step 4: Configure the Bot

Open `config.py` and update:

```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Paste your bot token
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Paste your chat ID
```

### Step 5: Test the Setup

```powershell
python main.py test
```

This will:
- Test database connection
- Test Telegram bot
- Send a test message
- Run a sample scrape

### Step 6: Run the Bot

**Option A: Run Once**
```powershell
python main.py once
```

**Option B: Run Continuously (Recommended)**
```powershell
python main.py
```

The bot will:
- Check LinkedIn every 10 minutes
- Send Telegram alerts for new jobs
- Keep running until you stop it (Ctrl+C)

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Job titles to search
JOB_TITLES = [
    "DevOps Engineer",
    "Cloud Engineer",
    "Site Reliability Engineer",  # Add more
]

# Location
LOCATION = "India"  # Change to your location

# Check interval (seconds)
CHECK_INTERVAL = 600  # 10 minutes
```

## 📊 View Statistics

```powershell
python main.py stats
```

Shows:
- Total jobs tracked
- Total scrapes performed
- Jobs found in last 24 hours

## 🗂️ Project Structure

```
AUTOMATION_JOB/
├── main.py                 # Main entry point
├── linkedin_scraper.py     # LinkedIn scraping logic
├── telegram_notifier.py    # Telegram notification handler
├── database.py             # SQLite database manager
├── config.py               # Configuration file
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── jobs.db                 # SQLite database (created automatically)
```

## 🎯 Usage Examples

### Run continuously (background monitoring)
```powershell
python main.py
```

### Run once and exit
```powershell
python main.py once
```

### Test all components
```powershell
python main.py test
```

### Check statistics
```powershell
python main.py stats
```

## 📱 Telegram Commands

Once configured, you'll receive:

1. **Startup notification** - When bot starts
2. **Job alerts** - For each new job found
3. **Error notifications** - If something goes wrong
4. **Shutdown notification** - When bot stops

## 🔧 Troubleshooting

### Issue: No jobs found
- LinkedIn might be blocking requests
- Try increasing delay between requests
- Check if LinkedIn URL structure has changed

### Issue: Telegram not working
- Verify bot token is correct
- Verify chat ID is correct
- Make sure you've started the bot (send `/start` to your bot)

### Issue: Database errors
- Delete `jobs.db` and restart
- Check file permissions

## ⚠️ Important Notes

1. **LinkedIn Terms of Service**: Web scraping may violate LinkedIn's ToS. Use at your own risk.
2. **Rate Limiting**: The script includes delays to avoid aggressive scraping
3. **Reliability**: LinkedIn may change their HTML structure, breaking the scraper
4. **Privacy**: Keep your bot token and chat ID secret

## 🔄 Running as a Background Service

### Option 1: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: "At log on" or "Daily"
4. Action: Start a program
5. Program: `python`
6. Arguments: `"D:\lakshya\Cloud\AUTOMATION_JOB\main.py"`

### Option 2: Run in PowerShell Background

```powershell
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

## 📝 License

This project is for educational purposes only. Use responsibly and respect LinkedIn's Terms of Service.

## 🤝 Contributing

Feel free to modify and improve the script for your needs!

## 📧 Support

If you encounter issues:
1. Check the `job_scraper.log` file
2. Run `python main.py test` to diagnose
3. Verify your Telegram credentials

---

**Happy Job Hunting! 🎯**
