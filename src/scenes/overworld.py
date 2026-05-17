import pygame
from .base import Scene


class OverworldScene(Scene):
    def on_enter(self):
        self.x, self.y = 320, 240
        self.speed = 180
        self.font = pygame.font.SysFont("consolas", 18)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                au = self.game.aus.get(self.game.state.current_au, {})
                self.game.dialogue_lines = [
                    "A strange timeline hums around you.",
                    f"Current AU: {self.game.state.current_au}",
                    f"Trait: {au.get('special_rule', 'Unknown')}",
                    "Defeat foes to collect relics shared across AUs.",
                ]
                self.game.state.scene = "dialogue"
                self.game.scene_manager.switch("dialogue")
            elif event.key == pygame.K_x:
                self.game.state.scene = "battle"
                self.game.scene_manager.switch("battle")
            elif event.key == pygame.K_s:
                self.game.save()
            elif event.key == pygame.K_q:
                self.game.cycle_au(-1)
            elif event.key == pygame.K_e:
                self.game.cycle_au(1)
            elif event.key == pygame.K_c:
                self.game.state.scene = "ending"
                self.game.scene_manager.switch("ending")

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed * dt
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed * dt
        self.x = max(10, min(630, self.x + dx))
        self.y = max(10, min(470, self.y + dy))

    def draw(self, surface):
        surface.fill((20, 20, 30))
        pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, 14, 14))
        au_name = self.game.aus.get(self.game.state.current_au, {}).get("name", self.game.state.current_au)
        inv = ", ".join(self.game.state.inventory) if self.game.state.inventory else "(none)"
        ui1 = self.font.render("Arrows move | Z talk | X battle | S save", True, (255, 255, 255))
        ui2 = self.font.render("Q/E change AU | C convergence/endings", True, (200, 220, 255))
        ui3 = self.font.render(f"AU: {au_name}", True, (255, 255, 100))
        ui4 = self.font.render(f"Cross-AU gear: {inv}", True, (180, 255, 180))
        surface.blit(ui1, (10, 10))
        surface.blit(ui2, (10, 32))
        surface.blit(ui3, (10, 54))
        surface.blit(ui4, (10, 76))
