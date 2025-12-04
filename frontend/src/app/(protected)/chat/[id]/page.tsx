"use client";

import { useState, useCallback, useEffect } from "react";
import { motion } from "framer-motion";
import { useParams, useRouter } from "next/navigation";
import { ChatContainer } from "@/components/chat/chat-container";
import { ChatInput } from "@/components/chat/chat-input";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { Loader2 } from "lucide-react";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const chatId = params.id as string;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isLoadingChat, setIsLoadingChat] = useState(true);
  const [chatTitle, setChatTitle] = useState("Chat");

  // Load existing chat
  useEffect(() => {
    const loadChat = async () => {
      try {
        const response = await api.get(`/api/v1/chats/${chatId}`);
        const chat = response.data;

        setChatTitle(chat.title || "Chat");
        setMessages(
          chat.messages?.map((msg: any) => ({
            id: msg.id,
            role: msg.role,
            content: msg.content,
            timestamp: new Date(msg.created_at),
          })) || []
        );
      } catch (error: any) {
        console.error("Failed to load chat:", error);
        toast.error("Failed to load chat");
        router.push("/chat");
      } finally {
        setIsLoadingChat(false);
      }
    };

    if (chatId) {
      loadChat();
    }
  }, [chatId, router]);

  const handleSendMessage = useCallback(
    async (content: string) => {
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
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/ai/chat/stream`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
              "X-Current-Org": orgId,
            },
            body: JSON.stringify({
              message: content,
              chat_id: chatId,
              model: "gemini-1.5-flash",
              stream: true,
            }),
          }
        );

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error("Chat API error:", response.status, errorData);
          
          // Handle 401 - redirect to login
          if (response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login";
            throw new Error("Session expired. Please login again.");
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

        let accumulatedContent = "";

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n");

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const data = line.slice(6);
              if (data === "[DONE]") {
                continue;
              }

              try {
                const parsed = JSON.parse(data);
                if (parsed.content) {
                  accumulatedContent += parsed.content;

                  setMessages((prev) =>
                    prev.map((msg) =>
                      msg.id === aiMessageId
                        ? { ...msg, content: accumulatedContent }
                        : msg
                    )
                  );
                }
              } catch (e) {
                // Skip invalid JSON
              }
            }
          }
        }

        setIsStreaming(false);
      } catch (error: any) {
        console.error("Chat error:", error);
        toast.error(error.message || "Failed to send message");
        setIsLoading(false);
        setIsStreaming(false);
        setMessages((prev) => prev.filter((msg) => msg.content !== ""));
      }
    },
    [chatId]
  );

  const handleRegenerate = useCallback(
    (messageId: string) => {
      const messageIndex = messages.findIndex((m) => m.id === messageId);
      if (messageIndex > 0) {
        const previousUserMessage = messages[messageIndex - 1];
        if (previousUserMessage.role === "user") {
          setMessages((prev) => prev.slice(0, messageIndex));
          handleSendMessage(previousUserMessage.content);
        }
      }
    },
    [messages, handleSendMessage]
  );

  if (isLoadingChat) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

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
            <h1 className="text-xl font-semibold">{chatTitle}</h1>
            <p className="text-sm text-white/60">
              {messages.length} message{messages.length !== 1 ? "s" : ""}
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
