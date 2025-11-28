from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = 'youth_compass_flow_2024'

# User Flow Data Structures
USER_LEVELS = ['Matric', 'Some Tertiary', 'Diploma/Degree', 'No Formal Education']

PROVINCES = ['Gauteng', 'Western Cape', 'KwaZulu-Natal', 'Eastern Cape', 'Limpopo', 'Mpumalanga', 'North West', 'Free State', 'Northern Cape']

# AI Coach Questions for First Chat
COACH_QUESTIONS = [
    "What activities make you feel energized and excited?",
    "What are you naturally good at, even if it's just small things?",
    "If you could solve one problem in your community, what would it be?",
    "What do you do in your free time that you really enjoy?",
    "What kind of work environment appeals to you most?"
]

# Skills Detection Keywords
SKILLS_KEYWORDS = {
    'communication': ['talking', 'explaining', 'helping others', 'teaching', 'presenting'],
    'problem_solving': ['fixing', 'solving', 'figuring out', 'troubleshooting', 'organizing'],
    'creativity': ['drawing', 'designing', 'creating', 'art', 'music', 'writing'],
    'technology': ['computer', 'phone', 'apps', 'internet', 'social media', 'coding'],
    'leadership': ['leading', 'organizing', 'managing', 'coordinating', 'responsible'],
    'analytical': ['numbers', 'data', 'calculating', 'planning', 'researching'],
    'hands_on': ['building', 'making', 'crafting', 'repairing', 'physical work'],
    'sales': ['selling', 'convincing', 'persuading', 'negotiating', 'marketing']
}

# Career Pathways Database
CAREER_PATHWAYS = {
    'digital_economy': {
        'name': 'Digital Economy Path',
        'icon': '💻',
        'description': 'Technology and digital skills for the modern economy',
        'careers': ['Software Developer', 'Data Analyst', 'Digital Marketer', 'IT Support'],
        'courses': [
            {'name': 'Google Data Analytics Certificate', 'provider': 'Coursera', 'cost': 'Free', 'duration': '6 months'},
            {'name': 'Python Programming', 'provider': 'FreeCodeCamp', 'cost': 'Free', 'duration': '3 months'},
            {'name': 'Digital Marketing', 'provider': 'Google Skillshop', 'cost': 'Free', 'duration': '2 months'}
        ],
        'success_rate': 72
    },
    'green_economy': {
        'name': 'Green Economy Path',
        'icon': '🌱',
        'description': 'Sustainable energy and environmental careers',
        'careers': ['Solar Technician', 'Environmental Consultant', 'Renewable Energy Specialist'],
        'courses': [
            {'name': 'Solar PV Installation', 'provider': 'TVET College', 'cost': 'R8000', 'duration': '6 months'},
            {'name': 'Environmental Management', 'provider': 'UNISA', 'cost': 'R15000', 'duration': '1 year'},
            {'name': 'Green Building', 'provider': 'GBCSA', 'cost': 'R5000', 'duration': '3 months'}
        ],
        'success_rate': 68
    },
    'entrepreneurship': {
        'name': 'Entrepreneurship Path',
        'icon': '🚀',
        'description': 'Start your own business and create opportunities',
        'careers': ['Business Owner', 'Freelancer', 'Consultant', 'E-commerce Seller'],
        'courses': [
            {'name': 'Business Fundamentals', 'provider': 'SEDA', 'cost': 'Free', 'duration': '2 months'},
            {'name': 'Financial Management', 'provider': 'MANCOSA', 'cost': 'Free', 'duration': '6 weeks'},
            {'name': 'Digital Marketing', 'provider': 'Facebook Blueprint', 'cost': 'Free', 'duration': '4 weeks'}
        ],
        'success_rate': 75
    },
    'creative_industries': {
        'name': 'Creative Industries Path',
        'icon': '🎨',
        'description': 'Arts, design, and creative expression careers',
        'careers': ['Graphic Designer', 'Content Creator', 'Photographer', 'Writer'],
        'courses': [
            {'name': 'Graphic Design', 'provider': 'Adobe', 'cost': 'R500/month', 'duration': '4 months'},
            {'name': 'Photography', 'provider': 'Local Studio', 'cost': 'R3000', 'duration': '2 months'},
            {'name': 'Content Creation', 'provider': 'YouTube Creator Academy', 'cost': 'Free', 'duration': '6 weeks'}
        ],
        'success_rate': 65
    }
}

