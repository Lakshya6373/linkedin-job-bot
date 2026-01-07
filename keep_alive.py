"""
Keep-alive web server for Replit
This keeps the deployment active
"""
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>LinkedIn Job Bot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f5f5f5;
                }
                .container {
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 { color: #0077b5; }
                .status { 
                    padding: 10px; 
                    background: #d4edda; 
                    border-radius: 5px;
                    margin: 20px 0;
                }
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
                <hr>
                <p>Your bot is actively monitoring LinkedIn for new job postings.</p>
                <p>You'll receive Telegram notifications when new jobs are found!</p>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "running", "bot": "active"}

def run():
    """Run Flask server"""
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def keep_alive():
    """Start the web server in a separate thread"""
    print("🔌 Starting keep-alive server...")
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("✅ Keep-alive server thread started")
