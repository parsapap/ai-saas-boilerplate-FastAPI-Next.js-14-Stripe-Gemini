"use client";

import { motion } from "framer-motion";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { PricingCard } from "@/components/pricing/pricing-card";
import { Navbar } from "@/components/navbar";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

const plans = [
  {
    name: "Free",
    price: 0,
    description: "Perfect for trying out our platform",
    features: [
      "100 messages per month",
      "Basic AI models",
      "Email support",
      "1 organization",
      "Community access",
    ],
    planType: "FREE",
  },
  {
    name: "Pro",
    price: 29,
    description: "For professionals and small teams",
    features: [
      "10,000 messages per month",
      "Advanced AI models",
      "Priority support",
      "5 organizations",
      "Custom integrations",
      "API access",
      "Advanced analytics",
    ],
    planType: "PRO",
    highlighted: true,
  },
  {
    name: "Team",
    price: 99,
    description: "For larger teams and enterprises",
    features: [
      "Unlimited messages",
      "All AI models",
      "24/7 dedicated support",
      "Unlimited organizations",
      "Custom integrations",
      "API access",
      "Advanced analytics",
      "SSO & SAML",
      "Custom contracts",
      "SLA guarantee",
    ],
    planType: "TEAM",
  },
];

export default function PricingPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { isAuthenticated } = useAuthStore();
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    // Handle success/cancel redirects
    const status = searchParams.get("status");
    const sessionId = searchParams.get("session_id");

    if (status === "success" && sessionId) {
      toast.success("Payment successful! Your subscription is now active.");
      // Clear query params
      router.replace("/pricing");
    } else if (status === "cancel") {
      toast.error("Payment cancelled. You can try again anytime.");
      // Clear query params
      router.replace("/pricing");
    }
  }, [searchParams, router]);

  const handleSelectPlan = async (planType: string) => {
    if (planType === "FREE") {
      if (isAuthenticated) {
        router.push("/dashboard");
      } else {
        router.push("/register");
      }
      return;
    }

    if (!isAuthenticated) {
      toast.error("Please login to subscribe");
      router.push("/login");
      return;
    }

    setIsProcessing(true);
    try {
      // Get current organization ID from localStorage
      const currentOrgId = localStorage.getItem('current_org_id');
      
      if (!currentOrgId) {
        toast.error("Please select an organization first");
        router.push("/dashboard");
        return;
      }

      const response = await api.post(
        "/api/v1/billing/checkout",
        {
          plan_type: planType,
          success_url: `${window.location.origin}/pricing?status=success&session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${window.location.origin}/pricing?status=cancel`,
        },
        {
          headers: {
            "X-Current-Org": currentOrgId,
          },
        }
      );

      // Redirect to Stripe Checkout
      if (response.data.checkout_url) {
        window.location.href = response.data.checkout_url;
      }
    } catch (error: any) {
      console.error("Checkout error:", error);
      
      // Handle validation errors
      if (error.response?.data?.detail) {
        const detail = error.response.data.detail;
        
        // Check if it's a validation error array
        if (Array.isArray(detail)) {
          const errorMessages = detail.map((err: any) => err.msg).join(', ');
          toast.error(`Validation error: ${errorMessages}`);
        } else if (typeof detail === 'string') {
          toast.error(detail);
        } else {
          toast.error("Failed to create checkout session");
        }
      } else {
        toast.error("Failed to create checkout session");
      }
      
      setIsProcessing(false);
    }
  };

  return (
    <>
      <div className="min-h-screen py-20 px-4 pt-32">
        <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4">
            Simple, transparent pricing
          </h1>
          <p className="text-xl text-white/60 max-w-2xl mx-auto">
            Choose the perfect plan for your needs. Upgrade, downgrade, or cancel
            anytime.
          </p>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <PricingCard
              key={plan.name}
              name={plan.name}
              price={plan.price}
              description={plan.description}
              features={plan.features}
              highlighted={plan.highlighted}
              buttonText={
                plan.price === 0
                  ? "Get Started"
                  : isProcessing
                  ? "Processing..."
                  : "Subscribe Now"
              }
              onSelect={() => handleSelectPlan(plan.planType)}
              delay={0.2 + index * 0.1}
            />
          ))}
        </div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="max-w-3xl mx-auto"
        >
          <h2 className="text-3xl font-bold text-center mb-8">
            Frequently asked questions
          </h2>
          <div className="space-y-6">
            {[
              {
                q: "Can I change plans later?",
                a: "Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.",
              },
              {
                q: "What payment methods do you accept?",
                a: "We accept all major credit cards through Stripe, including Visa, Mastercard, and American Express.",
              },
              {
                q: "Is there a free trial?",
                a: "Yes! The Free plan is available forever with no credit card required. You can upgrade anytime.",
              },
              {
                q: "Can I cancel my subscription?",
                a: "Yes, you can cancel your subscription at any time. You'll continue to have access until the end of your billing period.",
              },
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all duration-300"
              >
                <h3 className="text-lg font-semibold mb-2">{faq.q}</h3>
                <p className="text-white/60">{faq.a}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.5 }}
          className="text-center mt-20"
        >
          <div className="p-12 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
            <h2 className="text-3xl font-bold mb-4">
              Still have questions?
            </h2>
            <p className="text-white/60 mb-6">
              Our team is here to help. Contact us for more information.
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push("/contact")}
              className="px-8 py-3 bg-white text-black rounded-lg font-medium hover:bg-white/90 transition-colors duration-300"
            >
              Contact Sales
            </motion.button>
          </div>
        </motion.div>
      </div>
    </div>
    <Navbar />
    </>
  );
}