# Hidden Job Market Sources (Simulated)
HIDDEN_JOBS = [
    {'title': 'Social Media Assistant', 'company': 'Local Restaurant', 'location': 'Johannesburg', 'source': 'Facebook Page'},
    {'title': 'Delivery Driver', 'company': 'Pharmacy Chain', 'location': 'Cape Town', 'source': 'Community Notice'},
    {'title': 'Tutor', 'company': 'Private Family', 'location': 'Durban', 'source': 'WhatsApp Group'},
    {'title': 'Event Helper', 'company': 'Wedding Planner', 'location': 'Pretoria', 'source': 'Instagram Story'},
    {'title': 'Shop Assistant', 'company': 'Spaza Shop', 'location': 'Soweto', 'source': 'Community Board'}
]

# Motivational Messages
MOTIVATIONAL_MESSAGES = [
    "Your potential is unlimited. Every expert was once a beginner.",
    "South Africa needs your unique talents and perspective.",
    "Small consistent actions lead to big transformations.",
    "Your dreams are valid and achievable with the right plan.",
    "Every challenge is an opportunity to grow stronger."
]

def analyze_skills_from_responses(responses):
    """Extract skills from user responses using NLP"""
    detected_skills = {}
    
    for response in responses:
        response_lower = response.lower()
        for skill, keywords in SKILLS_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in response_lower)
            detected_skills[skill] = detected_skills.get(skill, 0) + score
    
    # Normalize scores
    max_score = max(detected_skills.values()) if detected_skills.values() else 1
    normalized_skills = {skill: round((score / max_score) * 100) for skill, score in detected_skills.items()}
    
    return normalized_skills

def recommend_pathway(skills_profile, user_data):
    """AI Pathway Engine - Recommend best career path"""
    # Score each pathway based on user skills
    pathway_scores = {}
    
    for pathway_id, pathway in CAREER_PATHWAYS.items():
        score = 0
        
        # Technology pathway scoring
        if pathway_id == 'digital_economy':
            score += skills_profile.get('technology', 0) * 2
            score += skills_profile.get('analytical', 0) * 1.5
            score += skills_profile.get('problem_solving', 0) * 1.5
        
        # Green economy scoring
        elif pathway_id == 'green_economy':
            score += skills_profile.get('hands_on', 0) * 2
            score += skills_profile.get('problem_solving', 0) * 1.5
            score += skills_profile.get('analytical', 0) * 1
        
        # Entrepreneurship scoring
        elif pathway_id == 'entrepreneurship':
            score += skills_profile.get('leadership', 0) * 2
            score += skills_profile.get('sales', 0) * 2
            score += skills_profile.get('communication', 0) * 1.5
        
        # Creative industries scoring
        elif pathway_id == 'creative_industries':
            score += skills_profile.get('creativity', 0) * 2
            score += skills_profile.get('communication', 0) * 1.5
            score += skills_profile.get('technology', 0) * 1
        
        pathway_scores[pathway_id] = score
    
    # Return top pathway
    best_pathway_id = max(pathway_scores, key=pathway_scores.get)
    return best_pathway_id, CAREER_PATHWAYS[best_pathway_id]

def find_hidden_opportunities(user_location, skills_profile):
    """Hidden Job Market Scanner"""
    # Filter jobs by location and skills
    relevant_jobs = []
    
    for job in HIDDEN_JOBS:
        # Simple location matching
        if user_location.lower() in job['location'].lower() or job['location'] == 'Multiple':
            relevant_jobs.append(job)
    
    # If no location matches, return random selection
    if not relevant_jobs:
        relevant_jobs = random.sample(HIDDEN_JOBS, min(3, len(HIDDEN_JOBS)))
    
    return relevant_jobs[:3]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    """Quick Sign-Up Process"""
    data = request.json
    
    session['user'] = {
        'name': data.get('name'),
        'age': data.get('age'),
        'location': data.get('location'),
        'education_level': data.get('education_level'),
        'signup_date': datetime.now().isoformat()
    }
    
    return jsonify({'success': True, 'message': f"Welcome {data.get('name')}! Let's start your journey."})

@app.route('/coach_chat', methods=['POST'])
def coach_chat():
    """First Chat with AI Coach"""
    data = request.json
    responses = data.get('responses', [])
    
    if not responses:
        return jsonify({'questions': COACH_QUESTIONS})
    
    # Analyze responses and generate skills profile
    skills_profile = analyze_skills_from_responses(responses)
    
    # Store in session
    session['skills_profile'] = skills_profile
    session['coach_responses'] = responses
    
    return jsonify({
        'skills_profile': skills_profile,
        'message': "Great! I've analyzed your responses and created your Skills Passport."
    })

