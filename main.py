import sys
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.append(str(Path(__file__).parent / "src"))

import asyncio
from polaris.weather.client import WeatherBug

async def main():
    zone = os.getenv("ZONE", None)
    fc = WeatherBug(zone) 

    info = await fc.get_zone_info()
    print("Zone Info:", info)

    daily = await fc.get_daily_summary()
    print("\n=== Daily Summary ===")
    print(daily)

    alerts = await fc.get_alerts()
    print("\nAlerts:", alerts['features'])

if __name__ == "__main__":
    asyncio.run(main())
