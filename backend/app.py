from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.regex_layer import check_pii

app = Flask(__name__)
CORS(app)  # Allow Chrome extension & external requests


@app.route("/")
def home():
    return "RiskWatch Backend Running 🚀"


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    score = 0

    # 🔴 Basic Threat Keyword Detection
    if "hate" in text.lower():
        score += 50

    if "attack" in text.lower():
        score += 50

    # 🟡 PII Detection (Regex Layer)
    score += check_pii(text)

    # 🟢 Final Status Decision
    status = "SAFE"
    if score >= 50:
        status = "CRITICAL"

    return jsonify({
        "analyzed_text": text,
        "score": score,
        "status": status
    })


if __name__ == "__main__":
    app.run(debug=True)
