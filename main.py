from flask import Flask, request, render_template_string
import datetime

app = Flask(__name__)

# Simple in-memory storage (Resets if server restarts)
# For permanent storage, you'd need a real database file (SQLite).
database = []

# HTML Template (Clean Dark GUI)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Booth Database</title>
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
        h1 { color: #ffffff; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .card { background-color: #1e1e1e; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #00d26a; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .card.alert { border-left: 5px solid #ff4444; background-color: #2a1a1a; } /* Highlight Lytherion */
        .info { flex-grow: 1; }
        .sign-text { font-size: 1.2em; font-weight: bold; color: #fff; margin-bottom: 5px; display: block; }
        .meta { font-size: 0.9em; color: #888; }
        a { color: #4dabf7; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .timestamp { font-family: monospace; color: #555; }
    </style>
    <meta http-equiv="refresh" content="5"> <!-- Auto refresh every 5s -->
</head>
<body>
    <h1>Live Booth Database</h1>
    <div id="container">
        {% for entry in entries %}
        <div class="card {% if 'lytherion' in entry.sign_text.lower() %}alert{% endif %}">
            <div class="info">
                <span class="sign-text">"{{ entry.sign_text }}"</span>
                <div class="meta">
                    User: <a href="{{ entry.user_link }}" target="_blank">{{ entry.username }}</a> | 
                    Decal: <a href="{{ entry.decal_link }}" target="_blank">{{ entry.decal_id }}</a>
                </div>
            </div>
            <div class="timestamp">{{ entry.timestamp }}</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Show newest first
    return render_template_string(HTML_TEMPLATE, entries=reversed(database))

@app.route('/api/log', methods=['POST'])
def log_booth():
    data = request.json
    if data:
        # Save to database list
        database.append(data)
        # Keep list form getting too big (optional, keep last 100)
        if len(database) > 100:
            database.pop(0)
    return {"status": "success"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
