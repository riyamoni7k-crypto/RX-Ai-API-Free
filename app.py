import os
import json
import time
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# ফুল CORS সাপোর্ট নিশ্চিত করা (যেকোনো ডোমেইন থেকে অ্যাক্সেস করার জন্য)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ব্র্যান্ডিং এবং ডেভেলপার তথ্য
DEV_INFO = {
    "status": True,
    "developer": "RX PREMIUM ZONE",
    "contact": {
        "telegram": "@Roman_no_1",
        "whatsapp": "+8801603410849",
        "channel": "@RX_PREMIUM_ZONE"
    }
}

# সাপোর্ট করা মডেলের তালিকা (অটোমেটিক ফলব্যাক সিস্টেম)
AVAILABLE_MODELS = [
    "gemini-2.0-flash-exp",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def generate_ai_response(api_key, user_query):
    """এটি জেমিনি এপিআই কল করে এবং এরর হলে পরবর্তী মডেল ট্রাই করে"""
    errors = []
    for model_name in AVAILABLE_MODELS:
        try:
            genai.configure(api_key=api_key)
            # জেনারেশন কনফিগারেশন (দ্রুত রেসপন্সের জন্য)
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are a highly professional AI Assistant by RX PREMIUM ZONE. Focus on code, logic, and accurate research."
            )
            
            # এপিআই রিকোয়েস্ট পাঠানো
            response = model.generate_content(user_query)
            
            if response and response.text:
                return response.text, model_name
        except Exception as e:
            errors.append(f"{model_name}: {str(e)}")
            continue # পরবর্তী মডেলে চলে যাবে
            
    return None, f"All models failed. Last error: {errors[-1] if errors else 'Unknown'}"

# CORS প্রি-ফ্লাইট রিকোয়েস্ট হ্যান্ডেল করার জন্য মিডলওয়্যার
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def home():
    """অত্যন্ত প্রফেশনাল ডকুমেন্টেশন ল্যান্ডিং পেজ"""
    return render_template_string(DOCS_HTML, dev=DEV_INFO)

@app.route('/api', methods=['GET', 'POST', 'OPTIONS'])
def api_handler():
    # OPTIONS রিকোয়েস্ট হ্যান্ডেল করা (ব্রাউজার সিকিউরিটির জন্য)
    if request.method == 'OPTIONS':
        return make_response('', 200)

    # ইনপুট ডাটা গ্রহণ
    api_key = request.args.get('api') or (request.json.get('api') if request.is_json else None)
    prompt = request.args.get('ask') or (request.json.get('ask') if request.is_json else None)

    # ভ্যালিডেশন
    if not api_key:
        return jsonify({**DEV_INFO, "status": False, "error": "API Key is required"}), 400
    if not prompt:
        return jsonify({**DEV_INFO, "status": False, "error": "Ask query is required"}), 400

    # এআই রেসপন্স জেনারেট করা
    ai_response, model_used = generate_ai_response(api_key, prompt)

    if ai_response:
        return jsonify({
            **DEV_INFO,
            "model": model_used,
            "response": ai_response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "Failed to process request",
            "details": model_used
        }), 500

# প্রিমিয়াম ডিজাইন টেমপ্লেট
DOCS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ dev.developer }} | AI Middleware</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Poppins', sans-serif; background: radial-gradient(circle at top right, #1e293b, #0f172a); color: #e2e8f0; }
        .glass { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); }
        .gradient-text { background: linear-gradient(135deg, #60a5fa, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        pre { background: #020617 !important; color: #a5f3fc !important; border-radius: 12px; padding: 15px; overflow-x: auto; border: 1px solid #1e293b; }
    </style>
</head>
<body class="min-h-screen">

    <div class="container mx-auto px-4 py-12 max-w-5xl">
        <!-- Header -->
        <div class="text-center mb-16">
            <div class="inline-block px-4 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-bold uppercase tracking-widest mb-4">Production Level API</div>
            <h1 class="text-5xl md:text-7xl font-bold mb-6 gradient-text tracking-tight">{{ dev.developer }}</h1>
            <p class="text-lg text-gray-400 max-w-2xl mx-auto">Gemini AI মিডলওয়্যার প্রক্সি। কোনো CORS ঝামেলা ছাড়াই সরাসরি আপনার ক্লায়েন্ট-সাইড প্রজেক্টে এআই ব্যবহার করুন।</p>
            
            <div class="flex flex-wrap justify-center gap-4 mt-8">
                <a href="https://t.me/Roman_no_1" target="_blank" class="glass px-6 py-3 rounded-xl flex items-center gap-2 hover:bg-white/5 transition border-blue-500/30">
                    <i class="fab fa-telegram text-blue-400"></i> @Roman_no_1
                </a>
                <a href="https://wa.me/8801603410849" target="_blank" class="glass px-6 py-3 rounded-xl flex items-center gap-2 hover:bg-white/5 transition border-green-500/30">
                    <i class="fab fa-whatsapp text-green-400"></i> WhatsApp
                </a>
            </div>
        </div>

        <!-- Documentation Grid -->
        <div class="grid md:grid-cols-2 gap-8">
            <!-- GET Usage -->
            <div class="glass p-8 rounded-3xl">
                <h3 class="text-2xl font-bold mb-4 flex items-center gap-3">
                    <span class="p-2 bg-blue-500/20 rounded-lg"><i class="fas fa-link text-blue-400"></i></span>
                    GET Method
                </h3>
                <p class="text-gray-400 mb-4 text-sm">সরাসরি ব্রাউজার বা ইমেজ জেনারেশন টুলে ব্যবহার করার জন্য সেরা।</p>
                <div class="text-xs font-mono mb-2 text-gray-500 uppercase">Endpoint URL:</div>
                <pre class="text-xs break-all">/api?api=YOUR_KEY&ask=Hello</pre>
            </div>

            <!-- POST Usage -->
            <div class="glass p-8 rounded-3xl">
                <h3 class="text-2xl font-bold mb-4 flex items-center gap-3">
                    <span class="p-2 bg-purple-500/20 rounded-lg"><i class="fas fa-microchip text-purple-400"></i></span>
                    POST Method
                </h3>
                <p class="text-gray-400 mb-4 text-sm">অ্যাপ্লিকেশন বা কমপ্লেক্স রিকোয়েস্টের জন্য JSON পে-লোড।</p>
                <pre class="text-xs">
{
  "api": "GEMINI_KEY",
  "ask": "Solve this math..."
}</pre>
            </div>
        </div>

        <!-- Example Response -->
        <div class="mt-12 glass p-8 rounded-3xl">
            <h3 class="text-2xl font-bold mb-6 flex items-center gap-3">
                <span class="p-2 bg-emerald-500/20 rounded-lg"><i class="fas fa-check-circle text-emerald-400"></i></span>
                API Response Format
            </h3>
            <pre class="text-sm">
{
  "status": true,
  "developer": "RX PREMIUM ZONE",
  "model": "gemini-2.0-flash-exp",
  "response": "Hello! I am Gemini, how can I help you today?",
  "timestamp": "2024-05-20 12:00:00",
  "contact": { "telegram": "@Roman_no_1", ... }
}</pre>
        </div>

        <!-- Footer -->
        <footer class="mt-20 text-center text-gray-500 text-sm">
            <p>&copy; 2024 {{ dev.developer }} | All Rights Reserved.</p>
            <p class="mt-2">Official Channel: <span class="text-blue-400">{{ dev.contact.channel }}</span></p>
        </footer>
    </div>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
