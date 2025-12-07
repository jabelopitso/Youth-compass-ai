# 🚀 START HERE - Youth Compass AI

## Quick Start (3 Steps)

### Step 1: Open Terminal
```bash
cd /Users/jabelo/IdeaProjects/Youth-compass-ai
```

### Step 2: Start the Server
```bash
python3 start.py
```

You should see:
```
======================================================================
🧭 Youth Compass AI - Starting Application
======================================================================

✓ Python version: 3.x.x
✓ Flask version: 2.3.3

📦 Loading application...
✓ Application loaded successfully

======================================================================
🚀 Starting Flask Server
======================================================================

📱 Access Points:
   Main Platform:  http://localhost:5001
   AI Chatbot:     http://localhost:5001/chat
   Dashboard:      http://localhost:5001/dashboard

💡 Tips:
   - Open the URL in your browser
   - Press Ctrl+C to stop the server
   - Check the terminal for any errors

======================================================================
Server is starting...

 * Running on http://0.0.0.0:5001
 * Running on http://127.0.0.1:5001
```

### Step 3: Open Browser
Go to: **http://localhost:5001**

---

## If You Get "Couldn't Connect to Server"

### Fix 1: Check if server is actually running
Look at your terminal - you should see "Running on http://..."

### Fix 2: Try different URL
- http://localhost:5001
- http://127.0.0.1:5001

### Fix 3: Port might be in use
```bash
# Kill any process on port 5001
lsof -ti:5001 | xargs kill -9

# Then restart
python3 start.py
```

### Fix 4: Use different port
```bash
python3 -c "from app import app; app.run(host='0.0.0.0', port=5002, debug=True)"
```
Then open: http://localhost:5002

---

## Alternative Start Methods

### Method 1: Using start.py (Recommended)
```bash
python3 start.py
```

### Method 2: Using app.py
```bash
python3 app.py
```

### Method 3: Using shell script
```bash
./run.sh
```

---

## Verify Everything Works

Before starting, run tests:
```bash
python3 test_app.py
```

Should show:
```
✅ PASS - Imports
✅ PASS - Templates
✅ PASS - App Structure
✅ PASS - Routes
✅ PASS - AI Functions

Total: 5/5 tests passed
```

---

## What You Should See

### In Terminal:
```
* Running on http://0.0.0.0:5001
* Running on http://127.0.0.1:5001
```

### In Browser:
- Beautiful purple gradient background
- "🧭 Youth Compass AI" title
- "Complete Life Direction Platform for South African Youth"
- Sign-up form with name, age, location, education fields

---

## Need More Help?

See **TROUBLESHOOTING.md** for detailed solutions to common issues.

---

## Quick Commands

```bash
# Start server
python3 start.py

# Run tests
python3 test_app.py

# Check if port is free
lsof -ti:5001

# Kill process on port
lsof -ti:5001 | xargs kill -9

# Install Flask (if needed)
pip3 install flask
```

---

**🎯 Most Important:**

1. Run: `python3 start.py`
2. Wait for "Running on http://..."
3. Open: http://localhost:5001
4. Enjoy! 🎉

---

**Still stuck?** Check TROUBLESHOOTING.md or the error message in your terminal.
