import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app
from app.models import Base, User
from app.auth import get_password_hash, verify_password, create_access_token, decode_access_token

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def root_admin_user(db_session):
    user = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("password"),
        role="root_admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def super_accountant_user(db_session):
    user = User(
        username="super",
        email="super@example.com",
        hashed_password=get_password_hash("password"),
        role="super_accountant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def accountant_user(db_session):
    user = User(
        username="accountant",
        email="accountant@example.com",
        hashed_password=get_password_hash("password"),
        role="accountant"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

class TestPasswordHashing:
    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "testpassword"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrongpassword", hashed)

class TestJWTTokens:
    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data=data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_access_token(self):
        """Test JWT token decoding."""
        data = {"sub": "testuser"}
        token = create_access_token(data=data)
        decoded = decode_access_token(token)
        
        assert decoded["username"] == "testuser"
    
    def test_decode_invalid_token(self):
        """Test JWT token decoding with invalid token."""
        with pytest.raises(Exception):
            decode_access_token("invalid_token")

class TestAuthenticationEndpoints:
    def test_login_success(self, client, accountant_user):
        """Test successful login."""
        response = client.post("/auth/login", data={
            "username": "accountant",
            "password": "password"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post("/auth/login", data={
            "username": "nonexistent",
            "password": "wrongpass"
        })
        
        assert response.status_code == 401
    
    def test_login_json_success(self, client, accountant_user):
        """Test successful login with JSON."""
        response = client.post("/auth/login-json", json={
            "username": "accountant",
            "password": "password"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

class TestProtectedEndpoints:
    def test_get_current_user_info(self, client, accountant_user):
        """Test getting current user info with valid token."""
        # Login to get token
        login_response = client.post("/auth/login", data={
            "username": "accountant",
            "password": "password"
        })
        token = login_response.json()["access_token"]
        
        # Use token to access protected endpoint
        response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "accountant"
        assert data["role"] == "accountant"
    
    def test_access_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get("/users/me")
        
        assert response.status_code == 401
    
    def test_access_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
        
        assert response.status_code == 401

class TestRoleBasedAccess:
    def test_root_admin_access(self, client, root_admin_user):
        """Test root admin can access all endpoints."""
        # Login as root admin
        login_response = client.post("/auth/login", data={
            "username": "admin",
            "password": "password"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test access to users endpoint
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
    
    def test_super_accountant_limited_access(self, client, super_accountant_user):
        """Test super accountant has limited access."""
        # Login as super accountant
        login_response = client.post("/auth/login", data={
            "username": "super",
            "password": "password"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test access to users endpoint (should work)
        response = client.get("/users/", headers=headers)
        assert response.status_code == 200
        
        # Test access to create user (should fail - root admin only)
        response = client.post("/users/", headers=headers, json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass",
            "role": "accountant"
        })
        assert response.status_code == 403
    
    def test_accountant_limited_access(self, client, accountant_user):
        """Test accountant has very limited access."""
        # Login as accountant
        login_response = client.post("/auth/login", data={
            "username": "accountant",
            "password": "password"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test access to users endpoint (should fail)
        response = client.get("/users/", headers=headers)
        assert response.status_code == 403
        
        # Test access to own info (should work)
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 200
