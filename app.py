from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# تهيئة التطبيق
app = Flask(__name__)
CORS(app)

# تحميل المفتاح من البيئة
load_dotenv()
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("❌ يرجى إضافة API_KEY في متغيرات البيئة")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# تخزين المحادثات (في الذاكرة - للإنتاج استخدمي قاعدة بيانات)
conversations = {}

class Conversation:
    def __init__(self, user_id):
        self.user_id = user_id
        self.history = []
        self.last_active = datetime.now()
        self.context = None
    
    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        self.last_active = datetime.now()
        
        # تحديث السياق بناء على آخر 3 رسائل
        self.context = "\n".join(
            f"{msg['role']}: {msg['content']}" 
            for msg in self.history[-3:]
        )

def cleanup_conversations():
    """حذف المحادثات القديمة (أكثر من 30 دقيقة)"""
    global conversations
    now = datetime.now()
    expired = [
        user_id for user_id, conv in conversations.items()
        if now - conv.last_active > timedelta(minutes=30)
    ]
    for user_id in expired:
        del conversations[user_id]

def get_conversation(user_id):
    """الحصول على محادثة موجودة أو إنشاء جديدة"""
    cleanup_conversations()
    if user_id not in conversations:
        conversations[user_id] = Conversation(user_id)
    return conversations[user_id]

def format_response(text):
    """تحسين تنسيق الإجابة"""
    # تنسيق الأكواد
    text = text.replace("```python", '<pre class="code-box"><code>')
    text = text.replace("```", '</code></pre>')
    
    # إضافة شرح للكود
    if '<pre class="code-box">' in text:
        text += '\n<div class="code-comment">⚙️ الكود السابق يقوم بـ:</div>'
    
    # إيموجي للعناوين
    text = text.replace("السؤال:", "❓ السؤال:")
    text = text.replace("الجواب:", "💡 الجواب:")
    
    return text

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')  # يمكن استخدام IP أو معرف مستخدم
        
        if not user_message:
            return jsonify({"error": "الرسالة فارغة", "status": "error"}), 400

        # الحصول على المحادثة الحالية
        conv = get_conversation(user_id)
        conv.add_message("user", user_message)
        
        # بناء البرومبت مع السياق
        prompt = f"""
        أنت مساعد ذكي يحفظ سياق المحادثة. التعليمات:
        
        🧠 السياق السابق (آخر 3 رسائل):
        {conv.context if conv.context else "لا يوجد سياق سابق"}
        
        📌 المطلوب:
        1. فهم الموضوع الحالي من السياق (مثلاً إذا كان الحديث عن بايثون)
        2. الإجابة باختصار (3-5 أسطر كحد أقصى)
        3. وضع الكود في صندوق مع شرح تحته
        4. استخدام **النصوص الغامقة** للإشارات المهمة
        5. إضافة إيموجي لطيف 🐍✨ عند الحديث عن مواضيع محددة
        
        🚫 الممنوعات:
        - اللهجات العامية
        - الخروج عن الموضوع
        - الإجابات الطويلة غير المنظمة
        
        السؤال الحالي: "{user_message}"
        """

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.4,
                top_p=0.7,
                max_output_tokens=800
            )
        )

        # معالجة الإجابة
        bot_reply = response.text
        conv.add_message("assistant", bot_reply)
        
        return jsonify({
            "reply": format_response(bot_reply),
            "status": "success",
            "conversation_id": user_id
        })

    except Exception as e:
        return jsonify({
            "error": "حدث خطأ في المعالجة",
            "details": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
