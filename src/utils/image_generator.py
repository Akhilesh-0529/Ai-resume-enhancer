import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tempfile

class ResumeImageGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            leading=14,
            spaceAfter=10
        )

    def create_resume_image(self, resume_data):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as fp:
                pdf_path = fp.name
            
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            content = []
            if 'personal_info' in resume_data:
                name_style = ParagraphStyle(
                    'NameStyle',
                    parent=self.styles['Heading1'],
                    fontSize=24,
                    spaceAfter=20
                )
                content.append(Paragraph(resume_data['personal_info']['name'], name_style))
                
                contact_text = (
                    f"{resume_data['personal_info'].get('email', '')}<br/>"
                    f"{resume_data['personal_info'].get('phone', '')}<br/>"
                    f"{resume_data['personal_info'].get('location', '')}"
                )
                content.append(Paragraph(contact_text, self.custom_style))
                content.append(Spacer(1, 20))

            sections = ['summary', 'experience', 'education', 'skills']
            for section in sections:
                if section in resume_data:
                    content.append(Paragraph(
                        section.upper(),
                        self.styles['Heading2']
                    ))
                    content.append(Spacer(1, 10))
                    if isinstance(resume_data[section], list):
                        for item in resume_data[section]:
                            if isinstance(item, dict):
                                for key, value in item.items():
                                    content.append(Paragraph(
                                        f"<b>{key}:</b> {value}",
                                        self.custom_style
                                    ))
                            else:
                                content.append(Paragraph(str(item), self.custom_style))
                    else:
                        content.append(Paragraph(str(resume_data[section]), self.custom_style))
                    content.append(Spacer(1, 15))

            doc.build(content)
            return pdf_path

        except Exception as e:
            raise Exception(f"Error generating resume image: {str(e)}")

    def cleanup_image_file(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up image file: {str(e)}")