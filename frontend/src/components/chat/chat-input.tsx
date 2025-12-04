"use client";

import { motion } from "framer-motion";
import { Send, Loader2 } from "lucide-react";
import { useState, useRef, useEffect, KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  isLoading?: boolean;
}

export function ChatInput({ onSend, disabled = false, isLoading = false }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    if (message.trim() && !disabled && !isLoading) {
      onSend(message.trim());
      setMessage("");
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = "auto";
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [message]);

  const canSend = message.trim().length > 0 && !disabled && !isLoading;

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky bottom-0 left-0 right-0 bg-black/50 backdrop-blur-xl border-t border-white/10 p-4"
    >
      <div className="max-w-4xl mx-auto">
        <div className="relative flex items-end gap-3">
          {/* Textarea */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message... (Shift+Enter for new line)"
              disabled={disabled || isLoading}
              rows={1}
              className="w-full px-4 py-3 pr-12 bg-white/5 border border-white/10 rounded-2xl resize-none focus:outline-none focus:border-white/30 transition-all duration-200 placeholder:text-white/40 disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ maxHeight: "200px" }}
            />
            
            {/* Character count (optional) */}
            {message.length > 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="absolute bottom-2 right-2 text-xs text-white/40"
              >
                {message.length}
              </motion.div>
            )}
          </div>

          {/* Send Button */}
          <motion.button
            whileHover={canSend ? { scale: 1.05 } : {}}
            whileTap={canSend ? { scale: 0.95 } : {}}
            onClick={handleSend}
            disabled={!canSend}
            className={`flex-shrink-0 p-3 rounded-xl transition-all duration-200 ${
              canSend
                ? "bg-white text-black hover:bg-white/90"
                : "bg-white/10 text-white/40 cursor-not-allowed"
            }`}
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </motion.button>
        </div>

        {/* Helper Text */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-xs text-white/40 mt-2 text-center"
        >
          Press Enter to send, Shift+Enter for new line
        </motion.p>
      </div>
    </motion.div>
  );
}
