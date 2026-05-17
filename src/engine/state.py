from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class GameState:
    player_name: str = "FRISK"
    hp: int = 20
    max_hp: int = 20
    lv: int = 1
    gold: int = 0
    current_au: str = "core_fell_swap"
    scene: str = "title"
    route_flags: Dict[str, Any] = field(default_factory=lambda: {
        "spared": 0,
        "defeated": 0,
        "kindness": 0,
        "violence": 0,
    })
    progress_flags: Dict[str, Any] = field(default_factory=dict)
    inventory: List[str] = field(default_factory=list)
