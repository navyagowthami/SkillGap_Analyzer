def calculate_ats(resume_skills, job_skills):

    matched = resume_skills.intersection(job_skills)

    if len(job_skills) == 0:
        return 0

    ats_score = (len(matched) / len(job_skills)) * 100

    return round(ats_score, 2)