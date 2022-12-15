import pygame
import random
from dino_runner.components.obstacles.cactus import Cactus, Large_Cactus# importei o cacto maior
from dino_runner.components.obstacles.bird import Bird # importei arquivo do passaro
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD # importei variáveis globais

pygame.mixer.init() # iniciei o metodo do mixer
dead = pygame.mixer.Sound('dino_runner/assets/other/Dead.wav') # atribui valor na variavel dead

class ObstacleManager:
    def __init__ (self):
        self.obstacles = []

    def update (self, game):
        if len(self.obstacles) == 0: # se o tamanho da lista for 0 e é
            if random.randint (0, 2) == 0: # vai sortear 
                self.obstacles.append(Cactus(SMALL_CACTUS)) # o small cactus
            elif random.randint (0, 2) == 1: # copiei e colei
                self.obstacles.append(Large_Cactus(LARGE_CACTUS))
            elif random.randint (0, 2) == 2:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles: # para cada obstaculo que aparecer 
            obstacle.update(game.game_speed, self.obstacles) # mostra o obstaculo
            if game.player.dino_rect.colliderect(obstacle.rect): # se hitbox do dino colidir com a do obstaculo
                dead.play() # 15 - TOCA SOM DE MORTE
                game.score -= 1 # 15 - QUANDO MORRER, PEGA A PONTUACAO E SUBTRAI 1, PQ SEMPRE ADICIONAVA +1 N SEI PQ
                game.game_speed = 20 # 15 - SETA VELOCIDADE COMO PADRÃO
                pygame.time.delay(500) # freeza a tela
                game.playing = False # playing false, logo fecha a tela
                game.death_count += 1 # 15 - ADICIONA MAIS 1 NA CONTAGEM DE MORTE
                break # quebra o loop

    def draw (self, screen): # desenhar na tela
        for obstacle in self.obstacles: # para cada obstaculo
            obstacle.draw(screen) # mostra na tela ele

    def reset_obstacles (self):
        self.obstacles = []