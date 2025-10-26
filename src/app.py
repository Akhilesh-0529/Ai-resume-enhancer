"""
Main Streamlit application for Resume Enhancement with advanced analysis and session management.
"""
import streamlit as st
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.ai_feedback import initialize_gemini, get_ai_feedback
from utils.session_manager import SessionManager

def display_scores(scores):
    """Display resume scores in a visually appealing way."""
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
        with st.expander(f"Analysis {i+1} - {entry['timestamp']}"):
            st.text_area("Resume Text", entry['resume_text'], height=100)
            if entry['job_description']:
                st.text_area("Job Description", entry['job_description'], height=100)
            
            results = entry['analysis_results']
            
            # Display scores
            st.subheader("📊 Scores")
            display_scores(results['scores'])
            
            # Display keyword matches
            if 'keyword_matches' in results:
                st.subheader("🎯 Keywords")
                display_keyword_matches(results['keyword_matches'])
            
            # Display AI suggestions
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
    # Initialize Gemini and Session Manager
    initialize_gemini()
    session_manager = SessionManager()
    
    # Set page config
    st.set_page_config(
        page_title="AI Resume Enhancer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    st.sidebar.title("⚙️ Options")
    page = st.sidebar.radio("Navigate", ["Resume Analysis", "History & Insights"])
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Options")
        include_job = st.checkbox("Include Job Description", value=True)
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.rerun()
    
    # Main content
    st.title("🚀 AI Resume Enhancer")
    st.write("Get professional feedback on your resume using advanced AI analysis.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF/DOCX)",
        type=["pdf", "docx"],
        help="Upload your resume to get detailed feedback and suggestions."
    )
    
    # Job description input
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
                        
                        # Display AI suggestions
                        st.subheader("💡 AI Recommendations")
                        st.markdown(results['ai_suggestions'])
                        
                        # Success message
                        st.success("Analysis complete! Review the feedback above to improve your resume.")
                        
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