from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")

model = genai.GenerativeModel("gemini-1.5-flash")

system_prompt = """
✅ تعليمات مهمة:
- جاوب بنفس لغة السؤال (عربي أو إنجليزي).
- بعد عرض أي كود، اشرحه خطوة بخطوة.
- خلي الإجابة منظمة وسهلة، واتبع هذا الشكل:
1. ملخص قصير للفكرة.
2. نقاط رئيسية مختصرة.
3. أمثلة كود إذا لزم.
4. شرح الكود سطر بسطر.
5. ابتعد عن الفقرات الطويلة.
6. المعلومات المهمة أو النقاط المهمة خليها بخط غامق.

✅ دائماً جاوب بهيك شكل.
"""

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_input = request.json["message"]

        chat = model.start_chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        response = chat.send_message(user_input)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)





