"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/store/auth";
import { Sidebar } from "@/components/dashboard/sidebar";
import { OrganizationSwitcher } from "@/components/organization-switcher";
import { motion } from "framer-motion";
import { LogOut, User } from "lucide-react";
import { toast } from "sonner";

export default function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { isAuthenticated, isLoading, user, logout, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
    router.push("/login");
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-white border-t-transparent" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <motion.header
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="h-16 border-b border-white/10 bg-black/20 backdrop-blur-xl flex items-center justify-between px-6 z-30"
        >
          <div className="flex items-center gap-4">
            <div className="lg:hidden text-xl font-bold">AI SaaS</div>
          </div>
          
          <div className="flex items-center gap-4">
            <OrganizationSwitcher />
            
            <div className="flex items-center gap-3 px-3 py-2 rounded-lg border border-white/10 bg-white/5">
              <User className="w-4 h-4 text-white/60" />
              <span className="text-sm text-white/80">{user?.email}</span>
            </div>

            <button
              onClick={handleLogout}
              className="p-2 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 transition-all duration-300"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </motion.header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
