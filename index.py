import smtplib
import requests
import os
import threading
import uuid
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
# CORS Issue সমাধান
CORS(app, resources={r"/*": {"origins": "*"}})

# আপনার ব্র্যান্ডিং তথ্য
BRAND = {
    "name": "RX PREMIUM ZONE",
    "developer": "Roman",
    "telegram": "@Roman_no_1",
    "channel": "@RX_PREMIUM_ZONE",
    "whatsapp": "01603410849",
    "tg_url": "https://t.me/RX_PREMIUM_ZONE"
}

# রেস্পন্সিভ, মোবাইল ফ্রেন্ডলি UI এবং টেলিগ্রাম পপআপ সহ
HTML_HOME = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RX Premium API Gateway</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .gradient-text { background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .glass-panel { background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); }
        
        /* Popup Animation */
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
        .popup-animate { animation: fadeIn 0.4s ease-out forwards; }
    </style>
</head>
<body class="p-4 md:p-8 min-h-screen flex items-center justify-center relative overflow-x-hidden">
    
    <div id="tgPopup" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm hidden">
        <div class="glass-panel p-8 rounded-3xl max-w-sm w-full mx-4 text-center popup-animate shadow-2xl shadow-blue-500/20">
            <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.99 1.26-5.61 3.71-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.06-.49-.83-.27-1.49-.41-1.43-.87.03-.23.36-.48 1.02-.75 3.99-1.74 6.65-2.88 7.98-3.43 3.79-1.58 4.58-1.85 5.09-1.86.11 0 .36.03.49.14.11.09.15.22.16.33.01.07 0 .15-.01.24z"/></svg>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">Join Our Community</h2>
            <p class="text-slate-300 text-sm mb-6">Stay updated with the latest API features and free premium tools directly on Telegram.</p>
            <a href="{{ tg }}" target="_blank" class="block w-full bg-gradient-to-r from-blue-600 to-indigo-600 py-3 rounded-xl font-bold text-white mb-3 hover:scale-105 transition-transform">Join Channel Now</a>
            <button onclick="closePopup()" class="text-slate-400 text-sm hover:text-white underline">Maybe Later</button>
        </div>
    </div>

    <div class="max-w-4xl w-full glass-panel rounded-3xl p-6 md:p-10 shadow-2xl">
        <div class="text-center mb-10 border-b border-slate-700 pb-8">
            <h1 class="text-4xl md:text-5xl font-black gradient-text mb-4 tracking-tight">{{ name }}</h1>
            <p class="text-slate-400 text-sm md:text-base">Ultra-Fast Professional Email Gateway v5.5</p>
        </div>
        
        <div class="grid md:grid-cols-2 gap-6">
            <section class="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50 hover:border-blue-500/50 transition-colors">
                <h2 class="text-xl font-bold text-blue-400 mb-2 flex items-center">⚡ GET Request</h2>
                <p class="text-xs text-slate-400 mb-4">Quick send with automatic beautiful template</p>
                <div class="bg-[#0f172a] p-4 rounded-xl font-mono text-xs text-green-400 break-all border border-green-900/30 overflow-hidden">
                    {{ url }}?from=GMAIL&pass=APP_PASS&to=TARGET&subject=HELLO&compose=Welcome%20Message&attach=URL
                </div>
            </section>
            
            <section class="bg-slate-800/50 p-6 rounded-2xl border border-slate-700/50 hover:border-purple-500/50 transition-colors">
                <h2 class="text-xl font-bold text-purple-400 mb-2 flex items-center">🚀 POST Request</h2>
                <p class="text-xs text-slate-400 mb-4">Advanced JSON with multiple attachments</p>
                <pre class="bg-[#0f172a] p-4 rounded-xl font-mono text-xs text-blue-300 overflow-x-auto border border-blue-900/30">
{
  "from": "your@gmail.com",
  "pass": "xxxx xxxx",
  "to": "user@gmail.com",
  "subject": "Pro Test",
  "compose": "Clear Message",
  "attachments": [{"filename": "pic.jpg", "path": "URL"}]
}
                </pre>
            </section>
        </div>

        <div class="mt-10 pt-6 border-t border-slate-700 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="text-sm text-slate-300 text-center md:text-left">
                Developed by <span class="font-bold text-blue-400">{{ dev }}</span><br>
                WhatsApp: <span class="font-bold text-green-400">{{ wa }}</span>
            </div>
            <a href="{{ tg }}" target="_blank" class="bg-blue-600 hover:bg-blue-500 px-8 py-3 rounded-full text-white font-bold transition-all w-full md:w-auto text-center">Contact Developer</a>
        </div>
    </div>

    <script>
        // Show popup on load
        window.onload = function() {
            setTimeout(() => {
                document.getElementById('tgPopup').classList.remove('hidden');
            }, 500); // 0.5s delay for better UX
        };
        // Close popup function
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
    <div style="font-family: 'Arial', sans-serif; max-width: 600px; margin: 0 auto; background-color: #f4f7f6; padding: 20px;">
        <div style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            
            <div style="background-color: #1e293b; padding: 30px 20px; text-align: center; border-bottom: 4px solid #3b82f6;">
                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: bold; text-transform: uppercase;">{BRAND['name']}</h1>
                <p style="color: #94a3b8; margin: 8px 0 0 0; font-size: 13px; letter-spacing: 1px;">SECURE & PREMIUM DELIVERY</p>
            </div>
            
            <div style="padding: 40px 30px; color: #1e293b; font-size: 16px; line-height: 1.8;">
                {content}
            </div>
            
            <div style="padding: 0 30px;">
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 0;">
            </div>
            
            <div style="background-color: #ffffff; padding: 30px; text-align: center;">
                <p style="margin: 0 0 20px 0; color: #64748b; font-size: 14px; font-weight: bold;">Stay Connected With Our Community</p>
                
                <a href="{BRAND['tg_url']}" style="display: inline-block; background-color: #2563eb; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px; margin: 0 5px;">🚀 Join Telegram</a>
                
                <a href="https://wa.me/{BRAND['whatsapp']}" style="display: inline-block; background-color: #10b981; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 14px; margin: 0 5px;">💬 WhatsApp Us</a>
                
                <p style="color: #cbd5e1; font-size: 12px; margin-top: 25px; margin-bottom: 0;">System Developed by {BRAND['developer']} | {BRAND['channel']}</p>
            </div>
        </div>
    </div>
    """

# ব্যাকগ্রাউন্ডে ইমেইল পাঠানোর ফাংশন (Fast Delivery)
def send_email_async(sender, password, to, subject, final_html, attachments):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{BRAND['name']} <{sender}>"
        msg['To'] = to
        msg['Subject'] = subject

        # জিমেইলের 'Hide Quoted Text' বা থ্রেডিং বন্ধ করার ট্রিক (Anti-Clipping UUID)
        anti_clip_string = f'<div style="display:none; max-height:0px; overflow:hidden; opacity:0; font-size:0px;">Unique ID: {uuid.uuid4()} - This prevents email clipping.</div>'
        html_with_anticlip = final_html + anti_clip_string

        msg.attach(MIMEText(html_with_anticlip, 'html'))

        # অ্যাটাচমেন্ট প্রসেসিং
        if attachments:
            for file in attachments:
                try:
                    file_url = file.get('path')
                    file_name = file.get('filename', 'document_file')
                    if file_url:
                        response = requests.get(file_url, timeout=10)
                        if response.status_code == 200:
                            part = MIMEApplication(response.content)
                            part.add_header('Content-Disposition', 'attachment', filename=file_name)
                            msg.attach(part)
                except Exception as e:
                    print(f"Attachment processing failed: {e}")

        # ইমেইল সেন্ড করা
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            
    except Exception as e:
        print(f"Background Email Error: {e}")

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json() if request.method == 'POST' and request.is_json else request.values

    sender = data.get('from')
    password = data.get('pass')
    to = data.get('to')
    
    # UI রেন্ডার (যদি কোনো ডেটা না থাকে)
    if not any([sender, password, to]):
        return render_template_string(HTML_HOME, name=BRAND['name'], url=request.url_root, dev=BRAND['developer'], wa=BRAND['whatsapp'], tg=BRAND['tg_url'])

    # এরর হ্যান্ডলিং
    if not all([sender, password, to]):
        return jsonify({
            "status": "error",
            "message_en": "Missing required parameters: 'from', 'pass', or 'to'.",
            "message_bn": "প্রয়োজনীয় ডাটা (from, pass, to) দেওয়া হয়নি।",
            "branding": BRAND
        }), 400

    try:
        # সাবজেক্ট এ রেন্ডম স্পেস বা ক্যারেক্টার দিয়ে থ্রেডিং এড়ানো যায়, তবে আমরা বডিতে UUID দিয়েছি।
        subject = data.get('subject', f"Secure Message from {BRAND['name']}")
        attachments = []
        
        # HTML কন্টেন্ট রেডি করা
        if request.method == 'GET':
            compose_text = data.get('compose', 'Hello, this is a premium message.').replace('%', ' ')
            raw_html = f"<p style='margin: 0; font-size: 16px;'>{compose_text}</p>"
            final_html = get_professional_email_template(raw_html)
            
            single_attach = data.get('attach')
            if single_attach:
                attachments.append({"filename": "attachment", "path": single_attach})
        else:
            custom_html = data.get('html')
            if custom_html:
                final_html = custom_html # যদি ইউজার নিজে ডিজাইন দেয়
            else:
                compose_text = data.get('compose', 'Hello, this is a premium message.').replace('%', ' ')
                raw_html = f"<p style='margin: 0; font-size: 16px;'>{compose_text}</p>"
                final_html = get_professional_email_template(raw_html)
            
            attachments = data.get('attachments', [])

        # *ম্যাজিক ট্রিক*: Threading এর মাধ্যমে ব্যাকগ্রাউন্ডে ইমেইল পাঠানো হচ্ছে (Fast Response)
        thread = threading.Thread(target=send_email_async, args=(sender, password, to, subject, final_html, attachments))
        thread.start()

        # ইমেইল সেন্ড হওয়ার জন্য অপেক্ষা না করে সাথে সাথেই সাকসেস রেসপন্স দিয়ে দিবে
        return jsonify({
            "status": "success",
            "message_en": "Email processing started successfully (Ultra Fast).",
            "message_bn": "ইমেইলটি প্রসেসিং এ চলে গেছে এবং ব্যাকগ্রাউন্ডে দ্রুত পাঠানো হচ্ছে।",
            "branding": BRAND
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message_en": f"System error: {str(e)}",
            "message_bn": f"সিস্টেম এরর: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run()
