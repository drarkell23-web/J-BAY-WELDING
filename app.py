from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='public')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ TELEGRAM CONFIGURATION
TELEGRAM_TOKEN = "8595813958:AAFpKSuq9j_qny2DlIgP2rJwHe1Mu_xTsDU"
CHAT_ID = "8187670531"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        # Get text data
        name = request.form.get('name')
        phone = request.form.get('phone')
        service = request.form.get('service')
        description = request.form.get('description')

        caption = (
            f"🚀 *NEW JOB: J-BAY WELDERS*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Client:* {name}\n"
            f"📞 *Phone:* {phone}\n"
            f"🛠 *Service:* {service}\n\n"
            f"📝 *Details:*\n{description}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        # Check if an image was uploaded
        image = request.files.get('image')

        if image:
            # Send with Photo
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': (image.filename, image.read(), image.content_type)}
            data = {'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
            response = requests.post(url, data=data, files=files)
        else:
            # Send Text Only
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'Markdown'}
            response = requests.post(url, data=data)

        if response.status_code == 200:
            print("✅ Success: Message sent to Telegram")
            return jsonify({"success": True}), 200
        else:
            print(f"❌ Telegram Error: {response.text}")
            return jsonify({"error": "Telegram rejected the message"}), 400

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 J-Bay Welders Python System Live on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)