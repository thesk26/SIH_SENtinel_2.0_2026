import { useState,useEffect } from "react";
import {
  Shield,
  LayoutDashboard,
  Monitor,
  AlertTriangle,
  Network,
  BarChart3,
  ShieldCheck,
  Lock,
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
  X,
  Menu,
  Sun,
  UserCircle,
  LogOut,
  Download,
  CheckCircle2 as CheckIcon,

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
    status: "Active",
    source: "Endpoint telemetry",
    description: "Malware activity was detected on the endpoint. SENTINEL recommends isolating the device and running a full security scan.",
    recommendation: "Isolate CAM-07 and start a full malware scan.",
  },
  {
    title: "Unauthorized Access Attempt",
    device: "SRV-APP-02",
    severity: "High",
    color: "orange",
    time: "Today, 09:15 AM",
    status: "Active",
    source: "Authentication logs",
    description: "Multiple failed login attempts were detected from an unusual source against the application server.",
    recommendation: "Review authentication logs and verify the source IP.",
  },
  {
    title: "Anomalous Behavior",
    device: "IOT-22",
    severity: "High",
    color: "purple",
    time: "Today, 08:45 AM",
    status: "Investigating",
    source: "Network telemetry",
    description: "Traffic patterns for this IoT device differ from its learned baseline and require investigation.",
    recommendation: "Inspect recent connections and compare the device against its normal traffic profile.",
  },
  {
    title: "Policy Violation",
    device: "PC-ADMIN-03",
    severity: "Medium",
    color: "orange",
    time: "Today, 07:30 AM",
    status: "Resolved",
    source: "Endpoint policy engine",
    description: "A USB policy violation was detected. The policy event has been reviewed and resolved.",
    recommendation: "Keep the current endpoint policy and monitor for recurrence.",
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

function SecurityEvents({ onViewAll }) {
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

      <button type="button" className="view-events" onClick={onViewAll}>
        View All Events <ArrowUpRight size={14} />
      </button>
    </div>
  );
}

function AIRecommendation({ onTakeAction }) {
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

        <button type="button" onClick={onTakeAction}>Take Action</button>
      </div>
    </div>
  );
}

