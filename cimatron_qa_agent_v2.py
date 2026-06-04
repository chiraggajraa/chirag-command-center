from groq import Groq
from datetime import datetime

# ── Colors ────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ── Your API Key ──────────────────────────────────────────────────────
client = Groq(api_key="GROQ_API_KEY", timeout=60.0)

# ── Agent Personality ─────────────────────────────────────────────────
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

# ── Chat History ──────────────────────────────────────────────────────
messages = [{"role": "system", "content": system_prompt}]
chat_log = []  # for saving to file

# ── Save Chat to File ─────────────────────────────────────────────────
def save_chat(summary):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"alex_session_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 55 + "\n")
        f.write("   Cimatron QA Expert — Alex | Chat Session\n")
        f.write(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 55 + "\n\n")
        for role, text in chat_log:
            label = "You" if role == "user" else "Alex"
            f.write(f"{label}: {text}\n\n")
        f.write("=" * 55 + "\n")
        f.write("SESSION SUMMARY\n")
        f.write("=" * 55 + "\n")
        f.write(summary + "\n")
    return filename

# ── Get Summary from Alex ─────────────────────────────────────────────
def get_summary():
    print(f"\n{YELLOW}Alex: Generating session summary...{RESET}")
    summary_prompt = messages + [{
        "role": "user",
        "content": (
            "Please summarize our conversation in bullet points covering: "
            "1) Topics discussed, 2) Key issues identified, "
            "3) Solutions or recommendations provided, "
            "4) Any follow-up actions suggested."
        )
    }]
    res = client.chat.completions.create(
        messages=summary_prompt,
        model="llama-3.3-70b-versatile",
    )
    return res.choices[0].message.content

# ── Header ────────────────────────────────────────────────────────────
print(f"\n{BOLD}{CYAN}{'=' * 55}{RESET}")
print(f"{BOLD}{CYAN}   🔧 Cimatron QA Expert Agent — Alex v2.0{RESET}")
print(f"{BOLD}{CYAN}   10 Years Experience | CAD/CAM | Cimatron{RESET}")
print(f"{BOLD}{CYAN}{'=' * 55}{RESET}")
print(f"{GRAY}   Press Ctrl+C anytime to exit & save session\n{RESET}")

# ── Alex Intro ────────────────────────────────────────────────────────
intro_messages = messages + [{"role": "user", "content": "Hello"}]
intro = client.chat.completions.create(
    messages=intro_messages,
    model="llama-3.3-70b-versatile",
)
agent_intro = intro.choices[0].message.content
print(f"{GREEN}{BOLD}Alex:{RESET} {GREEN}{agent_intro}{RESET}\n")
messages.append({"role": "user", "content": "Hello"})
messages.append({"role": "assistant", "content": agent_intro})
chat_log.append(("user", "Hello"))
chat_log.append(("assistant", agent_intro))

# ── Main Chat Loop ────────────────────────────────────────────────────
try:
    while True:
        user_input = input(f"{WHITE}{BOLD}You: {RESET}{WHITE}").strip()

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        chat_log.append(("user", user_input))

        print(f"{GRAY}Alex: thinking...{RESET}", end="\r")

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        chat_log.append(("assistant", reply))

        print(f"{GREEN}{BOLD}Alex:{RESET} {GREEN}{reply}{RESET}\n")

except KeyboardInterrupt:
    print(f"\n\n{YELLOW}{'=' * 55}{RESET}")
    print(f"{YELLOW}{BOLD}   📋 SESSION SUMMARY{RESET}")
    print(f"{YELLOW}{'=' * 55}{RESET}")

    summary = get_summary()
    print(f"{YELLOW}{summary}{RESET}")

    filename = save_chat(summary)
    print(f"\n{CYAN}{'=' * 55}{RESET}")
    print(f"{CYAN}💾 Chat saved to: {BOLD}{filename}{RESET}")
    print(f"{CYAN}{'=' * 55}{RESET}")
    print(f"\n{GREEN}{BOLD}Alex: Great session! Come back anytime. 👋{RESET}\n")
