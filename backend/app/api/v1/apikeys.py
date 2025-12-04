from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.dependencies import get_current_active_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyWithSecret
from app.crud import api_key as crud_api_key

router = APIRouter()


@router.post("/", response_model=ApiKeyWithSecret, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_in: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """
    Generate a new API key for current organization
    
    ⚠️ The full key is only shown once! Save it securely.
    """
    api_key, full_key = await crud_api_key.create_api_key(
        db, key_in, current_org.id, current_user.id
    )
    
    # Return with full key (only time it's visible)
    return ApiKeyWithSecret(
        id=api_key.id,
        name=api_key.name,
        key_prefix=api_key.key_prefix,
        organization_id=api_key.organization_id,
        created_by=api_key.created_by,
        last_used_at=api_key.last_used_at,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
        key=full_key
    )


@router.get("/", response_model=List[ApiKeyResponse])
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """List all API keys for current organization"""
    keys = await crud_api_key.get_organization_api_keys(db, current_org.id)
    return keys


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Revoke (deactivate) an API key"""
    keys = await crud_api_key.get_organization_api_keys(db, current_org.id)
    api_key = next((k for k in keys if k.id == key_id), None)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    await crud_api_key.revoke_api_key(db, api_key)


@router.delete("/{key_id}/permanent", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    current_org: Organization = Depends(get_current_organization)
):
    """Permanently delete an API key"""
    keys = await crud_api_key.get_organization_api_keys(db, current_org.id)
    api_key = next((k for k in keys if k.id == key_id), None)
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    await crud_api_key.delete_api_key(db, api_key)
