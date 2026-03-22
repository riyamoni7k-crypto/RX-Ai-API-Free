import os
import json
import time
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# ফুল CORS সাপোর্ট নিশ্চিত করা যাতে লোকাল HTML বা অন্য ব্রাউজার থেকে রিকোয়েস্ট ব্লক না হয়
CORS(app, resources={r"/*": {"origins": "*"}})

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

# ২০২৬ সালের লেটেস্ট এবং স্টেবল মডেল লিস্ট
# ১. gemini-2.0-flash: সুপার ফাস্ট এবং স্টেবল
# ২. gemini-2.0-pro-exp-02-05: হাই-লেভেল কোডিং এবং রিসার্চের জন্য
AI_MODELS = [
    "gemini-2.0-flash", 
    "gemini-2.0-pro-exp-02-05",
    "gemini-1.5-flash-latest"
]

def get_ai_response(api_key, query):
    """এটি ২০২৬ সালের লেটেস্ট এপিআই মেথড ব্যবহার করে রেসপন্স জেনারেট করে"""
    error_list = []
    
    # এপিআই কি কনফিগার করা
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        return None, f"API Configuration Failed: {str(e)}"

    for model_name in AI_MODELS:
        try:
            # লেটেস্ট জেনারেটিভ মডেল অবজেক্ট তৈরি
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are RX PREMIUM ZONE AI, a professional developer assistant. Response must be high-quality and verified."
            )
            
            # জেনারেশন কনফিগারেশন (Safety settings এবং temperature অপ্টিমাইজড)
            generation_config = {
                "temperature": 0.8,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }

            # এপিআই কল করা (v1beta স্টাইল)
            response = model.generate_content(
                query,
                generation_config=generation_config
            )
            
            if response and response.text:
                return response.text, model_name
                
        except Exception as e:
            error_list.append(f"{model_name}: {str(e)}")
            continue # পরবর্তী মডেলে ফলব্যাক করবে
            
    return None, f"সবগুলো মডেল ফেইল করেছে। এরর: {error_list[0] if error_list else 'API Key Invalid or Quota Exceeded'}"

# ব্রাউজার সিকিউরিটি (CORS) এর জন্য কাস্টম হেডার মিডলওয়্যার
@app.after_request
def after_request_func(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    """স্মার্ট ইউআই যা এপিআই প্যারামিটার থাকলে সরাসরি রেসপন্স দিবে"""
    api_key = request.args.get('api') or (request.json.get('api') if request.is_json else None)
    ask_query = request.args.get('ask') or (request.json.get('ask') if request.is_json else None)

    if api_key and ask_query:
        return handle_logic(api_key, ask_query)
    
    # যদি প্যারামিটার না থাকে তবে সুন্দর ড্যাশবোর্ড দেখাবে
    return render_template_string(UI_HTML, dev=DEV_INFO)

@app.route('/api', methods=['GET', 'POST', 'OPTIONS'])
def api_endpoint():
    """ডেডিকেটেড এপিআই গেটওয়ে"""
    if request.method == 'OPTIONS':
        return make_response('', 200)

    api_key = request.args.get('api') or (request.json.get('api') if request.is_json else None)
    ask_query = request.args.get('ask') or (request.json.get('ask') if request.is_json else None)

    return handle_logic(api_key, ask_query)

def handle_logic(api_key, query):
    """কোর এপিআই লজিক"""
    if not api_key or not query:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "Missing Information",
            "message": "সঠিকভাবে রিকোয়েস্ট পাঠান। উদাহরণ: ?api=YOUR_KEY&ask=Hello"
        }), 400

    ai_text, model_id = get_ai_response(api_key, query)

    if ai_text:
        return jsonify({
            **DEV_INFO,
            "model": model_id,
            "response": ai_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "AI Request Failed",
            "details": model_id
        }), 500

