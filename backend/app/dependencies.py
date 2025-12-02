from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple
from app.database import get_db
from app.core.security import decode_token
from app.crud import user as crud_user
from app.crud import organization as crud_org
from app.crud import api_key as crud_api_key
from app.models.user import User
from app.models.organization import Organization, MemberRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_or_api_key(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
    api_key: Optional[str] = Depends(api_key_header)
) -> Tuple[Optional[User], Optional[Organization]]:
    """
    Authenticate via JWT token OR API key
    Returns: (user, organization)
    - JWT: (user, None) - org selected via header
    - API Key: (None, organization) - org from API key
    """
    # Try API Key first
    if api_key:
        if not api_key.startswith("sk-"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key format"
            )
        
        key_hash = crud_api_key.hash_api_key(api_key)
        db_key = await crud_api_key.get_api_key_by_hash(db, key_hash)
        
        if not db_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Check expiration
        if db_key.expires_at and db_key.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key expired"
            )
        
        # Update last used
        await crud_api_key.update_api_key_last_used(db, db_key)
        
        # Get organization
        org = await crud_org.get_organization_by_id(db, db_key.organization_id)
        if not org or not org.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Organization not found or inactive"
            )
        
        return None, org
    
    # Try JWT token
    if token:
        payload = decode_token(token)
        if payload and payload.get("type") == "access":
            user_id = payload.get("sub")
            if user_id:
                user = await crud_user.get_user_by_id(db, user_id=user_id)
                if user and user.is_active:
                    return user, None
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_organization(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    x_current_org: Optional[str] = Header(None)
) -> Organization:
    """Get current organization from header"""
    if not x_current_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Current-Org header required"
        )
    
    # Try to parse as ID or slug
    try:
        org_id = int(x_current_org)
        org = await crud_org.get_organization_by_id(db, org_id)
    except ValueError:
        org = await crud_org.get_organization_by_slug(db, x_current_org)
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check user is member
    membership = await crud_org.get_membership(db, current_user.id, org.id)
    if not membership or not membership.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization"
        )
    
    return org


async def require_org_role(
    required_roles: list[MemberRole],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Check if user has required role in current organization"""
    membership = await crud_org.get_membership(db, current_user.id, current_org.id)
    
    if not membership or membership.role not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Required role: {', '.join([r.value for r in required_roles])}"
        )
    
    return membership


# Specific role dependencies
async def require_owner(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    return await require_org_role([MemberRole.OWNER], db, current_user, current_org)


async def require_admin(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    return await require_org_role([MemberRole.OWNER, MemberRole.ADMIN], db, current_user, current_org)


from datetime import datetime
