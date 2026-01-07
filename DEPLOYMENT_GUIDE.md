# 🚀 Deploy to PythonAnywhere (Free Hosting)

## Why PythonAnywhere?
- ✅ 100% FREE (no credit card needed)
- ✅ Easy to setup
- ✅ Can run scheduled tasks
- ✅ Perfect for Python scripts

---

## 📋 Step-by-Step Deployment Guide

### Step 1: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click **"Start running Python online for FREE"**
3. Create a free account (Beginner tier)
4. Verify your email

---

### Step 2: Upload Your Files

#### Option A: Upload via Web Interface

1. Login to PythonAnywhere
2. Go to **"Files"** tab
3. Create a new directory: `linkedin_job_bot`
4. Upload these files one by one:
   - `main.py`
   - `linkedin_scraper.py`
   - `telegram_notifier.py`
   - `database.py`
   - `config.py`
   - `requirements.txt`

#### Option B: Use Git (Recommended)

1. First, push your code to GitHub (see separate guide below)
2. In PythonAnywhere, go to **"Consoles"** → **"Bash"**
3. Run:
```bash
git clone https://github.com/YOUR_USERNAME/linkedin-job-bot.git
cd linkedin-job-bot
```

---

### Step 3: Install Dependencies

In PythonAnywhere Bash console:

```bash
cd linkedin_job_bot  # or your directory name
pip3 install --user -r requirements.txt
```

Wait for installation to complete.

---

### Step 4: Test Your Bot

```bash
python3 main.py test
```

You should see:
```
✅ Database connected
✅ Telegram bot working!
✅ Scraper working
```

---

### Step 5: Create Scheduled Task

1. Go to **"Tasks"** tab in PythonAnywhere
2. Under **"Scheduled tasks"**, enter:
   - **Command:** `python3 /home/YOUR_USERNAME/linkedin_job_bot/main.py once`
   - **Hour:** Select any hour (e.g., 10)
   - **Minute:** 00

3. Click **"Create"**

⚠️ **Important:** Free tier only allows **1 scheduled task per day**

---

### Step 6: Workaround for 10-Minute Intervals

Since free tier only runs once per day, you have two options:

#### Option A: Run Multiple Times Daily (Manual Setup)
Create the task to run once per hour:
- Set hour to: `*` (every hour)
- Set minute to: `0`

#### Option B: Keep Script Running (Better)
Create a file `run_continuous.py`:

```python
from main import JobAutomation
import time

automation = JobAutomation()

# Send startup notification
if automation.notifications_enabled:
    startup_msg = "✅ Bot started on PythonAnywhere!"
    automation.notifier.send_message(startup_msg)

# Run continuously
automation.run_continuous()
```

Then in **"Consoles"** → **"Bash"**, run:
```bash
python3 run_continuous.py
```

Keep this console tab open. It will run until you close it.

---

## 🔒 Security Tips

### Protect Your Credentials

Never commit `config.py` with real credentials to GitHub!

1. Create `.gitignore`:
```
config.py
jobs.db
*.pyc
__pycache__/
.env
```

2. Create `config.example.py`:
```python
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
JOB_TITLES = ["DevOps Engineer", "Cloud Engineer"]
LOCATION = "India"
CHECK_INTERVAL = 600
```

3. On PythonAnywhere, manually edit `config.py` with real values

---

## 🐙 Optional: Push to GitHub First

### Step 1: Initialize Git
```powershell
cd "d:\lakshya\Cloud\AUTOMATION_JOB"
git init
```

### Step 2: Create .gitignore
```powershell
echo "config.py
jobs.db
*.pyc
__pycache__/
.env" > .gitignore
```

### Step 3: Create config.example.py
Copy `config.py` to `config.example.py` and replace real values with placeholders

### Step 4: Commit and Push
```powershell
git add .
git commit -m "Initial commit - LinkedIn Job Bot"
git remote add origin https://github.com/YOUR_USERNAME/linkedin-job-bot.git
git push -u origin main
```

Now you can clone it on PythonAnywhere!

---

## 🔄 Alternative: Render.com (Background Worker)

If you want true 24/7 operation:

1. Sign up at https://render.com
2. Create a new **"Background Worker"**
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python main.py`
6. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
7. Deploy!

---

## 📊 Monitoring Your Bot

### Check if it's running:
- PythonAnywhere: Check **"Consoles"** tab
- Telegram: Bot sends startup notification
- Check Telegram for job alerts

### View Logs:
In PythonAnywhere Bash:
```bash
cd linkedin_job_bot
python3 main.py stats
```

Shows:
- Total jobs tracked
- Total scrapes
- Recent activity

---

## ⚡ Quick Comparison

| Platform | Cost | Setup | 24/7 | Best For |
|----------|------|-------|------|----------|
| **PythonAnywhere** | Free | Easy | Limited | Testing |
| **Render.com** | Free | Medium | Yes | Production |
| **Railway** | $5/mo | Easy | Yes | Production |
| **Oracle Cloud** | Free | Hard | Yes | Advanced users |

---

## 🎯 Recommended Approach

1. **Start with PythonAnywhere** (test for free)
2. If you like it, upgrade to **Render.com** (still free, better 24/7)
3. For maximum control, use **Oracle Cloud** free tier

---

## 🆘 Troubleshooting

### Bot not running?
Check PythonAnywhere console for errors

### Dependencies failed?
Use Python 3.9+ on PythonAnywhere

### Telegram not sending?
Verify config.py has correct credentials

### Database errors?
Make sure jobs.db has write permissions

---

## ✅ You're Done!

Your bot is now running in the cloud 24/7! 🎉

You'll receive Telegram notifications for new jobs automatically.

**No need to keep your PC on!** 🚀
