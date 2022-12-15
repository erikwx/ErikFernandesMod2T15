import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, JUMPING, GAME_OVER

pygame.mixer.init() # iniciei o metodo do mixer
pygame.font.init() # iniciei font 
scored = pygame.mixer.Sound('dino_runner/assets/other/Score.wav')

FONT_STYLE = "freesansbold.ttf"
FONT = pygame.font.Font(FONT_STYLE, 22)
BIGFONT = pygame.font.Font(FONT_STYLE, 22)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE) # titulo da janela
        pygame.display.set_icon(ICON) # icone da janela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # resolucao da janela
        self.clock = pygame.time.Clock() # fps do jogo
        self.playing = False # jogando
        self.running = False
        self.game_speed = 20 # velocidade do jogo
        self.x_pos_bg = 0 # posicao x do dino
        self.y_pos_bg = 380 # posição y do dino
        self.score = 0
        self.death_count = 0
        self.player = Dinosaur() # objeto jogador
        self.obstacle_manager =  ObstacleManager() # objeto obstaculo manager

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
            
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True # determina que ta jogando
        self.obstacle_manager.reset_obstacles()
        self.score = 0 # 15 - SO VAI COLOCAR 0 QUANDO CHAMAR O MÉTODO RUN (handle_events_on_menu)
        while self.playing: # enquanto self playing for true
            self.events() # chama os events
            self.update() # chama o update
            self.draw() # e chama os draws

    def events(self): 
        for event in pygame.event.get(): # para cada evento em pygame.event.get
            if event.type == pygame.QUIT: # se clicar em quit
                self.playing = False # false, e fecha o jogo
                self.running = False

    def update_score (self):
        self.score += 1
        if self.score % 100 == 0: #15 -  TOCA O SOM LA DE 100 PONTOS
            scored.play() # toca o som
            self.game_speed += 3 # 15 - mudei a velocidade pra 3
    
    def update(self):
        user_input = pygame.key.get_pressed() # get tecla pressionada
        self.obstacle_manager.update(self)
        self.player.update(user_input) # da update na tecla presionada
        self.update_score()

    def draw(self): # BACKGROUND BRANCO
        self.clock.tick(FPS) # aqui define o fps
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background() # chama o metodo de desenho do bg
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
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

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        text_rect_center = (950, 20)
        self.screen.blit(text, text_rect_center)

    def handle_events_on_menu (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run() # 15 - TA SENDO CHAMADO AQUI


    def show_menu (self):
        self.screen.fill((255, 255, 255))
        larguraX = 380
        alturaY = 290
        
        if self.death_count == 0:
            self.screen.blit(JUMPING, (490, 200))
            font = pygame.font.Font(FONT_STYLE, 30)
            text = font.render("Press any key to start", True, (0, 0, 0))
            text_rect_center = (larguraX, alturaY)
            self.screen.blit(text, text_rect_center)
        else:
            self.screen.blit(ICON, (490, 190))
            self.screen.blit(GAME_OVER, (365, 120))
            font = pygame.font.Font(FONT_STYLE, 30)
            text2 = font.render("Press any key to restart", True, (0, 0, 0))
            text = font.render(f"Total Score: {self.score}   Deaths: {self.death_count}", True, (0, 0, 0))
            text_rect_center = (365, 50)
            text_rect_center2 = (larguraX, alturaY)
            self.screen.blit(text, text_rect_center)
            self.screen.blit(text2, text_rect_center2)

        pygame.display.update()
        self.handle_events_on_menu()