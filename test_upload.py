#!/usr/bin/env python3
"""
Test script to upload document to LexAI backend
"""

import requests
import json

def test_upload():
    """Test document upload to backend API"""
    
    # File path
    file_path = 'sample_documents/employment_contract.txt'
    
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        # Prepare files for upload
        files = {
            'file': ('employment_contract.txt', file_content, 'text/plain')
        }
        
        # Prepare form data
        data = {
            'analysis_type': 'detailed',
            'language': 'en'
        }
        
        print("Uploading document to backend...")
        print(f"File: {file_path}")
        print(f"Analysis type: {data['analysis_type']}")
        print(f"Language: {data['language']}")
        print("-" * 50)
        
        # Make request
        response = requests.post(
            'http://localhost:5000/api/documents/upload',
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"Document ID: {result.get('document', {}).get('id')}")
            print(f"Total clauses: {result.get('analysis', {}).get('total_clauses', 0)}")
            print(f"Processing time: {result.get('analysis', {}).get('processing_time', 0):.2f}s")
            
            # Show risk distribution
            if result.get('analysis', {}).get('risk_distribution'):
                risk_dist = json.loads(result['analysis']['risk_distribution'])
                print("Risk Distribution:")
                for level, count in risk_dist.items():
                    print(f"  {level.capitalize()}: {count}")
            
            # Show first few clauses
            clauses = result.get('clauses', [])
            if clauses:
                print(f"\nFirst {min(3, len(clauses))} clauses:")
                for i, clause in enumerate(clauses[:3]):
                    risk_level = clause.get('risk_assessment', {}).get('risk_level', 'unknown')
                    confidence = clause.get('confidence_score', 0) * 100
                    print(f"  {i+1}. {clause.get('clause_type', 'Unknown')} - {risk_level.upper()} ({confidence:.1f}% confidence)")
                    print(f"     Text: {clause.get('clause_text', '')[:100]}...")
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_upload()
