def calculate_ats(resume_skills, job_skills, resume_text):

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    # 1. Skill Match Score
    if len(job_skills) > 0:
        skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills)
    else:
        skill_match = 0

    # 2. Skill Coverage (how many total skills candidate has)
    skill_coverage = len(resume_skills) / 50   # normalize (assuming 50 max skills)
    if skill_coverage > 1:
        skill_coverage = 1

    # 3. Keyword Score (basic resume quality proxy)
    keyword_score = len(resume_text.split()) / 500   # normalize
    if keyword_score > 1:
        keyword_score = 1

    # Final ATS Score
    ats_score = (
        (skill_match * 0.6) +
        (skill_coverage * 0.2) +
        (keyword_score * 0.2)
    ) * 100

    return round(ats_score, 2)