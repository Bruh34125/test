import pygame
from .base import Scene


class EndingScene(Scene):
    def on_enter(self):
        self.font = pygame.font.SysFont("consolas", 22)
        self.small = pygame.font.SysFont("consolas", 18)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_z, pygame.K_x):
            self.game.state.scene = "overworld"
            self.game.scene_manager.switch("overworld")

    def draw(self, surface):
        surface.fill((0, 0, 0))
        endings = self.game.compute_endings()
        t1 = self.font.render("Timeline Convergence", True, (255, 255, 255))
        surface.blit(t1, (180, 60))

        y = 130
        for line in endings:
            txt = self.small.render(line, True, (200, 255, 200))
            surface.blit(txt, (60, y))
            y += 30

        hint = self.small.render("Z/X: Return to overworld", True, (180, 180, 180))
        surface.blit(hint, (200, 430))
