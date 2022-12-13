import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE) # titulo da janela
        pygame.display.set_icon(ICON) # icone da janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # resolucao da janela
        self.clock = pygame.time.Clock() # fps do jogo
        self.playing = False # jogando
        self.game_speed = 20 # velocidade do jogo
        self.x_pos_bg = 0 # posicao x do dino
        self.y_pos_bg = 380 # posição y do dino
        self.player = Dinosaur() # objeto jogador
        
    def run(self):
        # Game loop: events - update - draw
        self.playing = True # determina que ta jogando
        while self.playing: # enquanto self playing for true
            self.events() # chama os events
            self.update() # chama o update
            self.draw() # e chama os draws
        pygame.quit()   # se for false, quit

    def events(self): 
        for event in pygame.event.get(): # para cada evento em pygame.event.get
            if event.type == pygame.QUIT: # se clicar em quit
                self.playing = False # false, e fecha o jogo

    def update(self):
        user_input = pygame.key.get_pressed() # get tecla pressionada
        self.player.update(user_input) # da update na tecla presiionada

    def draw(self): # BACKGROUND BRANCO
        self.clock.tick(FPS) # aqui define o fps
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background() # chama o metodo de desenho do bg
        self.player.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self): # CHAO
        image_width = BG.get_width() # get largura da imagem
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) # mostra na tela, pos x e y do bg
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg)) #
        if self.x_pos_bg <= -image_width: # animacao aqui n sei
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed