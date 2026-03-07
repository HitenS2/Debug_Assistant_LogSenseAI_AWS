import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Pause, Play, Search, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";
import { api, LogEntry as ApiLogEntry } from "@/lib/api";

interface LogEntry {
  id: string;
  timestamp: string;
  service: string;
  level: "INFO" | "WARN" | "ERROR" | "DEBUG";
  message: string;
}

export function LiveLogsPanel() {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [paused, setPaused] = useState(false);
  const [search, setSearch] = useState("");
  const [filterLevel, setFilterLevel] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const fetchLogs = async () => {
    try {
      const res = await api.getLogs();
      const mapped: LogEntry[] = res.logs.map((l, i) => ({
        id: `${l.timestamp}-${i}-${Math.random().toString(36).substr(2, 5)}`,
        timestamp: l.timestamp.replace("T", " ").substring(0, 23),
        service: l.service,
        level: l.level === "WARNING" ? "WARN" : l.level as LogEntry["level"],
        message: l.message,
      }));
      setLogs((prev) => {
        const combined = [...prev, ...mapped];
        return combined.slice(-100); // keep last 100
      });
      setError(null);
    } catch (err) {
      setError("Could not fetch logs from backend");
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  useEffect(() => {
    if (paused) return;
    const interval = setInterval(fetchLogs, 3000);
    return () => clearInterval(interval);
  }, [paused]);

  useEffect(() => {
    if (!paused && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs, paused]);

  const filtered = logs.filter((l) => {
    if (filterLevel && l.level !== filterLevel) return false;
    if (search && !l.message.toLowerCase().includes(search.toLowerCase()) && !l.service.includes(search)) return false;
    return true;
  });

  const levelColor: Record<string, string> = {
    INFO: "text-info bg-info/10",
    WARN: "text-warning bg-warning/10",
    ERROR: "text-destructive bg-destructive/10",
    DEBUG: "text-muted-foreground bg-muted",
  };

  return (
    <div className="flex flex-col h-full">
      {/* Controls */}
      <div className="px-4 py-3 border-b border-border/50 flex items-center gap-2 flex-wrap">
        <button
          onClick={() => setPaused(!paused)}
          className={cn(
            "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors",
            paused ? "bg-success/10 text-success" : "bg-secondary text-muted-foreground"
          )}
        >
          {paused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
          {paused ? "Resume" : "Pause"}
        </button>

        <button
          onClick={fetchLogs}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-secondary text-muted-foreground hover:text-foreground transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Refresh
        </button>

        <div className="relative flex-1 min-w-[120px] max-w-[200px]">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Filter logs..."
            className="w-full bg-secondary/60 border border-border/40 rounded-md pl-7 pr-2 py-1.5 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary/40"
          />
        </div>

        <div className="flex gap-1">
          {["INFO", "WARN", "ERROR", "DEBUG"].map((lv) => (
            <button
              key={lv}
              onClick={() => setFilterLevel(filterLevel === lv ? null : lv)}
              className={cn(
                "px-2 py-1 rounded text-[10px] font-mono font-medium transition-colors",
                filterLevel === lv ? levelColor[lv] : "text-muted-foreground hover:bg-secondary"
              )}
            >
              {lv}
            </button>
          ))}
        </div>

        {error && (
          <span className="text-[10px] text-destructive ml-auto">⚠ {error}</span>
        )}
      </div>

      {/* Logs */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-thin font-mono text-xs">
        {filtered.length === 0 && (
          <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
            {error ? "Backend unavailable — check server" : "No logs yet"}
          </div>
        )}
        <AnimatePresence initial={false}>
          {filtered.map((log) => (
            <motion.div
              key={log.id}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              className="flex items-start gap-3 px-4 py-1.5 border-b border-border/20 hover:bg-secondary/30 transition-colors"
            >
              <span className="text-muted-foreground w-[170px] flex-shrink-0">{log.timestamp}</span>
              <span className={cn("w-12 text-center rounded px-1 py-0.5 text-[10px] font-bold flex-shrink-0", levelColor[log.level])}>
                {log.level}
              </span>
              <span className="text-primary/80 w-[120px] flex-shrink-0 truncate">{log.service}</span>
              <span className="text-foreground/80 flex-1 truncate">{log.message}</span>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
