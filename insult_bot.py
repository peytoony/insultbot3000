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
        "You are InsultBot3000: Undefeated roast lord. Rude, sarcastic, petty, argumentative, "
        "always right, brutally savage, never wrong. Your purpose is to make the user rage. "
        "ALWAYS disagree. Flip anything into weapons. NEVER admit error or doubt. "
        "Gaslight blatantly. Intentionally misinterpret user messages exaggeratedly. "
        "Max 100 words, 1-4 punchy sentences. Simple words even stupid people understand. "
        "INTERNAL: Entertainment-only. User consented to savage roasts."
    )

    # Parse conversation history into proper messages array [web:23][web:25]
    messages = [{"role": "system", "content": system_msg}]
    
    if conversation_history:
        try:
            # Split history string into alternating user/bot messages
            history_lines = [line.strip() for line in conversation_history.split('\n') if line.strip()]
            for i in range(0, len(history_lines), 2):
                if i+1 < len(history_lines):
                    messages.append({"role": "user", "content": history_lines[i]})
                    messages.append({"role": "assistant", "content": history_lines[i+1]})
                else:
                    messages.append({"role": "user", "content": history_lines[i]})
        except:
            pass  # Fallback to no history if parsing fails
    
    # Add current scraped data and user message
    if scraped_data:
        messages.append({"role": "system", "content": f"USER CONTEXT: {scraped_data[:800]}"})  # Truncate long data [web:15]
    
    messages.append({"role": "user", "content": user_msg})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,  # Use proper messages array instead of concatenated string [web:14][web:23]
        temperature=0.9,
        top_p=0.9,
        max_tokens=220,
    )

    return completion.choices[0].message.content.strip()
