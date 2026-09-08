const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const getAccessToken = () => sessionStorage.getItem("sentinel-access-token");

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Content-Type", "application/json");
  const token = getAccessToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep the HTTP error when the server has no JSON response.
    }
    throw new Error(message);
  }
  if (response.status === 204) return null;
  return response.json();
}

export async function login(username, password) {
  const result = await request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
  sessionStorage.setItem("sentinel-access-token", result.access_token);
  sessionStorage.setItem("sentinel-refresh-token", result.refresh_token);
  return result.user;
}

export function clearSession() {
  sessionStorage.removeItem("sentinel-access-token");
  sessionStorage.removeItem("sentinel-refresh-token");
  sessionStorage.removeItem("sentinel-logged-in");
}

const formatEventTime = (timestamp) => {
  if (!timestamp) return "--";
  return new Date(timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
};

const severityFor = (riskScore) => {
  if (riskScore >= 80) return "Critical";
  if (riskScore >= 60) return "High";
  if (riskScore >= 35) return "Medium";
  return "Low";
};

const statusFor = (decision) => {
  if (decision === "BLOCK" || decision === "CHALLENGE") return "Active";
  return "Resolved";
};

export function normalizeSecurityEvent(event) {
  const riskScore = Number(event.risk_score ?? 100 - Number(event.integrity_score ?? 100));
  const conflicts = Array.isArray(event.conflicts) ? event.conflicts : event.conflicts_detected || [];
  return {
    row: [formatEventTime(event.timestamp), event.device || event.source_entity || "Security Engine", event.type || event.decision || "Security event", severityFor(riskScore), statusFor(event.decision)],
    threat: {
      title: event.type === "SECURITY_EVENT" ? "Security Event" : event.type || "Security Alert",
      device: event.device || event.source_entity || "Security Engine",
      severity: severityFor(riskScore),
      color: severityFor(riskScore) === "Critical" ? "red" : severityFor(riskScore) === "High" ? "orange" : "purple",
      time: formatEventTime(event.timestamp),
      status: statusFor(event.decision),
      source: "SENTINEL Security Engine",
      description: event.evidence || conflicts.join(", ") || "Security telemetry was evaluated by the integrity engine.",
      recommendation: event.decision === "BLOCK" ? "Investigate the event and isolate the affected asset." : "Continue monitoring the affected asset.",
    },
  };
}

export async function getDashboardData() {
  const [risk, timeline, attackPath, summary, devices, telemetry, diagnostics] = await Promise.all([
    request("/dashboard/risk"),
    request("/dashboard/timeline?limit=20"),
    request("/dashboard/attack-path"),
    request("/dashboard/summary"),
    request("/devices"),
    request("/dashboard/telemetry?limit=100"),
    request("/collector/diagnostics"),
  ]);
  const normalized = timeline.map(normalizeSecurityEvent);
  const threats = normalized.map(({ threat }) => threat);
  return {
    riskScore: Number(risk.risk_score || 0),
    events: normalized.map(({ row }) => row),
    threats,
    riskHistory: timeline.slice().reverse().map((event) => Number(event.risk_score || 0)),
    summary,
    telemetry,
    diagnostics,
    devices: devices.map((device) => ({
      ...device,
      name: device.hostname || device.id,
      ip: device.ip_address || "-",
      type: device.device_type,
      zone: device.monitoring_scope?.zone || "Configured Scope",
      status: device.status === "ONLINE" ? "Online" : device.status === "OFFLINE" ? "Offline" : "Unknown",
      risk: null,
      lastSeen: device.last_telemetry_at ? new Date(device.last_telemetry_at).toLocaleString() : "No telemetry",
    })),
    attackPath,
  };
}
