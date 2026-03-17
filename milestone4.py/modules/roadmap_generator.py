import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

role_file = os.path.join(BASE_DIR, "data", "role_skills.json")

with open(role_file) as f:
    role_db = json.load(f)

def generate_roadmap(resume_skills, desired_role):

    required = set(role_db.get(desired_role, []))

    current = set(resume_skills)

    missing = required - current

    roadmap = []

    step = 1

    for skill in missing:
        roadmap.append(f"Step {step} – Learn {skill}")
        step += 1

    return list(missing), roadmap