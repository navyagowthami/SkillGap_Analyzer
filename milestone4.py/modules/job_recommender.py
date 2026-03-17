import random

def recommend_jobs(resume_skills):

    job_roles = []

    if "python" in resume_skills:
        job_roles.append("Python Developer")

    if "machine learning" in resume_skills:
        job_roles.append("Machine Learning Engineer")

    if "sql" in resume_skills:
        job_roles.append("Data Analyst")

    if "javascript" in resume_skills:
        job_roles.append("Frontend Developer")

    cities = ["Chennai", "Bangalore", "Hyderabad", "Pune"]

    jobs = []

    for role in job_roles:
        jobs.append(f"{role} – {random.choice(cities)}")

    return jobs