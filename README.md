# Multi - 1xBet Accumulator Helper (Free)

Free tool to help build accumulator (multi) bets on 1xBet.

**No paid API. No paid service.**

## What it does

1. You give a list of matches + desired market (example: W1, BTTS Yes, Over 2.5, Double Chance 2X, etc.)
2. The tool tries to find those matches on 1xBet
3. It selects the odds one by one
4. Tries to generate / show the accumulator coupon code

## Important Reality Check

1xBet uses strong anti-bot protection (Cloudflare + dynamic JS).  
Fully automatic free scraping + clicking is **very unstable** and often fails.

This project has **two modes**:

### Mode 1: Assisted (Recommended - Most Reliable)
- You paste match list + markets
- Tool generates a clean checklist
- You open 1xBet and select quickly following the checklist
- Much faster and works every day

### Mode 2: Auto Attempt (Playwright)
- Tries to open 1xBet and click automatically
- May work sometimes, may get blocked
- Needs local browser

## How to use (Assisted Mode - Recommended)

1. Copy `matches_input.example.txt` → rename to `matches_input.txt`
2. Edit the file with your matches and markets
3. Run:

```bash
pip install -r requirements.txt
python multi.py
```

### Input Format (`matches_input.txt`)

```
Team A vs Team B | W1
Team C vs Team D | BTTS Yes
Team E vs Team F | Over 2.5
Team G vs Team H | Double Chance 2X
```

Supported market keywords (case insensitive):
- `W1` / `1` / `Home`
- `W2` / `2` / `Away`
- `X` / `Draw`
- `1X` / `12` / `X2` (Double Chance)
- `BTTS Yes` / `BTTS No` / `GG` / `NG`
- `Over 2.5` / `Under 2.5` / `Over 1.5` / `Under 1.5` / `Over 3.5` etc.
- Any other market text will be searched as-is

## How to use (Auto Mode)

```bash
python multi.py --auto
```

## Requirements

- Python 3.10+

```bash
pip install -r requirements.txt
playwright install chromium
```

## Disclaimer

- For personal educational use only
- Respect 1xBet Terms of Service
- Gambling involves risk. Bet responsibly.

---

Made for free use. No paid API required.
