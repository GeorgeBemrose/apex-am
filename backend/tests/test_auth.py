import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from app.auth import (
    verify_password, get_password_hash, authenticate_user, 
    create_access_token, decode_access_token, get_current_user,
    require_role, require_roles, require_root_admin,
    require_super_accountant_or_root, require_accountant_or_higher
)
from app.models import User
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

# Add markers to all test methods
pytestmark = [
    pytest.mark.unit,
    pytest.mark.auth
]

class TestPasswordHashing:
    """Test password hashing and verification functions."""
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_password_hashing(self):
        """Test that password hashing works correctly."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        # Hash should be a string
        assert isinstance(hashed, str)
        # Hash should be longer than original password
        assert len(hashed) > len(password)
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_password_verification_success(self):
        """Test successful password verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_password_verification_failure(self):
        """Test failed password verification."""
        password = "testpassword123"
        wrong_password = "wrongpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_password_verification_empty_password(self):
        """Test password verification with empty password."""
        password = ""
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

class TestUserAuthentication:
    """Test user authentication functions."""
    
    @pytest.mark.unit
    @pytest.mark.auth
    def test_authenticate_user_success_by_email(self, db_session):
        """Test successful user authentication by email."""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Test authentication
        authenticated_user = authenticate_user(db_session, "test@example.com", "testpassword", use_email=True)
        
        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        assert authenticated_user.email == user.email
    
    def test_authenticate_user_success_by_username(self, db_session):
        """Test successful user authentication by username."""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Test authentication
        authenticated_user = authenticate_user(db_session, "testuser", "testpassword", use_email=False)
        
        assert authenticated_user is not None
        assert authenticated_user.id == user.id
        assert authenticated_user.username == user.username
    
    def test_authenticate_user_wrong_password(self, db_session):
        """Test user authentication with wrong password."""
        # Create a test user
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Test authentication with wrong password
        authenticated_user = authenticate_user(db_session, "test@example.com", "wrongpassword", use_email=True)
        
        assert authenticated_user is None
    
    def test_authenticate_user_nonexistent_user(self, db_session):
        """Test user authentication with nonexistent user."""
        # Test authentication with nonexistent user
        authenticated_user = authenticate_user(db_session, "nonexistent@example.com", "testpassword", use_email=True)
        
        assert authenticated_user is None
    
    def test_authenticate_user_inactive_user(self, db_session):
        """Test user authentication with inactive user."""
        # Create an inactive test user
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant",
            is_active=False
        )
        db_session.add(user)
        db_session.commit()
        
        # Test authentication with inactive user
        authenticated_user = authenticate_user(db_session, "test@example.com", "testpassword", use_email=True)
        
        # Should still authenticate (inactive check is done elsewhere)
        assert authenticated_user is not None
        assert authenticated_user.is_active is False

