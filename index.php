import smtplib
import requests
import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
# CORS Issue সমাধান (Allow all origins & Methods)
CORS(app, resources={r"/*": {"origins": "*"}})

# প্রফেশনাল ব্র্যান্ডিং তথ্য
BRAND = {
    "name": "RX PREMIUM ZONE",
    "developer": "Roman",
    "telegram": "@Roman_no_1",
    "channel": "@RX_PREMIUM_ZONE",
    "whatsapp": "01603410849",
    "tg_url": "https://t.me/RX_PREMIUM_ZONE"
}

# চমৎকার ও প্রফেশনাল API কনসোল UI (Tailwind CSS)
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
        .glass-panel { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="p-5 md:p-10 min-h-screen flex items-center justify-center">
    <div class="max-w-4xl w-full glass-panel rounded-3xl p-8 border border-slate-700 shadow-[0_0_40px_rgba(59,130,246,0.2)]">
        <div class="text-center mb-8 border-b border-slate-700 pb-6">
            <h1 class="text-5xl font-black gradient-text mb-3 tracking-tight">RX PREMIUM API</h1>
            <p class="text-slate-400 text-lg">High-Performance Professional Email Gateway v5.0</p>
        </div>
        
        <div class="grid md:grid-cols-2 gap-8">
            <section class="bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
                <h2 class="text-2xl font-bold text-blue-400 mb-4 flex items-center">⚡ GET Method</h2>
                <p class="text-sm text-slate-400 mb-3">সিম্পল টেক্সট ইমেইলের জন্য (Auto Beautiful Template)</p>
                <div class="bg-black p-4 rounded-xl font-mono text-sm text-green-400 break-all border border-green-900/30">
                    {{ url }}?from=GMAIL&pass=APP_PASS&to=TARGET&subject=HELLO&compose=Welcome%20Message&attach=URL
                </div>
            </section>
            
            <section class="bg-slate-900/50 p-6 rounded-2xl border border-slate-800">
                <h2 class="text-2xl font-bold text-purple-400 mb-4 flex items-center">🚀 POST Method</h2>
                <p class="text-sm text-slate-400 mb-3">অ্যাডভান্সড কাস্টম HTML এবং মাল্টিপল অ্যাটাচমেন্টের জন্য</p>
                <pre class="bg-black p-4 rounded-xl font-mono text-xs text-blue-300 overflow-x-auto border border-blue-900/30">
{
  "from": "your@gmail.com",
  "pass": "xxxx xxxx",
  "to": "user@gmail.com",
  "subject": "Pro Testing",
  "html": "&lt;h1&gt;Custom Design&lt;/h1&gt;", 
  "compose": "Or simple text here",
  "attachments": [
    {"filename": "image.jpg", "path": "URL"}
  ]
}
                </pre>
            </section>
        </div>

        <div class="mt-8 pt-6 border-t border-slate-700 flex justify-between items-center flex-wrap gap-4">
            <div class="text-sm text-slate-300">
                Developed by <span class="font-bold text-blue-400">{{ dev }}</span> | WhatsApp: <span class="font-bold text-green-400">{{ wa }}</span>
            </div>
            <a href="{{ tg }}" target="_blank" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 px-8 py-3 rounded-full text-white font-bold transition-all shadow-lg shadow-blue-500/30">Join Telegram Channel</a>
        </div>
    </div>
</body>
</html>
"""

# ডিফল্ট প্রফেশনাল ইমেইল টেমপ্লেট
def get_professional_email_template(content):
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
        <div style="background: linear-gradient(135deg, #2563eb, #7c3aed); padding: 30px 20px; text-align: center;">
            <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: 1px;">{BRAND['name']}</h1>
            <p style="color: #cbd5e1; margin: 10px 0 0 0; font-size: 14px;">Premium Email Services</p>
        </div>
        
        <div style="padding: 40px 30px; color: #334155; font-size: 16px; line-height: 1.8;">
            {content}
        </div>
        
        <div style="background-color: #f8fafc; padding: 30px; border-top: 1px solid #e2e8f0; text-align: center;">
            <h3 style="margin-top: 0; color: #475569; font-size: 16px;">Stay Connected with us</h3>
            <div style="margin: 20px 0;">
                <a href="{BRAND['tg_url']}" style="display: inline-block; background: #0088cc; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 50px; font-weight: bold; margin: 5px 10px; font-size: 14px; box-shadow: 0 4px 6px rgba(0,136,204,0.2);">✈️ Join Telegram</a>
                <a href="https://wa.me/{BRAND['whatsapp']}" style="display: inline-block; background: #25d366; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 50px; font-weight: bold; margin: 5px 10px; font-size: 14px; box-shadow: 0 4px 6px rgba(37,211,102,0.2);">💬 WhatsApp Support</a>
            </div>
            <p style="color: #94a3b8; font-size: 12px; margin-top: 20px;">© Developed by {BRAND['developer']} | {BRAND['channel']}</p>
        </div>
    </div>
    """

def send_mail_logic(sender, password, to, subject, html_content, is_custom_html=False, attachments=None):
    msg = MIMEMultipart()
    msg['From'] = f"{BRAND['name']} <{sender}>"
    msg['To'] = to
    msg['Subject'] = subject

    # যদি ইউজার নিজের কাস্টম HTML না দেয়, তাহলে আমাদের প্রফেশনাল টেমপ্লেট ব্যবহার করবে
    if not is_custom_html:
        final_html = get_professional_email_template(html_content)
    else:
        final_html = html_content

    msg.attach(MIMEText(final_html, 'html'))

    # ফাইল, ছবি, ভিডিও অ্যাটাচমেন্ট হ্যান্ডলিং
    if attachments:
        for file in attachments:
            try:
                file_url = file.get('path')
                file_name = file.get('filename', 'attachment_file')
                if file_url:
                    response = requests.get(file_url, timeout=10)
                    if response.status_code == 200:
                        part = MIMEApplication(response.content)
                        part.add_header('Content-Disposition', 'attachment', filename=file_name)
                        msg.attach(part)
            except Exception as e:
                print(f"Attachment error: {e}")

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def index():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json() if request.method == 'POST' and request.is_json else request.values

    sender = data.get('from')
    password = data.get('pass')
    to = data.get('to')
    
    # UI প্রদর্শন যদি ডেটা না থাকে
    if not any([sender, password, to]):
        return render_template_string(HTML_HOME, url=request.url_root, dev=BRAND['developer'], wa=BRAND['whatsapp'], tg=BRAND['tg_url'])

    # বাংলা ও ইংরেজি বাইলিঙ্গুয়াল এরর মেসেজ
    if not all([sender, password, to]):
        return jsonify({
            "status": "error",
            "message_en": "Missing required parameters: 'from', 'pass', or 'to'.",
            "message_bn": "প্রয়োজনীয় ডাটা (from, pass, to) দেওয়া হয়নি। দয়া করে সব ইনফরমেশন দিন।",
            "branding": BRAND
        }), 400

    try:
        subject = data.get('subject', f"Message from {BRAND['name']}")
        attachments = []
        is_custom_html = False

        # GET এবং POST মেথডের জন্য লজিক
        if request.method == 'GET':
            compose_text = data.get('compose', 'Hello, this is a test message.').replace('%', ' ')
            html_content = f"<p style='font-size: 18px;'>{compose_text}</p>"
            
            # GET মেথডে সিঙ্গেল ফাইল অ্যাটাচ করার সুবিধা (&attach=URL)
            single_attach = data.get('attach')
            if single_attach:
                attachments.append({"filename": "document_file", "path": single_attach})
        else:
            # POST মেথড
            custom_html = data.get('html')
            if custom_html:
                html_content = custom_html
                is_custom_html = True
            else:
                compose_text = data.get('compose', 'Hello, this is a test message.').replace('%', ' ')
                html_content = f"<p style='font-size: 18px;'>{compose_text}</p>"
            
            attachments = data.get('attachments', [])

        # ইমেইল সেন্ড ফাংশন কল
        send_mail_logic(sender, password, to, subject, html_content, is_custom_html, attachments)

        # সফলতার বাইলিঙ্গুয়াল রেসপন্স
        return jsonify({
            "status": "success",
            "message_en": "Email sent successfully with High Quality formatting.",
            "message_bn": "ইমেইল সফলভাবে এবং প্রফেশনাল ফরম্যাটে পাঠানো হয়েছে।",
            "branding": BRAND
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message_en": f"Failed to send email: {str(e)}",
            "message_bn": f"ইমেইল পাঠানো ব্যর্থ হয়েছে: {str(e)}",
            "branding": BRAND
        }), 500

if __name__ == '__main__':
    app.run()
