#!/usr/bin/env python3
"""Manually fix subscription plan in database"""

import requests
import sys

API_URL = "http://localhost:8000"

def main():
    # Get credentials
    email = input("Enter email: ").strip() or "chattest@example.com"
    password = input("Enter password: ").strip() or "Test123!@#"
    org_id = input("Enter organization ID: ").strip() or "2"
    
    print("\nSelect plan:")
    print("1. FREE")
    print("2. PRO")
    print("3. TEAM")
    plan_choice = input("Enter choice (1-3): ").strip()
    
    plan_map = {"1": "FREE", "2": "PRO", "3": "TEAM"}
    plan_type = plan_map.get(plan_choice, "PRO")
    
    print(f"\n🔐 Logging in as {email}...")
    
    # Login
    login_resp = requests.post(
        f"{API_URL}/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    
    if login_resp.status_code != 200:
        print(f"❌ Login failed: {login_resp.text}")
        sys.exit(1)
    
    token = login_resp.json()["access_token"]
    print("✅ Logged in successfully")
    
    # Get current subscription
    print(f"\n📊 Checking current subscription for org {org_id}...")
    sub_resp = requests.get(
        f"{API_URL}/api/v1/billing/subscription",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Current-Org": org_id
        }
    )
    
    if sub_resp.status_code == 200:
        current_sub = sub_resp.json()
        print(f"Current plan: {current_sub['plan_type']}")
        print(f"Status: {current_sub['status']}")
    
    # Update via admin endpoint (if exists) or direct database
    print(f"\n⚠️  Manual database update required")
    print(f"\nTo fix this, run this SQL in your database:")
    print(f"\nUPDATE subscriptions SET plan_type = '{plan_type.lower()}' WHERE organization_id = {org_id};")
    print(f"\nOr use the admin panel at: http://localhost:8000/admin")
    
    # Alternative: trigger a webhook manually
    print(f"\n💡 Alternative: Use Stripe CLI to trigger webhook:")
    print(f"stripe trigger checkout.session.completed")

if __name__ == "__main__":
    main()
