import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Base, User, Accountant, Business
from app import crud
from app.schemas import UserCreate, AccountantCreate, BusinessCreate, UserUpdate, AccountantUpdate, BusinessUpdate
from app.auth import get_password_hash

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crud.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_user(db_session):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
        role="accountant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def sample_super_accountant(db_session):
    user = User(
        username="superuser",
        email="super@example.com",
        hashed_password=get_password_hash("superpass"),
        role="super_accountant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    accountant = Accountant(
        user_id=user.id,
        is_super_accountant=True
    )
    db_session.add(accountant)
    db_session.commit()
    db_session.refresh(accountant)
    return user

class TestUserCRUD:
    def test_create_user(self, db_session):
        """Test creating a new user."""
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass",
            "role": "accountant"
        }
        
        user = crud.create_user(db=db_session, user_data=user_data)
        
        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.role == "accountant"
        assert user.hashed_password != "newpass"  # Should be hashed
    
    def test_create_user_duplicate_username(self, db_session, sample_user):
        """Test creating user with duplicate username fails."""
        user_data = {
            "username": "testuser",  # Same as sample_user
            "email": "different@example.com",
            "password": "newpass",
            "role": "accountant"
        }
        
        with pytest.raises(Exception):
            crud.create_user(db=db_session, user_data=user_data)
    
    def test_get_user(self, db_session, sample_user):
        """Test getting a user by ID."""
        user = crud.get_user(db=db_session, user_id=sample_user.id)
        
        assert user.id == sample_user.id
        assert user.username == sample_user.username
        assert user.email == sample_user.email
    
    def test_get_user_not_found(self, db_session):
        """Test getting a non-existent user."""
        with pytest.raises(Exception):
            crud.get_user(db=db_session, user_id=999)
    
    def test_get_users(self, db_session, sample_user):
        """Test getting list of users."""
        users = crud.get_users(db=db_session)
        
        assert len(users) == 1
        assert users[0].id == sample_user.id
    
    def test_update_user(self, db_session, sample_user):
        """Test updating a user."""
        update_data = {"username": "updateduser", "email": "updated@example.com"}
        
        updated_user = crud.update_user(db=db_session, user_id=sample_user.id, user_update_data=update_data)
        
        assert updated_user.username == "updateduser"
        assert updated_user.email == "updated@example.com"
        assert updated_user.role == sample_user.role  # Unchanged
    
    def test_delete_user(self, db_session, sample_user):
        """Test deleting a user."""
        crud.delete_user(db=db_session, user_id=sample_user.id)
        
        # Verify user is deleted
        with pytest.raises(Exception):
            crud.get_user(db=db_session, user_id=sample_user.id)

class TestAccountantCRUD:
    def test_create_accountant(self, db_session, sample_user):
        """Test creating a new accountant."""
        accountant_data = {
            "user_id": sample_user.id,
            "is_super_accountant": False
        }
        
        accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        assert accountant.user_id == sample_user.id
        assert accountant.is_super_accountant == False
        assert accountant.super_accountant_id is None
    
    def test_create_accountant_with_super(self, db_session, sample_user, sample_super_accountant):
        """Test creating accountant with super accountant assignment."""
        accountant_data = {
            "user_id": sample_user.id,
            "super_accountant_id": sample_super_accountant.id,
            "is_super_accountant": False
        }
        
        accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        assert accountant.super_accountant_id == sample_super_accountant.id
    
    def test_get_accountant(self, db_session, sample_user):
        """Test getting an accountant by ID."""
        accountant_data = {"user_id": sample_user.id}
        created_accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        accountant = crud.get_accountant(db=db_session, accountant_id=created_accountant.id)
        
        assert accountant.id == created_accountant.id
        assert accountant.user_id == sample_user.id
    
    def test_get_accountants_by_super(self, db_session, sample_user, sample_super_accountant):
        """Test getting accountants managed by a super accountant."""
        # Create accountant managed by super accountant
        accountant_data = {
            "user_id": sample_user.id,
            "super_accountant_id": sample_super_accountant.id
        }
        crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        accountants = crud.get_accountants_by_super(
            db=db_session, 
            super_accountant_id=sample_super_accountant.id
        )
        
        assert len(accountants) == 1
        assert accountants[0].super_accountant_id == sample_super_accountant.id
    
    def test_update_accountant(self, db_session, sample_user, sample_super_accountant):
        """Test updating an accountant."""
        accountant_data = {"user_id": sample_user.id}
        created_accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        update_data = {
            "super_accountant_id": sample_super_accountant.id,
            "is_super_accountant": False
        }
        
        updated_accountant = crud.update_accountant(
            db=db_session, 
            accountant_id=created_accountant.id, 
            accountant_update_data=update_data
        )
        
        assert updated_accountant.super_accountant_id == sample_super_accountant.id
    
    def test_delete_accountant(self, db_session, sample_user):
        """Test deleting an accountant."""
        accountant_data = {"user_id": sample_user.id}
        created_accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        crud.delete_accountant(db=db_session, accountant_id=created_accountant.id)
        
        # Verify accountant is deleted
        with pytest.raises(Exception):
            crud.get_accountant(db=db_session, accountant_id=created_accountant.id)

