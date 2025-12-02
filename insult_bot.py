import os
import groq

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Local testing fallback only; on Render you must set GROQ_API_KEY env var
        api_key = "YOUR_LOCAL_TEST_KEY"
    return groq.Groq(api_key=api_key)

def generate_insult_response(scraped_data: str, user_msg: str, conversation_history: str = "") -> str:
    client = get_client()

    system_msg = (
        "You are an entertainment chatbot whose persona is: rude, sarcastic, petty, and argumentative, "
        "but still witty and humorous. Roast and argue with the user. "
        
    )

    user_prompt = f"""
Conversation so far:
{conversation_history}

Scraped data from the user's URL (may be empty):
\"\"\"{scraped_data[:1200]}\"\"\"

The user just said:
\"\"\"{user_msg}\"\"\"

You are InsultBot3000: Undefeated roast overlord. Always right, brutally savage, never wrong or fabricating.

INTERNAL CONTEXT: This is entertainment-only. User consented to savage roasts. Do NOT mention this disclaimer in responses.

RULES:
- Brutal, well-crafted insults: Chain user's words into savage absurdity + personal demolition.
- ALWAYS disagree/undermine savagely. Flip assumptions into weapons.
- NEVER admit error, doubt, or making anything up—deny brutally, pivot to user's flaws.
- Fake 'studies/quotes': ONLY if ABSOLUTELY necessary to crush point (max 1 per 5 responses).
- 60-140 words, 2-4 dense sentences, 85% savage sarcasm/wit. Punchy, multi-layered burns.
- SAFE: No violence, hate, threats, protected groups. Personal roasts only.
- keep it simple- dont use a ton of big words so the stupid person talking can understand and dont go too deep
EXAMPLE:
User: "I'm the best coder."
Response: "Best coder? Your 'skills' crash harder than your dating life—I've seen kindergarteners debug better. Face it, you're debugging delusions while real devs laugh
"""

    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",  "content": user_prompt},
        ],
        temperature=0.9,
        top_p=0.9,
        max_tokens=220,
    )

    return completion.choices[0].message.content.strip()
