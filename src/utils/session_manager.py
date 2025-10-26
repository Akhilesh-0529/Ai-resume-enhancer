import streamlit as st
from typing import Dict, List, Optional
from datetime import datetime

class SessionManager:
    def __init__(self):
        if 'resume_history' not in st.session_state:
            st.session_state.resume_history = []
        if 'learning_data' not in st.session_state:
            st.session_state.learning_data = {
                'successful_keywords': set(),
                'common_improvements': {},
                'section_patterns': {},
                'industry_specific_terms': set()
            }

    def add_to_history(self, 
                      resume_text: str, 
                      analysis_results: Dict,
                      job_description: Optional[str] = None,
                      is_modified: bool = False) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        history_entry = {
            'timestamp': timestamp,
            'resume_text': resume_text,
            'job_description': job_description,
            'analysis_results': analysis_results,
            'is_modified': is_modified
        }
        
        # If there are previous entries for this resume, mark this as latest
        history_entry['is_latest'] = True
        for prev_entry in st.session_state.resume_history:
            if prev_entry['resume_text'] == resume_text:
                prev_entry['is_latest'] = False
        
        st.session_state.resume_history.append(history_entry)
        self._learn_from_analysis(analysis_results)

    def get_history(self) -> List[Dict]:
        return st.session_state.resume_history

    def clear_history(self) -> None:
        st.session_state.resume_history = []

    def _learn_from_analysis(self, analysis_results: Dict) -> None:
        if 'keyword_matches' in analysis_results:
            matched_keywords = analysis_results['keyword_matches'].get('matched', [])
            st.session_state.learning_data['successful_keywords'].update(matched_keywords)

        if 'ai_suggestions' in analysis_results:
            suggestions = analysis_results['ai_suggestions']
            for improvement in self._extract_improvements(suggestions):
                if improvement in st.session_state.learning_data['common_improvements']:
                    st.session_state.learning_data['common_improvements'][improvement] += 1
                else:
                    st.session_state.learning_data['common_improvements'][improvement] = 1

        if 'section_analysis' in analysis_results:
            for section, details in analysis_results['section_analysis'].items():
                if section not in st.session_state.learning_data['section_patterns']:
                    st.session_state.learning_data['section_patterns'][section] = []
                st.session_state.learning_data['section_patterns'][section].append(
                    details.get('content', '')
                )

    def _extract_improvements(self, suggestions: str) -> List[str]:
        improvements = []
        for line in suggestions.split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('•'):
                improvements.append(line.strip()[2:].strip())
        return improvements

    def get_learned_insights(self) -> Dict:
        return {
            'top_keywords': list(st.session_state.learning_data['successful_keywords']),
            'common_improvements': dict(sorted(
                st.session_state.learning_data['common_improvements'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]),
            'section_patterns': {
                section: len(patterns)
                for section, patterns in st.session_state.learning_data['section_patterns'].items()
            }
        }

    def get_personalized_suggestions(self, resume_text: str) -> List[str]:
        suggestions = []
        
        # Check for successful keywords
        if st.session_state.learning_data['successful_keywords']:
            missing_keywords = [
                keyword for keyword in st.session_state.learning_data['successful_keywords']
                if keyword.lower() not in resume_text.lower()
            ]
            if missing_keywords:
                suggestions.append(
                    f"Consider adding these successful keywords: {', '.join(missing_keywords)}"
                )

        # Suggest common improvements
        top_improvements = dict(sorted(
            st.session_state.learning_data['common_improvements'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3])
        
        if top_improvements:
            suggestions.append("Common areas for improvement:")
            for improvement, count in top_improvements.items():
                suggestions.append(f"- {improvement}")

        return suggestions