"use client";

import { motion } from "framer-motion";
import { Check, X } from "lucide-react";

const features = [
  {
    category: "Usage",
    items: [
      { name: "Messages per month", free: "100", pro: "10,000", team: "Unlimited" },
      { name: "AI Models", free: "Basic", pro: "Advanced", team: "All" },
      { name: "API Access", free: false, pro: true, team: true },
    ],
  },
  {
    category: "Collaboration",
    items: [
      { name: "Organizations", free: "1", pro: "5", team: "Unlimited" },
      { name: "Team Members", free: "1", pro: "10", team: "Unlimited" },
      { name: "Shared Workspaces", free: false, pro: true, team: true },
    ],
  },
  {
    category: "Support",
    items: [
      { name: "Email Support", free: true, pro: true, team: true },
      { name: "Priority Support", free: false, pro: true, team: true },
      { name: "24/7 Dedicated Support", free: false, pro: false, team: true },
      { name: "SLA Guarantee", free: false, pro: false, team: true },
    ],
  },
];

export function FeatureComparison() {
  const renderValue = (value: string | boolean) => {
    if (typeof value === "boolean") {
      return value ? (
        <Check className="w-5 h-5 text-green-400 mx-auto" />
      ) : (
        <X className="w-5 h-5 text-white/20 mx-auto" />
      );
    }
    return <span className="text-sm">{value}</span>;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8, duration: 0.5 }}
      className="max-w-5xl mx-auto mt-20"
    >
      <h2 className="text-3xl font-bold text-center mb-8">
        Compare all features
      </h2>

      <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
        {/* Header */}
        <div className="grid grid-cols-4 gap-4 p-6 border-b border-white/10 bg-white/5">
          <div className="font-semibold">Feature</div>
          <div className="text-center font-semibold">Free</div>
          <div className="text-center font-semibold">Pro</div>
          <div className="text-center font-semibold">Team</div>
        </div>

        {/* Features */}
        {features.map((category, categoryIndex) => (
          <div key={categoryIndex}>
            <div className="px-6 py-3 bg-white/5 border-b border-white/10">
              <h3 className="font-semibold text-sm text-white/80">
                {category.category}
              </h3>
            </div>
            {category.items.map((item, itemIndex) => (
              <motion.div
                key={itemIndex}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.9 + itemIndex * 0.05 }}
                className="grid grid-cols-4 gap-4 p-6 border-b border-white/10 hover:bg-white/5 transition-colors duration-200"
              >
                <div className="text-sm text-white/80">{item.name}</div>
                <div className="text-center">{renderValue(item.free)}</div>
                <div className="text-center">{renderValue(item.pro)}</div>
                <div className="text-center">{renderValue(item.team)}</div>
              </motion.div>
            ))}
          </div>
        ))}
      </div>
    </motion.div>
  );
}
