const BASE_URL = "http://127.0.0.1:8000";

export interface AgentChatResponse {
  output: string;
}

export interface TwilioMessageResponse {
  status: string;
  to: string;
  message: string;
  sid: string;
  timestamp: string;
}

export interface TwilioCallResponse {
  status: string;
  to: string;
  spoken_message: string;
  call_sid: string;
  timestamp: string;
}

export interface SystemMetrics {
  cpu_usage_percent: number;
  memory_usage_percent: number;
  disk_usage_percent: number;
  active_db_connections: number;
  service_status: string;
  timestamp: string;
}

export interface LogEntry {
  timestamp: string;
  level: "INFO" | "WARNING" | "ERROR";
  service: string;
  message: string;
}

export interface LogsResponse {
  total_logs: number;
  logs: LogEntry[];
}

export interface ApiError {
  error: boolean;
  message: string;
  code: number;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: "Request failed" }));
    throw new Error(err.message || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  agentChat: (input_string: string) =>
    request<AgentChatResponse>("/agent-chat", {
      method: "POST",
      body: JSON.stringify({ input_string }),
    }),

  sendMessage: (message: string) =>
    request<TwilioMessageResponse>("/twilio/send-message", {
      method: "POST",
      body: JSON.stringify({ message }),
    }),

  makeCall: (message: string) =>
    request<TwilioCallResponse>("/twilio/make-call", {
      method: "POST",
      body: JSON.stringify({ message }),
    }),

  getMetrics: () => request<SystemMetrics>("/system/metrics"),

  getLogs: () => request<LogsResponse>("/logs"),

  graphAgentChat: (input_string: string) =>
    request<AgentChatResponse>("/graph-agent-chat", {
      method: "POST",
      body: JSON.stringify({ input_string }),
    }),
};
