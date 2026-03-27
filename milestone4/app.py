import streamlit as st
import time
from file_parser import parse_file, is_valid_file_type
from role_database import get_available_roles, get_role_data
from nlp_engine import analyze_resume_vs_jd, generate_roadmap, get_youtube_resources

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for aesthetic, modern layout
st.markdown("""
<style>
    .stProgress .st-bo {
        background-color: #3b82f6;
    }
    .skill-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    .matched { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .missing { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .neutral { background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
    .yt-card {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
        background: white;
    }
    .yt-card:hover {
        border-color: #ef4444;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .yt-card a {
        text-decoration: none;
        color: inherit;
    }
</style>
""", unsafe_allow_html=True)

def reset_analysis():
    for key in ['analysis_result', 'roadmap', 'yt_resources', 'desired_role']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def main():
    if 'analysis_result' not in st.session_state:
        show_dashboard()
    else:
        show_results()

def show_dashboard():
    st.title("⚡ SkillGap AI")
    st.subheader("Resume Analysis & Learning Roadmap")
    st.markdown("Upload your resume and a job description to get your skill match, ATS score, and a personalized learning roadmap.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### 📄 Upload Resume')
        resume_file = st.file_uploader("Drop your resume here (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"], key="resume")
        
    with col2:
        st.markdown('#### 📝 Upload Job Description')
        jd_file = st.file_uploader("Drop the JD here (TXT, PDF, DOCX)", type=["txt", "pdf", "docx"], key="jd")
        
    st.markdown(" ")
    desired_role = st.selectbox("🎯 Desired Role", options=[""] + get_available_roles(), index=0)

    if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
        if not resume_file or not jd_file:
            st.error("Please upload both your resume and job description.")
            return
        if not desired_role:
            st.error("Please select your desired role.")
            return
        
        with st.spinner("Analyzing with NLP..."):
            try:
                resume_text = parse_file(resume_file)
                jd_text = parse_file(jd_file)
                
                if len(resume_text.strip()) < 20:
                    st.error("Could not extract enough text from resume. Ensure the file contains text.")
                    return
                
                result = analyze_resume_vs_jd(resume_text, jd_text)
                
                role_data = get_role_data(desired_role)
                from nlp_engine import find_missing_skills
                missing_for_role = find_missing_skills(result["resumeSkills"], role_data["requiredSkills"])
                
                roadmap = generate_roadmap(missing_for_role)
                yt_resources = get_youtube_resources(desired_role, missing_for_role)
                
                # Save to session state
                st.session_state["analysis_result"] = result
                st.session_state["desired_role"] = desired_role
                st.session_state["missing_for_role"] = missing_for_role
                st.session_state["roadmap"] = roadmap
                st.session_state["yt_resources"] = yt_resources
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

def show_results():
    result = st.session_state["analysis_result"]
    desired_role = st.session_state["desired_role"]
    missing_for_role = st.session_state["missing_for_role"]
    roadmap = st.session_state["roadmap"]
    yt_resources = st.session_state["yt_resources"]

    with st.sidebar:
        st.markdown("### Actions")
        if st.button("← New Analysis", use_container_width=True):
            reset_analysis()

    st.title("📊 Analysis Results")
    st.markdown(f"**Desired Role:** {desired_role}")

    # Scores
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Skill Match", f"{result['skillMatchPercentage']}%")
        st.progress(result['skillMatchPercentage'] / 100)
    with col2:
        st.metric("ATS Score", f"{result['atsScore']}%")
        st.progress(result['atsScore'] / 100)
        
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["🎯 Overview", "📍 Learning Roadmap", "▶️ YouTube Resources"])
    
    with tab1:
        st.subheader("Skill Breakdown")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### ✅ Matched Skills")
            if result['matchedSkills']:
                html = "".join([f'<span class="skill-badge matched">{s}</span>' for s in result['matchedSkills']])
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.write("None")
                
            st.markdown("#### ❌ Missing for JD")
            if result['missingSkillsForJD']:
                html = "".join([f'<span class="skill-badge missing">{s}</span>' for s in result['missingSkillsForJD']])
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.write("None")
                
        with c2:
            st.markdown(f"#### 🎯 Missing for {desired_role}")
            if missing_for_role:
                html = "".join([f'<span class="skill-badge missing">{s}</span>' for s in missing_for_role])
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.write("None")
                
            st.markdown("#### 📖 Your Resume Skills")
            if result['resumeSkills']:
                html = "".join([f'<span class="skill-badge neutral">{s}</span>' for s in result['resumeSkills']])
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.write("None")
        
        st.markdown("---")
        st.subheader("💼 Recommended Jobs")
        for job in result['recommendedJobs']:
            st.info(f"**{job['title']}** - {job['location']}")

    with tab2:
        st.subheader(f"Learning Roadmap for {desired_role}")
        if not roadmap:
            st.success("No missing skills detected – you're already qualified! 🎉")
        else:
            for step in roadmap:
                with st.expander(f"Step {step['step']}: {step['title']} ({step['duration']})", expanded=True):
                    st.write(step['description'])

    with tab3:
        st.subheader("YouTube Learning Resources")
        if not yt_resources:
            st.success("No additional resources needed – your skills are complete! 🎉")
        else:
            for item in yt_resources:
                st.markdown(f"""
                <div class="yt-card">
                    <a href="{item['url']}" target="_blank">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <div style="background-color: #fee2e2; color: #ef4444; padding: 10px; border-radius: 8px;">
                                ▶️
                            </div>
                            <div>
                                <h5 style="margin: 0; padding: 0; color: #ef4444; text-transform: uppercase; font-size: 10px;">{item['skill']}</h5>
                                <p style="margin: 0; padding: 2px 0 0 0; font-weight: bold;">{item['title']}</p>
                            </div>
                        </div>
                    </a>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
