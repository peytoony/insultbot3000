from flask import Flask, send_from_directory, request, jsonify
from insult_bot import generate_insult_response
import os

app = Flask(__name__)
chat_sessions = {}

def get_client_id(data):
    # 1) Prefer explicit session_id from frontend (best)
    sid = data.get('session_id')
    if sid:
        return sid

    # 2) Fallback: use IP address as ID
    ip = request.access_route[-1] if request.access_route else request.remote_addr
    return f"ip:{ip}"

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)

    user_msg = data.get('message', '').strip()
    if not user_msg:
        return jsonify({'error': 'No message provided'}), 400
        
    session_id = get_client_id(data)

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # Append current user msg first
    chat_sessions[session_id].append({'user': user_msg, 'bot': ''})

    # Use last 4 exchanges for context (8 messages total)
    history_items = chat_sessions[session_id][-8:]
    history_str = "\n".join(
        f"User: {h['user']}\nBot: {h['bot']}"
        for h in history_items
    )

    try:
        bot_response = generate_insult_response(user_msg, history_str)
    except Exception as e:
        bot_response = f"Bot error: {str(e)}"

    chat_sessions[session_id][-1]['bot'] = bot_response

    return jsonify({
        'response': bot_response,
        'session_id': session_id,  # frontend can reuse this to be extra safe
    })

if __name__ == '__main__':
    print("Starting Flask insult bot on http://127.0.0.1:5000")
    app.run(debug=True)
