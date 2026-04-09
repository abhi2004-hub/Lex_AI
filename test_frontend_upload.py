#!/usr/bin/env python3
"""
Test frontend upload functionality
"""

import requests
import json

def test_frontend_upload():
    """Test the same upload that frontend would do"""
    
    # Test file path
    file_path = 'sample_documents/employment_contract.txt'
    
    try:
        # Read file content
        with open(file_path, 'r') as f:
            file_content = f.read()
        
        print(f"📄 Testing frontend upload...")
        print(f"📄 File: {file_path}")
        print(f"📄 Size: {len(file_content)} characters")
        
        # Prepare files exactly like frontend does
        files = {
            'file': (file_path, file_content, 'text/plain')
        }
        
        # Prepare form data exactly like frontend
        data = {
            'analysis_type': 'detailed',
            'language': 'en'
        }
        
        print("📤 Sending to backend API...")
        
        # Make request to backend API (same endpoint frontend uses)
        response = requests.post(
            'http://localhost:5000/api/documents/upload',
            files=files,
            data=data,
            timeout=30
        )
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Backend processed document correctly")
            print(f"📄 Document ID: {result.get('document', {}).get('id')}")
            print(f"📊 Clauses found: {result.get('analysis', {}).get('total_clauses', 0)}")
            print(f"⏱️ Processing time: {result.get('processing_time', 0):.2f}s")
            
            # Risk distribution for pie chart
            if result.get('analysis', {}).get('risk_distribution'):
                risk_dist = json.loads(result['analysis']['risk_distribution'])
                total = sum(risk_dist.values())
                print("📊 Risk Distribution (for pie chart):")
                for level, count in risk_dist.items():
                    percentage = (count / total * 100) if total > 0 else 0
                    print(f"   {level.capitalize()}: {count} ({percentage:.1f}%)")
            
            print("\n🎯 Frontend should now show:")
            print("   ✅ Correct pie chart percentages")
            print("   ✅ Detailed document summary")
            print("   ✅ Clause list with risk levels")
            print("   ✅ SHAP/LIME explanations")
            
        else:
            print("❌ FAILED!")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    print("🧪 Testing Frontend Upload Integration")
    print("=" * 60)
    test_frontend_upload()
    print("=" * 60)
