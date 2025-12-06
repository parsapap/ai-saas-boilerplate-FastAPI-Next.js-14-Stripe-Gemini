# Scripts Directory

## Development Scripts
- `start_backend.sh` - Start the backend server
- `start_local_dev.sh` - Start local development environment
- `run_manual.sh` - Run manual testing

## Deployment Scripts
- `deployment/deploy.sh` - Deploy to production
- `deployment/start.sh` - Start production services

## Stripe Scripts
- `stripe/setup_stripe.sh` - Setup Stripe integration
- `stripe/get_stripe_prices.py` - Fetch Stripe prices
- `stripe/upgrade_user_plan.sh` - Upgrade user subscription plan

## Test Scripts
- `tests/test_all.sh` - Run all tests
- `tests/test_all_features.sh` - Test all features
- `tests/test_chat_api.sh` - Test chat API
- `tests/test_complete_flow.sh` - Test complete user flow
- `tests/test_create_org.sh` - Test organization creation
- `tests/test_pricing_page.sh` - Test pricing page
- `tests/test_registration.py` - Test user registration
- `tests/test_stripe_quick.sh` - Quick Stripe test
- `tests/test_stripe_simple.sh` - Simple Stripe test
- `tests/test_subscription_upgrade.py` - Test subscription upgrade
- `tests/test_user_registration.sh` - Test user registration flow

## Usage

All scripts should be run from the project root directory:

```bash
# Development
./scripts/start_local_dev.sh

# Testing
./scripts/tests/test_all.sh

# Deployment
./scripts/deployment/deploy.sh

# Stripe
./scripts/stripe/setup_stripe.sh
```
