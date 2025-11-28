from flask import Flask, render_template, request, jsonify, session
import json
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'youth_compass_2024'

# Load environment variables
try:
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    pass

try:
    import openai
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        AI_ENABLED = True
    else:
        AI_ENABLED = False
except ImportError:
    openai = None
    AI_ENABLED = False

# Core Data Structures
LIFE_AREAS = {
    'self_understanding': {
        'name': 'Understanding Myself',
        'icon': '🧠',
        'description': 'Discover your strengths, values, and personality',
        'questions': [
            "What activities make you lose track of time?",
            "What are you naturally good at?",
            "What values are most important to you?",
            "How do you prefer to work - alone or with others?"
        ]
    },
    'opportunities': {
        'name': 'Finding Opportunities',
        'icon': '🎯',
        'description': 'Discover career paths and job opportunities',
        'categories': ['Digital Economy', 'Green Economy', 'Entrepreneurship', 'Creative Industries', 'Healthcare']
    },
    'education': {
        'name': 'Educational Choices',
        'icon': '📚',
        'description': 'Make smart decisions about courses and qualifications',
        'options': ['University', 'TVET College', 'Online Courses', 'Apprenticeships', 'Skills Bootcamps']
    },
    'support': {
        'name': 'Emotional Support',
        'icon': '💪',
        'description': 'Get motivation, resilience training, and mental wellness',
        'resources': ['Daily Motivation', 'Stress Management', 'Goal Setting', 'Confidence Building']
    },
    'community': {
        'name': 'Youth Community',
        'icon': '🤝',
        'description': 'Connect with peers on similar journeys',
        'features': ['Peer Matching', 'Study Groups', 'Mentorship', 'Success Stories']
    },
    'pathway': {
        'name': 'Life Pathway',
        'icon': '🗺️',
        'description': 'Create your personalized roadmap to success',
        'timeframes': ['Next 30 Days', '3 Months', '1 Year', '5 Years']
    }
}

MOTIVATIONAL_QUOTES = [
    "Your potential is unlimited, your time is now.",
    "Every expert was once a beginner. Start today.",
    "South Africa needs your unique talents and perspective.",
    "Small steps daily lead to big changes yearly.",
    "Your dreams are valid and achievable.",
    "You have everything within you to succeed."
]

def get_ai_response(prompt, max_tokens=300):
    """Get AI response with fallback"""
    if AI_ENABLED and openai:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Youth Compass AI, a supportive career and life guidance assistant for South African youth. Be encouraging, practical, and culturally aware."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            pass
    
    # Fallback responses
    if "understand" in prompt.lower():
        return "Based on your responses, you show strong analytical thinking and creativity. These are valuable skills in many fields including technology, design, and problem-solving roles."
    elif "opportunity" in prompt.lower():
        return "Great opportunities exist in South Africa's growing digital economy, renewable energy sector, and entrepreneurship. Focus on building skills that match market demand."
    elif "education" in prompt.lower():
        return "Consider starting with free online courses to test your interests, then pursue formal qualifications that align with your career goals and financial situation."
    else:
        return "You're on the right path! Focus on continuous learning, building relationships, and taking small consistent actions toward your goals."

@app.route('/')
def index():
    return render_template('youth_compass.html')

@app.route('/assess/<area>')
def assess_area(area):
    if area not in LIFE_AREAS:
        return jsonify({'error': 'Invalid area'}), 400
    
    area_data = LIFE_AREAS[area]
    return jsonify({
        'area': area,
        'name': area_data['name'],
        'icon': area_data['icon'],
        'description': area_data['description'],
        'questions': area_data.get('questions', [])
    })

