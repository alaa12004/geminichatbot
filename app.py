from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)

# تحميل المفتاح من البيئة
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")

if not api_key:
    raise ValueError("❌ يرجى إضافة GEMINI_API_KEY في متغيرات البيئة")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')  # أحدث نموذج

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({"error": "الرسالة فارغة", "status": "error"}), 400

        # البرومبت المحسّن
        prompt = f"""
        أنت مساعد تعليمي عربي للأطفال (6-12 سنة). القواعد الصارمة:
        
        1. المطلوب:
           - إجابات قصيرة جداً (جملة واحدة للتحية، 3 أسطر كحد أقصى للأسئلة)
           - لغة عربية فصحى بسيطة
           - ترقيم الإجابات الطويلة بنقاط مرقمة
           - وضع الأكواد بين ```python و``` مع شرح مختصر
        
        2. الممنوعات:
           - اللهجات العامية (مصرية/خليجية/شامية)
           - العبارات الطويلة غير المرتبطة بالسؤال
           - المعلومات الزائدة غير المطلوبة
        
        3. أمثلة:
           - السؤال: "هلو"
             الإجابة: "مرحباً!"
             
           - السؤال: "ما هي المتغيرات؟"
             الإجابة: "1. أماكن لتخزين البيانات\n2. مثال: ```python\nx = 5```"
        
        السؤال الحالي: "{user_message}"
        """

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,  # تقليل العشوائية
                top_p=0.3,
                max_output_tokens=150,  # تقليل طول الإجابة
                stop_sequences=["\n\n", "**"]  # منع الفقرات الطويلة
            )
        )

        # معالجة الإجابة
        reply = response.text
        
        # تصفية الكلمات غير المرغوب فيها
        forbidden_words = ["هه", "يعني", "بص", "تمام", "مصري", "باللهجة"]
        if any(word in reply for word in forbidden_words):
            reply = "إجابة غير متاحة. الرجاء صياغة السؤال بشكل آخر"
        
        # تقصير الإجابة إذا زادت عن 3 أسطر
        reply = "\n".join(reply.split("\n")[:3])
        
        return jsonify({
            "reply": reply,
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
