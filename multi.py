#!/usr/bin/env python3
"""
Multi - 1xBet Accumulator Helper (Free)
Local auto mode: add matches to Bet Slip, click Save/load events, try to get Event code.
Based on real flow from bd.1xbet.com (Save/load events → Save → code like 9B93C)
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
        return self.home if len(self.home) <= 22 else self.home.split()[0]


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
        (r"Regular time,?\s*1X2:\s*W1", "1 (Home)"),
        (r"Regular time,?\s*1X2:\s*W2", "2 (Away)"),
        (r"Regular time,?\s*1X2:\s*X", "X (Draw)"),
        (r"Regular time,?\s*Double Chance:\s*1X", "1X"),
        (r"Regular time,?\s*Double Chance:\s*12", "12"),
        (r"Regular time,?\s*Double Chance:\s*2X", "2X"),
        (r"Double Chance \+ Both Teams To Score:\s*2X And Both To Score - Yes", "2X + BTTS Yes"),
        (r"Double Chance \+ Both Teams To Score:\s*1X And Both To Score - Yes", "1X + BTTS Yes"),
        (r"Both Teams To Score:?\s*Yes", "BTTS Yes"),
        (r"Both Teams To Score:?\s*No", "BTTS No"),
        (r"Yellow Cards,?\s*Total 1:\s*\(1\.5\)\s*Over", "Yellow Cards Over 1.5"),
        (r"Shots On Target,?\s*1X2:\s*W2", "Shots On Target 2"),
        (r"Shots On Target,?\s*1X2:\s*W1", "Shots On Target 1"),
    ]

    for pattern, repl in replacements:
        p = re.sub(pattern, repl, p, flags=re.IGNORECASE)

    return p


def print_checklist(selections: List[MatchSelection]):
    print("\n" + "=" * 70)
    print("  MULTI ACCUMULATOR CHECKLIST")
    print("=" * 70)
    for s in selections:
        print(f"{s.number:2d}. {s.league}")
        print(f"    {s.home}  vs  {s.away}")
        print(f"    Date : {s.date_time}")
        print(f"    → Select: {s.market_clean}")
        if s.odds:
            print(f"    Odds : {s.odds}")
        print()
    print("-" * 70)
    print(f"Total: {len(selections)} selections")
    print("After all selected → Bet Slip → Save/load events → Save → copy code")
    print("=" * 70)


def try_auto_mode(selections: List[MatchSelection]):
    print("\n" + "=" * 70)
    print("  LOCAL AUTO MODE (bd.1xbet.com style)")
    print("=" * 70)
    print("Goal:")
    print("  1. Open 1xBet")
    print("  2. Help you add matches to Bet Slip (Accumulator)")
    print("  3. Click Save/load events → Save")
    print("  4. Try to read the Event code (like 9B93C)")
    print("Browser stays open. You can click markets if needed.")
    print("=" * 70 + "\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[!] First install:")
        print("    pip install playwright")
        print("    playwright install chromium")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--start-maximized",
            ]
        )
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)

        page = context.new_page()

        # Prefer Bangladesh domain (from your video)
        urls = [
            "https://bd.1xbet.com/en",
            "https://bd.1xbet.com/en/line",
            "https://1xbet.com/en",
            "https://1xbet.com",
        ]

        opened = False
        for url in urls:
            try:
                print(f"[+] Opening {url}")
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(4)
                opened = True
                print("[+] Page loaded")
                break
            except Exception as e:
                print(f"    Failed: {e}")

        if not opened:
            print("[!] Could not open 1xBet")
            print_checklist(selections)
            browser.close()
            return

        print("\n[!] If any popup/captcha appears → close/solve it manually.")
        print("[!] Script will now go through each match.\n")

        for idx, s in enumerate(selections, 1):
            print(f"\n========== [{idx}/{len(selections)}] {s.teams} ==========")
            print(f"League : {s.league}")
            print(f"Market : {s.market_clean}")
            print(f"Search : {s.search_query}")

            try:
                # Search box selectors (common on 1xBet)
                search_box = None
                for sel in [
                    "input[placeholder*='Search']",
                    "input[placeholder*='search']",
                    "input[placeholder*='match']",
                    "input[type='search']",
                    ".search input",
                    "#search-input",
                    "input.search-input",
                    "[class*='search'] input",
                ]:
                    try:
                        el = page.query_selector(sel)
                        if el and el.is_visible():
                            search_box = el
                            break
                    except:
                        pass

                if search_box:
                    search_box.click()
                    time.sleep(0.3)
                    search_box.fill("")
                    search_box.type(s.search_query, delay=50)
                    time.sleep(1.2)
                    page.keyboard.press("Enter")
                    print("    → Search submitted")
                    time.sleep(3)
                else:
                    print("    [!] Search box not found automatically")
                    print(f"    → Please search manually for: {s.teams}")
                    print("    Waiting 15 seconds for you...")
                    time.sleep(15)

                print(f"    → Click the correct market: {s.market_clean}")
                print("    Waiting 12 seconds (you can click if needed)...")
                time.sleep(12)

            except Exception as e:
                print(f"    Error: {e}")
                time.sleep(3)

        # ========== After all matches: try Save/load events ==========
        print("\n" + "=" * 70)
        print("  TRYING TO GENERATE EVENT CODE")
        print("=" * 70)
        print("Looking for 'Save/load events' button (as in your video)...")

        code_found = None

        try:
            # Click "Save/load events"
            save_load_clicked = False
            for sel in [
                "text=Save/load events",
                "text=Save/load",
                "text=Save / load events",
                "a:has-text('Save/load')",
                "[class*='save']",
                "text=Save",
            ]:
                try:
                    el = page.query_selector(sel)
                    if el and el.is_visible():
                        el.scroll_into_view_if_needed()
                        time.sleep(0.5)
                        el.click()
                        print(f"[+] Clicked: {sel}")
                        save_load_clicked = True
                        time.sleep(2)
                        break
                except:
                    pass

            if not save_load_clicked:
                print("[!] Could not auto-click 'Save/load events'")
                print("    → Please click it yourself on the Bet Slip (right side)")
                print("    Waiting 20 seconds...")
                time.sleep(20)

            # Now try to click the green Save button and read the code
            time.sleep(1)

            # Look for Event code input or the generated code
            for sel in [
                "input[placeholder*='code']",
                "input[placeholder*='Code']",
                "input[placeholder*='Event']",
                ".event-code input",
                "input[type='text']",
            ]:
                try:
                    inputs = page.query_selector_all(sel)
                    for inp in inputs:
                        if inp.is_visible():
                            val = inp.input_value()
                            if val and len(val) >= 4 and len(val) <= 12:
                                code_found = val.strip()
                                print(f"[+] Found code in input: {code_found}")
                                break
                    if code_found:
                        break
                except:
                    pass

            # Try clicking Save button if code not yet there
            if not code_found:
                for sel in [
                    "button:has-text('Save')",
                    "text=Save",
                    "button.green",
                    "[class*='save'] button",
                ]:
                    try:
                        btn = page.query_selector(sel)
                        if btn and btn.is_visible():
                            btn.click()
                            print("[+] Clicked Save button")
                            time.sleep(2)
                            break
                    except:
                        pass

                # Re-check input after Save
                time.sleep(1)
                for sel in [
                    "input[placeholder*='code']",
                    "input[placeholder*='Code']",
                    "input[placeholder*='Event']",
                    "input[type='text']",
                ]:
                    try:
                        inputs = page.query_selector_all(sel)
                        for inp in inputs:
                            if inp.is_visible():
                                val = inp.input_value()
                                if val and len(val) >= 4 and len(val) <= 12:
                                    code_found = val.strip()
                                    print(f"[+] Code after Save: {code_found}")
                                    break
                        if code_found:
                            break
                    except:
                        pass

        except Exception as e:
            print(f"[!] Error while trying to save: {e}")

        print("\n" + "=" * 70)
        if code_found:
            print(f"  SUCCESS! Event code: {code_found}")
        else:
            print("  Code not auto-detected")
            print("  Please do this manually:")
            print("  1. Check Bet Slip has all your selections (Accumulator)")
            print("  2. Click 'Save/load events'")
            print("  3. Click green 'Save' button")
            print("  4. Copy the Event code (e.g. 9B93C)")
        print("=" * 70)
        print("\nBrowser will stay open 5 minutes so you can finish & copy code.")
        print("Press Ctrl+C in terminal when done.\n")

        try:
            page.wait_for_timeout(300000)  # 5 minutes
        except KeyboardInterrupt:
            pass

        browser.close()
        print("[+] Browser closed.")


def main():
    parser = argparse.ArgumentParser(description="Multi - 1xBet Accumulator Helper")
    parser.add_argument("--auto", action="store_true", help="Local full selection + Save code attempt")
    parser.add_argument("--input", default=str(INPUT_FILE))
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] {input_path} not found.")
        if EXAMPLE_FILE.exists():
            print(f"    Copy {EXAMPLE_FILE} → {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    selections = parse_rich_format(text)

    if not selections:
        print("[!] No valid matches found.")
        sys.exit(1)

    print(f"Loaded {len(selections)} selections.\n")

    if args.auto:
        try_auto_mode(selections)
    else:
        print_checklist(selections)
        print("\nTo try full auto on local PC (bd.1xbet.com style):")
        print("  python multi.py --auto")


if __name__ == "__main__":
    main()
