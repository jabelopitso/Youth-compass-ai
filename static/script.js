let responses = [];

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, 'user');
        responses.push(message);
        input.value = '';
        
        setTimeout(() => {
            if (responses.length >= 3) {
                analyzeResponses();
            } else {
                addMessage("Tell me more about your interests and goals.", 'bot');
            }
        }, 500);
    }
}

function askQuestion(question) {
    addMessage(question, 'bot');
    document.getElementById('questions').style.display = 'none';
}

function addMessage(text, sender) {
    const messages = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function analyzeResponses() {
    fetch('/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({responses: responses})
    })
    .then(response => response.json())
    .then(data => {
        sessionStorage.setItem('careerPath', JSON.stringify(data.career_path));
        window.location.href = '/result';
    });
}

function displayResults() {
    const pathData = JSON.parse(sessionStorage.getItem('careerPath'));
    if (pathData) {
        document.getElementById('path-title').textContent = pathData.title;
        
        const careersList = document.getElementById('careers-list');
        careersList.innerHTML = '<h4>Recommended Careers:</h4>' + 
            pathData.careers.map(career => `<li>${career}</li>`).join('');
        
        const nextSteps = document.getElementById('next-steps');
        nextSteps.innerHTML = '<h4>Next Steps:</h4>' + 
            pathData.next_steps.map(step => `<li>${step}</li>`).join('');
    }
}

function submitFeedback() {
    const feedback = document.getElementById('feedback').value;
    if (feedback) {
        alert('Thank you for your feedback! We\'ll use this to improve your recommendations.');
    }
}

function startOver() {
    sessionStorage.clear();
    window.location.href = '/';
}

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/result') {
        displayResults();
    } else {
        document.getElementById('questions').style.display = 'block';
        addMessage("Hi! I'm here to help you discover your career path. What are you passionate about?", 'bot');
    }
});

document.getElementById('user-input')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});