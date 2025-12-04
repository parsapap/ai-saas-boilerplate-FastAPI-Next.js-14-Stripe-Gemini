"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Key, Copy, Trash2, Plus, Eye, EyeOff, Check } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { DashboardSkeleton } from "@/components/dashboard/skeleton";

interface ApiKey {
  id: string;
  name: string;
  key: string;
  prefix: string;
  created_at: string;
  last_used_at?: string;
}

export default function ApiKeysPage() {
  const [keys, setKeys] = useState<ApiKey[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [showNewKey, setShowNewKey] = useState<string | null>(null);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [revealedKeys, setRevealedKeys] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    try {
      const response = await api.get("/api/v1/apikeys", {
        headers: { "X-Current-Org": "1" },
      });
      setKeys(response.data);
    } catch (error) {
      toast.error("Failed to load API keys");
    } finally {
      setIsLoading(false);
    }
  };

  const createKey = async () => {
    if (!newKeyName.trim()) {
      toast.error("Please enter a key name");
      return;
    }

    setIsCreating(true);
    try {
      const response = await api.post(
        "/api/v1/apikeys",
        {
          name: newKeyName,
        },
        {
          headers: { "X-Current-Org": "1" },
        }
      );
      setShowNewKey(response.data.key);
      setNewKeyName("");
      await loadKeys();
      toast.success("API key created successfully");
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to create API key");
    } finally {
      setIsCreating(false);
    }
  };

  const revokeKey = async (keyId: string) => {
    if (!confirm("Are you sure you want to revoke this API key? This action cannot be undone.")) {
      return;
    }

    try {
      await api.delete(`/api/v1/apikeys/${keyId}`, {
        headers: { "X-Current-Org": "1" },
      });
      setKeys(keys.filter((k) => k.id !== keyId));
      toast.success("API key revoked");
    } catch (error) {
      toast.error("Failed to revoke API key");
    }
  };

  const copyKey = (key: string) => {
    navigator.clipboard.writeText(key);
    setCopiedKey(key);
    toast.success("API key copied to clipboard");
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const toggleReveal = (keyId: string) => {
    const newRevealed = new Set(revealedKeys);
    if (newRevealed.has(keyId)) {
      newRevealed.delete(keyId);
    } else {
      newRevealed.add(keyId);
    }
    setRevealedKeys(newRevealed);
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
        <h1 className="text-4xl font-bold mb-2">API Keys</h1>
        <p className="text-white/60">
          Manage your API keys for programmatic access
        </p>
      </motion.div>

      {/* New Key Alert */}
      {showNewKey && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-6 rounded-xl bg-green-500/10 border border-green-500/20"
        >
          <h3 className="text-lg font-semibold mb-2 text-green-400">
            API Key Created Successfully
          </h3>
          <p className="text-sm text-white/60 mb-4">
            Make sure to copy your API key now. You won't be able to see it again!
          </p>
          <div className="flex items-center gap-2">
            <code className="flex-1 px-4 py-3 bg-black/50 rounded-lg font-mono text-sm break-all">
              {showNewKey}
            </code>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => copyKey(showNewKey)}
              className="p-3 bg-white text-black rounded-lg hover:bg-white/90 transition-colors"
            >
              {copiedKey === showNewKey ? (
                <Check className="w-5 h-5" />
              ) : (
                <Copy className="w-5 h-5" />
              )}
            </motion.button>
          </div>
          <button
            onClick={() => setShowNewKey(null)}
            className="mt-4 text-sm text-white/60 hover:text-white transition-colors"
          >
            I've saved my key
          </button>
        </motion.div>
      )}

      {/* Create New Key */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10"
      >
        <h2 className="text-xl font-semibold mb-4">Create New API Key</h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={newKeyName}
            onChange={(e) => setNewKeyName(e.target.value)}
            placeholder="Key name (e.g., Production API)"
            className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-white/30 transition-colors"
            onKeyDown={(e) => e.key === "Enter" && createKey()}
          />
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={createKey}
            disabled={isCreating}
            className="px-6 py-3 bg-white text-black rounded-lg font-medium hover:bg-white/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Plus className="w-5 h-5" />
            {isCreating ? "Creating..." : "Create Key"}
          </motion.button>
        </div>
      </motion.div>

      {/* Keys List */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Your API Keys</h2>
        {keys.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-12 text-center rounded-xl bg-white/5 border border-white/10"
          >
            <Key className="w-12 h-12 mx-auto mb-4 text-white/40" />
            <p className="text-white/60">No API keys yet. Create one to get started.</p>
          </motion.div>
        ) : (
          keys.map((key, index) => (
            <motion.div
              key={key.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.05 }}
              className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold mb-1">{key.name}</h3>
                  <p className="text-sm text-white/60">
                    Created {new Date(key.created_at).toLocaleDateString()}
                    {key.last_used_at && (
                      <> · Last used {new Date(key.last_used_at).toLocaleDateString()}</>
                    )}
                  </p>
                </div>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => revokeKey(key.id)}
                  className="p-2 rounded-lg hover:bg-red-500/10 text-red-400 transition-colors"
                  title="Revoke key"
                >
                  <Trash2 className="w-5 h-5" />
                </motion.button>
              </div>

              <div className="flex items-center gap-2">
                <code className="flex-1 px-4 py-3 bg-black/50 rounded-lg font-mono text-sm">
                  {revealedKeys.has(key.id)
                    ? key.key || `${key.prefix}••••••••••••••••`
                    : `${key.prefix}••••••••••••••••`}
                </code>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => toggleReveal(key.id)}
                  className="p-3 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
                  title={revealedKeys.has(key.id) ? "Hide" : "Reveal"}
                >
                  {revealedKeys.has(key.id) ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => copyKey(key.key || `${key.prefix}••••••••••••••••`)}
                  className="p-3 bg-white/10 rounded-lg hover:bg-white/20 transition-colors"
                  title="Copy"
                >
                  {copiedKey === key.key ? (
                    <Check className="w-5 h-5 text-green-400" />
                  ) : (
                    <Copy className="w-5 h-5" />
                  )}
                </motion.button>
              </div>
            </motion.div>
          ))
        )}
      </div>

      {/* Usage Example */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="p-6 rounded-xl bg-white/5 border border-white/10"
      >
        <h3 className="text-lg font-semibold mb-4">Usage Example</h3>
        <pre className="p-4 bg-black/50 rounded-lg overflow-x-auto">
          <code className="text-sm font-mono text-white/80">
{`curl -X POST https://api.yourdomain.com/v1/ai/chat \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Hello, AI!",
    "model": "gemini"
  }'`}
          </code>
        </pre>
      </motion.div>
    </div>
  );
}
