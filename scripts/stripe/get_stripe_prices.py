#!/usr/bin/env python3
"""
Script to fetch Stripe Price IDs for your products
"""
import stripe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

print("🔍 Fetching Stripe Products and Prices...\n")
print("=" * 60)

try:
    # Get all products
    products = stripe.Product.list(limit=10, active=True)
    
    for product in products.data:
        print(f"\n📦 Product: {product.name}")
        print(f"   Product ID: {product.id}")
        print(f"   Description: {product.description or 'N/A'}")
        
        # Get prices for this product
        prices = stripe.Price.list(product=product.id, active=True)
        
        if prices.data:
            print(f"   💰 Prices:")
            for price in prices.data:
                amount = price.unit_amount / 100 if price.unit_amount else 0
                interval = price.recurring.interval if price.recurring else 'one-time'
                print(f"      → Price ID: {price.id}")
                print(f"        Amount: ${amount:.2f}/{interval}")
                print(f"        Currency: {price.currency.upper()}")
        else:
            print(f"   ⚠️  No prices found for this product")
        
        print("-" * 60)
    
    print("\n✅ Done! Copy the Price IDs above.\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure your STRIPE_SECRET_KEY is correct in backend/.env")
