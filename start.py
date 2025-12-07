#!/usr/bin/env python3
"""
Simple startup script for Youth Compass AI
Shows clear status messages and error handling
"""

import sys
import os

print("=" * 70)
print("🧭 Youth Compass AI - Starting Application")
print("=" * 70)

# Check Python version
print(f"\n✓ Python version: {sys.version.split()[0]}")

# Check Flask
try:
    import flask
    print(f"✓ Flask version: {flask.__version__}")
except ImportError:
    print("✗ Flask not found! Installing...")
    os.system("pip3 install flask")
    import flask
    print(f"✓ Flask installed: {flask.__version__}")

# Import the app
print("\n📦 Loading application...")
try:
    from app import app
    print("✓ Application loaded successfully")
except Exception as e:
    print(f"✗ Error loading application: {e}")
    sys.exit(1)

# Start the server
print("\n" + "=" * 70)
print("🚀 Starting Flask Server")
print("=" * 70)
print("\n📱 Access Points:")
print("   Main Platform:  http://localhost:5001")
print("   AI Chatbot:     http://localhost:5001/chat")
print("   Dashboard:      http://localhost:5001/dashboard")
print("\n💡 Tips:")
print("   - Open the URL in your browser")
print("   - Press Ctrl+C to stop the server")
print("   - Check the terminal for any errors")
print("\n" + "=" * 70)
print("Server is starting...\n")

try:
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
except KeyboardInterrupt:
    print("\n\n👋 Server stopped by user")
except Exception as e:
    print(f"\n\n✗ Server error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if port 5001 is already in use")
    print("2. Try running: lsof -ti:5001 | xargs kill -9")
    print("3. Try a different port by editing app.py")
    sys.exit(1)
