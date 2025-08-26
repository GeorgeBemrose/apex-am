from fastapi import Depends, HTTPException
from app.auth import decode_access_token
from app.models import User

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    user = User.get(id=payload.get("sub"))  # Replace with DB query
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker