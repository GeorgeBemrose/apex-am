import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import get_db, Base
from app.models import User, Accountant, Business
from app.auth import get_password_hash, create_access_token
import os
import tempfile

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        role="accountant",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin_user(db_session):
    """Create a test admin user."""
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        role="root_admin",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_super_accountant_user(db_session):
    """Create a test super accountant user."""
    user = User(
        username="superaccountant",
        email="super@example.com",
        hashed_password=get_password_hash("superpassword"),
        role="super_accountant",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_accountant(db_session, test_user):
    """Create a test accountant."""
    accountant = Accountant(
        user_id=test_user.id,
        first_name="Test",
        last_name="Accountant",
        is_super_accountant=False
    )
    db_session.add(accountant)
    db_session.commit()
    db_session.refresh(accountant)
    return accountant

@pytest.fixture
def test_super_accountant(db_session, test_super_accountant_user):
    """Create a test super accountant."""
    accountant = Accountant(
        user_id=test_super_accountant_user.id,
        first_name="Super",
        last_name="Accountant",
        is_super_accountant=True
    )
    db_session.add(accountant)
    db_session.commit()
    db_session.refresh(accountant)
    return accountant

@pytest.fixture
def test_business(db_session, test_user, test_accountant):
    """Create a test business."""
    business = Business(
        name="Test Business",
        description="A test business for testing",
        owner_id=test_user.id,
        accountant_id=test_accountant.id,
        is_active=True
    )
    db_session.add(business)
    db_session.commit()
    db_session.refresh(business)
    return business

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers for a test user."""
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def admin_auth_headers(test_admin_user):
    """Create authentication headers for a test admin user."""
    access_token = create_access_token(data={"sub": test_admin_user.email})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def super_accountant_auth_headers(test_super_accountant_user):
    """Create authentication headers for a test super accountant user."""
    access_token = create_access_token(data={"sub": test_super_accountant_user.email})
    return {"Authorization": f"Bearer {access_token}"}

# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
