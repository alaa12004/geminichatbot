from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai


genai.configure(api_key="AIzaSyBjO-eYYJR7DRS-GiDROV3jbsYwymz79EQ")


model = genai.GenerativeModel("gemini-1.5-flash")


system_prompt = """
✅ Important Instructions:
- Answer in the same language as the question (Arabic or English).
- After showing any code, explain it step by step.
- Keep the answer organized and simple. Follow this structure:
1. A short summary of the idea.
2. Key points in brief.
3. Code examples if needed.
4. Line-by-line code explanation.
5. Avoid long paragraphs.
6. Highlight important information or key points in **bold**.

✅ Always follow this format.
"""

# Create chat session
chat = model.start_chat()

# Send system prompt as the first message to set the context
chat.send_message(system_prompt)

# Set up Flask app
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_api():
    try:
        user_input = request.json.get("message")

        # Send user input to Gemini chat
        response = chat.send_message(user_input)

        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
