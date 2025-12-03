parsapc@parsaPc:~/Desktop/ai-saas-boilerplate-FastAPI-Next.js-14-Stripe-Gemini$ git log --oneline -10
a0b989f (HEAD -> dev, origin/dev) docs: add multi-tenant documentation and test scripts
46d7b62 feat(migrations): add database migrations for multi-tenant
f48943d feat(app): register multi-tenant routers in main app
9f6bfb6 feat(api): add organizations and API keys endpoints
b43fe42 feat(auth): add API key authentication and organization context
8521319 feat(crud): add organization and API key CRUD operations
54aea73 feat(schemas): add multi-tenant Pydantic schemas
dc18b4d feat(models): add multi-tenant models (Organization, Members
hip, ApiKey)
556f76c docs: add project summary and tree structure
6dad500 docs: add setup checklist
(END)from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.organization import MemberRole


class OrganizationBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=50, pattern="^[a-z0-9-]+$")
    description: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Organization(OrganizationBase):
    id: int
    is_active: bool
    stripe_customer_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MembershipBase(BaseModel):
    role: MemberRole


class MembershipCreate(BaseModel):
    email: str
    role: MemberRole = MemberRole.MEMBER


class MembershipUpdate(BaseModel):
    role: Optional[MemberRole] = None
    is_active: Optional[bool] = None


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    organization_id: int
    role: MemberRole
    is_active: bool
    joined_at: datetime
    user_email: str
    user_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class OrganizationWithRole(Organization):
    user_role: MemberRole
    
    class Config:
        from_attributes = True
