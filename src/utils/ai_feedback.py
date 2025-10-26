import google.generativeai as genai
import streamlit as st
from .resume_analyzer import (
    calculate_resume_scores,
    calculate_keyword_match,
    analyze_resume_sections
)

def initialize_gemini():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_ai_feedback(resume_text: str, job_description: str = None) -> dict:
    # Calculate various scores
    scores = calculate_resume_scores(resume_text, job_description)
    
    # Get keyword matches if job description is provided
    keyword_matches = {}
    if job_description:
        matched, missing = calculate_keyword_match(resume_text, job_description)
        keyword_matches = {
            'matched': matched,
            'missing': missing
        }
    
    # Analyze resume sections
    section_analysis = analyze_resume_sections(resume_text)
    
    # Get AI suggestions
    model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite')
    
    # Create a detailed prompt based on analysis
    prompt = f"""
    As an expert career advisor, provide specific suggestions to improve this resume.
    
    Current Scores:
    - Readability: {scores.get('readability')}%
    - Formatting: {scores.get('formatting')}%
    - Content: {scores.get('content')}%
    {f"- Keyword Match: {scores.get('keyword_match')}%" if 'keyword_match' in scores else ""}
    
    Areas to focus on:
    1. Summary Section:
    {section_analysis['summary']['suggestions']}
    
    2. Experience Section:
    {section_analysis['experience']['suggestions']}
    
    3. Education Section:
    {section_analysis['education']['suggestions']}
    
    4. Skills Section:
    {section_analysis['skills']['suggestions']}
    
    Original Resume:
    {resume_text}
    
    {f"Job Description:\\n{job_description}" if job_description else ""}
    
    Provide specific, actionable improvements for:
    1. Making the resume more ATS-friendly
    2. Strengthening achievement descriptions
    3. Improving overall impact and readability
    4. Optimizing format and structure
    """
    
    response = model.generate_content(prompt)
    
    return {
        'scores': scores,
        'keyword_matches': keyword_matches,
        'section_analysis': section_analysis,
        'ai_suggestions': response.text
    }