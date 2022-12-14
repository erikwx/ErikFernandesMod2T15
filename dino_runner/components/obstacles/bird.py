import random

from dino_runner.components.obstacles.obstacles import Obstacle # importa obstacle

listay = [250, 320] # lista com posicaos aleatorias de y

class Bird (Obstacle): # cria bird recebendo obstacle
    def __init__ (self, image): 
        self.type = 0 # type é 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(listay) # random para posição y dele ser aleatória
        self.index = 0

    def draw (self, screen): # metodo de draw
        if self.index >= 9: # se o index for maior ou igual a 9
            self.index = 0 # reseta
        screen.blit (self.image[self.index//5], self.rect) # de 0 a 4 uma imagem, de 5 a 9 outra imagem
        self.index += 1 # adiciona +1 no index a cada iteração