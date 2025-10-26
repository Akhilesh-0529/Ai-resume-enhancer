"""
Main Streamlit application for Resume Enhancement with advanced analysis.
"""
import streamlit as st
from utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from utils.ai_feedback import initialize_gemini, get_ai_feedback

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

def main():
    # Initialize Gemini
    initialize_gemini()
    
    # Set page config
    st.set_page_config(
        page_title="AI Resume Enhancer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
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