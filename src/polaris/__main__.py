"""
Polaris CLI entry point.

Usage:
    python -m polaris speedtest
    python -m polaris weather
"""

from polaris.speedtest.client import run_speedtest
from polaris.weather.client import run_weather


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Polaris CLI")
    parser.add_argument(
        "command",
        choices=["speedtest", "weather"],
        help="Which tool to run",
    )
    args = parser.parse_args()

    if args.command == "speedtest":
        print(run_speedtest())
    elif args.command == "weather":
        print(run_weather())


if __name__ == "__main__":
    main()