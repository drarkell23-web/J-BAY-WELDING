from flask import Flask, request, jsonify, send_from_directory
import requests
import os

# Initialize Flask and point to your 'public' folder where index.html lives
app = Flask(__name__, static_folder='public')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ TELEGRAM CONFIGURATION (AUTHENTICATED)
TELEGRAM_TOKEN = "8595813958:AAFpKSuq9j_qny2DlIgP2rJwHe1Mu_xTsDU"
CHAT_ID = "8187670531"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    """Serves the front-end website."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    """Receives data from the website form and forwards to Telegram."""
    try:
        # Get text data from the form
        name = request.form.get('name')
        phone = request.form.get('phone')
        service = request.form.get('service')
        description = request.form.get('description')

        # Format the Telegram Message
        caption = (
            f"🚀 *NEW JOB: J-BAY WELDERS*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 *Client:* {name}\n"
            f"📞 *Phone:* {phone}\n"
            f"🛠 *Service:* {service}\n\n"
            f"📝 *Details:*\n{description}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        # Check if an image/screenshot was uploaded or pasted
        image = request.files.get('image')

        if image:
            # Send to Telegram with Photo
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
            files = {'photo': (image.filename, image.read(), image.content_type)}
            data = {'chat_id': CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
            response = requests.post(url, data=data, files=files)
        else:
            # Send Text-Only Message
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {'chat_id': CHAT_ID, 'text': caption, 'parse_mode': 'Markdown'}
            response = requests.post(url, data=data)

        # Log results to terminal
        if response.status_code == 200:
            print(f"✅ Lead from {name} sent to Telegram!")
            return jsonify({"success": True}), 200
        else:
            print(f"❌ Telegram API Error: {response.text}")
            return jsonify({"error": "Telegram rejected the message"}), 400

    except Exception as e:
        print(f"❌ Critical Server Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get port from environment for Cloud Deployment (Render), default to 5000 for local
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 J-Bay Welders System Live on Port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
