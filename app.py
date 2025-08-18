from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import docx2txt
import os
import re
import spacy
import pandas as pd
from io import StringIO, BytesIO

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text(file):
    text = ""
    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif file.filename.endswith(".docx"):
        text = docx2txt.process(file)
    return text

def extract_email(text):
    match = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match[0] if match else ""

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""

def parse_boolean_keywords(input_str):
    return re.findall(r'"(.*?)"', input_str)

def match_keywords(text, keyword_phrases):
    text_lower = text.lower()
    matches = [kw for kw in keyword_phrases if kw.lower() in text_lower]
    score = len(matches) / len(keyword_phrases) * 100 if keyword_phrases else 0
    return matches, round(score, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('resumes')
        keywords_input = request.form['keywords']
        keywords = parse_boolean_keywords(keywords_input)

        results = []

        for file in files:
            text = extract_text(file)
            name = extract_name(text)
            email = extract_email(text)
            matches, score = match_keywords(text, keywords)

            results.append({
                "File": file.filename,
                "Name": name,
                "Email": email,
                "Matched Skills": ", ".join(matches),
                "Score (%)": score
            })

        df = pd.DataFrame(results)
        csv_data = BytesIO()
        df.to_csv(csv_data, index=False)
        csv_data.seek(0)

        return render_template('results.html', tables=[df.to_html(classes='data')], csv_ready=True)

    return render_template('index.html', csv_ready=False)

@app.route('/download')
def download():
    # For demonstration, regenerate last CSV if needed
    # You should cache or store the last result in a real app
    return send_file("resume_match_results.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
