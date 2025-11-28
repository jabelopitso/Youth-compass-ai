from ai_engine import ContextualProfiler, EconomicChoicesAI, SupportAI

# Initialize AI engines
contextual_profiler = ContextualProfiler()
economic_ai = EconomicChoicesAI()
support_ai = SupportAI()

# Enhanced pathway keywords
PATHWAY_KEYWORDS = {
    'digital': ['organizing', 'data', 'computer', 'files', 'numbers', 'tracking', 'online', 'learn', 'study', 'certificate', 'phone', 'app'],
    'green': ['fixing', 'building', 'hands', 'tools', 'repairing', 'outdoors', 'sun', 'physical', 'solar', 'environment'],
    'entrepreneurship': ['selling', 'buy and sell', 'resell', 'service', 'start a business', 'talking', 'persuading', 'negotiating', 'money', 'profit'],
}

# Dynamic pathways data with AI integration
PATHWAYS_DATA = {
    'digital': {
        'name': 'The Digital Economy Path',
        'description': 'Transform your digital skills into economic opportunities',
        'base_steps': [
            "1. Foundational Skill: Enroll in the free Google Data Analytics Certificate (via Coursera/Grow with Google).",
            "2. Funding/Location: Search for an accredited TVET College offering IT/Computer Science near your location.",
            "3. Next Step: Apply for a SEDA/Services SETA micro-internship (Simulated)."
        ],
        'initial_success_rate': 65
    },
    'green': {
        'name': 'The Green Economy Path',
        'description': 'Build a sustainable future through green skills and renewable energy',
        'base_steps': [
            "1. Foundational Skill: Enroll at the nearest TVET College for an Electrical/Mechanical NCV course (focus on Solar PV).",
            "2. Funding/Location: Apply immediately for an NSFAS bursary (R350k family income max).",
            "3. Next Step: Search for Energy & Water SETA (EWSETA) learnerships."
        ],
        'initial_success_rate': 55
    },
    'entrepreneurship': {
        'name': 'The Entrepreneurship Path',
        'description': 'Create your own opportunities and build local economic value',
        'base_steps': [
            "1. Foundational Skill: Take the free MANCOSA skillME course on Business Management/Digital Marketing.",
            "2. Funding/Location: Identify local business support services in your district (e.g., SEDA, local incubator).",
            "3. Next Step: Use the platform's Informal Sector Financial Tool (Simulated) to build a credit history."
        ],
        'initial_success_rate': 70
    },
}

def analyze_profile(answers):
    """Enhanced AI analysis using contextual profiler and economic AI"""
    # Basic keyword scoring
    scores = {'digital': 0, 'green': 0, 'entrepreneurship': 0}
    
    for answer in answers:
        answer_lower = answer.lower()
        for pathway, keywords in PATHWAY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in answer_lower:
                    scores[pathway] += 1
    
    # AI Enhancement: Extract transferable skills
    skills_profile = contextual_profiler.extract_transferable_skills(answers)
    
    # Determine winning pathway
    if not scores or max(scores.values()) == 0:
        winning_pathway = 'entrepreneurship'
    else:
        winning_pathway = max(scores, key=scores.get)
    
    # Get dynamic success rate
    dynamic_success_rate = contextual_profiler.calculate_dynamic_success_rate(winning_pathway)
    
    # Get personalized course recommendations
    recommended_courses = economic_ai.rank_courses_by_roi(winning_pathway)
    
    # Get hidden opportunities
    hidden_opps = economic_ai.find_hidden_opportunities(skills_profile)
    
    # Get motivational support
    motivation = support_ai.get_motivational_message()
    
    # Get peer matches
    peer_matches = support_ai.find_peer_matches(skills_profile)
    
    # Enhanced pathway data
    pathway_data = PATHWAYS_DATA[winning_pathway].copy()
    pathway_data['success_rate'] = dynamic_success_rate
    pathway_data['skills_profile'] = skills_profile
    pathway_data['recommended_courses'] = recommended_courses[:3]
    pathway_data['hidden_opportunities'] = hidden_opps
    pathway_data['motivation'] = motivation
    pathway_data['peer_matches'] = peer_matches
    pathway_data['steps'] = pathway_data['base_steps']  # Keep original steps
    
    return pathway_data, scores

def update_pathway_success(pathway, success=True):
    """Update pathway success rate based on user feedback (Reinforcement Learning)"""
    contextual_profiler.update_success_rate(pathway, success)
    return contextual_profiler.calculate_dynamic_success_rate(pathway)

# Legacy functions for compatibility
def analyze_responses(responses):
    """Legacy function - redirects to analyze_profile"""
    pathway_data, scores = analyze_profile(responses)
    return scores

def generate_career_path(scores):
    """Legacy function - generates path from scores"""
    if not scores or max(scores.values()) == 0:
        winning_pathway = 'entrepreneurship'
    else:
        winning_pathway = max(scores, key=scores.get)
    
    pathway_data = PATHWAYS_DATA[winning_pathway]
    return {
        'title': pathway_data['name'],
        'careers': pathway_data['steps'],
        'next_steps': [f"Success Rate: {pathway_data['initial_success_rate']}%"]
    }