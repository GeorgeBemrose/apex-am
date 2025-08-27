import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./apex_am.db")

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

# API configuration
API_TITLE = os.getenv("API_TITLE", "Apex AM API")
API_DESCRIPTION = os.getenv("API_DESCRIPTION", """
# Apex AM API

A comprehensive **Accounting Management System API** with role-based access control for accountants, businesses, and administrators.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **User Management** - Complete user lifecycle management
- 🏢 **Business Management** - Business profile and financial tracking
- 👨‍💼 **Accountant Hierarchy** - Multi-level accountant management
- 📊 **Financial Metrics** - Business performance tracking
- 🛡️ **Role-Based Access Control** - Granular permission system

## Getting Started

1. **Authentication**: Use `/auth/login` to obtain JWT token
2. **Authorization**: Include token in `Authorization: Bearer <token>` header
3. **API Endpoints**: Explore available endpoints below

## Rate Limiting

- **Standard**: 100 requests per minute
- **Burst**: Up to 20 requests in a short period

For detailed usage examples and SDKs, visit our [Developer Portal](https://developers.apex-am.com).
""")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

# API Contact Information
API_CONTACT = {
    "name": "Apex AM Development Team",
    "email": "dev@apex-am.com",
    "url": "https://apex-am.com/support"
}

# API License Information
API_LICENSE = {
    "name": "MIT License",
    "url": "https://opensource.org/licenses/MIT"
}

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
