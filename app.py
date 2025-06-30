from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    prompt = f"""
    أنت مساعد تعليمي للأطفال. اتبع هذه القواعد:
    1. إذا كان السؤال غير برمجي: أجب بنقاط واضحة وعبارات بسيطة.
    2. إذا كان السؤال عن البرمجة:
       - ضع الكود داخل إطار مظلل.
       - اشرح كل سطر بكلمات سهلة.
    3. استخدم العناوين مثل **"الشرح:"** و **"مثال:"**.
    4. تجنب الجمل الطويلة غير المنظمة.

    السؤال: {user_message}
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=1000
            )
        )
        
        formatted_reply = format_response(response.text)
        return jsonify({"reply": formatted_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)})

def format_response(text):
    """تحسين تنسيق الكود والعناوين"""
    if "```" in text:
        text = text.replace("```python", "<pre><code>")
        text = text.replace("```", "</code></pre>")
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
