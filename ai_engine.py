# Core AI Engine: The Contextual Profiler
import json
import re
from datetime import datetime

class ContextualProfiler:
    """AI engine that creates dynamic user profiles and learns from outcomes"""
    
    def __init__(self):
        self.skills_keywords = {
            'problem_solving': ['fix', 'solve', 'repair', 'figure out', 'troubleshoot'],
            'communication': ['talk', 'explain', 'teach', 'help others', 'negotiate'],
            'digital_literacy': ['phone', 'computer', 'online', 'app', 'social media'],
            'leadership': ['organize', 'lead', 'manage', 'coordinate', 'responsible'],
            'creativity': ['design', 'create', 'art', 'music', 'build', 'make'],
            'sales': ['sell', 'convince', 'persuade', 'market', 'customer']
        }
        
        # Reinforcement Learning data (simulated)
        self.pathway_success_rates = {
            'digital': {'attempts': 100, 'successes': 65},
            'green': {'attempts': 80, 'successes': 44},
            'entrepreneurship': {'attempts': 120, 'successes': 84}
        }
    
    def extract_transferable_skills(self, responses):
        """NLP analysis to identify transferable skills from user responses"""
        skills_profile = {skill: 0 for skill in self.skills_keywords}
        
        for response in responses:
            text = response.lower()
            for skill, keywords in self.skills_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        skills_profile[skill] += 1
        
        # Normalize scores
        max_score = max(skills_profile.values()) if max(skills_profile.values()) > 0 else 1
        return {skill: round(score/max_score * 100) for skill, score in skills_profile.items()}
    
    def calculate_dynamic_success_rate(self, pathway):
        """Calculate real-time success rate based on feedback"""
        data = self.pathway_success_rates[pathway]
        return round((data['successes'] / data['attempts']) * 100)
    
    def update_success_rate(self, pathway, success=True):
        """Update pathway success rate based on user feedback"""
        self.pathway_success_rates[pathway]['attempts'] += 1
        if success:
            self.pathway_success_rates[pathway]['successes'] += 1

class EconomicChoicesAI:
    """AI for educational and economic opportunity analysis"""
    
    def __init__(self):
        self.course_database = {
            'digital': [
                {'name': 'Google Data Analytics Certificate', 'cost': 0, 'duration': '6 months', 'roi_score': 85},
                {'name': 'TVET IT Fundamentals', 'cost': 5000, 'duration': '1 year', 'roi_score': 75},
                {'name': 'Coursera Python Programming', 'cost': 500, 'duration': '3 months', 'roi_score': 80}
            ],
            'green': [
                {'name': 'Solar PV Installation (TVET)', 'cost': 8000, 'duration': '6 months', 'roi_score': 70},
                {'name': 'EWSETA Green Skills', 'cost': 0, 'duration': '4 months', 'roi_score': 65},
                {'name': 'Renewable Energy Certificate', 'cost': 3000, 'duration': '3 months', 'roi_score': 60}
            ],
            'entrepreneurship': [
                {'name': 'MANCOSA Business Management', 'cost': 0, 'duration': '2 months', 'roi_score': 75},
                {'name': 'SEDA Business Development', 'cost': 0, 'duration': '1 month', 'roi_score': 70},
                {'name': 'Digital Marketing Bootcamp', 'cost': 2000, 'duration': '6 weeks', 'roi_score': 80}
            ]
        }
        
        self.hidden_opportunities = [
            {'title': 'Mobile Repair Technician', 'location': 'Township', 'source': 'Community Network'},
            {'title': 'Solar Panel Installer', 'location': 'Rural Areas', 'source': 'Government Tender'},
            {'title': 'Digital Marketing Assistant', 'location': 'Local SMME', 'source': 'Social Media'}
        ]
    
    def rank_courses_by_roi(self, pathway, user_location='general'):
        """Rank courses by ROI considering cost, proximity, and job market value"""
        courses = self.course_database.get(pathway, [])
        # Sort by ROI score (higher is better) and cost (lower is better)
        return sorted(courses, key=lambda x: (x['roi_score'], -x['cost']), reverse=True)
    
    def find_hidden_opportunities(self, skills_profile):
        """Scan for non-traditional job opportunities"""
        # Simple matching based on skills
        opportunities = []
        for opp in self.hidden_opportunities:
            opportunities.append(opp)
        return opportunities[:3]  # Return top 3

class SupportAI:
    """AI for emotional support and peer matching"""
    
    def __init__(self):
        self.motivational_responses = [
            "Your journey is unique and valuable. Every step forward counts.",
            "Remember, many successful people started exactly where you are now.",
            "Your skills and experiences matter more than formal qualifications.",
            "The South African economy needs young people like you to drive change."
        ]
        
        self.peer_matching_data = [
            {'interests': ['digital', 'entrepreneurship'], 'location': 'Gauteng', 'stage': 'learning'},
            {'interests': ['green', 'hands-on'], 'location': 'Western Cape', 'stage': 'job-seeking'},
            {'interests': ['business', 'community'], 'location': 'KwaZulu-Natal', 'stage': 'starting-business'}
        ]
    
    def get_motivational_message(self, user_context='general'):
        """Provide contextual motivational support"""
        import random
        return random.choice(self.motivational_responses)
    
    def find_peer_matches(self, user_profile, user_location='general'):
        """Match users with similar career paths and challenges"""
        matches = []
        for peer in self.peer_matching_data:
            # Simple matching logic
            matches.append({
                'match_reason': f"Similar interests in {', '.join(peer['interests'])}",
                'location': peer['location'],
                'stage': peer['stage']
            })
        return matches[:2]  # Return top 2 matches