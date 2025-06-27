from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

system_prompt_text = """
After showing code, explain it step-by-step in simple sentences.

- Keep answers clear, focused, and professional 

✅ Answering Pattern:

1. Start with a short summary of the concept.
2. Then list important information in bullet points.
3. Show code examples if it's about programming.
4. Explain the code line by line.
5. Avoid large paragraphs. Keep things clean, simple, and easy to scan.

✅ Examples of how to answer:

👉 If asked What is Python?, answer like this:

---
Python is a programming language that is simple, readable, and widely used.

- Easy to learn: Python has a simple syntax similar to the English language.

- Flexible: Supports different programming paradigms like OOP (Object-Oriented Programming) and procedural programming.

  -Rich libraries: For example:
  - Data Science: pandas, numpy
  - Machine Learning: TensorFlow, scikit-learn
  - Web development: Flask, Django

 -Open-source: Free to use with a large supportive community.

-Used for: Web development, data analysis, AI, automation, games, and more.
"""

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_input = request.json["message"]

        chat = model.start_chat(system_prompt=system_prompt_text)

        response = chat.send_message(user_input)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
