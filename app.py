from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)

# تحميل المفتاح من البيئة
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ يرجى إضافة GEMINI_API_KEY في متغيرات البيئة")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')  # أحدث نموذج

def format_response(text):
    """تحسين تنسيق الإجابة مع إضافة التنسيقات المطلوبة"""
    # إضافة التنسيق للكود
    text = re.sub(r'```python(.*?)```', 
                r'<pre class="code-box"><code>\1</code></pre><div class="code-comment">⚙️ الكود السابق يقوم بـ:</div>',
                text, flags=re.DOTALL)
    
    # جعل الكلمات المهمة غامقة
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # تحويل النقاط إلى قوائم منظمة
    text = re.sub(r'(\d+\.)', r'<br>\1', text)
    
    # إضافة إيموجي للعناوين
    text = text.replace("السؤال:", "❓ السؤال:")
    text = text.replace("الجواب:", "💡 الجواب:")
    text = text.replace("مثال:", "📌 مثال:")
    
    return text

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "الرسالة فارغة", "status": "error"}), 400

        # البرومبت المحسّن
        prompt = f"""
        أنت مساعد ذكي متعدد الاستخدامات للأطفال. التعليمات:
        
        🌟 المطلوب:
        1. الإجابات المنظمة:
           - استخدام النقاط المرقمة للشرح
           - وضع الكود في صندوق خاص مع شرح تحته
           - جعل الكلمات المهمة **غامقة**
        
        2. التنسيق:
           - استخدام إيموجي لطيف 🎯✨💡
           - الإجابات القصيرة (3-5 أسطر كحد أقصى)
           - العربية الفصحى فقط
        
        3. المحتوى:
           - فهم جميع الأسئلة (برمجة/علوم/ثقافة عامة)
           - شرح المفاهيم بطريقة بسيطة
           - أمثلة عملية عند الطلب
        
        🚫 الممنوعات:
           - اللهجات العامية
           - الإجابات الطويلة غير المنظمة
           - المعلومات غير الدقيقة
        
        أمثلة:
        - السؤال: "شو يعني بايثون؟"
          الجواب: "**بايثون** لغة برمجة سهلة 🐍✨
          📌 مميزاتها:
          1. تستخدم في الذكاء الاصطناعي 🤖
          2. كتابتها بسيطة وسهلة الفهم
          3. مثال: ```python\nprint('مرحباً')```"
        
        السؤال الحالي: "{user_message}"
        """

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.5,
                max_output_tokens=500,
                stop_sequences=["\n\n", "Note:"]
            )
        )

        # معالجة الإجابة
        reply = response.text
        
        # تطبيق التنسيقات الإضافية
        formatted_reply = format_response(reply)
        
        return jsonify({
            "reply": formatted_reply,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "حدث خطأ في المعالجة",
            "details": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
