# HR Automation Platform

## Project Overview

This project aims to automate two critical Human Resources (HR) processes using Artificial Intelligence:

1. **Resume Screening**:  
   An AI-powered tool that filters and shortlists resumes for the "Software Engineer" role by matching candidate skills, experience, and qualifications against job descriptions and company-specific requirements.

2. **Employee Sentiment Analysis**:  
   Analyzes employee feedback from surveys and exit interviews to predict attrition risks and recommend engagement strategies to improve workforce retention.

---

## Features

- **Resume Screening Interface**:  
  - HR can upload multiple resumes in a single ZIP file.  
  - Select the number of candidates to shortlist.  
  - Define the target role and specific skill requirements.  
  - One-click processing to get the top shortlisted candidates based on model evaluation.

- **Employee Sentiment Analyzer**:  
  - Input employee feedback data to analyze sentiments.  
  - Predict potential attrition risks.  
  - Suggest actionable engagement strategies to HR.

---

## Technical Approach

- **Data Pipeline**:  
  - Resume documents are extracted and parsed for text content.  
  - Employee feedback data is cleaned and preprocessed for analysis.

- **Model Selection**:  
  - Resume Screening uses Natural Language Processing (NLP) models fine-tuned for skill and experience extraction, leveraging embeddings and similarity scoring.  
  - Sentiment Analysis employs Large Language Models (LLMs) fine-tuned for classification and prediction of attrition risk.

- **Platform Integration**:  
  - User-friendly web interface for HR operations.  
  - Backend ML models deployed on Azure AI Studio or Google AI Studio.  
  - Prompt engineering applied to optimize LLM output accuracy and relevance.  
  - API integration to connect frontend with deployed models for seamless processing.

---

## Technologies Used

- Python (NLP libraries like SpaCy, transformers)  
- Azure AI Studio / Google AI Studio (Model building and deployment)  
- Flask/Django or React (Frontend interface)  
- ZIP file processing and text extraction libraries  
- Git for version control

---

## Usage Instructions

1. Upload a ZIP file containing resumes.  
2. Select the number of resumes to shortlist.  
3. Enter the role (e.g., Software Engineer) and any specific skill requirements.  
4. Click **Process** to get shortlisted resumes.  
5. For sentiment analysis, upload employee feedback data and run the analysis to get attrition risk and engagement recommendations.

---

## Future Work

- Expand resume screening to multiple roles and more complex requirements.  
- Integrate real-time feedback analysis and dashboard visualization.  
- Add continuous learning capabilities to improve model accuracy over time.

---

## License

This project is for internship assignment purposes and is not licensed for commercial use.

---

*Developed as part of the HR Automation internship assignment.*
