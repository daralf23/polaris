from dataclasses import dataclass

@dataclass
class SpeedTestResult:
    ping_ms: float
    download_mbps: float
    upload_mbps: float