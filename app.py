from flask import Flask, send_from_directory, request, jsonify
from insult_bot import generate_insult_response
import os
import json
import uuid
import time
from pathlib import Path

app = Flask(__name__)
chat_sessions = {}  # session_id -> list[{"role": "...", "content": "..."}]
SAVED_CONVERSATIONS_DIR = Path("saved_conversations")
SAVED_CONVERSATIONS_DIR.mkdir(exist_ok=True)

def get_client_id(data):
    sid = data.get('session_id')
    if sid:
        return sid
    ip = request.access_route[-1] if request.access_route else request.remote_addr
    return f"ip:{ip}"

def save_conversation(history, title="Untitled Rage Session"):
    conv_id = str(uuid.uuid4())[:8]
    timestamp = time.time()
    
    conv_data = {
        "id": conv_id,
        "title": title[:50],
        "history": history,
        "created": timestamp,
        "updated": timestamp
    }
    
    filepath = SAVED_CONVERSATIONS_DIR / f"{conv_id}.json"
    with open(filepath, 'w') as f:
        json.dump(conv_data, f, indent=2)
    
    return conv_id

def load_conversation(conv_id):
    filepath = SAVED_CONVERSATIONS_DIR / f"{conv_id}.json"
    if not filepath.exists():
        return None
    with open(filepath, 'r') as f:
        return json.load(f)

def list_conversations():
    convs = []
    for file in SAVED_CONVERSATIONS_DIR.glob("*.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                convs.append({
                    "id": data["id"],
                    "title": data["title"],
                    "created": data["created"],
                    "updated": data["updated"],
                    "message_count": len(data["history"])
                })
        except:
            continue
    return sorted(convs, key=lambda x: x["updated"], reverse=True)[:20]

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
    history = chat_sessions.setdefault(session_id, [])

    history.append({"role": "user", "content": user_msg})
    trimmed_history = history[-10:]

    try:
        bot_response = generate_insult_response(trimmed_history)
    except Exception as e:
        bot_response = f"Bot error: {str(e)}"

    history.append({"role": "assistant", "content": bot_response})

    return jsonify({
        'response': bot_response,
        'session_id': session_id,
    })

@app.route('/save_conversation', methods=['POST'])
def save_conversation_endpoint():
    data = request.get_json(force=True)
    session_id = data.get('session_id')
    title = data.get('title', 'Untitled Rage Session')
    
    if not session_id or session_id not in chat_sessions:
        return jsonify({'error': 'No conversation found'}), 400
    
    conv_id = save_conversation(chat_sessions[session_id].copy(), title)
    
    return jsonify({
        'conversation_id': conv_id,
        'share_url': f'/load/{conv_id}',
        'message': 'Conversation saved successfully!'
    })

@app.route('/load/<conv_id>')
def load_conversation_endpoint(conv_id):
    conv = load_conversation(conv_id)
    if not conv:
        return "Conversation not found", 404
    
    return jsonify(conv)

@app.route('/conversations')
def list_conversations_endpoint():
    return jsonify(list_conversations())

if __name__ == '__main__':
    print("Starting Flask insult bot on http://127.0.0.1:5000")
    print("Saved conversations will be stored in 'saved_conversations/' folder")
    app.run(debug=True)
