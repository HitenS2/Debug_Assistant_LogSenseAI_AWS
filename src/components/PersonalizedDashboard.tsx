import { useState } from "react";
import { motion } from "framer-motion";
import { Send, Loader2, BarChart3, Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

interface ChatEntry {
  role: "user" | "assistant";
  content: string;
}

const suggestions = [
  "Generate a pie chart for error classification",
  "Show a bar chart of requests per service",
  "Create a line chart of latency over time",
  "Generate a chart for top failing endpoints",
];

export function PersonalizedDashboard() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<ChatEntry[]>([]);

  const handleSubmit = async (query?: string) => {
    const text = query || input.trim();
    if (!text || loading) return;

    setInput("");
    setHistory((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);

    try {
      const res = await api.graphAgentChat(text);
      setHistory((prev) => [...prev, { role: "assistant", content: res.output }]);
    } catch {
      setHistory((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Failed to reach the backend. Please ensure the server is running." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-border/50">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
            <BarChart3 className="w-4 h-4 text-primary-foreground" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-foreground">Personalized Dashboard</h2>
            <p className="text-xs text-muted-foreground">Generate custom charts and visualizations with AI</p>
          </div>
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-4">
        {history.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col items-center justify-center h-full gap-6"
          >
            <div className="w-16 h-16 rounded-2xl gradient-primary flex items-center justify-center">
              <Sparkles className="w-8 h-8 text-primary-foreground" />
            </div>
            <div className="text-center">
              <h3 className="text-lg font-semibold text-foreground mb-1">What would you like to visualize?</h3>
              <p className="text-sm text-muted-foreground">Describe a chart or dashboard and AI will generate it for you.</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg w-full">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => handleSubmit(s)}
                  className="glass-panel px-4 py-3 text-left text-sm text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all"
                >
                  {s}
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {history.map((entry, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn(
              "max-w-3xl",
              entry.role === "user" ? "ml-auto" : "mr-auto"
            )}
          >
            <div
              className={cn(
                "rounded-xl px-4 py-3",
                entry.role === "user"
                  ? "gradient-primary text-primary-foreground"
                  : "glass-panel"
              )}
            >
              {entry.role === "assistant" ? (
                <div className="prose prose-invert prose-sm max-w-none [&_img]:rounded-xl [&_img]:border [&_img]:border-border/30 [&_img]:mt-3 [&_img]:max-w-full">
                  <ReactMarkdown>{entry.content}</ReactMarkdown>
                </div>
              ) : (
                <p className="text-sm">{entry.content}</p>
              )}
            </div>
          </motion.div>
        ))}

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-muted-foreground text-sm"
          >
            <Loader2 className="w-4 h-4 animate-spin text-primary" />
            Generating visualization…
          </motion.div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 border-t border-border/50">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
          className="flex items-center gap-2 max-w-3xl mx-auto"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="e.g. Generate a pie chart for error classification…"
            className="flex-1 bg-secondary/60 border border-border/40 rounded-xl px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary/50"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="gradient-primary text-primary-foreground p-3 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
