from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

CHATBASE_API_KEY = "35e28390-4160-4e92-b84c-8d11f17f055d"  # 👈 pega aquí la API key que generaste
CHATBASE_API_URL = "https://api.chatbase.co/api/v1/chat"  # endpoint oficial

@app.route("/", methods=["GET"])
def home():
    return "Bot Sofía está activo y conectado a Chatbase!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("📩 Mensaje recibido:", data)

    # Verifica si el mensaje viene con texto
    message = ""
    try:
        message = data.get("text") or data.get("message", {}).get("text", "")
    except:
        pass

    if not message:
        return jsonify({"status": "no text found"}), 200

    # Llama a Chatbase (Sofía)
    payload = {
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {CHATBASE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(CHATBASE_API_URL, headers=headers, json=payload)
    bot_reply = "Lo siento, ocurrió un error procesando la respuesta."

    if response.status_code == 200:
        data = response.json()
        try:
            bot_reply = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            bot_reply = "No hay respuesta disponible."

    print("🤖 Sofía respondió:", bot_reply)

    # Devuelve respuesta a WATI
    retur
