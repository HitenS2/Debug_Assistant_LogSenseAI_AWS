import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Check, Loader2, Search, Database, Brain, BarChart3, LayoutDashboard, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

interface Step {
  id: number;
  label: string;
  icon: React.ElementType;
  status: "pending" | "active" | "done";
  detail?: string;
}

const defaultSteps: Step[] = [
  { id: 1, label: "Parsing user intent", icon: Brain, status: "done", detail: "Query: anomaly detection" },
  { id: 2, label: "Querying log indices", icon: Database, status: "done", detail: "Scanned 2.3M events" },
  { id: 3, label: "Running anomaly detection", icon: Search, status: "done", detail: "3 anomalies found" },
  { id: 4, label: "Aggregating metrics", icon: BarChart3, status: "active", detail: "Processing p95 latency..." },
  { id: 5, label: "Generating visualization", icon: LayoutDashboard, status: "pending" },
  { id: 6, label: "Creating dashboard widget", icon: Zap, status: "pending" },
];

export function AIThinkingPanel() {
  const [steps, setSteps] = useState<Step[]>(defaultSteps);

  // Simulate step progression
  useEffect(() => {
    const interval = setInterval(() => {
      setSteps((prev) => {
        const activeIdx = prev.findIndex((s) => s.status === "active");
        if (activeIdx === -1 || activeIdx >= prev.length - 1) {
          // Reset cycle
          return defaultSteps;
        }
        return prev.map((s, i) => {
          if (i === activeIdx) return { ...s, status: "done" as const };
          if (i === activeIdx + 1) return { ...s, status: "active" as const, detail: getDetail(s.id) };
          return s;
        });
      });
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full flex flex-col">
      <div className="px-4 py-3 border-b border-border/50">
        <h3 className="text-sm font-semibold text-foreground flex items-center gap-2">
          <Brain className="w-4 h-4 text-primary" />
          Agent Pipeline
        </h3>
        <p className="text-xs text-muted-foreground mt-0.5">Real-time processing steps</p>
      </div>

      <div className="flex-1 p-4 overflow-y-auto scrollbar-thin">
        <div className="space-y-0">
          {steps.map((step, idx) => (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1, duration: 0.3 }}
              className="flex gap-3 relative"
            >
              {/* Line */}
              {idx < steps.length - 1 && (
                <div className="absolute left-[15px] top-8 w-[2px] h-[calc(100%-8px)]">
                  <div
                    className={cn(
                      "w-full h-full rounded-full transition-colors duration-500",
                      step.status === "done" ? "bg-primary/40" : "bg-border/40"
                    )}
                  />
                </div>
              )}

              {/* Icon */}
              <div
                className={cn(
                  "w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 z-10 transition-all duration-500",
                  step.status === "done" ? "bg-primary/20 text-primary" :
                  step.status === "active" ? "bg-primary/10 text-primary glow-border" :
                  "bg-secondary text-muted-foreground"
                )}
              >
                {step.status === "done" ? (
                  <Check className="w-4 h-4" />
                ) : step.status === "active" ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <step.icon className="w-4 h-4" />
                )}
              </div>

              {/* Content */}
              <div className="pb-6 flex-1 min-w-0">
                <p
                  className={cn(
                    "text-sm font-medium transition-colors",
                    step.status === "done" ? "text-foreground" :
                    step.status === "active" ? "text-primary" :
                    "text-muted-foreground"
                  )}
                >
                  {step.label}
                </p>
                {step.detail && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-xs text-muted-foreground mt-0.5 font-mono"
                  >
                    {step.detail}
                  </motion.p>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="p-4 border-t border-border/50 space-y-3">
        <div className="glass-panel p-3 space-y-2">
          <p className="text-xs font-medium text-muted-foreground">Processing Stats</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-muted-foreground">Events scanned</span>
              <p className="text-foreground font-mono font-medium">2,341,892</p>
            </div>
            <div>
              <span className="text-muted-foreground">Time elapsed</span>
              <p className="text-foreground font-mono font-medium">1.24s</p>
            </div>
            <div>
              <span className="text-muted-foreground">Services</span>
              <p className="text-foreground font-mono font-medium">4 active</p>
            </div>
            <div>
              <span className="text-muted-foreground">Anomalies</span>
              <p className="text-primary font-mono font-medium">3 found</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function getDetail(stepId: number): string {
  const details: Record<number, string> = {
    4: "Processing p95 latency...",
    5: "Rendering line chart...",
    6: "Saving to dashboard...",
  };
  return details[stepId] || "Processing...";
}
