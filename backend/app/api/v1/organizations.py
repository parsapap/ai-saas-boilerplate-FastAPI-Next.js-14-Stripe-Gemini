from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.dependencies import (
    get_current_active_user,
    get_current_organization,
    require_admin,
    require_owner
)
from app.models.user import User
from app.models.organization import Organization, MemberRole
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    Organization as OrganizationSchema,
    OrganizationWithRole,
    MembershipCreate,
    MembershipResponse,
    MembershipUpdate
)
from app.crud import organization as crud_org
from app.crud import user as crud_user

router = APIRouter()


@router.post("/", response_model=OrganizationSchema, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_in: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new organization (user becomes owner)"""
    # Check if slug already exists
    existing = await crud_org.get_organization_by_slug(db, org_in.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug already exists"
        )
    
    org = await crud_org.create_organization(db, org_in, current_user.id)
    return org


@router.get("/", response_model=List[OrganizationWithRole])
async def list_my_organizations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all organizations current user is member of"""
    orgs = await crud_org.get_user_organizations(db, current_user.id)
    
    # Add user role to each org
    result = []
    for org in orgs:
        membership = await crud_org.get_membership(db, current_user.id, org.id)
        org_dict = OrganizationSchema.model_validate(org).model_dump()
        org_dict["user_role"] = membership.role
        result.append(OrganizationWithRole(**org_dict))
    
    return result


@router.get("/{org_id}", response_model=OrganizationSchema)
async def get_organization(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get organization details"""
    org = await crud_org.get_organization_by_id(db, org_id)
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


@router.patch("/{org_id}", response_model=OrganizationSchema)
async def update_organization(
    org_id: int,
    org_in: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update organization (admin or owner only)"""
    org = await crud_org.get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check permission
    has_permission = await crud_org.check_user_permission(
        db, current_user.id, org_id, [MemberRole.OWNER, MemberRole.ADMIN]
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and owners can update organization"
        )
    
    org = await crud_org.update_organization(db, org, org_in)
    return org



@router.post("/{org_id}/invite", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
async def invite_member(
    org_id: int,
    invite: MembershipCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Invite a user to organization (admin or owner only)"""
    # Check permission
    has_permission = await crud_org.check_user_permission(
        db, current_user.id, org_id, [MemberRole.OWNER, MemberRole.ADMIN]
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and owners can invite members"
        )
    
    # Get user by email
    user = await crud_user.get_user_by_email(db, invite.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. They must register first."
        )
    
    # Check if already member
    existing = await crud_org.get_membership(db, user.id, org_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member"
        )
    
    # Create membership
    membership = await crud_org.create_membership(
        db, user.id, org_id, invite.role, current_user.id
    )
    
    # Build response
    return MembershipResponse(
        id=membership.id,
        user_id=membership.user_id,
        organization_id=membership.organization_id,
        role=membership.role,
        is_active=membership.is_active,
        joined_at=membership.joined_at,
        user_email=user.email,
        user_name=user.full_name
    )


@router.get("/{org_id}/members", response_model=List[MembershipResponse])
async def list_organization_members(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all members of organization"""
    # Check user is member
    membership = await crud_org.get_membership(db, current_user.id, org_id)
    if not membership or not membership.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization"
        )
    
    memberships = await crud_org.get_organization_members(db, org_id)
    
    # Build response with user info
    result = []
    for m in memberships:
        user = await crud_user.get_user_by_id(db, m.user_id)
        result.append(MembershipResponse(
            id=m.id,
            user_id=m.user_id,
            organization_id=m.organization_id,
            role=m.role,
            is_active=m.is_active,
            joined_at=m.joined_at,
            user_email=user.email,
            user_name=user.full_name
        ))
    
    return result


@router.patch("/{org_id}/members/{user_id}", response_model=MembershipResponse)
async def update_member_role(
    org_id: int,
    user_id: int,
    update: MembershipUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update member role (owner only)"""
    # Check permission
    has_permission = await crud_org.check_user_permission(
        db, current_user.id, org_id, [MemberRole.OWNER]
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can update member roles"
        )
    
    membership = await crud_org.get_membership(db, user_id, org_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Update role
    if update.role:
        membership = await crud_org.update_membership_role(db, membership, update.role)
    
    # Update active status
    if update.is_active is not None:
        membership.is_active = update.is_active
        await db.commit()
        await db.refresh(membership)
    
    user = await crud_user.get_user_by_id(db, user_id)
    return MembershipResponse(
        id=membership.id,
        user_id=membership.user_id,
        organization_id=membership.organization_id,
        role=membership.role,
        is_active=membership.is_active,
        joined_at=membership.joined_at,
        user_email=user.email,
        user_name=user.full_name
    )


@router.delete("/{org_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    org_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove member from organization (admin or owner only)"""
    # Check permission
    has_permission = await crud_org.check_user_permission(
        db, current_user.id, org_id, [MemberRole.OWNER, MemberRole.ADMIN]
    )
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and owners can remove members"
        )
    
    membership = await crud_org.get_membership(db, user_id, org_id)
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Membership not found"
        )
    
    # Can't remove yourself if you're the only owner
    if user_id == current_user.id and membership.role == MemberRole.OWNER:
        # Check if there are other owners
        members = await crud_org.get_organization_members(db, org_id)
        owners = [m for m in members if m.role == MemberRole.OWNER and m.user_id != user_id]
        if not owners:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the last owner. Transfer ownership first."
            )
    
    await crud_org.delete_membership(db, membership)
