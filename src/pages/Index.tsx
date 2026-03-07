import { useState } from "react";
import { AppSidebar } from "@/components/AppSidebar";
import { TopHeader } from "@/components/TopHeader";
import { AIChatPanel } from "@/components/AIChatPanel";
import { AIThinkingPanel } from "@/components/AIThinkingPanel";
import { LiveLogsPanel } from "@/components/LiveLogsPanel";
import { IngestionStats } from "@/components/IngestionStats";
import { DashboardCharts } from "@/components/DashboardCharts";
import { PersonalizedDashboard } from "@/components/PersonalizedDashboard";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";
import { toast } from "@/hooks/use-toast";
import { Phone, MessageSquare, Loader2 } from "lucide-react";

type View = "home" | "logs" | "ai" | "dashboards" | "personalized" | "alerts" | "incidents" | "settings";

const Index = () => {
  const [activeTab, setActiveTab] = useState<View>("home");

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden">
      <AppSidebar activeTab={activeTab} onTabChange={(t) => setActiveTab(t as View)} />

      <div className="flex-1 flex flex-col min-w-0">
        <TopHeader />

        {activeTab === "home" && <HomeView />}
        {activeTab === "logs" && <LogsView />}
        {activeTab === "ai" && <AIView />}
        {activeTab === "dashboards" && <DashboardView />}
        {activeTab === "personalized" && <PersonalizedDashboard />}
        {activeTab === "alerts" && <AlertsView />}
        {activeTab === "incidents" && <IncidentsView />}
        {activeTab === "settings" && <SettingsView />}
      </div>
    </div>
  );
};

function HomeView() {
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <IngestionStats />
      <div className="flex-1 flex min-h-0">
        {/* AI Chat - Main */}
        <div className="flex-1 min-w-0 border-r border-border/50">
          <AIChatPanel />
        </div>
        {/* Agent Thinking - Right */}
        <div className="w-72 flex-shrink-0 border-l border-border/30">
          <AIThinkingPanel />
        </div>
      </div>
    </div>
  );
}

function LogsView() {
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <IngestionStats />
      <div className="flex-1 min-h-0">
        <LiveLogsPanel />
      </div>
    </div>
  );
}

function AIView() {
  return (
    <div className="flex-1 flex min-h-0">
      <div className="flex-1 min-w-0">
        <AIChatPanel />
      </div>
      <div className="w-80 flex-shrink-0 border-l border-border/30">
        <AIThinkingPanel />
      </div>
    </div>
  );
}

function DashboardView() {
  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin">
      <IngestionStats />
      <DashboardCharts />
    </div>
  );
}

