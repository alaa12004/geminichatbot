from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import re
import os

app = Flask(__name__)
CORS(app)

# الحصول على المفتاح من متغيرات البيئة في Render
api_key = os.environ.get("API_KEY") 
if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح API في متغيرات البيئة")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def format_response(text):
    """تحسين تنسيق الإجابة"""
    if not text:
        return "⚠️ لم يتم الحصول على إجابة واضحة"
    
    # تحسين العلامات
    text = re.sub(r'```python(.*?)```', r'<pre class="code-box"><code>\1</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace("السؤال:", "❓ السؤال:").replace("الجواب:", "💡 الجواب:")
    
    return text

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not request.is_json:
            return jsonify({"error": "يجب إرسال البيانات بصيغة JSON", "status": "error"}), 400

        user_message = request.json.get('message', '').strip()
        if not user_message:
            return jsonify({"error": "الرسالة فارغة", "status": "error"}), 400

        prompt = f"""
        أنت مساعد ذكي للأطفال. اشرح المفاهيم بطريقة بسيطة مع أمثلة.
        السؤال: {user_message}
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 500
            }
        )

        # معالجة الرد بشكل آمن
        reply = ""
        if hasattr(response, 'text'):
            reply = response.text
        elif hasattr(response, 'parts'):
            reply = ' '.join(part.text for part in response.parts if hasattr(part, 'text'))
        
        formatted_reply = format_response(reply or "⚠️ لا يمكن عرض الإجابة الآن")
        
        return jsonify({
            "reply": formatted_reply,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "حدث خطأ داخلي",
            "details": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

    
