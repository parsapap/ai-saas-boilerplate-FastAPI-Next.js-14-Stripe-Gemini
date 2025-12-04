"use client";

import { motion } from "framer-motion";
import { Copy, ThumbsUp, ThumbsDown, RefreshCw, Check } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

interface MessageProps {
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  onRegenerate?: () => void;
  onCopy?: () => void;
  onLike?: () => void;
  onDislike?: () => void;
}

export function Message({
  role,
  content,
  isStreaming = false,
  onRegenerate,
  onCopy,
  onLike,
  onDislike,
}: MessageProps) {
  const [copied, setCopied] = useState(false);
  const [liked, setLiked] = useState<boolean | null>(null);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    onCopy?.();
    setTimeout(() => setCopied(false), 2000);
  };

  const handleLike = () => {
    setLiked(liked === true ? null : true);
    onLike?.();
  };

  const handleDislike = () => {
    setLiked(liked === false ? null : false);
    onDislike?.();
  };

  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-6`}
    >
      <div className={`flex gap-4 max-w-[80%] ${isUser ? "flex-row-reverse" : "flex-row"}`}>
        {/* Avatar */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
            isUser
              ? "bg-white text-black"
              : "bg-white/10 text-white border border-white/20"
          }`}
        >
          {isUser ? "U" : "AI"}
        </motion.div>

        {/* Message Content */}
        <div className="flex-1 min-w-0">
          <motion.div
            initial={{ scale: 0.95 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.2 }}
            className={`rounded-2xl px-4 py-3 ${
              isUser
                ? "bg-white text-black"
                : "bg-white/5 backdrop-blur-xl border border-white/10"
            }`}
          >
            {isUser ? (
              <p className="text-sm whitespace-pre-wrap break-words">{content}</p>
            ) : (
              <div className="prose prose-invert prose-sm max-w-none">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || "");
                      return !inline && match ? (
                        <SyntaxHighlighter
                          style={vscDarkPlus}
                          language={match[1]}
                          PreTag="div"
                          className="rounded-lg !bg-black/50 !mt-2 !mb-2"
                          {...props}
                        >
                          {String(children).replace(/\n$/, "")}
                        </SyntaxHighlighter>
                      ) : (
                        <code
                          className="bg-white/10 px-1.5 py-0.5 rounded text-sm"
                          {...props}
                        >
                          {children}
                        </code>
                      );
                    },
                    p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
                    li: ({ children }) => <li className="mb-1">{children}</li>,
                    h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-bold mb-2">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-base font-bold mb-2">{children}</h3>,
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-2 border-white/20 pl-4 italic my-2">
                        {children}
                      </blockquote>
                    ),
                    table: ({ children }) => (
                      <div className="overflow-x-auto my-2">
                        <table className="min-w-full border border-white/10">{children}</table>
                      </div>
                    ),
                    th: ({ children }) => (
                      <th className="border border-white/10 px-3 py-2 bg-white/5">{children}</th>
                    ),
                    td: ({ children }) => (
                      <td className="border border-white/10 px-3 py-2">{children}</td>
                    ),
                  }}
                >
                  {content}
                </ReactMarkdown>
              </div>
            )}
          </motion.div>

          {/* Actions (only for AI messages) */}
          {!isUser && !isStreaming && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex items-center gap-2 mt-2 ml-1"
            >
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleCopy}
                className="p-1.5 rounded-lg hover:bg-white/10 transition-colors duration-200"
                title="Copy"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-green-400" />
                ) : (
                  <Copy className="w-4 h-4 text-white/60" />
                )}
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleLike}
                className={`p-1.5 rounded-lg hover:bg-white/10 transition-colors duration-200 ${
                  liked === true ? "text-green-400" : "text-white/60"
                }`}
                title="Like"
              >
                <ThumbsUp className="w-4 h-4" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleDislike}
                className={`p-1.5 rounded-lg hover:bg-white/10 transition-colors duration-200 ${
                  liked === false ? "text-red-400" : "text-white/60"
                }`}
                title="Dislike"
              >
                <ThumbsDown className="w-4 h-4" />
              </motion.button>

              {onRegenerate && (
                <motion.button
                  whileHover={{ scale: 1.1, rotate: 180 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={onRegenerate}
                  className="p-1.5 rounded-lg hover:bg-white/10 transition-colors duration-200"
                  title="Regenerate"
                >
                  <RefreshCw className="w-4 h-4 text-white/60" />
                </motion.button>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
