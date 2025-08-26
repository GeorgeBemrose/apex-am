from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import (
    get_current_user, require_root_admin, require_super_accountant_or_root,
    require_accountant_or_higher
)
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserResponse, RoleAssignment
from app import crud

router = APIRouter()

@router.post("/")
async def create_user(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Create a new user (Root Admin only)."""
    try:
        body = await request.json()
        schema = UserCreate()
        user_data = schema.load(body)
        return crud.create_user(db=db, user_data=user_data)
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
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Get list of users (Super Accountant or Root Admin only)."""
    users = crud.get_users(db=db, skip=skip, limit=limit)
    schema = UserResponse(many=True)
    return schema.dump(users)

@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    schema = UserResponse()
    return schema.dump(current_user)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Get a specific user (Super Accountant or Root Admin only)."""
    user = crud.get_user(db=db, user_id=user_id)
    schema = UserResponse()
    return schema.dump(user)

@router.put("/{user_id}")
async def update_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Update a user (Super Accountant or Root Admin only)."""
    try:
        body = await request.json()
        schema = UserUpdate()
        user_update_data = schema.load(body)
        updated_user = crud.update_user(db=db, user_id=user_id, user_update_data=user_update_data)
        response_schema = UserResponse()
        return response_schema.dump(updated_user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Delete a user (Root Admin only)."""
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully"}

@router.post("/{user_id}/assign-role")
async def assign_role(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Assign a role to a user (Root Admin only)."""
    try:
        body = await request.json()
        schema = RoleAssignment()
        role_data = schema.load(body)
        
        user = crud.get_user(db=db, user_id=user_id)
        
        # Update user role
        user_update_data = {"role": role_data["new_role"]}
        updated_user = crud.update_user(db=db, user_id=user_id, user_update_data=user_update_data)
        
        # If assigning super accountant role, create accountant record
        if role_data["new_role"] == "super_accountant":
            from app.models import Accountant
            existing_accountant = db.query(Accountant).filter(Accountant.user_id == user_id).first()
            if not existing_accountant:
                accountant_data = {"user_id": user_id, "is_super_accountant": True}
                crud.create_accountant(db=db, accountant_data=accountant_data)
        
        # If assigning accountant role, create accountant record
        elif role_data["new_role"] == "accountant":
            from app.models import Accountant
            existing_accountant = db.query(Accountant).filter(Accountant.user_id == user_id).first()
            if not existing_accountant:
                accountant_data = {
                    "user_id": user_id, 
                    "is_super_accountant": False,
                    "super_accountant_id": role_data.get("super_accountant_id")
                }
                crud.create_accountant(db=db, accountant_data=accountant_data)
        
        response_schema = UserResponse()
        return {"message": f"Role {role_data['new_role']} assigned successfully", "user": response_schema.dump(updated_user)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.get("/{user_id}/businesses")
async def get_user_businesses(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_accountant_or_higher)
):
    """Get businesses owned by a specific user."""
    # Check permissions
    if current_user.role == "accountant" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only view own businesses"
        )
    
    businesses = crud.get_businesses_by_owner(db=db, owner_id=user_id, skip=skip, limit=limit)
    from app.schemas import BusinessResponse
    schema = BusinessResponse(many=True)
    return schema.dump(businesses)