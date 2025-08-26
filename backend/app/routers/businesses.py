from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user, require_root_admin, require_super_accountant_or_root, require_accountant_or_higher
from app.models import User
from app.schemas import BusinessCreate, BusinessUpdate, BusinessResponse
from app import crud

router = APIRouter()

@router.post("/")
async def create_business(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Create a new business (Root Admin only)."""
    try:
        body = await request.json()
        schema = BusinessCreate()
        business_data = schema.load(body)
        return crud.create_business(db=db, business_data=business_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.get("/")
async def get_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of businesses based on user role."""
    if current_user.role == "accountant":
        # Accountants can only see their own businesses
        businesses = crud.get_businesses_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    elif current_user.role == "super_accountant":
        # Super accountants can see businesses of their managed accountants
        accountant = crud.get_accountant_by_user_id(db=db, user_id=current_user.id)
        if not accountant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Accountant record not found"
            )
        
        # Get all businesses managed by accountants under this super accountant
        managed_accountants = crud.get_accountants_by_super(db=db, super_accountant_id=current_user.id)
        all_businesses = []
        for acc in managed_accountants:
            businesses = crud.get_businesses_by_accountant(db=db, accountant_id=acc.id)
            all_businesses.extend(businesses)
        
        # Apply pagination
        businesses = all_businesses[skip:skip + limit]
    else:
        # Root admin can see all businesses
        businesses = crud.get_businesses(db=db, skip=skip, limit=limit)
    
    schema = BusinessResponse(many=True)
    return schema.dump(businesses)

@router.get("/my-businesses")
async def get_my_businesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get businesses owned by the current user."""
    businesses = crud.get_businesses_by_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    schema = BusinessResponse(many=True)
    return schema.dump(businesses)

@router.get("/{business_id}")
async def get_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific business."""
    business = crud.get_business(db=db, business_id=business_id)
    
    # Check permissions
    if current_user.role == "accountant":
        if business.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only view own businesses"
            )
    elif current_user.role == "super_accountant":
        # Check if business belongs to a managed accountant
        if business.accountant_id:
            accountant = crud.get_accountant(db=db, accountant_id=business.accountant_id)
            if accountant.super_accountant_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only view businesses of managed accountants"
                )
    
    schema = BusinessResponse()
    return schema.dump(business)

@router.put("/{business_id}")
async def update_business(
    business_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a business."""
    business = crud.get_business(db=db, business_id=business_id)
    
    # Check permissions
    if current_user.role == "accountant":
        if business.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Can only update own businesses"
            )
    elif current_user.role == "super_accountant":
        # Check if business belongs to a managed accountant
        if business.accountant_id:
            accountant = crud.get_accountant(db=db, accountant_id=business.accountant_id)
            if accountant.super_accountant_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only update businesses of managed accountants"
                )
    
    try:
        body = await request.json()
        schema = BusinessUpdate()
        business_update_data = schema.load(body)
        updated_business = crud.update_business(db=db, business_id=business_id, business_update_data=business_update_data)
        response_schema = BusinessResponse()
        return response_schema.dump(updated_business)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.delete("/{business_id}")
async def delete_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_root_admin)
):
    """Delete a business (Root Admin only)."""
    crud.delete_business(db=db, business_id=business_id)
    return {"message": "Business deleted successfully"}

@router.post("/{business_id}/assign-accountant")
async def assign_accountant_to_business(
    business_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Assign an accountant to manage a business."""
    business = crud.get_business(db=db, business_id=business_id)
    
    # Check if super accountant can assign to this business
    if current_user.role == "super_accountant":
        if business.accountant_id:
            accountant = crud.get_accountant(db=db, accountant_id=business.accountant_id)
            if accountant.super_accountant_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only assign accountants to businesses you manage"
                )
    
    try:
        body = await request.json()
        accountant_id = body.get("accountant_id")
        if not accountant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="accountant_id is required"
            )
        
        # Update business with new accountant
        business_update_data = {"accountant_id": accountant_id}
        updated_business = crud.update_business(db=db, business_id=business_id, business_update_data=business_update_data)
        response_schema = BusinessResponse()
        return response_schema.dump(updated_business)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(e)}"
        )

@router.post("/{business_id}/remove-accountant")
async def remove_accountant_from_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_accountant_or_root)
):
    """Remove accountant assignment from a business."""
    business = crud.get_business(db=db, business_id=business_id)
    
    # Check if super accountant can remove from this business
    if current_user.role == "super_accountant":
        if business.accountant_id:
            accountant = crud.get_accountant(db=db, accountant_id=business.accountant_id)
            if accountant.super_accountant_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Can only remove accountants from businesses you manage"
                )
    
    # Remove accountant assignment
    business_update_data = {"accountant_id": None}
    updated_business = crud.update_business(db=db, business_id=business_id, business_update_data=business_update_data)
    response_schema = BusinessResponse()
    return response_schema.dump(updated_business)