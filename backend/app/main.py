from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from app.routers import users, businesses, accountants, auth
from app.database import engine
from app.models import Base
from app.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION, CORS_ORIGINS,
    API_CONTACT, API_LICENSE
)
from datetime import datetime

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app with enhanced OpenAPI configuration
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact=API_CONTACT,
    license_info=API_LICENSE,
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.apex-am.com", "description": "Production server"}
    ],
    tags_metadata=[
        {
            "name": "Authentication",
            "description": "Operations for user authentication and authorization. Includes login endpoints and token management.",
            "externalDocs": {
                "description": "Authentication Guide",
                "url": "https://docs.apex-am.com/auth",
            },
        },
        {
            "name": "Users",
            "description": "Manage user accounts, roles, and permissions. Supports CRUD operations for user management.",
        },
        {
            "name": "Accountants",
            "description": "Manage accountant profiles and assignments. Includes super accountant hierarchy and business assignments.",
        },
        {
            "name": "Businesses",
            "description": "Business management operations including creation, updates, and financial metrics tracking.",
        },
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(accountants.router, prefix="/accountants", tags=["Accountants"])
app.include_router(businesses.router, prefix="/businesses", tags=["Businesses"])

def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    
    # Add custom security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter the JWT token in the value below. Example: 'Bearer <JWT>'"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [
        {
            "BearerAuth": []
        }
    ]
    
    # Add additional info
    openapi_schema["info"]["x-logo"] = {
        "url": "https://apex-am.com/logo.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Root endpoint
@app.get("/", 
    summary="API Root",
    description="Welcome endpoint providing basic API information and links to documentation.",
    response_description="API information and documentation links",
    tags=["API Information"]
)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Apex AM API",
        "version": API_VERSION,
        "description": "Accounting Management System API with Role-Based Access Control",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "endpoints": {
            "authentication": "/auth",
            "users": "/users",
            "accountants": "/accountants",
            "businesses": "/businesses"
        }
    }

# Health check endpoint
@app.get("/health",
    summary="Health Check",
    description="Check if the API is running and healthy. Useful for monitoring and load balancers.",
    response_description="Health status of the API",
    tags=["API Information"]
)
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

# API Info endpoint
@app.get("/api-info",
    summary="API Information",
    description="Detailed information about the API including version, features, and capabilities.",
    response_description="Comprehensive API information",
    tags=["API Information"]
)
async def api_info():
    """Get detailed API information."""
    return {
        "title": API_TITLE,
        "version": API_VERSION,
        "description": API_DESCRIPTION,
        "features": [
            "Role-based access control",
            "JWT authentication",
            "User management",
            "Accountant hierarchy management",
            "Business management",
            "Financial metrics tracking"
        ],
        "authentication": {
            "type": "JWT Bearer Token",
            "endpoint": "/auth/login",
            "description": "Use email and password to obtain JWT token"
        }
    }

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global exception handler for HTTP errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.status_code,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)