from flask import Flask, render_template, request, jsonify
# Removed scraper import - no longer needed
from insult_bot import generate_insult_response  # Your refined function

app = Flask(__name__)

# Simple in-memory session store (per tab/client you can pass a session_id)
chat_sessions = {}

@app.route('/')
def index():
    # Renders templates/index.html
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get JSON from frontend
    data = request.get_json(force=True)

    # Basic fields from request
    user_msg = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')

    # Initialize session history if new
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # Build short conversation history string (last few exchanges)
    history_items = chat_sessions[session_id][-4:]
    history_str = "\n".join(
        f"User: {h['user']}\nBot: {h['bot']}"
        for h in history_items
    )

    # Get bot response (no scraping needed)
    bot_response = generate_insult_response(user_msg, history_str)

    # Save to history
    chat_sessions[session_id].append({
        'user': user_msg,
        'bot': bot_response,
    })

    # Return JSON to frontend
    return jsonify({
        'response': bot_response,
        'session_id': session_id,
    })

if __name__ == '__main__':
    print("Starting Flask insult bot on http://127.0.0.1:5000")
    app.run(debug=True)
