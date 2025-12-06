from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token
from app.crud import user as crud_user
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user and create Stripe customer"""
    # Check if user exists
    user = await crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create Stripe customer (optional - will be created later if needed)
    stripe_customer_id = None
    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        if stripe.api_key and stripe.api_key != "sk_test_dummy" and not stripe.api_key.startswith("sk_test_dummy"):
            stripe_customer = stripe.Customer.create(
                email=user_in.email,
                name=user_in.full_name,
                metadata={"source": "saas_registration"}
            )
            stripe_customer_id = stripe_customer.id
    except Exception as e:
        # Log error but don't fail registration
        print(f"Warning: Failed to create Stripe customer: {str(e)}")
        # Customer will be created later when needed
    
    # Create user
    user = await crud_user.create_user(db, user_in=user_in, stripe_customer_id=stripe_customer_id)
    
    # Create default organization for new user
    from app.crud import organization as crud_org
    from app.crud import subscription as crud_subscription
    from app.models.subscription import PlanType
    from app.schemas.organization import OrganizationCreate
    import re
    
    # Generate slug from email
    email_prefix = user_in.email.split('@')[0]
    slug = re.sub(r'[^a-z0-9-]', '-', email_prefix.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')  # Remove multiple dashes
    
    # Ensure unique slug
    base_slug = slug
    counter = 1
    while await crud_org.get_organization_by_slug(db, slug):
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    org_in = OrganizationCreate(
        name=f"{user_in.full_name}'s Organization" if user_in.full_name else "My Organization",
        slug=slug,
        description="Default organization"
    )
    org = await crud_org.create_organization(db, org_in, user.id)
    
    # Create FREE subscription for the organization
    await crud_subscription.create_subscription(
        db,
        org_id=org.id,
        plan_type=PlanType.FREE
    )
    
    return user


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login and get access + refresh tokens"""
    user = await crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Refresh access token using refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise credentials_exception
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception
    
    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    
    new_access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
