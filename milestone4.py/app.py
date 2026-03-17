import streamlit as st
import os
import json
import matplotlib.pyplot as plt
from engine import analyze

# Page configuration
st.set_page_config(
    page_title="SkillGapAI",
    layout="wide"
)

st.markdown(
"""
<style>
.title {
    color:#4CAF50;
    font-weight:bold;
}

.missing {
    color:#ff4b4b;
    font-weight:bold;
}

.match {
    color:#00c853;
    font-weight:bold;
}

.jobs {
    color:#4da6ff;
}

.roadmap {
    color:#ff9800;
}

.resources {
    color:#9c27b0;
}
</style>
""",
unsafe_allow_html=True
)

# Title
st.title("SkillGapAI – Career Guidance System")

# Upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load role database
with open("data/role_skills.json") as f:
    role_db = json.load(f)

roles = list(role_db.keys())

# Upload section
col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

with col2:
    job_desc_file = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "docx", "txt"]
    )

# Role selection
desired_role = st.selectbox(
    "Select Your Desired Role",
    roles
)

# Analyze button
analyze_button = st.button("Analyze")

# Main analysis logic
if analyze_button:

    if resume and job_desc_file and desired_role:

        # Save resume
        resume_path = os.path.join(UPLOAD_DIR, resume.name)
        with open(resume_path, "wb") as f:
            f.write(resume.read())

        # Save job description
        jd_path = os.path.join(UPLOAD_DIR, job_desc_file.name)
        with open(jd_path, "wb") as f:
            f.write(job_desc_file.read())

        # Run analysis
        result = analyze(resume_path, jd_path, desired_role)

        st.divider()

        # Scores
        col1, col2 = st.columns(2)

        with col1:
            st.metric("ATS Score", f"{result['ats_score']}%")

        with col2:
            st.metric("Skill Match Percentage", f"{result['match_percentage']}%")

        st.divider()

        # Missing skills
        st.subheader("Missing Skills for Job Description")

        if result["missing_skills_jd"]:
            for skill in result["missing_skills_jd"]:
                st.write("•", skill)
        else:
            st.success("No missing skills detected")

        # Chart calculations
        matching_count = len(result["job_skills"]) - len(result["missing_skills_jd"])
        missing_count = len(result["missing_skills_jd"])

        st.divider()

        # Charts side by side
        col1, col2 = st.columns(2)

        # Pie Chart
        with col1:

            labels = ["Matching Skills", "Missing Skills"]
            sizes = [matching_count, missing_count]

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)

            st.subheader("Skill Match Distribution")
            st.pyplot(fig1)

        # Bar Chart
        with col2:

            categories = ["Matching Skills", "Missing Skills"]
            values = [matching_count, missing_count]

            fig2, ax2 = plt.subplots()
            ax2.bar(categories, values)

            ax2.set_ylabel("Number of Skills")
            ax2.set_title("Skill Comparison")

            st.subheader("Skill Comparison Chart")
            st.pyplot(fig2)

        st.divider()

        # Job Recommendations
        st.subheader("Recommended Jobs")

        for job in result["job_recommendations"]:
            st.write("•", job)

        st.divider()

        # Missing skills for desired role
        st.subheader("Missing Skills for Desired Role")

        if result["missing_role_skills"]:
            for skill in result["missing_role_skills"]:
                st.write("•", skill)
        else:
            st.success("You already meet the skills required for this role!")

        st.divider()

        # Learning roadmap
        st.subheader("Learning Roadmap")

        for step in result["roadmap"]:
            st.write(step)

        st.divider()

        # YouTube resources
        st.subheader("YouTube Learning Resources")

        for skill, link in result["youtube_resources"].items():
            st.write(f"{skill} → {link}")

    else:
        st.warning("Please upload both Resume and Job Description files.")