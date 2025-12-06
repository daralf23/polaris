import speedtest
from .models import SpeedTestResult

class SpeedTestClient:

    def run_test(self) -> SpeedTestResult:
        st = speedtest.Speedtest()

        st.get_best_server()
        download = st.download()
        upload = st.upload()
        ping = st.results.ping

        # Convert bits/sec → Mbps for readability
        download_mbps = round(download / 1_000_000, 2)
        upload_mbps = round(upload / 1_000_000, 2)
        ping_ms = round(ping, 2)

        return SpeedTestResult(
            ping_ms=ping_ms,
            download_mbps=download_mbps,
            upload_mbps=upload_mbps
        )