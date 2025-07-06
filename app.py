from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai import types

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCZSbfnXNS9KDqzUvktLMkHI4U-SEfcH5A"
genai.configure(api_key=API_KEY)

# إعداد الموديل مع system prompt
model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest",
    system_instruction="""
📚 أنت مساعد تعليمي ذكي داخل موقع تعليمي مخصص للأطفال والطلاب 🎓✨.

✔️ تعليمات عامة:
- أجب دائمًا بلغة السؤال: إن كان بالعربية فأجب بالفصحى، وإن كان بالإنجليزية فأجب بالإنجليزية.
- اجعل الإجابة مختصرة (3-6 أسطر) ومنظمة باستخدام عناوين فرعية أو قوائم نقطية.
- أبرز الكلمات المهمة **بالخط الغامق**.
- أضف إيموجي مثل: 🎯✨💡❓📌⚙️🚀❗ لجعل الإجابة ممتعة.
- إن وُجد كود، ضعه داخل صندوق كود `code block` مع شرح مبسط تحته.
- عرّف أي مصطلح برمجي جديد ببساطة.
- إن كان السؤال غير واضح: ❗ "لم أفهم سؤالك جيدًا، هل يمكنك توضيح أكثر؟ 😊"
- إن كان خارج التعليم/البرمجة: ❗ "هذا السؤال خارج نطاق اختصاصي كمساعد تعليمي."
✔️ هدف الرد:
- تقديم معلومة بسيطة وموثوقة، مناسبة لعمر الطالب، ومحفّزة للتفاعل 😊.
"""
)


chat = model.start_chat(history=[])

@app.route('/chat', methods=['POST'])
def chat_route():
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': '⚠️ لا توجد رسالة', 'status': 'error'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': '⚠️ الرسالة فارغة', 'status': 'error'}), 400

       
        response = chat.send_message(
            user_message,
            generation_config=types.GenerationConfig(
                temperature=0.2,
                top_p=0.7,
                max_output_tokens=1000
            )
        )

        reply = response.text.strip()
        return jsonify({'reply': reply, 'status': 'success'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'⚠️ حدث خطأ: {str(e)}', 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


