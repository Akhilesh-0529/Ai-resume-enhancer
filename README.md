# 🚀 AI Resume Enhancer

An intelligent resume enhancement tool powered by Google'\''s Gemini AI that helps you create ATS-friendly resumes with professional feedback and suggestions.

## ✨ Features

- **Smart Text Extraction** - Automatically extract text from PDF and DOCX resumes
- **AI-Powered Analysis** - Get professional feedback using Google'\''s Gemini AI
- **Grammar Enhancement** - Improve clarity and professionalism of your writing
- **ATS Optimization** - Make your resume more friendly to Applicant Tracking Systems
- **Project Descriptions** - Get suggestions to make your achievements stand out
- **Format Improvement** - Receive formatting recommendations for better readability
- **User-Friendly Interface** - Clean and intuitive Streamlit-based web interface

## 🛠️ Tech Stack

- **Python 3.7+** - Modern Python for robust development
- **Streamlit** - Beautiful web interface
- **Google Generative AI** - Gemini 2.5 Flash-Lite model for AI analysis
- **PyMuPDF** - PDF processing and text extraction
- **python-docx** - DOCX file handling
- **pytest** - Comprehensive testing framework

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Akhilesh-0529/Ai-resume-enhancer.git
cd Ai-resume-enhancer
```

2. **Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure Gemini API:**
   - Create `.streamlit/secrets.toml`
   - Add your API key: `GEMINI_API_KEY = "your-api-key-here"`

## 🚀 Usage

1. **Start the application:**
```bash
streamlit run src/app.py
```

2. **Access the web interface:**
   - Open your browser
   - Go to `http://localhost:8501`

3. **Enhance your resume:**
   - Upload your resume (PDF/DOCX)
   - Click "Get Gemini Suggestions"
   - Review AI-powered feedback
   - Make improvements based on suggestions

## 📁 Project Structure

```
.
├── src/                    # Source code directory
│   ├── app.py             # Main Streamlit application
│   └── utils/             # Utility modules
│       ├── text_extractor.py  # PDF/DOCX processing
│       └── ai_feedback.py     # Gemini AI integration
├── tests/                 # Test directory
│   └── test_text_extraction.py
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
├── README.md            # Project documentation
├── pyproject.toml       # Python tool configurations
└── requirements.txt     # Project dependencies
```

## ✅ Development

- **Code Style:** Project uses Black formatter and isort
- **Testing:** Run tests with `pytest`
- **Type Checking:** Python type hints included
- **Documentation:** Docstrings and comments for clarity

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -am '\''Add amazing feature'\'')
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👤 Author

**Akhilesh**
- GitHub: [@Akhilesh-0529](https://github.com/Akhilesh-0529)

---

⭐ Star this repo if you find it helpful!
