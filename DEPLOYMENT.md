# 🚀 Deployment Guide - Youth Compass AI

## Production Deployment Options

### Option 1: Heroku (Easiest)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
```bash
# Login to Heroku
heroku login

# Create app
heroku create youth-compass-ai

# Add Procfile
echo "web: gunicorn app:app" > Procfile

# Update requirements.txt
echo "Flask==3.0.0" > requirements.txt
echo "gunicorn==21.2.0" >> requirements.txt

# Deploy
git init
git add .
git commit -m "Initial deployment"
git push heroku main

# Open app
heroku open
```

#### Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set FLASK_ENV=production
```

---

### Option 2: AWS Elastic Beanstalk

#### Prerequisites
- AWS account
- EB CLI installed

#### Steps
```bash
# Initialize EB
eb init -p python-3.9 youth-compass-ai

# Create environment
eb create youth-compass-production

# Deploy
eb deploy

# Open app
eb open
```

#### Configuration (.ebextensions/python.config)
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

---

### Option 3: Google Cloud Run

#### Prerequisites
- Google Cloud account
- gcloud CLI installed

#### Steps
```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT app:app
EOF

# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/youth-compass-ai
gcloud run deploy youth-compass-ai --image gcr.io/PROJECT_ID/youth-compass-ai --platform managed
```

---

### Option 4: DigitalOcean App Platform

#### Prerequisites
- DigitalOcean account

#### Steps
1. Connect GitHub repository
2. Select Python app
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn app:app`
5. Deploy

---

### Option 5: Traditional VPS (Ubuntu)

#### Prerequisites
- Ubuntu 20.04+ server
- Domain name (optional)

#### Steps
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone <your-repo-url>
cd youth-compass-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/youth-compass.service
```

#### Service File Content
```ini
[Unit]
Description=Youth Compass AI
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/youth-compass-ai
Environment="PATH=/path/to/youth-compass-ai/venv/bin"
ExecStart=/path/to/youth-compass-ai/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Start Services
```bash
# Enable and start service
sudo systemctl enable youth-compass
sudo systemctl start youth-compass

# Configure nginx
sudo ln -s /etc/nginx/sites-available/youth-compass /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Production Checklist

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Set FLASK_ENV=production
- [ ] Disable debug mode
- [ ] Add CORS headers if needed
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Sanitize user inputs

### Database
- [ ] Replace session storage with PostgreSQL/MongoDB
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Add database migrations (Alembic)

### Performance
- [ ] Enable caching (Redis)
- [ ] Add CDN for static files
- [ ] Compress responses (gzip)
- [ ] Optimize images
- [ ] Implement lazy loading
- [ ] Add database indexing

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Add application monitoring (New Relic/DataDog)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Add analytics (Google Analytics)

### Scalability
- [ ] Configure auto-scaling
- [ ] Set up load balancer
- [ ] Implement caching strategy
- [ ] Add queue system (Celery/RQ)
- [ ] Optimize database queries

---

## Environment Variables

Create `.env` file for production:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=production
FLASK_DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# External APIs
WHATSAPP_API_KEY=your-whatsapp-api-key
SMS_API_KEY=your-sms-api-key

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

---

## Production Updates

### Update requirements.txt for production
```txt
Flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
redis==5.0.1
python-dotenv==1.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Cors==4.0.0
celery==5.3.4
sentry-sdk[flask]==1.39.1
```

### Update app.py for production
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
```

---

## Database Migration

### Install Alembic
```bash
pip install alembic
alembic init migrations
```

### Create Models
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    location = db.Column(db.String(100))
    # ... more fields
```

### Run Migrations
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## SSL/HTTPS Setup (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Backup Strategy

### Database Backups
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump youth_compass > /backups/db_$DATE.sql
find /backups -name "db_*.sql" -mtime +7 -delete
```

### Application Backups
```bash
# Backup application files
tar -czf /backups/app_$(date +%Y%m%d).tar.gz /path/to/youth-compass-ai
```

---

## Monitoring Setup

### Sentry Integration
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

---

## Performance Optimization

### Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': os.getenv('REDIS_URL')})

@app.route('/pathways')
@cache.cached(timeout=300)
def get_pathways():
    return jsonify(CAREER_PATHWAYS)
```

### Compress Responses
```python
from flask_compress import Compress

Compress(app)
```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (AWS ELB, Nginx)
- Stateless application design
- Shared session storage (Redis)
- Database connection pooling

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layers
- Use CDN for static assets

---

## Support & Maintenance

### Regular Tasks
- [ ] Monitor error logs daily
- [ ] Review performance metrics weekly
- [ ] Update dependencies monthly
- [ ] Backup verification weekly
- [ ] Security patches as needed

### Emergency Contacts
- DevOps: devops@youthcompass.co.za
- Database: dba@youthcompass.co.za
- Security: security@youthcompass.co.za

---

**🚀 Ready for production deployment!**
