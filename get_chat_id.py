"""
Quick script to get your Telegram Chat ID
"""
import requests

BOT_TOKEN = "7574450060:AAFRqNmC3QkS7Sb7AgXyu0pBjMLsQFIIsjY"

print("=" * 60)
print("🔍 Getting your Telegram Chat ID")
print("=" * 60)
print("\n📱 IMPORTANT: Open Telegram and send any message to your bot first!")
print("   Bot: @Job3737BOT")
print("   Send: /start or Hello\n")
input("Press Enter after you've sent a message to the bot...")

# Get updates
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

try:
    response = requests.get(url, timeout=10)
    data = response.json()
    
    if data.get('ok') and data.get('result'):
        print("\n✅ Found messages!")
        print("=" * 60)
        
        for update in data['result']:
            if 'message' in update:
                chat = update['message']['chat']
                chat_id = chat['id']
                first_name = chat.get('first_name', 'N/A')
                username = chat.get('username', 'N/A')
                
                print(f"\n👤 User: {first_name}")
                print(f"📱 Username: @{username}")
                print(f"🆔 Chat ID: {chat_id}")
                print("=" * 60)
                print(f"\n✅ Your Chat ID is: {chat_id}")
                print("\nAdd this to config.py:")
                print(f'TELEGRAM_CHAT_ID = "{chat_id}"')
                break
        else:
            print("\n⚠️ No messages found!")
            print("Make sure you sent a message to @Job3737BOT")
    else:
        print("\n❌ No updates found!")
        print("Please send /start to @Job3737BOT on Telegram")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
