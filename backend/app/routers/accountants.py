from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import (
    get_current_user, require_root_admin, require_super_accountant_or_root,
    require_accountant_or_higher
)
from app.models import User, Accountant
from app.schemas import AccountantCreate, AccountantUpdate, AccountantResponse
from app import crud

router = APIRouter()

@router.post("/")
async def create_accountant(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Create a new accountant (Root Admin only)."""
    try:
        body = await request.json()
        schema = AccountantCreate()
        accountant_data = schema.load(body)
        return crud.create_accountant(db=db, accountant_data=accountant_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.get("/")
async def get_accountants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Get list of accountants (Super Accountant or Root Admin only)."""
    accountants = crud.get_accountants(db=db, skip=skip, limit=limit)
    schema = AccountantResponse(many=True)
    return schema.dump(accountants)

@router.get("/my-accountants")
async def get_my_accountants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Get accountants managed by the current super accountant."""
    if current_user.role == "super_accountant":
        # Get the accountant record for the current user
        accountant = crud.get_accountant_by_user_id(db=db, user_id=current_user.id)
        if not accountant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Accountant record not found"
            )
        accountants = crud.get_accountants_by_super(
            db=db, 
            super_accountant_id=current_user.id, 
            skip=skip, 
            limit=limit
        )
    else:
        # Root admin can see all accountants
        accountants = crud.get_accountants(db=db, skip=skip, limit=limit)
    
    schema = AccountantResponse(many=True)
    return schema.dump(accountants)

@router.get("/{accountant_id}")
async def get_accountant(
    accountant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Get a specific accountant (Super Accountant or Root Admin only)."""
    accountant = crud.get_accountant(db=db, accountant_id=accountant_id)
    
    # Check if super accountant can access this accountant
    if current_user.role == "super_accountant":
        if accountant.super_accountant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only access managed accountants"
            )
    
    schema = AccountantResponse()
    return schema.dump(accountant)

@router.put("/{accountant_id}")
async def update_accountant(
    accountant_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Update an accountant (Super Accountant or Root Admin only)."""
    accountant = crud.get_accountant(db=db, accountant_id=accountant_id)
    
    # Check if super accountant can update this accountant
    if current_user.role == "super_accountant":
        if accountant.super_accountant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only update managed accountants"
            )
    
    try:
        body = await request.json()
        schema = AccountantUpdate()
        accountant_update_data = schema.load(body)
        updated_accountant = crud.update_accountant(db=db, accountant_id=accountant_id, accountant_update_data=accountant_update_data)
        response_schema = AccountantResponse()
        return response_schema.dump(updated_accountant)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.delete("/{accountant_id}")
async def delete_accountant(
    accountant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Delete an accountant (Root Admin only)."""
    crud.delete_accountant(db=db, accountant_id=accountant_id)
    return {"message": "Accountant deleted successfully"}

@router.post("/{accountant_id}/assign-super")
async def assign_super_accountant(
    accountant_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Assign a super accountant to manage an accountant (Root Admin only)."""
    try:
        body = await request.json()
        super_accountant_id = body.get("super_accountant_id")
        if not super_accountant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="super_accountant_id is required"
            )
        
        crud.assign_super_accountant(db=db, user_id=accountant_id, super_accountant_id=super_accountant_id)
        return {"message": "Super accountant assigned successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.post("/{accountant_id}/remove-super")
async def remove_super_accountant(
    accountant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Remove super accountant assignment from an accountant (Root Admin only)."""
    crud.remove_super_accountant(db=db, user_id=accountant_id)
    return {"message": "Super accountant assignment removed successfully"}

@router.get("/{accountant_id}/businesses")
async def get_accountant_businesses(
    accountant_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_accountant_or_higher)
):
    """Get businesses managed by a specific accountant."""
    accountant = crud.get_accountant(db=db, accountant_id=accountant_id)
    
    # Check permissions
    if current_user.role == "accountant":
        if current_user.id != accountant.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own businesses"
            )
    elif current_user.role == "super_accountant":
        if accountant.super_accountant_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view businesses of managed accountants"
            )
    
    businesses = crud.get_businesses_by_accountant(db=db, accountant_id=accountant_id, skip=skip, limit=limit)
    from app.schemas import BusinessResponse
    schema = BusinessResponse(many=True)
    return schema.dump(businesses)
