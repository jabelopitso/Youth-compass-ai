from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from logic import analyze_profile, PATHWAYS_DATA, PATHWAY_KEYWORDS, update_pathway_success
from ai_engine import ContextualProfiler, EconomicChoicesAI, SupportAI
import os

app = Flask(__name__)
# Crucial for using sessions (like storing the answers across pages)
app.secret_key = os.urandom(24) 

# --- Routes for the Profiler Flow ---

@app.route('/', methods=['GET', 'POST'])
def start_profiler():
    """Route 1: Handles the start screen and stores the user's name/initials."""
    
    if request.method == 'POST':
        # Clear any previous session data
        session.clear() 
        
        # Store the user's name and initialize the answers list
        session['user_name'] = request.form.get('user_name', 'Young South African')
        session['answers'] = []
        
        # Start the question flow
        return redirect(url_for('profiler', q_index=0))
    
    # GET request shows the starting page
    return render_template('index.html')

@app.route('/profiler/<int:q_index>', methods=['GET', 'POST'])
def profiler(q_index):
    """Route 2: Handles the 5 questions one by one."""
    
    # The 5 questions defined for your NLP Profiler
    QUESTIONS = [
        "What are you good at, even if it's just a hobby or something you do for fun?",
        "Describe a time you showed initiative or solved a problem for someone else (family, friend, community).",
        "If you had R500 and 3 days, what would you try to do with it to make more money, or to improve your community?",
        "What kind of environment do you prefer? Indoors, outdoors, or a mix of both?",
        "What is the biggest challenge or obstacle you currently face in finding a job/getting skills?",
    ]
    
    # Check for session data
    if 'answers' not in session:
        return redirect(url_for('start_profiler')) # Redirect if session is lost

    if request.method == 'POST':
        # 1. Save the answer from the submitted form
        answer = request.form.get('user_input')
        session['answers'].append(answer)
        session.modified = True # Tell Flask the list has changed
        
        # 2. Check if all questions are answered
        next_q_index = q_index + 1
        if next_q_index >= len(QUESTIONS):
            # If all done, analyze the profile and show results
            return redirect(url_for('results'))
        else:
            # Continue to the next question
            return redirect(url_for('profiler', q_index=next_q_index))

    # GET request shows the current question
    if q_index < len(QUESTIONS):
        return render_template(
            'profiler.html', 
            question=QUESTIONS[q_index], 
            q_number=q_index + 1,
            total_questions=len(QUESTIONS)
        )
    
    # Should not happen, but as a fallback:
    return redirect(url_for('results'))

@app.route('/results')
def results():
    """Route 3: Enhanced AI analysis and comprehensive pathway display."""
    
    if 'answers' not in session or not session['answers']:
        return redirect(url_for('start_profiler'))

    # AI Acceleration with enhanced features
    pathway_data, scores = analyze_profile(session['answers'])
    
    # Store enhanced results in session
    pathway_key = None
    for key, data in PATHWAYS_DATA.items():
        if data['name'] == pathway_data['name']:
            pathway_key = key
            break
    
    session['pathway_key'] = pathway_key or 'entrepreneurship'
    session['current_success_rate'] = pathway_data['success_rate']
    session['skills_profile'] = pathway_data['skills_profile']
    session['pathway_data'] = pathway_data
    session.modified = True

    # Render enhanced result template
    return render_template(
        'result.html',
        user_name=session['user_name'],
        pathway_data=pathway_data,
        scores=scores,
        success_rate=pathway_data['success_rate']
    )

@app.route('/feedback', methods=['POST'])
def feedback():
    """Route 4: Enhanced feedback loop with reinforcement learning."""
    
    feedback_type = request.form.get('feedback_type')
    pathway_key = session.get('pathway_key', 'entrepreneurship')
    
    if feedback_type == 'success':
        # Update AI success rate using reinforcement learning
        new_rate = update_pathway_success(pathway_key, success=True)
        session['current_success_rate'] = new_rate
        session.modified = True
        
        return render_template(
            'feedback_success.html',
            new_rate=new_rate,
            pathway=PATHWAYS_DATA[pathway_key]['name']
        )
    elif feedback_type == 'not_helpful':
        # Update AI with negative feedback
        new_rate = update_pathway_success(pathway_key, success=False)
        session['current_success_rate'] = new_rate
        session.modified = True
        
        return render_template(
            'feedback_improve.html',
            pathway=PATHWAYS_DATA[pathway_key]['name']
        )
    
    return redirect(url_for('results'))

@app.route('/opportunities')
def opportunities():
    """Route 5: Display hidden job market opportunities."""
    if 'pathway_data' not in session:
        return redirect(url_for('start_profiler'))
    
    # Get opportunities from AI engine
    economic_ai = EconomicChoicesAI()
    skills_profile = session.get('skills_profile', {})
    opportunities = economic_ai.find_hidden_opportunities(skills_profile)
    
    return render_template('opportunities.html', opportunities=opportunities)

@app.route('/support')
def support():
    """Route 6: Emotional support and peer matching."""
    if 'user_name' not in session:
        return redirect(url_for('start_profiler'))
    
    support_ai_engine = SupportAI()
    motivation = support_ai_engine.get_motivational_message()
    peer_matches = support_ai_engine.find_peer_matches({}, session.get('user_location', 'general'))
    
    return render_template('support.html', 
                         motivation=motivation, 
                         peer_matches=peer_matches,
                         user_name=session['user_name'])

@app.route('/api/update_success', methods=['POST'])
def api_update_success():
    """API endpoint for real-time success rate updates."""
    data = request.json
    pathway = data.get('pathway')
    success = data.get('success', True)
    
    if pathway in PATHWAYS_DATA:
        new_rate = update_pathway_success(pathway, success)
        return jsonify({'success': True, 'new_rate': new_rate})
    
    return jsonify({'success': False, 'error': 'Invalid pathway'})

if __name__ == '__main__':
    # Use a port that works well in hackathon environments
    app.run(debug=True, host='0.0.0.0', port=5000)