function AlertsView() {
  const [sendingMsg, setSendingMsg] = useState(false);
  const [callingPhone, setCallingPhone] = useState(false);

  const alerts = [
    { name: "Error Rate > 5%", service: "payment-service", status: "firing", severity: "critical" },
    { name: "Latency p99 > 200ms", service: "gateway-api", status: "firing", severity: "warning" },
    { name: "DB Connection Pool > 80%", service: "db-shard-1", status: "resolved", severity: "warning" },
    { name: "Memory Usage > 90%", service: "auth-service", status: "resolved", severity: "info" },
  ];

  const handleSendSMS = async (alertName: string) => {
    setSendingMsg(true);
    try {
      const res = await api.sendMessage(`Alert: ${alertName}`);
      toast({ title: "SMS Sent", description: `${res.status} to ${res.to}` });
    } catch {
      toast({ title: "SMS Failed", description: "Could not reach backend", variant: "destructive" });
    } finally {
      setSendingMsg(false);
    }
  };

  const handleCall = async (alertName: string) => {
    setCallingPhone(true);
    try {
      const res = await api.makeCall(`Alert. ${alertName}`);
      toast({ title: "Call Initiated", description: `${res.status} to ${res.to}` });
    } catch {
      toast({ title: "Call Failed", description: "Could not reach backend", variant: "destructive" });
    } finally {
      setCallingPhone(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto scrollbar-thin p-4">
      <h2 className="text-lg font-semibold text-foreground mb-4">Active Alerts</h2>
      <div className="space-y-3">
        {alerts.map((alert, i) => (
          <motion.div
            key={alert.name}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className={cn(
              "glass-panel p-4 flex items-center justify-between",
              alert.status === "firing" && "glow-border"
            )}
          >
            <div>
              <p className="text-sm font-medium text-foreground">{alert.name}</p>
              <p className="text-xs text-muted-foreground font-mono mt-0.5">{alert.service}</p>
            </div>
            <div className="flex items-center gap-3">
              {alert.status === "firing" && (
                <>
                  <button
                    onClick={() => handleSendSMS(alert.name)}
                    disabled={sendingMsg}
                    className="flex items-center gap-1 px-2 py-1 rounded-lg bg-info/10 text-info text-[10px] font-medium hover:bg-info/20 transition-colors disabled:opacity-50"
                  >
                    {sendingMsg ? <Loader2 className="w-3 h-3 animate-spin" /> : <MessageSquare className="w-3 h-3" />}
                    SMS
                  </button>
                  <button
                    onClick={() => handleCall(alert.name)}
                    disabled={callingPhone}
                    className="flex items-center gap-1 px-2 py-1 rounded-lg bg-warning/10 text-warning text-[10px] font-medium hover:bg-warning/20 transition-colors disabled:opacity-50"
                  >
                    {callingPhone ? <Loader2 className="w-3 h-3 animate-spin" /> : <Phone className="w-3 h-3" />}
                    Call
                  </button>
                </>
              )}
              <span className={cn(
                "text-[10px] font-medium px-2 py-0.5 rounded-full",
                alert.severity === "critical" ? "bg-destructive/10 text-destructive" :
                alert.severity === "warning" ? "bg-warning/10 text-warning" :
                "bg-info/10 text-info"
              )}>
                {alert.severity}
              </span>
              <span className={cn(
                "text-xs font-medium flex items-center gap-1.5",
                alert.status === "firing" ? "text-destructive" : "text-success"
              )}>
                <span className={cn(
                  "w-1.5 h-1.5 rounded-full",
                  alert.status === "firing" ? "bg-destructive pulse-dot" : "bg-success"
                )} />
                {alert.status}
              </span>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Alert Builder */}
      <div className="mt-6">
        <h3 className="text-sm font-semibold text-foreground mb-3">Create Alert</h3>
        <div className="glass-panel p-4 space-y-3">
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Metric</label>
              <select className="w-full bg-secondary/60 border border-border/40 rounded-lg px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary/50">
                <option>Error Rate</option>
                <option>Latency p99</option>
                <option>Memory Usage</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Condition</label>
              <select className="w-full bg-secondary/60 border border-border/40 rounded-lg px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-primary/50">
                <option>&gt; Greater than</option>
                <option>&lt; Less than</option>
                <option>= Equals</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">Threshold</label>
              <input type="text" placeholder="5%" className="w-full bg-secondary/60 border border-border/40 rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary/50" />
            </div>
          </div>
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">Notify via</label>
            <div className="flex gap-2">
              {["Slack", "Email", "PagerDuty", "SMS", "Phone Call"].map((ch) => (
                <button key={ch} className="px-3 py-1.5 rounded-lg bg-secondary/60 border border-border/40 text-xs text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all">
                  {ch}
                </button>
              ))}
            </div>
          </div>
          <button className="gradient-primary text-primary-foreground px-4 py-2 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity">
            Create Alert
          </button>
        </div>
      </div>
    </div>
  );
}

function IncidentsView() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center">
        <p className="text-lg font-semibold text-foreground mb-1">No Active Incidents</p>
        <p className="text-sm text-muted-foreground">All systems operational</p>
      </div>
    </div>
  );
}

function SettingsView() {
  return (
    <div className="flex-1 flex items-center justify-center">
      <div className="text-center">
        <p className="text-lg font-semibold text-foreground mb-1">Settings</p>
        <p className="text-sm text-muted-foreground">Configuration coming soon</p>
      </div>
    </div>
  );
}

export default Index;
