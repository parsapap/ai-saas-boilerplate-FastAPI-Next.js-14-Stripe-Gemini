"use client";

import { motion } from "framer-motion";

export function TypingIndicator() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="flex w-full justify-start mb-6"
    >
      <div className="flex gap-4 max-w-[80%]">
        {/* Avatar */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
          className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-white/10 text-white border border-white/20"
        >
          AI
        </motion.div>

        {/* Typing Animation */}
        <motion.div
          initial={{ scale: 0.95 }}
          animate={{ scale: 1 }}
          className="rounded-2xl px-4 py-3 bg-white/5 backdrop-blur-xl border border-white/10"
        >
          <div className="flex items-center gap-1">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-2 h-2 bg-white/60 rounded-full"
                animate={{
                  y: [0, -8, 0],
                  opacity: [0.6, 1, 0.6],
                }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  delay: i * 0.15,
                  ease: "easeInOut",
                }}
              />
            ))}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
