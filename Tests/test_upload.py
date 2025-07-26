#!/usr/bin/env python3
"""
Simple test script to debug file upload issue
"""

import requests
import os

def test_upload():
    # Test file upload endpoint
    url = 'http://localhost:3000/submit-upload'
    
    # Create a small test file
    test_content = b"This is a test video file content"
    
    try:
        # Prepare the file for upload
        files = {'video_file': ('test.mp4', test_content, 'video/mp4')}
        data = {'model_size': 'tiny'}
        
        print("Testing file upload...")
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    test_upload()
