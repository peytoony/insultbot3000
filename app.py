from flask import Flask, send_from_directory, request, jsonify
from insult_bot import generate_insult_response
import os

app = Flask(__name__)
chat_sessions = {}  # session_id -> list[{"role": "...", "content": "..."}]

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

    # Get or init history for this session
    history = chat_sessions.setdefault(session_id, [])

    # Append current user message
    history.append({"role": "user", "content": user_msg})

    # Only keep the last 10 turns to control token usage
    trimmed_history = history[-10:]

    try:
        # Pass only the history (no system here; insult_bot adds system message)
        bot_response = generate_insult_response(trimmed_history)
    except Exception as e:
        bot_response = f"Bot error: {str(e)}"

    # Append assistant reply to full history
    history.append({"role": "assistant", "content": bot_response})

    return jsonify({
        'response': bot_response,
        'session_id': session_id,
    })

if __name__ == '__main__':
    print("Starting Flask insult bot on http://127.0.0.1:5000")
    app.run(debug=True)
