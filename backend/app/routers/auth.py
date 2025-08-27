from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_access_token
from app.schemas import Token, LoginRequest

router = APIRouter()

@router.post("/login",
    summary="Login with OAuth2 Form",
    description="""
    Authenticate user and obtain JWT access token using OAuth2 password flow.
    
    **Note**: Use email in the username field for compatibility.
    
    **Security**: This endpoint is not protected and accepts email/password credentials.
    """,
    response_model=Token,
    response_description="JWT access token for authenticated user",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect email or password"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "username"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["Authentication"]
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login endpoint to get access token using email as username.
    
    This endpoint follows OAuth2 password flow standards and is compatible with
    standard OAuth2 clients. The email should be provided in the username field.
    
    Args:
        form_data: OAuth2 form data containing username (email) and password
        db: Database session dependency
        
    Returns:
        Token object containing JWT access token and type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # For backward compatibility, we'll accept email in the username field
    email = form_data.username
    user = authenticate_user(db, email, form_data.password, use_email=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json",
    summary="Login with JSON",
    description="""
    Alternative login endpoint using JSON payload instead of form data.
    
    This endpoint accepts a JSON request body with email and password fields.
    Useful for applications that prefer JSON over form-encoded data.
    
    **Security**: This endpoint is not protected and accepts email/password credentials.
    """,
    response_model=Token,
    response_description="JWT access token for authenticated user",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        400: {
            "description": "Bad request - missing or invalid data",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email and password are required"
                    }
                }
            }
        },
        401: {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Incorrect email or password"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid JSON format: Expecting property name enclosed in double quotes"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error: Database connection failed"
                    }
                }
            }
        }
    },
    tags=["Authentication"]
)
async def login_with_json(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Alternative login endpoint using JSON with email.
    
    This endpoint provides a JSON-based alternative to the OAuth2 form login.
    It's designed for applications that prefer JSON payloads over form data.
    
    Args:
        request: FastAPI request object for JSON parsing
        db: Database session dependency
        
    Returns:
        Token object containing JWT access token and type
        
    Raises:
        HTTPException: Various error codes for different failure scenarios
    """
    try:
        body = await request.json()
        
        email = body.get("email")
        password = body.get("password")
        
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )
        
        user = authenticate_user(db, email, password, use_email=True)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        # Re-raise HTTPExceptions as-is (like "Incorrect email or password")
        raise
    except ValueError as e:
        # JSON parsing error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON format: {str(e)}"
        )
    except Exception as e:
        # Log the actual error for debugging
        print(f"Login error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {type(e).__name__}: {str(e)}"
        )
