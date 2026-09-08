"""Opt-in local SENTINEL collector for authorized connection metadata.

The collector does not discover or authorize devices. An administrator must
register, authorize, and activate the device through the API first, then provide
its JWT and device ID through environment variables.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import platform
import socket
import time
from datetime import UTC, datetime

import httpx
import psutil



def _event_id(device_id: str, connection: psutil._common.sconn, observed_at: datetime) -> str:
    value = f"{device_id}:{connection.fd}:{connection.laddr}:{connection.raddr}:{connection.status}:{observed_at.isoformat()}"
    return f"collector-{hashlib.sha256(value.encode()).hexdigest()[:32]}"


class AuthorizationRevoked(RuntimeError):
    pass


def _raise_for_collection(response: httpx.Response) -> None:
    if response.status_code in {401, 403, 404}:
        raise AuthorizationRevoked(f"collector authorization rejected: HTTP {response.status_code}")
    response.raise_for_status()


def collect_once(api_url: str, token: str, device_id: str) -> int:
    observed_at = datetime.now(UTC)
    headers = {"Authorization": f"Bearer {token}"}
    submitted = 0
    with httpx.Client(base_url=api_url, headers=headers, timeout=10.0) as client:
        heartbeat = client.post("/collector/heartbeat", json={"device_id": device_id, "timestamp": observed_at.isoformat(), "status": "online"})
        _raise_for_collection(heartbeat)
        system_drive = os.environ.get("SystemDrive", "C:") + "\\"
        disk_path = system_drive if os.name == "nt" else "/"
        counters = psutil.net_io_counters()
        telemetry = client.post("/collector/telemetry", json={
            "device_id": device_id,
            "timestamp": observed_at.isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage(disk_path).percent,
            "uptime_seconds": int(time.time() - psutil.boot_time()),
            "os_information": {"system": platform.system(), "release": platform.release(), "version": platform.version(), "machine": platform.machine()},
            "interfaces": {name: {"is_up": stats.isup, "speed_mbps": stats.speed, "mtu": stats.mtu} for name, stats in psutil.net_if_stats().items()},
            "bytes_sent": counters.bytes_sent,
            "bytes_received": counters.bytes_recv,
            "connection_count": len(psutil.net_connections(kind="inet")),
        })
        _raise_for_collection(telemetry)
        try:
            connections = psutil.net_connections(kind="inet")
        except psutil.AccessDenied as error:
            raise RuntimeError("OS denied connection metadata access; run with approved permissions") from error
        for connection in connections:
            if not connection.raddr or not connection.laddr:
                continue
            destination_ip = connection.raddr.ip
            if destination_ip in {"0.0.0.0", "::", "127.0.0.1", "::1"}:
                continue
            source_ip = connection.laddr.ip
            protocol = "TCP" if connection.type == socket.SOCK_STREAM else "UDP"
            payload = {
                "device_id": device_id,
                "source_event_id": _event_id(device_id, connection, observed_at),
                "ingestion_source": "LOCAL_COLLECTOR",
                "source_ip": source_ip,
                "destination_ip": destination_ip,
                "source_port": connection.laddr.port,
                "destination_port": connection.raddr.port,
                "protocol": protocol,
                "packet_count": 0,
                "byte_count": 0,
                "flow_duration_ms": 0,
                "timestamp": observed_at.isoformat(),
                "connection_status": connection.status or "observed",
                "request_frequency": 1,
            }
            response = client.post("/network/traffic", json=payload)
            _raise_for_collection(response)
            submitted += 1
    return submitted


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit authorized local connection metadata to SENTINEL")
    parser.add_argument("--api-url", default=os.getenv("SENTINEL_API_URL", "http://127.0.0.1:8000/api"))
    parser.add_argument("--token", default=os.getenv("SENTINEL_ACCESS_TOKEN"), required=os.getenv("SENTINEL_ACCESS_TOKEN") is None)
    parser.add_argument("--device-id", default=os.getenv("SENTINEL_DEVICE_ID"), required=os.getenv("SENTINEL_DEVICE_ID") is None)
    parser.add_argument("--interval", type=float, default=30.0)
    args = parser.parse_args()

    while True:
        try:
            submitted = collect_once(args.api_url.rstrip("/"), args.token, args.device_id)
            print(f"submitted={submitted} source=REAL ingestion_source=LOCAL_COLLECTOR", flush=True)
        except AuthorizationRevoked as error:
            print(f"collector_stopped={error}", flush=True)
            return
        except (httpx.HTTPError, RuntimeError) as error:
            print(f"collector_error={error} source=REAL", flush=True)
        time.sleep(max(args.interval, 5.0))


if __name__ == "__main__":
    main()
