import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, JUMPING, GAME_OVER, DEFAULT_TYPE, GAME_OVER, CLOUD
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
import random
pygame.mixer.init() # iniciei o metodo do mixer
pygame.font.init() # iniciei font
scored = pygame.mixer.Sound('dino_runner/assets/other/Score.wav')
up = pygame.mixer.Sound('dino_runner/assets/other/Up.wav')

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
        self.power_up_manager = PowerUpManager()
        self.destroyed_objects = 0

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
        self.power_up_manager.reset_power_ups()
        self.score = 0 # 15 - SO VAI COLOCAR 0 QUANDO CHAMAR O MÉTODO RUN (handle_events_on_menu)
        self.destroyed_objects = 0
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
            self.game_speed += 1 # 15 - mudei a velocidade pra 1

    
    def update(self):
        user_input = pygame.key.get_pressed() # get tecla pressionada
        self.obstacle_manager.update(self)
        self.player.update(user_input) # da update na tecla presionada
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)


    def draw_background(self): # CHAO
        image_width = BG.get_width() # get largura da imagem
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) # mostra na tela, pos x e y do bg
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg)) #
        if self.x_pos_bg <= -image_width: # animacao aqui n sei
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message_component(
            f"Score: {self.score}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50
        )

        draw_message_component(
            f"Objetos destruidos: {self.destroyed_objects}",
            self.screen,
            pos_x_center=930,
            pos_y_center=70
        )


    # DRAW SCORE
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        self.screen.blit(CLOUD, (500, 100))
        pygame.display.update()
        pygame.display.flip()

    # DRAW POWER UP
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 1)
            if time_to_show >= 0:
                draw_message_component(
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 50
                )
            else:
                pygame.mixer.fadeout(500)
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    # SHOW MENU
    def show_menu (self):
        self.screen.fill((255, 255, 255))
        alturaY = 290
        
        if self.death_count == 0:
            self.screen.blit(JUMPING, (510, 200))
            draw_message_component("Press any key to start", self.screen)
        else:
            draw_message_component("Press any key to restart", self.screen, pos_y_center= alturaY + 100)
            draw_message_component(
                f"Your score: {self.score}",
                self.screen,
                pos_y_center= 200
            )
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen,
                pos_y_center = 230
            )
            draw_message_component(
            f"Objetos destruidos: {self.destroyed_objects}",
            self.screen,
            pos_x_center= 550,
            pos_y_center= 175
        )
            self.screen.blit(GAME_OVER, (370, 130))
            self.screen.blit(ICON, (500, 250))

        pygame.display.update()
        self.handle_events_on_menu()