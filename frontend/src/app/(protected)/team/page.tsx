"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { UserPlus, Mail, Shield, Trash2, Crown, User as UserIcon } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { DashboardSkeleton } from "@/components/dashboard/skeleton";

interface TeamMember {
  id: string;
  user_id: string;
  email: string;
  full_name: string;
  role: "owner" | "admin" | "member";
  is_active: boolean;
  joined_at: string;
}

const roleIcons = {
  owner: Crown,
  admin: Shield,
  member: UserIcon,
};

const roleColors = {
  owner: "text-yellow-400",
  admin: "text-blue-400",
  member: "text-white/60",
};

export default function TeamPage() {
  const [members, setMembers] = useState<TeamMember[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isInviting, setIsInviting] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState<"admin" | "member">("member");

  useEffect(() => {
    loadMembers();
  }, []);

  const loadMembers = async () => {
    try {
      const response = await api.get("/api/v1/orgs/1/members", {
        headers: { "X-Current-Org": "1" },
      });
      setMembers(response.data);
    } catch (error) {
      toast.error("Failed to load team members");
    } finally {
      setIsLoading(false);
    }
  };

  const inviteMember = async () => {
    if (!inviteEmail.trim()) {
      toast.error("Please enter an email address");
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(inviteEmail)) {
      toast.error("Please enter a valid email address");
      return;
    }

    setIsInviting(true);
    try {
      await api.post(
        "/api/v1/orgs/1/invite",
        {
          email: inviteEmail,
          role: inviteRole,
        },
        {
          headers: { "X-Current-Org": "1" },
        }
      );
      setInviteEmail("");
      await loadMembers();
      toast.success(`Invitation sent to ${inviteEmail}`);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to invite member");
    } finally {
      setIsInviting(false);
    }
  };

  const updateRole = async (memberId: string, newRole: "admin" | "member") => {
    try {
      await api.patch(
        `/api/v1/orgs/1/members/${memberId}`,
        { role: newRole },
        {
          headers: { "X-Current-Org": "1" },
        }
      );
      await loadMembers();
      toast.success("Role updated successfully");
    } catch (error) {
      toast.error("Failed to update role");
    }
  };

  const removeMember = async (memberId: string, memberName: string) => {
    if (!confirm(`Are you sure you want to remove ${memberName} from the team?`)) {
      return;
    }

    try {
      await api.delete(`/api/v1/orgs/1/members/${memberId}`, {
        headers: { "X-Current-Org": "1" },
      });
      await loadMembers();
      toast.success("Member removed from team");
    } catch (error) {
      toast.error("Failed to remove member");
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
      >
        <h1 className="text-4xl font-bold mb-2">Team</h1>
        <p className="text-white/60">
          Manage your team members and their roles
        </p>
      </motion.div>

      {/* Invite Member */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
      >
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <UserPlus className="w-5 h-5" />
          Invite Team Member
        </h2>
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="flex-1 flex gap-3">
            <input
              type="email"
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              placeholder="colleague@company.com"
              className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors"
              onKeyDown={(e) => e.key === "Enter" && inviteMember()}
            />
            <select
              value={inviteRole}
              onChange={(e) => setInviteRole(e.target.value as "admin" | "member")}
              className="px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors"
            >
              <option value="member">Member</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={inviteMember}
            disabled={isInviting}
            className="px-6 py-3 bg-white text-black rounded-lg font-medium hover:bg-white/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <Mail className="w-5 h-5" />
            {isInviting ? "Sending..." : "Send Invite"}
          </motion.button>
        </div>
        <p className="text-sm text-white/40 mt-3">
          Invited members will receive an email with instructions to join your team.
        </p>
      </motion.div>

      {/* Team Members */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">
          Team Members ({members.length})
        </h2>
        {members.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-12 text-center rounded-xl bg-white/5 border border-white/10"
          >
            <UserIcon className="w-12 h-12 mx-auto mb-4 text-white/40" />
            <p className="text-white/60">No team members yet. Invite someone to get started.</p>
          </motion.div>
        ) : (
          members.map((member, index) => {
            const RoleIcon = roleIcons[member.role];
            const roleColor = roleColors[member.role];

            return (
              <motion.div
                key={member.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 + index * 0.05 }}
                className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center">
                      <span className="text-lg font-semibold">
                        {member.full_name?.charAt(0)?.toUpperCase() || member.email?.charAt(0)?.toUpperCase() || "?"}
                      </span>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold">{member.full_name || "Pending"}</h3>
                      <p className="text-sm text-white/60">{member.email || "No email"}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <RoleIcon className={`w-4 h-4 ${roleColor}`} />
                        <span className={`text-sm capitalize ${roleColor}`}>
                          {member.role}
                        </span>
                        {!member.is_active && (
                          <span className="text-xs px-2 py-0.5 bg-yellow-500/20 text-yellow-400 rounded">
                            Pending
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {member.role !== "owner" && (
                      <>
                        <select
                          value={member.role}
                          onChange={(e) => updateRole(member.id, e.target.value as "admin" | "member")}
                          className="px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm focus:outline-none focus:border-white/30 transition-colors"
                        >
                          <option value="member">Member</option>
                          <option value="admin">Admin</option>
                        </select>
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => removeMember(member.id, member.full_name || member.email)}
                          className="p-2 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors"
                          title="Remove member"
                        >
                          <Trash2 className="w-5 h-5" />
                        </motion.button>
                      </>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })
        )}
      </div>

      {/* Role Descriptions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="p-6 rounded-xl bg-white/5 border border-white/10"
      >
        <h3 className="text-lg font-semibold mb-4">Role Permissions</h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <Crown className="w-5 h-5 text-yellow-400 mt-0.5" />
            <div>
              <p className="font-medium">Owner</p>
              <p className="text-sm text-white/60">
                Full access to all features, billing, and team management. Can delete the organization.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <Shield className="w-5 h-5 text-blue-400 mt-0.5" />
            <div>
              <p className="font-medium">Admin</p>
              <p className="text-sm text-white/60">
                Can manage team members, API keys, and organization settings. Cannot access billing.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <UserIcon className="w-5 h-5 text-white/60 mt-0.5" />
            <div>
              <p className="font-medium">Member</p>
              <p className="text-sm text-white/60">
                Can use the platform and access shared resources. Cannot manage team or settings.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
