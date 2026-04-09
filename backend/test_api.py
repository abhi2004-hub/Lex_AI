"""
Simple API test for LexAI Backend
"""

import requests
import json

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

def test_model_info():
    """Test the model info endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/models/info')
        print(f"Model info status: {response.status_code}")
        if response.status_code == 200:
            print(f"Models available: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    print("Testing LexAI Backend API...")
    print("=" * 50)
    
    print("\n1. Testing health endpoint...")
    test_health_endpoint()
    
    print("\n2. Testing model info endpoint...")
    test_model_info()
    
    print("\n" + "=" * 50)
    print("API testing complete!")
