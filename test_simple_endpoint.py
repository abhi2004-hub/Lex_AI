#!/usr/bin/env python3
"""
Test simple endpoint
"""

import requests

def test_simple_endpoint():
    """Test the simple test endpoint"""
    
    file_path = 'test_small.txt'
    
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        print(f"📄 Testing simple endpoint...")
        print(f"📄 File: {file_path}")
        print(f"📄 Size: {len(file_content)} characters")
        
        files = {
            'file': (file_path, file_content, 'text/plain')
        }
        
        print("📤 Sending to simple test server...")
        
        response = requests.post(
            'http://localhost:5001/test',
            files=files,
            timeout=10
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_simple_endpoint()