# ২০২৬ সালের প্রিমিয়াম ডার্ক নিওন ইউআই
UI_HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ dev.developer }} | Premium AI Proxy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Quicksand:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #010409; color: #c9d1d9; font-family: 'Quicksand', sans-serif; overflow-x: hidden; }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        .neon-bg { background: linear-gradient(135deg, #007cf0 0%, #00dfd8 100%); }
        .card-blur { background: rgba(13, 17, 23, 0.8); backdrop-filter: blur(15px); border: 1px solid rgba(48, 54, 61, 1); }
        .neon-text { text-shadow: 0 0 10px #007cf0, 0 0 20px #007cf0; }
        .btn-hover:hover { box-shadow: 0 0 25px rgba(0, 124, 240, 0.6); transform: translateY(-3px); transition: all 0.3s ease; }
        pre { background: #0d1117; padding: 1rem; border-radius: 1rem; border: 1px solid #30363d; color: #58a6ff; font-family: monospace; }
    </style>
</head>
<body class="min-h-screen relative">
    
    <!-- Hero Section -->
    <div class="container mx-auto px-6 py-20 max-w-6xl relative z-10">
        <header class="text-center mb-24">
            <div class="inline-block px-4 py-1 mb-6 text-[10px] font-bold tracking-[0.3em] text-blue-400 uppercase border border-blue-500/30 rounded-full orbitron">
                2026 NEXT-GEN MIDDLEWARE
            </div>
            <h1 class="text-6xl md:text-8xl font-black orbitron mb-6 neon-text text-white">
                {{ dev.developer }}
            </h1>
            <p class="text-xl text-gray-400 max-w-3xl mx-auto font-light leading-relaxed">
                গুগল জেমিনি এপিআই-কে এখন সরাসরি এইচটিএমএল বা লোকাল প্রজেক্টে ব্যবহার করুন। 
                কোনো CORS এরর নেই, কোনো সার্ভার সেটাপ নেই—সবই অটোমেটিক।
            </p>
        </header>

        <!-- Documentation Grid -->
        <div class="grid md:grid-cols-2 gap-10">
            <!-- Documentation -->
            <div class="card-blur p-10 rounded-[2.5rem] relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full -mr-16 -mt-16 blur-3xl"></div>
                <h3 class="text-2xl font-bold mb-8 orbitron flex items-center gap-4">
                    <i class="fas fa-code text-blue-500"></i> API Endpoint
                </h3>
                
                <div class="space-y-6">
                    <div>
                        <p class="text-xs font-bold text-gray-500 uppercase mb-3 tracking-widest">GET Request</p>
                        <pre class="text-xs break-all">/api?api=YOUR_KEY&ask=Hello</pre>
                    </div>
                    <div>
                        <p class="text-xs font-bold text-gray-500 uppercase mb-3 tracking-widest">POST Payload (JSON)</p>
                        <pre class="text-xs">
{
  "api": "GEMINI_API_KEY",
  "ask": "Solve a coding problem"
}</pre>
                    </div>
                </div>
            </div>

            <!-- Developer Contact -->
            <div class="card-blur p-10 rounded-[2.5rem] flex flex-col justify-between">
                <div>
                    <h3 class="text-2xl font-bold mb-6 orbitron flex items-center gap-4">
                        <i class="fas fa-bolt text-yellow-500"></i> Support
                    </h3>
                    <p class="text-gray-400 mb-8 leading-relaxed">
                        এপিআই কাজ না করলে বা আপনার কাস্টম ফিচারের প্রয়োজন হলে সরাসরি আমাদের সাথে যোগাযোগ করুন। আমরা ২৪ ঘণ্টার মধ্যেই সাপোর্ট প্রদান করি।
                    </p>
                </div>
                
                <div class="space-y-4">
                    <a href="https://t.me/Roman_no_1" class="neon-bg p-5 rounded-2xl flex items-center justify-between text-black font-black uppercase tracking-wider btn-hover">
                        Telegram Chat <i class="fab fa-telegram-plane"></i>
                    </a>
                    <a href="https://wa.me/8801603410849" class="bg-white/5 border border-white/10 p-5 rounded-2xl flex items-center justify-between font-bold text-green-400 btn-hover">
                        WhatsApp Help <i class="fab fa-whatsapp"></i>
                    </a>
                </div>
            </div>
        </div>

        <!-- JSON Showcase -->
        <div class="mt-12 card-blur p-10 rounded-[2.5rem] border-blue-500/20">
            <div class="flex items-center gap-3 mb-8">
                <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                <span class="text-xs font-mono text-gray-500 ml-4 tracking-widest uppercase">Response.json</span>
            </div>
            <pre class="text-sm md:text-base leading-relaxed">
{
  "status": true,
  "developer": "{{ dev.developer }}",
  "model": "gemini-2.0-flash",
  "response": "Hello Master! How can I assist you today?",
  "timestamp": "2026-03-22 14:30:15",
  "contact": { "telegram": "@Roman_no_1", ... }
}</pre>
        </div>

        <!-- Footer -->
        <footer class="mt-32 text-center text-gray-600">
            <p class="orbitron font-bold text-[10px] tracking-[0.5em] uppercase mb-4">Official RX Premium AI Proxy</p>
            <p class="text-[10px] uppercase tracking-widest">© 2026 {{ dev.developer }} All Rights Reserved</p>
        </footer>
    </div>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
