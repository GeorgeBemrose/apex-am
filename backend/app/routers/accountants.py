from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user, require_super_accountant_or_root
from app import crud, schemas
from app.models import User, Accountant

router = APIRouter()

@router.get("/")
async def get_accountants(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "root_admin":
        accountants = crud.get_accountants(db, skip=skip, limit=limit)
    elif current_user.role == "super_accountant":
        # Super accountants can see all accountants so they can assign them to businesses
        # They can see accountants they manage plus independent accountants
        accountant = crud.get_accountant_by_user_id(db, current_user.id)
        if accountant:
            # Get accountants they manage
            managed_accountants = crud.get_accountants_by_super(db, accountant.id, skip=skip, limit=limit)
            # Get independent accountants (not assigned to any super accountant)
            independent_accountants = crud.get_independent_accountants(db, skip=skip, limit=limit)
            # Combine both lists, avoiding duplicates
            all_accountants = managed_accountants + independent_accountants
            # Remove duplicates based on ID
            seen_ids = set()
            unique_accountants = []
            for acc in all_accountants:
                if acc.id not in seen_ids:
                    seen_ids.add(acc.id)
                    unique_accountants.append(acc)
            accountants = unique_accountants
        else:
            accountants = []
    else:
        # Regular accountants can only see themselves
        accountant = crud.get_accountant_by_user_id(db, current_user.id)
        accountants = [accountant] if accountant else []
    
    return accountants

@router.get("/{accountant_id}")
async def get_accountant(
    accountant_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    accountant = crud.get_accountant(db, accountant_id)
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    # Check permissions
    if current_user.role == "accountant" and accountant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return accountant

@router.post("/")
async def create_accountant(
    accountant_data: schemas.AccountantCreate,
    current_user: User = Depends(require_super_accountant_or_root()),
    db: Session = Depends(get_db)
):
    accountant = crud.create_accountant(db, accountant_data.dict())
    return accountant

@router.put("/{accountant_id}")
async def update_accountant(
    accountant_id: str,
    accountant_data: schemas.AccountantCreate,
    current_user: User = Depends(require_super_accountant_or_root()),
    db: Session = Depends(get_db)
):
    accountant = crud.get_accountant(db, accountant_id)
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    # Check permissions
    if current_user.role == "super_accountant":
        if accountant.super_accountant_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    updated_accountant = crud.update_accountant(db, accountant_id, accountant_data.dict())
    
    if not updated_accountant:
        raise HTTPException(status_code=500, detail="Failed to update accountant")
    
    return updated_accountant

@router.delete("/{accountant_id}")
async def delete_accountant(
    accountant_id: str,
    current_user: User = Depends(require_super_accountant_or_root()),
    db: Session = Depends(get_db)
):
    accountant = crud.get_accountant(db, accountant_id)
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    # Check permissions
    if current_user.role == "super_accountant":
        if accountant.super_accountant_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    success = crud.delete_accountant(db, accountant_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete accountant")
    
    return {"message": "Accountant deleted successfully"}

@router.post("/{accountant_id}/assign-super")
async def assign_super_accountant(
    accountant_id: str,
    request: dict,
    current_user: User = Depends(require_super_accountant_or_root),
    db: Session = Depends(get_db)
):
    accountant = crud.get_accountant(db, accountant_id)
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    super_accountant_id = request.get("super_accountant_id")
    if not super_accountant_id:
        raise HTTPException(status_code=400, detail="super_accountant_id is required")
    
    # Update the accountant with the new super accountant
    update_data = {"super_accountant_id": super_accountant_id}
    updated_accountant = crud.update_accountant(db, accountant_id, update_data)
    
    if not updated_accountant:
        raise HTTPException(status_code=500, detail="Failed to assign super accountant")
    
    return {"message": "Super accountant assigned successfully"}

@router.post("/{accountant_id}/remove-super")
async def remove_super_accountant(
    accountant_id: str,
    current_user: User = Depends(require_super_accountant_or_root),
    db: Session = Depends(get_db)
):
    accountant = crud.get_accountant(db, accountant_id)
    if not accountant:
        raise HTTPException(status_code=404, detail="Accountant not found")
    
    # Remove the super accountant by setting super_accountant_id to None
    update_data = {"super_accountant_id": None}
    updated_accountant = crud.update_accountant(db, accountant_id, update_data)
    
    if not updated_accountant:
        raise HTTPException(status_code=500, detail="Failed to remove super accountant")
    
    return {"message": "Super accountant removed successfully"}
