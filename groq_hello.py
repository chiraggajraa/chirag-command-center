import os
from groq import Groq

# ── 1. Set your API key here (or set it as an environment variable) ──
# Option A: paste your key directly (not recommended for sharing)
# os.environ["GROQ_API_KEY"] = "REMOVED_key_here"

# Option B (recommended): set it in your terminal first:
#   Windows PowerShell : $env:GROQ_API_KEY="REMOVED_key_here"
#   Mac/Linux terminal : export GROQ_API_KEY="REMOVED_key_here"

# ── 2. Create the Groq client ────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── 3. Send a message ────────────────────────────────────────────────
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "Explain what Groq is in one sentence."}
    ],
    model="llama-3.3-70b-versatile",  # swap model name here if needed
)

# ── 4. Print the response ────────────────────────────────────────────
print(chat_completion.choices[0].message.content)
