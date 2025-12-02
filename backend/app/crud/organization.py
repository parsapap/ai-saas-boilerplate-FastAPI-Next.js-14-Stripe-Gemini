from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from app.models.organization import Organization, Membership, MemberRole
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


async def get_organization_by_id(db: AsyncSession, org_id: int) -> Optional[Organization]:
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    return result.scalar_one_or_none()


async def get_organization_by_slug(db: AsyncSession, slug: str) -> Optional[Organization]:
    result = await db.execute(select(Organization).where(Organization.slug == slug))
    return result.scalar_one_or_none()


async def create_organization(
    db: AsyncSession,
    org_in: OrganizationCreate,
    owner_id: int
) -> Organization:
    """Create organization and add creator as owner"""
    db_org = Organization(
        name=org_in.name,
        slug=org_in.slug,
        description=org_in.description
    )
    db.add(db_org)
    await db.flush()
    
    # Add creator as owner
    membership = Membership(
        user_id=owner_id,
        organization_id=db_org.id,
        role=MemberRole.OWNER
    )
    db.add(membership)
    
    await db.commit()
    await db.refresh(db_org)
    return db_org


async def update_organization(
    db: AsyncSession,
    org: Organization,
    org_in: OrganizationUpdate
) -> Organization:
    update_data = org_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(org, field, value)
    
    await db.commit()
    await db.refresh(org)
    return org


async def get_user_organizations(db: AsyncSession, user_id: int) -> List[Organization]:
    """Get all organizations user is member of"""
    result = await db.execute(
        select(Organization)
        .join(Membership)
        .where(
            and_(
                Membership.user_id == user_id,
                Membership.is_active == True,
                Organization.is_active == True
            )
        )
    )
    return result.scalars().all()


async def get_membership(
    db: AsyncSession,
    user_id: int,
    org_id: int
) -> Optional[Membership]:
    result = await db.execute(
        select(Membership).where(
            and_(
                Membership.user_id == user_id,
                Membership.organization_id == org_id
            )
        )
    )
    return result.scalar_one_or_none()


async def create_membership(
    db: AsyncSession,
    user_id: int,
    org_id: int,
    role: MemberRole,
    invited_by: int
) -> Membership:
    membership = Membership(
        user_id=user_id,
        organization_id=org_id,
        role=role,
        invited_by=invited_by
    )
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership


async def get_organization_members(db: AsyncSession, org_id: int) -> List[Membership]:
    result = await db.execute(
        select(Membership)
        .where(Membership.organization_id == org_id)
        .order_by(Membership.joined_at.desc())
    )
    return result.scalars().all()


async def update_membership_role(
    db: AsyncSession,
    membership: Membership,
    role: MemberRole
) -> Membership:
    membership.role = role
    await db.commit()
    await db.refresh(membership)
    return membership


async def delete_membership(db: AsyncSession, membership: Membership):
    await db.delete(membership)
    await db.commit()


async def check_user_permission(
    db: AsyncSession,
    user_id: int,
    org_id: int,
    required_roles: List[MemberRole]
) -> bool:
    """Check if user has required role in organization"""
    membership = await get_membership(db, user_id, org_id)
    if not membership or not membership.is_active:
        return False
    return membership.role in required_roles
