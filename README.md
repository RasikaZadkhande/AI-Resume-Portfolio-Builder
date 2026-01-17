# AI Resume & Portfolio Builder 🚀

An **AI-powered Resume & Portfolio Builder and Analyzer** that helps students and early-career professionals create **ATS-friendly resumes**, **personalized cover letters**, and **portfolio content**, while also analyzing resumes to detect **skill gaps** and **possible disqualification reasons** for specific job roles.

---

## 📌 Problem Statement

Many students struggle to present their skills, projects, and achievements in a professional and job-specific manner. Generic resume templates fail to highlight individual strengths and often do not meet Applicant Tracking System (ATS) requirements. As a result, deserving candidates get rejected during initial screening without understanding the reason. There is a need for an intelligent, automated system that can generate tailored career documents and provide actionable feedback to improve employability.

---

## 💡 Proposed Solution

This project uses **Generative AI** to automatically:

* Generate customized resumes based on student data
* Create job-specific cover letters
* Build portfolio content (About Me, Skills, Projects, Goals)
* Analyze uploaded resumes for strengths, weaknesses, and ATS score
* Identify missing skills and explain possible disqualification reasons

The system provides clear guidance on what skills students need to learn to improve their chances of selection.

---

## 🧠 AI & Technologies Used

* **Generative AI (LLM)** – Resume, cover letter, and portfolio generation
* **Agentic AI Approach** – Separate AI logic for generation, analysis, and skill-gap detection
* **Natural Language Processing (NLP)** – Resume text extraction and understanding
* **Conceptual RAG** – Job-role skill requirements combined with resume context
* **Python** – Core backend logic
* **Streamlit** – Web-based user interface
* **Groq AI (LLaMA-based model)** – AI inference
* **PyPDF2** – PDF resume text extraction
* **dotenv** – Secure API key management

---

## ✨ Key Features

### 🔹 Resume Builder

* ATS-friendly resume generation
* Job-role–specific customization

### 🔹 Cover Letter Generator

* Personalized cover letters for different roles

### 🔹 Portfolio Generator

* Auto-generated professional portfolio content

### 🔹 Resume Analyzer

* Strengths & weaknesses analysis
* ATS score estimation

### 🔹 Skill Gap & Disqualification Detection

* Required skills for job role
* Missing skills in resume
* Disqualification risk explanation
* Learning roadmap suggestions

---

## 🏗️ System Architecture (High Level)

1. User enters student details or uploads resume
2. Streamlit UI sends data to backend
3. AI model processes input using prompts
4. Resume / Cover Letter / Portfolio is generated
5. Resume Analyzer provides feedback and skill-gap report

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/AI-Resume-Portfolio-Builder.git
cd AI-Resume-Portfolio-Builder
```

### 2️⃣ Install Dependencies

```bash
pip install streamlit python-dotenv PyPDF2 groq
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

### 4️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 📊 Expected Impact

* Improves student employability
* Reduces time and effort in resume preparation
* Helps students understand rejection reasons
* Provides clear guidance on required skills
* Supports better career and internship opportunities

---

## 🔮 Future Enhancements

* PDF export for resumes and portfolios
* Company-specific skill checks (TCS, Google, etc.)
* 30-day personalized learning roadmap
* Interview preparation assistance
* Job portal integration

---

## 👤 Target Users

* Students and fresh graduates
* Internship and job applicants
* Early-career professionals
* College placement and training cells

---

## 📄 License

This project is created for **educational and learning purposes**.

---

⭐ If you find this project useful, feel free to star the repository!
