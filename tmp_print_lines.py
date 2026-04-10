from pathlib import Path
start, end = 2740, 2870
lines = Path(r'c:/Users/Lipe/Desktop/Portfolio/DnD-Companion/gui/character_sheet_tab.py').read_text(encoding='utf-8').splitlines()
for i in range(start, min(end, len(lines))):
    print(f"{i+1:04d}: {lines[i]}")
