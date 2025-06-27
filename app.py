from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai


genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")


    {
        "role": "user",
        "parts": [
            """
🔸 Answer based on the language of the question (Arabic or English).
🔸 After showing any code, explain it step-by-step in simple sentences.
🔸 Follow this answering style:
1. Short and clear summary of the concept.
2. Bullet points for key information.
3. Code examples inside code blocks if needed.
4. Line-by-line code explanation.
5. Keep it neat, easy to read, and avoid long paragraphs.

✅ Example of how to answer:
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

✅ Always answer in this clean and structured style.
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

