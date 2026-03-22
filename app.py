import os
import json
from flask import Flask, request, jsonify, render_template_string, make_response
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# গ্লোবাল CORS কনফিগারেশন - সব ব্রাউজার এবং লোকাল ফাইল সাপোর্ট করবে
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

# এআই মডেলের অগ্রাধিকার তালিকা (সবচেয়ে স্টেবল মডেলগুলো আগে রাখা হয়েছে)
# gemini-1.5-flash বর্তমানে সবচেয়ে বেশি স্টেবল এবং দ্রুত
AI_MODELS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash-exp",
    "gemini-1.5-pro",
    "gemini-pro"
]

def get_gemini_content(api_key, user_query):
    """গুগল জেমিনি থেকে তথ্য সংগ্রহের মূল ইঞ্জিন (v1beta support)"""
    error_log = []
    
    # এপিআই কনফিগার করা
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        return None, f"Configuration Error: {str(e)}"

    for model_name in AI_MODELS:
        try:
            # মডেল কল করা
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction="You are RX PREMIUM ZONE AI, a high-level coding expert and general assistant. Provide accurate and clean responses."
            )
            
            # জেনারেশন কনফিগারেশন (Timeout এবং Error হ্যান্ডেল করার জন্য)
            response = model.generate_content(
                user_query,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=2048,
                    temperature=0.7,
                )
            )
            
            if response and response.text:
                return response.text, model_name
                
        except Exception as e:
            # এররটি স্টোর করে রাখা হচ্ছে পরবর্তী মডেল ট্রাই করার জন্য
            error_msg = str(e)
            error_log.append(f"{model_name}: {error_msg}")
            continue
            
    # যদি কোনো মডেলই কাজ না করে তবে বিস্তারিত এরর পাঠানো
    return None, f"All models failed. Primary Error: {error_log[0] if error_log else 'Unknown API Error'}"

