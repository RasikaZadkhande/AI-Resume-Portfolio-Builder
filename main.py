import streamlit as st
import PyPDF2
from dotenv import load_dotenv
from groq import Groq
import os
import io

# -------------------- ENV SETUP --------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------- STREAMLIT CONFIG --------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# -------------------- GROQ CLIENT --------------------
client = Groq(api_key=GROQ_API_KEY)

# -------------------- PDF TEXT EXTRACTION --------------------
def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()

# -------------------- AI MODEL --------------------
DEFAULT_MODEL = "llama-3.1-8b-instant"

def analyze_resume_with_ai(resume_text, job_role, model=DEFAULT_MODEL):
    """Check if document is resume and analyze it using Groq AI."""

    prompt = f"""
You are an expert document classifier and HR career coach.

First decide whether this document is a RESUME or NOT.

Follow exactly this format:

IS_RESUME: YES or NO
DOC_TYPE: <type of document if not resume>
REASON: <why you think so>

If IS_RESUME is YES:
- Analyze the resume for job role: {job_role}
- Provide:
  1. Strengths
  2. Areas for Improvement
  3. Job-Specific Advice
  4. ATS Score (percentage + explanation)
  5. Actionable Tips

Each topic must contain 6 sub-points.

If IS_RESUME is NO:
- Do NOT analyze as a resume
- Describe what this document contains

Here is the document text:
{resume_text}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert document classifier and HR career coach."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=1500,
        temperature=0.4
    )

    return response.choices[0].message.content

# -------------------- STREAMLIT UI --------------------
st.title("📄 AI Resume Analyzer")
st.markdown("Upload your **PDF resume** for AI-powered feedback and career advice.")

# Sidebar
st.sidebar.header("Analysis Settings")
job_role = st.sidebar.text_input("Target Job Role", value="Software Engineer")
model_choice = st.sidebar.text_input("Groq Model ID", value=DEFAULT_MODEL)

# File uploader
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

    resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text:
        with st.expander("📄 Resume Text Preview"):
            st.text_area("Extracted Text", resume_text, height=250)

        if st.button("🔍 Analyze Resume"):
            analysis = analyze_resume_with_ai(
                resume_text,
                job_role,
                model_choice
            )

            st.subheader("📊 AI Feedback")
            st.markdown(analysis)

            st.download_button(
                label="⬇️ Download Feedback",
                data=analysis,
                file_name=f"resume_feedback_{job_role}.txt",
                mime="text/plain"
            )

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using **Python, Streamlit & Groq**")
