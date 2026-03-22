import os
import json
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
# Enable CORS for all domains and routes to support static HTML/Local files
CORS(app, resources={r"/*": {"origins": "*"}})

# Branding Constants
DEVELOPER_INFO = {
    "status": True,
    "developer": "RX PREMIUM ZONE",
    "contact": {
        "telegram": "@Roman_no_1",
        "whatsapp": "+8801603410849",
        "channel": "@RX_PREMIUM_ZONE"
    }
}

# Model Fallback Configuration
MODELS = [
    "gemini-2.0-flash-exp", 
    "gemini-1.5-flash", 
    "gemini-1.5-pro"
]

def get_gemini_response(api_key, prompt, model_index=0):
    """Handles the AI generation with automatic fallback logic."""
    if model_index >= len(MODELS):
        return None, "All models failed or API key is invalid."
    
    current_model_name = MODELS[model_index]
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(current_model_name)
        
        # Adding a system instruction layer for developer-focused queries
        enhanced_prompt = f"System: Act as a high-level developer assistant. User: {prompt}"
        
        response = model.generate_content(enhanced_prompt)
        return response.text, current_model_name
    except Exception as e:
        # Recursive fallback to the next model in the list
        return get_gemini_response(api_key, prompt, model_index + 1)

@app.route('/', methods=['GET'])
def index():
    """Beautiful documentation landing page."""
    return render_template_string(HTML_TEMPLATE, developer=DEVELOPER_INFO)

@app.route('/api', methods=['GET', 'POST'])
def ai_api():
    """Main API endpoint supporting GET and POST."""
    api_key = ""
    prompt = ""
    
    # 1. Extract Data based on Method
    if request.method == 'GET':
        api_key = request.args.get('api')
        prompt = request.args.get('ask')
    else:
        data = request.get_json(silent=True) or {}
        api_key = data.get('api')
        prompt = data.get('ask')

    # 2. Validation
    if not api_key:
        return jsonify({**DEVELOPER_INFO, "status": False, "error": "Missing 'api' parameter (Gemini API Key)"}), 400
    if not prompt:
        return jsonify({**DEVELOPER_INFO, "status": False, "error": "Missing 'ask' parameter (User Query)"}), 400

    # 3. Process with Gemini
    ai_text, used_model = get_gemini_response(api_key, prompt)

    if ai_text:
        return jsonify({
            **DEVELOPER_INFO,
            "model": used_model,
            "response": ai_text,
            "timestamp": datetime.now().isoformat()
        })
    else:
        return jsonify({
            **DEVELOPER_INFO,
            "status": False,
            "error": "Failed to generate response. Check your API key or quota.",
            "details": used_model # Contains the error message from fallback
        }), 500

# Documentation Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RX PREMIUM ZONE | Gemini AI API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; }
        .gradient-text { background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .card { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        code { color: #f472b6; font-family: monospace; }
    </style>
</head>
<body class="min-h-screen p-4 md:p-10">
    <div class="max-w-4xl mx-auto">
        <!-- Header -->
        <header class="text-center mb-12">
            <h1 class="text-4xl md:text-6xl font-bold mb-4 gradient-text">{{ developer.developer }}</h1>
            <p class="text-gray-400 text-lg">The ultimate Middleware API for Google Gemini. No CORS, no backend required.</p>
            <div class="flex justify-center gap-4 mt-6">
                <a href="https://t.me/Roman_no_1" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-full flex items-center gap-2 transition">
                    <i class="fab fa-telegram"></i> Telegram
                </a>
                <a href="https://wa.me/8801603410849" class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-full flex items-center gap-2 transition">
                    <i class="fab fa-whatsapp"></i> WhatsApp
                </a>
            </div>
        </header>

        <!-- Documentation -->
        <main class="space-y-8">
            <!-- Section 1: GET -->
            <section class="card p-6 rounded-2xl">
                <h2 class="text-2xl font-semibold mb-4 text-sky-400"><i class="fas fa-bolt mr-2"></i>GET Method Usage</h2>
                <p class="text-gray-300 mb-3">Perfect for quick testing or simple browser-based tools.</p>
                <div class="bg-black/50 p-4 rounded-lg overflow-x-auto">
                    <code>{{ request.url_root }}api?api=<span class="text-yellow-400">YOUR_KEY</span>&ask=<span class="text-yellow-400">Hello</span></code>
                </div>
            </section>

            <!-- Section 2: POST -->
            <section class="card p-6 rounded-2xl">
                <h2 class="text-2xl font-semibold mb-4 text-indigo-400"><i class="fas fa-code mr-2"></i>POST Method Usage</h2>
                <p class="text-gray-300 mb-3">Endpoint: <code>/api</code></p>
                <div class="bg-black/50 p-4 rounded-lg overflow-x-auto">
                    <pre class="text-pink-400 text-sm">
{
  "api": "YOUR_GEMINI_API_KEY",
  "ask": "Write a Python login script"
}</pre>
                </div>
            </section>

            <!-- Response Format -->
            <section class="card p-6 rounded-2xl">
                <h2 class="text-2xl font-semibold mb-4 text-emerald-400"><i class="fas fa-reply-all mr-2"></i>Standard Response</h2>
                <div class="bg-black/50 p-4 rounded-lg overflow-x-auto">
                    <pre class="text-gray-300 text-sm">
{
  "status": true,
  "developer": "RX PREMIUM ZONE",
  "model": "gemini-2.0-flash-exp",
  "response": "Generated AI content here...",
  "contact": { ... }
}</pre>
                </div>
            </section>
        </main>

        <!-- Footer -->
        <footer class="mt-20 pt-8 border-t border-white/10 text-center text-gray-500 text-sm">
            <p>&copy; 2024 {{ developer.developer }}. Designed for the developer community.</p>
            <p class="mt-2">Join Channel: {{ developer.contact.channel }}</p>
        </footer>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
