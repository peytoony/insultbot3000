from flask import Flask, send_from_directory, request, jsonify
from insult_bot import generate_insult_response

import os

app = Flask(__name__)

# Serve index.html from the same directory as this app.py file
@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    user_msg = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    history_items = chat_sessions[session_id][-4:]
    history_str = "\n".join(
        f"User: {h['user']}\nBot: {h['bot']}"
        for h in history_items
    )

    bot_response = generate_insult_response(user_msg, history_str)

    chat_sessions[session_id].append({
        'user': user_msg,
        'bot': bot_response,
    })

    return jsonify({
        'response': bot_response,
        'session_id': session_id,
    })

chat_sessions = {}  # Move outside routes for global scope

if __name__ == '__main__':
    print("Starting Flask insult bot on http://127.0.0.1:5000")
    app.run(debug=True)
