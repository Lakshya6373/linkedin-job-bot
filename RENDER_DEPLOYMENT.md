# 🚀 Complete Guide: Deploy to Render.com (24/7 Free Hosting)

## Why Render.com?
- ✅ **FREE** 750 hours/month (enough for 24/7)
- ✅ **True 24/7** operation - checks every 10 minutes
- ✅ **Easy deployment** from GitHub
- ✅ **Automatic restarts** if it crashes
- ✅ **Environment variables** for security
- ❌ Requires credit card (but won't charge on free tier)

---

# 📋 STEP-BY-STEP DEPLOYMENT

## PART 1: Prepare Your Code for GitHub

### Step 1: Create a GitHub Account
1. Go to https://github.com
2. Click **"Sign up"**
3. Create your account (free)
4. Verify your email

---

### Step 2: Create a New Repository

1. Click **"+"** in top-right → **"New repository"**
2. Repository name: `linkedin-job-bot`
3. Description: `Automated LinkedIn job scraper with Telegram notifications`
4. Select: **Private** (to hide your code)
5. Check: ✅ **Add a README file**
6. Click **"Create repository"**

---

### Step 3: Install Git on Your PC (if not installed)

**Download Git:**
- Go to https://git-scm.com/download/win
- Download and install
- Restart PowerShell after installation

**Verify installation:**
```powershell
git --version
```

---

### Step 4: Configure Git (First Time Only)

```powershell
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

### Step 5: Prepare Your Project

Open PowerShell in your project folder:

```powershell
cd "d:\lakshya\Cloud\AUTOMATION_JOB"
```

**Initialize Git:**
```powershell
git init
```

**Verify .gitignore exists:**
```powershell
cat .gitignore
```

Should show:
```
config.py
jobs.db
*.pyc
__pycache__/
.env
*.log
job_scraper.log
.venv/
venv/
```

---

### Step 6: Stage Your Files

```powershell
git add .
```

This adds all files EXCEPT those in `.gitignore` (like `config.py` with your secrets)

**Check what will be committed:**
```powershell
git status
```

You should see:
- ✅ main.py
- ✅ linkedin_scraper.py
- ✅ telegram_notifier.py
- ✅ database.py
- ✅ config.example.py
- ✅ requirements.txt
- ✅ README.md
- ❌ NOT config.py (your secrets are safe!)

---

### Step 7: Commit Your Code

```powershell
git commit -m "Initial commit: LinkedIn Job Bot"
```

---

### Step 8: Connect to GitHub

Go back to your GitHub repository page and copy the URL:
```
https://github.com/YOUR_USERNAME/linkedin-job-bot.git
```

In PowerShell:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/linkedin-job-bot.git
git branch -M main
git push -u origin main
```

**Enter your GitHub credentials when asked:**
- Username: Your GitHub username
- Password: Use **Personal Access Token** (not your actual password)

#### How to Get Personal Access Token:
1. Go to GitHub → Click your profile → **Settings**
2. Scroll down → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Note: `Git access for linkedin-job-bot`
6. Expiration: **No expiration**
7. Check: ✅ **repo** (full control)
8. Click **"Generate token"**
9. **COPY THE TOKEN** (you won't see it again!)
10. Use this as password when pushing to GitHub

---

### Step 9: Verify Upload

Refresh your GitHub repository page. You should see all your files!

---

## PART 2: Deploy to Render.com

### Step 1: Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with GitHub (recommended) or email
4. If using GitHub: Click **"Authorize Render"**
5. Add credit card (required but won't charge on free tier)

---

### Step 2: Create a Background Worker

1. Click **"New +"** → **"Background Worker"**
2. Connect your repository:
   - Click **"Connect account"** if not connected
   - Find `linkedin-job-bot`
   - Click **"Connect"**

---

### Step 3: Configure the Worker

**Basic Settings:**
- **Name:** `linkedin-job-bot`
- **Region:** Choose closest to you (e.g., Singapore, Oregon)
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```
  python main.py
  ```

---

### Step 4: Set Environment Variables

Scroll down to **"Environment Variables"**

Click **"Add Environment Variable"** and add these:

**Variable 1:**
- Key: `TELEGRAM_BOT_TOKEN`
- Value: `7574450060:AAFRqNmC3QkS7Sb7AgXyu0pBjMLsQFIIsjY`

**Variable 2:**
- Key: `TELEGRAM_CHAT_ID`
- Value: `YOUR_CHAT_ID` (the number you got from @userinfobot)

---

### Step 5: Update config.py to Use Environment Variables

We need to modify `config.py` to read from environment variables on Render:

**Create a new file: `config_render.py`**

```python
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
```

**Add this to PowerShell:**
```powershell
# Create the new config file
New-Item -Path "config_render.py" -ItemType File
# Copy the content above into it
```

---

### Step 6: Update main.py to Use Config Render

Open `main.py` and change line 7:

**OLD:**
```python
import config
```

**NEW:**
```python
try:
    import config_render as config
except ImportError:
    import config
```

This makes it work both locally AND on Render!

---

### Step 7: Push Changes to GitHub

```powershell
git add config_render.py main.py
git commit -m "Add Render.com configuration support"
git push origin main
```

---

### Step 8: Select Plan & Deploy

Back on Render:

1. **Instance Type:** Select **"Free"**
2. Click **"Create Background Worker"**

Render will now:
- Clone your GitHub repo
- Install dependencies
- Start your bot
- Keep it running 24/7!

---

### Step 9: Monitor Deployment

Watch the **"Logs"** tab:

You should see:
```
Installing dependencies...
Successfully installed requests beautifulsoup4 lxml
Starting bot...
✅ Database initialized
🤖 LinkedIn Job Automation Bot Started
⏰ Check interval: 600 seconds (10.0 minutes)
🔍 Job titles: DevOps Engineer, Cloud Engineer
📍 Location: India
📱 Notifications: Enabled
🔌 Testing Telegram connection...
✅ Connected to Telegram Bot: @Job3737BOT
```

**Check your Telegram!** You should receive a startup notification! 📱

---

## PART 3: Verify It's Working

### Test 1: Check Telegram
You should receive:
```
✅ Job Scraper Started!

🔍 Monitoring: DevOps Engineer, Cloud Engineer
📍 Location: India
⏰ Check interval: 10.0 minutes
🕒 Started at: 2026-01-08 15:30:00
```

### Test 2: Wait 10 Minutes
After 10 minutes, you'll get job alerts for new jobs!

### Test 3: Check Render Logs
Go to Render dashboard → Your service → **"Logs"** tab

You should see:
```
🔄 Iteration #1
🚀 Job Scraper Running - 2026-01-08 15:30:00
🔍 Searching for: DevOps Engineer
✅ Found 7 jobs for DevOps Engineer
📊 Found 7 total jobs
✨ 7 new jobs
📱 Sending 7 notification(s)...
✅ Notifications sent!
⏳ Waiting 600 seconds until next check...
```

---

## 🎯 Success! Your Bot is Live 24/7!

### What Happens Now:
1. ✅ Bot runs on Render's servers (not your PC)
2. ✅ Checks LinkedIn every 10 minutes
3. ✅ Sends Telegram alerts for new jobs
4. ✅ No duplicate alerts
5. ✅ Automatically restarts if it crashes
6. ✅ You can turn off your PC!

---

## 📊 Managing Your Bot

### View Logs
Render Dashboard → Your service → **"Logs"**

### Restart Bot
Render Dashboard → Your service → **"Manual Deploy"** → **"Clear build cache & deploy"**

### Stop Bot
Render Dashboard → Your service → **"Suspend"**

### Update Code
1. Make changes locally
2. Commit: `git add . && git commit -m "Update message"`
3. Push: `git push origin main`
4. Render auto-deploys in 2-3 minutes!

---

## 🔧 Advanced Configuration

### Change Job Search Settings

Edit `config_render.py` on GitHub:
1. Go to your repo → Click `config_render.py`
2. Click pencil icon (Edit)
3. Modify `JOB_TITLES`, `LOCATION`, etc.
4. Scroll down → **"Commit changes"**

Render will auto-redeploy!

### Add More Job Titles
```python
JOB_TITLES = [
    "DevOps Engineer",
    "Cloud Engineer",
    "Site Reliability Engineer",
    "Platform Engineer",
    "AWS Engineer",
    "Azure DevOps Engineer",
]
```

### Change Check Interval
```python
CHECK_INTERVAL = 300  # 5 minutes (more frequent)
CHECK_INTERVAL = 1800  # 30 minutes (less frequent)
```

---

## 💰 Render Free Tier Limits

- ✅ **750 hours/month** = 31.25 days (perfect for 24/7!)
- ✅ **Unlimited builds**
- ✅ **Automatic deploys**
- ✅ **Free SSL**
- ⚠️ Sleeps after 15 min inactivity (but background workers DON'T sleep!)

Your bot will run **100% free, 24/7, all month!** 🎉

---

## 🆘 Troubleshooting

### Issue: "Build failed"
**Solution:** Check logs for error. Usually missing dependency.
```powershell
# Make sure requirements.txt is complete
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Issue: "Telegram not working"
**Solution:** Verify environment variables in Render:
1. Dashboard → Your service → **"Environment"**
2. Check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
3. Click **"Save Changes"**

### Issue: "Database error"
**Solution:** Database is ephemeral on Render. Use persistent disk:
1. Dashboard → Your service → **"Disks"**
2. Add disk: `/opt/render/project/src/data`
3. Update `config_render.py`: `DATABASE_PATH = "/opt/render/project/src/data/jobs.db"`

### Issue: "Bot stopped after some time"
**Solution:** Check logs for errors. Render auto-restarts on crash.

### Issue: "Too many API calls"
**Solution:** Increase `CHECK_INTERVAL` to reduce frequency

---

## 🔐 Security Best Practices

### ✅ DO:
- Keep repository **Private**
- Use environment variables for secrets
- Use `.gitignore` to exclude `config.py`
- Rotate bot token if exposed

### ❌ DON'T:
- Commit `config.py` with real credentials
- Make repository public with secrets
- Share your bot token
- Push database files to GitHub

---

## 📈 Monitoring & Statistics

### Check Bot Status
Send a message to your Telegram bot (won't respond, but you'll know it's running by the alerts)

### View Statistics
Unfortunately, can't run commands directly on Render Free tier.

**Alternative:** Add a stats notification feature:

Edit `main.py`, add to `run_continuous()` after startup:
```python
# Send daily stats at midnight
if datetime.now().hour == 0 and datetime.now().minute < 10:
    stats = self.db.get_stats()
    stats_msg = f"📊 <b>Daily Stats Report</b>\n\n"
    stats_msg += f"Total jobs tracked: {stats['total_jobs']}\n"
    stats_msg += f"Total scrapes: {stats['total_scrapes']}\n"
    stats_msg += f"Jobs in last 24h: {stats['recent_jobs']}"
    self.notifier.send_message(stats_msg)
```

---

## 🎓 What You've Learned

1. ✅ Git version control
2. ✅ GitHub repository management
3. ✅ Environment variables for security
4. ✅ Cloud deployment (Render.com)
5. ✅ Background workers
6. ✅ 24/7 automation

---

## 🎉 Congratulations!

Your LinkedIn Job Alert Bot is now:
- ✅ Running 24/7 in the cloud
- ✅ Checking every 10 minutes
- ✅ Sending instant Telegram alerts
- ✅ Tracking jobs (no duplicates)
- ✅ Completely FREE!

**You don't need to keep your PC on anymore!** 🚀

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- GitHub Docs: https://docs.github.com
- Check logs in Render dashboard
- Test locally first: `python main.py once`

---

## 🔄 Next Steps

1. Monitor Telegram for job alerts
2. Check Render logs occasionally
3. Update job search criteria as needed
4. Apply to jobs! 🎯

**Happy Job Hunting!** 🎊
