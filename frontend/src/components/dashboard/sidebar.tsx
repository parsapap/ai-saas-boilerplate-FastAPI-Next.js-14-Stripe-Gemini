"use client";

import { useState, memo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  MessageSquare,
  Settings,
  CreditCard,
  Users,
  Menu,
  X,
  Key,
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSubscription } from "@/hooks/useSubscription";

const menuItems = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/dashboard" },
  { icon: MessageSquare, label: "Chat", href: "/chat" },
  { icon: Users, label: "Team", href: "/team" },
  { icon: CreditCard, label: "Billing", href: "/billing" },
  { icon: Key, label: "API Keys", href: "/api-keys" },
  { icon: Settings, label: "Settings", href: "/settings" },
];

function SidebarComponent() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const { subscription, currentPlan } = useSubscription();

  return (
    <>
      {/* Hamburger Menu Button - Visible on all screen sizes */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-[60] p-2 rounded-lg bg-black/80 backdrop-blur-xl border border-white/10 hover:bg-black/90 transition-colors"
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
            className="lg:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          />
        )}
      </AnimatePresence>

      {/* Sidebar - Toggleable on all screen sizes */}
      <motion.aside
        initial={false}
        animate={{
          x: isOpen ? 0 : "-100%",
        }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        className="fixed top-0 left-0 h-screen w-64 bg-black/40 backdrop-blur-xl border-r border-white/10 z-50 flex flex-col"
      >
        <div className="p-6">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-2xl font-bold"
          >
            AI SaaS
          </motion.div>
        </div>

        <nav className="flex-1 px-3 space-y-1">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <motion.div
                key={item.href}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Link
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                    isActive
                      ? "bg-white text-black"
                      : "text-white/60 hover:text-white hover:bg-white/5"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </motion.div>
            );
          })}
        </nav>

        <div className="p-4 border-t border-white/10">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="p-4 rounded-lg bg-white/5 border border-white/10"
          >
            <div className="flex items-center justify-between mb-1">
              <div className="text-sm font-medium">{currentPlan.name} Plan</div>
              {subscription?.status && (
                <div className="px-2 py-0.5 text-xs rounded bg-green-500/20 text-green-400 capitalize">
                  {subscription.status}
                </div>
              )}
            </div>
            <div className="text-xs text-white/60 mb-3">
              {currentPlan.limit}
            </div>
            {subscription?.plan_type?.toUpperCase() === "FREE" && (
              <Link
                href="/pricing"
                onClick={() => setIsOpen(false)}
                className="block w-full px-3 py-2 text-sm text-center bg-white text-black rounded-lg hover:bg-white/90 transition-colors duration-200"
              >
                Upgrade
              </Link>
            )}
            {subscription?.plan_type?.toUpperCase() !== "FREE" && (
              <Link
                href="/billing"
                onClick={() => setIsOpen(false)}
                className="block w-full px-3 py-2 text-sm text-center bg-white/10 text-white rounded-lg hover:bg-white/20 transition-colors duration-200"
              >
                Manage
              </Link>
            )}
          </motion.div>
        </div>
      </motion.aside>
    </>
  );
}

export const Sidebar = memo(SidebarComponent);
