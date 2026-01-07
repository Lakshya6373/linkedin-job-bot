# 📖 Step-by-Step Setup Guide

## 🎯 Complete Setup in 5 Minutes!

### Step 1: Install Python Dependencies ⚙️

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed requests-2.31.0 beautifulsoup4-4.12.2 lxml-5.1.0
```

---

### Step 2: Create Your Telegram Bot 🤖

#### 2.1: Open Telegram
- Open Telegram on your phone or computer
- Search for `@BotFather` (official bot with blue checkmark)

#### 2.2: Create New Bot
Send these commands:

```
/newbot
```

BotFather will ask: **"Alright, a new bot. How are we going to call it?"**

Reply with your bot name:
```
LinkedIn Job Alert Bot
```

BotFather will ask: **"Good. Now let's choose a username for your bot."**

Reply with a username (must end with 'bot'):
```
my_linkedin_job_alert_bot
```

#### 2.3: Save Your Bot Token 🔑

BotFather will reply with something like:

```
Done! Congratulations on your new bot!

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456

Keep your token secure and store it safely...
```

**✅ COPY THIS TOKEN!** You'll need it in Step 4.

---

### Step 3: Get Your Chat ID 💬

#### 3.1: Find Your Chat ID
- In Telegram, search for `@userinfobot`
- Send `/start` command

#### 3.2: Copy Your ID
The bot will reply with:

```
Id: 123456789
First name: Your Name
```

**✅ COPY THE ID NUMBER!** (Example: `123456789`)

---

### Step 4: Configure Your Bot ⚙️

#### 4.1: Open config.py
Open the file `config.py` in any text editor (Notepad, VS Code, etc.)

#### 4.2: Add Your Credentials
Replace these two lines:

**BEFORE:**
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
```

**AFTER:**
```python
TELEGRAM_BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456"
TELEGRAM_CHAT_ID = "123456789"
```

#### 4.3: (Optional) Customize Job Search
You can also change:

```python
# Job titles to search
JOB_TITLES = [
    "DevOps Engineer",
    "Cloud Engineer",
    "Site Reliability Engineer",  # Add more titles
    "Platform Engineer",
]

# Location
LOCATION = "India"  # Or "Bangalore", "Remote", etc.

# Check interval
CHECK_INTERVAL = 600  # 600 seconds = 10 minutes
```

#### 4.4: Save the File
Press `Ctrl + S` to save

---

### Step 5: Test Your Setup 🧪

Run the test command:

```powershell
python main.py test
```

**Expected output:**
```
🧪 Testing Job Automation Setup

1️⃣ Testing database...
   ✅ Database connected - 0 jobs tracked

2️⃣ Testing Telegram...
   ✅ Connected to Telegram Bot: @my_linkedin_job_alert_bot
   ✅ Telegram bot working!

3️⃣ Testing LinkedIn scraper...
   🔍 Searching for: DevOps Engineer
   ✅ Found 5 jobs for DevOps Engineer
   ✅ Scraper working - Found 5 jobs

======================================================================
✅ All tests completed!
======================================================================
```

**✅ You should also receive a test message on Telegram!**

---

### Step 6: Start the Bot 🚀

#### Option A: Run Once (Test Mode)
```powershell
python main.py once
```

This will:
- Scrape jobs once
- Send notifications
- Exit

#### Option B: Run Continuously (Production Mode)
```powershell
python main.py
```

This will:
- Run forever
- Check every 10 minutes
- Send notifications for new jobs
- Press `Ctrl + C` to stop

**Expected output:**
```
======================================================================
🤖 LinkedIn Job Automation Bot Started
======================================================================
⏰ Check interval: 600 seconds (10.0 minutes)
🔍 Job titles: DevOps Engineer, Cloud Engineer
📍 Location: India
📱 Notifications: Enabled
======================================================================

🔌 Testing Telegram connection...
✅ Connected to Telegram Bot: @my_linkedin_job_alert_bot

💡 Press Ctrl+C to stop

======================================================================
🔄 Iteration #1
======================================================================
🚀 Job Scraper Running - 2026-01-08 14:30:00
======================================================================

🔍 Searching for: DevOps Engineer
✅ Found 5 jobs for DevOps Engineer
🔍 Searching for: Cloud Engineer
✅ Found 3 jobs for Cloud Engineer

📊 Found 8 total jobs
✨ 8 new jobs

📱 Sending 8 notification(s)...
✅ Notifications sent!

📈 Database Stats:
   Total jobs tracked: 8
   Total scrapes: 1
   Jobs in last 24h: 8

⏳ Waiting 600 seconds until next check...
⏰ Next check at: 2026-01-08 14:40:00
```

---

### Step 7: Start Your Telegram Bot 💬

**IMPORTANT**: You must start a conversation with your bot!

1. Open Telegram
2. Search for your bot (e.g., `@my_linkedin_job_alert_bot`)
3. Click **START** button or send `/start`

Now your bot can send you messages!

---

## 🎊 You're All Set!

Your bot is now:
- ✅ Monitoring LinkedIn for jobs
- ✅ Checking every 10 minutes
- ✅ Sending Telegram alerts for new postings
- ✅ Tracking jobs in database to avoid duplicates

---

## 📱 What Notifications Look Like

### Startup Notification:
```
✅ Job Scraper Started!

🔍 Monitoring: DevOps Engineer, Cloud Engineer
📍 Location: India
⏰ Check interval: 10.0 minutes
🕒 Started at: 2026-01-08 14:30:00
```

### New Job Alert:
```
🎯 New Job Alerts!

Found 2 new job(s)
⏰ 2026-01-08 14:30:00
━━━━━━━━━━━━━━━━━━━━

📋 Job #1

💼 Senior DevOps Engineer

🏢 Company: Tech Corp
📍 Location: Bangalore, India
🕒 Posted: 2 days ago
🔍 Search Term: DevOps Engineer

🔗 View Job Details

━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 Quick Commands Reference

```powershell
# Test setup
python main.py test

# Run once and exit
python main.py once

# Run continuously (recommended)
python main.py

# View statistics
python main.py stats

# Stop the bot
Press Ctrl + C
```

---

## ❓ Troubleshooting

### Issue: "Telegram connection failed"
**Solution:**
- Double-check your bot token in `config.py`
- Make sure you started the bot on Telegram (send `/start`)
- Verify chat ID is correct

### Issue: "No jobs found"
**Solution:**
- LinkedIn might be temporarily blocking
- Wait a few minutes and try again
- Check your internet connection

### Issue: "Module not found"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: Bot not sending messages
**Solution:**
1. Open Telegram
2. Search for your bot
3. Click **START** button
4. Run `python main.py test` again

---

## 🎯 Next Steps

1. **Keep it running**: Leave the script running in PowerShell
2. **Check Telegram**: You'll get notifications for new jobs
3. **Monitor logs**: Check output for any errors
4. **Customize**: Edit `config.py` to add more job titles or change location

---

## 🎉 Congratulations!

Your LinkedIn Job Alert Bot is now live and monitoring for opportunities! 🚀

**Happy Job Hunting!** 🎯
