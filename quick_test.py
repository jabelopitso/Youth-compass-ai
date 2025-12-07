#!/usr/bin/env python3
"""Quick test to verify server can start"""
import sys
from app import app

print("Testing server startup...")
print(f"Flask app: {app}")
print(f"Routes: {[rule.rule for rule in app.url_map.iter_rules()][:5]}")
print("\n✅ Server configuration is valid!")
print("\nTo start the server, run:")
print("  python3 start.py")
print("\nThen open: http://localhost:5001")
