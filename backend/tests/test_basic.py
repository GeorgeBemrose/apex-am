import pytest

@pytest.mark.unit
def test_basic_setup():
    """Basic test to verify testing setup works."""
    assert True

@pytest.mark.unit
def test_imports():
    """Test that all required modules can be imported."""
    try:
        from app.auth import verify_password, get_password_hash
        from app.crud import create_user, get_user
        from app.models import User, Accountant, Business
        from app.main import app
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")

@pytest.mark.unit
def test_pytest_markers():
    """Test that pytest markers are working."""
    # This test should be marked as unit
    assert True
