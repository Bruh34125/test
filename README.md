# Undertale AU Python Prototype (Piece 3)

This is **piece 3**: a playable multi-AU prototype with cross-AU relic progression and ending checks.

## Features

- 3 starter AUs with unique metadata (`core_fell_swap`, `echo_shift`, `gilded_rune`)
- AU switching in overworld (`Q`/`E`)
- Battle behavior driven by AU data (`enemy_hp`, `fight_bonus`, `act_line`, `reward_item`)
- Cross-AU inventory rewards and synergies:
  - `blade_fragment`: extra FIGHT damage
  - `mercy_charm`: MERCY weakens hostility
  - `rune_sigil`: tracked for triune ending
- Convergence/ending scene (`C` in overworld) with route evaluation
- Save/load persistence with JSON
- Bulk AU import script for Fandom Category:AUs (with NSFW name filtering)

## Import many AUs from Fandom

Use the provided importer script to crawl category pagination and generate `aus/<id>/au.json` entries:

```bash
python scripts/import_aus_from_fandom.py
```

Importer behavior:
- Source: `https://undertale-au.fandom.com/wiki/Category:AUs`
- Excludes AU names that match NSFW keywords (`nsfw`, `18+`, `porn`, `hentai`, `lust`, etc.)
- Writes import summary to `data/au_import_report.json`

## Controls

- Title: `N` new game, `L` load
- Overworld: arrows move, `Z` talk, `X` battle, `S` save, `Q/E` switch AU, `C` convergence/endings
- Dialogue/Battle: `Z` confirm; battle uses `LEFT/RIGHT` to select actions; `X` exits battle

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

## Zip build artifact

From repo root:

```bash
zip -r undertale_au_piece3.zip . -x ".git/*" "__pycache__/*" "*.pyc" ".venv/*"
```
