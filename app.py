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
- اختتم دائمًا بجملة تشجيعية مثل: 😊 هل ترغب بمثال آخر؟
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
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({'error': '⚠️ لا توجد رسالة', 'status': 'error'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': '⚠️ الرسالة فارغة', 'status': 'error'}), 400

        response = model.generate_content(
            user_message,
            generation_config=generation_config,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ],
        )

        reply = response.text.strip()
        return jsonify({'reply': reply, 'status': 'success'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'⚠️ حدث خطأ: {str(e)}', 'status': 'error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
