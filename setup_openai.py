#!/usr/bin/env python3
"""
Setup script for OpenAI integration
Run this to install OpenAI and set up your API key
"""

import subprocess
import sys
import os

def install_openai():
    """Install OpenAI package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==0.28.1"])
        print("✅ OpenAI package installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install OpenAI package")
        return False

def setup_api_key():
    """Guide user through API key setup"""
    print("\n🔑 OpenAI API Key Setup")
    print("=" * 40)
    print("1. Go to: https://platform.openai.com/api-keys")
    print("2. Create a new API key")
    print("3. Copy your API key")
    print("4. Set it as environment variable:")
    print("   export OPENAI_API_KEY='your-api-key-here'")
    print("\nOr create a .env file with:")
    print("OPENAI_API_KEY=your-api-key-here")
    
    api_key = input("\n🔑 Paste your OpenAI API key here (or press Enter to skip): ").strip()
    
    if api_key:
        # Create .env file
        with open('.env', 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
        print("✅ API key saved to .env file!")
        
        # Also set environment variable for current session
        os.environ['OPENAI_API_KEY'] = api_key
        print("✅ API key set for current session!")
        return True
    else:
        print("⚠️  Skipping API key setup. App will use fallback responses.")
        return False

def test_api():
    """Test OpenAI API connection"""
    try:
        import openai
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  No API key found. Using fallback mode.")
            return False
            
        openai.api_key = api_key
        
        # Test with a simple request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        print("App will use fallback responses.")
        return False

def main():
    print("🚀 YouthCompass AI - OpenAI Setup")
    print("=" * 40)
    
    # Install OpenAI package
    if install_openai():
        # Setup API key
        if setup_api_key():
            # Test API
            test_api()
    
    print("\n🎯 Setup complete!")
    print("Run: python3 simple_app.py")
    print("Then visit: http://localhost:5000")

if __name__ == "__main__":
    main()