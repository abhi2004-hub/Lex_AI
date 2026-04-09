#!/usr/bin/env python3
"""
Test with small file
"""

import requests

def test_small_upload():
    """Test upload with small file"""
    
    # Test small file
    file_path = 'test_small.txt'
    
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        print(f"📄 Testing small file upload...")
        print(f"📄 File: {file_path}")
        print(f"📄 Size: {len(file_content)} characters")
        
        files = {
            'file': (file_path, file_content, 'text/plain')
        }
        
        data = {
            'analysis_type': 'detailed',
            'language': 'en'
        }
        
        print("📤 Sending to backend...")
        
        response = requests.post(
            'http://localhost:5000/api/documents/upload',
            files=files,
            data=data,
            timeout=10
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Document ID: {result.get('document', {}).get('id')}")
            print(f"📊 Clauses: {result.get('analysis', {}).get('total_clauses', 0)}")
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_small_upload()
