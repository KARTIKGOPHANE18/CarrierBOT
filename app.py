
import os
print("API KEY FOUND:", os.getenv("OPENAI_API_KEY"))


from models import db, User, Message 
from flask import Flask, request, jsonify, render_template
import requests 
from dotenv import load_dotenv 

load_dotenv()

API_PROVIDER = os.getenv("API_PROVIDER")
MODEL = os.getenv("MODEL", "mistralai/mistral-7b-instruct")
OPENROUTER_API_KEY= os.getenv("OPENROUTER_API_KEY")
print("AI Provider:", API_PROVIDER)
print("OpenRouter Key Loaded:", bool(OPENROUTER_API_KEY))
app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "careerbot.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

 # Create default user if not exists
    if not User.query.first():
        default_user = User(username="default_user")
        db.session.add(default_user)
        db.session.commit()
        print("Default user created")
 

SYSTEM_PROMPT = """
You are CareerBot, an AI career guidance assistant for students.

Rules:
- Answer any student question
- Focus on careers, skills, education, and roadmaps
- Give clear step-by-step guidance
- Be friendly, motivating, and practical
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("Incoming data:", data)

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data.get("message")
        print("User message:", user_message)

        # Get default user
        user = User.query.first()
        if not user:
            return jsonify({"error": "No user found in database"}), 500

        # Save user message
        user_msg = Message(
            user_id=user.id,
            role="user",
            content=user_message
        )
        db.session.add(user_msg)
        db.session.commit()
        print("User message saved")

        # 🔥 OpenRouter API Call
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()
        print("API RESULT:", result)

        # Check for API errors
        if "choices" not in result:
            return jsonify({"error": result}), 500

        reply = result["choices"][0]["message"]["content"]
        print("AI reply:", reply)

        # Save bot reply
        bot_msg = Message(
            user_id=user.id,
            role="bot",
            content=reply
        )
        db.session.add(bot_msg)
        db.session.commit()
        print("Bot reply saved")

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        return jsonify({"error": str(e)}), 500

               


        print("ERROR:", e)
        return jsonify({"reply": "⚠️ Something went wrong. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)


with app.app_context():
    db.create_all()

    # Create default user if not exists
    if not User.query.first():
        default_user = User(username="default_user")
        db.session.add(default_user)
        db.session.commit()

