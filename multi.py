#!/usr/bin/env python3
"""
Multi - 1xBet Accumulator Helper (Free, No Paid API)
Supports rich multi-line match format + improved auto mode attempt
"""

import argparse
import re
import sys
import time
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

INPUT_FILE = Path("matches_input.txt")
EXAMPLE_FILE = Path("matches_input.example.txt")


@dataclass
class MatchSelection:
    number: int
    league: str
    home: str
    away: str
    date_time: str
    prediction: str
    odds: Optional[str] = None
    market_clean: str = ""

    @property
    def teams(self) -> str:
        return f"{self.home} vs {self.away}"

    @property
    def search_query(self) -> str:
        # Prefer shorter unique team name for search
        return self.home if len(self.home) <= len(self.away) else self.away


def parse_rich_format(text: str) -> List[MatchSelection]:
    selections = []
    blocks = re.split(r"\n(?=\d+\.\s)", text.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if len(lines) < 3:
            continue

        m = re.match(r"^(\d+)\.\s*(.+)$", lines[0])
        if not m:
            continue
        number = int(m.group(1))
        league = m.group(2).strip()

        teams_line = lines[1]
        if " vs " in teams_line.lower():
            parts = re.split(r"\s+vs\s+", teams_line, flags=re.IGNORECASE)
            home = parts[0].strip()
            away = parts[1].strip() if len(parts) > 1 else ""
        else:
            home = teams_line
            away = ""

        date_time = lines[2] if len(lines) > 2 else ""

        prediction = ""
        odds = None
        for line in lines[3:]:
            if line.lower().startswith("prediction:"):
                prediction = line[len("Prediction:"):].strip()
                odds_match = re.search(r"\(Odds?:\s*([0-9.]+)\)", prediction, re.IGNORECASE)
                if odds_match:
                    odds = odds_match.group(1)
                break

        if not prediction:
            prediction = " ".join(lines[3:])

        market_clean = clean_market(prediction)

        selections.append(MatchSelection(
            number=number,
            league=league,
            home=home,
            away=away,
            date_time=date_time,
            prediction=prediction,
            odds=odds,
            market_clean=market_clean
        ))

    return selections


def clean_market(prediction: str) -> str:
    p = prediction.strip()
    p = re.sub(r"\s*\(Odds?:\s*[0-9.]+\)", "", p, flags=re.IGNORECASE).strip()

    replacements = [
        (r"Regular time,?\s*1X2:\s*W1", "1X2 → Home Win (1)"),
        (r"Regular time,?\s*1X2:\s*W2", "1X2 → Away Win (2)"),
        (r"Regular time,?\s*1X2:\s*X", "1X2 → Draw (X)"),
        (r"Regular time,?\s*Double Chance:\s*1X", "Double Chance → 1X"),
        (r"Regular time,?\s*Double Chance:\s*12", "Double Chance → 12"),
        (r"Regular time,?\s*Double Chance:\s*2X", "Double Chance → 2X"),
        (r"Double Chance \+ Both Teams To Score:\s*2X And Both To Score - Yes",
         "Double Chance 2X + BTTS Yes"),
        (r"Double Chance \+ Both Teams To Score:\s*1X And Both To Score - Yes",
         "Double Chance 1X + BTTS Yes"),
        (r"Both Teams To Score:?\s*Yes", "BTTS Yes"),
        (r"Both Teams To Score:?\s*No", "BTTS No"),
        (r"Yellow Cards,?\s*Total 1:\s*\(1\.5\)\s*Over", "Yellow Cards → Total Over 1.5"),
        (r"Shots On Target,?\s*1X2:\s*W2", "Shots On Target → Away (2)"),
        (r"Shots On Target,?\s*1X2:\s*W1", "Shots On Target → Home (1)"),
    ]

    for pattern, repl in replacements:
        p = re.sub(pattern, repl, p, flags=re.IGNORECASE)

    return p


def print_checklist(selections: List[MatchSelection]):
    print("\n" + "=" * 70)
    print("  MULTI ACCUMULATOR CHECKLIST")
    print("=" * 70)
    print("Open 1xBet → Search by Team name (or Date) → Select the market\n")

    for s in selections:
        print(f"{s.number:2d}. {s.league}")
        print(f"    {s.home}  vs  {s.away}")
        print(f"    Date : {s.date_time}")
        print(f"    → Select: {s.market_clean}")
        if s.odds:
            print(f"    Odds : {s.odds}")
        print()

    print("-" * 70)
    print(f"Total selections: {len(selections)}")
    print("After selecting all → Bet Slip → Share / Save Code")
    print("=" * 70)
    print()


def try_auto_mode(selections: List[MatchSelection]):
    print("\n" + "=" * 70)
    print("  AUTO MODE - Best Effort Automation")
    print("=" * 70)
    print("1xBet anti-bot strong. Script will:")
    print("  - Open browser (visible)")
    print("  - Search each match")
    print("  - Try to click markets")
    print("  - Keep browser open so you can finish + copy Save Code")
    print("=" * 70 + "\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] Install first:")
        print("    pip install playwright")
        print("    playwright install chromium")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
        )

        # Stealth-ish
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()

        # Try open 1xBet
        urls = [
            "https://1xbet.com/en",
            "https://1xbet.com",
            "https://1xbet.com/en/line",
        ]

        opened = False
        for url in urls:
            try:
                print(f"[+] Opening {url} ...")
                page.goto(url, timeout=45000, wait_until="domcontentloaded")
                time.sleep(3)
                opened = True
                print("[+] Page loaded")
                break
            except Exception as e:
                print(f"    Failed: {e}")

        if not opened:
            print("[!] Could not open 1xBet. Showing checklist instead.")
            print_checklist(selections)
            browser.close()
            return

        print("\n[!] Browser is open.")
        print("[!] Script will try to search matches one by one.")
        print("[!] If it gets stuck / captcha / blocked → you finish manually.")
        print("[!] After all selections → go to Bet Slip → Share / Save Code\n")

        for s in selections:
            print(f"\n--- [{s.number}] {s.teams} ---")
            print(f"    Market: {s.market_clean}")
            print(f"    Searching for: {s.search_query}")

            try:
                # Try to find search box (common selectors)
                search_selectors = [
                    "input[placeholder*='Search']",
                    "input[placeholder*='search']",
                    "input[type='search']",
                    ".search-input input",
                    "#search",
                    "input.search",
                ]

                search_box = None
                for sel in search_selectors:
                    try:
                        el = page.query_selector(sel)
                        if el:
                            search_box = el
                            break
                    except:
                        pass

                if search_box:
                    search_box.click()
                    search_box.fill("")
                    search_box.type(s.search_query, delay=80)
                    time.sleep(2)
                    page.keyboard.press("Enter")
                    time.sleep(2.5)
                    print("    Search submitted")
                else:
                    print("    [!] Search box not found automatically")
                    print("    → Please search manually for:", s.teams)

                # Give time for results
                time.sleep(2)

            except Exception as e:
                print(f"    Search error: {e}")

            print(f"    → Now select: {s.market_clean}")
            print("    (Script waits 8 sec for you to click if needed)")
            time.sleep(8)

        print("\n" + "=" * 70)
        print("  ALL MATCHES PROCESSED")
        print("=" * 70)
        print("1. Check Bet Slip (right side)")
        print("2. Click Share / Save Code / Coupon")
        print("3. Copy the code")
        print("4. Browser will stay open 3 more minutes")
        print("=" * 70 + "\n")

        # Keep open so user can finish and copy code
        page.wait_for_timeout(180000)
        browser.close()
        print("[+] Browser closed.")


def main():
    parser = argparse.ArgumentParser(description="Multi - 1xBet Accumulator Helper")
    parser.add_argument("--auto", action="store_true", help="Try automatic browser mode (best effort)")
    parser.add_argument("--input", default=str(INPUT_FILE), help="Input file path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] {input_path} not found.")
        if EXAMPLE_FILE.exists():
            print(f"    Copy {EXAMPLE_FILE} → {input_path} and paste your list.")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    selections = parse_rich_format(text)

    if not selections:
        print("[!] No valid matches found. Check the format.")
        print("    Expected format example is in matches_input.example.txt")
        sys.exit(1)

    print(f"Loaded {len(selections)} selections successfully.\n")

    if args.auto:
        try_auto_mode(selections)
    else:
        print_checklist(selections)
        print("Tip: python multi.py --auto")
        print("     (Browser will open, try to search matches, you finish + copy Save Code)")


if __name__ == "__main__":
    main()
