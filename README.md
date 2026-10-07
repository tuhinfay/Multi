# Multi - Accumulator Helper (Free)

Local tool to help build multi/accumulator bets and get the **Event code**.

## How it works

1. Paste your match list in the given format
2. Run the script
3. Browser opens (then minimizes)
4. Script tries to search matches and reach Save/load events
5. Event code is saved inside the `output/` folder

## Setup (Windows CMD)

```cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/tuhinfay/Multi.git
cd Multi

pip install -r requirements.txt
playwright install chromium

copy matches_input.example.txt matches_input.txt
notepad matches_input.txt
```

Paste your matches, then save the file.

## Run

**Checklist only:**
```cmd
python multi.py
```

**Full auto (browser minimizes, tries to get code):**
```cmd
python multi.py --auto
```

## Input format (`matches_input.txt`)

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

## Output

All generated files go into the `output/` folder:

- `checklist_YYYY-MM-DD_HH-MM-SS.txt` — clean selection list
- `event_code_YYYY-MM-DD_HH-MM-SS.txt` — the Event code (when detected)

## Notes

- Browser starts minimized so you can do other work
- If search or market click fails, restore the browser and click manually
- Script continues and waits for you
- Final step: Bet Slip → Save/load events → Save → copy code

## Requirements

- Python 3.10+
- playwright

```cmd
pip install -r requirements.txt
playwright install chromium
```

## Disclaimer

For personal educational use only. Bet responsibly.
