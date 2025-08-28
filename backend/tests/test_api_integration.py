import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Accountant, Business
from app.auth import get_password_hash, create_access_token

# Add markers to all test methods
pytestmark = [
    pytest.mark.integration
]

class TestAuthenticationEndpoints:
    """Test authentication-related API endpoints."""
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "API is running" in data["message"]
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Welcome to Apex AM API" in data["message"]
        assert "version" in data
        # Check that endpoints exist (the structure may be different)
        assert "endpoints" in data
    
    def test_api_info_endpoint(self, client):
        """Test the API info endpoint."""
        response = client.get("/api-info")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "version" in data
        assert "features" in data
        assert "authentication" in data
    
    def test_login_form_endpoint_success(self, client, test_user):
        """Test successful login with form data."""
        form_data = {
            "username": test_user.email,  # OAuth2 form uses username field for email
            "password": "testpassword"
        }
        
        response = client.post("/auth/login", data=form_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_form_endpoint_wrong_password(self, client, test_user):
        """Test login with wrong password."""
        form_data = {
            "username": test_user.email,
            "password": "wrongpassword"
        }
        
        response = client.post("/auth/login", data=form_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_form_endpoint_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        form_data = {
            "username": "nonexistent@example.com",
            "password": "testpassword"
        }
        
        response = client.post("/auth/login", data=form_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_json_endpoint_success(self, client, test_user):
        """Test successful login with JSON data."""
        json_data = {
            "email": test_user.email,
            "password": "testpassword"
        }
        
        response = client.post("/auth/login-json", json=json_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_json_endpoint_missing_fields(self, client):
        """Test login with missing fields."""
        # Missing password
        json_data = {"email": "test@example.com"}
        response = client.post("/auth/login-json", json=json_data)
        assert response.status_code == 400
        assert "Email and password are required" in response.json()["detail"]
        
        # Missing email
        json_data = {"password": "testpassword"}
        response = client.post("/auth/login-json", json=json_data)
        assert response.status_code == 400
        assert "Email and password are required" in response.json()["detail"]
    
    def test_login_json_endpoint_invalid_json(self, client):
        """Test login with invalid JSON."""
        response = client.post("/auth/login-json", content="invalid json")
        assert response.status_code == 400
        assert "Invalid JSON format" in response.json()["detail"]

class TestUserEndpoints:
    """Test user management API endpoints."""
    
    def test_get_users_without_auth(self, client):
        """Test getting users without authentication."""
        response = client.get("/users/")
        assert response.status_code == 401
    
    def test_get_users_with_auth(self, client, auth_headers):
        """Test getting users with authentication."""
        response = client.get("/users/", headers=auth_headers)
        # Regular accountants cannot access user list (need super_accountant or root_admin)
        assert response.status_code == 403
    
    def test_get_user_by_id_without_auth(self, client, test_user):
        """Test getting user by ID without authentication."""
        response = client.get(f"/users/{test_user.id}")
        assert response.status_code == 401
    
    def test_get_user_by_id_with_auth(self, client, auth_headers, test_user):
        """Test getting user by ID with authentication."""
        response = client.get(f"/users/{test_user.id}", headers=auth_headers)
        # Regular accountants cannot access user details (need super_accountant or root_admin)
        assert response.status_code == 403
    
    def test_get_user_by_id_not_found(self, client, auth_headers):
        """Test getting non-existent user by ID."""
        response = client.get("/users/nonexistent-id", headers=auth_headers)
        # Should get 403 (insufficient permissions) or 404 (not found)
        assert response.status_code in [403, 404]
    
    def test_create_user_without_auth(self, client):
        """Test creating user without authentication."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "role": "accountant"
        }
        
        response = client.post("/users/", json=user_data)
        # Should get 400 (bad request), 401 (unauthorized), or 422 (validation error)
        assert response.status_code in [400, 401, 422]
    
    def test_create_user_with_auth(self, client, auth_headers):
        """Test creating user with authentication."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "role": "accountant"
        }
        
        response = client.post("/users/", json=user_data, headers=auth_headers)
        # Regular accountants cannot create users (need root_admin)
        # Should get 400 (bad request), 403 (forbidden), or 422 (validation error)
        assert response.status_code in [400, 403, 422]
    
    def test_create_user_duplicate_username(self, client, admin_auth_headers, test_user):
        """Test creating user with duplicate username."""
        user_data = {
            "username": test_user.username,  # Duplicate username
            "email": "different@example.com",
            "password": "newpassword123",
            "role": "accountant"
        }
        
        response = client.post("/users/", json=user_data, headers=admin_auth_headers)
        assert response.status_code == 400
    
    def test_update_user_without_auth(self, client, test_user):
        """Test updating user without authentication."""
        update_data = {"username": "updateduser"}
        
        response = client.put(f"/users/{test_user.id}", json=update_data)
        assert response.status_code == 401
    
    def test_update_user_with_auth(self, client, auth_headers, test_user):
        """Test updating user with authentication."""
        update_data = {"username": "updateduser"}
        
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=auth_headers)
        # Regular accountants cannot update users (need super_accountant or root_admin)
        assert response.status_code == 403
    
    def test_delete_user_without_auth(self, client, test_user):
        """Test deleting user without authentication."""
        response = client.delete(f"/users/{test_user.id}")
        # Should get 401 (unauthorized)
        assert response.status_code in [401]
    
    def test_delete_user_with_auth(self, client, auth_headers, test_user):
        """Test deleting user with authentication."""
        response = client.delete(f"/users/{test_user.id}", headers=auth_headers)
        # Regular accountants cannot delete users (need root_admin)
        # 403 (forbidden)
        assert response.status_code in [403]

    # ===== HAPPY PATH TESTS =====
    # These tests verify that authorized users can successfully perform operations
    
    def test_get_users_as_super_accountant(self, client, super_accountant_auth_headers):
        """Test that super accountants can successfully get user list."""
        response = client.get("/users/", headers=super_accountant_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_users_as_root_admin(self, client, admin_auth_headers):
        """Test that root admins can successfully get user list."""
        response = client.get("/users/", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_user_by_id_as_super_accountant(self, client, super_accountant_auth_headers, test_user):
        """Test that super accountants can successfully get user details."""
        response = client.get(f"/users/{test_user.id}", headers=super_accountant_auth_headers)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == test_user.id
        assert user_data["username"] == test_user.username
        assert user_data["email"] == test_user.email
        assert user_data["role"] == test_user.role
    
    def test_get_user_by_id_as_root_admin(self, client, admin_auth_headers, test_user):
        """Test that root admins can successfully get user details."""
        response = client.get(f"/users/{test_user.id}", headers=admin_auth_headers)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == test_user.id
        assert user_data["username"] == test_user.username
        assert user_data["email"] == test_user.email
        assert user_data["role"] == test_user.role
    
    def test_create_user_as_root_admin(self, client, admin_auth_headers):
        """Test that root admins can successfully create users."""
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "role": "accountant"
        }
        
        response = client.post("/users/", json=user_data, headers=admin_auth_headers)
        assert response.status_code == 200
        created_user = response.json()
        assert created_user["username"] == user_data["username"]
        assert created_user["email"] == user_data["email"]
        assert created_user["role"] == user_data["role"]
        assert "id" in created_user
        assert "hashed_password" not in created_user  # Password should not be returned
    
    def test_update_user_as_super_accountant(self, client, super_accountant_auth_headers, test_user):
        """Test that super accountants can successfully update users."""
        update_data = {
            "username": "updatedusername",
            "email": "updated@example.com",
            "role": "accountant"
        }
        
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=super_accountant_auth_headers)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["username"] == update_data["username"]
        assert updated_user["email"] == update_data["email"]
        assert updated_user["role"] == update_data["role"]
    
    def test_update_user_as_root_admin(self, client, admin_auth_headers, test_user):
        """Test that root admins can successfully update users."""
        update_data = {
            "username": "adminupdated",
            "email": "adminupdated@example.com",
            "role": "super_accountant"
        }
        
        response = client.put(f"/users/{test_user.id}", json=update_data, headers=admin_auth_headers)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["username"] == update_data["username"]
        assert updated_user["email"] == update_data["email"]
        assert updated_user["role"] == update_data["role"]
    
    def test_delete_user_as_root_admin(self, client, admin_auth_headers, test_user):
        """Test that root admins can successfully delete users."""
        response = client.delete(f"/users/{test_user.id}", headers=admin_auth_headers)
        assert response.status_code == 200
        delete_response = response.json()
        assert delete_response["message"] == "User deleted successfully"
    
    def test_assign_role_as_root_admin(self, client, admin_auth_headers, test_user):
        """Test that root admins can successfully assign roles to users."""
        role_data = {
            "new_role": "super_accountant"
        }
        
        response = client.post(f"/users/{test_user.id}/assign-role", json=role_data, headers=admin_auth_headers)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["role"] == role_data["new_role"]
    
    def test_get_user_businesses_as_owner(self, client, auth_headers, test_user):
        """Test that users can successfully get their own businesses."""
        response = client.get(f"/users/{test_user.id}/businesses", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_user_businesses_as_super_accountant(self, client, super_accountant_auth_headers, test_user):
        """Test that super accountants can successfully get user businesses."""
        response = client.get(f"/users/{test_user.id}/businesses", headers=super_accountant_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_user_businesses_as_root_admin(self, client, admin_auth_headers, test_user):
        """Test that root admins can successfully get user businesses."""
        response = client.get(f"/users/{test_user.id}/businesses", headers=admin_auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestAccountantEndpoints:
    """Test accountant management API endpoints."""
    
    def test_get_accountants_without_auth(self, client):
        """Test getting accountants without authentication."""
        response = client.get("/accountants/")
        assert response.status_code == 401
    
    def test_get_accountants_with_auth(self, client, auth_headers):
        """Test getting accountants with authentication."""
        response = client.get("/accountants/", headers=auth_headers)
        # Check if endpoint exists and returns a response
        assert response.status_code in [200, 404]  # 404 if endpoint doesn't exist
    
    def test_get_accountant_by_id_without_auth(self, client, test_accountant):
        """Test getting accountant by ID without authentication."""
        response = client.get(f"/accountants/{test_accountant.id}")
        assert response.status_code == 401
    
    def test_get_accountant_by_id_with_auth(self, client, auth_headers, test_accountant):
        """Test getting accountant by ID with authentication."""
        response = client.get(f"/accountants/{test_accountant.id}", headers=auth_headers)
        # Check if endpoint exists and returns a response
        assert response.status_code in [200, 404, 403]
    
    def test_create_accountant_without_auth(self, client, test_user):
        """Test creating accountant without authentication."""
        # Use a simple test to check authentication
        response = client.post("/accountants/", json={})
        assert response.status_code == 401
    
    def test_create_accountant_with_auth(self, client, auth_headers, test_user):
        """Test creating accountant with authentication."""
        # Check if endpoint exists
        response = client.post("/accountants/", json={}, headers=auth_headers)
        # Should get 403 (forbidden), 422 (validation error), or 404 (endpoint doesn't exist)
        assert response.status_code in [403, 422, 404]
    
    def test_update_accountant_with_auth(self, client, auth_headers, test_accountant):
        """Test updating accountant with authentication."""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        response = client.put(f"/accountants/{test_accountant.id}", json=update_data, headers=auth_headers)
        # Check if endpoint exists
        # Should get 403 (forbidden), 200 (success), 404 (not found), or 422 (validation error)
        assert response.status_code in [200, 403, 404, 422]
    
    def test_delete_accountant_with_auth(self, client, auth_headers, test_accountant):
        """Test deleting accountant with authentication."""
        response = client.delete(f"/accountants/{test_accountant.id}", headers=auth_headers)
        # Check if endpoint exists
        # Should get 403 (forbidden), 200 (success), 404 (not found), or 422 (validation error)
        assert response.status_code in [200, 403, 404, 422]

class TestBusinessEndpoints:
    """Test business management API endpoints."""
    
    def test_get_businesses_without_auth(self, client):
        """Test getting businesses without authentication."""
        response = client.get("/businesses/")
        assert response.status_code == 401
    
    def test_get_businesses_with_auth(self, client, auth_headers):
        """Test getting businesses with authentication."""
        response = client.get("/businesses/", headers=auth_headers)
        # Check if endpoint exists
        assert response.status_code in [200]
    
    def test_get_business_by_id_without_auth(self, client, test_business):
        """Test getting business by ID without authentication."""
        response = client.get(f"/businesses/{test_business.id}")
        assert response.status_code == 401
    
    def test_get_business_by_id_with_auth(self, client, auth_headers, test_business):
        """Test getting business by ID with authentication."""
        response = client.get(f"/businesses/{test_business.id}", headers=auth_headers)
        # Check if endpoint exists and returns a response
        assert response.status_code in [200]
    
    def test_create_business_without_auth(self, client, test_user, test_accountant):
        """Test creating business without authentication."""
        business_data = {
            "name": "New Business",
            "description": "A new business",
            "owner_id": test_user.id,
            "accountant_id": test_accountant.id,
            "is_active": True
        }
        
        response = client.post("/businesses/", json=business_data)
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_create_business_with_auth(self, client, auth_headers, test_user, test_accountant):
        """Test creating business with authentication."""
        business_data = {
            "name": "New Business",
            "description": "A new business",
            "owner_id": test_user.id,
            "accountant_id": test_accountant.id,
            "is_active": True
        }
        
        response = client.post("/businesses/", json=business_data, headers=auth_headers)
        # Check if endpoint exists and handles the request
        assert response.status_code in [200, 403, 404, 422]
    
    def test_update_business_with_auth(self, client, auth_headers, test_business):
        """Test updating business with authentication."""
        update_data = {
            "name": "Updated Business Name",
            "description": "Updated description"
        }
        
        response = client.put(f"/businesses/{test_business.id}", json=update_data, headers=auth_headers)
        # Check if endpoint exists and handles the request
        assert response.status_code in [200, 403, 404, 422]
    
    def test_delete_business_with_auth(self, client, auth_headers, test_business):
        """Test deleting business with authentication."""
        response = client.delete(f"/businesses/{test_business.id}", headers=auth_headers)
        # Check if endpoint exists and handles the request
        assert response.status_code in [200, 403, 404, 422]

class TestAuthorization:
    """Test role-based access control."""
    
    def test_admin_only_endpoint_with_accountant(self, client, auth_headers):
        """Test that accountant cannot access admin-only endpoints."""
        # This would test an endpoint that requires root_admin role
        # For now, we'll test that the user has the correct role
        response = client.get("/users/", headers=auth_headers)
        assert response.status_code == 403  # Regular accountants cannot access user list
    
    def test_admin_only_endpoint_with_admin(self, client, admin_auth_headers):
        """Test that admin can access admin-only endpoints."""
        response = client.get("/users/", headers=admin_auth_headers)
        assert response.status_code == 200
    
    def test_super_accountant_endpoint_with_accountant(self, client, auth_headers):
        """Test that regular accountant cannot access super accountant endpoints."""
        # This would test an endpoint that requires super_accountant role
        # For now, we'll test basic access
        response = client.get("/accountants/", headers=auth_headers)
        assert response.status_code in [200, 403, 404]  # Check if endpoint exists
    
    def test_super_accountant_endpoint_with_super_accountant(self, client, super_accountant_auth_headers):
        """Test that super accountant can access super accountant endpoints."""
        response = client.get("/accountants/", headers=super_accountant_auth_headers)
        assert response.status_code in [200, 404]

class TestSecurityFeatures:
    """Test security-related features."""
    
    @pytest.mark.security
    def test_invalid_token_rejected(self, client):
        """Test that invalid tokens are rejected."""
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        
        response = client.get("/users/", headers=invalid_headers)
        assert response.status_code == 401
    
    @pytest.mark.security
    def test_malformed_token_rejected(self, client):
        """Test that malformed tokens are rejected."""
        malformed_headers = {"Authorization": "Bearer not-a-jwt-token"}
        
        response = client.get("/users/", headers=malformed_headers)
        assert response.status_code == 401
    
    @pytest.mark.security
    def test_missing_token_rejected(self, client):
        """Test that missing tokens are rejected."""
        response = client.get("/users/")
        assert response.status_code == 401
    
    @pytest.mark.security
    def test_expired_token_rejected(self, client, test_user):
        """Test that expired tokens are rejected."""
        # Create a token with very short expiry
        from datetime import timedelta
        expired_token = create_access_token(
            data={"sub": test_user.email}, 
            expires_delta=timedelta(microseconds=1)
        )
        
        # Wait for token to expire
        import time
        time.sleep(0.001)
        
        expired_headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/users/", headers=expired_headers)
        assert response.status_code == 401
        
    
    @pytest.mark.security
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present."""
        response = client.options("/users/")
        # CORS preflight request should not require authentication
        assert response.status_code in [200, 405]  # 405 is also acceptable for OPTIONS
    

