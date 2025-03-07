import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer

pygame.mixer.init() # iniciei o metodo do mixer
powerup = pygame.mixer.Sound('dino_runner/assets/other/PowerUp.wav')
powerupend = pygame.mixer.Sound('dino_runner/assets/other/PowerUpEnd.wav')
up = pygame.mixer.Sound('dino_runner/assets/other/Up.wav')

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            ups = random.randint (0, 100)
            if ups % 2 == 0:
                self.when_appears += random.randint(300, 400)
                self.power_ups.append(Shield())
            elif ups % 2 == 1:
                self.when_appears += random.randint (300, 400)
                self.power_ups.append(Hammer())

    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                powerup.play()
                up.play()
                power_up.start_time = pygame.time.get_ticks()
                player.shield = False
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        powerupend.play()
        self.power_ups = []
        self.when_appears = random.randint(200, 300)