# Multi - 1xBet Accumulator Helper (Free)

Free tool to help build accumulator (multi) bets on 1xBet.

**No paid API. No paid service.**

## New Easy Input Format (Recommended)

Just paste the full prediction list like this:

```
1. Europe. UEFA Nations League
Germany vs Serbia
02.10.2026 (12:45 am)
Prediction: Regular time, 1X2: W1 (Odds: 1.22)

2. Europe. UEFA Nations League
Greece vs Netherlands
02.10.2026 (12:45 am)
Prediction: Shots On Target, 1X2: W2 (Odds: 1.65)

3. Europe. UEFA Nations League
Denmark vs Portugal
02.10.2026 (12:45 am)
Prediction: Yellow Cards, Total 1: (1.5) Over (Odds: 1.79)

4. Europe. UEFA Nations League
Wales vs Norway
02.10.2026 (12:45 am)
Prediction: Regular time, 1X2: W2 (Odds: 1.432)

5. Colombia. Primera A
Internacional de Bogota vs Once Caldas
02.10.2026 (07:00 am)
Prediction: Regular time, Double Chance: 2X (Odds: 1.37)

6. Club Friendly (Women)
Austria Wien (Women) vs Internazionale Milano (Women)
01.10.2026 (10:45 pm)
Prediction: Regular time, Double Chance + Both Teams To Score: 2X And Both To Score - Yes (Odds: 2.17)
```

### How matching works
- First tries exact **Team vs Team** name
- If not perfect → uses **Date** to confirm the correct match
- League / Country helps reduce wrong selection

## How to use

1. Copy the example file:
```bash
cp matches_input.example.txt matches_input.txt
```

2. Paste your full list into `matches_input.txt`

3. Run:
```bash
pip install -r requirements.txt
python multi.py
```

It will show a clean checklist with:
- League
- Teams
- Date & Time
- Exact market to select
- Odds

Then you just open 1xBet and follow the checklist quickly.

### Auto mode (experimental)
```bash
python multi.py --auto
```

## Supported Markets (examples)

- Regular time, 1X2: W1 / W2 / X
- Double Chance: 1X / 12 / 2X
- Both Teams To Score: Yes / No
- Double Chance + BTTS combinations
- Total Over/Under (1.5, 2.5, 3.5...)
- Yellow Cards Total
- Shots On Target 1X2
- Asian Handicap
- Any other text you write will be shown as-is

## Requirements

```bash
pip install -r requirements.txt
playwright install chromium   # only needed for --auto
```

## Disclaimer

- For personal educational use only
- Respect 1xBet Terms of Service
- Gambling involves risk. Bet responsibly.

---

Made for free use. No paid API required.
