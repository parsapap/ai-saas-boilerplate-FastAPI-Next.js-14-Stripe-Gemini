"use client";

import { motion } from "framer-motion";
import { MessageSquare, Clock } from "lucide-react";

interface Chat {
  id: string;
  title: string;
  preview: string;
  timestamp: string;
}

const mockChats: Chat[] = [
  {
    id: "1",
    title: "Product Strategy Discussion",
    preview: "Let's analyze the market trends for Q4...",
    timestamp: "2 hours ago",
  },
  {
    id: "2",
    title: "Code Review Assistant",
    preview: "Can you help me review this React component?",
    timestamp: "5 hours ago",
  },
  {
    id: "3",
    title: "Marketing Campaign Ideas",
    preview: "I need creative ideas for our new product launch...",
    timestamp: "1 day ago",
  },
  {
    id: "4",
    title: "Technical Documentation",
    preview: "Help me write API documentation for...",
    timestamp: "2 days ago",
  },
];

export function RecentChats() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.5 }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="p-6 rounded-xl bg-white/5 backdrop-blur-xl border border-white/10 hover:border-white/20 transition-all duration-300"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold mb-1">Recent Chats</h3>
          <p className="text-sm text-white/60">Your latest conversations</p>
        </div>
        <button className="text-sm text-white/60 hover:text-white transition-colors duration-200">
          View all
        </button>
      </div>

      <div className="space-y-3">
        {mockChats.map((chat, index) => (
          <motion.div
            key={chat.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 + index * 0.1 }}
            whileHover={{ x: 4, transition: { duration: 0.2 } }}
            className="p-4 rounded-lg bg-white/5 hover:bg-white/10 border border-white/5 hover:border-white/20 transition-all duration-300 cursor-pointer group"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-white/10 group-hover:bg-white/20 transition-colors duration-300">
                <MessageSquare className="w-4 h-4" />
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium mb-1 truncate">
                  {chat.title}
                </h4>
                <p className="text-xs text-white/60 mb-2 truncate">
                  {chat.preview}
                </p>
                <div className="flex items-center gap-1 text-xs text-white/40">
                  <Clock className="w-3 h-3" />
                  <span>{chat.timestamp}</span>
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
