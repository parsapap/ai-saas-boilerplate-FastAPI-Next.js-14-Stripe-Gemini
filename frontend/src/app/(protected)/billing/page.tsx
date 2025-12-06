"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CreditCard, ExternalLink, Calendar, TrendingUp } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { DashboardSkeleton } from "@/components/dashboard/skeleton";

interface Subscription {
  id: string;
  plan_type: string;
  status: string;
  current_period_start: string;
  current_period_end: string;
  cancel_at_period_end: boolean;
}

export default function BillingPage() {
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreatingPortal, setIsCreatingPortal] = useState(false);

  useEffect(() => {
    loadSubscription();
  }, []);

  const loadSubscription = async () => {
    try {
      const response = await api.get("/api/v1/billing/subscription", {
        headers: { "X-Current-Org": "1" },
      });
      setSubscription(response.data);
    } catch (error) {
      console.error("Failed to load subscription:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const openCustomerPortal = async () => {
    setIsCreatingPortal(true);
    try {
      const response = await api.post(
        "/api/v1/billing/portal",
        {
          return_url: `${window.location.origin}/billing`,
        },
        {
          headers: { "X-Current-Org": "1" },
        }
      );

      if (response.data.portal_url) {
        window.location.href = response.data.portal_url;
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to open billing portal");
      setIsCreatingPortal(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 lg:p-8">
        <DashboardSkeleton />
      </div>
    );
  }

  const planDetails = {
    FREE: {
      name: "Free",
      price: "$0",
      features: ["100 messages/month", "Basic AI models", "Email support"],
    },
    PRO: {
      name: "Pro",
      price: "$29",
      features: ["10,000 messages/month", "Advanced AI models", "Priority support"],
    },
    TEAM: {
      name: "Team",
      price: "$99",
      features: ["Unlimited messages", "All AI models", "24/7 support"],
    },
  };

  const currentPlan = subscription
    ? planDetails[subscription.plan_type as keyof typeof planDetails] || planDetails.FREE
    : planDetails.FREE;

  return (
    <div className="p-6 lg:p-8 space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold mb-2">Billing</h1>
        <p className="text-white/60">
          Manage your subscription and billing information
        </p>
      </motion.div>

      {/* Current Plan */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="p-8 rounded-xl bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl border border-white/20"
      >
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold mb-2">{currentPlan.name} Plan</h2>
            <p className="text-3xl font-bold text-white/90">
              {currentPlan.price}
              {subscription && subscription.plan_type !== "FREE" && (
                <span className="text-lg text-white/60">/month</span>
              )}
            </p>
          </div>
          {subscription && subscription.status && (
            <div className="px-4 py-2 rounded-lg bg-green-500/20 border border-green-500/30">
              <span className="text-sm font-medium text-green-400 capitalize">
                {subscription.status}
              </span>
            </div>
          )}
        </div>

        <div className="space-y-2 mb-6">
          {currentPlan.features.map((feature, index) => (
            <div key={index} className="flex items-center gap-2 text-white/80">
              <div className="w-1.5 h-1.5 rounded-full bg-white/60" />
              <span>{feature}</span>
            </div>
          ))}
        </div>

        {subscription && subscription.plan_type !== "FREE" && (
          <div className="flex items-center gap-4 text-sm text-white/60 mb-6">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              <span>
                Renews on {new Date(subscription.current_period_end).toLocaleDateString()}
              </span>
            </div>
            {subscription.cancel_at_period_end && (
              <div className="px-3 py-1 rounded bg-yellow-500/20 text-yellow-400">
                Cancels at period end
              </div>
            )}
          </div>
        )}

        <div className="flex gap-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={openCustomerPortal}
            disabled={isCreatingPortal}
            className="px-6 py-3 bg-white text-black rounded-lg font-medium hover:bg-white/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <CreditCard className="w-5 h-5" />
            {isCreatingPortal ? "Loading..." : "Manage Billing"}
            <ExternalLink className="w-4 h-4" />
          </motion.button>

          {subscription?.plan_type === "FREE" && (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => (window.location.href = "/pricing")}
              className="px-6 py-3 bg-white/10 rounded-lg font-medium hover:bg-white/20 border border-white/20 transition-colors flex items-center gap-2"
            >
              <TrendingUp className="w-5 h-5" />
              Upgrade Plan
            </motion.button>
          )}
        </div>
      </motion.div>

      {/* Billing Portal Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="p-6 rounded-xl bg-white/5 border border-white/10"
      >
        <h3 className="text-lg font-semibold mb-4">Billing Portal</h3>
        <p className="text-white/60 mb-4">
          Click "Manage Billing" to access the Stripe Customer Portal where you can:
        </p>
        <ul className="space-y-2 text-white/80">
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-white/60 mt-2" />
            <span>Update your payment method</span>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-white/60 mt-2" />
            <span>View billing history and invoices</span>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-white/60 mt-2" />
            <span>Update billing information</span>
          </li>
          <li className="flex items-start gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-white/60 mt-2" />
            <span>Cancel your subscription</span>
          </li>
        </ul>
      </motion.div>

      {/* Usage Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-6"
      >
        <div className="p-6 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-white/60 mb-2">Messages This Month</p>
          <p className="text-3xl font-bold">125</p>
          <p className="text-sm text-white/40 mt-1">of 1,000 used</p>
        </div>
        <div className="p-6 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-white/60 mb-2">API Calls</p>
          <p className="text-3xl font-bold">1,234</p>
          <p className="text-sm text-white/40 mt-1">this month</p>
        </div>
        <div className="p-6 rounded-xl bg-white/5 border border-white/10">
          <p className="text-sm text-white/60 mb-2">Team Members</p>
          <p className="text-3xl font-bold">3</p>
          <p className="text-sm text-white/40 mt-1">active users</p>
        </div>
      </motion.div>
    </div>
  );
}
