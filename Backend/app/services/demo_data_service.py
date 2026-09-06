from __future__ import annotations

from app.schemas.network_traffic import NetworkTrafficCreate


DEMO_LABEL = "SIMULATED DEMO DATA"


def build_demo_flows(scenario: str) -> list[NetworkTrafficCreate]:
    if scenario == "normal":
        return [NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=443, packet_count=40, byte_count=12_000, flow_duration_ms=800, request_frequency=2)]
    if scenario == "suspicious":
        return [
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=22, packet_count=100, byte_count=80_000, flow_duration_ms=400, request_frequency=35, connection_status="failed"),
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-database", destination_port=5432, packet_count=5_000, byte_count=8_000_000, flow_duration_ms=1_000, request_frequency=45, connection_status="failed"),
        ]
    if scenario == "reconnaissance":
        return [
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=22, packet_count=20, byte_count=2_000, request_frequency=40, connection_status="failed"),
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=23, packet_count=20, byte_count=2_000, request_frequency=40, connection_status="failed"),
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=3389, packet_count=20, byte_count=2_000, request_frequency=40, connection_status="failed"),
        ]
    if scenario == "progression":
        return [
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-server-a", destination_port=22, packet_count=20, byte_count=2_000, request_frequency=40, connection_status="failed"),
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-database", destination_port=5432, packet_count=100, byte_count=80_000, request_frequency=30, connection_status="failed"),
            NetworkTrafficCreate(source_ip="demo-device-a", destination_ip="demo-database", destination_port=5432, packet_count=5_000, byte_count=8_000_000, request_frequency=45, connection_status="failed"),
        ]
    raise ValueError("Demo scenario must be 'normal', 'reconnaissance', 'progression', or 'suspicious'")
