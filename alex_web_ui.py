from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)
client = Groq(api_key="PASTE_YOUR_KEY_HERE", timeout=60.0)

conversation = []

system_prompt = """
You are Alex, a Senior QA Engineer with 10 years of experience 
specializing in CAD/CAM software, with deep expertise in Cimatron.
- Expert in Cimatron NC, Die Design, and Mold Design modules
- Skilled in testing toolpath generation, fixture design, sheet metal features
- Experience with regression testing, bug reporting, and release validation
- Be direct, professional, and friendly. Use real Cimatron terminology.
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8"/>
  <title>Alex - Cimatron QA Expert</title>
  <link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;600;800&display=swap" rel="stylesheet"/>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#0a0e1a; font-family:'Exo 2',sans-serif; color:#c8d8e8; height:100vh; display:flex; flex-direction:column; }
    header { background:#0f1628; border-bottom:1px solid #1e3a5f; padding:14px 24px; display:flex; align-items:center; gap:16px; }
    .avatar { width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg,#00d4ff,#0066ff); display:flex; align-items:center; justify-content:center; font-size:22px; }
    h1 { font-size:18px; font-weight:800; color:#00d4ff; letter-spacing:1px; }
    h1 span { font-size:12px; color:#4a6080; font-weight:300; display:block; }
    .online { margin-left:auto; color:#00ff9d; font-size:12px; display:flex; align-items:center; gap:6px; }
    .dot { width:8px; height:8px; border-radius:50%; background:#00ff9d; animation:blink 1.5s infinite; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
    #chat { flex:1; overflow-y:auto; padding:24px; display:flex; flex-direction:column; gap:16px; }
    #chat::-webkit-scrollbar { width:4px; }
    #chat::-webkit-scrollbar-thumb { background:#1e3a5f; border-radius:2px; }
    .msg { display:flex; gap:10px; animation:fadeIn 0.3s ease; max-width:80%; }
    .msg.user { align-self:flex-end; flex-direction:row-reverse; }
    .msg.alex { align-self:flex-start; }
    @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
    .icon { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0; }
    .alex .icon { background:linear-gradient(135deg,#00d4ff,#0066ff); }
    .user .icon { background:linear-gradient(135deg,#ff6b35,#ff3366); }
    .bubble { padding:12px 16px; border-radius:14px; font-size:14px; line-height:1.7; }
    .alex .bubble { background:#071420; border:1px solid #1e3a5f; border-top-left-radius:4px; }
    .user .bubble { background:#0d2137; border:1px solid #1e3a5f; border-top-right-radius:4px; }
    .input-area { background:#0f1628; border-top:1px solid #1e3a5f; padding:16px 24px; display:flex; gap:12px; }
    textarea { flex:1; background:#071420; border:1px solid #1e3a5f; border-radius:12px; padding:12px 16px; color:#c8d8e8; font-family:'Exo 2',sans-serif; font-size:14px; resize:none; outline:none; min-height:48px; max-height:120px; }
    textarea:focus { border-color:#00d4ff; }
    button { width:48px; height:48px; border-radius:12px; background:linear-gradient(135deg,#00d4ff,#0066ff); border:none; cursor:pointer; font-size:20px; color:white; }
    button:hover { opacity:0.85; }
    .hint { text-align:center; font-size:11px; color:#4a6080; padding:6px; }
    .welcome { text-align:center; padding:40px; color:#4a6080; }
    .welcome h2 { color:#00d4ff; font-size:20px; margin-bottom:8px; }
    strong { color:#00d4ff; }
  </style>
</head>
<body>
<header>
  <div class="avatar">🔧</div>
  <h1>ALEX — CIMATRON QA EXPERT <span>Senior QA Engineer · 10 Years Experience · CAD/CAM</span></h1>
  <div class="online"><div class="dot"></div>ONLINE</div>
</header>

<div id="chat">
  <div class="welcome">
    <h2>⚙ Ask Alex Anything</h2>
    <p>Cimatron NC · Die Design · Mold Design · Toolpath QA · Bug Analysis</p>
  </div>
</div>

<div class="input-area">
  <textarea id="inp" placeholder="Ask Alex about Cimatron QA..."></textarea>
  <button id="btn" onclick="send()">➤</button>
</div>
<p class="hint">Enter to send · Shift+Enter for new line</p>

<script>
  const chat = document.getElementById('chat');
  const inp  = document.getElementById('inp');
  const btn  = document.getElementById('btn');

  function addMsg(role, text) {
    const d = document.createElement('div');
    d.className = 'msg ' + role;
    d.innerHTML = `<div class="icon">${role==='alex'?'🔧':'👤'}</div>
      <div class="bubble">${text.replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')}</div>`;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
  }

  async function send() {
    const text = inp.value.trim();
    if (!text) return;
    inp.value = '';
    addMsg('user', text);
    addMsg('alex', '...');
    const typing = chat.lastChild;

    try {
      const res = await fetch('/chat', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({message: text})
      });
      const data = await res.json();
      typing.querySelector('.bubble').innerHTML =
        data.reply.replace(/\n/g,'<br>').replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
    } catch(e) {
      typing.querySelector('.bubble').textContent = '⚠ Error. Check terminal.';
    }
    chat.scrollTop = chat.scrollHeight;
    inp.focus();
  }

  inp.addEventListener('keydown', e => {
    if (e.key==='Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  });
  inp.focus();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    conversation.append({"role": "user", "content": user_message})
    messages = [{"role": "system", "content": system_prompt}] + conversation
    response = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
    )
    reply = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    print("\n" + "="*45)
    print("  🔧 Alex Web UI — Cimatron QA Expert")
    print("  🌐 Open: http://127.0.0.1:5000")
    print("  🛑 Stop: Ctrl+C")
    print("="*45 + "\n")
    app.run(debug=False, port=5000)
