# 📡 API Documentation - Youth Compass AI

## Base URL
```
http://localhost:5001
```

---

## Endpoints

### 1. Home Page
**GET** `/`

Returns the main landing page with complete user journey flow.

**Response:** HTML page

---

### 2. User Sign-Up
**POST** `/signup`

Quick registration for new users.

**Request Body:**
```json
{
  "name": "Thabo Mokoena",
  "age": 23,
  "location": "Gauteng",
  "education_level": "Matric"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Welcome Thabo Mokoena! Let's start your journey."
}
```

**Status Codes:**
- `200`: Success
- `400`: Invalid input

---

### 3. AI Coach Chat
**POST** `/coach_chat`

First interaction with AI coach for skills assessment.

#### Get Questions
**Request Body:**
```json
{
  "responses": []
}
```

**Response:**
```json
{
  "questions": [
    "What activities make you feel energized and excited?",
    "What are you naturally good at, even if it's just small things?",
    "If you could solve one problem in your community, what would it be?",
    "What do you do in your free time that you really enjoy?",
    "What kind of work environment appeals to you most?"
  ]
}
```

#### Submit Responses
**Request Body:**
```json
{
  "responses": [
    "I love working with computers and solving problems",
    "I'm good at explaining things to people",
    "I want to help youth find jobs",
    "I enjoy coding and building websites",
    "I prefer flexible remote work"
  ]
}
```

**Response:**
```json
{
  "skills_profile": {
    "communication": 75,
    "problem_solving": 85,
    "creativity": 60,
    "technology": 95,
    "leadership": 70,
    "analytical": 80,
    "hands_on": 45,
    "sales": 50
  },
  "message": "Great! I've analyzed your responses and created your Skills Passport."
}
```

---

### 4. Generate Career Pathway
**POST** `/generate_pathway`

AI-powered career path recommendation based on skills profile.

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "pathway_id": "digital_economy",
  "pathway": {
    "name": "Digital Economy Path",
    "icon": "💻",
    "description": "Technology and digital skills for the modern economy",
    "careers": [
      "Software Developer",
      "Data Analyst",
      "Digital Marketer",
      "IT Support"
    ],
    "courses": [
      {
        "name": "Google Data Analytics Certificate",
        "provider": "Coursera",
        "cost": "Free",
        "duration": "6 months"
      }
    ],
    "success_rate": 72
  },
  "message": "Based on your skills, I recommend the Digital Economy Path!"
}
```

**Status Codes:**
- `200`: Success
- `400`: Skills assessment not completed

---

### 5. Find Hidden Opportunities
**POST** `/find_opportunities`

Scans hidden job market for opportunities.

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "opportunities": [
    {
      "title": "Social Media Assistant",
      "company": "Local Restaurant",
      "location": "Johannesburg",
      "source": "Facebook Page"
    },
    {
      "title": "Delivery Driver",
      "company": "Pharmacy Chain",
      "location": "Cape Town",
      "source": "Community Notice"
    }
  ],
  "message": "I found these hidden opportunities in your area!"
}
```

---

### 6. Wellness Support
**POST** `/wellness_support`

Mental wellness AI coach for emotional support.

**Request Body:**
```json
{
  "mood": "stressed"
}
```

**Mood Options:**
- `stressed`
- `motivated`
- `confused`
- `excited`
- `discouraged`

**Response:**
```json
{
  "support_message": "I understand you're feeling stressed. Remember, every challenge is temporary. Take deep breaths and focus on one small step at a time.",
  "daily_motivation": "Your potential is unlimited. Every expert was once a beginner.",
  "wellness_tips": [
    "Set small daily goals",
    "Celebrate small wins",
    "Connect with supportive people",
    "Practice gratitude daily"
  ]
}
```

---

### 7. Find Peers
**POST** `/find_peers`

