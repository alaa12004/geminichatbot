from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai


genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat()

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_input = request.json["message"]
        response = chat.send_message(user_input)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

if __name__ == "__main__":
    app.run()
