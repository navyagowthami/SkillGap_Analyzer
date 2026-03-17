from modules.extractor import extract_text
from modules.nlp_processor import preprocess
from modules.skill_extractor import extract_skills
from modules.matcher import match_skills
from modules.ats_calculator import calculate_ats
from modules.job_recommender import recommend_jobs
from modules.roadmap_generator import generate_roadmap
from modules.youtube_resources import youtube_resources


def analyze(resume_path, jd_path, desired_role):

    resume_text = extract_text(resume_path)
    jd_text = extract_text(jd_path)

    resume_tokens = preprocess(resume_text)
    jd_tokens = preprocess(jd_text)

    resume_skills = extract_skills(resume_tokens, resume_text)
    jd_skills = extract_skills(jd_tokens, jd_text)

    match_result = match_skills(resume_skills, jd_skills)

    ats_score = calculate_ats(resume_skills, jd_skills)

    jobs = recommend_jobs(resume_skills)

    missing_role_skills, roadmap = generate_roadmap(resume_skills, desired_role)

    youtube = youtube_resources(missing_role_skills)

    return {
        "resume_skills": list(resume_skills),
        "job_skills": list(jd_skills),
        "match_percentage": match_result["match_percentage"],
        "missing_skills_jd": match_result["missing_skills"],
        "ats_score": ats_score,
        "job_recommendations": jobs,
        "missing_role_skills": missing_role_skills,
        "roadmap": roadmap,
        "youtube_resources": youtube
    }