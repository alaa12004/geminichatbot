from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# تحقق من وجود المفتاح السري
api_key = os.getenv("API_KEY")
if not api_key:
    print("⚠️ يرجى إضافة API_KEY في إعدادات Render")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        prompt = f"أجب بلغة عربية بسيطة ومناسبة للأطفال: {user_message}"
        
        response = model.generate_content(prompt)
        reply = response.text if response.text else "لم أفهم السؤال"
        
        return jsonify({"reply": reply, "status": "success"})

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
