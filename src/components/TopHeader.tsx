import { Search, Bell, ChevronDown, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

const environments = ["Production", "Staging", "Development"];

export function TopHeader() {
  const [env, setEnv] = useState("Production");
  const [envOpen, setEnvOpen] = useState(false);

  return (
    <header className="h-14 border-b border-border flex items-center justify-between px-4 bg-card/40 backdrop-blur-md z-10 flex-shrink-0">
      {/* Left: Project & Env */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-secondary text-secondary-foreground text-sm font-medium">
          <div className="w-2 h-2 rounded-full bg-success pulse-dot" />
          <span>acme-prod</span>
          <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
        </div>

        <div className="relative">
          <button
            onClick={() => setEnvOpen(!envOpen)}
            className={cn(
              "flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
              env === "Production" ? "bg-success/10 text-success" :
              env === "Staging" ? "bg-warning/10 text-warning" :
              "bg-info/10 text-info"
            )}
          >
            <div className={cn(
              "w-1.5 h-1.5 rounded-full",
              env === "Production" ? "bg-success" :
              env === "Staging" ? "bg-warning" :
              "bg-info"
            )} />
            {env}
            <ChevronDown className="w-3.5 h-3.5" />
          </button>
          {envOpen && (
            <div className="absolute top-full mt-1 left-0 glass-panel-strong p-1 min-w-[140px] z-50 animate-scale-in">
              {environments.map((e) => (
                <button
                  key={e}
                  onClick={() => { setEnv(e); setEnvOpen(false); }}
                  className={cn(
                    "w-full text-left px-3 py-1.5 rounded-md text-sm transition-colors",
                    e === env ? "bg-primary/10 text-primary" : "text-foreground hover:bg-secondary"
                  )}
                >
                  {e}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Center: Search */}
      <div className="flex-1 max-w-md mx-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search logs, services, traces..."
            className="w-full bg-secondary/60 border border-border/50 rounded-lg pl-9 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary/50 focus:border-primary/50 transition-all"
          />
          <kbd className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-muted-foreground bg-muted px-1.5 py-0.5 rounded border border-border font-mono">⌘K</kbd>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        <button className="relative p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-destructive" />
        </button>
        <div className="w-8 h-8 rounded-lg gradient-accent flex items-center justify-center cursor-pointer">
          <User className="w-4 h-4 text-accent-foreground" />
        </div>
      </div>
    </header>
  );
}
