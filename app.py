from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Get your API key from environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.json

    prompt = f"""
    Create a professional resume for this person:
    Name: {data['name']}
    Address: {data['address']}
    Phone: {data['phone']}
    Email: {data['email']}
    Education: {data['education']}
    Work Experience: {data['experience']}
    Skills: {data['skills']}
    References: {data['references']}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    result = response.json()["choices"][0]["message"]["content"]
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
