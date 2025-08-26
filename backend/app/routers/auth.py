from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import authenticate_user, create_access_token
from app.schemas import Token, UserLogin

router = APIRouter()

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login endpoint to get access token using email as username."""
    # For backward compatibility, we'll accept email in the username field
    email = form_data.username
    user = authenticate_user(db, email, form_data.password, use_email=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json")
async def login_with_json(
    request: Request,
    db: Session = Depends(get_db)
):
    """Alternative login endpoint using JSON with email."""
    try:
        print("Starting login-json request")
        body = await request.json()
        print(f"Request body: {body}")
        
        email = body.get("email")
        password = body.get("password")
        print(f"Email: {email}, Password: {password}")
        
        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password are required"
            )
        
        print("Calling authenticate_user")
        user = authenticate_user(db, email, password, use_email=True)
        print(f"Authenticate result: {user}")
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print("Creating access token")
        access_token = create_access_token(data={"sub": user.username})
        print("Login successful")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except ValueError as e:
        # JSON parsing error
        print(f"JSON parsing error: {e}")
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
