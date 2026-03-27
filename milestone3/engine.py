from modules.extractor import extract_text
from modules.nlp_processor import preprocess
from modules.skill_extractor import extract_skills
from modules.matcher import match_skills


def analyze(resume_path,job_description):

    resume_text=extract_text(resume_path)

    resume_tokens=preprocess(resume_text)

    job_tokens=preprocess(job_description)

    resume_skills=extract_skills(resume_tokens,resume_text)

    job_skills=extract_skills(job_tokens,job_description)

    result=match_skills(resume_skills,job_skills)

    return result