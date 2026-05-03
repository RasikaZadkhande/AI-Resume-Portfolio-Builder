import streamlit as st 
import PyPDF2
import json
from dotenv import load_dotenv
from groq import Groq
import os
import io

# Load environment variables
load_dotenv()
# Read Groq API key from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit page config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Initialize Groq client (reads API key from env if provided)
client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        p = page.extract_text()
        if p:
            text += p + "\n"
    return text.strip()

# Using a high-performance model as the default
DEFAULT_MODEL = "llama-3.1-8b-instant"

def analyze_resume_with_ai(resume_text, job_role, model=DEFAULT_MODEL):
    """Use Groq to check if file is a resume + analyze it."""

    prompt = f"""
You are an expert document classifier + HR career coach.

First decide whether this document is a RESUME or NOT.

Follow exactly this format:

IS_RESUME: YES or sNO
DOC_TYPE: <type of document if not resume>
REASON: <why you think so>

If IS_RESUME is YES:
  - Analyze the resume for job role: {job_role}
  - Provide the following:
      1. Strengths
      2. Areas for Improvement
      3. Job-Specific Advice
      4. ATS score in percentages with description
      5. Actionable Tips
    
in this topic each topic caontain 6 subpoints 
If IS_RESUME is NO:
  - Do NOT analyze as a resume.
  - Describe what this document contains.

Here is the full document text:
{resume_text}
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert document classifier + HR career coach."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=1500,
        temperature=0.4,
    )

    return resp.choices[0].message.content
#---------

def generate_portfolio_data(resume_text, model=DEFAULT_MODEL):

    prompt = f"""
    Extract structured data from this resume.

    Return ONLY JSON:

    {{
      "name": "",
      "about": "",
      "skills": ["", ""],
      "projects": [
    {{
      "title": "",
      "description": ""
    }}
  ],
  "experience": ["", ""],
  "contact": {{
    "email": ""
  }}
}}

Resume:
{resume_text}

"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a data extractor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    data = response.choices[0].message.content
    data = data.replace("```json", "").replace("```", "")

    return json.loads(data)

#----
def render_portfolio(template, data):

    # Skills
    skills_html = "".join(
        f'<span class="tag">{s}</span>' 
        for s in data.get("skills", [])
    )

    # Projects
    projects_html = ""
    for p in data.get("projects", []):
        projects_html += f"""
        <div class="project">
            <h3>{p.get('title','')}</h3>
            <p>{p.get('description','')}</p>
        </div>
        """

    # Experience
    experience_html = "".join(
        f"<p>{e}</p>" 
        for e in data.get("experience", [])
    )

    html = template.replace("{{name}}", data.get("name",""))
    html = html.replace("{{about}}", data.get("about",""))
    html = html.replace("{{skills}}", skills_html)
    html = html.replace("{{projects}}", projects_html)
    html = html.replace("{{experience}}", experience_html)
    html = html.replace("{{email}}", data.get("contact", {}).get("email",""))

    return html
# Main App
st.title("📄 AI Resume Analyzer ")
st.markdown("Upload your PDF resume below for AI-powered feedback and career advice!")

# Sidebar for job role input and model selection
st.sidebar.header("Analysis Settings")
job_role = st.sidebar.text_input("Enter the target job role:", value="Software Engineer")
model_choice = st.sidebar.text_input("Groq Model ID:", value=DEFAULT_MODEL)

# File uploader
uploaded_file = st.file_uploader("Choose a PDF resume file", type="pdf")

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
    
    resume_text = extract_text_from_pdf(uploaded_file)
    
    if resume_text:
        with st.expander("Resume Text Preview", expanded=False):
            st.text_area("Content", resume_text, height=200)
        
        if st.button("🔍 Analyze Resume"):
            analysis = analyze_resume_with_ai(resume_text, job_role, model=model_choice)
            st.subheader("AI Feedback")
            st.markdown(analysis)
            
            st.download_button(
                label="Download Feedback as TXT",
                data=analysis,
                file_name=f"resume_feedback_{job_role}.txt",
                mime="text/plain"
            )
        
        if st.button("🚀 Generate Portfolio"):

           data = generate_portfolio_data(resume_text, model_choice)

           with open("template.html", "r", encoding="utf-8") as f:
               template = f.read()

           final_html = render_portfolio(template, data)

           st.subheader("🌍 Portfolio Preview")
           st.components.v1.html(final_html, height=500, scrolling=True)

           st.download_button(
               "⬇️ Download Portfolio",
               final_html,
               "portfolio.html",
               "text/html"
            )
           

           

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using python,Streamlit & Groq.")
