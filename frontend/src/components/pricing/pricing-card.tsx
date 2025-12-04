"use client";

import { motion } from "framer-motion";
import { Check, Loader2 } from "lucide-react";
import { useState } from "react";

interface PricingCardProps {
  name: string;
  price: number;
  period?: string;
  description: string;
  features: string[];
  highlighted?: boolean;
  buttonText: string;
  onSelect: () => Promise<void>;
  delay?: number;
}

export function PricingCard({
  name,
  price,
  period = "month",
  description,
  features,
  highlighted = false,
  buttonText,
  onSelect,
  delay = 0,
}: PricingCardProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    try {
      await onSelect();
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
      whileHover={{ y: -8, transition: { duration: 0.3 } }}
      className={`relative p-8 rounded-2xl backdrop-blur-xl transition-all duration-300 ${
        highlighted
          ? "bg-white/10 border-2 border-white/30 shadow-2xl shadow-white/10"
          : "bg-white/5 border border-white/10 hover:border-white/20"
      }`}
    >
      {highlighted && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: delay + 0.2 }}
          className="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-white text-black text-sm font-medium rounded-full"
        >
          Most Popular
        </motion.div>
      )}

      <div className="mb-6">
        <h3 className="text-2xl font-bold mb-2">{name}</h3>
        <p className="text-white/60 text-sm">{description}</p>
      </div>

      <div className="mb-6">
        <div className="flex items-baseline gap-2">
          <span className="text-5xl font-bold">${price}</span>
          {price > 0 && (
            <span className="text-white/60">/{period}</span>
          )}
        </div>
      </div>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleClick}
        disabled={isLoading}
        className={`w-full py-3 px-6 rounded-lg font-medium transition-all duration-300 mb-8 ${
          highlighted
            ? "bg-white text-black hover:bg-white/90"
            : "bg-white/10 hover:bg-white/20 border border-white/20"
        }`}
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            Loading...
          </span>
        ) : (
          buttonText
        )}
      </motion.button>

      <div className="space-y-4">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: delay + 0.1 + index * 0.05 }}
            className="flex items-start gap-3"
          >
            <div className="mt-0.5 p-1 rounded-full bg-white/10">
              <Check className="w-4 h-4" />
            </div>
            <span className="text-sm text-white/80">{feature}</span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
