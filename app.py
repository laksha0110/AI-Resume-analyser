from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber
import streamlit as st

# ----------------------------
# Setup
# ----------------------------

load_dotenv()
client = OpenAI()

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to receive an ATS analysis.")

# ----------------------------
# Inputs
# ----------------------------

uploaded_pdf = st.file_uploader(
    "Upload your resume (PDF format)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the Job Description",
    height=250
)

# ----------------------------
# Analyze Button
# ----------------------------

if st.button("Analyze Resume", use_container_width=True):

    # Validation
    if uploaded_pdf is None:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    # Extract PDF text
    try:
        with pdfplumber.open(uploaded_pdf) as pdf:

            resume_text = ""

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    resume_text += page_text + "\n"

        st.success("Resume uploaded and processed successfully!")

    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        st.stop()

    # Optional: Show extracted resume text
    with st.expander("View Extracted Resume Text"):
        st.text_area(
            "Resume Text",
            resume_text,
            height=300
        )

    # OpenAI Analysis
    try:
        with st.spinner("Analyzing resume..."):

            response = client.responses.create(
                model="gpt-5",
                input=f"""
You are an expert ATS (Applicant Tracking System) resume reviewer.

Analyze the following resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:

1. ATS Match Score (0-100)
2. Overall Summary
3. Strengths
4. Weaknesses
5. Missing Keywords
6. Recommended Improvements
7. Suggested Resume Bullet Points (if applicable)

Format your answer clearly using headings and bullet points.
"""
            )

        st.subheader("📊 Analysis Results")
        st.markdown(response.output_text)

    except Exception as e:
        st.error(f"OpenAI Error: {e}")