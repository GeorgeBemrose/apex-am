from fastapi import APIRouter
from .users import router as users_router
from .businesses import router as businesses_router

# Create a master router to include all sub-routers
api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(businesses_router, prefix="/businesses", tags=["businesses"])