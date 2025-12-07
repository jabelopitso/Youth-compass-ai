#!/usr/bin/env python3
"""
Test script for Youth Compass AI
Verifies all endpoints and functionality
"""

import sys
import json

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    try:
        from flask import Flask, render_template, request, jsonify, session
        import json
        import os
        from datetime import datetime
        import random
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_templates():
    """Test if all template files exist"""
    print("\n🔍 Testing template files...")
    templates = ['index.html', 'dashboard.html', 'chatbot.html']
    all_exist = True
    
    for template in templates:
        path = f'templates/{template}'
        if os.path.exists(path):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            all_exist = False
    
    return all_exist

def test_app_structure():
    """Test if app.py has correct structure"""
    print("\n🔍 Testing app structure...")
    try:
        from app import app, CAREER_PATHWAYS, SKILLS_KEYWORDS, COACH_QUESTIONS
        print(f"✅ App initialized")
        print(f"✅ {len(CAREER_PATHWAYS)} career pathways loaded")
        print(f"✅ {len(SKILLS_KEYWORDS)} skill categories defined")
        print(f"✅ {len(COACH_QUESTIONS)} coach questions ready")
        return True
    except Exception as e:
        print(f"❌ App structure error: {e}")
        return False

def test_routes():
    """Test if all routes are defined"""
    print("\n🔍 Testing routes...")
    try:
        from app import app
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        
        expected_routes = [
            '/',
            '/signup',
            '/coach_chat',
            '/generate_pathway',
            '/find_opportunities',
            '/wellness_support',
            '/find_peers',
            '/chatbot',
            '/vat_tracker',
            '/update_progress',
            '/chat',
            '/dashboard'
        ]
        
        all_present = True
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} defined")
            else:
                print(f"❌ Route {route} missing")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"❌ Route testing error: {e}")
        return False

def test_ai_functions():
    """Test AI analysis functions"""
    print("\n🔍 Testing AI functions...")
    try:
        from app import analyze_skills_from_responses, recommend_pathway, find_hidden_opportunities
        
        # Test skills analysis
        test_responses = [
            "I love working with computers and solving technical problems",
            "I enjoy helping people and explaining things clearly",
            "I'm good at organizing events and leading teams"
        ]
        skills = analyze_skills_from_responses(test_responses)
        print(f"✅ Skills analysis working: {len(skills)} skills detected")
        
        # Test pathway recommendation
        pathway_id, pathway = recommend_pathway(skills, {'location': 'Gauteng'})
        print(f"✅ Pathway recommendation working: {pathway['name']}")
        
        # Test opportunity finder
        opportunities = find_hidden_opportunities('Johannesburg', skills)
        print(f"✅ Opportunity finder working: {len(opportunities)} opportunities found")
        
        return True
    except Exception as e:
        print(f"❌ AI function error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧭 Youth Compass AI - System Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Templates", test_templates()))
    results.append(("App Structure", test_app_structure()))
    results.append(("Routes", test_routes()))
    results.append(("AI Functions", test_ai_functions()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   python3 app.py")
        print("   or")
        print("   ./run.sh")
        print("\n📱 Then visit: http://localhost:5001")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        return False

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = run_all_tests()
    sys.exit(0 if success else 1)
