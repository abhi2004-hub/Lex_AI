#!/usr/bin/env python3
"""
Simple test to verify backend is working
"""

import requests

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("Testing LexAI Backend...")
    print("=" * 50)
    test_health()
    print("=" * 50)
