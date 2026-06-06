from dotenv import load_dotenv
from openai import OpenAI
import pdfplumber

load_dotenv()
client = OpenAI()

with pdfplumber.open("resumeTest.pdf") as pdf:
    resumeTest_text = ""
    for page in pdf.pages:
        resumeTest_text += page.extract_text() or ""

        with open("job.txt", "r") as f:
         job_description = f.read()

        response = client.responses.create(
            model="gpt-5",
            input=f"""
            Analyse this resume

            Give:
            1. A score out of 10 for the resume against the job description
            2.Summarise the strengths of the resume
            3.Summarise the weaknesses of the resume
            4.Provide a match score as a percentage for the resume against the job description
            5.Provide missing skills

            Resume:

            {resumeTest_text}
            
            Job Description:

            {job_description}

            """
        )

print(response.output_text)

