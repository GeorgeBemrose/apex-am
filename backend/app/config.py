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
API_DESCRIPTION = os.getenv("API_DESCRIPTION", "Accounting Management System API with Role-Based Access Control")
API_VERSION = os.getenv("API_VERSION", "1.0.0")

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
