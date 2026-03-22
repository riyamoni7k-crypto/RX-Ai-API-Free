import os
import json
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# ফুল CORS সাপোর্ট (গ্লোবাল লেভেলে)
CORS(app, resources={r"/*": {"origins": "*"}})

# ব্র্যান্ডিং এবং ডেভেলপার ইনফরমেশন
DEV_INFO = {
    "status": True,
    "developer": "RX PREMIUM ZONE",
    "contact": {
        "telegram": "@Roman_no_1",
        "whatsapp": "+8801603410849",
        "channel": "@RX_PREMIUM_ZONE"
    }
}

# এআই মডেল লিস্ট (ফলব্যাক সিস্টেম)
MODELS = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"]

def get_ai_content(api_key, query):
    """গুগল জেমিনি থেকে রেসপন্স আনার মূল ফাংশন"""
    last_error = ""
    for model_id in MODELS:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=model_id,
                system_instruction="You are RX PREMIUM ZONE AI. Be professional, concise and accurate."
            )
            response = model.generate_content(query)
            if response and response.text:
                return response.text, model_id
        except Exception as e:
            last_error = str(e)
            continue
    return None, last_error

@app.after_request
def add_cors_headers(response):
    """ম্যানুয়ালি হেডার সেট করা যাতে কোনো ব্রাউজার ব্লক না করে"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/', methods=['GET'])
def landing():
    """অত্যন্ত কালারফুল এবং নিওন স্টাইলের হোমপেজ"""
    return render_template_string(PREMIUM_UI, dev=DEV_INFO)

@app.route('/api', methods=['GET', 'POST', 'OPTIONS'])
def handle_api():
    """মূল এপিআই গেটওয়ে"""
    if request.method == 'OPTIONS':
        return make_response('', 200)

    # ডাটা এক্সট্রাকশন (GET এবং POST উভয় সাপোর্ট করে)
    api_key = request.args.get('api')
    prompt = request.args.get('ask')

    if request.is_json:
        data = request.get_json(silent=True) or {}
        api_key = api_key or data.get('api')
        prompt = prompt or data.get('ask')

    # ভ্যালিডেশন এবং এরর হ্যান্ডেলিং
    if not api_key or not prompt:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "Invalid Request Format",
            "message": "সঠিকভাবে রিকোয়েস্ট পাঠান। উদাহরণ: /api?api=YOUR_KEY&ask=Hello",
            "usage": {
                "GET": "/api?api=YOUR_API_KEY&ask=YOUR_QUESTION",
                "POST": {"api": "YOUR_API_KEY", "ask": "YOUR_QUESTION"}
            }
        }), 400

    # এআই প্রসেসিং
    result, used_model = get_ai_content(api_key, prompt)

    if result:
        return jsonify({
            **DEV_INFO,
            "model": used_model,
            "response": result,
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "AI Processing Failed",
            "details": used_model
        }), 500

@app.errorhandler(404)
def not_found(e):
    """ভুল URL এ রিকোয়েস্ট পাঠালে এটি দেখাবে"""
    return jsonify({
        **DEV_INFO,
        "status": False,
        "error": "Wrong Endpoint",
        "message": "আপনি ভুল লিংকে রিকোয়েস্ট পাঠিয়েছেন। দয়া করে /api এন্ডপয়েন্ট ব্যবহার করুন।"
    }), 404

# প্রিমিয়াম নিওন ইউআই ডিজাইন
PREMIUM_UI = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RX PREMIUM ZONE | AI Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { 
            background: #050505; 
            color: #fff; 
            font-family: 'Rajdhani', sans-serif;
            overflow-x: hidden;
        }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        .neon-glow {
            text-shadow: 0 0 10px #3b82f6, 0 0 20px #3b82f6, 0 0 40px #3b82f6;
        }
        .card-neon {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.1);
            transition: 0.3s;
        }
        .card-neon:hover {
            border-color: #3b82f6;
            box-shadow: 0 0 25px rgba(59, 130, 246, 0.3);
            transform: translateY(-5px);
        }
        .gradient-bg {
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        }
        .animate-pulse-slow {
            animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 0.6; }
        }
    </style>
</head>
<body class="relative">
    <!-- Background Decoration -->
    <div class="fixed top-0 left-0 w-full h-full -z-10 opacity-20 pointer-events-none">
        <div class="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-blue-600 rounded-full blur-[120px] animate-pulse-slow"></div>
        <div class="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-purple-600 rounded-full blur-[120px] animate-pulse-slow"></div>
    </div>

    <div class="max-w-6xl mx-auto px-6 py-12">
        <!-- Main Header -->
        <header class="text-center mb-16">
            <div class="inline-block px-4 py-1 mb-4 text-xs font-bold tracking-widest text-blue-400 uppercase border border-blue-400/30 rounded-full orbitron bg-blue-400/5">
                Next-Gen AI Bridge
            </div>
            <h1 class="text-6xl md:text-8xl font-bold orbitron mb-6 neon-glow">{{ dev.developer }}</h1>
            <p class="text-xl text-gray-400 max-w-2xl mx-auto mb-8 font-light">
                গুগল জেমিনি এপিআই-কে এখন ব্যবহার করুন যেকোনো ফ্রন্টএন্ড থেকে, কোনো ব্যাকএন্ড কোডিং বা CORS লিমিটেশন ছাড়াই।
            </p>
            
            <div class="flex flex-wrap justify-center gap-6">
                <a href="https://t.me/Roman_no_1" target="_blank" class="gradient-bg px-8 py-4 rounded-2xl font-bold flex items-center gap-3 hover:scale-105 transition shadow-lg shadow-blue-500/20">
                    <i class="fab fa-telegram-plane text-xl"></i> Telegram Contact
                </a>
                <a href="https://wa.me/8801603410849" target="_blank" class="bg-white/5 border border-white/10 px-8 py-4 rounded-2xl font-bold flex items-center gap-3 hover:bg-white/10 transition">
                    <i class="fab fa-whatsapp text-xl text-green-400"></i> WhatsApp Help
                </a>
            </div>
        </header>

        <!-- Documentation Section -->
        <div class="grid lg:grid-cols-3 gap-8 mb-16">
            <!-- Usage 1 -->
            <div class="card-neon p-8 rounded-3xl">
                <div class="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center mb-6 border border-blue-500/30">
                    <i class="fas fa-bolt text-blue-400 text-xl"></i>
                </div>
                <h3 class="text-2xl font-bold mb-4 orbitron text-blue-300">GET Method</h3>
                <p class="text-gray-400 mb-6 text-sm">URL প্যারামিটার ব্যবহার করে খুব সহজে রিকোয়েস্ট পাঠান।</p>
                <div class="bg-black/60 p-4 rounded-xl border border-white/5 font-mono text-xs overflow-x-auto text-blue-200">
                    /api?api=<span class="text-yellow-400">YOUR_KEY</span>&ask=<span class="text-yellow-400">Hi</span>
                </div>
            </div>

            <!-- Usage 2 -->
            <div class="card-neon p-8 rounded-3xl">
                <div class="w-12 h-12 bg-purple-500/20 rounded-xl flex items-center justify-center mb-6 border border-purple-500/30">
                    <i class="fas fa-paper-plane text-purple-400 text-xl"></i>
                </div>
                <h3 class="text-2xl font-bold mb-4 orbitron text-purple-300">POST Method</h3>
                <p class="text-gray-400 mb-6 text-sm">অ্যাপ্লিকেশন ডেভেলপমেন্টের জন্য JSON পে-লোড সাপোর্ট।</p>
                <div class="bg-black/60 p-4 rounded-xl border border-white/5 font-mono text-xs text-purple-200">
                    {<br>
                    &nbsp;&nbsp;"api": "YOUR_KEY",<br>
                    &nbsp;&nbsp;"ask": "Hello Gemini"<br>
                    }
                </div>
            </div>

            <!-- Features -->
            <div class="card-neon p-8 rounded-3xl">
                <div class="w-12 h-12 bg-emerald-500/20 rounded-xl flex items-center justify-center mb-6 border border-emerald-500/30">
                    <i class="fas fa-shield-alt text-emerald-400 text-xl"></i>
                </div>
                <h3 class="text-2xl font-bold mb-4 orbitron text-emerald-300">Key Features</h3>
                <ul class="text-gray-400 text-sm space-y-3">
                    <li class="flex items-center gap-2"><i class="fas fa-check text-emerald-500"></i> No CORS Policy Errors</li>
                    <li class="flex items-center gap-2"><i class="fas fa-check text-emerald-500"></i> Auto Model Fallback</li>
                    <li class="flex items-center gap-2"><i class="fas fa-check text-emerald-500"></i> Faster Response Time</li>
                    <li class="flex items-center gap-2"><i class="fas fa-check text-emerald-500"></i> Clean JSON Output</li>
                </ul>
            </div>
        </div>

        <!-- JSON Preview Area -->
        <div class="card-neon p-10 rounded-[40px] relative overflow-hidden">
            <div class="absolute top-0 right-0 p-4">
                <span class="flex h-3 w-3">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
            </div>
            <h3 class="text-3xl font-bold mb-8 orbitron flex items-center gap-4">
                <i class="fas fa-terminal text-blue-500"></i> JSON Output Example
            </h3>
            <div class="bg-black/80 rounded-2xl p-6 border border-white/10 font-mono text-sm leading-relaxed text-blue-100 shadow-inner">
                <pre>
{
  "status": true,
  "developer": "{{ dev.developer }}",
  "model": "gemini-2.0-flash-exp",
  "response": "Hello! I am your AI Assistant powered by RX PREMIUM ZONE...",
  "contact": {
      "telegram": "{{ dev.contact.telegram }}",
      "channel": "{{ dev.contact.channel }}"
  }
}</pre>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-24 pb-12 text-center">
            <div class="flex justify-center gap-8 mb-8 text-gray-400 text-2xl">
                <a href="https://t.me/Roman_no_1" class="hover:text-blue-400 transition"><i class="fab fa-telegram"></i></a>
                <a href="#" class="hover:text-green-400 transition"><i class="fab fa-whatsapp"></i></a>
                <a href="#" class="hover:text-pink-400 transition"><i class="fab fa-instagram"></i></a>
            </div>
            <p class="text-gray-500 font-light orbitron tracking-widest uppercase text-xs">
                &copy; 2024 {{ dev.developer }} | Created for Innovation
            </p>
        </footer>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
