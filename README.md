# Youth Compass AI

An AI-powered career guidance platform that helps young people discover their career paths through interactive conversations and intelligent analysis.

## Project Pitch

Youth Compass AI addresses the challenge of career uncertainty among young people by providing personalized, AI-driven career guidance. The platform uses natural language processing to analyze user responses and generate tailored career recommendations with actionable next steps.

## Features

- Interactive chat interface for career exploration
- AI-powered analysis of interests and responses
- Personalized career path recommendations
- Mobile-first responsive design
- Feedback loop for continuous improvement

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd youth-compass-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## How It Works

1. Users engage in a conversational interface about their interests
2. The AI analyzes responses using keyword matching and scoring
3. Career recommendations are generated based on interest patterns
4. Users receive personalized paths with specific next steps
5. Feedback collection helps refine future recommendations

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI/NLP**: Custom keyword analysis algorithm
- **Design**: Mobile-first responsive interface

## Project Structure

```
youth-compass-ai/
├── app.py              # Flask application and routing
├── logic.py            # AI analysis and career matching logic
├── templates/          # HTML templates
│   ├── index.html      # Main chat interface
│   └── result.html     # Results and feedback page
├── static/             # CSS and JavaScript files
│   ├── style.css       # Mobile-first styling
│   └── script.js       # Frontend interaction logic
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```