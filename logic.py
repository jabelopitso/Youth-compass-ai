import re
from collections import Counter

def analyze_responses(responses):
    """Analyze user responses and return interest scores"""
    keywords = {
        'technology': ['computer', 'coding', 'programming', 'tech', 'software', 'digital'],
        'creative': ['art', 'design', 'music', 'creative', 'drawing', 'writing'],
        'science': ['science', 'research', 'experiment', 'biology', 'chemistry', 'physics'],
        'business': ['business', 'management', 'leadership', 'entrepreneur', 'sales'],
        'helping': ['help', 'people', 'community', 'social', 'care', 'support']
    }
    
    scores = {category: 0 for category in keywords}
    
    for response in responses:
        text = response.lower()
        for category, words in keywords.items():
            for word in words:
                scores[category] += text.count(word)
    
    return scores

def generate_career_path(scores):
    """Generate career recommendations based on scores"""
    top_interest = max(scores, key=scores.get)
    
    paths = {
        'technology': {
            'title': 'Technology & Programming',
            'careers': ['Software Developer', 'Data Scientist', 'Cybersecurity Analyst'],
            'next_steps': ['Learn Python or JavaScript', 'Build coding projects', 'Join tech communities']
        },
        'creative': {
            'title': 'Creative Arts & Design',
            'careers': ['Graphic Designer', 'Content Creator', 'UX/UI Designer'],
            'next_steps': ['Build a portfolio', 'Learn design software', 'Take art classes']
        },
        'science': {
            'title': 'Science & Research',
            'careers': ['Research Scientist', 'Lab Technician', 'Environmental Scientist'],
            'next_steps': ['Excel in STEM subjects', 'Join science clubs', 'Seek internships']
        },
        'business': {
            'title': 'Business & Leadership',
            'careers': ['Business Analyst', 'Project Manager', 'Marketing Specialist'],
            'next_steps': ['Develop leadership skills', 'Learn business basics', 'Network with professionals']
        },
        'helping': {
            'title': 'Social Impact & Care',
            'careers': ['Social Worker', 'Teacher', 'Healthcare Professional'],
            'next_steps': ['Volunteer in community', 'Develop communication skills', 'Shadow professionals']
        }
    }
    
    return paths.get(top_interest, paths['technology'])