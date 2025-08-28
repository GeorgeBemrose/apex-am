from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_super_accountant_or_root
from app import crud, schemas
from app.models import User, Business

router = APIRouter()

@router.get("/")
async def get_businesses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "root_admin":
        businesses = crud.get_businesses(db, skip=skip, limit=limit)
    elif current_user.role == "super_accountant":
        businesses = crud.get_businesses(db, skip=skip, limit=limit)
    else:
        businesses = crud.get_user_businesses(db, current_user.id)
    
    return businesses

@router.get("/{business_id}")
async def get_business(
    business_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Check permissions
    if current_user.role == "accountant":
        # Accountants can view businesses they own OR businesses they're assigned to manage
        if business.owner_id != current_user.id:
            # Check if they're assigned to manage this business
            from app.models import Accountant
            accountant = db.query(Accountant).filter(Accountant.user_id == current_user.id).first()
            if not accountant or accountant not in business.accountants:
                raise HTTPException(status_code=403, detail="Access denied")
    
    return business

@router.post("/")
async def create_business(
    business_data: schemas.BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["root_admin", "super_accountant"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    business_data_dict = business_data.model_dump()
    business_data_dict["owner_id"] = current_user.id
    
    business = crud.create_business(db, business_data_dict)
    return business

@router.put("/{business_id}")
async def update_business(
    business_id: str,
    business_data: schemas.BusinessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Check permissions
    if current_user.role == "accountant":
        # Accountants can update businesses they own OR businesses they're assigned to manage
        if business.owner_id != current_user.id:
            # Check if they're assigned to manage this business
            from app.models import Accountant
            accountant = db.query(Accountant).filter(Accountant.user_id == current_user.id).first()
            if not accountant or accountant not in business.accountants:
                raise HTTPException(status_code=403, detail="Access denied")
    
    business_data_dict = business_data.model_dump()
    updated_business = crud.update_business(db, business_id, business_data_dict)
    
    if not updated_business:
        raise HTTPException(status_code=500, detail="Failed to update business")
    
    return updated_business

@router.delete("/{business_id}")
async def delete_business(
    business_id: str,
    current_user: User = Depends(require_super_accountant_or_root()),
    db: Session = Depends(get_db)
):
    business = crud.get_business(db, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    success = crud.delete_business(db, business_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete business")
    
    return {"message": "Business deleted successfully"}

@router.post("/{business_id}/assign-accountant")
async def assign_accountant_to_business(
    business_id: str,
    request: schemas.AssignAccountantRequest,
    current_user: User = Depends(require_super_accountant_or_root),
    db: Session = Depends(get_db)
):
    updated_business = crud.assign_accountant_to_business(db, business_id, request.accountant_id)
    return {"message": "Accountant assigned successfully"}

@router.post("/{business_id}/remove-accountant")
async def remove_accountant_from_business(
    business_id: str,
    request: schemas.AssignAccountantRequest,
    current_user: User = Depends(require_super_accountant_or_root),
    db: Session = Depends(get_db)
):
    updated_business = crud.remove_accountant_from_business(db, business_id, request.accountant_id)
    return {"message": "Accountant removed successfully"}