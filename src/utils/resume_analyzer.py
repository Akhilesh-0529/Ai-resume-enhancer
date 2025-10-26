"""
Resume analysis utilities for scoring and detailed feedback.
"""
import re
from typing import Dict, List, Tuple

def calculate_keyword_match(resume_text: str, job_description: str) -> Tuple[List[str], List[str]]:
    """
    Find matching and missing keywords between resume and job description.
    
    Args:
        resume_text: The text content of the resume
        job_description: The job description text
        
    Returns:
        Tuple containing lists of matched and missing keywords
    """
    # Extract important keywords from job description
    job_keywords = extract_keywords(job_description)
    resume_keywords = extract_keywords(resume_text)
    
    matched = list(set(job_keywords) & set(resume_keywords))
    missing = list(set(job_keywords) - set(resume_keywords))
    
    return matched, missing

def calculate_resume_scores(resume_text: str, job_description: str = None) -> Dict[str, float]:
    """
    Calculate various scores for the resume.
    
    Args:
        resume_text: The text content of the resume
        job_description: Optional job description for matching
        
    Returns:
        Dictionary containing different score metrics
    """
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
    """Extract important keywords from text."""
    # Common technical skills and job-related terms
    technical_keywords = [
        'python', 'java', 'javascript', 'react', 'node', 'aws', 'docker',
        'kubernetes', 'ci/cd', 'agile', 'scrum', 'machine learning', 'ai',
        'data science', 'cloud', 'devops', 'frontend', 'backend', 'fullstack'
    ]
    
    # Common soft skills
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical', 'project management', 'time management', 'collaborative'
    ]
    
    # Find all words that match our keywords
    words = set(re.findall(r'\b\w+\b', text.lower()))
    return [word for word in words if word in technical_keywords + soft_skills]

def analyze_resume_sections(resume_text: str) -> Dict[str, Dict[str, str]]:
    """
    Analyze different sections of the resume.
    
    Args:
        resume_text: The text content of the resume
        
    Returns:
        Dictionary containing analysis for each section
    """
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
    """Extract content of a specific section from resume text."""
    # Implementation would look for section headers and extract content
    return ""  # Placeholder

def calculate_readability_score(text: str) -> float:
    """Calculate readability score based on sentence structure and word choice."""
    # Simple implementation based on average sentence length and word complexity
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    readability = 100 - (avg_sentence_length - 15) * 2  # Penalize very long sentences
    return max(0, min(100, readability))

def calculate_formatting_score(text: str) -> float:
    """Calculate formatting score based on structure and consistency."""
    # Check for consistent spacing, bullet points, section headers
    return 85.0  # Placeholder

def calculate_content_score(text: str) -> float:
    """Calculate content quality score based on various factors."""
    # Check for action verbs, quantifiable achievements, etc.
    return 90.0  # Placeholder

def analyze_summary_section(text: str) -> str:
    """Analyze and provide suggestions for summary section."""
    return "Make sure to include your years of experience and key achievements."

def analyze_experience_section(text: str) -> str:
    """Analyze and provide suggestions for experience section."""
    return "Use action verbs and quantify achievements with metrics."

def analyze_education_section(text: str) -> str:
    """Analyze and provide suggestions for education section."""
    return "Include relevant coursework and academic achievements."

def analyze_skills_section(text: str) -> str:
    """Analyze and provide suggestions for skills section."""
    return "Group skills by category and highlight proficiency levels."