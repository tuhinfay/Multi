#!/usr/bin/env python3
"""
Multi - 1xBet Accumulator Helper (Free, No Paid API)
"""

import argparse
import sys
from pathlib import Path

INPUT_FILE = Path("matches_input.txt")
EXAMPLE_FILE = Path("matches_input.example.txt")


def parse_input(file_path: Path):
    if not file_path.exists():
        print(f"[!] {file_path} not found.")
        if EXAMPLE_FILE.exists():
            print(f"    Copy {EXAMPLE_FILE} to {file_path} and edit it.")
        sys.exit(1)

    selections = []
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" not in line:
                print(f"[!] Skipping invalid line: {line}")
                continue
            match, market = line.split("|", 1)
            selections.append((match.strip(), market.strip()))
    return selections


def normalize_market(market: str) -> str:
    m = market.lower().strip()
    mapping = {
        "w1": "1", "home": "1", "1": "1",
        "w2": "2", "away": "2", "2": "2",
        "x": "X", "draw": "X",
        "1x": "1X", "x2": "X2", "12": "12",
        "btts yes": "Both Teams To Score - Yes", "gg": "Both Teams To Score - Yes",
        "btts no": "Both Teams To Score - No", "ng": "Both Teams To Score - No",
        "over 2.5": "Total Over 2.5", "under 2.5": "Total Under 2.5",
        "over 1.5": "Total Over 1.5", "under 1.5": "Total Under 1.5",
        "over 3.5": "Total Over 3.5", "under 3.5": "Total Under 3.5",
        "double chance 1x": "Double Chance 1X",
        "double chance x2": "Double Chance X2",
        "double chance 12": "Double Chance 12",
        "dc 1x": "Double Chance 1X",
        "dc x2": "Double Chance X2",
        "dc 12": "Double Chance 12",
    }
    return mapping.get(m, market)


def print_checklist(selections):
    print("\n" + "=" * 60)
    print("  MULTI ACCUMULATOR CHECKLIST (Assisted Mode)")
    print("=" * 60)
    print("Open 1xBet → Search each match → Select the market → Add to bet slip\n")

    for i, (match, market) in enumerate(selections, 1):
        clean_market = normalize_market(market)
        print(f"{i:2d}. {match}")
        print(f"    → Select: {clean_market}")
        print()

    print("-" * 60)
    print(f"Total selections: {len(selections)}")
    print("After selecting all → Bet Slip → Share / Get Coupon Code")
    print("=" * 60)


def try_auto_mode(selections):
    print("\n[Auto Mode] Trying Playwright...")
    print("Note: 1xBet anti-bot is strong. Success rate low.\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Install: pip install playwright && playwright install chromium")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        urls = ["https://1xbet.com", "https://1xbet.com/en"]
        opened = False
        for url in urls:
            try:
                print(f"Opening {url} ...")
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                opened = True
                break
            except Exception as e:
                print(f"  Failed: {e}")

        if not opened:
            print("[!] Could not open 1xBet. Using checklist instead.")
            print_checklist(selections)
            browser.close()
            return

        print("\nBrowser opened. Automatic clicking is unreliable.")
        print("Keeping open 2 minutes so you can finish the multi...")
        page.wait_for_timeout(120000)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Multi - 1xBet Accumulator Helper")
    parser.add_argument("--auto", action="store_true", help="Try automatic mode")
    parser.add_argument("--input", default=str(INPUT_FILE))
    args = parser.parse_args()

    selections = parse_input(Path(args.input))
    if not selections:
        print("[!] No valid matches found.")
        sys.exit(1)

    print(f"Loaded {len(selections)} selections.")

    if args.auto:
        try_auto_mode(selections)
    else:
        print_checklist(selections)
        print("Tip: python multi.py --auto  (for browser attempt)")


if __name__ == "__main__":
    main()
