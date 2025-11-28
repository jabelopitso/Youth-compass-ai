from flask import Flask, render_template, request, jsonify
import json
import os

# Load environment variables from .env file if it exists
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
except ImportError:
    openai = None
    print("⚠️  OpenAI not installed. Run 'python3 setup_openai.py' for real AI responses.")

app = Flask(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
    print("✅ OpenAI API configured - Real AI responses enabled!")
else:
    print("⚠️  Using fallback responses. Set OPENAI_API_KEY for real AI.")

# Simple AI responses (simulating OpenAI API)
CAREER_SUGGESTIONS = {
    'tech': {
        'careers': ['Software Developer', 'Data Analyst', 'Cybersecurity Specialist'],
        'skills': ['Python', 'SQL', 'Problem Solving', 'Critical Thinking'],
        'courses': ['FreeCodeCamp', 'Coursera Python', 'Google Data Analytics'],
        'roadmap': ['Learn basics (Month 1)', 'Build projects (Month 2)', 'Apply for jobs (Month 3)']
    },
    'design': {
        'careers': ['UX Designer', 'Graphic Designer', 'Digital Marketer'],
        'skills': ['Adobe Creative Suite', 'Figma', 'User Research', 'Creativity'],
        'courses': ['Adobe Tutorials', 'Google UX Design', 'Canva Design School'],
        'roadmap': ['Design fundamentals (Month 1)', 'Portfolio building (Month 2)', 'Client work (Month 3)']
    },
    'business': {
        'careers': ['Business Analyst', 'Project Manager', 'Entrepreneur'],
        'skills': ['Communication', 'Leadership', 'Excel', 'Strategic Thinking'],
        'courses': ['Google Project Management', 'Coursera Business', 'Khan Academy'],
        'roadmap': ['Business basics (Month 1)', 'Leadership skills (Month 2)', 'Network & apply (Month 3)']
    }
}

LEARNING_PLANS = {
    'web_dev': {
        'Day 1': 'HTML & CSS Basics - Build your first webpage',
        'Day 2': 'JavaScript Fundamentals - Add interactivity',
        'Day 3': 'Responsive Design - Make it mobile-friendly',
        'Day 4': 'Git & GitHub - Version control basics',
        'Day 5': 'React Basics - Modern web development',
        'Day 6': 'API Integration - Connect to external data',
        'Day 7': 'Deploy Your Project - Show the world'
    },
    'ai': {
        'Day 1': 'Python Basics - Programming fundamentals',
        'Day 2': 'Data Analysis with Pandas - Handle data',
        'Day 3': 'Machine Learning Intro - Basic concepts',
        'Day 4': 'Build Your First Model - Hands-on practice',
        'Day 5': 'Deep Learning Basics - Neural networks',
        'Day 6': 'AI Ethics & Applications - Real-world use',
        'Day 7': 'Create AI Portfolio Project - Showcase skills'
    },
    'data': {
        'Day 1': 'Excel Mastery - Data manipulation basics',
        'Day 2': 'SQL Fundamentals - Database queries',
        'Day 3': 'Python for Data - Programming for analysis',
        'Day 4': 'Data Visualization - Charts and graphs',
        'Day 5': 'Statistics Basics - Understanding data',
        'Day 6': 'Dashboard Creation - Present insights',
        'Day 7': 'Real Project Analysis - Apply all skills'
    }
}

@app.route('/')
def index():
    return render_template('simple_index.html')

@app.route('/ai_status')
def ai_status():
    """Check if real AI is available"""
    real_ai = bool(openai and OPENAI_API_KEY)
    return jsonify({
        'real_ai': real_ai,
        'message': 'Real ChatGPT AI active' if real_ai else 'Using fallback responses'
    })

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    age = data.get('age', '')
    skills = data.get('skills', '')
    interests = data.get('interests', '')
    
    if openai and OPENAI_API_KEY != 'your-api-key-here':
        # Real ChatGPT API
        try:
            prompt = f"""
You are YouthCompass AI, a career guidance assistant for young South Africans. 

User Profile:
- Age: {age}
- Skills: {skills}
- Interests: {interests}

Provide career guidance in this JSON format:
{{
    "message": "Personalized message based on their profile",
    "careers": ["3 specific career suggestions"],
    "required_skills": ["4-5 key skills they need"],
    "free_courses": ["3 specific free courses/platforms"],
    "roadmap": ["3 actionable steps for next 3 months"]
}}

Focus on South African context, accessible opportunities, and be encouraging.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful career guidance AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            # Try to parse JSON response
            try:
                return jsonify(json.loads(ai_response))
            except:
                # Fallback if JSON parsing fails
                return jsonify({
                    "message": ai_response,
                    "careers": ["Software Developer", "Data Analyst", "Digital Marketer"],
                    "required_skills": ["Communication", "Problem Solving", "Technical Skills"],
                    "free_courses": ["FreeCodeCamp", "Coursera", "Khan Academy"],
                    "roadmap": ["Learn basics", "Build portfolio", "Apply for opportunities"]
                })
                
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Fall back to simple logic
            pass
    
    # Fallback logic when no API key or error
    career_type = 'business'  # default
    if any(word in skills.lower() + interests.lower() for word in ['code', 'program', 'tech', 'computer']):
        career_type = 'tech'
    elif any(word in skills.lower() + interests.lower() for word in ['design', 'art', 'creative', 'visual']):
        career_type = 'design'
    
    suggestion = CAREER_SUGGESTIONS[career_type]
    
    response = {
        'message': f"Based on your interests in {interests} and skills in {skills}, here are perfect career paths for you:",
        'careers': suggestion['careers'],
        'required_skills': suggestion['skills'],
        'free_courses': suggestion['courses'],
        'roadmap': suggestion['roadmap']
    }
    
    return jsonify(response)

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    data = request.json
    skills = data.get('skills', '')
    experience = data.get('experience', '')
    strengths = data.get('strengths', '')
    
    if openai and OPENAI_API_KEY != 'your-api-key-here':
        # Real ChatGPT API for CV generation
        try:
            prompt = f"""
Create a professional CV summary paragraph for a young South African job seeker.

Their profile:
- Skills: {skills}
- Experience: {experience} 
- Strengths: {strengths}

Write a compelling 2-3 sentence professional summary that:
- Highlights their key skills and experience
- Shows their value to employers
- Sounds professional but authentic
- Is suitable for South African job market

Return only the summary paragraph, no extra text.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional CV writing assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            cv_summary = response.choices[0].message.content.strip()
            return jsonify({'cv_summary': cv_summary})
            
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Fall back to simple logic
            pass
    
    # Fallback CV generation
    cv_summary = f"Dynamic professional with expertise in {skills}. Proven experience in {experience}, demonstrating strong {strengths}. Passionate about continuous learning and delivering results that drive organizational success. Ready to contribute innovative solutions and collaborative leadership to achieve business objectives."
    
    return jsonify({'cv_summary': cv_summary})

@app.route('/learning_plan', methods=['POST'])
def learning_plan():
    data = request.json
    area = data.get('area', 'web_dev')
    
    if openai and OPENAI_API_KEY != 'your-api-key-here':
        # Real ChatGPT API for learning plans
        try:
            area_names = {
                'web_dev': 'Web Development',
                'ai': 'Artificial Intelligence', 
                'data': 'Data Analysis'
            }
            
            prompt = f"""
Create a 7-day learning sprint plan for {area_names.get(area, area)}.

Requirements:
- Each day should have 1-2 hours of focused learning
- Include practical, hands-on activities
- Suitable for beginners
- Use free resources when possible
- Build towards a final project

Return in this JSON format:
{{
    "Day 1": "Specific learning task and activity",
    "Day 2": "Specific learning task and activity",
    "Day 3": "Specific learning task and activity",
    "Day 4": "Specific learning task and activity",
    "Day 5": "Specific learning task and activity",
    "Day 6": "Specific learning task and activity",
    "Day 7": "Specific learning task and activity"
}}

Make each day build on the previous day's learning.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert learning curriculum designer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            try:
                plan_data = json.loads(ai_response)
                return jsonify({
                    'area': area,
                    'plan': plan_data,
                    'message': f"Here's your AI-generated 7-day {area_names.get(area, area)} learning sprint!"
                })
            except:
                # Fallback if JSON parsing fails
                pass
                
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            # Fall back to simple logic
            pass
    
    # Fallback learning plan
    plan = LEARNING_PLANS.get(area, LEARNING_PLANS['web_dev'])
    
    return jsonify({
        'area': area,
        'plan': plan,
        'message': f"Here's your 7-day {area.replace('_', ' ').title()} learning sprint!"
    })

if __name__ == '__main__':
    try:
        print("\n🚀 Starting Youth Compass AI...")
        print("📱 Access at: http://localhost:5000")
        print("🌐 Or: http://127.0.0.1:5000")
        print("\n" + "="*50)
        app.run(debug=True, port=5000, host='127.0.0.1')
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("🔄 Trying alternative port...")
        app.run(debug=True, port=5001, host='127.0.0.1')