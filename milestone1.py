import PyPDF2
import docx
import os
import re

resume_file = "navyagowthami_resume.pdf"
job_file = "jobDesc.pdf"

if not os.path.exists(resume_file):
    print("Resume file not found.")
    exit()

if not os.path.exists(job_file):
    print("Job description file not found.")
    exit()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
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
        return "Unsupported file format"

resume_text = extract_text(resume_file)
job_text = extract_text(job_file)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

clean_resume = clean_text(resume_text)
clean_job = clean_text(job_text)

skill_list = [
    "python", "java", "c", "c++", "sql", "mysql",
    "pandas", "numpy", "machine learning", "deep learning",
    "flask", "django", "fastapi",
    "html", "css", "javascript",
    "git", "github",
    "aws", "azure", "docker",
    "data structures", "algorithms",
    "rest api", "json"
]

def extract_skills(text, skills):
    found_skills = []
    for skill in skills:
        if skill in text:
            found_skills.append(skill)
    return found_skills

resume_skills = extract_skills(clean_resume, skill_list)
job_skills = extract_skills(clean_job, skill_list)

matching_skills = list(set(resume_skills) & set(job_skills))
missing_skills = list(set(job_skills) - set(resume_skills))

if len(job_skills) > 0:
    match_percentage = (len(matching_skills) / len(job_skills)) * 100
else:
    match_percentage = 0

print("\n===== SKILL GAP ANALYSIS RESULT =====\n")

resume_skills_list = sorted(list(set(resume_skills)))
job_skills_list = sorted(list(set(job_skills)))
matching_skills_list = sorted(list(set(matching_skills)))
missing_skills_list = sorted(list(set(missing_skills)))

print("Skills Available (Resume Holder):")
print(resume_skills_list)

print("\nSkills Required (Job Description):")
print(job_skills_list)

print("\nMatching Skills:")
print(matching_skills_list)

print("\nMissing Skills:")
print(missing_skills_list)

print(f"\nMatch Percentage: {match_percentage:.2f}%")