AI-powered peer matching based on career path and location.

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "peers": [
    {
      "name": "Thabo M.",
      "pathway": "digital_economy",
      "location": "Gauteng",
      "stage": "Learning Phase",
      "interests": "Tech, Innovation"
    }
  ],
  "study_groups": [
    {
      "name": "Digital Economy Path Study Group",
      "members": 12,
      "location": "Gauteng"
    }
  ]
}
```

---

### 8. AI Chatbot
**POST** `/chatbot`

Comprehensive AI assistant for career guidance.

**Request Body:**
```json
{
  "message": "How do I write a good CV?"
}
```

**Response:**
```json
{
  "response": "I can help you create a strong CV! Focus on: 1) Clear contact details, 2) Skills summary, 3) Work experience (even informal), 4) Education, 5) References. Would you like specific tips for any section?",
  "suggestions": [
    "Tell me about CV writing",
    "How do I prepare for interviews?",
    "What skills should I learn?",
    "Help with starting a business",
    "Tax and VAT guidance"
  ]
}
```

**Supported Topics:**
- CV writing
- Interview preparation
- Salary negotiation
- Skills development
- Business startup
- Funding options
- Tax and VAT
- Networking
- Remote work
- Stress management

---

### 9. VAT/Tax Threshold Tracker
**POST** `/vat_tracker`

Track income and monitor tax thresholds.

**Request Body:**
```json
{
  "monthly_income": 50000
}
```

**Response:**
```json
{
  "annual_projection": 600000,
  "vat_threshold_percentage": 60.0,
  "alerts": [
    {
      "type": "info",
      "title": "Provisional Tax Required",
      "message": "Estimated annual tax liability: R91,242. You need to pay provisional tax.",
      "action": "Register for provisional tax and make bi-annual payments"
    }
  ],
  "recommendations": [
    "Keep detailed records of all income and expenses",
    "Set aside 15-20% of income for tax obligations",
    "Consider consulting a tax practitioner",
    "Use accounting software for better tracking"
  ]
}
```

**GET** `/vat_tracker`

Get current financial tracking status.

**Response:**
```json
{
  "monthly_income": [
    {
      "amount": 50000,
      "month": "2024-01",
      "date": "2024-01-15T10:30:00"
    }
  ],
  "annual_projection": 600000,
  "vat_registered": false,
  "tax_registered": true
}
```

---

### 10. Update Progress
**POST** `/update_progress`

Track user progress for reinforcement learning.

**Request Body:**
```json
{
  "type": "course_completed",
  "details": "Completed Google Data Analytics Certificate"
}
```

**Progress Types:**
- `course_completed`
- `job_applied`
- `interview`
- `hired`

**Response:**
```json
{
  "message": "Progress updated! This helps improve recommendations for other users.",
  "total_updates": 3,
  "reinforcement_learning": "Your success helps train our AI to better help other youth!"
}
```

---

### 11. Chatbot Page
**GET** `/chat`

Returns the AI chatbot interface page.

**Response:** HTML page

---

### 12. User Dashboard
**GET** `/dashboard`

Returns user dashboard with complete journey overview.

**Response:** HTML page with user data

---

## Data Models

### User Profile
```json
{
  "name": "string",
  "age": "integer",
  "location": "string",
  "education_level": "string",
  "signup_date": "ISO 8601 datetime"
}
```

### Skills Profile
```json
{
  "communication": "integer (0-100)",
  "problem_solving": "integer (0-100)",
  "creativity": "integer (0-100)",
  "technology": "integer (0-100)",
  "leadership": "integer (0-100)",
  "analytical": "integer (0-100)",
  "hands_on": "integer (0-100)",
  "sales": "integer (0-100)"
}
```

### Career Pathway
```json
{
  "name": "string",
  "icon": "string (emoji)",
  "description": "string",
  "careers": ["array of strings"],
  "courses": [
    {
      "name": "string",
      "provider": "string",
      "cost": "string",
      "duration": "string"
    }
  ],
  "success_rate": "integer (0-100)"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid input data",
  "details": "Age must be between 16 and 35"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting

Currently no rate limiting in development. For production:
- **Rate Limit:** 100 requests per minute per IP
- **Burst:** 20 requests per second
- **Headers:**
  - `X-RateLimit-Limit`: Maximum requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

---

## Authentication

Current version uses session-based authentication. For production API:

### Bearer Token Authentication
```
Authorization: Bearer <your-api-token>
```

### API Key Authentication
```
X-API-Key: <your-api-key>
```

---

## Webhooks (Future)

### Progress Update Webhook
```json
{
  "event": "progress.updated",
  "user_id": "12345",
  "progress_type": "hired",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Pathway Completion Webhook
```json
{
  "event": "pathway.completed",
  "user_id": "12345",
  "pathway_id": "digital_economy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## SDK Examples

### Python
```python
import requests

BASE_URL = "http://localhost:5001"

# Sign up
response = requests.post(f"{BASE_URL}/signup", json={
    "name": "Thabo",
    "age": 23,
    "location": "Gauteng",
    "education_level": "Matric"
})

# Get coach questions
response = requests.post(f"{BASE_URL}/coach_chat", json={"responses": []})
questions = response.json()["questions"]

# Submit responses
responses = ["I love coding", "I'm good at problem solving", ...]
response = requests.post(f"{BASE_URL}/coach_chat", json={"responses": responses})
skills = response.json()["skills_profile"]
```

### JavaScript
```javascript
const BASE_URL = "http://localhost:5001";

// Sign up
const signup = async () => {
  const response = await fetch(`${BASE_URL}/signup`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      name: "Thabo",
      age: 23,
      location: "Gauteng",
      education_level: "Matric"
    })
  });
  return await response.json();
};

// Chat with AI
const chatbot = async (message) => {
  const response = await fetch(`${BASE_URL}/chatbot`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  });
  return await response.json();
};
```

### cURL
```bash
# Sign up
curl -X POST http://localhost:5001/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Thabo","age":23,"location":"Gauteng","education_level":"Matric"}'

# Chatbot
curl -X POST http://localhost:5001/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message":"How do I write a CV?"}'
```

---

## Testing

### Postman Collection
Import the Postman collection for easy API testing:
[Download Collection](./postman_collection.json)

### Test Credentials
```
Name: Test User
Age: 23
Location: Gauteng
Education: Matric
```

---

## Changelog

### v1.0.0 (Current)
- Initial release
- Complete user journey flow
- AI skills analysis
- Career pathway recommendations
- Hidden job market scanner
- Wellness support
- Peer matching
- VAT/Tax tracker
- AI chatbot

---

**📡 API Documentation Complete**
