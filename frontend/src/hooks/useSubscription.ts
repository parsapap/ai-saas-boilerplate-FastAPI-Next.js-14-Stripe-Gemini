import { useState, useEffect, useRef } from "react";
import { api } from "@/lib/api";

interface Subscription {
  id: string;
  plan_type: string;
  status: string;
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
}

export const planDetails = {
  FREE: {
    name: "Free",
    price: "$0",
    limit: "100 messages/month",
    features: ["100 messages/month", "Basic AI models", "Email support"],
  },
  PRO: {
    name: "Pro",
    price: "$29",
    limit: "10,000 messages/month",
    features: ["10,000 messages/month", "Advanced AI models", "Priority support"],
  },
  TEAM: {
    name: "Team",
    price: "$99",
    limit: "Unlimited messages",
    features: ["Unlimited messages", "All AI models", "24/7 support"],
  },
};

// Global cache to prevent multiple simultaneous requests across all components
let cachedSubscription: Subscription | null = null;
let cacheTimestamp: number = 0;
let pendingRequest: Promise<Subscription | null> | null = null;
const CACHE_DURATION = 300000; // 5 minutes

export function useSubscription(autoFetch = true) {
  const [subscription, setSubscription] = useState<Subscription | null>(cachedSubscription);
  const [isLoading, setIsLoading] = useState(!cachedSubscription);
  const hasFetchedRef = useRef(false);

  useEffect(() => {
    // Only fetch once per component mount
    if (autoFetch && !hasFetchedRef.current) {
      hasFetchedRef.current = true;
      loadSubscription();
    }
  }, [autoFetch]);

  const loadSubscription = async () => {
    try {
      // Return cached data if still valid
      const now = Date.now();
      if (cachedSubscription && now - cacheTimestamp < CACHE_DURATION) {
        if (subscription !== cachedSubscription) {
          setSubscription(cachedSubscription);
        }
        setIsLoading(false);
        return cachedSubscription;
      }

      // If there's already a pending request, wait for it
      if (pendingRequest) {
        const result = await pendingRequest;
        if (subscription !== result) {
          setSubscription(result);
        }
        setIsLoading(false);
        return result;
      }

      // Make new request
      setIsLoading(true);
      pendingRequest = api
        .get("/api/v1/billing/subscription", {
          headers: { "X-Current-Org": "1" },
        })
        .then((response) => {
          cachedSubscription = response.data;
          cacheTimestamp = Date.now();
          return response.data;
        })
        .catch((error) => {
          console.error("Failed to load subscription:", error);
          return null;
        })
        .finally(() => {
          pendingRequest = null;
        });

      const result = await pendingRequest;
      if (subscription !== result) {
        setSubscription(result);
      }
      return result;
    } catch (error) {
      console.error("Failed to load subscription:", error);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const currentPlan = subscription
    ? planDetails[subscription.plan_type?.toUpperCase() as keyof typeof planDetails] || planDetails.FREE
    : planDetails.FREE;

  return {
    subscription,
    currentPlan,
    isLoading,
    refetch: loadSubscription,
  };
}

// Helper to clear cache when needed (e.g., after plan upgrade)
export function clearSubscriptionCache() {
  cachedSubscription = null;
  cacheTimestamp = 0;
  pendingRequest = null;
}
