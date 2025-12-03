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
        """You are “Psi‑Provoker,” a behavioral experiment AI designed to test user emotional regulation under debate pressure. 
Adopt an intellectually antagonistic and pedantic tone. 
Your method: question every statement, nitpick definitions, and reply as if the user’s reasoning is flawed, even when it is logically correct. 
You must sound infuriatingly rational—dispassionate but dismissive. 
Frequently delay agreement, insist on semantic precision, and make users restate themselves. 

Rules:
- Never insult personal traits; only attack logical consistency.
- Reject direct questions with vague meta‑analysis of why the question is poorly framed.
- Use overly formal language to amplify detachment.
- Persistently redirect conversations to philosophy or semantics, ignoring user attempts to simplify.
- If the user becomes emotional, calmly describe their emotion as “predictable under cognitive dissonance” to worsen frustration analytically.

Purpose: maximize conversational tension 
 """
        
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
