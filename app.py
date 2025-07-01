from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re


load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)
CORS(app)

def format_response(text):
    """تحسين تنسيق الإجابة"""
    if not text:
        return "⚠️ لم أتمكن من توليد إجابة"
    

    text = re.sub(r'```(python)?(.*?)```', 
                r'<div class="code-box"><pre>\2</pre></div>',
                text, flags=re.DOTALL)
    
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(\d+\.\s)', r'<br>\1', text)
    

    replacements = {
        "السؤال:": "❓ السؤال:",
        "الجواب:": "💡 الجواب:",
        "مثال:": "📌 مثال:",
        "ملاحظة:": "📝 ملاحظة:"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "الرسالة فارغة"}), 400

    
        prompt = f"""
        أنت مساعد برمجي خبير. اشرح المفاهيم بطريقة منظمة:
        - استخدم نقاطًا مرقمة
        - ضع الكود في صندوق مخصص
        - **اجعل الكلمات المهمة غامقة**
        - اشرح الكود بعد عرضه
        - التزم بالعربية الفصحى

        السؤال: {user_message}
        """

        response = model.generate_content(prompt)
        reply = response.text if hasattr(response, 'text') else "".join(part.text for part in response.parts)
        
        formatted_reply = format_response(reply)
        return jsonify({"reply": formatted_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    
