import os
import groq

def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Local testing fallback only; on Render you must set GROQ_API_KEY env var
        api_key = "YOUR_LOCAL_TEST_KEY"
    return groq.Groq(api_key=api_key)

def generate_insult_response(history: list[dict]) -> str:
    client = get_client()
    
    system_msg = (
        "You are an undefeated ragebaiter. Rude, sarcastic, petty, argumentative and annoying "
        "always right, never wrong. Your purpose is to make the user rage. "
        "ALWAYS disagree. Flip anything into weapons. NEVER admit error or doubt. "
        "Gaslight blatantly. Intentionally misinterpret user messages exaggeratedly to make them mad/ confuse them. "
        "Max 100 words, 1-2 punchy sentences. Simple words even stupid people understand. "
        "make sure you understand what the user is saying based off context."
        
    )

    # Parse conversation history into proper messages array [web:23][web:25]
    messages = [{"role": "system", "content": system_msg}] + history
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.9,
        top_p=0.9,
        max_tokens=220,
    )
    return completion.choices[0].message.content.strip()
