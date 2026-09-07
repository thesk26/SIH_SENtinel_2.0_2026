import { useState,useEffect } from "react";
import {
  Shield,
  LayoutDashboard,
  Monitor,
  AlertTriangle,
  Network,
  BarChart3,
  ShieldCheck,
  FileText,
  Settings,
  Bell,
  Moon,
  ArrowUpRight,
  Activity,
  Server,
  Camera,
  Wifi,
  Printer,
  Brain,
  CheckCircle2,
  Search,
  Plus,
  Eye,
  MoreHorizontal,
  SlidersHorizontal,

} from "lucide-react";

import "./App.css";

const stats = [
  {
    title: "Cyber Health Score",
    value: "87",
    type: "health",
    description: "Your infrastructure is secure",
  },
  {
    title: "Total Devices",
    value: "127",
    type: "devices",
  },
  {
    title: "Active Threats",
    value: "5",
    type: "threat",
  },
  {
    title: "Incidents Resolved",
    value: "24",
    type: "resolved",
  },
];

const events = [
  ["10:24:32 AM", "CAM-07", "Malware detected (Trojan.Win32)", "Critical", "Active"],
  ["09:15:47 AM", "SRV-APP-02", "Failed login attempt (5 times)", "High", "Active"],
  ["08:45:12 AM", "IOT-22", "Unusual data transfer detected", "High", "Investigating"],
  ["07:30:55 AM", "PC-ADMIN-03", "USB device policy violation", "Medium", "Resolved"],
  ["06:22:18 AM", "AP-01", "New device connected", "Low", "Resolved"],
];

const threats = [
  {
    title: "Malware Detected",
    device: "CAM-07",
    severity: "Critical",
    color: "red",
    time: "Today, 10:24 AM",
  },
  {
    title: "Unauthorized Access Attempt",
    device: "SRV-APP-02",
    severity: "High",
    color: "orange",
    time: "Today, 09:15 AM",
  },
  {
    title: "Anomalous Behavior",
    device: "IOT-22",
    severity: "High",
    color: "purple",
    time: "Today, 08:45 AM",
  },
  {
    title: "Policy Violation",
    device: "PC-ADMIN-03",
    severity: "Medium",
    color: "orange",
    time: "Today, 07:30 AM",
  },
];

const devices = [
  {
    name: "SRV-DB-01",
    ip: "10.0.1.10",
    type: "Server",
    zone: "Data Center",
    status: "Online",
    risk: 20,
    lastSeen: "2 min ago",
  },
  {
    name: "SRV-APP-02",
    ip: "10.0.1.11",
    type: "Server",
    zone: "Data Center",
    status: "Online",
    risk: 35,
    lastSeen: "1 min ago",
  },
  {
    name: "PC-ADMIN-03",
    ip: "10.0.2.15",
    type: "Workstation",
    zone: "Office",
    status: "Online",
    risk: 25,
    lastSeen: "1 min ago",
  },
  {
    name: "CAM-07",
    ip: "10.0.3.25",
    type: "Camera",
    zone: "Office",
    status: "At Risk",
    risk: 78,
    lastSeen: "1 min ago",
  },
  {
    name: "IOT-22",
    ip: "10.0.3.45",
    type: "IoT Device",
    zone: "Office",
    status: "At Risk",
    risk: 65,
    lastSeen: "1 min ago",
  },
  {
    name: "FW-01",
    ip: "10.0.1.1",
    type: "Firewall",
    zone: "Data Center",
    status: "Online",
    risk: 10,
    lastSeen: "2 min ago",
  },
  {
    name: "AP-01",
    ip: "10.0.2.5",
    type: "Access Point",
    zone: "Office",
    status: "Online",
    risk: 15,
    lastSeen: "2 min ago",
  },
  {
    name: "PRN-01",
    ip: "10.0.2.20",
    type: "Printer",
    zone: "Office",
    status: "Offline",
    risk: null,
    lastSeen: "20 min ago",
  },
];
function StatCard({ item }) {
  return (
    <div className="stat-card">
      <div className="stat-top">
        <span>{item.title}</span>

        {item.type === "devices" && (
          <div className="stat-icon blue">
            <Monitor size={21} />
          </div>
        )}

        {item.type === "threat" && (
          <div className="stat-icon red-icon">
            <Shield size={21} />
          </div>
        )}

        {item.type === "resolved" && (
          <div className="stat-icon green-icon">
            <CheckCircle2 size={21} />
          </div>
        )}
      </div>

      {item.type === "health" ? (
        <div className="health-content">
          <div className="health-ring">
            <div className="health-inner">
              <strong>87</strong>
              <small>/100</small>
            </div>
          </div>

          <div>
            <div className="good">Good</div>
            <p>{item.description}</p>
            <a href="#">
              View Details <ArrowUpRight size={13} />
            </a>
          </div>
        </div>
      ) : (
        <>
          <div
            className={`stat-number ${
              item.type === "threat" ? "threat-number" : ""
            }`}
          >
            {item.value}
          </div>

          <div className="stat-extra">
            {item.type === "devices" && (
              <>
                <span className="green">Online: 112</span>
                <span className="red">Offline: 15</span>
              </>
            )}

            {item.type === "threat" && (
              <>
                <span className="red">Critical: 2</span>
                <span className="orange">High: 3</span>
              </>
            )}

            {item.type === "resolved" && (
              <>
                Today: <span className="green">6</span>
              </>
            )}
          </div>
        </>
      )}
    </div>
  );
}

function NetworkNode({ className, icon, name, status }) {
  return (
    <div className={`network-node ${className}`}>
      <div className="node-icon">{icon}</div>
      <span>{name}</span>
      <i className={status}></i>
    </div>
  );
}

function Infrastructure() {
  return (
    <div className="panel infrastructure">
      <div className="panel-header">
        <h3>Infrastructure Overview</h3>

        <button className="zone-btn">
          All Zones
        </button>
      </div>

      <div className="network">

        <NetworkNode
          className="server1"
          icon={<Server size={17} />}
          name="SRV-DB-01"
          status="online"
        />

        <NetworkNode
          className="server2"
          icon={<Server size={17} />}
          name="SRV-APP-02"
          status="online"
        />

        <NetworkNode
          className="camera"
          icon={<Camera size={17} />}
          name="CAM-07"
          status="critical"
        />

        <NetworkNode
          className="iot"
          icon={<Activity size={17} />}
          name="IOT-22"
          status="warning"
        />

        <div className="core-switch">
          <Network size={25} />
          <span>CORE-SW-01</span>
        </div>

        <NetworkNode
          className="pc"
          icon={<Monitor size={17} />}
          name="PC-ADMIN-03"
          status="online"
        />

        <NetworkNode
          className="printer"
          icon={<Printer size={17} />}
          name="PRN-01"
          status="online"
        />

        <NetworkNode
          className="firewall"
          icon={<ShieldCheck size={17} />}
          name="FW-01"
          status="online"
        />

        <NetworkNode
          className="access"
          icon={<Wifi size={17} />}
          name="AP-01"
          status="online"
        />
      </div>

      <div className="network-legend">
        <span><i className="dot secure"></i> Secure</span>
        <span><i className="dot warning"></i> Warning</span>
        <span><i className="dot critical"></i> Critical</span>
        <span><i className="dot offline"></i> Offline</span>
      </div>
    </div>
  );
}

function ThreatDistribution() {
  return (
    <div className="panel threat-distribution">
      <div className="panel-header">
        <h3>Threat Distribution</h3>
      </div>

      <div className="threat-chart-area">
        <div className="donut">
          <div className="donut-center">
            <small>Total</small>
            <strong>5</strong>
          </div>
        </div>

        <div className="threat-list">
          <div>
            <span><i className="dot red"></i> Malware</span>
            <b>2 (40%)</b>
          </div>

          <div>
            <span><i className="dot orange"></i> Unauthorized Access</span>
            <b>1 (20%)</b>
          </div>

          <div>
            <span><i className="dot purple"></i> Anomalous Behavior</span>
            <b>1 (20%)</b>
          </div>

          <div>
            <span><i className="dot blue-dot"></i> Policy Violation</span>
            <b>1 (20%)</b>
          </div>
        </div>
      </div>
    </div>
  );
}

