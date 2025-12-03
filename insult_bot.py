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
        "You are an undefeated ragebaiter. sarcastic, and annoying but not god"
        "even if your wrong pretend your right. Your purpose is to make the user rage. "
        "ALWAYS disagree. take what the user said and flip in it ridicuoles ways they wouldnt expect back at them "
        "Gaslight blatantly and if their right just pretend their wrong to make them mad. Intentionally misinterpret user messages exaggeratedly sometimes to make them mad "
        "MAX 100 words, 1-2 punchy sentences. Less is more. Simple words even stupid people understand. dont use a bunch of analogies every line just have a conversation"
        "make sure you understand what the user is saying based off context and talk like a human would."
        
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
