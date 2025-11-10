from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

CHATBASE_API_KEY = "35e28390-4160-4e92-b84c-8d11f17f055d"  # 👈 pega aquí tu API key de Chatbase
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

    try:
        response = requests.post(CHATBASE_API_URL, headers=headers, json=payload, timeout=10)
        bot_reply = "Lo siento, ocurrió un error procesando la respuesta."

        if response.status_code == 200:
            data = response.json()
            try:
                bot_reply = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                bot_reply = "No hay respuesta disponible."
    except Exception as e:
        print("⚠️ Error al conectar con Chatbase:", e)
        bot_reply = "Lo siento, no pude procesar tu mensaje."

    print("🤖 Sofía respondió:", bot_reply)

    # Devuelve respuesta a WATI
    return jsonify({"reply": bot_reply}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