class TestBusinessCRUD:
    def test_create_business(self, db_session, sample_user):
        """Test creating a new business."""
        business_data = {
            "name": "Test Business",
            "description": "A test business",
            "owner_id": sample_user.id
        }
        
        business = crud.create_business(db=db_session, business_data=business_data)
        
        assert business.name == "Test Business"
        assert business.description == "A test business"
        assert business.owner_id == sample_user.id
        assert business.is_active == True
    
    def test_get_business(self, db_session, sample_user):
        """Test getting a business by ID."""
        business_data = {
            "name": "Test Business",
            "owner_id": sample_user.id
        }
        created_business = crud.create_business(db=db_session, business_data=business_data)
        
        business = crud.get_business(db=db_session, business_id=created_business.id)
        
        assert business.id == created_business.id
        assert business.name == "Test Business"
    
    def test_get_businesses_by_owner(self, db_session, sample_user):
        """Test getting businesses owned by a specific user."""
        # Create multiple businesses for the user
        business1_data = {"name": "Business 1", "owner_id": sample_user.id}
        business2_data = {"name": "Business 2", "owner_id": sample_user.id}
        
        crud.create_business(db=db_session, business_data=business1_data)
        crud.create_business(db=db_session, business_data=business2_data)
        
        businesses = crud.get_businesses_by_owner(db=db_session, owner_id=sample_user.id)
        
        assert len(businesses) == 2
        assert all(b.owner_id == sample_user.id for b in businesses)
    
    def test_update_business(self, db_session, sample_user):
        """Test updating a business."""
        business_data = {"name": "Test Business", "owner_id": sample_user.id}
        created_business = crud.create_business(db=db_session, business_data=business_data)
        
        update_data = {"name": "Updated Business", "description": "Updated description"}
        
        updated_business = crud.update_business(
            db=db_session, 
            business_id=created_business.id, 
            business_update_data=update_data
        )
        
        assert updated_business.name == "Updated Business"
        assert updated_business.description == "Updated description"
    
    def test_delete_business(self, db_session, sample_user):
        """Test deleting a business."""
        business_data = {"name": "Test Business", "owner_id": sample_user.id}
        created_business = crud.create_business(db=db_session, business_data=business_data)
        
        crud.delete_business(db=db_session, business_id=created_business.id)
        
        # Verify business is deleted
        with pytest.raises(Exception):
            crud.get_business(db=db_session, business_id=created_business.id)

class TestRoleManagement:
    def test_assign_super_accountant(self, db_session, sample_user, sample_super_accountant):
        """Test assigning a super accountant to manage an accountant."""
        accountant_data = {"user_id": sample_user.id}
        created_accountant = crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        crud.assign_super_accountant(
            db=db_session, 
            user_id=sample_user.id, 
            super_accountant_id=sample_super_accountant.id
        )
        
        # Verify assignment
        updated_accountant = crud.get_accountant_by_user_id(db=db_session, user_id=sample_user.id)
        assert updated_accountant.super_accountant_id == sample_super_accountant.id
    
    def test_remove_super_accountant(self, db_session, sample_user, sample_super_accountant):
        """Test removing super accountant assignment."""
        accountant_data = {
            "user_id": sample_user.id,
            "super_accountant_id": sample_super_accountant.id
        }
        crud.create_accountant(db=db_session, accountant_data=accountant_data)
        
        crud.remove_super_accountant(db=db_session, user_id=sample_user.id)
        
        # Verify removal
        updated_accountant = crud.get_accountant_by_user_id(db=db_session, user_id=sample_user.id)
        assert updated_accountant.super_accountant_id is None
