import streamlit as st
import pandas as pd
import zipfile
import os
import PyPDF2
import openai

# Set your OpenAI API Key here or use streamlit secrets
openai.api_key = "YOUR_OPENAI_API_KEY"

# Streamlit App
st.set_page_config(page_title="HR-Xpert", layout="wide")
st.title("🤖 HR-Xpert - Smart HR Automation")

tabs = st.tabs(["📄 Resume Screener", "💬 Employee Sentiment Analyzer"])

# ====================== 1. Resume Screener =======================
with tabs[0]:
    st.header("📄 Resume Screener")
    
    uploaded_zip = st.file_uploader("Upload ZIP of Resumes (PDF format only)", type="zip")
    job_role = st.text_input("Enter the Job Role (e.g., Software Engineer)")
    num_to_shortlist = st.number_input("Number of candidates to shortlist", min_value=1, step=1)
    required_skills = st.text_area("Required Skills (comma-separated, e.g., Python, Java, React)")

    if st.button("🔍 Analyze Resumes"):
        if uploaded_zip and job_role and num_to_shortlist:
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall("resumes/")
            
            scores = []
            for filename in os.listdir("resumes/"):
                if filename.endswith(".pdf"):
                    with open(f"resumes/{filename}", "rb") as f:
                        reader = PyPDF2.PdfReader(f)
                        resume_text = ""
                        for page in reader.pages:
                            resume_text += page.extract_text()

                    prompt = f"""
You are a technical recruiter hiring for the role of {job_role}.
Evaluate the following resume based on these required skills: {required_skills}.
Give a score out of 10 and justify your evaluation.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response['choices'][0]['message']['content']
                    scores.append((filename, result))
            
            scores.sort(key=lambda x: float([s for s in x[1].split() if s.replace('.', '', 1).isdigit()][0]), reverse=True)
            st.success("Shortlisting complete!")
            for i, (filename, result) in enumerate(scores[:int(num_to_shortlist)]):
                st.subheader(f"{i+1}. {filename}")
                st.markdown(result)

# =================== 2. Employee Sentiment Analyzer ================
with tabs[1]:
    st.header("💬 Employee Sentiment Analyzer")

    feedback_file = st.file_uploader("Upload Feedback File (CSV)", type="csv")
    
    if st.button("🧠 Analyze Sentiment"):
        if feedback_file:
            df = pd.read_csv(feedback_file)
            st.write("📄 Raw Feedback Data:", df.head())

            feedbacks = df.iloc[:, 0].tolist()  # assumes feedback is in first column

            analysis_results = []
            for feedback in feedbacks:
                prompt = f"""
Analyze the following employee feedback.
Classify as Positive, Neutral, or Negative.
Also predict attrition risk (High, Medium, Low), and suggest one engagement strategy.

Feedback: "{feedback}"
"""
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response['choices'][0]['message']['content']
                analysis_results.append(result)

            df['Analysis'] = analysis_results
            st.write("📊 Analysis Results:")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Result CSV", data=csv, file_name="sentiment_results.csv", mime="text/csv")
