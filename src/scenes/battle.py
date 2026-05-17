import pygame
from .base import Scene


class BattleScene(Scene):
    def on_enter(self):
        self.font = pygame.font.SysFont("consolas", 20)
        self.menu = ["FIGHT", "ACT", "ITEM", "MERCY"]
        self.cursor = 0
        self.enemy_hp = 30
        self.message = "A fractured echo blocks your way."

        au = self.game.aus.get(self.game.state.current_au, {})
        self.enemy_hp = int(au.get("enemy_hp", 30))
        self.reward = au.get("reward_item")
        self.act_line = au.get("act_line", "You reach out to this timeline.")
        self.fight_bonus = int(au.get("fight_bonus", 0))

        if "blade_fragment" in self.game.state.inventory:
            self.fight_bonus += 2
        if "mercy_charm" in self.game.state.inventory:
            self.message = "Your MERCY pulses with calm certainty."

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.cursor = (self.cursor - 1) % len(self.menu)
            elif event.key == pygame.K_RIGHT:
                self.cursor = (self.cursor + 1) % len(self.menu)
            elif event.key == pygame.K_z:
                choice = self.menu[self.cursor]
                if choice == "FIGHT":
                    self.enemy_hp -= (5 + self.fight_bonus)
                    self.game.state.route_flags["violence"] += 1
                    self.message = f"You strike. Enemy HP: {max(0, self.enemy_hp)}"
                elif choice == "ACT":
                    self.game.state.route_flags["kindness"] += 1
                    self.message = self.act_line
                elif choice == "MERCY":
                    self.game.state.route_flags["spared"] += 1
                    self.message = "You offer mercy."
                    if "mercy_charm" in self.game.state.inventory:
                        self.enemy_hp -= 4
                        self.message += " The charm weakens hostility."
                else:
                    self.message = "No consumable items yet."

                if self.enemy_hp <= 0:
                    self.game.state.route_flags["defeated"] += 1
                    if self.reward and self.reward not in self.game.state.inventory:
                        self.game.state.inventory.append(self.reward)
                    self.game.state.scene = "overworld"
                    self.game.scene_manager.switch("overworld")
            elif event.key == pygame.K_x:
                self.game.state.scene = "overworld"
                self.game.scene_manager.switch("overworld")

    def draw(self, surface):
        surface.fill((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), (120, 90, 400, 120), 2)
        pygame.draw.rect(surface, (255, 255, 255), (50, 320, 540, 130), 2)

        hp_text = self.font.render(f"HP {self.game.state.hp}/{self.game.state.max_hp}", True, (255, 255, 255))
        au_text = self.font.render(f"AU: {self.game.state.current_au}", True, (150, 200, 255))
        msg_text = self.font.render(self.message, True, (255, 255, 0))
        surface.blit(hp_text, (60, 264))
        surface.blit(au_text, (240, 264))
        surface.blit(msg_text, (70, 340))

        for i, label in enumerate(self.menu):
            color = (255, 140, 0) if i == self.cursor else (255, 255, 255)
            txt = self.font.render(label, True, color)
            surface.blit(txt, (80 + i * 130, 400))
