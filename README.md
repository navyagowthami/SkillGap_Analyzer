# SkillGapAI – Career Guidance System

SkillGapAI is an AI-based application that analyzes a resume, compares it with a job description, identifies skill gaps, calculates ATS score, and provides job recommendations along with a learning roadmap.

## Features

- Resume and Job Description analysis (PDF, DOCX, TXT)
- Skill extraction using NLP (spaCy)
- Skill match percentage calculation
- ATS score calculation
- Missing skills detection
- Job recommendations
- Desired role selection (dropdown)
- Skill gap analysis for desired role
- Learning roadmap generation
- YouTube learning resources
- Visualization (Pie Chart and Bar Chart)
- Clean UI using Streamlit

## Technologies Used

- Python
- Streamlit
- spaCy
- PyPDF2
- python-docx
- pytesseract
- matplotlib
- JSON


## Project Structure

SkillGapAI/
- app.py  
- engine.py  
- requirements.txt  

data/
- skill_database.json  
- role_skills.json  

modules/
- extractor.py  
- nlp_processor.py  
- skill_extractor.py  
- matcher.py  
- ats_calculator.py  
- job_recommender.py  
- roadmap_generator.py  
- youtube_resources.py  

uploads/

---

## Installation

1. Clone repository
git clone https://github.com/your-username/SkillGapAI.git  
cd SkillGapAI  

2. Install dependencies
pip install -r requirements.txt  

3. Install spaCy model
python -m spacy download en_core_web_sm  

4. Run application
streamlit run app.py  


## How It Works

1. Upload Resume  
2. Upload Job Description  
3. Select Desired Role  
4. Click Analyze  

The system performs:
- Text extraction  
- NLP preprocessing  
- Skill extraction  
- Resume vs JD comparison  
- ATS score calculation  
- Missing skill detection  
- Job recommendations  
- Role-based skill gap analysis  
- Learning roadmap generation  
- YouTube resource suggestions  

## Example Output

- ATS Score: 75%  
- Match Percentage: 70%  
- Missing Skills: Machine Learning, Statistics  

Recommended Jobs:
- Data Analyst – Chennai  
- Python Developer – Bangalore  

Desired Role: Data Scientist  

Missing Skills:
- Machine Learning  
- Statistics  
- Deep Learning  

Learning Roadmap:
- Learn Statistics  
- Learn Machine Learning  
- Build Projects  

## Author

Navya Gowthami

## License

This project is developed for educational purposes.
