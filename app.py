from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from docx import Document
from fpdf import FPDF

app = Flask(__name__)
generated_resume = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_resume():
    global generated_resume
    data = request.json

    prompt = f"""
    Create a {data['template']} style resume:
    Name: {data['name']}
    Address: {data['address']}
    Phone: {data['phone']}
    Email: {data['email']}
    Summary: {data['summary']}
    Education: {data['education']}
    Work Experience: {data['experience']}
    Skills: {data['skills']}
    References: {data['references']}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    generated_resume = response.json()["choices"][0]["message"]["content"]
    return jsonify({"output": generated_resume})

@app.route("/download/pdf")
def download_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True)
    pdf.set_font("Arial", size=12)
    for line in generated_resume.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output("resume.pdf")
    return send_file("resume.pdf", as_attachment=True)

@app.route("/download/docx")
def download_docx():
    doc = Document()
    for line in generated_resume.split('\n'):
        doc.add_paragraph(line)
    doc.save("resume.docx")
    return send_file("resume.docx", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
