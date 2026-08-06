from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.database.session import get_db
from app.modules.auth.schemas import (
    RegisterRequest, LoginRequest, RefreshRequest, 
    TokenResponse, UserResponse, CurrentUserResponse,
    BusinessMembershipResponse, RoleResponse
)
from app.modules.auth.service import register, login, refresh_tokens, logout
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register_user(
    request: RegisterRequest, 
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Register a new user in the system. 
    An email verification token is generated during this process.
    """
    user = await register(session, request)
    return user

@router.post(
    "/login", 
    response_model=TokenResponse,
    summary="Login user"
)
async def login_user(
    request: LoginRequest, 
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Authenticate a user using their email and password.
    Returns a short-lived access token and a long-lived refresh token.
    """
    tokens = await login(session, request)
    return tokens

@router.post(
    "/refresh", 
    response_model=TokenResponse,
    summary="Refresh access token"
)
async def refresh_user_tokens(
    request: RefreshRequest, 
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Rotate a valid refresh token. The old token is immediately revoked 
    to prevent replay attacks, and a new token pair is issued.
    """
    tokens = await refresh_tokens(session, request)
    return tokens

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Logout user"
)
async def logout_user(
    request: RefreshRequest, 
    session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Log out a user by immediately revoking their refresh token.
    The access token will naturally expire.
    """
    await logout(session, request.refresh_token)
    return {"message": "Successfully logged out"}

@router.get(
    "/me", 
    response_model=CurrentUserResponse,
    summary="Get current user profile"
)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Retrieve the profile of the currently authenticated user, 
    including their active business memberships, roles, and permissions.
    """
    memberships = [
        BusinessMembershipResponse(business_id=m.business_id, role_id=m.role_id)
        for m in current_user.memberships
    ]
    roles = [
        RoleResponse(id=r.id, name=r.name)
        for r in current_user.roles
    ]
    
    return CurrentUserResponse(
        user=UserResponse.model_validate(current_user),
        memberships=memberships,
        roles=roles
    )
