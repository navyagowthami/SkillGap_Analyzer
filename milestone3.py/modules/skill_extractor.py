import json

with open("skill_database.json") as f:
    skill_db=json.load(f)

all_skills=[]

for category in skill_db:
    all_skills.extend(skill_db[category])


def extract_skills(tokens,text):

    found=set()

    text=text.lower()

    for skill in all_skills:

        if " " in skill:

            if skill in text:
                found.add(skill)

        else:

            if skill in tokens:
                found.add(skill)

    return found