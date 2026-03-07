import { motion } from "framer-motion";
import { LineChart, Line, BarChart, Bar, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const latencyData = Array.from({ length: 24 }, (_, i) => ({
  time: `${i}:00`,
  p50: 40 + Math.random() * 30,
  p95: 80 + Math.random() * 60,
  p99: 120 + Math.random() * 100 + (i > 14 && i < 18 ? 80 : 0),
}));

const errorData = Array.from({ length: 24 }, (_, i) => ({
  time: `${i}:00`,
  errors: Math.floor(5 + Math.random() * 15 + (i > 14 && i < 18 ? 30 : 0)),
}));

const serviceData = [
  { name: "gateway-api", requests: 4500, errors: 120 },
  { name: "auth-service", requests: 3200, errors: 45 },
  { name: "payment-service", requests: 2800, errors: 210 },
  { name: "db-shard-1", requests: 1900, errors: 35 },
];

const chartTooltipStyle = {
  contentStyle: {
    background: "hsl(222 44% 8% / 0.95)",
    border: "1px solid hsl(222 30% 16%)",
    borderRadius: "8px",
    fontSize: "12px",
    color: "hsl(210 40% 93%)",
  },
};

export function DashboardCharts() {
  return (
    <div className="grid grid-cols-2 gap-3 p-4">
      {/* Latency Chart */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="glass-panel p-4"
      >
        <h4 className="text-xs font-semibold text-foreground mb-3">Latency Over Time (ms)</h4>
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart data={latencyData}>
            <defs>
              <linearGradient id="latencyGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="hsl(187 85% 53%)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="hsl(187 85% 53%)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(222 30% 16%)" />
            <XAxis dataKey="time" tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} />
            <Tooltip {...chartTooltipStyle} />
            <Area type="monotone" dataKey="p50" stroke="hsl(210 80% 55%)" fillOpacity={0} strokeWidth={1.5} />
            <Area type="monotone" dataKey="p95" stroke="hsl(38 92% 55%)" fillOpacity={0} strokeWidth={1.5} />
            <Area type="monotone" dataKey="p99" stroke="hsl(187 85% 53%)" fill="url(#latencyGrad)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Error Rate Chart */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="glass-panel p-4"
      >
        <h4 className="text-xs font-semibold text-foreground mb-3">Error Rate Over Time</h4>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={errorData}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(222 30% 16%)" />
            <XAxis dataKey="time" tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} />
            <YAxis tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} />
            <Tooltip {...chartTooltipStyle} />
            <Bar dataKey="errors" fill="hsl(0 72% 55%)" radius={[3, 3, 0, 0]} opacity={0.8} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Service Requests */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.2 }}
        className="glass-panel p-4"
      >
        <h4 className="text-xs font-semibold text-foreground mb-3">Requests per Service</h4>
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={serviceData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(222 30% 16%)" horizontal={false} />
            <XAxis type="number" tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} />
            <YAxis type="category" dataKey="name" tick={{ fontSize: 10, fill: "hsl(215 20% 55%)" }} tickLine={false} axisLine={false} width={100} />
            <Tooltip {...chartTooltipStyle} />
            <Bar dataKey="requests" fill="hsl(187 85% 53%)" radius={[0, 3, 3, 0]} opacity={0.8} />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Top Failing Endpoints */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4, delay: 0.3 }}
        className="glass-panel p-4"
      >
        <h4 className="text-xs font-semibold text-foreground mb-3">Top Failing Endpoints</h4>
        <div className="space-y-2.5">
          {[
            { endpoint: "POST /api/checkout", rate: 45, service: "payment-service" },
            { endpoint: "GET /api/orders", rate: 28, service: "gateway-api" },
            { endpoint: "POST /api/auth/refresh", rate: 12, service: "auth-service" },
            { endpoint: "GET /api/inventory", rate: 8, service: "db-shard-1" },
          ].map((ep) => (
            <div key={ep.endpoint} className="flex items-center gap-3">
              <div className="flex-1 min-w-0">
                <p className="text-xs font-mono text-foreground truncate">{ep.endpoint}</p>
                <p className="text-[10px] text-muted-foreground">{ep.service}</p>
              </div>
              <div className="w-20">
                <div className="w-full h-1.5 bg-secondary rounded-full overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${ep.rate}%` }}
                    transition={{ duration: 0.8, delay: 0.5 }}
                    className="h-full rounded-full"
                    style={{
                      background: ep.rate > 30 ? "hsl(0 72% 55%)" : ep.rate > 15 ? "hsl(38 92% 55%)" : "hsl(187 85% 53%)"
                    }}
                  />
                </div>
              </div>
              <span className="text-xs font-mono text-destructive w-8 text-right">{ep.rate}%</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
