import PyPDF2
import docx
import re
import spacy
import json
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

nlp = spacy.load("en_core_web_sm")

resume_file = "navyagowthami_resume.pdf"
job_file = "jobDesc.pdf"

def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass

    if text.strip() == "":
        print("Using OCR for scanned PDF...")
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    elif file_path.lower().endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""


resume_text = extract_text(resume_file)
job_text = extract_text(job_file)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)

    doc = nlp(text)

    tokens = []
    for token in doc:
        if token.is_alpha and not token.is_stop:
            tokens.append(token.lemma_)

    return tokens


resume_tokens = preprocess_text(resume_text)
job_tokens = preprocess_text(job_text)

skill_database = {
    "technical": [
        "python","java","c","c++","sql","machine learning",
        "deep learning","data science","pandas","numpy",
        "tensorflow","django","flask","aws","docker",
        "kubernetes","cloud computing","react","angular",
        "html","css","javascript"
    ],
    "soft": [
        "communication","teamwork","leadership",
        "problem solving","time management","adaptability"
    ],
    "domain": [
        "data analysis","computer vision",
        "cybersecurity","devops","project management",
        "business analysis","cloud security"
    ]
}

all_skills = []
for category in skill_database:
    all_skills.extend(skill_database[category])

skill_weights = {
    "python": 2,
    "machine learning": 2,
    "aws": 2
}

def extract_skills(tokens, original_text):
    found = set()
    original_text = original_text.lower()

    for skill in all_skills:
        if " " in skill:
            if skill in original_text:
                found.add(skill)
        else:
            if skill in tokens:
                found.add(skill)

    return found


resume_skills = extract_skills(resume_tokens, resume_text)
job_skills = extract_skills(job_tokens, job_text)

matching_skills = resume_skills.intersection(job_skills)
missing_skills = job_skills - resume_skills

total_weight = 0
matched_weight = 0

for skill in job_skills:
    weight = skill_weights.get(skill, 1)
    total_weight += weight
    if skill in matching_skills:
        matched_weight += weight

if total_weight > 0:
    match_percentage = (matched_weight / total_weight) * 100
else:
    match_percentage = 0

result = {
    "resume_skills": sorted(list(resume_skills)),
    "job_skills": sorted(list(job_skills)),
    "matching_skills": sorted(list(matching_skills)),
    "missing_skills": sorted(list(missing_skills)),
    "match_percentage": round(match_percentage, 2)
}

with open("milestone2_result.json", "w") as f:
    json.dump(result, f, indent=4)

print("\n===== COMPLETE MILESTONE 2 OUTPUT =====\n")
print(json.dumps(result, indent=4))