from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app import models, schemas
from app.auth import get_password_hash

# CRUD for Users
def create_user(db: Session, user_data: dict):
    """Create a new user with hashed password."""
    try:
        hashed_password = get_password_hash(user_data["password"])
        db_user = models.User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=hashed_password,
            role=user_data["role"]
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

def get_user(db: Session, user_id: str):
    """Get a user by ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of users with pagination."""
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user_update_data: dict):
    """Update a user."""
    db_user = get_user(db, user_id)
    
    for field, value in user_update_data.items():
        if value is not None:
            setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    """Delete a user."""
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
    return db_user

# CRUD for Accountants
def create_accountant(db: Session, accountant_data: dict):
    """Create a new accountant."""
    try:
        db_accountant = models.Accountant(**accountant_data)
        db.add(db_accountant)
        db.commit()
        db.refresh(db_accountant)
        return db_accountant
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Accountant already exists for this user"
        )

def get_accountant(db: Session, accountant_id: str):
    """Get an accountant by ID."""
    accountant = db.query(models.Accountant).filter(models.Accountant.id == accountant_id).first()
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    return accountant

def get_accountant_by_user_id(db: Session, user_id: str):
    """Get an accountant by user ID."""
    return db.query(models.Accountant).filter(models.Accountant.user_id == user_id).first()

def get_accountants(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of accountants with pagination."""
    return db.query(models.Accountant).options(
        joinedload(models.Accountant.user)
    ).offset(skip).limit(limit).all()

def get_accountants_by_super(db: Session, super_accountant_id: str, skip: int = 0, limit: int = 100):
    """Get accountants managed by a specific super accountant."""
    return db.query(models.Accountant).filter(
        models.Accountant.super_accountant_id == super_accountant_id
    ).offset(skip).limit(limit).all()

def get_independent_accountants(db: Session, skip: int = 0, limit: int = 100):
    """Get accountants that are not assigned to any super accountant."""
    return db.query(models.Accountant).options(
        joinedload(models.Accountant.user)
    ).filter(
        models.Accountant.super_accountant_id.is_(None)
    ).offset(skip).limit(limit).all()

def update_accountant(db: Session, accountant_id: str, accountant_update_data: dict):
    """Update an accountant."""
    db_accountant = get_accountant(db, accountant_id)
    
    for field, value in accountant_update_data.items():
        if value is not None:
            setattr(db_accountant, field, value)
    
    db.commit()
    db.refresh(db_accountant)
    return db_accountant

def delete_accountant(db: Session, accountant_id: str):
    """Delete an accountant."""
    db_accountant = get_accountant(db, accountant_id)
    db.delete(db_accountant)
    db.commit()
    return db_accountant

# CRUD for Businesses
def create_business(db: Session, business_data: dict):
    """Create a new business."""
    db_business = models.Business(**business_data)
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_business(db: Session, business_id: str):
    """Get a business by ID."""
    business = db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).filter(models.Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    return business

def get_businesses(db: Session, skip: int = 0, limit: int = 100):
    """Get a list of businesses with pagination."""
    return db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).offset(skip).limit(limit).all()

def get_businesses_by_owner(db: Session, owner_id: str, skip: int = 0, limit: int = 100):
    """Get businesses owned by a specific user."""
    return db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).filter(
        models.Business.owner_id == owner_id
    ).offset(skip).limit(limit).all()

def get_businesses_by_accountant(db: Session, accountant_id: str, skip: int = 0, limit: int = 100):
    """Get businesses managed by a specific accountant."""
    # Get businesses where the accountant is the primary accountant (accountant_id)
    primary_businesses = db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).filter(
        models.Business.accountant_id == accountant_id
    ).all()
    
    # Get businesses where the accountant is in the many-to-many relationship
    many_to_many_businesses = db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).filter(
        models.Business.accountants.any(id=accountant_id)
    ).all()
    
    # Combine both lists and remove duplicates
    all_businesses = primary_businesses + many_to_many_businesses
    unique_businesses = list({business.id: business for business in all_businesses}.values())
    
    # Apply pagination
    return unique_businesses[skip:skip + limit]

def update_business(db: Session, business_id: str, business_update_data: dict):
    """Update a business."""
    db_business = get_business(db, business_id)
    
    for field, value in business_update_data.items():
        if value is not None:
            setattr(db_business, field, value)
    
    db.commit()
    db.refresh(db_business)
    return db_business

def delete_business(db: Session, business_id: str):
    """Delete a business."""
    db_business = get_business(db, business_id)
    db.delete(db_business)
    db.commit()
    return db_business

# Role management
def assign_super_accountant(db: Session, user_id: str, super_accountant_id: str):
    """Assign a super accountant to manage an accountant."""
    accountant = get_accountant_by_user_id(db, user_id)
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    
    accountant.super_accountant_id = super_accountant_id
    db.commit()
    db.refresh(accountant)
    return accountant

def remove_super_accountant(db: Session, user_id: str):
    """Remove super accountant assignment from an accountant."""
    accountant = get_accountant_by_user_id(db, user_id)
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    
    accountant.super_accountant_id = None
    db.commit()
    db.refresh(accountant)
    return accountant

def assign_accountant_to_business(db: Session, business_id: str, accountant_id: str):
    """Assign an accountant to a business using the many-to-many relationship."""
    business = get_business(db, business_id)
    accountant = get_accountant(db, accountant_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    
    # Add accountant to the many-to-many relationship
    if accountant not in business.accountants:
        business.accountants.append(accountant)
        db.commit()
        db.refresh(business)
    
    return business

def remove_accountant_from_business(db: Session, business_id: str, accountant_id: str):
    """Remove an accountant from a business using the many-to-many relationship."""
    business = get_business(db, business_id)
    accountant = get_accountant(db, accountant_id)
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    
    # Remove accountant from the many-to-many relationship
    if accountant in business.accountants:
        business.accountants.remove(accountant)
        db.commit()
        db.refresh(business)
    
    return business

def get_user_businesses(db: Session, owner_id: str, skip: int = 0, limit: int = 100):
    """Get businesses owned by a specific user."""
    return db.query(models.Business).options(
        joinedload(models.Business.owner),
        joinedload(models.Business.accountant, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.accountants, innerjoin=False).joinedload(models.Accountant.user, innerjoin=False),
        joinedload(models.Business.financial_metrics, innerjoin=False),
        joinedload(models.Business.metrics, innerjoin=False)
    ).filter(
        models.Business.owner_id == owner_id
    ).offset(skip).limit(limit).all()