@app.route('/generate_pathway', methods=['POST'])
def generate_pathway():
    """AI Pathway Engine Analysis"""
    if 'skills_profile' not in session:
        return jsonify({'error': 'Complete skills assessment first'}), 400
    
    skills_profile = session['skills_profile']
    user_data = session.get('user', {})
    
    # Get recommended pathway
    pathway_id, pathway_data = recommend_pathway(skills_profile, user_data)
    
    # Store pathway in session
    session['recommended_pathway'] = {
        'id': pathway_id,
        'data': pathway_data,
        'generated_date': datetime.now().isoformat()
    }
    
    return jsonify({
        'pathway': pathway_data,
        'pathway_id': pathway_id,
        'message': f"Based on your skills, I recommend the {pathway_data['name']}!"
    })

@app.route('/find_opportunities', methods=['POST'])
def find_opportunities():
    """Hidden Job Market Scanner"""
    user_data = session.get('user', {})
    skills_profile = session.get('skills_profile', {})
    
    opportunities = find_hidden_opportunities(
        user_data.get('location', 'Johannesburg'), 
        skills_profile
    )
    
    return jsonify({
        'opportunities': opportunities,
        'message': "I found these hidden opportunities in your area!"
    })

@app.route('/wellness_support', methods=['POST'])
def wellness_support():
    """Mental Wellness AI Coach"""
    data = request.json
    mood = data.get('mood', 'neutral')
    
    support_messages = {
        'stressed': "I understand you're feeling stressed. Remember, every challenge is temporary. Take deep breaths and focus on one small step at a time.",
        'motivated': "That's amazing energy! Channel this motivation into your next learning goal. You're on the right path!",
        'confused': "Feeling confused is normal when exploring new paths. Let's break down your goals into smaller, clearer steps.",
        'excited': "Your excitement is contagious! This positive energy will help you overcome any obstacles ahead.",
        'discouraged': "I hear you. Remember, every successful person faced setbacks. Your persistence will make the difference."
    }
    
    message = support_messages.get(mood, random.choice(MOTIVATIONAL_MESSAGES))
    
    return jsonify({
        'support_message': message,
        'daily_motivation': random.choice(MOTIVATIONAL_MESSAGES),
        'wellness_tips': [
            "Set small daily goals",
            "Celebrate small wins",
            "Connect with supportive people",
            "Practice gratitude daily"
        ]
    })

@app.route('/find_peers', methods=['POST'])
def find_peers():
    """Peer Matching & Groups"""
    user_pathway = session.get('recommended_pathway', {}).get('id', 'digital_economy')
    user_location = session.get('user', {}).get('location', 'Johannesburg')
    
    # Simulated peer data
    peers = [
        {'name': 'Thabo M.', 'pathway': user_pathway, 'location': user_location, 'stage': 'Learning Phase', 'interests': 'Tech, Innovation'},
        {'name': 'Nomsa K.', 'pathway': user_pathway, 'location': user_location, 'stage': 'Job Searching', 'interests': 'Problem Solving'},
        {'name': 'Sipho N.', 'pathway': user_pathway, 'location': 'Near ' + user_location, 'stage': 'Starting Business', 'interests': 'Entrepreneurship'}
    ]
    
    return jsonify({
        'peers': peers,
        'study_groups': [
            {'name': f'{CAREER_PATHWAYS[user_pathway]["name"]} Study Group', 'members': 12, 'location': user_location},
            {'name': 'Career Development Circle', 'members': 8, 'location': 'Online'}
        ]
    })

@app.route('/update_progress', methods=['POST'])
def update_progress():
    """User Updates Progress"""
    data = request.json
    
    progress_update = {
        'type': data.get('type'),  # 'course_completed', 'job_applied', 'interview', 'hired'
        'details': data.get('details'),
        'date': datetime.now().isoformat()
    }
    
    # Store progress
    if 'progress_updates' not in session:
        session['progress_updates'] = []
    
    session['progress_updates'].append(progress_update)
    session.modified = True
    
    # Reinforcement Learning Simulation
    pathway_id = session.get('recommended_pathway', {}).get('id')
    if pathway_id and data.get('type') == 'hired':
        # Increase success rate (simulated)
        CAREER_PATHWAYS[pathway_id]['success_rate'] += 1
    
    return jsonify({
        'message': 'Progress updated! This helps improve recommendations for other users.',
        'total_updates': len(session.get('progress_updates', [])),
        'reinforcement_learning': 'Your success helps train our AI to better help other youth!'
    })

@app.route('/dashboard')
def dashboard():
    """User Dashboard"""
    return render_template('dashboard.html', 
                         user=session.get('user'),
                         skills_profile=session.get('skills_profile'),
                         pathway=session.get('recommended_pathway'),
                         progress=session.get('progress_updates', []))

if __name__ == '__main__':
    print("🧭 Youth Compass AI - Complete User Flow")
    print("📱 Access at: http://localhost:5000")
    print("🔄 Following the complete user journey flow")
    app.run(debug=True, port=5000)