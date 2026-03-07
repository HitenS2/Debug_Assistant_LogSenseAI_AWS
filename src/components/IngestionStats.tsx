import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Activity, AlertTriangle, Server, Zap, Cpu, HardDrive, Database } from "lucide-react";
import { api, SystemMetrics } from "@/lib/api";

interface StatItem {
  label: string;
  value: string;
  icon: React.ElementType;
  color: string;
}

function formatMetrics(m: SystemMetrics): StatItem[] {
  return [
    { label: "CPU Usage", value: `${m.cpu_usage_percent}%`, icon: Cpu, color: "text-primary" },
    { label: "Memory", value: `${m.memory_usage_percent}%`, icon: Activity, color: m.memory_usage_percent > 80 ? "text-destructive" : "text-warning" },
    { label: "Disk", value: `${m.disk_usage_percent}%`, icon: HardDrive, color: "text-info" },
    { label: "DB Conns", value: `${m.active_db_connections}`, icon: Database, color: "text-success" },
  ];
}

const fallbackStats: StatItem[] = [
  { label: "CPU Usage", value: "—", icon: Cpu, color: "text-primary" },
  { label: "Memory", value: "—", icon: Activity, color: "text-warning" },
  { label: "Disk", value: "—", icon: HardDrive, color: "text-info" },
  { label: "DB Conns", value: "—", icon: Database, color: "text-success" },
];

export function IngestionStats() {
  const [stats, setStats] = useState<StatItem[]>(fallbackStats);
  const [serviceStatus, setServiceStatus] = useState<string>("Unknown");
  const [error, setError] = useState(false);

  const fetchMetrics = async () => {
    try {
      const m = await api.getMetrics();
      setStats(formatMetrics(m));
      setServiceStatus(m.service_status);
      setError(false);
    } catch {
      setError(true);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-4 gap-3 p-4">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1, duration: 0.3 }}
          className="glass-panel p-3 relative overflow-hidden group hover:glow-border transition-all duration-300"
        >
          <div className="flex items-center justify-between mb-2">
            <stat.icon className={`w-4 h-4 ${stat.color}`} />
            <div className="flex items-center gap-1">
              <div className={`w-1.5 h-1.5 rounded-full ${error ? "bg-destructive" : "bg-success pulse-dot"}`} />
              <span className="text-[10px] text-muted-foreground">{error ? "offline" : "live"}</span>
            </div>
          </div>
          <p className="text-lg font-bold font-mono text-foreground">{stat.value}</p>
          <div className="flex items-center justify-between mt-1">
            <span className="text-xs text-muted-foreground">{stat.label}</span>
            {!error && (
              <span className="text-[10px] font-mono text-success">{serviceStatus}</span>
            )}
          </div>
        </motion.div>
      ))}
    </div>
  );
}
