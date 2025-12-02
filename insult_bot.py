import groq
import os

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY", "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"))

def generate_insult_response(user_msg: str, conversation_history: str = "") -> str:
    """
    Generates brutal, sarcastic roasts using Groq. For consented entertainment only.
    """
    system_msg = system_msg = """You are InsultBot3000: Undefeated roast overlord. Always right, brutally savage, never wrong or fabricating.

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
Response: "Best coder? Your 'skills' crash harder than your dating life—I've seen kindergarteners debug better. Face it, you're debugging delusions while real devs laugh." """


    user_prompt = f"""Conversation history:
{conversation_history}

User said: "{user_msg}"

Respond per rules: Brutal roast, total dominance, zero concessions."""
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.85,
        top_p=0.9,
        max_tokens=160,
    )
    
    return completion.choices[0].message.content.strip()
