import streamlit as st
import PyPDF2
from dotenv import load_dotenv
from groq import Groq
import os
import io

# ==================== ENV SETUP ====================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==================== STREAMLIT CONFIG ====================
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="📄",
    layout="wide"
)

# ==================== GROQ CLIENT ====================
client = Groq(api_key=GROQ_API_KEY)
DEFAULT_MODEL = "llama-3.1-8b-instant"

# ==================== PDF TEXT EXTRACTION ====================
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# ==================== AI FUNCTIONS ====================
def generate_resume(profile, model=DEFAULT_MODEL):
    prompt = f"""
You are a professional resume writer.

Create a tailored ATS-friendly resume.

Name: {profile['name']}
Education: {profile['education']}
Skills: {profile['skills']}
Projects: {profile['projects']}
Experience: {profile['experience']}
Target Job Role: {profile['job_role']}

Format:
- Professional Summary
- Skills
- Projects
- Experience
- Education
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1200,
        temperature=0.4
    )
    return response.choices[0].message.content


def generate_cover_letter(profile, model=DEFAULT_MODEL):
    prompt = f"""
Write a professional cover letter for the role of {profile['job_role']}.

Name: {profile['name']}
Education: {profile['education']}
Skills: {profile['skills']}
Projects: {profile['projects']}

Tone: Professional and confident.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=800,
        temperature=0.4
    )
    return response.choices[0].message.content


def generate_portfolio(profile, model=DEFAULT_MODEL):
    prompt = f"""
Create a student portfolio with sections:
- About Me
- Skills
- Projects
- Career Goals

Name: {profile['name']}
Skills: {profile['skills']}
Projects: {profile['projects']}
Target Role: {profile['job_role']}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1000,
        temperature=0.4
    )
    return response.choices[0].message.content


def analyze_resume(resume_text, job_role, model=DEFAULT_MODEL):
    prompt = f"""
You are an HR and ATS expert.

Analyze this resume for the role of {job_role}.
Provide:
1. Strengths (6 points)
2. Weaknesses (6 points)
3. Job-Specific Advice (6 points)
4. ATS Score with explanation
5. Actionable Tips

Resume:
{resume_text}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1500,
        temperature=0.4
    )
    return response.choices[0].message.content


def skill_gap_analysis(resume_text, job_role, model=DEFAULT_MODEL):
    prompt = f"""
You are an ATS system and technical recruiter.

Step 1: List top 10 mandatory skills for job role: {job_role}
Step 2: Identify skills present in resume
Step 3: Identify missing skills
Step 4: Explain disqualification risk
Step 5: Suggest learning roadmap

Format strictly as:

REQUIRED_SKILLS:
- ...

CANDIDATE_HAS:
- ...

MISSING_SKILLS:
- ...

DISQUALIFICATION_REASON:
- ...

IMPROVEMENT_ROADMAP:
- ...

Resume Text:
{resume_text}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1200,
        temperature=0.3
    )
    return response.choices[0].message.content

# ==================== UI ====================
st.title("📄 AI Resume & Portfolio Builder")
st.markdown(
    "Generate **Resumes, Cover Letters & Portfolios** or analyze resumes with **Skill Gap Detection**."
)

tab1, tab2 = st.tabs(["🛠️ Resume Builder", "🔍 Resume Analyzer"])

# ==================== TAB 1 : BUILDER ====================
with tab1:
    st.subheader("🧑‍🎓 Student Details")

    name = st.text_input("Full Name")
    education = st.text_area("Education")
    skills = st.text_area("Skills (comma separated)")
    projects = st.text_area("Projects")
    experience = st.text_area("Experience (optional)")
    job_role = st.text_input("Target Job Role")

    if st.button("🚀 Generate Resume, Cover Letter & Portfolio"):
        if not name or not skills or not job_role:
            st.warning("Please fill Name, Skills and Job Role.")
        else:
            profile = {
                "name": name,
                "education": education,
                "skills": skills,
                "projects": projects,
                "experience": experience,
                "job_role": job_role
            }

            with st.spinner("Generating using AI..."):
                resume = generate_resume(profile)
                cover_letter = generate_cover_letter(profile)
                portfolio = generate_portfolio(profile)

            st.subheader("📄 Resume")
            st.markdown(resume)

            st.subheader("✉️ Cover Letter")
            st.markdown(cover_letter)

            st.subheader("🌐 Portfolio")
            st.markdown(portfolio)

# ==================== TAB 2 : ANALYZER ====================
with tab2:
    st.subheader("Upload Resume (PDF)")
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    job_role_analysis = st.text_input("Target Job Role for Analysis", value="Software Engineer")

    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)

        with st.expander("📄 Extracted Resume Text"):
            st.text_area("Resume Text", resume_text, height=250)

        if st.button("🔍 Resume Analysis"):
            with st.spinner("Analyzing resume..."):
                analysis = analyze_resume(resume_text, job_role_analysis)

            st.subheader("📊 Resume Feedback")
            st.markdown(analysis)

        if st.button("🚨 Skill Gap & Disqualification Analysis"):
            with st.spinner("Checking skill gaps..."):
                skill_gap = skill_gap_analysis(resume_text, job_role_analysis)

            st.subheader("🚨 Skill Gap Report")
            st.markdown(skill_gap)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("Built with ❤️ using **Python, Streamlit & Groq AI**")
