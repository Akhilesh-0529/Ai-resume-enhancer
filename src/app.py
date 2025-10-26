"""
Main Streamlit application for Resume Enhancement.
"""
import streamlit as st
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.ai_feedback import initialize_gemini, get_ai_feedback

def main():
    # Initialize Gemini
    initialize_gemini()
    
    # Set page config
    st.set_page_config(page_title="Gemini Resume Enhancer", page_icon="📄", layout="wide")
    
    # Header
    st.title("Resume Enhancer")
    st.write("Upload your resume and get instant feedback from Google's Gemini AI. Improve your resume's grammar, project descriptions, ATS friendliness, and formatting.")
    
    # Upload resume
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], label_visibility="collapsed")
    
    # Main logic
    if uploaded_file:
        if st.sidebar.button("🗑️ Clear"):
            st.cache_data.clear()
            st.rerun()
            
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.subheader("📄 Your Resume")
            try:
                if uploaded_file.name.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(uploaded_file)
                else:
                    resume_text = extract_text_from_docx(uploaded_file)
                st.text_area("Preview", resume_text, height=500, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Error extracting text: {e}")
                st.stop()
        
        with col2:
            st.subheader("💡 Gemini's Suggestions")
            if st.button("🧠 Get Gemini Suggestions"):
                with st.spinner("Thinking..."):
                    try:
                        feedback = get_ai_feedback(resume_text)
                        st.success("Done!")
                        st.markdown(feedback)
                    except Exception as e:
                        st.error(f"Error getting feedback: {e}")
            else:
                st.info("Click the button to get feedback on your resume.")

if __name__ == "__main__":
    main()