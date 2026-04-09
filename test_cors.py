#!/usr/bin/env python3
"""
Test CORS and exact frontend request
"""

import requests

def test_cors():
    """Test exact request like frontend"""
    
    try:
        # Create FormData exactly like frontend
        files = {
            'file': ('employment_contract.txt', open('sample_documents/employment_contract.txt', 'r').read(), 'text/plain')
        }
        
        data = {
            'analysis_type': 'detailed',
            'language': 'en'
        }
        
        print("🧪 Testing exact frontend request...")
        print("📤 Sending to http://localhost:5000/api/documents/upload")
        
        # Make request exactly like frontend
        response = requests.post(
            'http://localhost:5000/api/documents/upload',
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"📄 Document ID: {result.get('document', {}).get('id')}")
            print(f"📊 Clauses: {result.get('analysis', {}).get('total_clauses', 0)}")
            
            # Check CORS headers
            print("\n🌐 CORS Headers:")
            for header, value in response.headers.items():
                if 'cors' in header.lower() or 'access' in header.lower():
                    print(f"   {header}: {value}")
                    
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_cors()
