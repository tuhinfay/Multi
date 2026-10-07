# Multi - 1xBet Accumulator Helper (Free)

Free tool to help build accumulator (multi) bets on 1xBet and get the **Save Code / Coupon Code**.

**No paid API.**

## Two Modes

### 1. Assisted Mode (Recommended & Reliable)
```bash
python multi.py
```
Gives clean checklist → you select fast on 1xBet → click **Share / Save Code**.

### 2. Auto Mode (Best Effort)
```bash
python multi.py --auto
```
- Opens real Chrome browser (visible)
- Tries to search each match
- Waits so you can click the market if needed
- Keeps browser open so you can go to Bet Slip → **Share / Save Code** and copy it

> 1xBet has strong anti-bot. Full 100% automatic is hard.  
> This mode helps as much as possible + lets you finish easily.

## Input Format (Easy)

Paste like this in `matches_input.txt`:

```
1. Europe. UEFA Nations League
Germany vs Serbia
02.10.2026 (12:45 am)
Prediction: Regular time, 1X2: W1 (Odds: 1.22)

2. Europe. UEFA Nations League
Greece vs Netherlands
02.10.2026 (12:45 am)
Prediction: Shots On Target, 1X2: W2 (Odds: 1.65)
```

## How to run

```bash
pip install -r requirements.txt
playwright install chromium

# Checklist only
python multi.py

# Auto attempt (browser opens)
python multi.py --auto
```

## Tips for higher success

1. First time run `--auto` and stay near the browser
2. If captcha / block appears → solve it manually
3. After all matches added → Bet Slip → Share / Save Code
4. Copy the code

## Disclaimer

- Personal educational use
- Respect 1xBet Terms
- Bet responsibly
