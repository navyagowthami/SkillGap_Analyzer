import streamlit as st
import os
import json
import matplotlib.pyplot as plt
from engine import analyze

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("SkillGapAI")

resume = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
job_desc = st.text_area("Enter Job Description")

if st.button("Analyze"):

    if resume is not None and job_desc != "":

        path = os.path.join(UPLOAD_DIR, resume.name)

        with open(path, "wb") as f:
            f.write(resume.read())

        result = analyze(path, job_desc)

        st.subheader("Matching Skills")
        st.write(result["matching_skills"])

        st.subheader("Missing Skills")
        st.write(result["missing_skills"])

        st.subheader("Match Score")
        st.progress(result["match_percentage"] / 100)

        st.metric("Match Percentage", f"{result['match_percentage']}%")

        # Skill Recommendations
        st.subheader("Recommended Skills to Learn")

        if result["missing_skills"]:
            st.write("To improve your job match, consider learning these skills:")
            for skill in result["missing_skills"]:
                st.write("•", skill)
        else:
            st.success("Great! Your resume matches all required skills.")

        # Download Report
        report = json.dumps(result, indent=2)

        st.download_button(
            label="Download Analysis Report",
            data=report,
            file_name="skillgap_report.json",
            mime="application/json"
        )

        # Visualization
        labels = ["Matching Skills", "Missing Skills"]
        sizes = [len(result["matching_skills"]), len(result["missing_skills"])]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')

        st.subheader("Skill Match Visualization")
        st.pyplot(fig)

    else:
        st.warning("Please upload a resume and enter a job description.")