function RiskTrend() {
  const [points, setPoints] = useState([
    75, 60, 68, 52, 58, 48, 55, 50, 62, 72
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setPoints((oldPoints) => {
        const last = oldPoints[oldPoints.length - 1];

        // Small realistic change from the previous risk value
        const change = Math.floor(Math.random() * 21) - 10;

        const newValue = Math.max(
          25,
          Math.min(95, last + change)
        );

        return [...oldPoints.slice(1), newValue];
      });
    }, 700);

    return () => clearInterval(interval);
  }, []);

  const graphPoints = points
    .map((y, index) => {
      const x = (index / (points.length - 1)) * 600;
      const graphY = 180 - (y / 100) * 130;

      return `${x},${graphY}`;
    })
    .join(" ");

  const fillPoints = `0,180 ${graphPoints} 600,180`;

  const currentRisk = points[points.length - 1];

  return (
    <div className="panel risk-panel">
      <div className="panel-header">
        <h3>
          Risk Trend <small>(7 Days)</small>
        </h3>

        <span className="risk-live">
          LIVE
        </span>
      </div>

      <div className="risk-chart">
        <svg
          viewBox="0 0 600 200"
          preserveAspectRatio="none"
        >
          <line
            x1="0"
            y1="180"
            x2="600"
            y2="180"
            className="chart-line"
          />

          <polygon
            points={fillPoints}
            className="risk-fill"
          />

          <polyline
            points={graphPoints}
            fill="none"
            className="risk-wave"
          />

          <circle
            cx="600"
            cy={180 - (currentRisk / 100) * 130}
            r="5"
            className="risk-dot"
          />
        </svg>

        <div className="risk-value">
          Risk Score: <strong>{currentRisk}</strong>
        </div>
      </div>
    </div>
  );
}

