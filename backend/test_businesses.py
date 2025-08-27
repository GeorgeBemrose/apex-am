#!/usr/bin/env python3
"""
Simple test script to check businesses endpoint functionality
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "admin@apexam.com"  # Replace with your actual admin email
TEST_PASSWORD = "your_password"   # Replace with your actual admin password

def test_businesses_endpoint():
    """Test the businesses endpoint"""
    
    print("Testing Apex AM API Businesses Endpoint")
    print("=" * 50)
    
    # Step 1: Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Health check failed: {e}")
        return
    
    # Step 2: Test root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Root endpoint: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Root endpoint failed: {e}")
        return
    
    # Step 3: Login to get access token
    print("\n3. Testing authentication...")
    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/auth/login-json", json=login_data)
        print(f"   Login response: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"   Access token obtained: {access_token[:20]}...")
        else:
            print(f"   Login failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   Login failed: {e}")
        return
    
    # Step 4: Test businesses endpoint with authentication
    print("\n4. Testing businesses endpoint...")
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{BASE_URL}/businesses/", headers=headers)
        print(f"   Businesses endpoint: {response.status_code}")
        
        if response.status_code == 200:
            businesses = response.json()
            print(f"   Success! Found {len(businesses)} businesses")
            if businesses:
                print(f"   First business: {businesses[0].get('name', 'N/A')}")
        else:
            print(f"   Businesses endpoint failed: {response.text}")
            
    except Exception as e:
        print(f"   Businesses endpoint failed: {e}")
    
    # Step 5: Test businesses endpoint without authentication
    print("\n5. Testing businesses endpoint without authentication...")
    try:
        response = requests.get(f"{BASE_URL}/businesses/")
        print(f"   Businesses endpoint (no auth): {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Businesses endpoint (no auth) failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_businesses_endpoint()
