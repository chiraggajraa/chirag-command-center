from flask import Flask, request
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), timeout=60.0)
conversation = []

@app.route("/", methods=["GET", "POST"])
def home():
    reply = ""
    user_msg = ""

    if request.method == "POST":
        user_msg = request.form.get("message", "")
        if user_msg:
            conversation.append({"role": "user", "content": user_msg})
            res = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Alex, a Cimatron QA Expert with 10 years experience. Be helpful and professional."}
                ] + conversation,
                model="llama-3.1-8b-instant"
            )
            reply = res.choices[0].message.content
            conversation.append({"role": "assistant", "content": reply})

    history_html = ""
    for msg in conversation:
        if msg["role"] == "user":
            history_html += f'<p><b style="color:#ff6b35">You:</b> {msg["content"]}</p>'
        else:
            history_html += f'<p><b style="color:#00d4ff">Alex:</b> {msg["content"]}</p><hr style="border-color:#1e3a5f">'

    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>Alex QA</title></head>
    <body style="background:#0a0e1a;color:#c8d8e8;font-family:sans-serif;padding:30px;max-width:800px;margin:auto">
      <h2 style="color:#00d4ff">🔧 Alex — Cimatron QA Expert</h2>
      <p style="color:#4a6080;margin-bottom:20px">Senior QA Engineer · 10 Years Experience</p>
      <div style="height:400px;overflow-y:auto;border:1px solid #1e3a5f;padding:15px;border-radius:10px;margin-bottom:20px">
        {history_html if history_html else '<p style="color:#4a6080">Ask Alex anything about Cimatron...</p>'}
      </div>
      <form method="POST">
        <input name="message" placeholder="Ask Alex about Cimatron QA..."
          style="width:75%;padding:12px;background:#071420;border:1px solid #1e3a5f;color:#fff;border-radius:8px;font-size:14px"
          autofocus autocomplete="off">
        <button type="submit"
          style="padding:12px 24px;background:#00d4ff;border:none;border-radius:8px;font-weight:bold;cursor:pointer;font-size:14px;margin-left:10px">
          Send ➤
        </button>
      </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("\n===============================")
    print("  Open: http://127.0.0.1:5000")
    print("  Stop: Ctrl+C")
    print("===============================\n")
    app.run(port=5000, debug=True)