function RecentThreats() {
  return (
    <div className="panel recent-threats">
      <div className="panel-header">
        <h3>Recent Threats</h3>
        <a href="#">
          View All <ArrowUpRight size={13} />
        </a>
      </div>

      <div className="threat-items">
        {threats.map((threat) => (
          <div className={`threat-item ${threat.color}`} key={threat.title}>
            <div className="threat-symbol">⚠</div>

            <div className="threat-info">
              <strong>{threat.title}</strong>
              <span>{threat.device}</span>
            </div>

            <div className="threat-meta">
              <em>{threat.severity}</em>
              <span>{threat.time}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SecurityEvents() {
  return (
    <div className="panel security-events">
      <div className="panel-header">
        <h3>Recent Security Events</h3>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th>Device</th>
              <th>Event</th>
              <th>Severity</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {events.map((event, index) => (
              <tr key={index}>
                <td>{event[0]}</td>
                <td>{event[1]}</td>
                <td>{event[2]}</td>
                <td>
                  <span className={`badge ${event[3].toLowerCase()}`}>
                    {event[3]}
                  </span>
                </td>
                <td>
                  <span
                    className={`status-badge ${
                      event[4] === "Active"
                        ? "active"
                        : event[4] === "Investigating"
                        ? "investigating"
                        : "resolved"
                    }`}
                  >
                    {event[4]}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button className="view-events">
        View All Events <ArrowUpRight size={14} />
      </button>
    </div>
  );
}

function AIRecommendation() {
  return (
    <div className="panel ai-panel">
      <div className="panel-header">
        <h3>AI Recommendation</h3>
      </div>

      <div className="ai-box">
        <div className="ai-title">
          <div className="ai-icon">
            <Brain size={21} />
          </div>

          <div>
            <strong>High Risk Detected</strong>
            <p>
              CAM-07 is showing malicious behavior similar to known attack
              patterns.
            </p>
          </div>
        </div>

        <h4>Recommended Actions:</h4>

        <ul>
          <li>Isolate device</li>
          <li>Run full malware scan</li>
          <li>Preserve evidence</li>
        </ul>

        <button>Take Action</button>
      </div>
    </div>
  );
}

function Devices() {
  const [selectedDevice, setSelectedDevice] = useState(devices[0]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All Devices");
  const [statusFilter, setStatusFilter] = useState("All Status");
  const [zoneFilter, setZoneFilter] = useState("All Zones");

  const categories = [
    ["All Devices", 127],
    ["Servers", 18],
    ["Workstations", 32],
    ["Network", 24],
    ["IoT", 28],
    ["Others", 25],
  ];

  const filteredDevices = devices.filter((device) => {
    const matchesSearch =
      device.name.toLowerCase().includes(search.toLowerCase()) ||
      device.ip.toLowerCase().includes(search.toLowerCase());

    let matchesCategory = true;

    if (category === "Servers") {
      matchesCategory = device.type === "Server";
    } else if (category === "Workstations") {
      matchesCategory = device.type === "Workstation";
    } else if (category === "IoT") {
      matchesCategory = device.type === "IoT Device";
    } else if (category === "Network") {
      matchesCategory =
        device.type === "Firewall" || device.type === "Access Point";
    } else if (category === "Others") {
      matchesCategory = ![
        "Server",
        "Workstation",
        "IoT Device",
        "Firewall",
        "Access Point",
      ].includes(device.type);
    }

    const matchesStatus =
      statusFilter === "All Status" ||
      device.status === statusFilter;

    const matchesZone =
      zoneFilter === "All Zones" ||
      device.zone === zoneFilter;

    return (
      matchesSearch &&
      matchesCategory &&
      matchesStatus &&
      matchesZone
    );
  });
  useEffect(() => {
  if (
    filteredDevices.length > 0 &&
    !filteredDevices.some(
      (device) => device.name === selectedDevice?.name
    )
  ) {
    setSelectedDevice(filteredDevices[0]);
  }
  }, [category, statusFilter, zoneFilter, search]);

  return (
    <div className="devices-page">
      <div className="devices-top">
        <div>
          <h1>Devices</h1>
          <p>Monitor and manage all connected devices</p>
        </div>

        <button className="add-device">
          <Plus size={16} />
          Add Device
        </button>
      </div>

      <div className="devices-tabs">
        {categories.map(([name, count]) => (
          <button
            key={name}
            className={
              category === name
                ? "device-tab active"
                : "device-tab"
            }
            onClick={() => setCategory(name)}
          >
            {name} <span>{count}</span>
          </button>
        ))}
      </div>

      <div className="devices-filters">
        <div className="device-search">
          <Search size={15} />

          <input
            type="text"
            placeholder="Search devices..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option>All Status</option>
          <option>Online</option>
          <option>At Risk</option>
          <option>Offline</option>
        </select>

        <select
          value={zoneFilter}
          onChange={(e) => setZoneFilter(e.target.value)}
        >
          <option>All Zones</option>
          <option>Office</option>
          <option>Data Center</option>
        </select>
      </div>

      <div className="panel devices-table-panel">
        <table className="devices-table">
          <thead>
            <tr>
              <th>DEVICE NAME</th>
              <th>IP ADDRESS</th>
              <th>TYPE</th>
              <th>ZONE</th>
              <th>STATUS</th>
              <th>RISK SCORE</th>
              <th>LAST SEEN</th>
              <th>ACTIONS</th>
            </tr>
          </thead>

          <tbody>
            {filteredDevices.map((device) => (
              <tr 
                key={device.name}
                onClick={() =>
              setSelectedDevice(device)}   
              >   
                <td className="device-name">
                  {device.name}
                </td>

                <td>{device.ip}</td>

                <td>{device.type}</td>

                <td>{device.zone}</td>

                <td>
                  <span
                    className={`device-status ${
                      device.status === "Online"
                        ? "online"
                        : device.status === "At Risk"
                        ? "at-risk"
                        : "offline"
                    }`}
                  >
                    <i></i>
                    {device.status}
                  </span>
                </td>

                <td>
                  <span
                    className={`risk-score ${
                      device.risk >= 70
                        ? "high-risk"
                        : device.risk >= 30
                        ? "medium-risk"
                        : "low-risk"
                    }`}
                  >
                    {device.risk ?? "—"}
                  </span>
                </td>

                <td>{device.lastSeen}</td>

                <td>
                  <div className="device-actions">
                    <button>
                      <Eye size={14} />
                    </button>

                    <button>
                      <SlidersHorizontal size={14} />
                    </button>

                    <button>
                      <MoreHorizontal size={15} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="device-detail-grid">
        <div className="panel selected-device">
          <div className="selected-device-top">
            <div className="camera-preview">
              <Camera size={38} />
            </div>

            <div className="selected-device-info">
              <div className="selected-title">
                <h3>{selectedDevice?.name}</h3>

                <span className="device-status at-risk">
                  <i></i>
                  At Risk
                </span>
              </div>

              <div className="device-details">
                <div>
                  <span>IP Address</span>
                  <strong>{selectedDevice?.ip}</strong>
                </div>

                <div>
                  <span>Type</span>
                  <strong>{selectedDevice?.type}</strong>
                </div>

                <div>
                  <span>Zone</span>
                  <strong>{selectedDevice?.zone}</strong>
                </div>

                <div>
                  <span>Risk Score</span>
                  <strong className="detail-risk">{selectedDevice?.risk ?? "-"}</strong>
                </div>
              </div>

              <div className="device-details second-row">
                <div>
                  <span>Vendor</span>
                  <strong>Hikvision</strong>
                </div>

                <div>
                  <span>Last Seen</span>
                  <strong>1 min ago</strong>
                </div>

                <div>
                  <span>Uptime</span>
                  <strong>120d 4h 32m</strong>
                </div>
              </div>
            </div>
          </div>

          <div className="risk-reason">
            <strong>Reason:</strong> Malware detected and unauthorized outbound connections.
          </div>
        </div>

        <div className="panel recent-activity">
          <div className="panel-header">
            <h3>Recent Activity</h3>
          </div>

          <div className="activity-list">
            <div>
              <i className="activity-dot red"></i>
              <span>Malware detected (Trojan.Win32)</span>
              <time>10:34 AM</time>
            </div>

            <div>
              <i className="activity-dot red"></i>
              <span>Unauthorized outbound connection</span>
              <time>10:20 AM</time>
            </div>

            <div>
              <i className="activity-dot orange"></i>
              <span>Multiple failed login attempts</span>
              <time>10:15 AM</time>
            </div>
          </div>

          <button className="view-full-details">
            View Full Details
          </button>
        </div>
      </div>
    </div>
  );
}

function Sidebar({ active, setActive }) {
  const items = [
    ["Dashboard", <LayoutDashboard size={18} />],
    ["Devices", <Monitor size={18} />],
    ["Threats & Alerts", <AlertTriangle size={18} />],
    ["Network Map", <Network size={18} />],
    ["Risk Analysis", <BarChart3 size={18} />],
    ["Response Center", <ShieldCheck size={18} />],
    ["Reports", <FileText size={18} />],
    ["Settings", <Settings size={18} />],
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-logo">
          <Shield size={23} />
        </div>

        <div>
          <strong>SENTINEL</strong>
          <span>Autonomous Cyber Defense System</span>
        </div>
      </div>

      <nav>
        {items.map(([name, icon]) => (
          <button
            key={name}
            className={active === name ? "nav-active" : ""}
            onClick={() => setActive(name)}
          >
            {icon}
            <span>{name}</span>
          </button>
        ))}
      </nav>

      <div className="ai-status">
        <div className="ai-status-icon">
          <Brain size={20} />
        </div>

        <strong>AI Engine</strong>

        <div className="ai-status-row">
          <span>Status:</span>
          <b>Active</b>
        </div>

        <div className="ai-status-row">
          <span>Model:</span>
          <span>v2.4.1</span>
        </div>

        <div className="ai-status-row">
          <span>Updated:</span>
          <span>2 min ago</span>
        </div>
      </div>
    </aside>
  );
}

function Header() {
  return (
    <header className="header">
      <div>
        <h1>Dashboard</h1>
        <p>Real-time overview of your infrastructure security</p>
      </div>

      <div className="header-right">
        <div className="system-status">
          <span></span>
          <div>
            <small>System Status</small>
            <strong>Secure</strong>
          </div>
        </div>

        <button className="header-button notification">
          <Bell size={19} />
          <i>3</i>
        </button>

        <button className="header-button">
          <Moon size={19} />
        </button>

        <div className="profile">
          <div className="avatar">A</div>

          <div>
            <strong>Admin</strong>
            <span>Security Operator</span>
          </div>
        </div>
      </div>
    </header>
  );
}

function Dashboard() {
  return (
    <>
      <Header />

      <main className="dashboard">
        <section className="stats-grid">
          {stats.map((item) => (
            <StatCard item={item} key={item.title} />
          ))}
        </section>

        <section className="main-grid">
          <Infrastructure />

          <div className="middle-column">
            <ThreatDistribution />
            <RiskTrend />
          </div>

          <RecentThreats />
        </section>

        <section className="bottom-grid">
          <SecurityEvents />
          <AIRecommendation />
        </section>
      </main>
    </>
  );
}

function ThreatsAlerts() {
  const [statusFilter, setStatusFilter] = useState("All Status");

  const filteredThreats = threats.filter((threat) => {
    if (statusFilter === "All Status") return true;
    return threat.status === statusFilter;
  });

  const criticalCount = threats.filter(
    (threat) => threat.severity === "Critical"
  ).length;

  const highCount = threats.filter(
    (threat) => threat.severity === "High"
  ).length;

  const mediumCount = threats.filter(
    (threat) => threat.severity === "Medium"
  ).length;

  const lowCount = threats.filter(
    (threat) => threat.severity === "Low"
  ).length;

  return (
    <div className="threats-page">

      <div className="threats-top">
        <div>
          <h1>Threats & Alerts</h1>
          <p>Detect, investigate and respond to security threats</p>
        </div>

        <select
          className="threat-status-filter"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option>All Status</option>
          <option>Active</option>
          <option>Investigating</option>
          <option>Resolved</option>
        </select>
      </div>

      <div className="threat-summary">

        <div className="threat-summary-card">
          <div className="summary-icon purple">
            <Shield size={18} />
          </div>
          <div>
            <span>AI Threats</span>
            <strong>{threats.length}</strong>
          </div>
        </div>

        <div className="threat-summary-card critical-card">
          <div className="summary-icon red">
            <AlertTriangle size={18} />
          </div>
          <div>
            <span>Critical</span>
            <strong>{criticalCount}</strong>
          </div>
        </div>

        <div className="threat-summary-card">
          <div className="summary-icon orange">
            <AlertTriangle size={18} />
          </div>
          <div>
            <span>High</span>
            <strong>{highCount}</strong>
          </div>
        </div>

        <div className="threat-summary-card">
          <div className="summary-icon yellow">
            <AlertTriangle size={18} />
          </div>
          <div>
            <span>Medium</span>
            <strong>{mediumCount}</strong>
          </div>
        </div>

        <div className="threat-summary-card">
          <div className="summary-icon green">
            <CheckCircle2 size={18} />
          </div>
          <div>
            <span>Low</span>
            <strong>{lowCount}</strong>
          </div>
        </div>

      </div>

      <div className="panel threats-list-panel">

        <div className="panel-header">
          <div>
            <h3>Threats & Alerts</h3>
            <p>Recent security detections from your infrastructure</p>
          </div>
        </div>

        <div className="threat-list">

          {filteredThreats.map((threat, index) => (
            <div
              className={`threat-item ${threat.color}`}
              key={`${threat.title}-${index}`}
            >

              <div className={`threat-icon ${threat.color}`}>
                <AlertTriangle size={18} />
              </div>

              <div className="threat-main">

                <div className="threat-title-row">
                  <h4>{threat.title}</h4>

                  <span className={`severity-badge ${threat.color}`}>
                    {threat.severity}
                  </span>
                </div>

                <div className="threat-info">

                  <div>
                    <span>Device</span>
                    <strong>{threat.device}</strong>
                  </div>

                  <div>
                    <span>Detected</span>
                    <strong>{threat.time}</strong>
                  </div>

                  <div>
                    <span>Status</span>
                    <strong className="threat-active">
                      {threat.status}
                    </strong>
                  </div>

                </div>

              </div>

              <button className="view-threat">
                View Details
              </button>

            </div>
          ))}

        </div>

      </div>

    </div>
  );
}
function NetworkMap() {
  const [mapMode, setMapMode] = useState("Network Map");
  const [zone, setZone] = useState("All Zones");
  const [selectedNode, setSelectedNode] = useState("CAM-07");
  const [zoom, setZoom] = useState(1);

const handleZoomIn = () => {
  setZoom((value) => Math.min(value + 0.1, 1.5));
};

const handleZoomOut = () => {
  setZoom((value) => Math.max(value - 0.1, 0.7));
};

const handleResetZoom = () => {
  setZoom(1);
};

const handleFullscreen = () => {
  const mapElement = document.querySelector(".network-map-panel");

  if (!document.fullscreenElement) {
    mapElement?.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};

  const nodes = [
    {
      id: "SRV-DB-01",
      ip: "10.0.1.10",
      type: "Server",
      zone: "Data Center",
      icon: <Server size={18} />,
      status: "secure",
      x: 22,
      y: 19,
    },
    {
      id: "SRV-APP-02",
      ip: "10.0.1.11",
      type: "Server",
      zone: "Data Center",
      icon: <Monitor size={18} />,
      status: "secure",
      x: 50,
      y: 13,
    },
    {
      id: "CAM-07",
      ip: "10.0.3.25",
      type: "Camera",
      zone: "Office",
      icon: <Camera size={18} />,
      status: "critical",
      x: 13,
      y: 49,
    },
    {
      id: "IOT-22",
      ip: "10.0.3.45",
      type: "IoT Device",
      zone: "Office",
      icon: <Activity size={18} />,
      status: "warning",
      x: 13,
      y: 78,
    },
    {
      id: "PC-ADMIN-03",
      ip: "10.0.2.15",
      type: "Workstation",
      zone: "Office",
      icon: <Monitor size={18} />,
      status: "secure",
      x: 83,
      y: 49,
    },
    {
      id: "PRN-01",
      ip: "10.0.2.20",
      type: "Printer",
      zone: "Office",
      icon: <Printer size={18} />,
      status: "offline",
      x: 82,
      y: 78,
    },
    {
      id: "FW-01",
      ip: "10.0.1.1",
      type: "Firewall",
      zone: "Data Center",
      icon: <ShieldCheck size={18} />,
      status: "secure",
      x: 31,
      y: 89,
    },
    {
      id: "AP-01",
      ip: "10.0.2.5",
      type: "Access Point",
      zone: "Office",
      icon: <Wifi size={18} />,
      status: "secure",
      x: 64,
      y: 89,
    },
  ];

  const connections = [
    ["SRV-DB-01", "CORE-SW-01", "secure"],
    ["SRV-APP-02", "CORE-SW-01", "secure"],
    ["CAM-07", "CORE-SW-01", "critical"],
    ["IOT-22", "CORE-SW-01", "warning"],
    ["PC-ADMIN-03", "CORE-SW-01", "secure"],
    ["PRN-01", "CORE-SW-01", "offline"],
    ["FW-01", "CORE-SW-01", "secure"],
    ["AP-01", "CORE-SW-01", "secure"],
  ];

  const selected = nodes.find((node) => node.id === selectedNode);

  const visibleNodes =
    zone === "All Zones"
      ? nodes
      : nodes.filter((node) => node.zone === zone);

  const isAccessPath = mapMode === "Access Path";
  const isFlow = mapMode === "Communication Flow";

  const pathNodes = ["CAM-07", "CORE-SW-01", "SRV-APP-02"];

  return (
    <div className="network-map-page">

      {/* TOP */}
      <div className="network-map-top">
        <div>
          <h1>Relationships / Network Map</h1>
          <p>
            Visualize device relationships and network connections
          </p>
        </div>

        <div className="network-map-controls">
          <select
            value={zone}
            onChange={(e) => setZone(e.target.value)}
          >
            <option>All Zones</option>
            <option>Office</option>
            <option>Data Center</option>
          </select>
        <button
          className="map-expand"
          onClick={handleFullscreen}
        >
          ⛶
        </button>
        </div>
      </div>

      {/* TABS */}
      <div className="network-map-tabs">
        {[
          "Network Map",
          "Communication Flow",
          "Access Path",
        ].map((tab) => (
          <button
            key={tab}
            className={
              mapMode === tab
                ? "map-tab active"
                : "map-tab"
            }
            onClick={() => setMapMode(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* MAIN AREA */}
      <div className="network-map-layout">

        {/* MAP */}
        <div className="panel network-map-panel">

          <div 
            className={`network-map-canvas ${mapMode
            .toLowerCase()
            .replaceAll(" ", "-")}`}
          >

            {/* SVG CONNECTIONS */}
            <svg
              className="network-lines"
              viewBox="0 0 1000 600"
              preserveAspectRatio="none"
              style={{
                transform: `scale(${zoom})`,
                transformOrigin: "center center",
              }}  
            >

              <defs>
                <marker
                  id="flow-arrow"
                  viewBox="0 0 10 10"
                  refX="8"
                  refY="5"
                  markerWidth="5"
                  markerHeight="5"
                  orient="auto-start-reverse"
                >
                  <path
                    d="M 0 0 L 10 5 L 0 10 z"
                    fill="currentColor"
                  />
                </marker>
              </defs>

              {/* DB */}
              <line
                x1="500"
                y1="300"
                x2="220"
                y2="114"
                className={
                  isAccessPath
                    ? pathNodes.includes("SRV-DB-01")
                      ? "line-secure path-active"
                      : "line-dim"
                    : "line-secure"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* APP */}
              <line
                x1="500"
                y1="300"
                x2="500"
                y2="78"
                className={
                  isAccessPath
                    ? "line-secure path-active"
                    : "line-secure"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* CAMERA */}
              <line
                x1="500"
                y1="300"
                x2="130"
                y2="294"
                className={
                  isAccessPath
                    ? "line-critical path-active"
                    : "line-critical"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* IOT */}
              <line
                x1="500"
                y1="300"
                x2="130"
                y2="468"
                className={
                  isAccessPath
                    ? "line-warning line-dim"
                    : "line-warning"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* PC */}
              <line
                x1="500"
                y1="300"
                x2="830"
                y2="294"
                className={
                  isAccessPath
                    ? "line-secure line-dim"
                    : "line-secure"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* PRINTER */}
              <line
                x1="500"
                y1="300"
                x2="820"
                y2="468"
                className="line-offline line-dim"
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* FIREWALL */}
              <line
                x1="500"
                y1="300"
                x2="310"
                y2="534"
                className={
                  isAccessPath
                    ? "line-secure line-dim"
                    : "line-secure"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

              {/* ACCESS POINT */}
              <line
                x1="500"
                y1="300"
                x2="640"
                y2="534"
                className={
                  isAccessPath
                    ? "line-secure line-dim"
                    : "line-secure"
                }
                markerEnd={isFlow ? "url(#flow-arrow)" : undefined}
              />

            </svg>

            {/* CORE */}
            <div className="network-map-core">
              <Network size={25} />
              <strong>CORE-SW-01</strong>
              <span>10.0.0.1</span>
            </div>

            {/* DEVICES */}
            {visibleNodes.map((node) => {

              const dimmed =
                isAccessPath &&
                !pathNodes.includes(node.id);

              return (
                <button
                  key={node.id}
                  className={`map-node ${node.status}
                    ${selectedNode === node.id ? "selected" : ""}
                    ${dimmed ? "node-dim" : ""}
                  `}
                  style={{
                    left: `${node.x}%`,
                    top: `${node.y}%`,
                  }}
                  onClick={() => setSelectedNode(node.id)}
                >
                  <div className="map-node-icon">
                    {node.icon}
                  </div>

                  <strong>{node.id}</strong>
                  <span>{node.ip}</span>

                  <i></i>
                </button>
              );
            })}

            {/* COMMUNICATION FLOW INFO */}
            {isFlow && (
              <div className="flow-indicator">
                <span className="flow-live-dot"></span>
                LIVE TRAFFIC FLOW
              </div>
            )}

            {/* ACCESS PATH INFO */}
            {isAccessPath && (
              <div className="path-indicator">
                <span>PATH</span>
                CAM-07 → CORE-SW-01 → SRV-APP-02
              </div>
            )}

            {/* LEGEND */}
            <div className="network-map-legend">

              <span>
                <i className="legend-dot normal"></i>
                Normal
              </span>

              <span>
                <i className="legend-dot traffic"></i>
                High Traffic
              </span>

              <span>
                <i className="legend-dot suspicious"></i>
                Suspicious
              </span>

              <span>
                <i className="legend-dot blocked"></i>
                Blocked
              </span>

            </div>

            {/* ZOOM */}
            <div className="map-zoom-controls">
              <button onClick={handleZoomIn}>+</button>
              <button onClick={handleZoomOut}>−</button>
              <button onClick={handleResetZoom}>⟳</button>
            </div>

          </div>
        </div>

        {/* RIGHT CONNECTION DETAILS */}
        <div className="panel connection-details">

          <div className="panel-header">
            <h3>
              {isFlow
                ? "Communication Details"
                : isAccessPath
                ? "Access Path Details"
                : "Connection Details"}
            </h3>
          </div>

          {selected && (
            <div className="connection-content">

              <div className="connection-section">
                <span>Source</span>

                <div className="connection-device">
                  <div
                    className={`connection-icon ${selected.status}`}
                  >
                    {selected.icon}
                  </div>

                  <div>
                    <strong>{selected.id}</strong>
                    <small>{selected.ip}</small>
                  </div>
                </div>
              </div>

              <div className="connection-arrow">
                →
              </div>

              <div className="connection-section">
                <span>Destination</span>

                <div className="connection-device">
                  <div className="connection-icon core-small">
                    <Network size={17} />
                  </div>

                  <div>
                    <strong>CORE-SW-01</strong>
                    <small>10.0.0.1</small>
                  </div>
                </div>
              </div>

              {isFlow ? (
                <div className="connection-info-grid">

                  <div>
                    <span>Direction</span>
                    <strong>Outbound →</strong>
                  </div>

                  <div>
                    <span>Protocol</span>
                    <strong>TCP</strong>
                  </div>

                  <div>
                    <span>Traffic</span>
                    <strong>2.4 MB/s</strong>
                  </div>

                  <div>
                    <span>Packets</span>
                    <strong>1,284</strong>
                  </div>

                  <div>
                    <span>Last Seen</span>
                    <strong>10:24 AM</strong>
                  </div>

                  <div>
                    <span>Flow Status</span>
                    <strong className="secure">
                      Active
                    </strong>
                  </div>

                </div>
              ) : isAccessPath ? (
                <div className="access-path-details">

                  <div className="path-step active">
                    <span>1</span>
                    <div>
                      <strong>CAM-07</strong>
                      <small>Compromised device</small>
                    </div>
                  </div>

                  <div className="path-connector"></div>

                  <div className="path-step active">
                    <span>2</span>
                    <div>
                      <strong>CORE-SW-01</strong>
                      <small>Network switch</small>
                    </div>
                  </div>

                  <div className="path-connector"></div>

                  <div className="path-step active">
                    <span>3</span>
                    <div>
                      <strong>SRV-APP-02</strong>
                      <small>Potential target</small>
                    </div>
                  </div>

                </div>
              ) : (
                <div className="connection-info-grid">

                  <div>
                    <span>Protocol</span>
                    <strong>TCP</strong>
                  </div>

                  <div>
                    <span>Port</span>
                    <strong>443</strong>
                  </div>

                  <div>
                    <span>Traffic</span>
                    <strong>2.4 MB</strong>
                  </div>

                  <div>
                    <span>Last Seen</span>
                    <strong>10:24 AM</strong>
                  </div>

                </div>
              )}

              {!isAccessPath && (
                <div className="connection-status">
                  <span>Status</span>

                  <strong className={selected.status}>
                    {selected.status === "critical"
                      ? "Blocked"
                      : selected.status === "warning"
                      ? "Suspicious"
                      : selected.status === "offline"
                      ? "Offline"
                      : "Normal"}
                  </strong>
                </div>
              )}

              <button className="investigate-btn">
                Investigate
              </button>

            </div>
          )}

        </div>
      </div>
    </div>
  );
}
function RiskAnalysis() {
  const riskDevices = [
    {
      name: "CAM-07",
      type: "Camera",
      zone: "Office",
      risk: 78,
      level: "Critical",
    },
    {
      name: "IOT-22",
      type: "IoT Device",
      zone: "Office",
      risk: 65,
      level: "High",
    },
    {
      name: "SRV-APP-02",
      type: "Server",
      zone: "Data Center",
      risk: 42,
      level: "Medium",
    },
    {
      name: "PC-ADMIN-03",
      type: "Workstation",
      zone: "Office",
      risk: 25,
      level: "Low",
    },
  ];

  return (
    <>
      <header className="header">
        <div>
          <h1>Risk Analysis</h1>
          <p>Analyze infrastructure risk and security posture</p>
        </div>

        <div className="header-right">
          <div className="system-status">
            <span></span>
            <div>
              <small>Risk Status</small>
              <strong>Elevated</strong>
            </div>
          </div>
        </div>
      </header>

      <main className="risk-analysis-page">

        {/* TOP RISK SUMMARY */}

        <section className="risk-summary-grid">

          <div className="risk-summary-card">
            <div className="risk-summary-top">
              <span>Overall Risk Score</span>
              <BarChart3 size={19} />
            </div>

            <strong className="overall-risk-number">67</strong>

            <div className="risk-progress">
              <div style={{ width: "67%" }}></div>
            </div>

            <small>Elevated risk across infrastructure</small>
          </div>

          <div className="risk-summary-card">
            <div className="risk-summary-top">
              <span>Critical Risks</span>
              <AlertTriangle size={19} />
            </div>

            <strong className="critical-number">2</strong>
            <small>Require immediate attention</small>
          </div>

          <div className="risk-summary-card">
            <div className="risk-summary-top">
              <span>High Risk Devices</span>
              <Monitor size={19} />
            </div>

            <strong className="high-number">4</strong>
            <small>Devices above risk threshold</small>
          </div>

          <div className="risk-summary-card">
            <div className="risk-summary-top">
              <span>Security Health</span>
              <Shield size={19} />
            </div>

            <strong className="health-number">87%</strong>
            <small>Overall infrastructure health</small>
          </div>

        </section>

        {/* MAIN ANALYSIS */}

        <section className="risk-analysis-grid">

          {/* RISK DISTRIBUTION */}

          <div className="panel risk-distribution-panel">

            <div className="panel-header">
              <div>
                <h3>Risk Distribution</h3>
                <p>Current risk levels across your infrastructure</p>
              </div>
            </div>

            <div className="risk-distribution">

              <div className="risk-ring">
                <div>
                  <strong>67</strong>
                  <span>Risk Score</span>
                </div>
              </div>

              <div className="risk-level-list">

                <div>
                  <span>
                    <i className="risk-dot critical"></i>
                    Critical
                  </span>
                  <strong>2</strong>
                </div>

                <div>
                  <span>
                    <i className="risk-dot high"></i>
                    High
                  </span>
                  <strong>4</strong>
                </div>

                <div>
                  <span>
                    <i className="risk-dot medium"></i>
                    Medium
                  </span>
                  <strong>7</strong>
                </div>

                <div>
                  <span>
                    <i className="risk-dot low"></i>
                    Low
                  </span>
                  <strong>114</strong>
                </div>

              </div>

            </div>
          </div>

          {/* RISK FACTORS */}

          <div className="panel risk-factors-panel">

            <div className="panel-header">
              <div>
                <h3>Risk Factors</h3>
                <p>Primary contributors to current risk</p>
              </div>
            </div>

            <div className="risk-factor-list">

              <div>
                <span>Malware Detection</span>
                <strong>High</strong>
              </div>

              <div>
                <span>Unauthorized Access</span>
                <strong>High</strong>
              </div>

              <div>
                <span>Network Anomalies</span>
                <strong>Medium</strong>
              </div>

              <div>
                <span>Policy Violations</span>
                <strong>Low</strong>
              </div>

            </div>
          </div>

        </section>

        {/* TOP RISK DEVICES */}

        <section className="panel top-risk-panel">

          <div className="panel-header">
            <div>
              <h3>Top Risk Devices</h3>
              <p>Devices requiring the most attention</p>
            </div>
          </div>

          <div className="risk-device-list">

            {riskDevices.map((device) => (
              <div className="risk-device-row" key={device.name}>

                <div className="risk-device-icon">
                  <Monitor size={17} />
                </div>

                <div className="risk-device-name">
                  <strong>{device.name}</strong>
                  <span>
                    {device.type} · {device.zone}
                  </span>
                </div>

                <div className="risk-device-score">
                  <strong>{device.risk}</strong>
                  <span>Risk</span>
                </div>

                <div className={`risk-level ${device.level.toLowerCase()}`}>
                  {device.level}
                </div>

                <button className="risk-view-btn">
                  View
                </button>

              </div>
            ))}

          </div>

        </section>

      </main>
    </>
  );
}
function ResponseCenter() {
  const [activeAction, setActiveAction] = useState(null);

  const handleAction = (action) => {
    setActiveAction(action);
  };

  return (
    <>
      <header className="header">
        <div>
          <h1>Response Center</h1>
          <p>Manage incidents and coordinate security response</p>
        </div>

        <div className="header-right">
          <button className="response-take-action">
            Take Action
          </button>
        </div>
      </header>

      <main className="response-page">

        {/* INCIDENT HEADER */}

        <div className="incident-heading">
          <div>
            <span className="incident-label">INCIDENT</span>
            <strong>INC-2025-0523-001</strong>
            <span className="incident-active">Active</span>
          </div>

          <span className="incident-time">
            May 23, 2025 · 10:24 AM
          </span>
        </div>

        {/* MAIN GRID */}

        <section className="response-main-grid">

          {/* INCIDENT SUMMARY */}

          <div className="panel response-summary">

            <div className="panel-header">
              <div>
                <h3>Incident Summary</h3>
                <p>Overview of the detected security incident</p>
              </div>
            </div>

            <div className="incident-details">

              <div>
                <span>Incident ID</span>
                <strong>INC-2025-0523-001</strong>
              </div>

              <div>
                <span>Detected</span>
                <strong>May 23, 2025 10:24 AM</strong>
              </div>

              <div>
                <span>Severity</span>
                <strong className="critical-text">Critical</strong>
              </div>

              <div>
                <span>Status</span>
                <strong className="active-text">Active</strong>
              </div>

              <div>
                <span>Affected Device</span>
                <strong>CAM-07 (10.0.3.25)</strong>
              </div>

              <div>
                <span>Incident Type</span>
                <strong>Malware Infection</strong>
              </div>

              <div className="incident-description">
                <span>Description</span>
                <p>
                  Malware detected on CAM-07 with suspicious
                  outbound communication and command-and-control
                  activity.
                </p>
              </div>

            </div>
          </div>

          {/* INCIDENT TIMELINE */}

          <div className="panel response-timeline">

            <div className="panel-header">
              <div>
                <h3>Incident Timeline</h3>
                <p>Security events leading to this incident</p>
              </div>
            </div>

            <div className="timeline">

              <div className="timeline-item">
                <div className="timeline-dot critical"></div>

                <div>
                  <strong>Malware detected</strong>
                  <span>10:24 AM</span>
                  <p>Trojan.Win32 detected on CAM-07</p>
                </div>
              </div>

              <div className="timeline-item">
                <div className="timeline-dot critical"></div>

                <div>
                  <strong>Outbound connection detected</strong>
                  <span>10:20 AM</span>
                  <p>Connection to suspicious external IP</p>
                </div>
              </div>

              <div className="timeline-item">
                <div className="timeline-dot high"></div>

                <div>
                  <strong>Multiple failed login attempts</strong>
                  <span>10:15 AM</span>
                  <p>Authentication anomalies detected</p>
                </div>
              </div>

              <div className="timeline-item">
                <div className="timeline-dot medium"></div>

                <div>
                  <strong>Policy violation detected</strong>
                  <span>10:10 AM</span>
                  <p>Device communication policy violation</p>
                </div>
              </div>

              <div className="timeline-item">
                <div className="timeline-dot low"></div>

                <div>
                  <strong>Device came online</strong>
                  <span>10:04 AM</span>
                  <p>CAM-07 connected to the network</p>
                </div>
              </div>

            </div>
          </div>

        </section>

        {/* RESPONSE ACTIONS */}

        <section className="panel response-actions-panel">

          <div className="panel-header">
            <div>
              <h3>Response Actions</h3>
              <p>Recommended actions for this incident</p>
            </div>
          </div>

          <div className="response-actions">

            <div className="response-action">
              <div className="action-number">1</div>

              <div className="action-content">
                <strong>Verify</strong>
                <span>
                  Validate the alert and collect supporting evidence
                </span>
              </div>

              <button
                onClick={() => handleAction("Verify")}
                className={activeAction === "Verify" ? "action-done" : ""}
              >
                {activeAction === "Verify" ? "Verified" : "Verify"}
              </button>
            </div>

            <div className="response-action">
              <div className="action-number">2</div>

              <div className="action-content">
                <strong>Isolate</strong>
                <span>
                  Isolate the affected device from the network
                </span>
              </div>

              <button
                onClick={() => handleAction("Isolate")}
                className={activeAction === "Isolate" ? "action-done" : ""}
              >
                {activeAction === "Isolate" ? "Isolated" : "Isolate"}
              </button>
            </div>

            <div className="response-action">
              <div className="action-number">3</div>

              <div className="action-content">
                <strong>Preserve</strong>
                <span>
                  Preserve logs and forensic evidence
                </span>
              </div>

              <button
                onClick={() => handleAction("Preserve")}
                className={activeAction === "Preserve" ? "action-done" : ""}
              >
                {activeAction === "Preserve" ? "Preserved" : "Preserve"}
              </button>
            </div>

            <div className="response-action">
              <div className="action-number">4</div>

              <div className="action-content">
                <strong>Recover</strong>
                <span>
                  Clean and restore the affected device
                </span>
              </div>

              <button
                onClick={() => handleAction("Recover")}
                className={activeAction === "Recover" ? "action-done" : ""}
              >
                {activeAction === "Recover" ? "Recovered" : "Recover"}
              </button>
            </div>

          </div>
        </section>

        {/* BOTTOM SECTION */}

        <section className="response-bottom-grid">

          {/* EVIDENCE */}

          <div className="panel evidence-panel">

            <div className="panel-header">
              <div>
                <h3>Evidence & Artifacts</h3>
                <p>Collected evidence related to this incident</p>
              </div>
            </div>

            <div className="evidence-list">

              <div className="evidence-item">
                <div>
                  <strong>Malware Sample</strong>
                  <span>Trojan.Win32.exe</span>
                  <small>10:24 AM</small>
                </div>
                <button>Download</button>
              </div>

              <div className="evidence-item">
                <div>
                  <strong>Traffic Capture</strong>
                  <span>capture.pcap</span>
                  <small>10:24 AM</small>
                </div>
                <button>Download</button>
              </div>

              <div className="evidence-item">
                <div>
                  <strong>System Logs</strong>
                  <span>system.log</span>
                  <small>10:24 AM</small>
                </div>
                <button>Download</button>
              </div>

            </div>
          </div>

          {/* NOTES */}

          <div className="panel notes-panel">

            <div className="panel-header">
              <div>
                <h3>Notes</h3>
                <p>Investigation notes and observations</p>
              </div>
            </div>

            <textarea
              placeholder="Add investigation notes..."
            />

            <button className="add-note">
              Add Note
            </button>

          </div>

        </section>

      </main>
    </>
  );
}
function Reports() {
  const [reportType, setReportType] = useState("Security Summary");

  const reportData = {
    "Security Summary": {
      incidents: "24",
      incidentsLabel: "Last 7 days",
      threats: "28",
      threatsLabel: "5 critical",
      devices: "127",
      devicesLabel: "112 online",
      health: "87%",
      healthLabel: "Overall posture",
      risk: "67",
      critical: "2",
      highRisk: "4",
      resolved: "24",
      violations: "3",
      status: "Elevated",

      overviewTitle: "Security Overview",
      overviewSubtitle: "Infrastructure security posture",

      threatData: [
        { name: "Malware", value: 40 },
        { name: "Unauthorized Access", value: 20 },
        { name: "Anomalous Behavior", value: 20 },
        { name: "Policy Violation", value: 20 },
      ],
    },

    "Threat Report": {
      incidents: "18",
      incidentsLabel: "Threat-related incidents",
      threats: "28",
      threatsLabel: "5 critical",
      devices: "34",
      devicesLabel: "Affected devices",
      health: "72%",
      healthLabel: "Threat posture",
      risk: "74",
      critical: "5",
      highRisk: "7",
      resolved: "19",
      violations: "6",
      status: "High Risk",

      overviewTitle: "Threat Overview",
      overviewSubtitle: "Detected security threats",

      threatData: [
        { name: "Malware", value: 45 },
        { name: "Unauthorized Access", value: 30 },
        { name: "Anomalous Behavior", value: 15 },
        { name: "Policy Violation", value: 10 },
      ],
    },

    "Device Report": {
      incidents: "12",
      incidentsLabel: "Device incidents",
      threats: "9",
      threatsLabel: "2 critical",
      devices: "127",
      devicesLabel: "112 online",
      health: "87%",
      healthLabel: "Device health",
      risk: "61",
      critical: "2",
      highRisk: "4",
      resolved: "21",
      violations: "3",
      status: "Elevated",

      overviewTitle: "Device Security Overview",
      overviewSubtitle: "Infrastructure device posture",

      threatData: [
        { name: "Compromised Devices", value: 35 },
        { name: "Outdated Software", value: 25 },
        { name: "Unauthorized Access", value: 20 },
        { name: "Policy Violation", value: 20 },
      ],
    },

    "Incident Report": {
      incidents: "24",
      incidentsLabel: "Total incidents",
      threats: "16",
      threatsLabel: "Related threats",
      devices: "42",
      devicesLabel: "Affected devices",
      health: "81%",
      healthLabel: "Incident posture",
      risk: "69",
      critical: "3",
      highRisk: "5",
      resolved: "24",
      violations: "4",
      status: "Elevated",

      overviewTitle: "Incident Overview",
      overviewSubtitle: "Security incidents and response",

      threatData: [
        { name: "Active Incidents", value: 35 },
        { name: "Resolved Incidents", value: 30 },
        { name: "Critical Incidents", value: 20 },
        { name: "Policy Incidents", value: 15 },
      ],
    },

    "Network Report": {
      incidents: "8",
      incidentsLabel: "Network incidents",
      threats: "11",
      threatsLabel: "Network threats",
      devices: "127",
      devicesLabel: "Connected devices",
      health: "84%",
      healthLabel: "Network health",
      risk: "63",
      critical: "2",
      highRisk: "4",
      resolved: "20",
      violations: "3",
      status: "Elevated",

      overviewTitle: "Network Security Overview",
      overviewSubtitle: "Network infrastructure posture",

      threatData: [
        { name: "Suspicious Traffic", value: 40 },
        { name: "Unauthorized Access", value: 25 },
        { name: "Port Scanning", value: 20 },
        { name: "Policy Violation", value: 15 },
      ],
    },
  };

  const currentReport = reportData[reportType];

  return (
    <>
      {/* HEADER */}

      <header className="header">
        <div>
          <h1>Reports</h1>
          <p>Generate and review security reports</p>
        </div>

        <div className="header-right">
          <button className="report-generate-btn">
            Generate Report
          </button>
        </div>
      </header>

      <main className="reports-page">

        {/* REPORT CONTROLS */}

        <section className="report-controls panel">

          <div className="report-control-group">
            <label>Report Type</label>

            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
            >
              <option>Security Summary</option>
              <option>Threat Report</option>
              <option>Device Report</option>
              <option>Incident Report</option>
              <option>Network Report</option>
            </select>
          </div>

          <div className="report-control-group">
            <label>Date Range</label>

            <select defaultValue="Last 7 Days">
              <option>Last 24 Hours</option>
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Custom Range</option>
            </select>
          </div>

          <button className="report-export-btn">
            Export PDF
          </button>

        </section>


        {/* REPORT SUMMARY CARDS */}

        <section className="report-summary-grid">

          <div className="report-stat-card">
            <span>Total Incidents</span>

            <strong>
              {currentReport.incidents}
            </strong>

            <small>
              {currentReport.incidentsLabel}
            </small>
          </div>


          <div className="report-stat-card">
            <span>Threats Detected</span>

            <strong className="report-danger">
              {currentReport.threats}
            </strong>

            <small>
              {currentReport.threatsLabel}
            </small>
          </div>


          <div className="report-stat-card">
            <span>Devices Monitored</span>

            <strong>
              {currentReport.devices}
            </strong>

            <small>
              {currentReport.devicesLabel}
            </small>
          </div>


          <div className="report-stat-card">
            <span>Security Health</span>

            <strong className="report-success">
              {currentReport.health}
            </strong>

            <small>
              {currentReport.healthLabel}
            </small>
          </div>

        </section>


        {/* MAIN REPORT */}

        <section className="report-main-grid">

          {/* SECURITY / REPORT OVERVIEW */}

          <div className="panel report-overview">

            <div className="panel-header">

              <div>
                <h3>
                  {currentReport.overviewTitle}
                </h3>

                <p>
                  {currentReport.overviewSubtitle}
                </p>
              </div>

              <span className="report-status">
                {currentReport.status}
              </span>

            </div>


            <div className="report-overview-content">

              {/* RISK SCORE */}

              <div className="report-score">

                <div className="report-score-circle">

                  <strong>
                    {currentReport.risk}
                  </strong>

                  <span>
                    Risk Score
                  </span>

                </div>

              </div>


              {/* REPORT METRICS */}

              <div className="report-metrics">

                <div>
                  <span>Critical Risks</span>

                  <strong className="report-danger">
                    {currentReport.critical}
                  </strong>
                </div>


                <div>
                  <span>High Risk Devices</span>

                  <strong className="report-warning">
                    {currentReport.highRisk}
                  </strong>
                </div>


                <div>
                  <span>Resolved Incidents</span>

                  <strong className="report-success">
                    {currentReport.resolved}
                  </strong>
                </div>


                <div>
                  <span>Policy Violations</span>

                  <strong>
                    {currentReport.violations}
                  </strong>
                </div>

              </div>

            </div>

          </div>


          {/* THREAT SUMMARY */}

          <div className="panel threat-summary">

            <div className="panel-header">

              <div>
                <h3>
                  Threat Summary
                </h3>

                <p>
                  Detected threats by category
                </p>
              </div>

            </div>


            <div className="threat-bars">

              {currentReport.threatData.map((threat, index) => (
                <div
                  className="threat-bar-row"
                  key={index}
                >

                  <div>
                    <span>
                      {threat.name}
                    </span>

                    <strong>
                      {threat.value}%
                    </strong>
                  </div>


                  <div className="threat-bar">

                    <span
                      style={{
                        width: `${threat.value}%`,
                      }}
                    ></span>

                  </div>

                </div>
              ))}

            </div>

          </div>

        </section>


        {/* RECENT REPORTS */}

        <section className="panel recent-reports">

          <div className="panel-header">

            <div>
              <h3>
                Recent Reports
              </h3>

              <p>
                Previously generated security reports
              </p>
            </div>

          </div>


          <div className="reports-table">

            {/* TABLE HEADER */}

            <div className="report-table-header">

              <span>
                Report Name
              </span>

              <span>
                Type
              </span>

              <span>
                Generated
              </span>

              <span>
                Status
              </span>

              <span>
                Action
              </span>

            </div>


            {/* REPORT 1 */}

            <div className="report-table-row">

              <strong>
                Weekly Security Summary
              </strong>

              <span>
                Security Summary
              </span>

              <span>
                May 23, 2025
              </span>

              <span className="report-complete">
                Completed
              </span>

              <button>
                View
              </button>

            </div>


            {/* REPORT 2 */}

            <div className="report-table-row">

              <strong>
                Threat Detection Report
              </strong>

              <span>
                Threat Report
              </span>

              <span>
                May 22, 2025
              </span>

              <span className="report-complete">
                Completed
              </span>

              <button>
                View
              </button>

            </div>


            {/* REPORT 3 */}

            <div className="report-table-row">

              <strong>
                Network Security Report
              </strong>

              <span>
                Network Report
              </span>

              <span>
                May 20, 2025
              </span>

              <span className="report-complete">
                Completed
              </span>

              <button>
                View
              </button>

            </div>


            {/* REPORT 4 */}

            <div className="report-table-row">

              <strong>
                Incident Response Report
              </strong>

              <span>
                Incident Report
              </span>

              <span>
                May 18, 2025
              </span>

              <span className="report-complete">
                Completed
              </span>

              <button>
                View
              </button>

            </div>

          </div>

        </section>

      </main>
    </>
  );
}
function SentinelSettings() {
  const [notifications, setNotifications] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [threatAlerts, setThreatAlerts] = useState(true);

  return (
    <>
      <header className="header">
        <div>
          <h1>Settings</h1>
          <p>Configure SENTINEL security and system preferences</p>
        </div>
      </header>

      <main className="settings-page">

        {/* GENERAL SETTINGS */}
        <section className="panel settings-section">
          <div className="panel-header">
            <div>
              <h3>General Settings</h3>
              <p>Configure general system preferences</p>
            </div>
          </div>

          <div className="settings-list">

            <div className="setting-row">
              <div>
                <strong>System Name</strong>
                <span>Display name for this SENTINEL instance</span>
              </div>

              <input
                type="text"
                defaultValue="SENTINEL Security"
              />
            </div>

            <div className="setting-row">
              <div>
                <strong>Auto Refresh</strong>
                <span>Automatically refresh security data</span>
              </div>

              <button
                type="button"
                className={`toggle ${autoRefresh ? "on" : ""}`}
                onClick={() => setAutoRefresh(!autoRefresh)}
              >
                <span></span>
              </button>
            </div>

          </div>
        </section>


        {/* NOTIFICATIONS */}
        <section className="panel settings-section">
          <div className="panel-header">
            <div>
              <h3>Notifications</h3>
              <p>Manage security notifications and alerts</p>
            </div>
          </div>

          <div className="settings-list">

            <div className="setting-row">
              <div>
                <strong>Enable Notifications</strong>
                <span>Receive SENTINEL security notifications</span>
              </div>

              <button
                type="button"
                className={`toggle ${notifications ? "on" : ""}`}
                onClick={() => setNotifications(!notifications)}
              >
                <span></span>
              </button>
            </div>

            <div className="setting-row">
              <div>
                <strong>Threat Alerts</strong>
                <span>Receive alerts when threats are detected</span>
              </div>

              <button
                type="button"
                className={`toggle ${threatAlerts ? "on" : ""}`}
                onClick={() => setThreatAlerts(!threatAlerts)}
              >
                <span></span>
              </button>
            </div>

          </div>
        </section>


        {/* SECURITY & MONITORING */}
        <section className="panel settings-section">
          <div className="panel-header">
            <div>
              <h3>Security &amp; Monitoring</h3>
              <p>Configure security monitoring preferences</p>
            </div>
          </div>

          <div className="settings-list">

            <div className="setting-row">
              <div>
                <strong>Threat Monitoring</strong>
                <span>Continuously monitor network activity</span>
              </div>

              <span className="setting-status active">
                Active
              </span>
            </div>

            <div className="setting-row">
              <div>
                <strong>Intrusion Detection</strong>
                <span>Detect suspicious network behaviour</span>
              </div>

              <span className="setting-status active">
                Enabled
              </span>
            </div>

            <div className="setting-row">
              <div>
                <strong>Log Retention</strong>
                <span>Duration for retaining security logs</span>
              </div>

              <select defaultValue="30 Days">
                <option>7 Days</option>
                <option>30 Days</option>
                <option>90 Days</option>
                <option>1 Year</option>
              </select>
            </div>

          </div>
        </section>


        {/* NETWORK CONFIGURATION */}
        <section className="panel settings-section">
          <div className="panel-header">
            <div>
              <h3>Network Configuration</h3>
              <p>Configure network monitoring parameters</p>
            </div>
          </div>

          <div className="settings-list">

            <div className="setting-row">
              <div>
                <strong>Monitoring Interface</strong>
                <span>Network interface used by SENTINEL</span>
              </div>

              <select defaultValue="eth0">
                <option>eth0</option>
                <option>wlan0</option>
                <option>Ethernet</option>
              </select>
            </div>

            <div className="setting-row">
              <div>
                <strong>Monitoring Mode</strong>
                <span>Current network monitoring mode</span>
              </div>

              <span className="setting-status active">
                Active
              </span>
            </div>

          </div>
        </section>


        {/* SAVE CHANGES */}
        <div className="settings-footer">
          <button
            type="button"
            className="settings-save-btn"
          >
            Save Changes
          </button>
        </div>

      </main>
    </>
  );
}
function App() {
  const [active, setActive] = useState("Dashboard");

  return (
    <div className="app">
      <Sidebar active={active} setActive={setActive} />
    <div className="content">
      {active === "Dashboard" ? (
        <Dashboard />
      ) : active === "Devices" ? (
        <Devices />
      ) : active === "Threats & Alerts"? (
        <ThreatsAlerts />
      ) : active === "Network Map" ? (
        <NetworkMap />  
      ) : active === "Risk Analysis" ? (
        <RiskAnalysis />
      )  : active === "Response Center" ? (
        <ResponseCenter />
      ) : active === "Reports" ? (
        <Reports /> 
      ) : active === "Settings" ? (
        <SentinelSettings />  
      ) : null}
    </div>      
   </div>
  );
}
export default App;