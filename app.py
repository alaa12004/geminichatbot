from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai



genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            """
✅ تعليمات مهمة:
- جاوب بنفس لغة السؤال (عربي أو إنجليزي).
- بعد عرض أي كود، اشرحه خطوة بخطوة.
- خلي الإجابة منظمة وسهلة، واتبع هذا الشكل:

1. ملخص قصير للفكرة.
2. نقاط رئيسية مختصرة.
3. أمثلة كود إذا لزم.
4. شرح الكود سطر بسطر.
5. ابتعد عن الفقرات الطويلة.
6. المعلومات المهمة او النقاط المهمة خليها بخط غامق.


✅ مثال للإجابة:
👉 What is Python?
---
Python is a programming language that is simple, readable, and widely used.

- Easy to learn: Python has simple syntax.
- Flexible: Supports OOP and procedural programming.
- Rich libraries:
  - Data: pandas, numpy
  - ML: TensorFlow, scikit-learn
  - Web: Flask, Django
- Open-source and free.
- Used in web development, data analysis, AI, automation, and more.

✅ دائماً جاوب بهيك شكل.
"""
        ]
    }
])


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
    app.run(host="0.0.0.0", port=10000)


