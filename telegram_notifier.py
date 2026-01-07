"""
Telegram Notification Module
Sends job alerts via Telegram Bot
"""
import requests
import json
from datetime import datetime

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        """
        Initialize Telegram Bot
        
        Args:
            bot_token: Your Telegram Bot token from @BotFather
            chat_id: Your Telegram chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message, parse_mode="HTML"):
        """Send a text message"""
        url = f"{self.api_url}/sendMessage"
        
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return True
            else:
                print(f"❌ Telegram API Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending Telegram message: {str(e)}")
            return False
    
    def send_job_alert(self, job):
        """Send formatted job alert"""
        message = self.format_job_message(job)
        return self.send_message(message)
    
    def send_multiple_jobs(self, jobs):
        """Send multiple job alerts"""
        if not jobs:
            return
        
        # Send summary first
        summary = f"🎯 <b>New Job Alerts!</b>\n\n"
        summary += f"Found {len(jobs)} new job(s)\n"
        summary += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += "━━━━━━━━━━━━━━━━━━━━"
        
        self.send_message(summary)
        
        # Send individual job details
        for i, job in enumerate(jobs, 1):
            message = self.format_job_message(job, index=i)
            self.send_message(message)
            
            # Add delay between messages to avoid rate limiting
            if i < len(jobs):
                import time
                time.sleep(1)
    
    def format_job_message(self, job, index=None):
        """Format job data as HTML message"""
        prefix = f"📋 <b>Job #{index}</b>\n\n" if index else ""
        
        message = prefix
        
        # Show title with note if hidden
        title = job['title']
        if title == "Job Title Hidden" or title == "N/A":
            message += f"💼 <b>[Title Hidden - Click link to view]</b>\n\n"
        else:
            message += f"💼 <b>{title}</b>\n\n"
        
        # Show company with note if hidden
        company = job['company']
        if company == "Company Name Hidden" or company == "N/A":
            message += f"🏢 <b>Company:</b> [Hidden - Click link to view]\n"
        else:
            message += f"🏢 <b>Company:</b> {company}\n"
        
        # Show location with note if hidden
        location = job['location']
        if location == "Location Hidden" or location == "N/A":
            message += f"📍 <b>Location:</b> [Hidden - Click link to view]\n"
        else:
            message += f"📍 <b>Location:</b> {location}\n"
        
        message += f"🕒 <b>Posted:</b> {job['posted_date']}\n"
        message += f"🔍 <b>Search Term:</b> {job['search_term']}\n\n"
        
        if job['url'] != "N/A":
            message += f"🔗 <a href='{job['url']}'>Click here to view full job details</a>\n"
            message += f"\n💡 <i>Some details may be hidden by LinkedIn. Click the link above to see complete job information.</i>\n"
        
        message += "\n━━━━━━━━━━━━━━━━━━━━"
        
        return message
    
    def test_connection(self):
        """Test Telegram bot connection"""
        url = f"{self.api_url}/getMe"
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    print(f"✅ Connected to Telegram Bot: @{bot_info.get('username')}")
                    return True
            
            print(f"❌ Telegram connection failed: {response.text}")
            return False
            
        except Exception as e:
            print(f"❌ Error testing Telegram connection: {str(e)}")
            return False
    
    def get_chat_info(self):
        """Get information about the chat"""
        url = f"{self.api_url}/getChat"
        
        payload = {
            'chat_id': self.chat_id
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    return data.get('result', {})
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting chat info: {str(e)}")
            return None


if __name__ == "__main__":
    # Test the notifier
    print("🤖 Telegram Notifier Test\n")
    print("You need to configure your bot token and chat ID first!")
    print("\nSteps to get Telegram credentials:")
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot and follow instructions")
    print("3. Copy the bot token")
    print("4. Search for @userinfobot to get your chat ID")
