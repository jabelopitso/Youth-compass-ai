# WhatsApp Integration for Low-Data Access
# This would integrate with WhatsApp Business API for maximum reach

class WhatsAppBot:
    """Simplified WhatsApp integration for low-data access"""
    
    def __init__(self):
        self.questions = [
            "Hi! I'm Youth Compass AI. What's your name?",
            "What are you good at, even if it's just a hobby?",
            "Tell me about a time you helped someone or solved a problem.",
            "If you had R500 and 3 days, what would you do to make money?",
            "Do you prefer working indoors, outdoors, or both?",
            "What's your biggest challenge in finding work or skills training?"
        ]
        self.user_sessions = {}
    
    def process_message(self, phone_number, message):
        """Process incoming WhatsApp message"""
        if phone_number not in self.user_sessions:
            self.user_sessions[phone_number] = {
                'step': 0,
                'answers': [],
                'name': ''
            }
        
        session = self.user_sessions[phone_number]
        
        if session['step'] == 0:
            session['name'] = message
            session['step'] = 1
            return self.questions[1]
        elif session['step'] < 5:
            session['answers'].append(message)
            session['step'] += 1
            if session['step'] < 5:
                return self.questions[session['step']]
            else:
                return self.generate_results(session)
        
        return "Type 'start' to begin your career assessment."
    
    def generate_results(self, session):
        """Generate career path results for WhatsApp"""
        from logic import analyze_profile
        
        pathway_data, scores = analyze_profile(session['answers'])
        
        result = f"🎯 {session['name']}, here's your path:\n\n"
        result += f"📈 {pathway_data['name']}\n"
        result += f"✅ Success Rate: {pathway_data['success_rate']}%\n\n"
        result += "📋 Next Steps:\n"
        
        for i, step in enumerate(pathway_data['steps'][:2], 1):
            result += f"{i}. {step[:100]}...\n"
        
        result += f"\n💪 Your top skills: "
        top_skills = sorted(pathway_data['skills_profile'].items(), 
                          key=lambda x: x[1], reverse=True)[:3]
        result += ", ".join([skill.replace('_', ' ').title() for skill, _ in top_skills])
        
        result += f"\n\n🔗 Get full details: https://youthcompass.co.za/results/{session['name']}"
        
        return result

# Usage example:
# bot = WhatsAppBot()
# response = bot.process_message("+27123456789", "Hello")