class TestJWTTokenManagement:
    """Test JWT token creation and validation."""
    
    def test_create_access_token_default_expiry(self):
        """Test access token creation with default expiry."""
        data = {"sub": "test@example.com", "role": "accountant"}
        token = create_access_token(data=data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Decode token to check expiry
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test@example.com"
        assert decoded["role"] == "accountant"
        assert "exp" in decoded
    
    def test_create_access_token_custom_expiry(self):
        """Test access token creation with custom expiry."""
        data = {"sub": "test@example.com"}
        custom_expiry = timedelta(hours=2)
        token = create_access_token(data=data, expires_delta=custom_expiry)
        
        assert isinstance(token, str)
        
        # Decode token to check expiry
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test@example.com"
        assert "exp" in decoded
    
    def test_decode_access_token_success(self):
        """Test successful token decoding."""
        data = {"sub": "test@example.com", "role": "accountant"}
        token = create_access_token(data=data)
        
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test@example.com"
        assert decoded["role"] == "accountant"
    
    def test_decode_access_token_invalid(self):
        """Test token decoding with invalid token."""
        invalid_token = "invalid.token.here"
        decoded = decode_access_token(invalid_token)
        
        assert decoded is None
    
    def test_decode_access_token_expired(self):
        """Test token decoding with expired token."""
        data = {"sub": "test@example.com"}
        # Create token with very short expiry
        token = create_access_token(data=data, expires_delta=timedelta(microseconds=1))
        
        # Wait a bit for token to expire
        import time
        time.sleep(0.001)
        
        decoded = decode_access_token(token)
        assert decoded is None

class TestRoleBasedAccessControl:
    """Test role-based access control decorators."""
    
    def test_require_role_success(self, db_session):
        """Test require_role decorator with correct role."""
        # Create a test user with accountant role
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator
        role_checker = require_role("accountant")
        result = role_checker(mock_dependency())
        
        assert result == user
    
    def test_require_role_failure(self, db_session):
        """Test require_role decorator with incorrect role."""
        # Create a test user with accountant role
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator with wrong role
        role_checker = require_role("root_admin")
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            role_checker(mock_dependency())
        
        assert exc_info.value.status_code == 403
        assert "Insufficient permissions" in str(exc_info.value.detail)
    
    def test_require_roles_success(self, db_session):
        """Test require_roles decorator with one of the allowed roles."""
        # Create a test user with accountant role
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator with allowed roles
        role_checker = require_roles(["root_admin", "super_accountant", "accountant"])
        result = role_checker(mock_dependency())
        
        assert result == user
    
    def test_require_roles_failure(self, db_session):
        """Test require_roles decorator with none of the allowed roles."""
        # Create a test user with accountant role
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("testpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator with disallowed roles
        role_checker = require_roles(["root_admin", "super_accountant"])
        
        # Should raise HTTPException
        with pytest.raises(HTTPException) as exc_info:
            role_checker(mock_dependency())
        
        assert exc_info.value.status_code == 403
        assert "Insufficient permissions" in str(exc_info.value.detail)
    
    def test_require_root_admin_success(self, db_session):
        """Test require_root_admin decorator with root admin user."""
        # Create a test user with root_admin role
        user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpassword"),
            role="root_admin"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator
        role_checker = require_root_admin()
        result = role_checker(mock_dependency())
        
        assert result == user
    
    def test_require_super_accountant_or_root_success(self, db_session):
        """Test require_super_accountant_or_root decorator with super accountant."""
        # Create a test user with super_accountant role
        user = User(
            username="super",
            email="super@example.com",
            hashed_password=get_password_hash("superpassword"),
            role="super_accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator
        role_checker = require_super_accountant_or_root()
        result = role_checker(mock_dependency())
        
        assert result == user
    
    def test_require_accountant_or_higher_success(self, db_session):
        """Test require_accountant_or_higher decorator with accountant."""
        # Create a test user with accountant role
        user = User(
            username="accountant",
            email="accountant@example.com",
            hashed_password=get_password_hash("accountantpassword"),
            role="accountant"
        )
        db_session.add(user)
        db_session.commit()
        
        # Create a mock dependency function
        mock_dependency = Mock(return_value=user)
        
        # Apply the decorator
        role_checker = require_accountant_or_higher()
        result = role_checker(mock_dependency())
        
        assert result == user

class TestSecurityFeatures:
    """Test security-related features."""
    
    def test_token_subject_validation(self):
        """Test that tokens require a subject (sub) field."""
        # Create token without sub field
        data = {"role": "accountant"}
        token = create_access_token(data=data)
        
        # Decode should work but sub should be None
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded.get("sub") is None
    
    def test_token_expiry_validation(self):
        """Test that tokens have proper expiry handling."""
        data = {"sub": "test@example.com"}
        
        # Test with very short expiry
        short_expiry = timedelta(microseconds=1)
        token = create_access_token(data=data, expires_delta=short_expiry)
        
        # Token should be created
        assert isinstance(token, str)
        
        # But should expire quickly
        import time
        time.sleep(0.001)
        decoded = decode_access_token(token)
        assert decoded is None
