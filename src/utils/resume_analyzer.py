import re
from typing import Dict, List, Tuple

def calculate_keyword_match(resume_text: str, job_description: str) -> Tuple[List[str], List[str]]:
    job_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)
    
    matched = list(set(job_keywords) & set(resume_keywords))
    missing = list(set(job_keywords) - set(resume_keywords))
    
    return matched, missing

def calculate_resume_scores(resume_text: str, job_description: str = None) -> Dict[str, float]:
    scores = {
        'readability': calculate_readability_score(resume_text),
        'formatting': calculate_formatting_score(resume_text),
        'content': calculate_content_score(resume_text),
    }
    
    if job_description:
        matched, missing = calculate_keyword_match(resume_text, job_description)
        scores['keyword_match'] = (len(matched) / (len(matched) + len(missing))) * 100
        
    return scores

def extract_keywords(text: str) -> List[str]:
    technical_keywords = [
        'python', 'java', 'javascript', 'react', 'node', 'aws', 'docker',
        'kubernetes', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai',
        'data science', 'cloud', 'devops', 'frontend', 'backend', 'fullstack'
    ]
    
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical', 'project management', 'time management', 'collaborative'
    ]
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return [word for word in words if word in technical_keywords + soft_skills]

def analyze_resume_sections(resume_text: str) -> Dict[str, Dict[str, str]]:
    sections = {
        'summary': {
            'content': extract_section(resume_text, 'summary'),
            'suggestions': analyze_summary_section(extract_section(resume_text, 'summary'))
        },
        'experience': {
            'content': extract_section(resume_text, 'experience'),
            'suggestions': analyze_experience_section(extract_section(resume_text, 'experience'))
        },
        'education': {
            'content': extract_section(resume_text, 'education'),
            'suggestions': analyze_education_section(extract_section(resume_text, 'education'))
        },
        'skills': {
            'content': extract_section(resume_text, 'skills'),
            'suggestions': analyze_skills_section(extract_section(resume_text, 'skills'))
        }
    }
    return sections

def extract_section(text: str, section_name: str) -> str:
    return ""

def calculate_readability_score(text: str) -> float:
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    readability = 100 - (avg_sentence_length - 15) * 2
    return max(0, min(100, readability))

def calculate_formatting_score(text: str) -> float:
    return 85.0

def calculate_content_score(text: str) -> float:
    return 90.0

def analyze_summary_section(text: str) -> str:
    return "Make sure to include your years of experience and key achievements."

def analyze_experience_section(text: str) -> str:
    return "Use action verbs and quantify achievements with metrics."

def analyze_education_section(text: str) -> str:
    return "Include relevant coursework and academic achievements."

def analyze_skills_section(text: str) -> str:
    return "Group skills by category and highlight proficiency levels."