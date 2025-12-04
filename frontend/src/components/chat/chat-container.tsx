"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Message } from "./message";
import { TypingIndicator } from "./typing-indicator";
import { Sparkles } from "lucide-react";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ChatContainerProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  isStreaming?: boolean;
  onRegenerate?: (messageId: string) => void;
}

export function ChatContainer({
  messages,
  isLoading = false,
  isStreaming = false,
  onRegenerate,
}: ChatContainerProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom with smooth animation
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  // Empty state
  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-center max-w-2xl"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-block p-6 rounded-full bg-white/5 border border-white/10 mb-6"
          >
            <Sparkles className="w-12 h-12" />
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-3xl font-bold mb-4"
          >
            Start a conversation
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-white/60 mb-8"
          >
            Ask me anything. I'm here to help with coding, writing, analysis, and more.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-4"
          >
            {[
              "Explain quantum computing",
              "Write a Python function",
              "Help me debug this code",
              "Summarize this article",
            ].map((suggestion, index) => (
              <motion.button
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 + index * 0.1 }}
                whileHover={{ scale: 1.02, y: -2 }}
                whileTap={{ scale: 0.98 }}
                className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-white/20 hover:bg-white/10 transition-all duration-200 text-left"
              >
                <p className="text-sm text-white/80">{suggestion}</p>
              </motion.button>
            ))}
          </motion.div>
        </motion.div>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 py-8 scroll-smooth"
      style={{
        scrollbarWidth: "thin",
        scrollbarColor: "rgba(255, 255, 255, 0.2) transparent",
      }}
    >
      <div className="max-w-4xl mx-auto">
        <AnimatePresence mode="popLayout">
          {messages.map((message) => (
            <Message
              key={message.id}
              role={message.role}
              content={message.content}
              isStreaming={isStreaming && message.id === messages[messages.length - 1]?.id}
              onRegenerate={
                message.role === "assistant"
                  ? () => onRegenerate?.(message.id)
                  : undefined
              }
            />
          ))}

          {isLoading && <TypingIndicator key="typing" />}
        </AnimatePresence>

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
