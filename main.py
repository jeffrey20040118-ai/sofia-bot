from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot Sofía está activo!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # Aquí puedes ver lo que envía WhatsApp
    print("Mensaje recibido:", data)
    
    # Respuesta de ejemplo
    response = {"reply": "Hola! Soy Sofía, tu bot de AFORE."}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