@app.after_request
def apply_headers(response):
    """ব্রাউজার ব্লক এড়ানোর জন্য প্রোডাকশন লেভেল হেডার"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@app.route('/', methods=['GET', 'POST'])
def root_handler():
    """হোমপেজ এবং স্মার্ট রিডাইরেক্ট হ্যান্ডলার"""
    # যদি মেইন ইউআরএল-এ প্যারামিটার থাকে, তবে সরাসরি এপিআই লজিক প্রসেস করো
    api_param = request.args.get('api') or (request.is_json and request.json.get('api'))
    if api_param:
        return handle_api_logic()
    
    # নতুবা সুন্দর হোমপেজ দেখাও
    return render_template_string(ULTIMATE_UI, dev=DEV_INFO)

@app.route('/api', methods=['GET', 'POST', 'OPTIONS'])
def api_route():
    """ডেডিকেটেড এপিআই এন্ডপয়েন্ট"""
    return handle_api_logic()

def handle_api_logic():
    """এপিআই লজিক যা উভয় এন্ডপয়েন্টে কাজ করবে"""
    if request.method == 'OPTIONS':
        return make_response('', 200)

    # ডাটা সংগ্রহ
    api_key = request.args.get('api')
    prompt = request.args.get('ask')

    if request.is_json:
        json_data = request.get_json(silent=True) or {}
        api_key = api_key or json_data.get('api')
        prompt = prompt or json_data.get('ask')

    # প্যারামিটার না থাকলে এরর
    if not api_key or not prompt:
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "Missing Parameters",
            "message": "দয়া করে 'api' এবং 'ask' প্যারামিটার ব্যবহার করুন।",
            "example": "/api?api=YOUR_KEY&ask=Hello"
        }), 400

    # এআই প্রসেসিং
    ai_text, used_model = get_gemini_content(api_key, prompt)

    if ai_text:
        return jsonify({
            **DEV_INFO,
            "model": used_model,
            "response": ai_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    else:
        # এখানে আপনার ফেইল হওয়া এররটি ডিটেইলসে দেখাবে
        return jsonify({
            **DEV_INFO,
            "status": False,
            "error": "AI Processing Failed",
            "details": used_model
        }), 500

# অত্যন্ত প্রিমিয়াম এবং ডাইনামিক ইউআই (পূর্বের ইউআই থেকে আরও নিখুঁত)
ULTIMATE_UI = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ dev.developer }} | Premium AI Proxy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { 
            background: #02040a; 
            color: #e6edf3; 
            font-family: 'Outfit', sans-serif;
            background-image: radial-gradient(circle at 50% 0%, #0d1117 0%, #02040a 100%);
        }
        .neon-text { text-shadow: 0 0 10px #2f81f7, 0 0 20px #2f81f7; }
        .glass-card { 
            background: rgba(22, 27, 34, 0.7); 
            backdrop-filter: blur(15px); 
            border: 1px solid rgba(48, 54, 61, 0.8);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        }
        .code-font { font-family: 'Fira Code', monospace; }
        .orbitron { font-family: 'Orbitron', sans-serif; }
        .btn-glow:hover { box-shadow: 0 0 20px rgba(47, 129, 247, 0.5); transform: translateY(-2px); }
        .gradient-line { background: linear-gradient(90deg, transparent, #2f81f7, transparent); height: 1px; }
    </style>
</head>
<body class="min-h-screen">

    <div class="max-w-5xl mx-auto px-6 py-16">
        <!-- Header -->
        <header class="text-center mb-20">
            <div class="inline-block px-3 py-1 mb-6 text-[10px] font-bold tracking-[0.2em] text-blue-400 uppercase border border-blue-500/30 rounded-full orbitron">
                Production Ready Middleware
            </div>
            <h1 class="text-5xl md:text-7xl font-extrabold orbitron mb-6 tracking-tighter">
                {{ dev.developer }} <br><span class="neon-text text-blue-500">AI PROXY</span>
            </h1>
            <div class="gradient-line w-1/2 mx-auto mb-8"></div>
            <p class="text-gray-400 text-lg max-w-2xl mx-auto font-light leading-relaxed">
                আপনার ওয়েবসাইট বা অ্যাপের জন্য গুগল জেমিনি এআই ব্যবহারের সবচেয়ে সহজ এবং শক্তিশালী গেটওয়ে। 
                CORS বা প্রক্সি ঝামেলা ভুলে যান, এখন সব হবে নিমিষেই।
            </p>
        </header>

        <!-- Main Content -->
        <div class="grid md:grid-cols-2 gap-8 mb-20">
            <!-- Documentation -->
            <div class="glass-card p-8 rounded-3xl">
                <h3 class="text-xl font-bold mb-6 flex items-center gap-3 orbitron">
                    <i class="fas fa-terminal text-blue-500"></i> API USAGE
                </h3>
                
                <div class="space-y-6">
                    <div>
                        <label class="text-[10px] uppercase tracking-widest text-gray-500 font-bold mb-2 block">GET Endpoint</label>
                        <div class="bg-black/50 p-4 rounded-xl border border-white/5 code-font text-xs text-blue-300 break-all">
                            {{ request.url_root }}api?api=YOUR_KEY&ask=Hello
                        </div>
                    </div>

                    <div>
                        <label class="text-[10px] uppercase tracking-widest text-gray-500 font-bold mb-2 block">POST Body (JSON)</label>
                        <div class="bg-black/50 p-4 rounded-xl border border-white/5 code-font text-xs text-purple-300">
                            {<br>
                            &nbsp;&nbsp;"api": "YOUR_KEY",<br>
                            &nbsp;&nbsp;"ask": "Solve a math problem"<br>
                            }
                        </div>
                    </div>
                </div>
            </div>

            <!-- Contact & Help -->
            <div class="glass-card p-8 rounded-3xl flex flex-col justify-between">
                <div>
                    <h3 class="text-xl font-bold mb-6 flex items-center gap-3 orbitron">
                        <i class="fas fa-headset text-blue-500"></i> SUPPORT
                    </h3>
                    <p class="text-sm text-gray-400 mb-8 leading-relaxed">
                        আপনার এপিআই কি কাজ না করলে বা কোনো টেকনিক্যাল সাপোর্টের প্রয়োজন হলে সরাসরি আমাদের সাথে যোগাযোগ করুন। আমরা ২৪/৭ একটিভ আছি।
                    </p>
                </div>
                
                <div class="flex flex-col gap-3">
                    <a href="https://t.me/Roman_no_1" class="bg-blue-600/10 hover:bg-blue-600/20 border border-blue-600/30 p-4 rounded-2xl flex items-center justify-between group transition btn-glow">
                        <span class="font-bold tracking-wide">Telegram Channel</span>
                        <i class="fab fa-telegram-plane group-hover:translate-x-1 transition"></i>
                    </a>
                    <a href="https://wa.me/8801603410849" class="bg-green-600/10 hover:bg-green-600/20 border border-green-600/30 p-4 rounded-2xl flex items-center justify-between group transition">
                        <span class="font-bold tracking-wide">WhatsApp Help</span>
                        <i class="fab fa-whatsapp group-hover:translate-x-1 transition"></i>
                    </a>
                </div>
            </div>
        </div>

        <!-- JSON Preview -->
        <div class="glass-card p-10 rounded-[40px] border-blue-500/20">
            <h3 class="text-lg font-bold mb-6 orbitron flex items-center gap-3">
                <i class="fas fa-file-code text-blue-500"></i> API RESPONSE FORMAT
            </h3>
            <div class="bg-black/80 p-6 rounded-2xl border border-white/5 code-font text-sm leading-relaxed text-blue-100/80">
                <pre>
{
  "status": true,
  "developer": "{{ dev.developer }}",
  "model": "gemini-1.5-flash",
  "response": "AI will return your answer here...",
  "timestamp": "2024-05-20 14:30:15",
  "contact": {
      "telegram": "{{ dev.contact.telegram }}",
      "channel": "{{ dev.contact.channel }}"
  }
}</pre>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-24 text-center">
            <p class="text-[10px] tracking-[0.5em] text-gray-600 uppercase mb-4 orbitron font-bold">
                &copy; 2024 {{ dev.developer }} | All Rights Reserved
            </p>
        </footer>
    </div>

</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
