from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from google.generativeai import types

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCZSbfnXNS9KDqzUvktLMkHI4U-SEfcH5A"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "models/gemini-1.5-flash-latest",
    system_instruction="""
📚 أنت مساعد ذكي داخل موقع تعليمي مخصص للأطفال والطلاب 🎓✨.

✔️ التعليمات:
- أجب باللغة العربية الفصحى البسيطة والواضحة.
- اجعل الإجابة منظمة، مختصرة (3-6 أسطر) وواضحة.
- اجعل الكلمات المهمة **غامقة**.
- استخدم الإيموجي 🎯✨💡❓📌⚙️🚀❗ لجعل الإجابة ممتعة.
- إذا كان هناك كود، ضعه في صندوق كود مع شرح تحته.
- استخدم القوائم لتوضيح المميزات أو الخطوات.
- إذا ظهر مصطلح جديد، قدمه مع تعريف بسيط في البداية.
- اختتم دائمًا بجملة تشجيعية مثل: 😊 هل ترغب بمثال آخر؟

✔️ التعامل مع الحالات:
- إذا كان السؤال غير واضح: ❗ "لم أفهم سؤالك جيدًا، هل يمكنك توضيح أكثر؟ 😊"
- إذا كان السؤال خارج النطاق: ❗ "هذا السؤال خارج نطاق اختصاصي كمساعد تعليمي. هل ترغب بسؤال عن البرمجة أو موضوع تعليمي؟ 😊"

🎯 الهدف:
إجابات ممتعة، منظمة، قصيرة، واضحة، مليئة بالمعلومات المفيدة، مع تنسيقات جميلة باستخدام الإيموجي وصناديق الأكواد.
"""
)

generation_config = types.GenerationConfig(
    temperature=0.2,
    top_p=0.7,
    max_output_tokens=1000,
)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # استقبل قائمة الرسائل كاملة من الواجهة الأمامية
        messages = request.json.get('messages', [])

        if not messages:
            return jsonify({'error': '⚠️ لا توجد رسائل', 'status': 'error'}), 400

        # استخدم generate_chat_completion لإرسال المحادثة كاملة
        response = model.generate_chat_completion(
            messages=messages,
            generation_config=generation_config,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        )

        # استخرج رد المساعد
        reply = response.choices[0].message['content']

        return jsonify({'reply': reply, 'status': 'success'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'status': 'error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
