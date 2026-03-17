def match_skills(resume_skills,job_skills):

    matching=resume_skills.intersection(job_skills)

    missing=job_skills-resume_skills

    if len(job_skills)>0:
        score=(len(matching)/len(job_skills))*100
    else:
        score=0

    return {

        "resume_skills":list(resume_skills),

        "job_skills":list(job_skills),

        "matching_skills":list(matching),

        "missing_skills":list(missing),

        "match_percentage":round(score,2)

    }