import streamlit as st
import fitz  # PyMuPDF
import docx
import google.generativeai as genai

# Load API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.set_page_config(page_title="Gemini Resume Enhancer", page_icon="📄", layout="wide")

st.title("Resume Enhancer")
st.write("Upload your resume and get instant feedback from Google's Gemini AI. Improve your resume's grammar, project descriptions, ATS friendliness, and formatting.")
# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

# Extract text from PDF
@st.cache_data
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

# Extract text from DOCX
@st.cache_data
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join(p.text for p in doc.paragraphs)

# Get AI Suggestions from Gemini
@st.cache_data
def get_ai_feedback(resume_text):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
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


