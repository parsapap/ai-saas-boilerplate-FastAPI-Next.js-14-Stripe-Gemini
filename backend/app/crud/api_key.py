from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List, Tuple
from datetime import datetime
import secrets
import hashlib
from app.models.api_key import ApiKey
from app.schemas.api_key import ApiKeyCreate


def generate_api_key() -> Tuple[str, str, str]:
    """
    Generate API key in format: sk-{random_string}
    Returns: (full_key, prefix, hash)
    """
    random_part = secrets.token_urlsafe(32)
    full_key = f"sk-{random_part}"
    prefix = full_key[:8]  # sk-xxxxx
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    return full_key, prefix, key_hash


async def create_api_key(
    db: AsyncSession,
    key_in: ApiKeyCreate,
    organization_id: int,
    user_id: int
) -> Tuple[ApiKey, str]:
    """Create API key and return it with the secret (only time it's visible)"""
    full_key, prefix, key_hash = generate_api_key()
    
    db_key = ApiKey(
        name=key_in.name,
        key_prefix=prefix,
        key_hash=key_hash,
        organization_id=organization_id,
        created_by=user_id,
        expires_at=key_in.expires_at
    )
    db.add(db_key)
    await db.commit()
    await db.refresh(db_key)
    
    return db_key, full_key


async def get_api_key_by_hash(db: AsyncSession, key_hash: str) -> Optional[ApiKey]:
    result = await db.execute(
        select(ApiKey).where(
            and_(
                ApiKey.key_hash == key_hash,
                ApiKey.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()


async def get_organization_api_keys(db: AsyncSession, org_id: int) -> List[ApiKey]:
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.organization_id == org_id)
        .order_by(ApiKey.created_at.desc())
    )
    return result.scalars().all()


async def update_api_key_last_used(db: AsyncSession, api_key: ApiKey):
    api_key.last_used_at = datetime.utcnow()
    await db.commit()


async def revoke_api_key(db: AsyncSession, api_key: ApiKey):
    api_key.is_active = False
    await db.commit()


async def delete_api_key(db: AsyncSession, api_key: ApiKey):
    await db.delete(api_key)
    await db.commit()


def hash_api_key(key: str) -> str:
    """Hash an API key for lookup"""
    return hashlib.sha256(key.encode()).hexdigest()
