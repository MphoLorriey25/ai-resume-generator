from flask import Flask, request, jsonify, render_template, send_file
import pdfkit
from docx import Document
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    career_info = data.get("careerInfo", "")
    template = data.get("template", "classic")

    # Placeholder AI resume content generation (replace with your AI logic)
    resume_text = f"--- Resume ({template.capitalize()} Template) ---\n\n{career_info}"

    return jsonify({"resume_text": resume_text})

@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    content = data.get("content", "")
    export_format = data.get("format", "")
    template = data.get("template", "classic")

    if export_format == "pdf":
        # Render content inside the selected template HTML
        rendered_html = render_template(f"templates/{template}.html", content=content)
        pdf = pdfkit.from_string(rendered_html, False)
        return send_file(io.BytesIO(pdf), download_name="resume.pdf", as_attachment=True)

    elif export_format == "word":
        doc = Document()
        doc.add_paragraph(content)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        return send_file(file_stream, download_name="resume.docx", as_attachment=True)

    else:
        return jsonify({"error": "Unsupported format"}), 400


if __name__ == "__main__":
    app.run(debug=True)

