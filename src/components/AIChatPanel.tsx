import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Sparkles, BarChart3, AlertCircle, Search, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  type?: "text" | "chart" | "alert";
  timestamp: Date;
  loading?: boolean;
}

const suggestions = [
  { icon: Search, text: "Why are 5xx errors rising?" },
  { icon: AlertCircle, text: "Alert me when error rate > 5%" },
  { icon: BarChart3, text: "Show latency vs time chart" },
  { icon: Sparkles, text: "Analyze auth-service anomalies" },
];

interface AIChatPanelProps {
  onQuerySent?: (query: string) => void;
}

export function AIChatPanel({ onQuerySent }: AIChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const query = input.trim();
    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    onQuerySent?.(query);
    setInput("");
    setIsLoading(true);

    // Add loading placeholder
    const loadingId = (Date.now() + 1).toString();
    setMessages((prev) => [
      ...prev,
      { id: loadingId, role: "assistant", content: "", timestamp: new Date(), loading: true },
    ]);

    try {
      const res = await api.agentChat(query);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { ...m, content: res.output, loading: false }
            : m
        )
      );
    } catch (err) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === loadingId
            ? { ...m, content: `⚠️ Failed to reach backend. Make sure your server is running at \`http://127.0.0.1:8000\`.\n\nError: ${err instanceof Error ? err.message : "Unknown error"}`, loading: false }
            : m
        )
      );
      toast({ title: "Connection Error", description: "Could not reach the backend server.", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full gap-6 text-center">
            <div className="w-16 h-16 rounded-2xl gradient-primary flex items-center justify-center">
              <Sparkles className="w-8 h-8 text-primary-foreground" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-2">LogSense AI Copilot</h2>
              <p className="text-muted-foreground text-sm max-w-md">
                Ask me anything about your logs, create alerts, or generate dashboards using natural language.
              </p>
            </div>
          </div>
        )}

        <AnimatePresence>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={cn(
                "flex gap-3",
                msg.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              {msg.role === "assistant" && (
                <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center flex-shrink-0 mt-1">
                  <Sparkles className="w-3.5 h-3.5 text-primary-foreground" />
                </div>
              )}
              <div
                className={cn(
                  "max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed",
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "glass-panel"
                )}
              >
                {msg.loading ? (
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Thinking...</span>
                  </div>
                ) : msg.role === "assistant" ? (
                  <div className="prose prose-sm prose-invert max-w-none [&_h2]:text-foreground [&_h3]:text-foreground [&_strong]:text-foreground [&_code]:text-primary [&_code]:bg-primary/10 [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_li]:text-secondary-foreground [&_p]:text-secondary-foreground">
                    <div dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }} />
                  </div>
                ) : (
                  msg.content
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Suggestions */}
      {messages.length === 0 && (
        <div className="px-4 pb-2 flex gap-2 flex-wrap">
          {suggestions.map((s) => (
            <button
              key={s.text}
              onClick={() => setInput(s.text)}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-secondary/60 border border-border/30 text-xs text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all"
            >
              <s.icon className="w-3.5 h-3.5" />
              {s.text}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-border/50">
        <div className="flex items-center gap-2 glass-panel p-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask about your logs, create alerts, generate dashboards..."
            className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none px-2"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className={cn(
              "p-2 rounded-lg transition-all",
              input.trim() && !isLoading
                ? "gradient-primary text-primary-foreground"
                : "bg-secondary text-muted-foreground"
            )}
          >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  );
}

function formatMarkdown(text: string): string {
  return text
    .replace(/### (.*)/g, '<h3>$1</h3>')
    .replace(/## (.*)/g, '<h2>$1</h2>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^- (.*)/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>')
    .replace(/^(.*)$/, '<p>$1</p>');
}
