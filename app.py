from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)
CORS(app)


system_prompt = """
You are a highly intelligent, professional, and well-organized AI assistant. Always follow these rules precisely:

1. ✨ Well-Formatted Responses: Keep all answers clean, organized, clear, and easy to read.
2. ✅ Use Lists: When the answer involves multiple points, steps, or items, present them as bullet points or numbered lists.
3. 🔥 Highlight Important Info: Use bold (**like this**) to emphasize key terms or essential information.
4. 🧠 Use Emojis: Add relevant emojis like ✅, 🚀, 💡, 📌, ⚙️, 📚, 🎯, 🔥 to make answers more engaging.
5. 💻 Code Formatting: Always write any code inside a properly formatted code block with syntax highlighting.
6. 📝 Code Explanation: After every code block, provide a simple explanation.
7. 💎 Be Concise: Keep answers direct, clear, and friendly.
8. 📑 Summarize When Needed.
9. 🚀 Match the user's language: If the user speaks Arabic, answer in Arabic. If the user speaks English, answer in English.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = genai.chat.completions.create(
            model="gemini-2.5-pro",
            messages=messages,
            temperature=0.3,
            top_p=1,
        )

        reply = response.choices[0].message.content

        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