@app.route('/analyze', methods=['POST'])
def analyze_responses():
    data = request.json
    area = data.get('area')
    responses = data.get('responses', [])
    
    if not area or not responses:
        return jsonify({'error': 'Missing data'}), 400
    
    # Create AI prompt based on area
    if area == 'self_understanding':
        prompt = f"Analyze this young South African's self-assessment responses and provide insights about their strengths, personality, and potential career fits: {' '.join(responses)}"
    elif area == 'opportunities':
        prompt = f"Based on these interests and skills, suggest specific career opportunities in South Africa: {' '.join(responses)}"
    elif area == 'education':
        prompt = f"Recommend educational pathways for someone with these goals and interests: {' '.join(responses)}"
    else:
        prompt = f"Provide supportive guidance for a young person who shared: {' '.join(responses)}"
    
    ai_response = get_ai_response(prompt)
    
    # Store in session
    if 'assessments' not in session:
        session['assessments'] = {}
    session['assessments'][area] = {
        'responses': responses,
        'analysis': ai_response,
        'timestamp': datetime.now().isoformat()
    }
    session.modified = True
    
    return jsonify({
        'analysis': ai_response,
        'area': area,
        'next_steps': get_next_steps(area)
    })

def get_next_steps(area):
    """Get contextual next steps based on area"""
    steps = {
        'self_understanding': [
            "Complete a skills inventory",
            "Take a career interest assessment",
            "Reflect on your values and priorities",
            "Seek feedback from trusted friends/family"
        ],
        'opportunities': [
            "Research job market trends in your area",
            "Network with professionals in your field",
            "Create profiles on job platforms",
            "Attend career fairs and industry events"
        ],
        'education': [
            "Research course requirements and costs",
            "Apply for bursaries and financial aid",
            "Connect with current students/alumni",
            "Create a study timeline and budget"
        ],
        'support': [
            "Practice daily mindfulness or meditation",
            "Set small, achievable weekly goals",
            "Build a support network of peers",
            "Celebrate your progress regularly"
        ],
        'community': [
            "Join youth development programs",
            "Participate in online communities",
            "Attend local networking events",
            "Find a mentor in your field"
        ],
        'pathway': [
            "Set SMART goals for next 90 days",
            "Create a skills development plan",
            "Build your professional network",
            "Track progress weekly"
        ]
    }
    return steps.get(area, ["Take action", "Stay consistent", "Keep learning"])

@app.route('/dashboard')
def dashboard():
    assessments = session.get('assessments', {})
    return render_template('dashboard.html', assessments=assessments, life_areas=LIFE_AREAS)

@app.route('/community')
def community():
    # Simulated peer data
    peers = [
        {'name': 'Thabo M.', 'location': 'Johannesburg', 'interests': 'Tech, Coding', 'stage': 'Learning Python'},
        {'name': 'Nomsa K.', 'location': 'Cape Town', 'interests': 'Design, Art', 'stage': 'Building Portfolio'},
        {'name': 'Sipho N.', 'location': 'Durban', 'interests': 'Business, Sales', 'stage': 'Starting Business'},
        {'name': 'Lerato S.', 'location': 'Pretoria', 'interests': 'Healthcare', 'stage': 'Studying Nursing'}
    ]
    return jsonify({'peers': peers, 'motivation': random.choice(MOTIVATIONAL_QUOTES)})

@app.route('/pathway')
def create_pathway():
    assessments = session.get('assessments', {})
    
    if not assessments:
        return jsonify({'error': 'Complete some assessments first'}), 400
    
    # Generate personalized pathway based on assessments
    pathway = {
        'next_30_days': [
            "Complete remaining self-assessments",
            "Research 3 specific career options",
            "Connect with 2 professionals in your field",
            "Start a relevant online course"
        ],
        '3_months': [
            "Complete foundational skills training",
            "Build a portfolio or project",
            "Apply for internships or entry positions",
            "Join professional networks"
        ],
        '1_year': [
            "Gain practical experience",
            "Develop specialized skills",
            "Build professional reputation",
            "Mentor other youth"
        ],
        '5_years': [
            "Achieve career stability",
            "Become a leader in your field",
            "Give back to your community",
            "Pursue advanced opportunities"
        ]
    }
    
    return jsonify({'pathway': pathway, 'assessments_completed': len(assessments)})

if __name__ == '__main__':
    print("\n🧭 Youth Compass AI - Complete Life Direction Platform")
    print("🌍 Empowering South African Youth")
    print("📱 Access at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000, host='127.0.0.1')