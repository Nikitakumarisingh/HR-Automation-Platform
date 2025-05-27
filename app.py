import streamlit as st
import pandas as pd
import zipfile
import os
import PyPDF2
import openai

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup page
st.set_page_config(page_title="HR-Xpert", layout="wide")
st.title("🤖 HR-Xpert - Smart HR Automation")

tabs = st.tabs(["📄 Resume Screener", "💬 Employee Sentiment Analyzer"])

# ====================== 1. Resume Screener =======================
with tabs[0]:
    st.header("📄 Resume Screener")

    uploaded_zip = st.file_uploader("Upload ZIP of Resumes (PDF format only)", type="zip")
    num_to_shortlist = st.number_input("Number of candidates to shortlist", min_value=1, step=1)

    # Load job description from file
    try:
        with open("job_description.txt", "r") as file:
            job_description = file.read()
    except FileNotFoundError:
        job_description = ""
        st.error("❌ 'job_description.txt' not found. Please create this file in the project root.")

    st.text_area("📄 Job Description Preview (from job_description.txt)", job_description, height=200, disabled=True)

    if st.button("🔍 Analyze Resumes"):
        if uploaded_zip and job_description and num_to_shortlist:
            # Clean up old resumes
            if not os.path.exists("resumes"):
                os.makedirs("resumes")
            else:
                for file in os.listdir("resumes"):
                    os.remove(f"resumes/{file}")

            # Extract resumes
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
You are a technical recruiter hiring for the following role. Evaluate the resume and score out of 10 with a justification.

Job Description:
{job_description}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""
                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}]
                        )
                        result = response['choices'][0]['message']['content']
                        scores.append((filename, result))
                    except Exception as e:
                        st.error(f"❌ Error analyzing {filename}: {e}")

            # Sort and show top resumes
            def extract_score(text):
                for word in text.split():
                    try:
                        score = float(word)
                        if 0 <= score <= 10:
                            return score
                    except:
                        continue
                return 0

            scores.sort(key=lambda x: extract_score(x[1]), reverse=True)

            st.success("✅ Shortlisting complete!")
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

            feedbacks = df.iloc[:, 0].tolist()

            analysis_results = []
            for feedback in feedbacks:
                prompt = f"""
Analyze the following employee feedback.
Classify as Positive, Neutral, or Negative.
Predict attrition risk (High, Medium, Low).
Suggest one engagement strategy.

Feedback: "{feedback}"
"""
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response['choices'][0]['message']['content']
                    analysis_results.append(result)
                except Exception as e:
                    analysis_results.append(f"Error: {e}")

            df['Analysis'] = analysis_results
            st.write("📊 Analysis Results:")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Result CSV", data=csv, file_name="sentiment_results.csv", mime="text/csv")