function Devices() {
  const [deviceList, setDeviceList] = useState(devices);
  const [selectedDevice, setSelectedDevice] = useState(devices[0]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All Devices");
  const [statusFilter, setStatusFilter] = useState("All Status");
  const [zoneFilter, setZoneFilter] = useState("All Zones");
  const [showAddDevice, setShowAddDevice] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [actionDevice, setActionDevice] = useState(null);
  const [menuDevice, setMenuDevice] = useState(null);
  const [notice, setNotice] = useState("");
  const [newDevice, setNewDevice] = useState({
    name: "",
    ip: "",
    type: "Workstation",
    zone: "Office",
  });

  const categories = [
    ["All Devices", 127 + Math.max(0, deviceList.length - devices.length)],
    ["Servers", 18],
    ["Workstations", 32],
    ["Network", 24],
    ["IoT", 28],
    ["Others", 25],
  ];

  const showNotice = (message) => {
    setNotice(message);
    window.setTimeout(() => setNotice(""), 2600);
  };

  const filteredDevices = deviceList.filter((device) => {
    const query = search.toLowerCase();
    const matchesSearch =
      device.name.toLowerCase().includes(query) ||
      device.ip.toLowerCase().includes(query);

    let matchesCategory = true;
    if (category === "Servers") matchesCategory = device.type === "Server";
    else if (category === "Workstations") matchesCategory = device.type === "Workstation";
    else if (category === "IoT") matchesCategory = device.type === "IoT Device";
    else if (category === "Network") {
      matchesCategory = device.type === "Firewall" || device.type === "Access Point";
    } else if (category === "Others") {
      matchesCategory = !["Server", "Workstation", "IoT Device", "Firewall", "Access Point"].includes(device.type);
    }

    const matchesStatus = statusFilter === "All Status" || device.status === statusFilter;
    const matchesZone = zoneFilter === "All Zones" || device.zone === zoneFilter;
    return matchesSearch && matchesCategory && matchesStatus && matchesZone;
  });

  useEffect(() => {
    if (filteredDevices.length > 0 && !filteredDevices.some((device) => device.name === selectedDevice?.name)) {
      setSelectedDevice(filteredDevices[0]);
    }
  }, [category, statusFilter, zoneFilter, search, deviceList]);

  const addDevice = (e) => {
    e.preventDefault();
    const name = newDevice.name.trim();
    const ip = newDevice.ip.trim();
    if (!name || !ip) return;
    if (deviceList.some((device) => device.name.toLowerCase() === name.toLowerCase())) {
      showNotice("A device with this name already exists.");
      return;
    }

    const created = {
      ...newDevice,
      name,
      ip,
      status: "Online",
      risk: 8,
      lastSeen: "Just now",
      vendor: "SENTINEL Demo",
      uptime: "0d 0h 1m",
      reason: "Newly enrolled device. No active security findings.",
    };
    setDeviceList((current) => [created, ...current]);
    setSelectedDevice(created);
    setShowAddDevice(false);
    setNewDevice({ name: "", ip: "", type: "Workstation", zone: "Office" });
    showNotice(`${name} was added successfully.`);
  };

  const runDeviceAction = (action, device) => {
    setActionDevice(null);
    setMenuDevice(null);
    const messages = {
      scan: `Security scan started for ${device.name}.`,
      isolate: `${device.name} has been queued for isolation.`,
      trust: `${device.name} has been marked as trusted for this demo.`,
      ping: `Ping request sent to ${device.name}.`,
      remove: `${device.name} removal request has been queued.`,
    };
    showNotice(messages[action] || `Action completed for ${device.name}.`);
  };

  return (
    <div className="devices-page">
      <div className="devices-top">
        <div>
          <h1>Devices</h1>
          <p>Monitor and manage all connected devices</p>
        </div>

        <button className="add-device" onClick={() => setShowAddDevice(true)}>
          <Plus size={16} />
          Add Device
        </button>
      </div>

      <div className="devices-tabs">
        {categories.map(([name, count]) => (
          <button key={name} className={category === name ? "device-tab active" : "device-tab"} onClick={() => setCategory(name)}>
            {name} <span>{count}</span>
          </button>
        ))}
      </div>

      <div className="devices-filters">
        <div className="device-search">
          <Search size={15} />
          <input type="text" placeholder="Search devices..." value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>

        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option>All Status</option>
          <option>Online</option>
          <option>At Risk</option>
          <option>Offline</option>
        </select>

        <select value={zoneFilter} onChange={(e) => setZoneFilter(e.target.value)}>
          <option>All Zones</option>
          <option>Office</option>
          <option>Data Center</option>
        </select>
      </div>

      <div className="panel devices-table-panel">
        <table className="devices-table">
          <thead>
            <tr>
              <th>DEVICE NAME</th><th>IP ADDRESS</th><th>TYPE</th><th>ZONE</th><th>STATUS</th><th>RISK SCORE</th><th>LAST SEEN</th><th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {filteredDevices.map((device) => (
              <tr key={device.name} className={selectedDevice?.name === device.name ? "device-row-selected" : ""} onClick={() => setSelectedDevice(device)}>
                <td className="device-name">{device.name}</td>
                <td>{device.ip}</td>
                <td>{device.type}</td>
                <td>{device.zone}</td>
                <td>
                  <span className={`device-status ${device.status === "Online" ? "online" : device.status === "At Risk" ? "at-risk" : "offline"}`}><i></i>{device.status}</span>
                </td>
                <td><span className={`risk-score ${device.risk >= 70 ? "high-risk" : device.risk >= 30 ? "medium-risk" : "low-risk"}`}>{device.risk ?? "-"}</span></td>
                <td>{device.lastSeen}</td>
                <td>
                  <div className="device-actions" onClick={(e) => e.stopPropagation()}>
                    <button title="View device details" onClick={() => { setSelectedDevice(device); setShowDetails(true); }}><Eye size={14} /></button>
                    <button title="Device actions" onClick={() => { setSelectedDevice(device); setActionDevice(device); setMenuDevice(null); }}><SlidersHorizontal size={14} /></button>
                    <button title="More actions" onClick={() => { setSelectedDevice(device); setMenuDevice(menuDevice?.name === device.name ? null : device); }}><MoreHorizontal size={15} /></button>
                  </div>
                  {menuDevice?.name === device.name && (
                    <div className="device-more-menu">
                      <button onClick={() => runDeviceAction("ping", device)}><Wifi size={13} /> Ping Device</button>
                      <button onClick={() => runDeviceAction("trust", device)}><ShieldCheck size={13} /> Mark Trusted</button>
                      <button className="danger" onClick={() => runDeviceAction("remove", device)}><AlertTriangle size={13} /> Remove Device</button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredDevices.length === 0 && <div className="devices-empty">No devices match the selected filters.</div>}
      </div>

      <div className="device-detail-grid">
        <div className="panel selected-device">
          <div className="selected-device-top">
            <div className="camera-preview"><Camera size={38} /></div>
            <div className="selected-device-info">
              <div className="selected-title">
                <h3>{selectedDevice?.name}</h3>
                <span className={`device-status ${selectedDevice?.status === "Online" ? "online" : selectedDevice?.status === "At Risk" ? "at-risk" : "offline"}`}><i></i>{selectedDevice?.status}</span>
              </div>
              <div className="device-details">
                <div><span>IP Address</span><strong>{selectedDevice?.ip}</strong></div>
                <div><span>Type</span><strong>{selectedDevice?.type}</strong></div>
                <div><span>Zone</span><strong>{selectedDevice?.zone}</strong></div>
                <div><span>Risk Score</span><strong className={`detail-risk ${selectedDevice?.risk < 30 ? "detail-risk-safe" : ""}`}>{selectedDevice?.risk ?? "-"}</strong></div>
              </div>
              <div className="device-details second-row">
                <div><span>Vendor</span><strong>{selectedDevice?.vendor || "Hikvision"}</strong></div>
                <div><span>Last Seen</span><strong>{selectedDevice?.lastSeen}</strong></div>
                <div><span>Uptime</span><strong>{selectedDevice?.uptime || "120d 4h 32m"}</strong></div>
              </div>
            </div>
          </div>
          <div className="risk-reason"><strong>Reason:</strong> {selectedDevice?.reason || (selectedDevice?.status === "At Risk" ? "Malware detected and unauthorized outbound connections." : "No active security findings.")}</div>
        </div>

        <div className="panel recent-activity">
          <div className="panel-header"><h3>Recent Activity</h3></div>
          <div className="activity-list">
            <div><i className="activity-dot red"></i><span>Malware detected (Trojan.Win32)</span><time>10:34 AM</time></div>
            <div><i className="activity-dot red"></i><span>Unauthorized outbound connection</span><time>10:20 AM</time></div>
            <div><i className="activity-dot orange"></i><span>Multiple failed login attempts</span><time>10:15 AM</time></div>
          </div>
          <button className="view-full-details" onClick={() => setShowDetails(true)}>View Full Details</button>
        </div>
      </div>

      {notice && <div className="devices-toast"><CheckCircle2 size={16} />{notice}</div>}

      {showAddDevice && (
        <div className="device-modal-backdrop" onClick={() => setShowAddDevice(false)}>
          <form className="device-modal" onSubmit={addDevice} onClick={(e) => e.stopPropagation()}>
            <div className="device-modal-header"><div><h3>Add Device</h3><p>Enroll a new device in SENTINEL</p></div><button type="button" onClick={() => setShowAddDevice(false)}><X size={18} /></button></div>
            <label>Device Name<input autoFocus value={newDevice.name} onChange={(e) => setNewDevice({ ...newDevice, name: e.target.value })} placeholder="e.g. LAPTOP-DEV-04" /></label>
            <label>IP Address<input value={newDevice.ip} onChange={(e) => setNewDevice({ ...newDevice, ip: e.target.value })} placeholder="e.g. 10.0.2.44" /></label>
            <div className="device-form-grid">
              <label>Type<select value={newDevice.type} onChange={(e) => setNewDevice({ ...newDevice, type: e.target.value })}><option>Server</option><option>Workstation</option><option>IoT Device</option><option>Camera</option><option>Firewall</option><option>Access Point</option><option>Printer</option></select></label>
              <label>Zone<select value={newDevice.zone} onChange={(e) => setNewDevice({ ...newDevice, zone: e.target.value })}><option>Office</option><option>Data Center</option></select></label>
            </div>
            <div className="device-modal-actions"><button type="button" className="device-cancel" onClick={() => setShowAddDevice(false)}>Cancel</button><button type="submit" className="device-confirm"><Plus size={14} /> Add Device</button></div>
          </form>
        </div>
      )}

      {showDetails && selectedDevice && (
        <div className="device-modal-backdrop" onClick={() => setShowDetails(false)}>
          <div className="device-modal device-details-modal" onClick={(e) => e.stopPropagation()}>
            <div className="device-modal-header"><div><h3>{selectedDevice.name}</h3><p>Complete device information</p></div><button onClick={() => setShowDetails(false)}><X size={18} /></button></div>
            <div className="device-detail-summary"><div><span>STATUS</span><strong>{selectedDevice.status}</strong></div><div><span>RISK SCORE</span><strong>{selectedDevice.risk ?? "-"}</strong></div><div><span>TYPE</span><strong>{selectedDevice.type}</strong></div><div><span>ZONE</span><strong>{selectedDevice.zone}</strong></div></div>
            <div className="device-detail-list"><p><span>IP Address</span><strong>{selectedDevice.ip}</strong></p><p><span>Vendor</span><strong>{selectedDevice.vendor || "Hikvision"}</strong></p><p><span>Last Seen</span><strong>{selectedDevice.lastSeen}</strong></p><p><span>Uptime</span><strong>{selectedDevice.uptime || "120d 4h 32m"}</strong></p><p><span>Security State</span><strong>{selectedDevice.status === "At Risk" ? "Investigation required" : "No active findings"}</strong></p></div>
            <button className="device-confirm full-action" onClick={() => { setShowDetails(false); setActionDevice(selectedDevice); }}>Open Device Actions</button>
          </div>
        </div>
      )}

      {actionDevice && (
        <div className="device-modal-backdrop" onClick={() => setActionDevice(null)}>
          <div className="device-modal" onClick={(e) => e.stopPropagation()}>
            <div className="device-modal-header"><div><h3>Device Actions</h3><p>Choose an action for {actionDevice.name}</p></div><button onClick={() => setActionDevice(null)}><X size={18} /></button></div>
            <div className="device-action-list">
              <button onClick={() => runDeviceAction("scan", actionDevice)}><Search size={16} /><span><strong>Run Security Scan</strong><small>Check the device for suspicious activity.</small></span></button>
              <button onClick={() => runDeviceAction("isolate", actionDevice)}><Shield size={16} /><span><strong>Isolate Device</strong><small>Restrict the device from the monitored network.</small></span></button>
              <button onClick={() => runDeviceAction("trust", actionDevice)}><CheckCircle2 size={16} /><span><strong>Mark as Trusted</strong><small>Clear the demo risk state for this device.</small></span></button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Sidebar({ active, setActive, sidebarOpen, setSidebarOpen }) {
  const items = [
    ["Dashboard", <LayoutDashboard size={18} />], ["Devices", <Monitor size={18} />],
    ["Threats & Alerts", <AlertTriangle size={18} />], ["Network Map", <Network size={18} />],
    ["Risk Analysis", <BarChart3 size={18} />], ["Response Center", <ShieldCheck size={18} />],
    ["Reports", <FileText size={18} />], ["Settings", <Settings size={18} />],
  ];
  return (
    <aside className={`sidebar ${sidebarOpen ? "" : "sidebar-closed"}`}>
      <div className="brand">
        <div className="brand-logo"><Lock size={23} /></div>
        <div><strong>SENTINEL</strong><span>Autonomous Cyber Defense System</span></div>
      </div>
      <nav>
        {items.map(([name, icon]) => (
          <button type="button" key={name} className={active === name ? "nav-active" : ""} onClick={() => setActive(name)}>{icon}<span>{name}</span></button>
        ))}
      </nav>
      <div className="ai-status">
        <div className="ai-status-icon"><Brain size={20} /></div><strong>AI Engine</strong>
        <div className="ai-status-row"><span>Status:</span><b>Active</b></div>
        <div className="ai-status-row"><span>Model:</span><span>v2.4.1</span></div>
        <div className="ai-status-row"><span>Updated:</span><span>2 min ago</span></div>
      </div>
    </aside>
  );
}

function Header({ sidebarOpen, setSidebarOpen, theme, setTheme, notificationOpen, setNotificationOpen, adminOpen, setAdminOpen, onLogout }) {
  return (
    <header className="header">
      <div className="header-left">
        <div><h1>Dashboard</h1><p>Real-time overview of your infrastructure security</p></div>
      </div>
      <div className="header-right">
        <div className="system-status"><span></span><div><small>System Status</small><strong>Secure</strong></div></div>
        <div className="header-menu-wrap">
          <button type="button" className="header-button notification" onClick={() => { setNotificationOpen(!notificationOpen); setAdminOpen(false); }} aria-label="Notifications"><Bell size={19} /><i>3</i></button>
          {notificationOpen && (
            <div className="popover notifications-popover">
              <div className="popover-title"><strong>Notifications</strong><button type="button" onClick={() => setNotificationOpen(false)}><X size={15} /></button></div>
              <div className="notification-item"><span className="notification-dot green-dot"></span><div><strong>Scan completed</strong><p>Security scan completed recently.</p><small>2 min ago</small></div></div>
              <div className="notification-item"><span className="notification-dot red-dot"></span><div><strong>Critical threat detected</strong><p>Malware detected on CAM-07.</p><small>10 min ago</small></div></div>
              <div className="notification-item"><span className="notification-dot orange-dot"></span><div><strong>Device activity</strong><p>New device connected to the network.</p><small>18 min ago</small></div></div>
            </div>
          )}
        </div>
        <button type="button" className="header-button theme-button" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}>
          {theme === "dark" ? <Moon size={19} /> : <Sun size={19} />}
        </button>
        <div className="header-menu-wrap">
          <button type="button" className="profile profile-button" onClick={() => { setAdminOpen(!adminOpen); setNotificationOpen(false); }} aria-label="Open Admin profile">
            <div className="avatar">A</div><div><strong>Admin</strong><span>Security Operator</span></div>
          </button>
          {adminOpen && (
            <div className="popover admin-popover">
              <div className="admin-card"><div className="admin-avatar"><UserCircle size={30} /></div><div><strong>Admin User</strong><span>Security Operator</span></div></div>
              <div className="admin-info"><span>Access</span><strong>Administrator</strong></div>
              <div className="admin-info"><span>Account</span><strong>Active</strong></div>
              <button type="button" className="logout-button" onClick={onLogout}><LogOut size={15} /> Logout</button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

function Dashboard({ setActive, onViewEvents, onTakeAction, onViewHealth }) {
  const [zoneFilter, setZoneFilter] = useState("All Zones");
  return (
    <>
      <Header
        sidebarOpen={false}
        setSidebarOpen={() => {}}
        theme="dark"
        setTheme={() => {}}
        notificationOpen={false}
        setNotificationOpen={() => {}}
        adminOpen={false}
        setAdminOpen={() => {}}
        onLogout={() => {}}
      />
      <main className="dashboard">
        <section className="stats-grid">
          {stats.map((item) => <StatCard item={item} key={item.title} onViewHealth={onViewHealth} />)}
        </section>
        <section className="main-grid">
          <Infrastructure zoneFilter={zoneFilter} setZoneFilter={setZoneFilter} />
          <div className="middle-column"><ThreatDistribution /><RiskTrend /></div>
          <RecentThreats setActive={setActive} />
        </section>
        <section className="bottom-grid"><SecurityEvents onViewAll={onViewEvents} /><AIRecommendation onTakeAction={onTakeAction} /></section>
      </main>
    </>
  );
}

function ThreatsAlerts() {
  const [statusFilter, setStatusFilter] = useState("All Status");
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [toast, setToast] = useState("");

  const filteredThreats = threats.filter((threat) => {
    if (statusFilter === "All Status") return true;
    return threat.status === statusFilter;
  });

  const runThreatAction = (action) => {
    const messages = {
      investigate: "Threat marked for investigation.",
      resolve: "Alert marked as resolved.",
      isolate: "Device isolation request queued.",
    };
    setToast(messages[action]);
    setTimeout(() => setToast(""), 2200);
  };

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

              <button
                className="view-threat"
                onClick={() => setSelectedThreat(threat)}
              >
                View Details <ArrowUpRight size={13} />
              </button>

            </div>
          ))}

        </div>

      </div>

      {selectedThreat && (
        <div className="threat-modal-backdrop" onClick={() => setSelectedThreat(null)}>
          <div className="threat-modal" onClick={(e) => e.stopPropagation()}>
            <div className="threat-modal-header">
              <div>
                <span className={`severity-badge ${selectedThreat.color}`}>{selectedThreat.severity}</span>
                <h3>{selectedThreat.title}</h3>
                <p>{selectedThreat.device} · {selectedThreat.time}</p>
              </div>
              <button className="threat-close" onClick={() => setSelectedThreat(null)} aria-label="Close details"><X size={18} /></button>
            </div>

            <div className="threat-detail-grid">
              <div><span>STATUS</span><strong>{selectedThreat.status}</strong></div>
              <div><span>SOURCE</span><strong>{selectedThreat.source}</strong></div>
              <div><span>DEVICE</span><strong>{selectedThreat.device}</strong></div>
              <div><span>SEVERITY</span><strong>{selectedThreat.severity}</strong></div>
            </div>

            <div className="threat-detail-section">
              <span>WHAT HAPPENED</span>
              <p>{selectedThreat.description}</p>
            </div>
            <div className="threat-detail-section recommendation">
              <span>RECOMMENDED ACTION</span>
              <p>{selectedThreat.recommendation}</p>
            </div>

            <div className="threat-modal-actions">
              <button onClick={() => runThreatAction("investigate")}><Search size={14} /> Investigate</button>
              <button onClick={() => runThreatAction("isolate")}><Shield size={14} /> Isolate Device</button>
              <button className="resolve" onClick={() => runThreatAction("resolve")}><CheckCircle2 size={14} /> Resolve</button>
            </div>
          </div>
        </div>
      )}

      {toast && <div className="threat-toast">{toast}</div>}
    </div>
  );
}
function NetworkMap() {
  const [mapMode, setMapMode] = useState("Network Map");
  const [zone, setZone] = useState("All Zones");
  const [selectedNode, setSelectedNode] = useState("CAM-07");
  const [zoom, setZoom] = useState(1);
  const [flowLive, setFlowLive] = useState(true);
  const [pathTracing, setPathTracing] = useState(false);
  const [mapToast, setMapToast] = useState("");
  const [showNodeDetails, setShowNodeDetails] = useState(false);

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

const notifyMap = (message) => {
  setMapToast(message);
  window.clearTimeout(window.__sentinelMapToast);
  window.__sentinelMapToast = window.setTimeout(() => setMapToast(""), 2400);
};

const handleInvestigate = () => {
  if (!selected) return;
  setShowNodeDetails(true);
  notifyMap(`Investigation started for ${selected.id}`);
};

const handleQueueInvestigation = (event) => {
  event?.stopPropagation();
  if (!selected) return;
  notifyMap(`${selected.id} investigation queued successfully`);
};

const handleModeAction = () => {
  if (isFlow) {
    setFlowLive((value) => !value);
    notifyMap(flowLive ? "Communication flow paused" : "Communication flow resumed");
  } else if (isAccessPath) {
    setPathTracing((value) => !value);
    notifyMap(pathTracing ? "Access path tracing paused" : "Access path tracing started");
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
            .replaceAll(" ", "-")} ${isFlow && !flowLive ? "flow-paused" : ""}`}
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
                    ? pathTracing && pathNodes.includes("SRV-DB-01")
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
                    ? pathTracing && pathNodes.includes("SRV-APP-02")
                      ? "line-secure path-active"
                      : "line-dim"
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
                    ? pathTracing && pathNodes.includes("CAM-07")
                      ? "line-critical path-active"
                      : "line-dim"
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
            <div className="network-map-core" style={{ transform: `translate(-50%, -50%) scale(${zoom})` }}>
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
                    transform: `translate(-50%, -50%) scale(${zoom})`,
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
              <button className={`flow-indicator ${flowLive ? "live" : "paused"}`} onClick={handleModeAction}>
                <span className="flow-live-dot"></span>
                {flowLive ? "LIVE TRAFFIC FLOW · PAUSE" : "TRAFFIC FLOW PAUSED · RESUME"}
              </button>
            )}

            {/* ACCESS PATH INFO */}
            {isAccessPath && (
              <button className={`path-indicator ${pathTracing ? "tracing" : "paused"}`} onClick={handleModeAction}>
                <span>PATH</span>
                {pathTracing ? "CAM-07 → CORE-SW-01 → SRV-APP-02" : "ACCESS PATH READY · CLICK TO TRACE"}
              </button>
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

              <button className="investigate-btn" onClick={handleInvestigate}>
                <Search size={15} /> Investigate
              </button>

              {isFlow && (
                <button className="map-secondary-action" onClick={handleModeAction}>
                  {flowLive ? "Pause Flow" : "Resume Flow"}
                </button>
              )}

              {isAccessPath && (
                <button className="map-secondary-action" onClick={handleModeAction}>
                  {pathTracing ? "Pause Trace" : "Trace Access Path"}
                </button>
              )}

            </div>
          )}

        </div>
      </div>

      {showNodeDetails && selected && (
        <div className="map-modal-backdrop" onClick={() => setShowNodeDetails(false)}>
          <div className="map-node-modal" onClick={(e) => e.stopPropagation()}>
            <div className="map-modal-header">
              <div>
                <span>NETWORK INVESTIGATION</span>
                <h3>{selected.id}</h3>
              </div>
              <button onClick={() => setShowNodeDetails(false)} aria-label="Close"><X size={18} /></button>
            </div>
            <div className="map-modal-grid">
              <div><span>IP ADDRESS</span><strong>{selected.ip}</strong></div>
              <div><span>TYPE</span><strong>{selected.type}</strong></div>
              <div><span>ZONE</span><strong>{selected.zone}</strong></div>
              <div><span>STATUS</span><strong className={selected.status}>{selected.status === "critical" ? "Critical" : selected.status === "warning" ? "Warning" : selected.status === "offline" ? "Offline" : "Secure"}</strong></div>
              <div><span>LAST ACTIVITY</span><strong>10:24 AM</strong></div>
              <div><span>CONNECTION</span><strong>CORE-SW-01</strong></div>
            </div>
            <div className="map-investigation-note">
              <ShieldCheck size={18} />
              <div><strong>Investigation ready</strong><p>SENTINEL can trace this node's relationships, communication activity and access path.</p></div>
            </div>
            <button type="button" className="investigate-btn queue-investigation-btn" onClick={handleQueueInvestigation}>Queue Investigation</button>
          </div>
        </div>
      )}

      {mapToast && <div className="map-toast">{mapToast}</div>}
    </div>
  );
}
function RiskAnalysis() {
  const [selectedRisk, setSelectedRisk] = useState(null);
  const [riskFilter, setRiskFilter] = useState("All Risks");
  const [toast, setToast] = useState("");

  const riskDevices = [
    { name: "CAM-07", type: "Camera", zone: "Office", risk: 78, level: "Critical", reason: "Malware activity and suspicious outbound communication were detected." },
    { name: "IOT-22", type: "IoT Device", zone: "Office", risk: 65, level: "High", reason: "Traffic behaviour is outside the learned baseline." },
    { name: "SRV-APP-02", type: "Server", zone: "Data Center", risk: 42, level: "Medium", reason: "Repeated authentication failures require review." },
    { name: "PC-ADMIN-03", type: "Workstation", zone: "Office", risk: 25, level: "Low", reason: "No active findings; device remains within normal risk range." },
  ];

  const filtered = riskFilter === "All Risks" ? riskDevices : riskDevices.filter((d) => d.level === riskFilter);
  const showToast = (message) => { setToast(message); window.clearTimeout(window.__sentinelRiskToast); window.__sentinelRiskToast = window.setTimeout(() => setToast(""), 2400); };

  return (
    <>
      <header className="header">
        <div><h1>Risk Analysis</h1><p>Analyze infrastructure risk and security posture</p></div>
        <div className="header-right"><div className="system-status"><span></span><div><small>Risk Status</small><strong>Elevated</strong></div></div></div>
      </header>

      <main className="risk-analysis-page">
        <section className="risk-summary-grid">
          <div className="risk-summary-card"><div className="risk-summary-top"><span>Overall Risk Score</span><BarChart3 size={19} /></div><strong className="overall-risk-number">67</strong><div className="risk-progress"><div style={{ width: "67%" }}></div></div><small>Elevated risk across infrastructure</small></div>
          <div className="risk-summary-card"><div className="risk-summary-top"><span>Critical Risks</span><AlertTriangle size={19} /></div><strong className="critical-number">2</strong><small>Require immediate attention</small></div>
          <div className="risk-summary-card"><div className="risk-summary-top"><span>High Risk Devices</span><Monitor size={19} /></div><strong className="high-number">4</strong><small>Devices above risk threshold</small></div>
          <div className="risk-summary-card"><div className="risk-summary-top"><span>Security Health</span><Shield size={19} /></div><strong className="health-number">87%</strong><small>Overall infrastructure health</small></div>
        </section>

        <section className="risk-analysis-grid">
          <div className="panel risk-distribution-panel"><div className="panel-header"><div><h3>Risk Distribution</h3><p>Current risk levels across your infrastructure</p></div></div><div className="risk-distribution"><div className="risk-ring"><div><strong>67</strong><span>Risk Score</span></div></div><div className="risk-level-list"><div><span><i className="risk-dot critical"></i>Critical</span><strong>2</strong></div><div><span><i className="risk-dot high"></i>High</span><strong>4</strong></div><div><span><i className="risk-dot medium"></i>Medium</span><strong>7</strong></div><div><span><i className="risk-dot low"></i>Low</span><strong>114</strong></div></div></div></div>
          <div className="panel risk-factors-panel"><div className="panel-header"><div><h3>Risk Factors</h3><p>Primary contributors to current risk</p></div></div><div className="risk-factor-list"><div><span>Malware Detection</span><strong>High</strong></div><div><span>Unauthorized Access</span><strong>High</strong></div><div><span>Network Anomalies</span><strong>Medium</strong></div><div><span>Policy Violations</span><strong>Low</strong></div></div></div>
        </section>

        <section className="panel top-risk-panel">
          <div className="panel-header"><div><h3>Top Risk Devices</h3><p>Devices requiring the most attention</p></div><select className="risk-filter" value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)}><option>All Risks</option><option>Critical</option><option>High</option><option>Medium</option><option>Low</option></select></div>
          <div className="risk-device-list">
            {filtered.map((device) => (
              <div className="risk-device-row" key={device.name}>
                <div className="risk-device-icon"><Monitor size={17} /></div><div className="risk-device-name"><strong>{device.name}</strong><span>{device.type} · {device.zone}</span></div><div className="risk-device-score"><strong>{device.risk}</strong><span>Risk</span></div><div className={`risk-level ${device.level.toLowerCase()}`}>{device.level}</div><button className="risk-view-btn" onClick={() => setSelectedRisk(device)}><Eye size={13} /> View</button>
              </div>
            ))}
          </div>
        </section>
      </main>

      {selectedRisk && <div className="risk-modal-backdrop" onClick={() => setSelectedRisk(null)}><div className="risk-detail-modal" onClick={(e) => e.stopPropagation()}><div className="risk-modal-header"><div><span className={`risk-level ${selectedRisk.level.toLowerCase()}`}>{selectedRisk.level}</span><h3>{selectedRisk.name}</h3><p>{selectedRisk.type} · {selectedRisk.zone}</p></div><button onClick={() => setSelectedRisk(null)} aria-label="Close"><X size={18} /></button></div><div className="risk-modal-grid"><div><span>RISK SCORE</span><strong>{selectedRisk.risk}/100</strong></div><div><span>ZONE</span><strong>{selectedRisk.zone}</strong></div><div><span>DEVICE TYPE</span><strong>{selectedRisk.type}</strong></div><div><span>ASSESSMENT</span><strong>{selectedRisk.level} Risk</strong></div></div><div className="risk-modal-note"><ShieldCheck size={18} /><div><strong>Assessment</strong><p>{selectedRisk.reason}</p></div></div><div className="risk-modal-actions"><button onClick={() => { showToast(`Risk scan started for ${selectedRisk.name}.`); setSelectedRisk(null); }}><Search size={14} /> Run Risk Scan</button><button onClick={() => { showToast(`Investigation queued for ${selectedRisk.name}.`); setSelectedRisk(null); }}><Shield size={14} /> Investigate</button></div></div></div>}
      {toast && <div className="action-toast">{toast}</div>}
    </>
  );
}
function ResponseCenter() {
  const [activeAction, setActiveAction] = useState(null);
  const [takeActionOpen, setTakeActionOpen] = useState(false);
  const [note, setNote] = useState("");
  const [notes, setNotes] = useState([]);
  const [toast, setToast] = useState("");

  const showToast = (message) => { setToast(message); window.clearTimeout(window.__sentinelResponseToast); window.__sentinelResponseToast = window.setTimeout(() => setToast(""), 2400); };
  const handleAction = (action) => {
    setActiveAction(action);
    setTakeActionOpen(false);
    showToast(`${action} action completed in demo mode.`);
  };
  const addNote = () => {
    const value = note.trim();
    if (!value) { showToast("Enter a note before saving."); return; }
    setNotes((current) => [{ id: Date.now(), text: value, time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) }, ...current]);
    setNote("");
    showToast("Investigation note added.");
  };
  const downloadEvidence = (name, content) => {
    const blob = new Blob([`SENTINEL EVIDENCE EXPORT\n\nIncident: INC-2025-0523-001\nArtifact: ${name}\nCollected: May 23, 2025 10:24 AM\n\n${content}`], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a"); link.href = url; link.download = name.replace(/\.[^.]+$/, "") + "-sentinel.txt"; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
    showToast(`${name} exported successfully.`);
  };
  const takeAction = (action) => handleAction(action);

  return (
    <>
      <header className="header"><div><h1>Response Center</h1><p>Manage incidents and coordinate security response</p></div><div className="header-right response-action-wrap"><button className="response-take-action" onClick={() => setTakeActionOpen((open) => !open)}>Take Action</button>{takeActionOpen && <div className="response-action-menu"><button onClick={() => takeAction("Verify")}><CheckCircle2 size={14} /> Verify Incident</button><button onClick={() => takeAction("Isolate")}><Shield size={14} /> Isolate CAM-07</button><button onClick={() => takeAction("Preserve")}><FileText size={14} /> Preserve Evidence</button><button onClick={() => takeAction("Recover")}><Activity size={14} /> Start Recovery</button></div>}</div></header>
      <main className="response-page">
        <div className="incident-heading"><div><span className="incident-label">INCIDENT</span><strong>INC-2025-0523-001</strong><span className="incident-active">{activeAction === "Isolate" ? "Isolated" : activeAction === "Recover" ? "Recovering" : activeAction === "Verify" ? "Verified" : "Active"}</span></div><span className="incident-time">May 23, 2025 · 10:24 AM</span></div>
        <section className="response-main-grid">
          <div className="panel response-summary"><div className="panel-header"><div><h3>Incident Summary</h3><p>Overview of the detected security incident</p></div></div><div className="incident-details"><div><span>Incident ID</span><strong>INC-2025-0523-001</strong></div><div><span>Detected</span><strong>May 23, 2025 10:24 AM</strong></div><div><span>Severity</span><strong className="critical-text">Critical</strong></div><div><span>Status</span><strong className="active-text">{activeAction || "Active"}</strong></div><div><span>Affected Device</span><strong>CAM-07 (10.0.3.25)</strong></div><div><span>Incident Type</span><strong>Malware Infection</strong></div><div className="incident-description"><span>Description</span><p>Malware detected on CAM-07 with suspicious outbound communication and command-and-control activity.</p></div></div></div>
          <div className="panel response-timeline"><div className="panel-header"><div><h3>Incident Timeline</h3><p>Security events leading to this incident</p></div></div><div className="timeline"><div className="timeline-item"><div className="timeline-dot critical"></div><div><strong>Malware detected</strong><span>10:24 AM</span><p>Trojan.Win32 detected on CAM-07</p></div></div><div className="timeline-item"><div className="timeline-dot critical"></div><div><strong>Outbound connection detected</strong><span>10:20 AM</span><p>Connection to suspicious external IP</p></div></div><div className="timeline-item"><div className="timeline-dot high"></div><div><strong>Multiple failed login attempts</strong><span>10:15 AM</span><p>Authentication anomalies detected</p></div></div><div className="timeline-item"><div className="timeline-dot medium"></div><div><strong>Policy violation detected</strong><span>10:10 AM</span><p>Device communication policy violation</p></div></div><div className="timeline-item"><div className="timeline-dot low"></div><div><strong>Device came online</strong><span>10:04 AM</span><p>CAM-07 connected to the network</p></div></div></div></div>
        </section>
        <section className="panel response-actions-panel"><div className="panel-header"><div><h3>Response Actions</h3><p>Recommended actions for this incident</p></div></div><div className="response-actions">{[["Verify","Validate the alert and collect supporting evidence",CheckCircle2],["Isolate","Isolate the affected device from the network",Shield],["Preserve","Preserve logs and forensic evidence",FileText],["Recover","Clean and restore the affected device",Activity]].map(([name,desc,Icon],i) => <div className="response-action" key={name}><div className="action-number">{i+1}</div><div className="action-content"><strong>{name}</strong><span>{desc}</span></div><button onClick={() => handleAction(name)} className={activeAction === name ? "action-done" : ""}><Icon size={14} /> {activeAction === name ? `${name}d` : name}</button></div>)}</div></section>
        <section className="response-bottom-grid"><div className="panel evidence-panel"><div className="panel-header"><div><h3>Evidence & Artifacts</h3><p>Collected evidence related to this incident</p></div></div><div className="evidence-list">{[["Malware Sample","Trojan.Win32.exe","10:24 AM","Executable sample preserved for analysis."],["Traffic Capture","capture.pcap","10:24 AM","Network traffic capture from the affected segment."],["System Logs","system.log","10:24 AM","Endpoint security and system event logs."]].map(([title,file,time,content]) => <div className="evidence-item" key={file}><div><strong>{title}</strong><span>{file}</span><small>{time}</small></div><button onClick={() => downloadEvidence(file, content)}><Download size={13} /> Download</button></div>)}</div></div>
          <div className="panel notes-panel"><div className="panel-header"><div><h3>Notes</h3><p>Investigation notes and observations</p></div></div><textarea value={note} onChange={(e) => setNote(e.target.value)} placeholder="Add investigation notes..."/><button className="add-note" onClick={addNote}>Add Note</button>{notes.length > 0 && <div className="saved-notes">{notes.map((item) => <div className="saved-note" key={item.id}><span>{item.time}</span><p>{item.text}</p></div>)}</div>}</div>
        </section>
      </main>
      {toast && <div className="action-toast">{toast}</div>}
    </>
  );
}
function Reports() {
  const [reportType, setReportType] = useState("Security Summary");
  const [dateRange, setDateRange] = useState("Last 7 Days");
  const [customStart, setCustomStart] = useState("");
  const [customEnd, setCustomEnd] = useState("");
  const [generatedReports, setGeneratedReports] = useState([]);
  const [viewReport, setViewReport] = useState(null);
  const [notice, setNotice] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const reportData = {
    "Security Summary": {
      incidents: "24", incidentsLabel: "Last 7 days", threats: "28", threatsLabel: "5 critical",
      devices: "127", devicesLabel: "112 online", health: "87%", healthLabel: "Overall posture",
      risk: "67", critical: "2", highRisk: "4", resolved: "24", violations: "3", status: "Elevated",
      overviewTitle: "Security Overview", overviewSubtitle: "Infrastructure security posture",
      threatData: [
        { name: "Malware", value: 40 }, { name: "Unauthorized Access", value: 20 },
        { name: "Anomalous Behavior", value: 20 }, { name: "Policy Violation", value: 20 },
      ],
    },
    "Threat Report": {
      incidents: "18", incidentsLabel: "Threat-related incidents", threats: "28", threatsLabel: "5 critical",
      devices: "34", devicesLabel: "Affected devices", health: "72%", healthLabel: "Threat posture",
      risk: "74", critical: "5", highRisk: "7", resolved: "19", violations: "6", status: "High Risk",
      overviewTitle: "Threat Overview", overviewSubtitle: "Detected security threats",
      threatData: [
        { name: "Malware", value: 45 }, { name: "Unauthorized Access", value: 30 },
        { name: "Anomalous Behavior", value: 15 }, { name: "Policy Violation", value: 10 },
      ],
    },
    "Device Report": {
      incidents: "12", incidentsLabel: "Device incidents", threats: "9", threatsLabel: "2 critical",
      devices: "127", devicesLabel: "112 online", health: "87%", healthLabel: "Device health",
      risk: "61", critical: "2", highRisk: "4", resolved: "21", violations: "3", status: "Elevated",
      overviewTitle: "Device Security Overview", overviewSubtitle: "Infrastructure device posture",
      threatData: [
        { name: "Compromised Devices", value: 35 }, { name: "Outdated Software", value: 25 },
        { name: "Unauthorized Access", value: 20 }, { name: "Policy Violation", value: 20 },
      ],
    },
    "Incident Report": {
      incidents: "24", incidentsLabel: "Total incidents", threats: "16", threatsLabel: "Related threats",
      devices: "42", devicesLabel: "Affected devices", health: "81%", healthLabel: "Incident posture",
      risk: "69", critical: "3", highRisk: "5", resolved: "24", violations: "4", status: "Elevated",
      overviewTitle: "Incident Overview", overviewSubtitle: "Security incidents and response",
      threatData: [
        { name: "Active Incidents", value: 35 }, { name: "Resolved Incidents", value: 30 },
        { name: "Critical Incidents", value: 20 }, { name: "Policy Incidents", value: 15 },
      ],
    },
    "Network Report": {
      incidents: "8", incidentsLabel: "Network incidents", threats: "11", threatsLabel: "Network threats",
      devices: "127", devicesLabel: "Connected devices", health: "84%", healthLabel: "Network health",
      risk: "63", critical: "2", highRisk: "4", resolved: "20", violations: "3", status: "Elevated",
      overviewTitle: "Network Security Overview", overviewSubtitle: "Network infrastructure posture",
      threatData: [
        { name: "Suspicious Traffic", value: 40 }, { name: "Unauthorized Access", value: 25 },
        { name: "Port Scanning", value: 20 }, { name: "Policy Violation", value: 15 },
      ],
    },
  };

  const currentReport = reportData[reportType];
  const activeDateLabel = dateRange === "Custom Range"
    ? (customStart && customEnd ? `${customStart} to ${customEnd}` : "Choose a custom date range")
    : dateRange;

  const showNotice = (message) => {
    setNotice(message);
    window.setTimeout(() => setNotice(""), 2800);
  };

  const validateDateRange = () => {
    if (dateRange !== "Custom Range") return true;
    if (!customStart || !customEnd) {
      showNotice("Please select both custom start and end dates.");
      return false;
    }
    if (customStart > customEnd) {
      showNotice("Start date cannot be after the end date.");
      return false;
    }
    return true;
  };

  const buildReport = () => ({
    id: `${Date.now()}-${reportType}`,
    name: `${reportType} — ${activeDateLabel}`,
    type: reportType,
    generated: new Date().toLocaleString([], { dateStyle: "medium", timeStyle: "short" }),
    status: "Completed",
    data: currentReport,
    dateRange: activeDateLabel,
  });

  const generateReport = () => {
    if (!validateDateRange()) return;
    setIsGenerating(true);
    window.setTimeout(() => {
      const report = buildReport();
      setGeneratedReports((items) => [report, ...items]);
      setViewReport(report);
      setIsGenerating(false);
      showNotice(`${reportType} generated successfully.`);
    }, 550);
  };

  const exportPDF = (report = buildReport()) => {
    if (!validateDateRange()) return;
    const data = report.data || reportData[report.type] || currentReport;
    const lines = [
      "SENTINEL SECURITY REPORT",
      "========================================",
      `Report Type: ${report.type || reportType}`,
      `Date Range: ${report.dateRange || activeDateLabel}`,
      `Generated: ${report.generated || new Date().toLocaleString()}`,
      "",
      "SECURITY SUMMARY",
      `Overall Risk Score: ${data.risk ?? "-"}`,
      `Security Health: ${data.health ?? "-"}`,
      `Threats Detected: ${data.threats ?? "-"}`,
      `Total Incidents: ${data.incidents ?? "-"}`,
      `Critical Risks: ${data.critical ?? "-"}`,
      `High Risk Devices: ${data.highRisk ?? "-"}`,
      `Resolved Incidents: ${data.resolved ?? "-"}`,
      `Policy Violations: ${data.violations ?? "-"}`,
      `Status: ${data.status ?? "-"}`,
      "",
      data.overviewTitle || "Security Overview",
      data.overviewSubtitle || "SENTINEL security posture report.",
      "",
      "THREAT DISTRIBUTION",
      ...(data.threatData || []).map((item) => `${item.name}: ${item.value}%`),
    ];
    const escapePdf = (value) => String(value).replace(/\\/g, "\\\\").replace(/\(/g, "\\(").replace(/\)/g, "\\)");
    const textLines = lines.flatMap((line) => {
      const clean = String(line);
      if (clean.length <= 88) return [clean];
      const chunks = []; for (let i = 0; i < clean.length; i += 88) chunks.push(clean.slice(i, i + 88)); return chunks;
    });
    const stream = ["BT", "/F1 10 Tf", "50 750 Td", "14 TL", ...textLines.map((line) => `(${escapePdf(line)}) Tj T*`), "ET"].join("\n");
    const objects = [
      "<< /Type /Catalog /Pages 2 0 R >>",
      "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
      "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
      "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
      `<< /Length ${new TextEncoder().encode(stream).length} >>\nstream\n${stream}\nendstream`,
    ];
    let pdf = "%PDF-1.4\n"; const offsets = [0];
    objects.forEach((obj, i) => { offsets.push(new TextEncoder().encode(pdf).length); pdf += `${i + 1} 0 obj\n${obj}\nendobj\n`; });
    const xref = new TextEncoder().encode(pdf).length;
    pdf += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
    for (let i = 1; i <= objects.length; i++) pdf += `${String(offsets[i]).padStart(10, "0")} 00000 n \n`;
    pdf += `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF`;
    const blob = new Blob([pdf], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a"); link.href = url; link.download = `${(report.name || `${reportType} Report`).replace(/[^a-z0-9]+/gi, "-").replace(/^-|-$/g, "")}.pdf`; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
    showNotice("PDF report downloaded successfully.");
  };

  const viewExistingReport = (report) => setViewReport(report);

  const recentReports = [
    { id: "weekly", name: "Weekly Security Summary", type: "Security Summary", generated: "May 23, 2025", status: "Completed" },
    { id: "threat", name: "Threat Detection Report", type: "Threat Report", generated: "May 22, 2025", status: "Completed" },
    { id: "network", name: "Network Security Report", type: "Network Report", generated: "May 20, 2025", status: "Completed" },
    { id: "incident", name: "Incident Response Report", type: "Incident Report", generated: "May 18, 2025", status: "Completed" },
    ...generatedReports,
  ];

  return (
    <>
      <header className="header">
        <div>
          <h1>Reports</h1>
          <p>Generate and review security reports</p>
        </div>
        <div className="header-right">
          <button className="report-generate-btn" onClick={generateReport} disabled={isGenerating}>
            <FileText size={16} />
            {isGenerating ? "Generating..." : "Generate Report"}
          </button>
        </div>
      </header>

      <main className="reports-page">
        <section className="report-controls panel">
          <div className="report-control-group">
            <label>Report Type</label>
            <select value={reportType} onChange={(e) => setReportType(e.target.value)}>
              <option>Security Summary</option>
              <option>Threat Report</option>
              <option>Device Report</option>
              <option>Incident Report</option>
              <option>Network Report</option>
            </select>
          </div>

          <div className="report-control-group">
            <label>Date Range</label>
            <select value={dateRange} onChange={(e) => setDateRange(e.target.value)}>
              <option>Last 24 Hours</option>
              <option>Last 7 Days</option>
              <option>Last 30 Days</option>
              <option>Custom Range</option>
            </select>
          </div>

          {dateRange === "Custom Range" && (
            <>
              <div className="report-control-group">
                <label>Start Date</label>
                <input type="date" value={customStart} onChange={(e) => setCustomStart(e.target.value)} />
              </div>
              <div className="report-control-group">
                <label>End Date</label>
                <input type="date" value={customEnd} onChange={(e) => setCustomEnd(e.target.value)} />
              </div>
            </>
          )}

          <button className="report-export-btn" onClick={() => exportPDF()}>
            <Download size={16} /> Export PDF
          </button>
        </section>

        <section className="report-summary-grid">
          <div className="report-stat-card"><span>Total Incidents</span><strong>{currentReport.incidents}</strong><small>{currentReport.incidentsLabel}</small></div>
          <div className="report-stat-card"><span>Threats Detected</span><strong className="report-danger">{currentReport.threats}</strong><small>{currentReport.threatsLabel}</small></div>
          <div className="report-stat-card"><span>Devices Monitored</span><strong>{currentReport.devices}</strong><small>{currentReport.devicesLabel}</small></div>
          <div className="report-stat-card"><span>Security Health</span><strong className="report-success">{currentReport.health}</strong><small>{currentReport.healthLabel}</small></div>
        </section>

        <section className="report-main-grid">
          <div className="panel report-overview">
            <div className="panel-header">
              <div><h3>{currentReport.overviewTitle}</h3><p>{currentReport.overviewSubtitle}</p></div>
              <span className="report-status">{currentReport.status}</span>
            </div>
            <div className="report-overview-content">
              <div className="report-score"><div className="report-score-circle"><strong>{currentReport.risk}</strong><span>Risk Score</span></div></div>
              <div className="report-metrics">
                <div><span>Critical Risks</span><strong className="report-danger">{currentReport.critical}</strong></div>
                <div><span>High Risk Devices</span><strong className="report-warning">{currentReport.highRisk}</strong></div>
                <div><span>Resolved Incidents</span><strong className="report-success">{currentReport.resolved}</strong></div>
                <div><span>Policy Violations</span><strong>{currentReport.violations}</strong></div>
              </div>
            </div>
          </div>

          <div className="panel threat-summary">
            <div className="panel-header"><div><h3>Threat Summary</h3><p>Detected threats by category</p></div></div>
            <div className="threat-bars">
              {currentReport.threatData.map((threat, index) => (
                <div className="threat-bar-row" key={index}>
                  <div><span>{threat.name}</span><strong>{threat.value}%</strong></div>
                  <div className="threat-bar"><span style={{ width: `${threat.value}%` }}></span></div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="panel recent-reports">
          <div className="panel-header">
            <div><h3>Recent Reports</h3><p>Previously generated security reports</p></div>
          </div>
          <div className="reports-table">
            <div className="report-table-header"><span>Report Name</span><span>Type</span><span>Generated</span><span>Status</span><span>Action</span></div>
            {recentReports.map((report) => (
              <div className="report-table-row" key={report.id}>
                <strong>{report.name}</strong>
                <span>{report.type}</span>
                <span>{report.generated}</span>
                <span className="report-complete">{report.status}</span>
                <button onClick={() => viewExistingReport({ ...report, data: reportData[report.type], dateRange: report.dateRange || "Historical report" })}>
                  <Eye size={14} /> View
                </button>
              </div>
            ))}
          </div>
        </section>
      </main>

      {notice && <div className="action-toast">{notice}</div>}

      {viewReport && (
        <div className="report-modal-backdrop" onClick={() => setViewReport(null)}>
          <div className="report-modal panel" onClick={(e) => e.stopPropagation()}>
            <div className="panel-header">
              <div>
                <h3>{viewReport.name}</h3>
                <p>{viewReport.type} • {viewReport.dateRange || "Historical report"}</p>
              </div>
              <button className="icon-btn" onClick={() => setViewReport(null)}><X size={18} /></button>
            </div>
            <div className="report-modal-grid">
              <div><span>Risk Score</span><strong>{viewReport.data?.risk ?? "-"}</strong></div>
              <div><span>Security Health</span><strong>{viewReport.data?.health ?? "-"}</strong></div>
              <div><span>Threats</span><strong>{viewReport.data?.threats ?? "-"}</strong></div>
              <div><span>Incidents</span><strong>{viewReport.data?.incidents ?? "-"}</strong></div>
            </div>
            <div className="report-modal-section">
              <h4>Security Summary</h4>
              <p>{viewReport.data?.overviewSubtitle || "Security posture report generated by SENTINEL."}</p>
              <div className="report-modal-metrics">
                <span>Critical risks: <b>{viewReport.data?.critical ?? "-"}</b></span>
                <span>High-risk devices: <b>{viewReport.data?.highRisk ?? "-"}</b></span>
                <span>Resolved incidents: <b>{viewReport.data?.resolved ?? "-"}</b></span>
                <span>Policy violations: <b>{viewReport.data?.violations ?? "-"}</b></span>
              </div>
            </div>
            <div className="report-modal-actions">
              <button className="report-export-btn" onClick={() => exportPDF(viewReport)}><Download size={15} /> Export PDF</button>
              <button className="report-generate-btn" onClick={() => showNotice("Report verification completed successfully.")}><CheckIcon size={15} /> Verify Report</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
function SentinelSettings() {
  const defaults = {
    systemName: "SENTINEL Security",
    autoRefresh: true,
    notifications: true,
    threatAlerts: true,
    logRetention: "30 Days",
    monitoringInterface: "eth0",
    monitoringMode: "Active",
  };

  const [settings, setSettings] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("sentinel-settings") || "null");
      return { ...defaults, ...(saved || {}) };
    } catch {
      return defaults;
    }
  });
  const [saved, setSaved] = useState(false);
  const [toast, setToast] = useState("");

  const update = (key, value) => {
    setSettings((current) => ({ ...current, [key]: value }));
    setSaved(false);
  };

  const saveSettings = () => {
    localStorage.setItem("sentinel-settings", JSON.stringify(settings));
    setSaved(true);
    setToast("Settings saved successfully");
    setTimeout(() => setToast(""), 2500);
  };

  const resetDefaults = () => {
    setSettings(defaults);
    localStorage.removeItem("sentinel-settings");
    setSaved(false);
    setToast("Settings restored to defaults");
    setTimeout(() => setToast(""), 2500);
  };

  return (
    <>
      <header className="header">
        <div>
          <h1>Settings</h1>
          <p>Configure SENTINEL security and system preferences</p>
        </div>
      </header>

      <main className="settings-page">
        {toast && <div className="settings-toast">{toast}</div>}

        <section className="panel settings-section">
          <div className="panel-header">
            <div><h3>General Settings</h3><p>Configure general system preferences</p></div>
          </div>
          <div className="settings-list">
            <div className="setting-row">
              <div><strong>System Name</strong><span>Display name for this SENTINEL instance</span></div>
              <input value={settings.systemName} onChange={(e) => update("systemName", e.target.value)} />
            </div>
            <div className="setting-row">
              <div><strong>Auto Refresh</strong><span>Automatically refresh security data</span></div>
              <button type="button" aria-label="Toggle auto refresh" className={`toggle ${settings.autoRefresh ? "on" : ""}`} onClick={() => update("autoRefresh", !settings.autoRefresh)}><span></span></button>
            </div>
          </div>
        </section>

        <section className="panel settings-section">
          <div className="panel-header">
            <div><h3>Notifications</h3><p>Manage security notifications and alerts</p></div>
          </div>
          <div className="settings-list">
            <div className="setting-row">
              <div><strong>Enable Notifications</strong><span>Receive SENTINEL security notifications</span></div>
              <button type="button" aria-label="Toggle notifications" className={`toggle ${settings.notifications ? "on" : ""}`} onClick={() => update("notifications", !settings.notifications)}><span></span></button>
            </div>
            <div className="setting-row">
              <div><strong>Threat Alerts</strong><span>Receive alerts when threats are detected</span></div>
              <button type="button" aria-label="Toggle threat alerts" className={`toggle ${settings.threatAlerts ? "on" : ""}`} onClick={() => update("threatAlerts", !settings.threatAlerts)}><span></span></button>
            </div>
          </div>
        </section>

        <section className="panel settings-section">
          <div className="panel-header">
            <div><h3>Security &amp; Monitoring</h3><p>Configure security monitoring preferences</p></div>
          </div>
          <div className="settings-list">
            <div className="setting-row">
              <div><strong>Threat Monitoring</strong><span>Continuously monitor network activity</span></div>
              <button type="button" className={`setting-status ${settings.monitoringMode === "Active" ? "active" : ""}`} onClick={() => update("monitoringMode", settings.monitoringMode === "Active" ? "Paused" : "Active")}>
                {settings.monitoringMode}
              </button>
            </div>
            <div className="setting-row">
              <div><strong>Intrusion Detection</strong><span>Detect suspicious network behaviour</span></div>
              <button type="button" className={`setting-status ${settings.threatAlerts ? "active" : ""}`} onClick={() => update("threatAlerts", !settings.threatAlerts)}>
                {settings.threatAlerts ? "Enabled" : "Disabled"}
              </button>
            </div>
            <div className="setting-row">
              <div><strong>Log Retention</strong><span>Duration for retaining security logs</span></div>
              <select value={settings.logRetention} onChange={(e) => update("logRetention", e.target.value)}>
                <option>7 Days</option><option>30 Days</option><option>90 Days</option><option>1 Year</option>
              </select>
            </div>
          </div>
        </section>

        <section className="panel settings-section">
          <div className="panel-header">
            <div><h3>Network Configuration</h3><p>Configure network monitoring parameters</p></div>
          </div>
          <div className="settings-list">
            <div className="setting-row">
              <div><strong>Monitoring Interface</strong><span>Network interface used by SENTINEL</span></div>
              <select value={settings.monitoringInterface} onChange={(e) => update("monitoringInterface", e.target.value)}>
                <option>eth0</option><option>wlan0</option><option>Ethernet</option>
              </select>
            </div>
            <div className="setting-row">
              <div><strong>Monitoring Mode</strong><span>Current network monitoring mode</span></div>
              <button type="button" className={`setting-status ${settings.monitoringMode === "Active" ? "active" : ""}`} onClick={() => update("monitoringMode", settings.monitoringMode === "Active" ? "Paused" : "Active")}>
                {settings.monitoringMode}
              </button>
            </div>
          </div>
        </section>

        <div className="settings-footer">
          <button type="button" className="settings-reset-btn" onClick={resetDefaults}>Reset Defaults</button>
          <button type="button" className="settings-save-btn" onClick={saveSettings}>{saved ? "Saved ✓" : "Save Changes"}</button>
        </div>
      </main>
    </>
  );
}

function Login({ onLogin }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const submit = (event) => {
    event.preventDefault();
    if (!email.trim() || !password.trim()) { setError("Enter your email and password."); return; }
    onLogin();
  };
  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-logo"><Shield size={31} /></div>
        <h1>SENTINEL</h1><p>Autonomous Cyber Defense System</p>
        <form onSubmit={submit}>
          <label>Email<input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@sentinel.local" /></label>
          <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter password" /></label>
          {error && <div className="login-error">{error}</div>}
          <button type="submit" className="login-button">Sign In</button>
        </form>
        <small>Demo login — backend authentication can be connected later.</small>
      </div>
    </div>
  );
}
function DashboardModal({ title, children, onClose, className = "" }) {
  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <div className={`dashboard-modal ${className}`} onMouseDown={(e) => e.stopPropagation()}>
        <div className="modal-header"><h2>{title}</h2><button type="button" onClick={onClose} aria-label="Close"><X size={18} /></button></div>
        {children}
      </div>
    </div>
  );
}
function App() {
  const [active, setActive] = useState("Dashboard");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [theme, setTheme] = useState("dark");
  const [loggedIn, setLoggedIn] = useState(() => sessionStorage.getItem("sentinel-logged-in") === "true");
  const [notificationOpen, setNotificationOpen] = useState(false);
  const [adminOpen, setAdminOpen] = useState(false);
  const [eventsOpen, setEventsOpen] = useState(false);
  const [actionOpen, setActionOpen] = useState(false);
  const [healthOpen, setHealthOpen] = useState(false);
  const [dashboardZone, setDashboardZone] = useState("All Zones");

  useEffect(() => {
    localStorage.setItem("sentinel-theme", theme);
  }, [theme]);

  const login = () => { sessionStorage.setItem("sentinel-logged-in", "true"); setLoggedIn(true); };
  const logout = () => { sessionStorage.removeItem("sentinel-logged-in"); setLoggedIn(false); setAdminOpen(false); setNotificationOpen(false); setActive("Dashboard"); };

  if (!loggedIn) return <Login onLogin={login} />;

  return (
    <div className={`app ${theme === "light" ? "theme-light" : "theme-dark"}`}>
      <Sidebar active={active} setActive={(page) => { setActive(page); setNotificationOpen(false); setAdminOpen(false); }} sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
      <button
        type="button"
        className={`global-sidebar-toggle ${sidebarOpen ? "nav-open" : "nav-closed"}`}
        onClick={() => setSidebarOpen((open) => !open)}
        aria-label={sidebarOpen ? "Hide navigation sidebar" : "Show navigation sidebar"}
        title={sidebarOpen ? "Hide navigation" : "Show navigation"}
      >
        <Menu size={21} />
      </button>
      <div className={`content ${sidebarOpen ? "" : "content-expanded"}`}>
        {active === "Dashboard" ? <>
          <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} theme={theme} setTheme={setTheme} notificationOpen={notificationOpen} setNotificationOpen={setNotificationOpen} adminOpen={adminOpen} setAdminOpen={setAdminOpen} onLogout={logout} />
          <main className="dashboard">
            <section className="stats-grid">{stats.map((item) => <StatCard item={item} key={item.title} onViewHealth={() => setHealthOpen(true)} />)}</section>
            <section className="main-grid"><Infrastructure zoneFilter={dashboardZone} setZoneFilter={setDashboardZone} /><div className="middle-column"><ThreatDistribution /><RiskTrend /></div><RecentThreats setActive={setActive} /></section>
            <section className="bottom-grid"><SecurityEvents onViewAll={() => setEventsOpen(true)} /><AIRecommendation onTakeAction={() => setActionOpen(true)} /></section>
          </main>
        </> : active === "Devices" ? <Devices /> : active === "Threats & Alerts" ? <ThreatsAlerts /> : active === "Network Map" ? <NetworkMap /> : active === "Risk Analysis" ? <RiskAnalysis /> : active === "Response Center" ? <ResponseCenter /> : active === "Reports" ? <Reports /> : active === "Settings" ? <SentinelSettings /> : null}
      </div>

      {eventsOpen && <DashboardModal title="All Security Events" onClose={() => setEventsOpen(false)}>
        <div className="modal-table"><table><thead><tr><th>Time</th><th>Device</th><th>Event</th><th>Severity</th><th>Status</th></tr></thead><tbody>{events.map((event, index) => <tr key={index}><td>{event[0]}</td><td>{event[1]}</td><td>{event[2]}</td><td><span className={`badge ${event[3].toLowerCase()}`}>{event[3]}</span></td><td>{event[4]}</td></tr>)}</tbody></table></div>
      </DashboardModal>}

      {actionOpen && <DashboardModal title="Recommended Actions" onClose={() => setActionOpen(false)} className="action-modal">
        <p className="modal-description">Choose an action for <strong>CAM-07</strong>. This demo action will be recorded locally and can later be connected to the backend API.</p>
        <div className="action-list"><button type="button" onClick={() => { setActionOpen(false); alert("CAM-07 isolation action queued."); }}>Isolate device</button><button type="button" onClick={() => { setActionOpen(false); alert("Full malware scan queued for CAM-07."); }}>Run full malware scan</button><button type="button" onClick={() => { setActionOpen(false); alert("Evidence preservation action queued for CAM-07."); }}>Preserve evidence</button></div>
      </DashboardModal>}

      {healthOpen && <DashboardModal title="Cyber Health Details" onClose={() => setHealthOpen(false)}><div className="health-modal-content"><div className="health-modal-score">87<span>/100</span></div><p>Infrastructure health is currently <strong>Good</strong>. No change to the current dashboard health score.</p><button type="button" onClick={() => setHealthOpen(false)}>Done</button></div></DashboardModal>}
    </div>
  );
}
export default App;