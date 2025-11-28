from flask import Flask, render_template, request, jsonify
from logic import analyze_responses, generate_career_path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    responses = data.get('responses', [])
    
    scores = analyze_responses(responses)
    career_path = generate_career_path(scores)
    
    return jsonify({
        'scores': scores,
        'career_path': career_path
    })

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)