import pygame
from engine.state import GameState
from engine.save import save_game, load_game
from engine.au_loader import load_aus
from engine.scene_manager import SceneManager
from scenes.title import TitleScene
from scenes.overworld import OverworldScene
from scenes.dialogue import DialogueScene
from scenes.battle import BattleScene
from scenes.ending import EndingScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Undertale AU Prototype - Piece 3")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState()
        self.dialogue_lines = []
        self.aus = load_aus()

        self.scene_manager = SceneManager()
        self.scene_manager.register("title", TitleScene(self))
        self.scene_manager.register("overworld", OverworldScene(self))
        self.scene_manager.register("dialogue", DialogueScene(self))
        self.scene_manager.register("battle", BattleScene(self))
        self.scene_manager.register("ending", EndingScene(self))
        self.scene_manager.switch("title")

    def cycle_au(self, direction: int):
        if not self.aus:
            return
        ids = sorted(self.aus.keys())
        current = self.state.current_au
        idx = ids.index(current) if current in ids else 0
        self.state.current_au = ids[(idx + direction) % len(ids)]

    def compute_endings(self):
        flags = self.state.route_flags
        inv = set(self.state.inventory)
        endings = []

        if flags["kindness"] >= flags["violence"] and flags["spared"] >= 3:
            endings.append("Pacifist Drift: Your mercy knits fractured worlds.")
        if flags["violence"] >= 5:
            endings.append("Ruin Route: Power conquers, but timelines decay.")
        if {"blade_fragment", "mercy_charm", "rune_sigil"}.issubset(inv):
            endings.append("Triune Route: Three relics stabilize the multiverse.")
        if not endings:
            endings.append("Neutral Route: The story is still being written.")

        endings.append(f"Stats K:{flags['kindness']} V:{flags['violence']} S:{flags['spared']}")
        endings.append(f"Gear: {', '.join(self.state.inventory) if self.state.inventory else '(none)'}")
        return endings

    def save(self):
        save_game(self.state)

    def load(self):
        self.state = load_game()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.scene_manager.handle_event(event)
            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
