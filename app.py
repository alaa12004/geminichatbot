from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_input = request.json["message"]

        
        chat = model.start_chat()

        system_prompt_text = """
Answer in the same language of the question.
(If the question is in Arabic, answer in Arabic. If in English, answer in English.)

When answering:
- Use **clear**, **simple**, and **direct** language.
- Organize the answer in **bullet points** or **numbered lists**.
- Add **line breaks** between points to make it easy to read.
- Highlight important words or terms using **bold** (surrounded by ** like this).
- Always write code inside code blocks like this:

```python
print("Hello, world!")
"""

        
        full_prompt = f"{system_prompt_text}\nUser: {user_input}"


        response = chat.send_message(full_prompt)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"حدث خطأ: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
