import { useState, useEffect } from "react";
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

export function useSubscription() {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadSubscription();
  }, []);

  const loadSubscription = async () => {
    try {
      const response = await api.get("/api/v1/billing/subscription", {
        headers: { "X-Current-Org": "1" },
      });
      console.log("Subscription data:", response.data);
      setSubscription(response.data);
    } catch (error) {
      console.error("Failed to load subscription:", error);
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
