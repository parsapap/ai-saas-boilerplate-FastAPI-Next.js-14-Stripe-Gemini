#!/bin/bash

# Upgrade user subscription plan
# Usage: ./upgrade_user_plan.sh <email> <plan_type>
# Example: ./upgrade_user_plan.sh parsa@gmail.com team

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: ./upgrade_user_plan.sh <email> <plan_type>"
    echo "Example: ./upgrade_user_plan.sh parsa@gmail.com team"
    echo ""
    echo "Plan types: free, pro, team"
    exit 1
fi

EMAIL=$1
PLAN=$2

# Validate plan type
if [[ ! "$PLAN" =~ ^(free|pro|team)$ ]]; then
    echo "❌ Invalid plan type: $PLAN"
    echo "   Valid options: free, pro, team"
    exit 1
fi

echo "🔍 Looking up user: $EMAIL"

# Connect to PostgreSQL and upgrade
docker exec -i postgres-saas psql -U postgres -d saas_db << EOF
-- Find user and their organization
WITH user_org AS (
    SELECT 
        u.id as user_id,
        u.email,
        o.id as org_id,
        o.name as org_name
    FROM users u
    JOIN memberships m ON m.user_id = u.id
    JOIN organizations o ON o.id = m.organization_id
    WHERE u.email = '$EMAIL'
    LIMIT 1
)
-- Show current status
SELECT 
    '👤 User: ' || uo.email as info,
    '🏢 Organization: ' || uo.org_name as org,
    '💳 Current Plan: ' || COALESCE(CAST(s.plan_type AS TEXT), 'FREE') as current_plan
FROM user_org uo
LEFT JOIN subscriptions s ON s.organization_id = uo.org_id;

-- Update subscription
UPDATE subscriptions
SET 
    plan_type = UPPER('$PLAN')::plantype,
    status = 'ACTIVE'::subscriptionstatus,
    updated_at = NOW()
FROM (
    SELECT o.id as org_id
    FROM users u
    JOIN memberships m ON m.user_id = u.id
    JOIN organizations o ON o.id = m.organization_id
    WHERE u.email = '$EMAIL'
    LIMIT 1
) AS user_org
WHERE subscriptions.organization_id = user_org.org_id;

-- Show updated status
SELECT 
    '✅ Updated Plan: ' || s.plan_type as result,
    '📊 Status: ' || s.status as status
FROM users u
JOIN memberships m ON m.user_id = u.id
JOIN organizations o ON o.id = m.organization_id
JOIN subscriptions s ON s.organization_id = o.id
WHERE u.email = '$EMAIL'
LIMIT 1;
EOF

echo ""
echo "🎉 Done! User $EMAIL is now on the $PLAN plan"
echo "   Refresh the dashboard to see the changes"
