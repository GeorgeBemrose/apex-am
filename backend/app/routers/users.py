from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import (
    get_current_user, require_root_admin, require_super_accountant_or_root,
    require_accountant_or_higher
)
from app.models import User, Accountant
from app.schemas import UserCreate, User, UserUpdate, UserResponse, RoleAssignment
from app import crud

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin())
):
    """Create a new user (Root Admin only)."""
    try:
        # Convert Pydantic model to dictionary (Pydantic v1)
        user_data_dict = user_data.dict()
        created_user = crud.create_user(db=db, user_data=user_data_dict)
        # Convert SQLAlchemy model to Pydantic schema to exclude sensitive fields
        return UserResponse.from_orm(created_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.get("/")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root())
):
    """Get list of users (Super Accountant or Root Admin only)."""
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user



# IMPORTANT: More specific routes must come BEFORE generic /{user_id} routes
# This prevents FastAPI from matching DELETE /{user_id} to GET /{user_id}

@router.post("/{user_id}/assign-role")
async def assign_role(
    user_id: str,
    role_data: RoleAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin())
):
    """Assign a role to a user (Root Admin only)."""
    try:
        user = crud.get_user(db=db, user_id=user_id)
        
        # Update user role
        user_update_data = {"role": role_data.new_role}
        updated_user = crud.update_user(db=db, user_id=user_id, user_update_data=user_update_data)
        
        # If assigning super accountant role, create or update accountant record
        if role_data.new_role == "super_accountant":
            from app.models import Accountant
            existing_accountant = db.query(Accountant).filter(Accountant.user_id == user_id).first()
            if existing_accountant:
                # Update existing accountant record
                accountant_update_data = {
                    "is_super_accountant": True,
                    "super_accountant_id": None  # Super accountants don't have supervisors
                }
                crud.update_accountant(db=db, accountant_id=existing_accountant.id, accountant_update_data=accountant_update_data)
            else:
                # Create new accountant record
                accountant_data = {"user_id": user_id, "is_super_accountant": True}
                crud.create_accountant(db=db, accountant_data=accountant_data)
        
        # If assigning accountant role, create or update accountant record
        elif role_data.new_role == "accountant":
            from app.models import Accountant
            existing_accountant = db.query(Accountant).filter(Accountant.user_id == user_id).first()
            if existing_accountant:
                # Update existing accountant record
                accountant_update_data = {
                    "is_super_accountant": False,
                    "super_accountant_id": role_data.super_accountant_id
                }
                crud.update_accountant(db=db, accountant_id=existing_accountant.id, accountant_update_data=accountant_update_data)
            else:
                # Create new accountant record
                accountant_data = {
                    "user_id": user_id, 
                    "is_super_accountant": False,
                    "super_accountant_id": role_data.super_accountant_id
                }
                crud.create_accountant(db=db, accountant_data=accountant_data)
        
        return UserResponse.from_orm(updated_user)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating user role: {str(e)}"
        )

@router.get("/{user_id}/businesses")
async def get_user_businesses(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get businesses for a specific user."""
    try:
        # Check permissions - only allow accountants to view their own businesses
        if current_user.role == "accountant" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own businesses"
            )
        
        # Check if user has required role
        if current_user.role not in ["root_admin", "super_accountant", "accountant"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        # For accountants, get businesses they manage
        if current_user.role == "accountant":
            # Get the accountant record for the user
            accountant = db.query(Accountant).filter(Accountant.user_id == user_id).first()
            if not accountant:
                return []
            
            businesses = crud.get_businesses_by_accountant(db=db, accountant_id=accountant.id, skip=skip, limit=limit)
        else:
            # For root admin and super accountants, get businesses owned by the user
            businesses = crud.get_businesses_by_owner(db=db, owner_id=user_id, skip=skip, limit=limit)
        
        return businesses
    except Exception as e:
        # Log error for monitoring (remove in production if not needed)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

# Generic /{user_id} routes come AFTER more specific routes
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root())
):
    """Get a specific user (Super Accountant or Root Admin only)."""
    user = crud.get_user(db=db, user_id=user_id)
    return UserResponse.from_orm(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root())
):
    """Update a user (Super Accountant or Root Admin only)."""
    try:
        # Convert Pydantic model to dictionary (Pydantic v1)
        user_update_dict = user_update_data.dict()
        updated_user = crud.update_user(db=db, user_id=user_id, user_update_data=user_update_dict)
        return UserResponse.from_orm(updated_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin())
):
    """Delete a user (Root Admin only)."""
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}