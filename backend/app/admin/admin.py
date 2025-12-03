from sqladmin import Admin, ModelView
from app.models.user import User
from app.models.organization import Organization, Membership
from app.models.subscription import Subscription
from app.models.api_key import ApiKey
from app.models.ai_usage import AIUsage
from sqlalchemy import select
from app.core.security import verify_password


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    
    column_list = [User.id, User.email, User.full_name, User.is_active, User.created_at]
    column_searchable_list = [User.email, User.full_name]
    column_sortable_list = [User.id, User.email, User.created_at]
    column_default_sort = [(User.created_at, True)]
    
    form_excluded_columns = [User.hashed_password, User.created_at, User.updated_at]
    
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True


class OrganizationAdmin(ModelView, model=Organization):
    name = "Organization"
    name_plural = "Organizations"
    icon = "fa-solid fa-building"
    
    column_list = [
        Organization.id,
        Organization.name,
        Organization.slug,
        Organization.is_active,
        Organization.stripe_customer_id,
        Organization.created_at
    ]
    column_searchable_list = [Organization.name, Organization.slug]
    column_sortable_list = [Organization.id, Organization.name, Organization.created_at]
    column_default_sort = [(Organization.created_at, True)]
    
    form_excluded_columns = [Organization.created_at, Organization.updated_at]
    
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True


class SubscriptionAdmin(ModelView, model=Subscription):
    name = "Subscription"
    name_plural = "Subscriptions"
    icon = "fa-solid fa-credit-card"
    
    column_list = [
        Subscription.id,
        Subscription.organization_id,
        Subscription.plan_type,
        Subscription.status,
        Subscription.amount,
        Subscription.current_period_end,
        Subscription.created_at
    ]
    column_searchable_list = [Subscription.stripe_subscription_id]
    column_sortable_list = [Subscription.id, Subscription.created_at, Subscription.plan_type]
    column_default_sort = [(Subscription.created_at, True)]
    
    form_excluded_columns = [Subscription.created_at, Subscription.updated_at]
    
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True


class MembershipAdmin(ModelView, model=Membership):
    name = "Membership"
    name_plural = "Memberships"
    icon = "fa-solid fa-users"
    
    column_list = [
        Membership.id,
        Membership.user_id,
        Membership.organization_id,
        Membership.role,
        Membership.is_active,
        Membership.joined_at
    ]
    column_sortable_list = [Membership.id, Membership.joined_at]
    column_default_sort = [(Membership.joined_at, True)]
    
    form_excluded_columns = [Membership.joined_at]
    
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class ApiKeyAdmin(ModelView, model=ApiKey):
    name = "API Key"
    name_plural = "API Keys"
    icon = "fa-solid fa-key"
    
    column_list = [
        ApiKey.id,
        ApiKey.name,
        ApiKey.organization_id,
        ApiKey.is_active,
        ApiKey.last_used_at,
        ApiKey.created_at
    ]
    column_searchable_list = [ApiKey.name]
    column_sortable_list = [ApiKey.id, ApiKey.created_at, ApiKey.last_used_at]
    column_default_sort = [(ApiKey.created_at, True)]
    
    # Hide the actual key hash
    form_excluded_columns = [ApiKey.key_hash, ApiKey.created_at, ApiKey.last_used_at]
    column_exclude_list = [ApiKey.key_hash]
    
    can_create = False  # Keys should be created via API
    can_edit = True
    can_delete = True
    can_view_details = True


class AIUsageAdmin(ModelView, model=AIUsage):
    name = "AI Usage"
    name_plural = "AI Usage"
    icon = "fa-solid fa-robot"
    
    column_list = [
        AIUsage.id,
        AIUsage.organization_id,
        AIUsage.provider,
        AIUsage.model,
        AIUsage.tokens_used,
        AIUsage.cost,
        AIUsage.created_at
    ]
    column_sortable_list = [AIUsage.id, AIUsage.created_at, AIUsage.tokens_used]
    column_default_sort = [(AIUsage.created_at, True)]
    
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True


def setup_admin(app, engine):
    """Setup admin panel"""
    admin = Admin(
        app,
        engine,
        title="AI SaaS Admin",
        base_url="/admin",
    )
    
    # Register models
    admin.add_view(UserAdmin)
    admin.add_view(OrganizationAdmin)
    admin.add_view(SubscriptionAdmin)
    admin.add_view(MembershipAdmin)
    admin.add_view(ApiKeyAdmin)
    admin.add_view(AIUsageAdmin)
    
    return admin
