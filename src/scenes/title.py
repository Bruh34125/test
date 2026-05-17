import pygame
from .base import Scene


class TitleScene(Scene):
    def on_enter(self):
        self.font = pygame.font.SysFont("consolas", 28)
        self.small = pygame.font.SysFont("consolas", 18)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                self.game.state.scene = "overworld"
                self.game.scene_manager.switch("overworld")
            elif event.key == pygame.K_l:
                self.game.load()
                self.game.scene_manager.switch(self.game.state.scene)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        t1 = self.font.render("UNDERTALE AU PROTOTYPE", True, (255, 255, 255))
        t2 = self.small.render("N: New  |  L: Load", True, (200, 200, 200))
        surface.blit(t1, (120, 180))
        surface.blit(t2, (230, 240))
