"use client";

import { motion } from "framer-motion";

export function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      {/* Stats Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: i * 0.1 }}
            className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1 space-y-3">
                <div className="h-4 w-24 bg-white/10 rounded animate-pulse" />
                <div className="h-8 w-32 bg-white/10 rounded animate-pulse" />
                <div className="h-3 w-28 bg-white/10 rounded animate-pulse" />
              </div>
              <div className="w-12 h-12 bg-white/10 rounded-lg animate-pulse" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
        >
          <div className="space-y-4">
            <div className="h-6 w-32 bg-white/10 rounded animate-pulse" />
            <div className="h-64 bg-white/5 rounded-lg animate-pulse" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
        >
          <div className="space-y-4">
            <div className="h-6 w-32 bg-white/10 rounded animate-pulse" />
            <div className="h-64 bg-white/5 rounded-lg animate-pulse" />
          </div>
        </motion.div>
      </div>

      {/* Recent Chats Skeleton */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
      >
        <div className="space-y-4">
          <div className="h-6 w-32 bg-white/10 rounded animate-pulse" />
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="p-4 rounded-lg bg-white/5 border border-white/5"
            >
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-white/10 rounded-lg animate-pulse" />
                <div className="flex-1 space-y-2">
                  <div className="h-4 w-48 bg-white/10 rounded animate-pulse" />
                  <div className="h-3 w-full bg-white/10 rounded animate-pulse" />
                  <div className="h-3 w-24 bg-white/10 rounded animate-pulse" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
