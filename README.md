# Multi - 1xBet Accumulator Helper (Free)

Local tool to help build accumulator and get **Event code** (Save/load events → Save) like `9B93C`.

Works with **bd.1xbet.com** flow shown in real usage.

## How the code is generated (from real site)

1. Add matches + markets to **Bet Slip** (Accumulator)
2. Click **Save/load events** (right side of bet slip)
3. Click green **Save**
4. Short **Event code** appears (e.g. `9B93C`)

## Usage (Windows CMD)

```cmd
cd %USERPROFILE%\Desktop
git clone https://github.com/tuhinfay/Multi.git
cd Multi

pip install -r requirements.txt
playwright install chromium

copy matches_input.example.txt matches_input.txt
notepad matches_input.txt

python multi.py --auto
```

## Modes

| Command | What it does |
|---------|--------------|
| `python multi.py` | Clean checklist only |
| `python multi.py --auto` | Opens browser, helps select matches, tries Save/load events + reads code |

## Notes

- Browser stays open so you can click markets / finish if script misses something
- Login not required for Save/load events (works as guest on many 1xBet domains)
- If search or market click fails → just click manually, script continues
- Final code appears in the Event code box after Save

## Disclaimer

Personal use. Respect 1xBet Terms. Bet responsibly.
