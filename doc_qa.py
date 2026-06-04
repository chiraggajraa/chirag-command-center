from flask import Flask, request, jsonify
from groq import Groq
import PyPDF2
import urllib.request
import re
import traceback

app = Flask(__name__)
client = Groq(api_key="", timeout=60.0)

doc_text = ""
conversation = []

def extract_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    print(f"PDF extracted: {len(text)} chars total")
    return text

def extract_url(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", errors="ignore")
    text = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)
    text = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def get_relevant_chunk(full_text, question, chunk_size=5000):
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    if not chunks:
        return full_text[:chunk_size]
    keywords = question.lower().split()
    best_chunk = chunks[0]
    best_score = 0
    for i, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = sum(chunk_lower.count(kw) for kw in keywords)
        if score > best_score:
            best_score = score
            best_chunk = chunk
            print(f"Best chunk: #{i} with score {score}")
    return best_chunk

@app.route("/")
def home():
    return open("doc_qa.html", encoding="utf-8").read()

@app.route("/upload", methods=["POST"])
def upload():
    global doc_text, conversation
    conversation = []
    try:
        if "pdf" in request.files:
            file = request.files["pdf"]
            doc_text = extract_pdf(file)
            preview = doc_text[:300].replace("\n", " ")
            return jsonify({"success": True, "source": "pdf", "preview": preview, "chars": len(doc_text)})
        if request.is_json:
            url = request.json.get("url", "")
            if url:
                doc_text = extract_url(url)
                preview = doc_text[:300].replace("\n", " ")
                return jsonify({"success": True, "source": "url", "preview": preview, "chars": len(doc_text)})
    except Exception as e:
        print("UPLOAD ERROR:", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)})
    return jsonify({"success": False, "error": "No file or URL provided"})

@app.route("/ask", methods=["POST"])
def ask():
    global conversation
    try:
        question = request.json.get("question", "")
        if not doc_text:
            return jsonify({"answer": "Please upload a PDF or load a URL first."})

        relevant_chunk = get_relevant_chunk(doc_text, question, chunk_size=5000)
        recent_history = conversation[-2:] if len(conversation) > 2 else conversation

        messages = [
            {
                "role": "system",
                "content": f"""You are Alex, a Senior QA Engineer with 10 years of Cimatron CAD/CAM experience.
Answer based on the document section below. Reference page numbers when available.

DOCUMENT SECTION:
{relevant_chunk}"""
            }
        ] + recent_history + [{"role": "user", "content": question}]

        print(f"Sending ~{sum(len(m['content']) for m in messages)} chars to Groq")

        res = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            max_tokens=800
        )
        answer = res.choices[0].message.content
        conversation.append({"role": "user", "content": question})
        conversation.append({"role": "assistant", "content": answer})
        return jsonify({"answer": answer})

    except Exception as e:
        print("ASK ERROR:", traceback.format_exc())
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    print("\n" + "="*45)
    print("  📄 Alex — Document Q&A (PDF + Web URL)")
    print("  🌐 Open: http://127.0.0.1:5001")
    print("  🛑 Stop: Ctrl+C")
    print("="*45 + "\n")
    app.run(port=5001, debug=True)
