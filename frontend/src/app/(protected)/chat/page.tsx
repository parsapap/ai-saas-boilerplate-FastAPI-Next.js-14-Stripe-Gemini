"use client";

import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { api } from "@/lib/api";
import { toast } from "sonner";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function NewChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSendMessage = useCallback(async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Create AI message placeholder
      const aiMessageId = `ai-${Date.now()}`;
      const aiMessage: ChatMessage = {
        id: aiMessageId,
        role: "assistant",
        content: "",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
      setIsLoading(false);
      setIsStreaming(true);

      // Get current organization ID
      const orgId = localStorage.getItem("current_org_id");
      if (!orgId) {
        throw new Error("Please select an organization first");
      }

      // Get fresh token
      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Please login again");
      }

      // Call AI API with streaming
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/ai/chat/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "X-Current-Org": orgId,
        },
        body: JSON.stringify({
          messages: [
            {
              role: "user",
              content: content,
            },
          ],
          model: "gemini-2.0-flash",
          stream: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("Chat API error:", response.status, errorData);
        console.error("Request details:", {
          url: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/ai/chat/stream`,
          orgId,
          hasToken: !!token
        });
        
        // Handle 401 - redirect to login
        if (response.status === 401) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
          throw new Error("Session expired. Please login again.");
        }
        
        // Handle 402 - no subscription
        if (response.status === 402) {
          throw new Error("No active subscription. Please upgrade your plan or contact support.");
        }
        
        // Handle 403 - not a member
        if (response.status === 403) {
          throw new Error("You are not a member of this organization. Please select a different organization.");
        }
        
        // Handle different error formats
        let errorMessage = `Server error: ${response.status}`;
        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            // Validation errors
            errorMessage = errorData.detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ');
          } else if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else {
            errorMessage = JSON.stringify(errorData.detail);
          }
        }
        
        throw new Error(errorMessage);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("No reader available");
      }

      console.log("Starting to read stream...");
      let accumulatedContent = "";
      let buffer = "";
      let chunkCount = 0;

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          console.log("Stream reading done");
          break;
        }

        const decoded = decoder.decode(value, { stream: true });
        console.log("Raw chunk received:", decoded);
        buffer += decoded;
        const lines = buffer.split("\n");
        
        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || "";

        for (const line of lines) {
          console.log("Processing line:", line);
          if (line.startsWith("data: ")) {
            const data = line.slice(6);  // Don't trim - preserve spaces
            if (data.trim() === "[DONE]") {
              console.log("Received [DONE] signal");
              continue;
            }
            if (!data) {
              console.log("Empty data, skipping");
              continue;
            }

            chunkCount++;
            console.log(`Chunk #${chunkCount}:`, data);
            
            // Backend sends plain text chunks directly
            accumulatedContent += data;

            // Update message with accumulated content
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === aiMessageId
                  ? { ...msg, content: accumulatedContent }
                  : msg
              )
            );
          }
        }
      }

      console.log(`Stream complete. Received ${chunkCount} chunks. Total content length: ${accumulatedContent.length}`);
      console.log("Final content:", accumulatedContent);
      setIsStreaming(false);
    } catch (error: any) {
      console.error("Chat error:", error);
      toast.error(error.message || "Failed to send message");
      setIsLoading(false);
      setIsStreaming(false);

      // Remove the empty AI message on error
      setMessages((prev) => prev.filter((msg) => msg.content !== ""));
    }
  }, []);

  const handleRegenerate = useCallback(
    (messageId: string) => {
      const messageIndex = messages.findIndex((m) => m.id === messageId);
      if (messageIndex > 0) {
        const previousUserMessage = messages[messageIndex - 1];
        if (previousUserMessage.role === "user") {
          // Remove the AI message and regenerate
          setMessages((prev) => prev.slice(0, messageIndex));
          handleSendMessage(previousUserMessage.content);
        }
      }
    },
    [messages, handleSendMessage]
  );

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-[calc(100vh-4rem)]"
    >
      {/* Chat Header */}
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="flex-shrink-0 border-b border-white/10 bg-black/20 backdrop-blur-xl px-6 py-4"
      >
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold">New Chat</h1>
            <p className="text-sm text-white/60">
              {messages.length > 0
                ? `${messages.length} message${messages.length !== 1 ? "s" : ""}`
                : "Start a conversation"}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Chat Messages */}
      <ChatContainer
        messages={messages}
        isLoading={isLoading}
        isStreaming={isStreaming}
        onRegenerate={handleRegenerate}
      />

      {/* Chat Input */}
      <ChatInput
        onSend={handleSendMessage}
        disabled={isLoading || isStreaming}
        isLoading={isLoading}
      />
    </motion.div>
  );
}
