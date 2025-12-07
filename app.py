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

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """AI Chatbot for Questions and Support"""
    data = request.json
    message = data.get('message', '').lower()
    
    # AI responses based on keywords
    if any(word in message for word in ['cv', 'resume']):
        response = "I can help you create a strong CV! Focus on: 1) Clear contact details, 2) Skills summary, 3) Work experience (even informal), 4) Education, 5) References. Would you like specific tips for any section?"
    
    elif any(word in message for word in ['interview', 'job interview']):
        response = "Great question about interviews! Key tips: 1) Research the company, 2) Practice common questions, 3) Prepare examples of your achievements, 4) Dress appropriately, 5) Ask thoughtful questions. What specific aspect would you like help with?"
    
    elif any(word in message for word in ['salary', 'negotiate', 'pay']):
        response = "Salary negotiation is important! In South Africa: Entry-level positions typically range R8,000-R15,000/month. Research market rates, highlight your value, and don't be afraid to negotiate respectfully. What role are you considering?"
    
    elif any(word in message for word in ['skills', 'learn', 'course']):
        response = "Skill development is key to career growth! Popular in-demand skills: Digital marketing, Data analysis, Programming, Project management. Free resources: Coursera, edX, FreeCodeCamp, Google Skillshop. What area interests you most?"
    
    elif any(word in message for word in ['business', 'entrepreneur', 'startup']):
        response = "Starting a business in SA? Key steps: 1) Validate your idea, 2) Register with CIPC, 3) Get tax clearance, 4) Open business bank account, 5) Consider SEDA support. What type of business are you thinking about?"
    
    elif any(word in message for word in ['funding', 'loan', 'money']):
        response = "Funding options for SA youth: 1) NYDA loans (up to R1M), 2) SEDA grants, 3) Provincial development agencies, 4) Crowdfunding, 5) Angel investors. What's your funding need and business stage?"
    
    elif any(word in message for word in ['tax', 'vat', 'sars']):
        response = "Tax basics for entrepreneurs: Register for income tax immediately, VAT registration required at R1M+ turnover, keep all receipts, file returns on time. Use our VAT tracker to monitor your thresholds!"
    
    elif any(word in message for word in ['networking', 'connect', 'mentor']):
        response = "Networking is crucial! Try: 1) LinkedIn groups, 2) Industry events, 3) Professional associations, 4) Alumni networks, 5) Our peer matching feature. What industry are you interested in?"
    
    elif any(word in message for word in ['stress', 'anxiety', 'overwhelmed']):
        response = "It's normal to feel overwhelmed on your career journey. Remember: 1) Take small steps daily, 2) Celebrate progress, 3) Connect with supportive people, 4) Practice self-care, 5) Seek help when needed. You're not alone in this!"
    
    elif any(word in message for word in ['location', 'remote', 'work from home']):
        response = "Remote work is growing in SA! Skills needed: Self-discipline, communication, tech literacy. Platforms: Remote Year, We Work Remotely, AngelList. Many companies now offer hybrid options. What type of remote work interests you?"
    
    else:
        # General career guidance
        responses = [
            "That's a great question! Career success comes from continuous learning, networking, and persistence. What specific area would you like guidance on?",
            "I'm here to help with your career journey! Whether it's skills development, job searching, or entrepreneurship - what's your main focus right now?",
            "Every career path is unique. Focus on building skills, gaining experience, and staying adaptable. What's your biggest career challenge currently?"
        ]
        response = random.choice(responses)
    
    return jsonify({
        'response': response,
        'suggestions': [
            'Tell me about CV writing',
            'How do I prepare for interviews?',
            'What skills should I learn?',
            'Help with starting a business',
            'Tax and VAT guidance'
        ]
    })

@app.route('/vat_tracker', methods=['GET', 'POST'])
def vat_tracker():
    """VAT/Tax Threshold Tracker"""
    if request.method == 'POST':
        data = request.json
        
        # Store financial data
        if 'financial_data' not in session:
            session['financial_data'] = {
                'monthly_income': [],
                'annual_projection': 0,
                'vat_registered': False,
                'tax_registered': True
            }
        
        monthly_income = float(data.get('monthly_income', 0))
        session['financial_data']['monthly_income'].append({
            'amount': monthly_income,
            'month': datetime.now().strftime('%Y-%m'),
            'date': datetime.now().isoformat()
        })
        
        # Calculate projections
        recent_months = session['financial_data']['monthly_income'][-6:]  # Last 6 months
        avg_monthly = sum(m['amount'] for m in recent_months) / len(recent_months) if recent_months else 0
        annual_projection = avg_monthly * 12
        
        session['financial_data']['annual_projection'] = annual_projection
        session.modified = True
        
        # VAT and Tax Thresholds (2024 SA rates)
        vat_threshold = 1000000  # R1M for VAT registration
        provisional_tax_threshold = 1000  # R1000+ annual tax liability
        
        alerts = []
        
        # VAT Registration Alert
        if annual_projection >= vat_threshold * 0.8:  # 80% of threshold
            if annual_projection >= vat_threshold:
                alerts.append({
                    'type': 'critical',
                    'title': 'VAT Registration Required!',
                    'message': f'Your projected annual income (R{annual_projection:,.0f}) exceeds R1M. You must register for VAT within 21 days.',
                    'action': 'Register for VAT immediately on SARS eFiling'
                })
            else:
                alerts.append({
                    'type': 'warning',
                    'title': 'Approaching VAT Threshold',
                    'message': f'Your projected income (R{annual_projection:,.0f}) is approaching the R1M VAT threshold.',
                    'action': 'Prepare for VAT registration and start keeping detailed records'
                })
        
        # Provisional Tax Alert
        estimated_tax = max(0, (annual_projection - 87300) * 0.18)  # Basic tax calculation
        if estimated_tax >= provisional_tax_threshold:
            alerts.append({
                'type': 'info',
                'title': 'Provisional Tax Required',
                'message': f'Estimated annual tax liability: R{estimated_tax:,.0f}. You need to pay provisional tax.',
                'action': 'Register for provisional tax and make bi-annual payments'
            })
        
        return jsonify({
            'annual_projection': annual_projection,
            'vat_threshold_percentage': (annual_projection / vat_threshold) * 100,
            'alerts': alerts,
            'recommendations': [
                'Keep detailed records of all income and expenses',
                'Set aside 15-20% of income for tax obligations',
                'Consider consulting a tax practitioner',
                'Use accounting software for better tracking'
            ]
        })
    
    # GET request - return current status
    financial_data = session.get('financial_data', {})
    return jsonify(financial_data)

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

@app.route('/chat')
def chat_page():
    """AI Chatbot Page"""
    return render_template('chatbot.html')

@app.route('/dashboard')
def dashboard():
    """User Dashboard"""
    return render_template('dashboard.html', 
                         user=session.get('user'),
                         skills_profile=session.get('skills_profile'),
                         pathway=session.get('recommended_pathway'),
                         progress=session.get('progress_updates', []),
                         financial_data=session.get('financial_data', {}))

if __name__ == '__main__':
    print("="*70)
    print("🧭 Youth Compass AI - Complete User Flow")
    print("="*70)
    print("\n📱 Access Points:")
    print("   Main Platform:  http://localhost:5001")
    print("   AI Chatbot:     http://localhost:5001/chat")
    print("   Dashboard:      http://localhost:5001/dashboard")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*70)
    print("\nStarting server...\n")
    
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if port 5001 is in use: lsof -ti:5001")
        print("2. Kill existing process: lsof -ti:5001 | xargs kill -9")
        print("3. Try a different port")