"""
AI feedback generation using Google's Gemini API.
"""
import google.generativeai as genai
import streamlit as st

def initialize_gemini():
    """Initialize the Gemini API with the API key."""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def get_ai_feedback(resume_text):
    """
    Get AI-powered feedback on the resume.
    
    Args:
        resume_text (str): The text content of the resume
        
    Returns:
        str: AI-generated feedback and suggestions
    """
    model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite')
    prompt = f"""
    You're a career expert. Review the following resume and give suggestions to improve:
    - Grammar and clarity
    - Project descriptions
    - ATS friendliness
    - Formatting
    Resume:
    {resume_text}
    """
    response = model.generate_content(prompt)
    return response.text