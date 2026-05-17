import json
from dataclasses import asdict
from pathlib import Path
from .state import GameState

SAVE_PATH = Path("savegame.json")


def save_game(state: GameState) -> None:
    SAVE_PATH.write_text(json.dumps(asdict(state), indent=2))


def load_game() -> GameState:
    if not SAVE_PATH.exists():
        return GameState()
    data = json.loads(SAVE_PATH.read_text())
    return GameState(**data)
