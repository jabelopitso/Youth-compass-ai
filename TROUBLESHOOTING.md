# 🔧 Troubleshooting Guide - Youth Compass AI

## Common Issues & Solutions

### Issue 1: "Couldn't connect to server"

#### Solution A: Start the server properly
```bash
# Method 1: Use the new start script
python3 start.py

# Method 2: Use the original app
python3 app.py

# Method 3: Use the shell script
./run.sh
```

#### Solution B: Check if server is running
```bash
# Check if process is running
ps aux | grep python

# Check if port 5001 is in use
lsof -ti:5001
```

#### Solution C: Kill existing process
```bash
# Kill any process on port 5001
lsof -ti:5001 | xargs kill -9

# Then restart
python3 start.py
```

---

### Issue 2: "Port already in use"

#### Solution: Use a different port
```bash
# Edit app.py and change port 5001 to 5002
# Or run directly:
python3 -c "from app import app; app.run(port=5002)"
```

---

### Issue 3: "Flask not found"

#### Solution: Install Flask
```bash
# Install Flask
pip3 install flask

# Or install from requirements
pip3 install -r requirements.txt

# If permission denied, use --user flag
pip3 install --user flask
```

---

### Issue 4: "Module not found" errors

#### Solution: Check Python path
```bash
# Make sure you're in the project directory
cd /Users/jabelo/IdeaProjects/Youth-compass-ai

# Check Python version
python3 --version

# Verify Flask installation
python3 -c "import flask; print(flask.__version__)"
```

---

### Issue 5: Browser shows "This site can't be reached"

#### Checklist:
1. ✅ Is the server running? (Check terminal for "Running on...")
2. ✅ Is the URL correct? (http://localhost:5001)
3. ✅ Try 127.0.0.1 instead: http://127.0.0.1:5001
4. ✅ Check firewall settings
5. ✅ Try a different browser

---

### Issue 6: Server starts but pages don't load

#### Solution: Check templates
```bash
# Verify templates exist
ls -la templates/

# Should show:
# - index.html
# - dashboard.html
# - chatbot.html
```

---

### Issue 7: "Address already in use"

#### Solution: Change the port
```bash
# Quick fix - use port 5002
python3 -c "from app import app; app.run(host='0.0.0.0', port=5002, debug=True)"

# Then access at: http://localhost:5002
```

---

## Quick Diagnostic Script

Run this to check everything:

```bash
python3 << 'EOF'
import sys
import os

print("🔍 Youth Compass AI - Diagnostic Check\n")

# Check Python
print(f"✓ Python: {sys.version.split()[0]}")

# Check Flask
try:
    import flask
    print(f"✓ Flask: {flask.__version__}")
except:
    print("✗ Flask: NOT INSTALLED")

# Check files
files = ['app.py', 'templates/index.html', 'templates/dashboard.html', 'templates/chatbot.html']
for f in files:
    if os.path.exists(f):
        print(f"✓ {f}: EXISTS")
    else:
        print(f"✗ {f}: MISSING")

# Check port
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5001))
if result == 0:
    print("⚠ Port 5001: IN USE")
else:
    print("✓ Port 5001: AVAILABLE")
sock.close()

print("\n✅ Diagnostic complete!")
EOF
```

---

## Step-by-Step Server Start

### 1. Open Terminal
```bash
cd /Users/jabelo/IdeaProjects/Youth-compass-ai
```

### 2. Verify Setup
```bash
python3 test_app.py
```

### 3. Start Server
```bash
python3 start.py
```

### 4. Open Browser
```
http://localhost:5001
```

### 5. Verify It's Working
You should see:
- Beautiful gradient background
- "Youth Compass AI" title
- Sign-up form

---

## Still Having Issues?

### Check Server Output
Look for these messages in terminal:
```
✓ Application loaded successfully
🚀 Starting Flask Server
* Running on http://0.0.0.0:5001
* Running on http://127.0.0.1:5001
```

### Try Alternative Access Methods
```bash
# Try localhost
http://localhost:5001

# Try 127.0.0.1
http://127.0.0.1:5001

# Try 0.0.0.0
http://0.0.0.0:5001
```

### Check for Errors
Common error messages and fixes:

**"Address already in use"**
→ Port 5001 is busy, use different port

**"Permission denied"**
→ Use sudo or change port to 8000+

**"Module not found"**
→ Install missing module with pip3

**"Template not found"**
→ Check templates/ directory exists

---

## Emergency Reset

If nothing works, try this complete reset:

```bash
# 1. Kill all Python processes
pkill -9 python3

# 2. Clear any cached files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 3. Reinstall Flask
pip3 install --force-reinstall flask

# 4. Restart server
python3 start.py
```

---

## Contact & Support

If you're still stuck:

1. **Check the error message** in terminal
2. **Copy the full error** text
3. **Note what you were doing** when it failed
4. **Check the logs** for more details

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python3 start.py` | Start server (recommended) |
| `python3 app.py` | Start server (alternative) |
| `python3 test_app.py` | Run tests |
| `lsof -ti:5001` | Check port usage |
| `lsof -ti:5001 \| xargs kill -9` | Kill process on port |
| `pip3 install flask` | Install Flask |

---

**🎯 Most Common Fix:**
```bash
# Kill any existing process and restart
lsof -ti:5001 | xargs kill -9
python3 start.py
```

Then open: http://localhost:5001

---

**✅ Server is working when you see:**
```
* Running on http://0.0.0.0:5001
* Running on http://127.0.0.1:5001
```

**🌐 Then open your browser to:**
```
http://localhost:5001
```

---

Good luck! 🚀
