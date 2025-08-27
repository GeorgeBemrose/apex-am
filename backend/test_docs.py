#!/usr/bin/env python3
"""
Test script to verify API documentation endpoints are working correctly.
Run this after starting the FastAPI server to test the documentation.
"""

import requests
import json
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, expected_status=200, description=""):
    """Test an endpoint and print the result."""
    url = urljoin(BASE_URL, endpoint)
    try:
        response = requests.get(url)
        status = "✅" if response.status_code == expected_status else "❌"
        print(f"{status} {endpoint} - {response.status_code} {description}")
        
        if response.status_code == 200 and endpoint == "/openapi.json":
            # Validate OpenAPI schema
            try:
                schema = response.json()
                required_fields = ["openapi", "info", "paths", "components"]
                missing_fields = [field for field in required_fields if field not in schema]
                
                if missing_fields:
                    print(f"   ⚠️  Missing OpenAPI fields: {missing_fields}")
                else:
                    print(f"   ✅ OpenAPI schema is valid")
                    
                # Check for security schemes
                if "components" in schema and "securitySchemes" in schema["components"]:
                    print(f"   ✅ Security schemes defined")
                else:
                    print(f"   ⚠️  No security schemes found")
                    
            except json.JSONDecodeError:
                print(f"   ❌ Invalid JSON response")
                
    except requests.exceptions.ConnectionError:
        print(f"❌ {endpoint} - Connection failed (server not running?)")
    except Exception as e:
        print(f"❌ {endpoint} - Error: {e}")

def main():
    """Test all documentation endpoints."""
    print("🧪 Testing API Documentation Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    test_endpoint("/", 200, "API root")
    test_endpoint("/health", 200, "Health check")
    test_endpoint("/api-info", 200, "API information")
    
    print("\n📚 Testing Documentation Endpoints")
    print("-" * 40)
    
    # Test documentation endpoints
    test_endpoint("/docs", 200, "Swagger UI")
    test_endpoint("/redoc", 200, "ReDoc")
    test_endpoint("/openapi.json", 200, "OpenAPI schema")
    
    print("\n🔐 Testing Authentication Endpoints")
    print("-" * 40)
    
    # Test auth endpoints (should return 422 for missing data, not 404)
    test_endpoint("/auth/login", 422, "Login endpoint (form)")
    test_endpoint("/auth/login-json", 422, "Login endpoint (JSON)")
    
    print("\n" + "=" * 50)
    print("🎯 Documentation Testing Complete!")
    print("\nTo view the documentation:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")
    print(f"   OpenAPI Schema: {BASE_URL}/openapi.json")

if __name__ == "__main__":
    main()
