"""
Main Streamlit application for Resume Enhancement
"""
import streamlit as st
import json
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.ai_feedback import initialize_gemini, get_ai_feedback
from utils.session_manager import SessionManager
from utils.speech_handler import SpeechHandler
from utils.image_generator import ResumeImageGenerator

def display_scores(scores):
    cols = st.columns(len(scores))
    for col, (metric, score) in zip(cols, scores.items()):
        with col:
            st.metric(
                label=metric.replace('_', ' ').title(),
                value=f"{score:.1f}%",
                delta=f"{score - 70:.1f}%" if score > 70 else f"{70 - score:.1f}%",
                delta_color="normal" if score > 70 else "inverse"
            )

def display_keyword_matches(matches):
    """Display keyword matches and missing keywords."""
    if not matches:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Matched Keywords")
        if matches['matched']:
            for keyword in matches['matched']:
                st.success(keyword)
        else:
            st.info("No keyword matches found")
    
    with col2:
        st.subheader("❌ Missing Keywords")
        if matches['missing']:
            for keyword in matches['missing']:
                st.error(keyword)
        else:
            st.success("No missing keywords!")

def display_section_analysis(analysis):
    """Display section-by-section analysis."""
    st.subheader("📝 Section Analysis")
    
    for section, details in analysis.items():
        with st.expander(f"{section.title()} Section"):
            if details['content']:
                st.text(details['content'])
            st.info(details['suggestions'])

def display_history(session_manager):
    """Display analysis history with expandable details."""
    st.subheader("📚 Analysis History")
    
    history = session_manager.get_history()
    if not history:
        st.info("No analysis history yet. Upload a resume to get started!")
        return
    
    for i, entry in enumerate(history):
        # Add modified badge if the entry was user-modified
        title = f"Analysis {i+1} - {entry['timestamp']}"
        if entry.get('is_modified', False):
            title += " 📝 (Modified)"
        if entry.get('is_latest', False):
            title += " ⭐ (Latest)"
            
        with st.expander(title):
            st.text_area("Resume Text", entry['resume_text'], height=100)
            if entry['job_description']:
                st.text_area("Job Description", entry['job_description'], height=100)
            
            results = entry['analysis_results']
            
            st.subheader("📊 Scores")
            display_scores(results['scores'])
            
            if 'keyword_matches' in results:
                st.subheader("🎯 Keywords")
                display_keyword_matches(results['keyword_matches'])
            
            st.subheader("💡 Suggestions")
            st.markdown(results['ai_suggestions'])

def display_insights(session_manager):
    """Display insights learned from previous analyses."""
    st.subheader("🧠 Learning Insights")
    
    insights = session_manager.get_learned_insights()
    
    # Display top keywords
    if insights['top_keywords']:
        st.write("**🔑 Most Successful Keywords:**")
        keywords_html = " ".join([
            f'<span style="background-color: #e6f3ff; padding: 0.2rem 0.5rem; '
            f'border-radius: 1rem; margin: 0.2rem; display: inline-block;">{keyword}</span>'
            for keyword in insights['top_keywords']
        ])
        st.markdown(keywords_html, unsafe_allow_html=True)
    
    # Display common improvements
    if insights['common_improvements']:
        st.write("**📈 Common Areas for Improvement:**")
        for improvement, count in insights['common_improvements'].items():
            st.write(f"- {improvement} *(suggested {count} times)*")
    
    # Display section patterns
    if insights['section_patterns']:
        st.write("**📑 Section Analysis Coverage:**")
        for section, count in insights['section_patterns'].items():
            st.write(f"- {section.title()}: {count} samples analyzed")

