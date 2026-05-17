import pygame
from .base import Scene


class DialogueScene(Scene):
    def on_enter(self):
        self.font = pygame.font.SysFont("consolas", 22)
        self.idx = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            self.idx += 1
            if self.idx >= len(self.game.dialogue_lines):
                self.game.state.scene = "overworld"
                self.game.scene_manager.switch("overworld")

    def draw(self, surface):
        surface.fill((0, 0, 0))
        box = pygame.Rect(40, 300, 560, 140)
        pygame.draw.rect(surface, (255, 255, 255), box, 3)
        if self.game.dialogue_lines:
            line = self.game.dialogue_lines[min(self.idx, len(self.game.dialogue_lines)-1)]
            text = self.font.render(line, True, (255, 255, 255))
            surface.blit(text, (60, 350))
