import streamlit as st
import fitz  # PyMuPDF
import docx
import google.generativeai as genai

# Load API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("📄 Gemini Resume Enhancer")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)
    return text

# Extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join(p.text for p in doc.paragraphs)

# Get AI Suggestions from Gemini
def get_ai_feedback(resume_text):
    model = genai.GenerativeModel('models/gemini-1.5-flash')  # or 'models/gemini-1.0-pro'
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
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("📄 Extracted Resume Text")
    st.text_area("Preview", resume_text, height=300)

    if st.button("🧠 Get Gemini Suggestions"):
        with st.spinner("Thinking..."):
            feedback = get_ai_feedback(resume_text)
            st.success("Done!")
            st.subheader("💡 Gemini Suggestions")
            st.markdown(feedback)