def main():
    initialize_gemini()
    session_manager = SessionManager()
    speech_handler = SpeechHandler()
    image_generator = ResumeImageGenerator()
    
    st.set_page_config(
        page_title="AI Resume Enhancer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.sidebar.title("⚙️ Options")
    page = st.sidebar.radio("Navigate", ["Resume Analysis", "History & Insights"])
    
    with st.sidebar:
        st.title("⚙️ Options")
        include_job = st.checkbox("Include Job Description", value=True)
        enable_audio = st.checkbox("Enable Audio Features", value=False)
        enable_image = st.checkbox("Enable Resume Image Generation", value=False)
        
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.rerun()
    
    st.title("🚀 AI Resume Enhancer")
    st.write("Get professional feedback on your resume using advanced AI analysis.")
    
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF/DOCX)",
        type=["pdf", "docx"],
        help="Upload your resume to get detailed feedback and suggestions."
    )
    
    job_description = None
    if include_job:
        job_description = st.text_area(
            "📋 Job Description",
            height=150,
            help="Paste the job description to get targeted feedback and keyword matching."
        )
    
    # Main analysis
    if uploaded_file:
        try:
            # Extract text
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)
            
            # Display resume text
            with st.expander("📄 View Resume Text", expanded=False):
                st.text_area(
                    "Resume Content",
                    value=resume_text,
                    height=300,
                    disabled=True
                )
            
            # Get AI analysis
            if st.button("🧠 Analyze Resume", use_container_width=True):
                with st.spinner("Analyzing your resume..."):
                    try:
                        results = get_ai_feedback(resume_text, job_description)
                        
                        # Display scores
                        st.subheader("� Resume Scores")
                        display_scores(results['scores'])
                        
                        # Display keyword matches if job description was provided
                        if job_description:
                            st.subheader("🎯 Keyword Analysis")
                            display_keyword_matches(results['keyword_matches'])
                        
                        # Display section analysis
                        display_section_analysis(results['section_analysis'])
                        
                        # Display AI suggestions with modification capability
                        st.subheader("💡 AI Recommendations")
                        
                        # Allow user to modify AI suggestions
                        modified_suggestions = st.text_area(
                            "Review and modify the AI suggestions below:",
                            value=results['ai_suggestions'],
                            height=300,
                            help="You can edit these suggestions to better match your needs. The changes will be saved in the analysis history."
                        )
                        
                        # Add buttons for suggestion modification
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("✅ Accept Modifications"):
                                results['ai_suggestions'] = modified_suggestions
                                session_manager.add_to_history(resume_text, results, job_description)
                                st.success("Modifications saved! Your customized feedback has been stored.")
                        with col2:
                            if st.button("🔄 Reset to Original"):
                                st.rerun()
                        with col3:
                            if st.button("📝 Add Custom Note"):
                                custom_note = st.text_area(
                                    "Add your custom note:",
                                    height=100,
                                    help="Add any additional notes or reminders"
                                )
                                if custom_note:
                                    modified_suggestions += f"\n\n📌 Custom Notes:\n{custom_note}"
                                    results['ai_suggestions'] = modified_suggestions
                        
                        # Success message
                        st.success("Analysis complete! Review, modify, and save the feedback above to improve your resume.")
                        
                        # Audio features
                        if enable_audio:
                            st.subheader("🎤 Audio Features")
                            # Text-to-speech for feedback
                            if st.button("🔊 Listen to Feedback"):
                                try:
                                    audio_file = speech_handler.text_to_speech(results['ai_suggestions'])
                                    st.audio(audio_file)
                                    speech_handler.cleanup_audio_file(audio_file)
                                except Exception as e:
                                    st.error(f"Error generating audio: {str(e)}")
                            
                            # Speech input for job description
                            st.write("🎙️ Or describe the job requirements verbally:")
                            audio_file = st.file_uploader("Upload audio file (WAV format)", type=['wav'])
                            if audio_file:
                                try:
                                    text = speech_handler.speech_to_text(audio_file)
                                    st.text_area("Transcribed Text", text, height=100)
                                except Exception as e:
                                    st.error(f"Error processing audio: {str(e)}")
                        
                        # Resume image generation
                        if enable_image:
                            st.subheader("🖼️ Resume Visualization")
                            try:
                                # Convert resume sections to structured data
                                resume_data = {
                                    'summary': results.get('section_analysis', {}).get('summary', {}).get('content', ''),
                                    'experience': results.get('section_analysis', {}).get('experience', {}).get('content', ''),
                                    'education': results.get('section_analysis', {}).get('education', {}).get('content', ''),
                                    'skills': results.get('section_analysis', {}).get('skills', {}).get('content', ''),
                                    'personal_info': {
                                        'name': 'Your Name',  # This should be extracted from the resume
                                        'email': 'email@example.com',
                                        'phone': '(123) 456-7890',
                                        'location': 'City, State'
                                    }
                                }
                                
                                if st.button("📄 Generate Resume Image"):
                                    image_path = image_generator.create_resume_image(resume_data)
                                    with open(image_path, "rb") as file:
                                        st.download_button(
                                            label="⬇️ Download Resume Image",
                                            data=file,
                                            file_name="enhanced_resume.pdf",
                                            mime="application/pdf"
                                        )
                                    image_generator.cleanup_image_file(image_path)
                            except Exception as e:
                                st.error(f"Error generating resume image: {str(e)}")
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Made with ❤️ using Streamlit and Google's Gemini AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()