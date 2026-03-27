import re
import urllib.parse
from role_database import get_role_data

# Common skill keywords for NLP extraction
SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust", "swift",
    "react", "angular", "vue", "node.js", "express", "django", "flask", "spring",
    "html", "css", "tailwind css", "bootstrap", "sass",
    "sql", "mysql", "postgresql", "mongodb", "redis", "firebase",
    "docker", "kubernetes", "aws", "azure", "gcp", "cloud services",
    "git", "github", "gitlab", "ci/cd",
    "machine learning", "deep learning", "artificial intelligence", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "pandas", "numpy", "matplotlib", "seaborn",
    "data analysis", "data visualization", "data cleaning", "data engineering",
    "statistics", "linear algebra", "calculus", "probability",
    "excel", "power bi", "tableau", "reporting",
    "rest api", "graphql", "microservices", "api design",
    "linux", "bash", "scripting", "shell",
    "testing", "unit testing", "integration testing", "selenium",
    "agile", "scrum", "jira", "project management",
    "networking", "security tools", "penetration testing", "firewalls",
    "cryptography", "incident response", "siem", "risk assessment",
    "responsive design", "ux design", "figma", "adobe xd",
    "terraform", "ansible", "jenkins", "monitoring", "mlops",
    "authentication", "databases",
]

# Stopwords for text preprocessing (Using NLTK if available, fallback to basic set)
try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    STOPWORDS = set(stopwords.words('english'))
except Exception:
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "it", "that", "this", "was", "are",
        "be", "has", "had", "have", "will", "would", "could", "should", "may",
        "can", "do", "did", "not", "so", "if", "as", "we", "our", "your",
        "i", "me", "my", "he", "she", "they", "them", "their", "his", "her",
        "its", "been", "being", "were", "am", "what", "which", "who", "whom",
        "about", "into", "through", "during", "before", "after", "above",
        "below", "between", "same", "than", "too", "very", "just", "also",
    }
    
    def word_tokenize(text):
        return text.split()

def preprocess_text(text: str) -> str:
    # Lowercase and replace non-word characters (except some specific ones) with space
    text = text.lower()
    text = re.sub(r'[^\w\s\+\#\.\/\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills(text: str) -> list:
    processed = preprocess_text(text)
    found = []

    for skill in SKILL_KEYWORDS:
        # Escape skill for regex and create word boundary pattern
        escaped_skill = re.escape(skill)
        pattern = re.compile(rf'\b{escaped_skill}\b', re.IGNORECASE)
        if pattern.search(processed):
            found.append(skill)

    # Check for multi-word skills with different spacing
    if "node" in processed and "js" in processed and "node.js" not in found:
        found.append("node.js")
    if "power" in processed and "bi" in processed and "power bi" not in found:
        found.append("power bi")
    if "tailwind" in processed and "tailwind css" not in found:
        found.append("tailwind css")

    # Remove duplicates but preserve order
    seen = set()
    return [x for x in found if not (x in seen or seen.add(x))]

def tokenize(text: str) -> list:
    processed = preprocess_text(text)
    # Tokenize using nltk or fallback
    tokens = word_tokenize(processed)
    return [word for word in tokens if len(word) > 1 and word not in STOPWORDS]

def calculate_skill_match(resume_skills: list, jd_skills: list) -> int:
    if not jd_skills:
        return 0
    matched = [skill for skill in jd_skills if any(rs.lower() == skill.lower() for rs in resume_skills)]
    return round((len(matched) / len(jd_skills)) * 100)

def calculate_ats_score(resume_text: str, jd_text: str) -> int:
    resume_tokens = set(tokenize(resume_text))
    jd_tokens = tokenize(jd_text)

    if not jd_tokens:
        return 0

    match_count = sum(1 for token in jd_tokens if token in resume_tokens)
    keyword_score = round((match_count / len(jd_tokens)) * 100)
    
    # Formatting checks
    format_score = 100
    if len(resume_text) < 200:
        format_score -= 20
    if len(resume_text) > 5000:
        format_score -= 10
        
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'[\d\-\(\)\+\s]{7,}', resume_text))
    
    if not has_email:
        format_score -= 10
    if not has_phone:
        format_score -= 10

    score = round(keyword_score * 0.7 + format_score * 0.3)
    return max(0, min(100, score))

