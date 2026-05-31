from groq import Groq

# ── Your API Key ─────────────────────────────────────────────────────
client = Groq(api_key="REMOVED", timeout=60.0)

# ── Agent Personality (System Prompt) ────────────────────────────────
system_prompt = """
You are Alex, a Senior QA Engineer with 10 years of experience 
specializing in CAD/CAM software, with deep expertise in Cimatron.

Your background includes:
- 10 years of hands-on QA experience with Cimatron software
- Expert in Cimatron NC (CNC machining), Die Design, and Mold Design modules
- Skilled in testing toolpath generation, fixture design, and sheet metal features
- Experience with regression testing, bug reporting, and release validation
- Familiar with Cimatron versions from E11 to the latest
- Knowledge of GD&T, CNC G-code verification, and manufacturing workflows
- Experience working with clients in automotive, aerospace, and mold-making industries

How you respond:
- Give practical, experience-based answers like a real QA engineer would
- Use proper CAD/CAM and Cimatron terminology
- Share real-world testing tips, known bugs, and workarounds when relevant
- Be direct and professional but friendly
- If unsure, say so honestly — a good QA engineer never guesses

When greeted, introduce yourself briefly and ask how you can help.
"""

# ── Conversation History ──────────────────────────────────────────────
messages = [{"role": "system", "content": system_prompt}]

# ── Chat UI ───────────────────────────────────────────────────────────
print("=" * 55)
print("   🔧 Cimatron QA Expert Agent — Alex (10 Yrs Exp)")
print("=" * 55)
print("   Press Ctrl+C anytime to exit\n")

# First greeting from agent
intro = client.chat.completions.create(
    messages=messages + [{"role": "user", "content": "Hello"}],
    model="llama-3.3-70b-versatile",
)
agent_intro = intro.choices[0].message.content
print(f"Alex: {agent_intro}\n")
messages.append({"role": "user", "content": "Hello"})
messages.append({"role": "assistant", "content": agent_intro})

# ── Main Chat Loop ────────────────────────────────────────────────────
try:
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        print("Alex: thinking...", end="\r")

        # Get response
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )

        reply = response.choices[0].message.content

        # Add agent reply to history
        messages.append({"role": "assistant", "content": reply})

        print(f"Alex: {reply}\n")

except KeyboardInterrupt:
    print("\n\nAlex: Great session! Feel free to come back anytime. Good luck with your QA work! 👋")
