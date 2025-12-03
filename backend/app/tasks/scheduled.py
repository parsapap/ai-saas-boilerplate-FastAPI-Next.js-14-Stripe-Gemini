from celery import shared_task
from sqlalchemy import select, update
from app.database import SessionLocal
from app.models.ai_usage import AIUsage
from app.models.subscription import Subscription, PlanType
from app.models.organization import Organization
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name="reset_daily_usage")
def reset_daily_usage():
    """Reset daily usage counters for all organizations"""
    logger.info("Starting daily usage reset task")
    
    # This would reset any daily limits if you implement them
    # For now, it's a placeholder for future daily limit tracking
    
    logger.info("Daily usage reset completed")
    return {"status": "completed", "timestamp": datetime.utcnow().isoformat()}


@shared_task(name="generate_usage_reports")
def generate_usage_reports():
    """Generate and send usage reports to organizations"""
    logger.info("Starting usage report generation")
    
    db = SessionLocal()
    try:
        # Get all active organizations
        result = db.execute(
            select(Organization).where(Organization.is_active == True)
        )
        organizations = result.scalars().all()
        
        for org in organizations:
            # Calculate usage for the past 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            usage_result = db.execute(
                select(AIUsage)
                .where(AIUsage.organization_id == org.id)
                .where(AIUsage.created_at >= thirty_days_ago)
            )
            usage_records = usage_result.scalars().all()
            
            if usage_records:
                total_tokens = sum(u.tokens_used for u in usage_records)
                total_cost = sum(float(u.cost) for u in usage_records)
                total_requests = len(usage_records)
                
                logger.info(
                    f"Org {org.id} ({org.name}): "
                    f"{total_requests} requests, "
                    f"{total_tokens} tokens, "
                    f"${total_cost:.2f} cost"
                )
                
                # Here you would send an email report
                # For now, just log it
        
        logger.info("Usage report generation completed")
        return {"status": "completed", "organizations_processed": len(organizations)}
        
    except Exception as e:
        logger.error(f"Error generating usage reports: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()


@shared_task(name="check_subscription_renewals")
def check_subscription_renewals():
    """Check for subscriptions that need renewal reminders"""
    logger.info("Checking subscription renewals")
    
    db = SessionLocal()
    try:
        # Get subscriptions expiring in the next 7 days
        seven_days_from_now = datetime.utcnow() + timedelta(days=7)
        
        result = db.execute(
            select(Subscription)
            .where(Subscription.current_period_end <= seven_days_from_now)
            .where(Subscription.current_period_end >= datetime.utcnow())
            .where(Subscription.cancel_at_period_end == False)
        )
        expiring_subscriptions = result.scalars().all()
        
        for subscription in expiring_subscriptions:
            logger.info(
                f"Subscription {subscription.id} for org {subscription.organization_id} "
                f"expires on {subscription.current_period_end}"
            )
            # Here you would send a renewal reminder email
        
        logger.info(f"Found {len(expiring_subscriptions)} subscriptions expiring soon")
        return {
            "status": "completed",
            "expiring_subscriptions": len(expiring_subscriptions)
        }
        
    except Exception as e:
        logger.error(f"Error checking subscription renewals: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        db.close()


@shared_task(name="cleanup_old_usage_data")
def cleanup_old_usage_data(days=90):
    """Clean up AI usage data older than specified days"""
    logger.info(f"Cleaning up usage data older than {days} days")
    
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = db.execute(
            select(AIUsage).where(AIUsage.created_at < cutoff_date)
        )
        old_records = result.scalars().all()
        
        count = len(old_records)
        
        for record in old_records:
            db.delete(record)
        
        db.commit()
        
        logger.info(f"Cleaned up {count} old usage records")
        return {"status": "completed", "records_deleted": count}
        
    except Exception as e:
        logger.error(f"Error cleaning up old usage data: {e}")
        db.rollback()
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
