import smtplib
import requests
import uuid
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
# বেসিক CORS
CORS(app)

# Vercel-এ ব্রাউজার ক্রস পলিসি (CORS) সম্পূর্ণ বাইপাস করার জন্য গ্লোবাল হেডার
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# আপনার ব্র্যান্ডিং তথ্য
BRAND = {
    "name": "RX PREMIUM ZONE",
    "developer": "Roman",
    "telegram": "@Roman_no_1",
    "channel": "@RX_PREMIUM_ZONE",
    "whatsapp": "01603410849",
    "tg_url": "https://t.me/RX_PREMIUM_ZONE"
}

# 100% মোবাইল ফ্রেন্ডলি ও ফিক্সড UI
HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>RX Premium API Gateway</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .gradient-text { background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .glass-panel { background: rgba(30, 41, 59, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        .popup-animate { animation: fadeIn 0.4s ease-out forwards; }
        /* কোড ব্লক যেন স্ক্রিনের বাইরে না যায় */
        pre { white-space: pre-wrap; word-wrap: break-word; }
    </style>
</head>
<body class="p-3 md:p-8 min-h-screen flex items-center justify-center w-full">
    
    <div id="tgPopup" class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
        <div class="glass-panel p-6 md:p-8 rounded-3xl w-full max-w-sm text-center popup-animate shadow-2xl">
            <div class="w-14 h-14 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.99 1.26-5.61 3.71-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.41-1.43-.87.03-.23.36-.48 1.02-.75 3.99-1.74 6.65-2.88 7.98-3.43 3.79-1.58 4.58-1.85 5.09-1.86.11 0 .36.03.49.14.11.09.15.22.16.33.01.07 0 .15-.01.24z"/></svg>
            </div>
            <h2 class="text-xl md:text-2xl font-bold text-white mb-2">Join Our Community</h2>
            <p class="text-slate-300 text-sm mb-6">Get premium updates directly on Telegram.</p>
            <a href="{{ tg }}" target="_blank" class="block w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-xl font-bold text-white mb-3 transition-colors">Join Channel Now</a>
            <button onclick="closePopup()" class="text-slate-400 text-sm hover:text-white underline p-2">Maybe Later</button>
        </div>
    </div>

    <div class="w-full max-w-4xl glass-panel rounded-2xl md:rounded-3xl p-5 md:p-10 shadow-2xl">
        <div class="text-center mb-8 border-b border-slate-700 pb-6">
            <h1 class="text-3xl md:text-5xl font-black gradient-text mb-2 tracking-tight">{{ name }}</h1>
            <p class="text-slate-400 text-xs md:text-base">Ultra-Fast Email Gateway v6.0</p>
        </div>
        
        <div class="flex flex-col md:flex-row gap-5">
            <section class="flex-1 bg-slate-800/60 p-5 rounded-2xl border border-slate-700 w-full overflow-hidden">
                <h2 class="text-lg font-bold text-blue-400 mb-2">⚡ GET Request</h2>
                <div class="bg-black p-3 rounded-xl font-mono text-xs text-green-400 overflow-x-auto break-words whitespace-pre-wrap">
{{ url }}?from=GMAIL&pass=APP_PASS&to=TARGET&subject=HELLO&compose=Welcome%20Message
                </div>
            </section>
            
            <section class="flex-1 bg-slate-800/60 p-5 rounded-2xl border border-slate-700 w-full overflow-hidden">
                <h2 class="text-lg font-bold text-purple-400 mb-2">🚀 POST Request</h2>
                <pre class="bg-black p-3 rounded-xl font-mono text-xs text-blue-300 overflow-x-auto break-words whitespace-pre-wrap">
{
  "from": "your@gmail.com",
  "pass": "xxxx xxxx",
  "to": "user@gmail.com",
  "subject": "Pro Test",
  "compose": "Clear Message"
}
                </pre>
            </section>
        </div>

        <div class="mt-8 pt-5 border-t border-slate-700 flex flex-col md:flex-row justify-between items-center gap-4 text-center md:text-left">
            <div class="text-xs md:text-sm text-slate-300">
                Dev: <span class="font-bold text-blue-400">{{ dev }}</span><br>
                WA: <span class="font-bold text-green-400">{{ wa }}</span>
            </div>
            <a href="{{ tg }}" target="_blank" class="bg-blue-600 px-6 py-2.5 rounded-full text-white text-sm font-bold w-full md:w-auto">Contact Developer</a>
        </div>
    </div>

    <script>
        window.onload = function() {
            setTimeout(() => { document.getElementById('tgPopup').classList.remove('hidden'); }, 800);
        };
        function closePopup() {
            document.getElementById('tgPopup').classList.add('hidden');
        }
    </script>
</body>
</html>
"""

# স্পস্ট এবং ইউনিক ইমেইল টেমপ্লেট
def get_professional_email_template(content):
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f8fafc; padding: 15px;">
        <div style="background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
            <div style="background-color: #1e293b; padding: 25px 20px; text-align: center; border-bottom: 3px solid #3b82f6;">
                <h1 style="color: #ffffff; margin: 0; font-size: 22px; font-weight: bold;">{BRAND['name']}</h1>
            </div>
            <div style="padding: 30px 20px; color: #1e293b; font-size: 16px; line-height: 1.6;">
                {content}
            </div>
            <div style="background-color: #f1f5f9; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0;">
                <a href="{BRAND['tg_url']}" style="display: inline-block; background-color: #2563eb; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 5px;">🚀 Join Telegram</a>
                <a href="https://wa.me/{BRAND['whatsapp']}" style="display: inline-block; background-color: #10b981; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 5px;">💬 WhatsApp Us</a>
                <p style="color: #64748b; font-size: 11px; margin-top: 15px; margin-bottom: 0;">Developed by {BRAND['developer']}</p>
            </div>
        </div>
    </div>
    """

def send_mail_logic(sender, password, to, subject, html_content, is_custom_html=False, attachments=None):
    msg = MIMEMultipart()
    msg['From'] = f"{BRAND['name']} <{sender}>"
    msg['To'] = to
    msg['Subject'] = subject

    if not is_custom_html:
        final_html = get_professional_email_template(html_content)
    else:
        final_html = html_content

    # 'Hide Quoted Text' বাইপাস ট্রিক (Anti-Clipping)
    anti_clip_string = f'<div style="display:none; max-height:0px; overflow:hidden; opacity:0; font-size:0px;">ID: {uuid.uuid4()}</div>'
    msg.attach(MIMEText(final_html + anti_clip_string, 'html'))

    # দ্রুত অ্যাটাচমেন্ট প্রসেস
    if attachments:
        for file in attachments:
            try:
                file_url = file.get('path')
                file_name = file.get('filename', 'file')
                if file_url:
                    response = requests.get(file_url, timeout=5) # ৫ সেকেন্ড টাইমআউট
                    if response.status_code == 200:
                        part = MIMEApplication(response.content)
                        part.add_header('Content-Disposition', 'attachment', filename=file_name)
                        msg.attach(part)
            except Exception as e:
                pass # ফাইল ফেইল হলে ইমেইল পাঠানো থামবে না

    # সিঙ্ক্রোনাস সেন্ডিং (একদম রিয়েল-টাইম এরর ধরার জন্য)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(msg)
    server.quit()

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json() if request.method == 'POST' and request.is_json else request.values

    sender = data.get('from')
    password = data.get('pass')
    to = data.get('to')
    
    if not any([sender, password, to]):
        return render_template_string(HTML_HOME, name=BRAND['name'], url=request.url_root, dev=BRAND['developer'], wa=BRAND['whatsapp'], tg=BRAND['tg_url'])

    if not all([sender, password, to]):
        return jsonify({
            "status": "error",
            "message_en": "Missing required parameters.",
            "message_bn": "প্রয়োজনীয় ডাটা (from, pass, to) দেওয়া হয়নি।",
            "branding": BRAND
        }), 400

    try:
        subject = data.get('subject', f"Secure Message from {BRAND['name']}")
        attachments = []
        is_custom_html = False
        
        if request.method == 'GET':
            compose_text = data.get('compose', 'Premium message.').replace('%', ' ')
            html_content = f"<p style='margin: 0;'>{compose_text}</p>"
            if data.get('attach'):
                attachments.append({"filename": "attachment", "path": data.get('attach')})
        else:
            if data.get('html'):
                html_content = data.get('html')
                is_custom_html = True
            else:
                compose_text = data.get('compose', 'Premium message.').replace('%', ' ')
                html_content = f"<p style='margin: 0;'>{compose_text}</p>"
            attachments = data.get('attachments', [])

        # থ্রেডিং বাদ দিয়ে সরাসরি ফাংশন কল (ভুল হলে সাথে সাথে catch ব্লকে চলে যাবে)
        send_mail_logic(sender, password, to, subject, html_content, is_custom_html, attachments)

        return jsonify({
            "status": "success",
            "message_en": "Email successfully delivered.",
            "message_bn": "ইমেইল সফলভাবে পাঠানো হয়েছে।",
            "branding": BRAND
        }), 200

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            "status": "error",
            "message_en": "Authentication failed. Invalid email or App Password.",
            "message_bn": "ইমেইল বা অ্যাপ পাসওয়ার্ড ভুল হয়েছে। দয়া করে চেক করুন।"
        }), 401
    except Exception as e:
        return jsonify({
            "status": "error",
            "message_en": f"System error: {str(e)}",
            "message_bn": f"ইমেইল পাঠানো সম্ভব হয়নি: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run()
