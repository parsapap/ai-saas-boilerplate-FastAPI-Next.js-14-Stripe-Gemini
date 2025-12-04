"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { MessageSquare, TrendingUp, Zap, Plus } from "lucide-react";
import { useRouter } from "next/navigation";
import { StatsCard } from "@/components/dashboard/stats-card";
import { UsageChart } from "@/components/usage-chart";
import { ActivityChart } from "@/components/dashboard/activity-chart";
import { RecentChats } from "@/components/dashboard/recent-chats";
import { DashboardSkeleton } from "@/components/dashboard/skeleton";
import { aiApi } from "@/lib/api";
import { toast } from "sonner";

interface UsageData {
  total_messages: number;
  total_tokens: number;
  messages_limit: number | null;
  tokens_limit: number | null;
  usage_percentage: number;
  models_breakdown: Record<string, number>;
}

export default function DashboardPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [usageData, setUsageData] = useState<UsageData | null>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      const orgId = localStorage.getItem('current_org_id');
      
      if (!orgId) {
        toast.error('Please select an organization');
        return;
      }

      const usage = await aiApi.getUsage(parseInt(orgId));
      setUsageData(usage);
    } catch (error: any) {
      console.error('Failed to load dashboard data:', error);
      // Don't show error toast for 402 (no subscription) - it's expected for new users
      if (error.response?.status !== 402) {
        toast.error('Failed to load dashboard data');
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 lg:p-8">
        <DashboardSkeleton />
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8 space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-white/60">Welcome back! Here's your overview</p>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard
          title="Total Messages"
          value={usageData?.total_messages.toString() || "0"}
          icon={MessageSquare}
          trend={{ value: 0, isPositive: true }}
          delay={0.1}
        />
        <StatsCard
          title="Usage This Month"
          value={`${usageData?.usage_percentage.toFixed(0) || 0}%`}
          icon={TrendingUp}
          trend={{ value: 0, isPositive: true }}
          delay={0.2}
        />
        <StatsCard
          title="Messages Limit"
          value={usageData?.messages_limit ? usageData.messages_limit.toString() : "Unlimited"}
          icon={Zap}
          trend={{ value: 0, isPositive: true }}
          delay={0.3}
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Usage Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          whileHover={{ y: -4, transition: { duration: 0.2 } }}
          className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all duration-300"
        >
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-1">Usage</h3>
            <p className="text-sm text-white/60">Monthly message quota</p>
          </div>
          <div className="h-64">
            <UsageChart 
              used={usageData?.total_messages || 0} 
              limit={usageData?.messages_limit || 1000} 
            />
          </div>
        </motion.div>

        {/* Activity Chart */}
        <ActivityChart />
      </div>

      {/* Recent Chats */}
      <RecentChats />

      {/* Floating New Chat Button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.8, type: "spring", stiffness: 260, damping: 20 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => router.push('/chat')}
        className="fixed bottom-8 right-8 w-16 h-16 bg-white text-black rounded-full shadow-2xl flex items-center justify-center hover:shadow-white/20 transition-all duration-300 z-50"
        style={{
          animation: "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        }}
      >
        <Plus className="w-6 h-6" />
      </motion.button>

      <style dangerouslySetInnerHTML={{
        __html: `
          @keyframes pulse {
            0%, 100% {
              box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.4);
            }
            50% {
              box-shadow: 0 0 0 20px rgba(255, 255, 255, 0);
            }
          }
        `
      }} />
    </div>
  );
}
