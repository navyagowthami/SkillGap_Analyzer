import streamlit as st
import PyPDF2
import docx
import re
import spacy
import json

nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="SkillGapAI - Milestone 2", layout="wide")

st.title("SkillGapAI - Intelligent Skill Gap Analyzer")
st.write("Milestone 2 - NLP Based Skill Extraction & Matching")

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfReader(uploaded_file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        return ""

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    doc = nlp(text)

    tokens = []
    for token in doc:
        if token.is_alpha and not token.is_stop:
            tokens.append(token.lemma_)
    return tokens

skill_database = {
    "technical": [
        "python","java","sql","machine learning","deep learning",
        "data science","pandas","numpy","tensorflow","django",
        "flask","aws","docker","kubernetes","react","html","css"
    ],
    "soft": [
        "communication","teamwork","leadership",
        "problem solving","time management"
    ],
    "domain": [
        "data analysis","cybersecurity","devops",
        "project management","cloud security"
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
 
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

with col2:
    job_file = st.file_uploader("Upload Job Description", type=["pdf", "docx"])

if resume_file and job_file:

    resume_text = extract_text(resume_file)
    job_text = extract_text(job_file)

    resume_tokens = preprocess_text(resume_text)
    job_tokens = preprocess_text(job_text)

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

    match_percentage = (matched_weight / total_weight) * 100 if total_weight > 0 else 0

    st.divider()

    st.subheader("Skills Available (Resume)")
    st.write(sorted(list(resume_skills)))

    st.subheader("Skills Required (Job Description)")
    st.write(sorted(list(job_skills)))

    st.subheader("Matching Skills")
    st.success(sorted(list(matching_skills)))

    st.subheader("Missing Skills")
    st.error(sorted(list(missing_skills)))

    st.subheader("Match Percentage")
    st.metric(label="Match Score", value=f"{match_percentage:.2f}%")

    result = {
        "resume_skills": sorted(list(resume_skills)),
        "job_skills": sorted(list(job_skills)),
        "matching_skills": sorted(list(matching_skills)),
        "missing_skills": sorted(list(missing_skills)),
        "match_percentage": round(match_percentage, 2)
    }

    st.subheader("JSON Output")
    st.json(result)