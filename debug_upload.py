#!/usr/bin/env python3
"""
Debug upload to identify the exact error
"""

import requests
import json

def debug_upload():
    """Debug the upload process step by step"""
    
    print("🔍 DEBUGGING UPLOAD PROCESS")
    print("=" * 50)
    
    # Test 1: Check backend health
    print("1. Testing backend health...")
    try:
        r = requests.get('http://localhost:5000/health', timeout=5)
        print(f"   ✅ Backend health: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Backend health failed: {e}")
        return
    
    # Test 2: Check frontend
    print("2. Testing frontend...")
    try:
        r = requests.get('http://localhost:3000', timeout=5)
        print(f"   ✅ Frontend: {r.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend failed: {e}")
        return
    
    # Test 3: Test upload endpoint
    print("3. Testing upload endpoint...")
    try:
        with open('sample_documents/employment_contract.txt', 'r') as f:
            content = f.read()
        
        files = {
            'file': ('test.txt', content, 'text/plain')
        }
        data = {
            'analysis_type': 'detailed',
            'language': 'en'
        }
        
        r = requests.post('http://localhost:5000/api/documents/upload', 
                         files=files, data=data, timeout=10)
        
        print(f"   📊 Upload status: {r.status_code}")
        
        if r.status_code == 200:
            result = r.json()
            print("   ✅ Upload successful!")
            print(f"   📄 Document ID: {result.get('document', {}).get('id')}")
            print(f"   📊 Clauses: {result.get('analysis', {}).get('total_clauses', 0)}")
        else:
            print(f"   ❌ Upload failed: {r.text}")
            
    except Exception as e:
        print(f"   ❌ Upload exception: {e}")
    
    print("=" * 50)
    print("🎯 If all tests pass, the issue is in the browser/frontend")
    print("🌐 Try: http://localhost:3000/test_upload.html")

if __name__ == "__main__":
    debug_upload()