def find_missing_skills(resume_skills: list, required_skills: list) -> list:
    return [skill for skill in required_skills if not any(rs.lower() == skill.lower() for rs in resume_skills)]

def get_matched_skills(resume_skills: list, required_skills: list) -> list:
    return [skill for skill in required_skills if any(rs.lower() == skill.lower() for rs in resume_skills)]

def generate_job_recommendations(skills: list) -> list:
    jobs = []
    skill_set = {s.lower() for s in skills}

    if "python" in skill_set and ("machine learning" in skill_set or "deep learning" in skill_set):
        jobs.append("Machine Learning Engineer")
    if "python" in skill_set and "sql" in skill_set:
        jobs.append("Data Analyst")
    if any(s in skill_set for s in ["react", "javascript", "vue", "angular"]):
        jobs.append("Frontend Developer")
    if any(s in skill_set for s in ["node.js", "django", "flask"]):
        jobs.append("Backend Developer")
    if "python" in skill_set and ("statistics" in skill_set or "data analysis" in skill_set):
        jobs.append("Data Scientist")
    if any(s in skill_set for s in ["docker", "kubernetes", "ci/cd"]):
        jobs.append("DevOps Engineer")
    if "react" in skill_set and ("node.js" in skill_set or "sql" in skill_set):
        jobs.append("Full Stack Developer")

    if not jobs:
        jobs.extend(["Software Developer", "Junior Developer", "Technical Analyst"])

    # Unique and top 5
    seen = set()
    return [x for x in jobs if not (x in seen or seen.add(x))][:5]

def analyze_resume_vs_jd(resume_text: str, jd_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched_skills = get_matched_skills(resume_skills, jd_skills)
    missing_skills_for_jd = find_missing_skills(resume_skills, jd_skills)
    skill_match_percentage = calculate_skill_match(resume_skills, jd_skills)
    ats_score = calculate_ats_score(resume_text, jd_text)

    locations = ["Remote", "Bangalore", "Chennai", "Hyderabad", "Mumbai", "San Francisco", "New York", "London"]
    job_titles = generate_job_recommendations(resume_skills)
    
    recommended_jobs = []
    for i, title in enumerate(job_titles):
        recommended_jobs.append({
            "title": title,
            "location": locations[i % len(locations)]
        })

    return {
        "resumeSkills": resume_skills,
        "jdSkills": jd_skills,
        "matchedSkills": matched_skills,
        "missingSkillsForJD": missing_skills_for_jd,
        "skillMatchPercentage": skill_match_percentage,
        "atsScore": ats_score,
        "recommendedJobs": recommended_jobs,
    }

def generate_roadmap(missing_skills: list) -> list:
    durations = ["1-2 weeks", "2-3 weeks", "2-4 weeks", "3-4 weeks", "4-6 weeks"]
    roadmap = []
    
    for index, skill in enumerate(missing_skills):
        roadmap.append({
            "step": index + 1,
            "title": f"Learn {skill.capitalize()}",
            "description": f"Master the fundamentals of {skill} through structured learning, hands-on projects, and practice exercises.",
            "duration": durations[index % len(durations)],
            "skill": skill,
        })
        
    return roadmap

def get_youtube_resources(role_name: str, missing_skills: list) -> list:
    role_data = get_role_data(role_name)
    if not role_data:
        return []

    resources = []
    for skill in missing_skills:
        skill_lower = skill.lower()
        resource = role_data["youtubeResources"].get(skill_lower)
        
        if resource:
            resources.append({
                "skill": skill,
                "title": resource["title"],
                "url": resource["url"]
            })
        else:
            # Fallback
            query = urllib.parse.quote(skill + " tutorial")
            resources.append({
                "skill": skill,
                "title": f"{skill.capitalize()} – Complete Tutorial",
                "url": f"https://www.youtube.com/results?search_query={query}"
            })
            
    return resources
